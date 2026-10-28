# claude-skills

Magnus Pladsen kit: personal global Claude Code skills, checked out at `~/.claude/skills/` as a
submodule of the [dotfiles](https://github.com/MagnusPladsen/dotfiles) repo.

## Install

### Easiest: paste this into Claude Code

```text
Install my global Claude Code skills from the public GitHub repo MagnusPladsen/claude-skills into ~/.claude/skills.

1. If ~/.claude/skills is already a git repo or a submodule of my dotfiles repo (~/.dotfiles, used as `git --git-dir=$HOME/.dotfiles --work-tree=$HOME`), just pull or run `submodule update --init .claude/skills` and stop there.
2. If ~/.claude/skills does not exist, clone https://github.com/MagnusPladsen/claude-skills.git there.
3. If it exists with other content, don't overwrite anything: back it up to ~/.claude/skills.bak-<timestamp>, clone https://github.com/MagnusPladsen/claude-skills.git to a temp dir, move its .git into ~/.claude/skills, then run `git status`. List any tracked files that differ from what was already on disk and ask me before running `git checkout -- .` to take the repo's version.
4. Never push, and never delete the backup.
5. When done, list the skills now in ~/.claude/skills and tell me to start a new session so they load.
```

### Manual

```bash
# Fresh machine with the dotfiles repo
dotfiles submodule update --init .claude/skills

# Standalone, when ~/.claude/skills does not exist yet
git clone https://github.com/MagnusPladsen/claude-skills.git ~/.claude/skills
```

Update later with `git -C ~/.claude/skills pull`. Skills load at session start.

## Git and tickets

| Skill | Purpose |
|-------|---------|
| `new-issue` | Start work on a ticket: fetch it, create the branch, plan |
| `commit` | Contextual commit with the ticket reference from the branch |
| `list-commits` | Commits ahead of upstream plus branch status |
| `create-pr` | Full PR workflow with quality checks, for GitHub, Azure DevOps and Bitbucket |
| `pr-description` | Ready-to-paste PR description on the clipboard |
| `changelog` | Generate or update a CHANGELOG from git history |
| `workdayrecap` | Azure Boards work item ids committed on in the current repo, as one line |

## Engineering workflow

| Skill | Purpose |
|-------|---------|
| `planning-with-issues` | Plan mode with GitHub issue integration and three review rounds |
| `debug` | Structured debugging: reproduce, isolate, fix, verify |
| `refactor` | Guided refactoring with tests before and after |
| `review` | Review the current diff or a PR against project conventions |
| `test` | Write and run tests for specified code |
| `test-run` | Interactive manual test run published as a Claude artifact, results read back |
| `document` | Generate or update documentation from code |
| `onboard` | Project overview for new developers |
| `todo` | Shared project TODOs in `./.claude/TODO.md` |

## Stack-specific and misc

| Skill | Purpose |
|-------|---------|
| `add-migration` | EF Core migration workflow (.NET) |
| `validate-architecture` | Clean architecture validation (.NET) |
| `frontend-design` | Distinctive, production-grade frontend interfaces |
| `dance` | ASCII dance party when something works |
| `runapp` | Build and open the Proton-ish app from `~/git/NotProton` (`--no-build` reopens the last build) |
| `highball-db-report` | Report a Proton-ish game session to highball-db as a `report.yml`-shaped issue created with `gh` |

Other skills in this directory (Superset, synced) are installed by their own tooling and
listed in `.gitignore`.
