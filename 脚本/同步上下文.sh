#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
mode=${1:-}
message=${2:-}
device_id=A

if [ -z "${GIT_SSH_COMMAND:-}" ]; then
  GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=15 -o ConnectionAttempts=1 -o ServerAliveInterval=10 -o ServerAliveCountMax=2'
  export GIT_SSH_COMMAND
fi

if [ -f "$repo_dir/.device-id" ]; then
  device_id=$(sed -n '1p' "$repo_dir/.device-id")
fi

current_branch=$(git -C "$repo_dir" symbolic-ref --quiet --short HEAD 2>/dev/null || printf 'main')

remote_branch_exists() {
  git -C "$repo_dir" show-ref --verify --quiet "refs/remotes/origin/$current_branch"
}

case "$mode" in
  开始)
    if [ -n "$(git -C "$repo_dir" status --porcelain)" ]; then
      printf '上下文仓库存在未提交修改。请先完成或处理上一次任务，避免覆盖另一台设备。\n' >&2
      git -C "$repo_dir" status --short >&2
      exit 2
    fi
    git -C "$repo_dir" fetch origin
    if remote_branch_exists; then
      git -C "$repo_dir" merge --ff-only "origin/$current_branch"
    fi
    printf '设备 %s 已取得上下文仓库最新版本。\n' "$device_id"
    ;;
  结束)
    if [ -z "$message" ]; then
      printf '用法：%s 结束 "项目名：任务简述"\n' "$0" >&2
      exit 2
    fi
    "$repo_dir/脚本/检查仓库.sh"
    git -C "$repo_dir" add -- \
      .gitignore README.md AGENTS.md 全局规则 全局技能 项目上下文 历史任务 同步清单 设备 清单 脚本
    git -C "$repo_dir" diff --cached --check
    if ! git -C "$repo_dir" diff --quiet; then
      printf '仍有未暂存的已跟踪修改，停止提交，请先确认：\n' >&2
      git -C "$repo_dir" diff --name-only >&2
      exit 3
    fi
    untracked_files=$(git -C "$repo_dir" ls-files --others --exclude-standard)
    if [ -n "$untracked_files" ]; then
      printf '仍有未纳入同步范围的新文件，停止提交，请先确认：\n%s\n' "$untracked_files" >&2
      exit 3
    fi
    if git -C "$repo_dir" diff --cached --quiet; then
      printf '没有需要同步的新上下文。\n'
      exit 0
    fi
    git -C "$repo_dir" commit -m "context($device_id): $message"
    git -C "$repo_dir" fetch origin
    if remote_branch_exists; then
      git -C "$repo_dir" rebase "origin/$current_branch"
    fi
    git -C "$repo_dir" push -u origin "$current_branch"
    printf '设备 %s 的最新上下文已经提交并推送：%s\n' "$device_id" "$message"
    ;;
  *)
    printf '用法：%s 开始 | %s 结束 "项目名：任务简述"\n' "$0" "$0" >&2
    exit 2
    ;;
esac
