#!/bin/sh
# Builds Proton-ish from the fork checkout, quits the running copy, opens the new one
# and brings its window forward. Usage: run.sh [--no-build]
set -u

repo="${PROTONISH_REPO:-$HOME/git/NotProton}"
app="$repo/out/Proton-ish.app"
binary="Proton-ish.app/Contents/MacOS/NotProtonApp"
log="${TMPDIR:-/tmp}/runapp-build.log"

cd "$repo" 2>/dev/null || { echo "runapp: no checkout at $repo (set PROTONISH_REPO)"; exit 1; }

if [ "${1:-}" != "--no-build" ]; then
  export PATH="$repo/scratch/fontvenv/bin:$PATH"
  echo "runapp: building $(git branch --show-current) @ $(git rev-parse --short HEAD)"
  if ! make app > "$log" 2>&1; then
    echo "runapp: build failed, last lines of $log:"
    tail -20 "$log"
    exit 1
  fi
fi

[ -d "$app" ] || { echo "runapp: $app is missing, run without --no-build"; exit 1; }

# Match on the bundle path: upstream NotProton's executable has the same name
if pgrep -f "$binary" > /dev/null; then
  osascript -e 'tell application id "com.magnuspladsen.protonish" to quit' > /dev/null 2>&1
  tries=0
  while pgrep -f "$binary" > /dev/null && [ "$tries" -lt 20 ]; do
    sleep 0.25
    tries=$((tries + 1))
  done
  pkill -f "$binary" 2> /dev/null
fi

open "$app"

if command -v aerospace > /dev/null; then
  tries=0
  while [ "$tries" -lt 20 ]; do
    window=$(aerospace list-windows --all --format '%{window-id}|%{app-name}' 2> /dev/null \
      | awk -F'|' '$2 == "Proton-ish" { print $1; exit }')
    if [ -n "$window" ]; then
      aerospace focus --window-id "$window"
      break
    fi
    sleep 0.25
    tries=$((tries + 1))
  done
fi

version=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$app/Contents/Info.plist" 2> /dev/null)
echo "runapp: opened Proton-ish ${version:-?} from $app"
