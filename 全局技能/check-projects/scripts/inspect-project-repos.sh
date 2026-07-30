#!/usr/bin/env bash
set -uo pipefail

usage() {
  printf '用法：%s [--fetch] <项目根目录> [项目根目录...]\n' "$0" >&2
  exit 2
}

fetch_remote=0
if [[ ${1:-} == "--fetch" ]]; then
  fetch_remote=1
  shift
fi

[[ $# -gt 0 ]] || usage

declare -a repo_paths=()
overall_status=0

add_repo() {
  local candidate=$1
  local repo_path
  local existing
  repo_path=$(git -C "$candidate" rev-parse --show-toplevel 2>/dev/null) || return 0
  repo_path=$(CDPATH= cd -- "$repo_path" 2>/dev/null && pwd -P) || return 0
  for existing in ${repo_paths[@]+"${repo_paths[@]}"}; do
    [[ $existing == "$repo_path" ]] && return 0
  done
  repo_paths[${#repo_paths[@]}]=$repo_path
}

for project_root in "$@"; do
  if [[ ! -d $project_root ]]; then
    printf 'PROJECT_MISSING\t%s\n' "$project_root"
    overall_status=1
    continue
  fi

  add_repo "$project_root"
  while IFS= read -r -d '' git_marker; do
    add_repo "$(dirname -- "$git_marker")"
  done < <(
    find "$project_root" \
      \( -type d \( -name node_modules -o -name .venv -o -name venv -o -name dist -o -name build -o -name .cache \) -prune \) -o \
      \( -name .git -type d -print0 -prune \) -o \
      \( -name .git -type f -print0 \)
  )
done

if [[ ${#repo_paths[@]} -eq 0 ]]; then
  printf 'NO_REPOSITORIES\n'
  exit 1
fi

printf 'STATE\tREPOSITORY\tBRANCH\tUPSTREAM\tDIRTY\tAHEAD\tBEHIND\tCONFLICTS\tFETCH\n'

for repo_path in "${repo_paths[@]}"; do
  fetch_state=skipped
  if [[ $fetch_remote -eq 1 ]]; then
    if git -C "$repo_path" fetch --all --prune >/dev/null 2>&1; then
      fetch_state=ok
    else
      fetch_state=failed
      overall_status=1
    fi
  fi

  branch=$(git -C "$repo_path" symbolic-ref --quiet --short HEAD 2>/dev/null || printf 'DETACHED')
  upstream=$(git -C "$repo_path" rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || printf '-')
  dirty=$(git -C "$repo_path" status --porcelain=v1 --untracked-files=all 2>/dev/null | awk 'END { print NR + 0 }')
  conflicts=$(git -C "$repo_path" diff --name-only --diff-filter=U 2>/dev/null | awk 'END { print NR + 0 }')
  ahead=-
  behind=-

  if [[ $upstream != "-" ]]; then
    counts=$(git -C "$repo_path" rev-list --left-right --count "HEAD...$upstream" 2>/dev/null || printf '%s' '- -')
    ahead=${counts%%[[:space:]]*}
    behind=${counts##*[[:space:]]}
  fi

  state=ok
  if [[ $branch == DETACHED || $conflicts -gt 0 || $upstream == "-" || $fetch_state == failed ]]; then
    state=blocked
    overall_status=1
  elif [[ $dirty -gt 0 || $ahead -gt 0 || $behind -gt 0 ]]; then
    state=action-needed
  fi

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$state" "$repo_path" "$branch" "$upstream" "$dirty" "$ahead" "$behind" "$conflicts" "$fetch_state"
done

exit "$overall_status"
