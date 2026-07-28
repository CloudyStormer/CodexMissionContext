#!/bin/sh
set -eu

device_id=${1:-}
if [ "$device_id" != A ] && [ "$device_id" != B ]; then
  printf '用法：%s A|B\n' "$0" >&2
  exit 2
fi

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
codex_dir=${CODEX_HOME:-"$HOME/.codex"}
skills_dir=${CODEX_SKILLS_DIR:-"$codex_dir/skills"}
timestamp=$(date '+%Y%m%d-%H%M%S')
backup_root="$codex_dir/sync-backups/$timestamp-$$"

mkdir -p "$skills_dir"

check_source() {
  source_path=$1
  if [ ! -e "$source_path" ]; then
    printf '同步源不存在，停止：%s\n' "$source_path" >&2
    exit 3
  fi
}

check_target() {
  source_path=$1
  target_path=$2
  if [ -L "$target_path" ]; then
    existing_source=$(readlink "$target_path")
    if [ "$existing_source" != "$source_path" ]; then
      printf '发现指向其他位置的链接，停止：%s -> %s\n' "$target_path" "$existing_source" >&2
      exit 3
    fi
  fi
}

install_link() {
  source_path=$1
  target_path=$2
  backup_path=$3

  if [ -L "$target_path" ]; then
    printf '已正确链接：%s\n' "$target_path"
    return
  fi

  if [ -e "$target_path" ]; then
    mkdir -p "$(dirname -- "$backup_path")"
    mv "$target_path" "$backup_path"
    printf '已备份原内容：%s\n' "$backup_path"
  fi

  ln -s "$source_path" "$target_path"
  printf '已建立链接：%s -> %s\n' "$target_path" "$source_path"
}

check_source "$repo_dir/全局技能/aidrama"
check_source "$repo_dir/全局技能/skillnotes"
check_source "$repo_dir/全局规则/AGENTS.md"
check_target "$repo_dir/全局技能/aidrama" "$skills_dir/aidrama"
check_target "$repo_dir/全局技能/skillnotes" "$skills_dir/skillnotes"
check_target "$repo_dir/全局规则/AGENTS.md" "$codex_dir/AGENTS.md"

install_link "$repo_dir/全局技能/aidrama" "$skills_dir/aidrama" "$backup_root/skills/aidrama"
install_link "$repo_dir/全局技能/skillnotes" "$skills_dir/skillnotes" "$backup_root/skills/skillnotes"
install_link "$repo_dir/全局规则/AGENTS.md" "$codex_dir/AGENTS.md" "$backup_root/AGENTS.md"

printf '%s\n' "$device_id" >"$repo_dir/.device-id"

printf '设备 %s 安装完成。请重启 Codex 或新建任务，然后先执行同步脚本。\n' "$device_id"
