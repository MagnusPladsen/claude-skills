---
name: runapp
description: Use when the user types /runapp, or asks to build, run, open, relaunch or try out the Proton-ish macOS app from the ~/git/NotProton checkout. Argument "--no-build" opens the last build without rebuilding.
---

# runapp

Builds the Proton-ish app from `~/git/NotProton` (override with `PROTONISH_REPO`), quits the copy that is running, opens `out/Proton-ish.app` and focuses its window in AeroSpace.

## Run

```bash
bash ~/.claude/skills/runapp/run.sh            # build, then open
bash ~/.claude/skills/runapp/run.sh --no-build # open the last build
```

Pass `--no-build` through when the user gave it. The build takes about a minute; run the command with a timeout of at least 10 minutes.

## Report

- Success: the script's last line (`runapp: opened Proton-ish <version> …`) plus the branch and commit it built.
- Build failure: the tail it prints. Do not retry blindly; read the error.
- If the app opens but **Install** later fails with "cannot write /Applications/Steam.app", tell the user to toggle Proton-ish off and on under System Settings → Privacy & Security → App Management. Each local build is ad-hoc signed, so macOS can treat it as a new app.

## Common mistakes

| Mistake | Fix |
|---|---|
| `pkill NotProtonApp` | Kills upstream NotProton too; the script matches the Proton-ish bundle path |
| Building without `scratch/fontvenv` on PATH | The script adds it; `make app` needs the font tools only when fonts rebuild |
| Saying "it works" after opening | Opening proves the build launches, nothing about games |
