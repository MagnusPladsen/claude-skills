"""Collect the facts for a highball-db report about the last Proton-ish session of a Steam game.

Usage: python3 -I collect.py [APPID]
Without APPID it picks the game whose protonish-run.log changed last. Prints one "key: value" per line.
"""

import glob
import json
import os
import platform
import re
import subprocess
import sys
import urllib.request
from datetime import datetime

STEAM = os.path.expanduser("~/Library/Application Support/Steam")
SUPPORT = os.path.expanduser("~/Library/Application Support/protonish")
RUN_HEADER = "=== notproton run "


def emit(key, value):
    print(f"{key}: {value if value not in (None, '', []) else 'unknown'}")


def read_text(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def pick_run_log(app_id):
    if app_id:
        return os.path.join(STEAM, "steamapps/compatdata", app_id, "protonish-run.log")
    logs = glob.glob(os.path.join(STEAM, "steamapps/compatdata/*/protonish-run.log"))
    return max(logs, key=os.path.getmtime) if logs else None


def last_run_block(log_text):
    start = log_text.rfind(RUN_HEADER)
    return log_text[start:] if start >= 0 else ""


def parse_run_start(block):
    match = re.match(r"=== notproton run \w{3} (\w{3}\s+\d+ [\d:]+) \S+ (\d{4})", block)
    if not match:
        return None
    return datetime.strptime(f"{match.group(1)} {match.group(2)}", "%b %d %H:%M:%S %Y")


def lines_starting(block, *prefixes):
    return [line for line in block.splitlines() if line.startswith(prefixes)]


def first_group(pattern, text):
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1) if match else None


def steam_log_lines(name):
    lines = []
    for suffix in (".previous.txt", ".txt"):
        lines += read_text(os.path.join(STEAM, "logs", name + suffix)).splitlines()
    return lines


def log_time(line):
    match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", line)
    return datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S") if match else None


def find_session(app_id, run_start):
    running_marker = f"AppID {app_id} state changed : "
    started = ended = None
    for line in steam_log_lines("content_log"):
        if running_marker not in line or not log_time(line):
            continue
        is_running = "App Running" in line
        stamp = log_time(line)
        if is_running and (run_start is None or abs((stamp - run_start).total_seconds()) < 120):
            started, ended = stamp, None
        elif started and not is_running and ended is None:
            ended = stamp
    if started and ended is None:
        for line in steam_log_lines("gameprocess_log"):
            stamp = log_time(line)
            if stamp and stamp > started and f"Remove {app_id} from running list" in line:
                ended = stamp
                break
    return started or run_start, ended


def read_manifest(app_id):
    text = read_text(os.path.join(STEAM, "steamapps", f"appmanifest_{app_id}.acf"))
    return first_group(r'"name"\s+"([^"]*)"', text), first_group(r'"installdir"\s+"([^"]*)"', text)


def vdf_tokens(text):
    return re.findall(r'"((?:[^"\\]|\\.)*)"|([{}])', text)


def find_launch_options(app_id):
    paths = glob.glob(os.path.join(STEAM, "userdata/*/config/localconfig.vdf"))
    for path in paths:
        stack, previous = [], None
        for quoted, brace in vdf_tokens(read_text(path)):
            if brace == "{":
                stack.append(previous)
                previous = None
            elif brace == "}":
                stack and stack.pop()
                previous = None
            elif previous is None:
                previous = quoted
            else:
                in_app = len(stack) >= 2 and stack[-1] == app_id and stack[-2].lower() == "apps"
                if in_app and previous == "LaunchOptions":
                    return quoted.replace('\\"', '"')
                previous = None
    return None


def detect_game_engine(install_dir):
    if not install_dir or not os.path.isdir(install_dir):
        return None
    names = os.listdir(install_dir)
    if "UnityPlayer.dll" in names:
        for data_dir in glob.glob(os.path.join(install_dir, "*_Data")):
            with open(os.path.join(data_dir, "globalgamemanagers"), "rb") as handle:
                found = re.search(rb"\d{4}\.\d+\.\d+[abfp]\d+|\d\.\d+\.\d+[abfp]\d+", handle.read(65536))
            if found:
                return f"Unity {found.group().decode()}"
        return "Unity"
    if "Engine" in names or glob.glob(os.path.join(install_dir, "*/Binaries/Win64")):
        return "Unreal Engine"
    if "data.win" in names:
        return "GameMaker"
    if glob.glob(os.path.join(install_dir, "*.pck")):
        return "Godot"
    if "hl2.exe" in names or os.path.isdir(os.path.join(install_dir, "bin")) and "engine.dll" in os.listdir(os.path.join(install_dir, "bin")):
        return "Source"
    return None


def fetch_store_info(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&filters=basic,developers,publishers,genres,release_date&l=english&cc=us"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            entry = json.load(response).get(app_id, {})
    except (OSError, ValueError):
        return {}
    return entry.get("data", {}) if entry.get("success") else {}


def system_value(*command):
    try:
        return subprocess.run(command, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main():
    run_log = pick_run_log(sys.argv[1] if len(sys.argv) > 1 else None)
    block = last_run_block(read_text(run_log)) if run_log else ""
    if not block:
        print(f"error: no Proton-ish run found in {run_log}")
        return 1
    app_id = first_group(r"^STEAM_COMPAT_APP_ID=(\d+)", block) or os.path.basename(os.path.dirname(run_log))
    name, install_name = read_manifest(app_id)
    store = fetch_store_info(app_id)
    run_start = parse_run_start(block)
    started, ended = find_session(app_id, run_start)
    exe = first_group(r"^launch_args=(.+)$", block)
    install_dir = first_group(r"^STEAM_COMPAT_INSTALL_PATH=(.+)$", block) or (
        install_name and os.path.join(STEAM, "steamapps/common", install_name))
    build = json.loads(read_text(os.path.join(SUPPORT, "install-build.json")) or "{}")

    emit("run_log", run_log)
    emit("game", name or store.get("name"))
    emit("steam_appid", app_id)
    emit("store_type", store.get("type"))
    emit("full_game", (store.get("fullgame") or {}).get("name"))
    emit("developers", ", ".join(store.get("developers") or []))
    emit("publishers", ", ".join(store.get("publishers") or []))
    emit("genres", ", ".join(genre["description"] for genre in store.get("genres") or []))
    emit("release_date", (store.get("release_date") or {}).get("date"))
    emit("game_engine", detect_game_engine(install_dir))
    emit("exe", exe)
    is_running = ended is None and bool(exe) and exe in (system_value("ps", "-axo", "command=") or "")
    emit("session_start", started)
    emit("session_end", "still running" if is_running else ended)
    if started and (ended or is_running):
        emit("session_minutes", round(((ended or datetime.now()) - started).total_seconds() / 60))
    else:
        emit("session_minutes", None)
    emit("engine_id", first_group(r"^runner: build (\S+)", block))
    emit("engine_name", first_group(r"^runner: build \S+ \((.+)\) at ", block))
    emit("protonish_version", build.get("version"))
    emit("highballkit_version", first_group(r"HighballKit (\S+)", block))
    emit("highball_db_commit", first_group(r"note: highball-db ([0-9a-f]{7,})$", block))
    emit("chip", system_value("sysctl", "-n", "machdep.cpu.brand_string"))
    emit("macos", platform.mac_ver()[0])
    emit("macos_build", system_value("sw_vers", "-buildVersion"))
    emit("recipe_other_engines", read_text(os.path.join(SUPPORT, "recipe-other-engines")).strip())
    emit("steam_launch_options", find_launch_options(app_id) or "none")
    for line in lines_starting(block, "sync:", "video:", "highball-env:", "recipe", "renderer report:"):
        emit("log", line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
