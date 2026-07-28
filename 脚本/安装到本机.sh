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

device_file="$repo_dir/.device-id"
device_file_was_present=0
if [ -f "$device_file" ]; then
  device_file_was_present=1
  existing_device_id=$(sed -n '1p' "$device_file")
  if [ "$existing_device_id" != "$device_id" ]; then
    printf '本仓库已登记为设备 %s，拒绝改写为设备 %s。请先人工核对仓库位置。\n' "$existing_device_id" "$device_id" >&2
    exit 4
  fi
fi

check_source() {
  check_path=$1
  if [ ! -e "$check_path" ]; then
    printf '同步源不存在，停止：%s\n' "$check_path" >&2
    exit 3
  fi
}

check_target() {
  expected_source=$1
  target_link=$2
  if [ -L "$target_link" ]; then
    existing_source=$(readlink "$target_link")
    if [ "$existing_source" != "$expected_source" ]; then
      printf '发现指向其他位置的链接，停止：%s -> %s\n' "$target_link" "$existing_source" >&2
      exit 3
    fi
  fi
}

skill_count=0
for source_path in "$repo_dir"/全局技能/*; do
  if [ ! -d "$source_path" ]; then
    continue
  fi
  skill_name=$(basename -- "$source_path")
  check_source "$source_path/SKILL.md"
  check_target "$source_path" "$skills_dir/$skill_name"
  skill_count=$((skill_count + 1))
done

if [ "$skill_count" -eq 0 ]; then
  printf '全局技能目录中没有可安装的 Skill，停止。\n' >&2
  exit 3
fi

check_source "$repo_dir/全局规则/AGENTS.md"
check_target "$repo_dir/全局规则/AGENTS.md" "$codex_dir/AGENTS.md"

change_log=$(mktemp -t codex-skill-install.XXXXXX)
install_complete=0

rollback_install() {
  exit_status=$?
  trap - EXIT HUP INT TERM
  set +e
  rollback_failed=0
  if [ "$install_complete" -ne 1 ]; then
    while IFS='|' read -r source_path target_path backup_path; do
      if [ -L "$target_path" ] && [ "$(readlink "$target_path")" = "$source_path" ]; then
        rm -f "$target_path" || rollback_failed=1
      fi
      if [ -n "$backup_path" ] && { [ -e "$backup_path" ] || [ -L "$backup_path" ]; }; then
        mv "$backup_path" "$target_path" || rollback_failed=1
      fi
    done <"$change_log"
    if [ "$device_file_was_present" -eq 0 ] && [ -f "$device_file" ]; then
      rm -f "$device_file" || rollback_failed=1
    fi
    printf '安装未完成，已自动恢复安装前状态。\n' >&2
  fi
  rm -f "$change_log" || rollback_failed=1
  if [ "$rollback_failed" -ne 0 ] && [ "$exit_status" -eq 0 ]; then
    exit_status=1
  fi
  exit "$exit_status"
}

trap rollback_install EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
mkdir -p "$skills_dir"

install_link() {
  install_source=$1
  install_target=$2
  install_backup=$3

  if [ -L "$install_target" ]; then
    printf '已正确链接：%s\n' "$install_target"
    return
  fi

  recorded_backup=
  if [ -e "$install_target" ]; then
    mkdir -p "$(dirname -- "$install_backup")"
    recorded_backup=$install_backup
  fi

  printf '%s|%s|%s\n' "$install_source" "$install_target" "$recorded_backup" >>"$change_log"

  if [ -n "$recorded_backup" ]; then
    mv "$install_target" "$install_backup"
    printf '已备份原内容：%s\n' "$install_backup"
  fi

  ln -s "$install_source" "$install_target"
  printf '已建立链接：%s -> %s\n' "$install_target" "$install_source"
}

for source_path in "$repo_dir"/全局技能/*; do
  if [ ! -d "$source_path" ]; then
    continue
  fi
  skill_name=$(basename -- "$source_path")
  install_link "$source_path" "$skills_dir/$skill_name" "$backup_root/skills/$skill_name"
done
install_link "$repo_dir/全局规则/AGENTS.md" "$codex_dir/AGENTS.md" "$backup_root/AGENTS.md"

printf '%s\n' "$device_id" >"$device_file"
install_complete=1

printf '设备 %s 安装完成。请重启 Codex 或新建任务，然后先执行同步脚本。\n' "$device_id"
