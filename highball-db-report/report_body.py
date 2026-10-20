"""Print a highball-db report issue body, shaped like a report.yml form submission, from a JSON file of fields.

Usage: python3 -I report_body.py FIELDS.json
Keys are the form's field ids: title, steam_appid, rating, issues, renderer, chip, macos, engine, version,
settings, session, notes. An empty or missing field renders as "_No response_", as the form does.
"""

import json
import sys

FIELDS = [
    ("title", "Game or launcher"),
    ("steam_appid", "Steam AppID (if a Steam game)"),
    ("rating", "Rating"),
    ("issues", "What was not perfect?"),
    ("renderer", "Renderer"),
    ("chip", "Chip"),
    ("macos", "macOS version"),
    ("engine", "Engine id"),
    ("version", "Highball version"),
    ("settings", "Environment settings"),
    ("session", "Session"),
    ("notes", "Notes"),
]
RENDERERS = {"dxmt", "d3dmetal", "dxvk", "wined3d"}
REQUIRED = {"title", "rating", "renderer"}


def main():
    with open(sys.argv[1], encoding="utf-8") as handle:
        values = json.load(handle)
    known = {key for key, _ in FIELDS}
    problems = [f"not a field of report.yml: {key}" for key in sorted(set(values) - known)]
    problems += [f"missing: {key}" for key in sorted(REQUIRED) if not values.get(key)]
    if values.get("renderer") and values["renderer"] not in RENDERERS:
        problems.append(f"renderer must be one of {', '.join(sorted(RENDERERS))}")
    if problems:
        print("error: " + "; ".join(problems), file=sys.stderr)
        return 1
    sections = [f"### {label}\n\n{str(values.get(key) or '').strip() or '_No response_'}" for key, label in FIELDS]
    print("\n\n".join(sections))
    return 0


if __name__ == "__main__":
    sys.exit(main())
