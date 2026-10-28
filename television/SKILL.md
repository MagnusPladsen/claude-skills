---
name: television
description: Use when working with the tv (television) fuzzy finder - its channels, keybindings, shell integration triggers, or editing channel TOML files under ~/.config/television/.
---

# Television (tv)

**tv** (television) is a fast, hackable TUI fuzzy finder. Config at `~/.config/television/`.

- **Shell integration:** `Ctrl-T` smart autocomplete (context-aware channel), `Ctrl-R` command history
- **Default channel:** `files` — alias `repos` opens `git-repos` channel
- **Config structure:** `config.toml` (global settings/keybindings/shell integration), `cable/*.toml` (channel definitions)

## Key channels & keybindings

| Channel | Purpose | Key bindings |
|---------|---------|-------------|
| `files` | Find files (fd) | Enter=bat, Ctrl-E=nvim, Ctrl-Up=parent dir |
| `procs` | Manage processes | Ctrl-K=kill(SIGKILL), F2=term(SIGTERM), Ctrl-S=stop, Ctrl-C=continue |
| `git-repos` | Browse repos | Enter=select |
| `git-worktrees` | Switch worktrees | Enter=cd, Ctrl-D=remove |
| `git-branch` | Switch branches | Enter=select |
| `git-diff` | Stage/restore files | Enter=select |
| `git-log` | Browse commits | Enter=select |
| `dotfiles` | Edit dotfiles | Enter=edit ($EDITOR) |
| `zoxide` | Directory history | Enter=cd, Ctrl-D=remove |
| `docker-*` | Docker resources | Enter=select |

## Global keybindings (all channels)

| Key | Action |
|-----|--------|
| Ctrl-T | Toggle remote control (channel switcher) |
| Ctrl-X | Toggle action picker |
| Ctrl-O | Toggle preview |
| Ctrl-Y | Copy to clipboard |
| Ctrl-S | Cycle sources |
| Ctrl-R | Reload source |
| Tab/Shift-Tab | Multi-select |

## Shell integration triggers

Commands auto-open relevant channels on `Ctrl-T`: `cd/ls/z` → dirs, `cat/vim/bat/cp/mv/rm` → files, `git checkout/branch/merge` → git-branch, `git add/restore` → git-diff, `nvim/code` → git-repos.

## Editing channels

Channel configs are TOML files in `~/.config/television/cable/`. Each has: `[metadata]`, `[source]`, `[preview]`, `[keybindings]`, and `[actions.*]` sections. Actions use `mode = "execute"` (replace tv) or `mode = "fork"` (return to tv after).
