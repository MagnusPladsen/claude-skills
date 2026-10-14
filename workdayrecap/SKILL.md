---
name: workdayrecap
description: List the Azure DevOps Boards work item ids I have committed on in the current repo, as one line "#25, #30, #31", or one line per day when the period covers several days. Use for timesheets, standups, or "which tasks did I touch". Optional argument limits the period (today, yesterday, a date, "8 and 9 October", "since 2026-10-01"); no argument means all time.
---

# Workday recap

Print the Azure Boards work item ids (not PR numbers) the user has commits on.

## Steps

1. Map the argument to `git` `--since` / `--until` values:
   - none → all time (no arguments)
   - `today` → since `midnight`
   - `yesterday` → since `yesterday.midnight`, until `midnight`
   - `this week` → since `last monday` (`midnight` if today is Monday)
   - a date or `since <date>` → since that date (`YYYY-MM-DD`; convert `DD.MM` to the current year)
   - several named days or an explicit range (`8 and 9 October`, `from 6th to 9th`) → since the
     first day, until **the day after the last** (`--until` is exclusive, so 8 and 9 October is
     `2026-10-08` to `2026-10-10`)
2. Decide the shape:
   - **one line per day** when the period covers more than one day: several named days, an explicit
     range, or `this week`. Pass `--by-day`.
   - **one line** for a single day, or for no argument (all time) — a per-day breakdown of all time
     is useless.
3. Run from the repo root: `~/.claude/skills/workdayrecap/recap.sh ["<since>"] ["<until>"] [--by-day]`
4. Reply with the output exactly as printed. Nothing else unless step 5 finds a problem.
   - one line: `#25, #30, #31`
   - per day, oldest first:
     ```
     2026-10-08  #84, #93, #108
     2026-10-09  #109, #112
     ```
5. Optional sanity check when `az` is logged in: confirm the ids exist on the board. Take `<org>` and
   `<project>` from the `origin` remote (`https://dev.azure.com/<org>/<project>/_git/<repo>` or
   `git@ssh.dev.azure.com:v3/<org>/<project>/<repo>`), then run
   `az boards query --org https://dev.azure.com/<org> --project <project> --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.Id] IN (<ids>)"`.
   Skip this when the remote is not Azure DevOps. Mention any id the board does not know.

## Rules

- Ids come only from commit scopes `type(#88)` / `type(88)` and Azure squash merges `Merged PR 39: #88: ...` (take 88, never 39).
- Skip `pull request #N` and old `issue #N` refs: those are GitHub/Bitbucket numbers, not Azure Boards.
- Skip Jira-style keys (`ABC-123`): they are not Azure Boards ids.
- An id appears on **every** day it was committed on, so the same id may repeat across days. That is
  correct — do not deduplicate across the range in `--by-day` mode.
- A day with no matching commits is omitted entirely rather than printed empty.
- An empty result means no matching commits in the period; say so in one line.
