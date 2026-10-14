# /todo

Manage shared project TODOs across the repository.

## TODO File Location

`./.claude/TODO.md`

## Commands

- `/todo` — Show current TODOs
- `/todo add <description>` — Add a new TODO
- `/todo done <number>` — Mark a TODO as complete
- `/todo clear` — Clear completed items

## File Format

```markdown
# Project TODOs

## High Priority
- [ ] Task description (added: YYYY-MM-DD)

## Medium Priority
- [ ] Task description (added: YYYY-MM-DD)

## Low Priority / Future
- [ ] Task description (added: YYYY-MM-DD)

## Completed
- [x] Task description (completed: YYYY-MM-DD)
```

## Rules

- Always add dates when creating or completing TODOs.
- Keep TODOs concise and repo-relevant.
- Use the shared file for cross-repo work; feature-specific notes can still live closer to the relevant area if needed.
