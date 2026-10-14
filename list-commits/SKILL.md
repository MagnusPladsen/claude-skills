# /list-commits

Show commits ahead of the current branch upstream and optionally show recent history.

## Instructions

1. Check whether the repo has a configured remote with `git remote get-url origin`.
2. Show commits ahead of upstream:

```bash
git log @{upstream}..HEAD --format="%h - %s" --no-merges
```

3. Show branch status with `git status -sb`.
4. If there are no commits ahead, say so clearly.
5. Optionally show recent full history if the user asks.

## Notes

- Use `@{upstream}`, not a hardcoded branch name.
- Handle missing upstream or missing remote gracefully.
