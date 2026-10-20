---
name: highball-db-report
description: Use when the user wants to report, file or submit how a game ran to highball-db (gauthierpiarrette/highball-db), a compatibility report for a game played through Proton-ish or Highball on macOS.
---

# highball-db-report

Files a compatibility report on [highball-db](https://github.com/gauthierpiarrette/highball-db) for the user's last
Proton-ish session of a Steam game, through the repo's `report.yml` issue form.

**The `report` label only sticks through the form.** The user has no triage rights on highball-db, so GitHub silently
drops `--label` from `gh issue create` and the API. The form's own `labels: [report]` is applied on submit. Never
create the issue with `gh`; open the prefilled form URL and let the user press Submit.

## 1. Collect the facts

```bash
python3 -I ~/.claude/skills/highball-db-report/collect.py [APPID]
```

No APPID picks the game whose `protonish-run.log` changed last. If the user named a game, find its id with
`grep -l '"name".*<game>' ~/Library/Application\ Support/Steam/steamapps/appmanifest_*.acf`.

`session_end: still running` means the game has not quit; `session_minutes` is then the time since launch. Ask the
user to quit the game and rerun the collector, or to give the length themselves.

Only the values the collector prints go into the report. Never copy other run-log lines or paths: they carry the
Mac user name and the Steam login.

The output covers game and store info, game engine (Unity version, Unreal, GameMaker, Godot), session start/end from
Steam's `content_log`, engine id and name, Proton-ish/HighballKit/highball-db versions, chip, macOS, Steam launch
options and the `log:` lines (sync, Retina, renderer, highball-db notes and recipes, renderer report).

## 2. Ask about performance

One `AskUserQuestion` call:

- **Rating:** `5 — perfect`, `4 — playable, minor issues`, `3 — playable with workarounds`,
  `2 — launches, not playable` (`1 — does not launch` goes through Other).
- **Performance** (multiSelect): smooth throughout, short frame drops, constant low fps or stutter, graphics glitches.
  The question text asks them to add fps, resolution and what they played into through Other or the notes.
- **Session length:** only when `session_minutes` is unknown, 0 or still running; options like ~15 min, ~30 min,
  ~1 h, 2 h+.

Use what they give; do not ask a second round for fps they left out.

## 3. Fill the form fields

Write `highball-report.json` in the scratchpad directory with these keys (the form's field ids) and nothing else:

| Key | Value |
|---|---|
| `title` | `game` (Steam library name) |
| `steam_appid` | `steam_appid` |
| `rating` | the exact rating option text |
| `issues` | one sentence built from the performance answers and their own words; omit for a 5 |
| `renderer` | `dxmt`, `d3dmetal`, `dxvk` or `wined3d`, from the `note: renderer X` log line |
| `chip`, `macos`, `engine` | `chip`, `macos`, `engine_id` |
| `version` | `Not the Highball app: run through Proton-ish <protonish_version> (HighballKit <highballkit_version>, highball-db <highball_db_commit>)` |
| `settings` | environment settings, see below |
| `session` | `Played for <N> min, launched from macOS Steam through Proton-ish.` |
| `notes` | see below |

**`settings`**, one per line:
- `renderer <X> (<source>)`. `log: highball-env: note: renderer X` is always the final renderer; the source is the
  first match of:

  | Log line (after `highball-env: note: `) | Source |
  |---|---|
  | `… only has Direct3D 12, running with …` | `Direct3D 12 take-over` |
  | `highball-db renderer X` | `highball-db` |
  | `highball-db suggests X; your Graphics choice stands` | `Graphics choice` |
  | `CX_GRAPHICS_BACKEND=` in `steam_launch_options` | `launch option` |
  | none of these | `Automatic` |

- `sync msync <on|off> (WINEMSYNC=<n>, from <from>)`, copying `<from>` from `sync: WINEMSYNC=<n> from <from>`.
- `Retina <on|off>`: `video: RetinaMode=1` is on, `0` is off and the default.
- `highball-db fix <id> (<status>)` from a `note: highball-db: <id> (<status>)` line, and each `recipe … applied` line.
- `launch options <value>` when not `none`.
- Last line `no settings changed` when the renderer source is `Automatic`, `<from>` is `default` or `carried-over`,
  Retina is off and launch options are `none`.

**`notes`**, three lines:
1. What the game is: store type when not `game` (demo, playtest) with `full_game`, the first developer, and
   `game_engine` when known, e.g. `This is the demo of Booster Pack Heroes, by zup. Unity 6000.4.10f1 game.`
2. `Ran on <renderer> through the <engine_name> engine (<engine_id>) with Highball's launch environment (HighballKit),
   launched from the macOS Steam client via Proton-ish (https://github.com/MagnusPladsen/Proton-ish).`
3. The user's performance answer: fps, resolution, what they played into, anything that mattered.

## 4. Confirm, then open the form

Show the user every field as a two-column table (field, value) and wait for an explicit yes; this posts publicly.
Then, with the absolute path of the JSON file:

```bash
open "$(python3 -I ~/.claude/skills/highball-db-report/report_url.py /absolute/path/to/highball-report.json)"
```

Tell the user to check the form and press **Submit new issue**. After they say it is submitted, verify:

```bash
gh issue list -R gauthierpiarrette/highball-db --author @me -L 1 --json number,title,labels,url
```

Report the URL and whether `report` is on it. If it is missing, say so; the user cannot add it afterwards.

## Common mistakes

| Mistake | Fix |
|---|---|
| `gh issue create --label report` | Label is dropped silently (#557 and #581 have no label); open the form instead |
| Leaving out `template=report.yml` | Blank issue, no label; use `report_url.py` |
| Guessing session length | Use Steam's `content_log`; ask when it has no end time (Steam may not have written it yet) |
| Reporting the Highball app version as `version` | This is Proton-ish, not the app; use the `Not the Highball app` line |
| Store name in another language | `game` comes from the Steam library manifest; keep it |
