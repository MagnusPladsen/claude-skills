"""Print the prefilled highball-db report form URL for a JSON file of form fields.

Usage: python3 -I report_url.py FIELDS.json
Keys are the form's field ids: title, steam_appid, rating, issues, renderer, chip, macos, engine, version,
settings, session, notes. The form carries `labels: [report]`, so an issue submitted from this URL gets the label.
"""

import json
import sys
from urllib.parse import urlencode

FORM = "https://github.com/gauthierpiarrette/highball-db/issues/new"
FIELD_ORDER = ["title", "steam_appid", "rating", "issues", "renderer", "chip", "macos", "engine", "version",
               "settings", "session", "notes"]


def main():
    with open(sys.argv[1], encoding="utf-8") as handle:
        fields = json.load(handle)
    unknown = sorted(set(fields) - set(FIELD_ORDER))
    if unknown:
        print(f"error: not a field of report.yml: {', '.join(unknown)}", file=sys.stderr)
        return 1
    query = [("template", "report.yml")] + [(key, str(fields[key])) for key in FIELD_ORDER if fields.get(key)]
    print(f"{FORM}?{urlencode(query)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
