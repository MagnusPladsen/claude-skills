#!/usr/bin/env bash
# Prints the Azure Boards work item ids the user has committed on in the current repo.
#
#   default      one line:  #25, #30, #31
#   --by-day     one line per day, oldest first:
#                  2026-10-08  #84, #93, #108
#                  2026-10-09  #109, #112
#
# Usage: recap.sh [since] [until] [--by-day]
#   recap.sh
#   recap.sh midnight
#   recap.sh yesterday.midnight midnight
#   recap.sh 2026-10-08 2026-10-10 --by-day
set -uo pipefail

by_day=0
positional=()
for arg in "$@"; do
  case "$arg" in
    --by-day) by_day=1 ;;
    *) positional+=("$arg") ;;
  esac
done

range_args=()
[[ -n "${positional[0]:-}" ]] && range_args+=(--since="${positional[0]}")
[[ -n "${positional[1]:-}" ]] && range_args+=(--until="${positional[1]}")

# Azure Repos merge commits are authored as "Magnus", local commits as "Magnus Pladsen".
# Ids come only from conventional-commit scopes, type(#88) or type(88), and from Azure
# squash merges, "Merged PR 39: #88: ...". The PR number (39) is never taken.
# Older "pull request #N" and "issue #N" refs are GitHub/Bitbucket numbers and are skipped.
SCOPE_RE='^[a-z]+\(#?[0-9]+\)|^Merged PR [0-9]+: #[0-9]+'

if [[ "$by_day" -eq 0 ]]; then
  git log --all -i --author='magnus' ${range_args[@]+"${range_args[@]}"} --format='%s' \
    | grep -oE "$SCOPE_RE" \
    | grep -oE '#?[0-9]+\)?$' \
    | tr -d '#)' \
    | sort -n -u \
    | sed 's/^/#/' \
    | paste -sd, - \
    | sed 's/,/, /g'
  exit 0
fi

# Per day. %ad with --date=short gives YYYY-MM-DD, so the day is the first field and the
# subject is everything after it.
git log --all -i --author='magnus' ${range_args[@]+"${range_args[@]}"} \
      --date=short --format='%ad %s' \
  | while IFS=' ' read -r day subject; do
      id=$(printf '%s' "$subject" \
            | grep -oE "$SCOPE_RE" \
            | grep -oE '#?[0-9]+\)?$' \
            | tr -d '#)') || true
      [[ -n "$id" ]] && printf '%s %s\n' "$day" "$id"
    done \
  | sort -u -k1,1 -k2,2n \
  | awk '{
      if ($1 != day) {
        if (day != "") printf "\n"
        printf "%s  ", $1
        day = $1; sep = ""
      }
      printf "%s#%s", sep, $2
      sep = ", "
    }
    END { if (day != "") printf "\n" }'
