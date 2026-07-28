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
host_os=$(uname -s)
case "$host_os" in
  MINGW*|MSYS*|CYGWIN*) windows_host=1 ;;
  *) windows_host=0 ;;
esac

global_rules_source="$repo_dir/全局规则/AGENTS.md"
windows_entry_source="$repo_dir/全局规则/AGENTS-Windows入口.md"

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
    if ! same_target "$expected_source" "$target_link"; then
      existing_source=$(readlink "$target_link" 2>/dev/null || printf '未知目标')
      printf '发现指向其他位置的链接，停止：%s -> %s\n' "$target_link" "$existing_source" >&2
      exit 3
    fi
  fi
}

same_target() {
  expected_source=$1
  target_link=$2
  if [ -d "$expected_source" ] && [ -d "$target_link" ]; then
    expected_physical=$(CDPATH= cd -- "$expected_source" 2>/dev/null && pwd -P)
    target_physical=$(CDPATH= cd -- "$target_link" 2>/dev/null && pwd -P)
    [ -n "$expected_physical" ] && [ "$target_physical" = "$expected_physical" ]
    return
  fi
  existing_source=$(readlink "$target_link" 2>/dev/null || true)
  [ "$existing_source" = "$expected_source" ]
}

windows_link_type() {
  target_link=$1
  target_windows=$(cygpath -aw "$target_link")
  MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -NonInteractive -Command \
    '& { param([string]$Path) (Get-Item -Force -LiteralPath $Path -ErrorAction Stop).LinkType }' \
    "$target_windows" | tr -d '\r'
}

create_windows_junction() {
  source_path=$1
  target_link=$2
  source_windows=$(cygpath -aw "$source_path")
  target_windows=$(cygpath -aw "$target_link")
  MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -NonInteractive -Command \
    '& { param([string]$Link,[string]$Target) $ErrorActionPreference = "Stop"; New-Item -ItemType Junction -Path $Link -Target $Target | Out-Null }' \
    "$target_windows" "$source_windows"
}

remove_windows_junction() {
  target_link=$1
  target_windows=$(cygpath -aw "$target_link")
  MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -NonInteractive -Command \
    '& { param([string]$Path) $ErrorActionPreference = "Stop"; $item = Get-Item -Force -LiteralPath $Path; if ($item.LinkType -ne "Junction") { throw "目标不是 Junction，拒绝删除" }; Remove-Item -Force -LiteralPath $Path }' \
    "$target_windows"
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

check_source "$global_rules_source"
if [ "$windows_host" -eq 1 ]; then
  check_source "$windows_entry_source"
  if ! command -v cygpath >/dev/null 2>&1 || ! command -v powershell.exe >/dev/null 2>&1; then
    printf 'Windows 安装需要 Git Bash 的 cygpath 和 PowerShell，停止。\n' >&2
    exit 3
  fi
  if [ -L "$codex_dir/AGENTS.md" ]; then
    if ! same_target "$global_rules_source" "$codex_dir/AGENTS.md" &&
       ! same_target "$windows_entry_source" "$codex_dir/AGENTS.md"; then
      existing_source=$(readlink "$codex_dir/AGENTS.md" 2>/dev/null || printf '未知目标')
      printf '发现指向其他位置的链接，停止：%s -> %s\n' "$codex_dir/AGENTS.md" "$existing_source" >&2
      exit 3
    fi
  fi
else
  check_target "$global_rules_source" "$codex_dir/AGENTS.md"
fi

change_log=$(mktemp -t codex-skill-install.XXXXXX)
install_complete=0

rollback_install() {
  exit_status=$?
  trap - EXIT HUP INT TERM
  set +e
  rollback_failed=0
  if [ "$install_complete" -ne 1 ]; then
    while IFS='|' read -r change_kind source_path target_path backup_path; do
      case "$change_kind" in
        junction)
          if [ -L "$target_path" ] && same_target "$source_path" "$target_path"; then
            remove_windows_junction "$target_path" || rollback_failed=1
          fi
          ;;
        symlink)
          if [ -L "$target_path" ] && same_target "$source_path" "$target_path"; then
            rm -f "$target_path" || rollback_failed=1
          fi
          ;;
        bootstrap)
          if [ -e "$target_path" ] && [ ! -L "$target_path" ]; then
            rm -f "$target_path" || rollback_failed=1
          fi
          ;;
      esac
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
    if ! same_target "$install_source" "$install_target"; then
      printf '链接目标在安装期间发生变化，停止：%s\n' "$install_target" >&2
      return 1
    fi
    printf '已正确链接：%s\n' "$install_target"
    return
  fi

  recorded_backup=
  if [ -e "$install_target" ]; then
    mkdir -p "$(dirname -- "$install_backup")"
    recorded_backup=$install_backup
  fi

  if [ "$windows_host" -eq 1 ]; then
    change_kind=junction
  else
    change_kind=symlink
  fi
  printf '%s|%s|%s|%s\n' "$change_kind" "$install_source" "$install_target" "$recorded_backup" >>"$change_log"

  if [ -n "$recorded_backup" ]; then
    mv "$install_target" "$install_backup"
    printf '已备份原内容：%s\n' "$install_backup"
  fi

  if [ "$windows_host" -eq 1 ]; then
    create_windows_junction "$install_source" "$install_target"
    if [ "$(windows_link_type "$install_target")" != Junction ]; then
      printf 'Windows 目录入口不是 Junction，停止：%s\n' "$install_target" >&2
      return 1
    fi
  else
    ln -s "$install_source" "$install_target"
  fi
  if [ ! -L "$install_target" ] || ! same_target "$install_source" "$install_target"; then
    printf '链接后置验证失败，停止：%s\n' "$install_target" >&2
    return 1
  fi
  printf '已建立链接：%s -> %s\n' "$install_target" "$install_source"
}

install_bootstrap() {
  install_source=$1
  install_target=$2
  install_backup=$3

  if [ -L "$install_target" ]; then
    if same_target "$global_rules_source" "$install_target" ||
       same_target "$install_source" "$install_target"; then
      printf '已正确链接：%s\n' "$install_target"
      return
    fi
    printf '全局规则入口链接在安装期间发生变化，停止：%s\n' "$install_target" >&2
    return 1
  fi

  if [ -f "$install_target" ] && cmp -s "$install_source" "$install_target"; then
    printf '已正确安装 Windows 全局规则入口：%s\n' "$install_target"
    return
  fi

  recorded_backup=
  if [ -e "$install_target" ]; then
    mkdir -p "$(dirname -- "$install_backup")"
    recorded_backup=$install_backup
  fi
  printf 'bootstrap|%s|%s|%s\n' "$install_source" "$install_target" "$recorded_backup" >>"$change_log"

  if [ -n "$recorded_backup" ]; then
    mv "$install_target" "$install_backup"
    printf '已备份原内容：%s\n' "$install_backup"
  fi

  cp "$install_source" "$install_target"
  if [ -L "$install_target" ] || ! cmp -s "$install_source" "$install_target"; then
    printf 'Windows 全局规则入口后置验证失败，停止：%s\n' "$install_target" >&2
    return 1
  fi
  printf '已安装 Windows 全局规则入口：%s\n' "$install_target"
}

for source_path in "$repo_dir"/全局技能/*; do
  if [ ! -d "$source_path" ]; then
    continue
  fi
  skill_name=$(basename -- "$source_path")
  install_link "$source_path" "$skills_dir/$skill_name" "$backup_root/skills/$skill_name"
done
if [ "$windows_host" -eq 1 ]; then
  install_bootstrap "$windows_entry_source" "$codex_dir/AGENTS.md" "$backup_root/AGENTS.md"
else
  install_link "$global_rules_source" "$codex_dir/AGENTS.md" "$backup_root/AGENTS.md"
fi

printf '%s\n' "$device_id" >"$device_file"
install_complete=1

printf '设备 %s 安装完成。请重启 Codex 或新建任务，然后先执行同步脚本。\n' "$device_id"
