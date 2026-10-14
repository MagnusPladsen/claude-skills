---
name: pr-description
description: Use when you want a ready-to-paste pull request description for the current branch on the clipboard, and are opening the PR yourself (GitHub, Azure Repos, Bitbucket or any other host).
---

<!-- magnus-pladsen-kit -->

# /pr-description

Compose a PR description for the current branch and copy it to the clipboard.

Read-only. This skill never commits, pushes, creates, updates, or merges a PR. For the full
workflow with checks and review, use `/create-pr` instead.

## Steps

### 1. Resolve the branch and its target

```bash
BRANCH=$(git branch --show-current)
DEFAULT=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
DEFAULT=${DEFAULT:-main}
TARGET=$DEFAULT
for b in dev develop; do
  if [ "$BRANCH" != "$b" ] && git show-ref --quiet "refs/remotes/origin/$b"; then TARGET=$b; break; fi
done
git fetch origin "$TARGET" --quiet
```

The target is the integration branch (`dev` or `develop`) when the repo has one, otherwise the
default branch. If the user names a target, use that instead.

Stop and say so if the branch is the default branch, or if `git log origin/$TARGET..HEAD` is empty.

### 2. Read the change

```bash
git log origin/$TARGET..HEAD --oneline --no-merges
git diff origin/$TARGET...HEAD --stat
```

Use `...` (three dots), not `..`. It diffs from the merge base, so a branch that has merged
`$TARGET` in does not report that merge's files as its own changes.

Read the actual diff for anything the commit subjects do not explain. Classify the change by the
repo's own top-level areas (for example frontend, backend, full stack, docs/config); in a single-area
repo, drop the classification.

### 3. Add ticket context

Find a ticket reference in the branch name:

- **Jira-style key** (`PROJ-123`): fetch the title with the Atlassian MCP when it is available.
- **Number** (`1234`, `1234-short-name`, `feature/1234`): read the tracker from the `origin` remote.
  - Azure DevOps (`dev.azure.com/<org>/<project>/...` or `ssh.dev.azure.com:v3/<org>/<project>/...`):
    `az boards work-item show --id "$ID" --org "https://dev.azure.com/<org>" --query 'fields."System.Title"' -o tsv`.
    Link: `https://dev.azure.com/<org>/<project>/_workitems/edit/<id>`.
  - GitHub: `gh issue view "$ID" --json title,url`.

Skip this silently if the CLI or MCP is missing or not logged in. Never block on it, and never
invent a summary.

### 4. Compose

```markdown
## Summary

**Ticket:** [<ref>](<link>) - <summary>

### Changes
- <what changed and why, one line each>

### Area
- <area, when the repo has more than one>

## Test plan
- [ ] <checks that were actually run, with their results>
```

Drop the `**Ticket:**` line entirely when the branch carries no reference. Never leave a placeholder
in place. Drop `### Area` in a single-area repo.

Describe the change, not the session: no narration of what you tried, no file inventories, no
tool output. A reviewer reads this to know what to look at and what to trust.

### 5. Copy it

```bash
printf '%s' "$DESCRIPTION" | pbcopy && echo "Copied to clipboard."
```

Fall back to `wl-copy` or `xclip -selection clipboard` off macOS. If none exist, print the
description and say that the clipboard step was skipped.

Print the description in the response as well, so it survives a clipboard overwrite.

## Common mistakes

| Mistake | Fix |
|---|---|
| `git diff origin/dev..HEAD` on a branch that merged `dev` | Use `...` so merged-in files are not reported as your changes |
| Test plan lists checks that were never run | List only what ran, with the result; write "not run" for the rest |
| Blocking because a tracker CLI is not logged in | Compose without the ticket line and note it |
| Creating or updating the PR | Out of scope; this skill only fills the clipboard |
