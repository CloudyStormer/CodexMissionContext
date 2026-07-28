#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
mode=${1:-}
message=${2:-}

if [ -z "${GIT_SSH_COMMAND:-}" ]; then
  GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=15 -o ConnectionAttempts=1 -o ServerAliveInterval=10 -o ServerAliveCountMax=2'
  export GIT_SSH_COMMAND
fi

if [ ! -f "$repo_dir/.device-id" ]; then
  printf '缺少设备标识。请先运行：%s/脚本/安装到本机.sh A|B\n' "$repo_dir" >&2
  exit 2
fi

device_id=$(sed -n '1p' "$repo_dir/.device-id")
case "$device_id" in
  A|B) ;;
  *)
    printf '设备标识无效：%s\n' "$device_id" >&2
    exit 2
    ;;
esac

current_branch=$(git -C "$repo_dir" symbolic-ref --quiet --short HEAD 2>/dev/null || true)
if [ -z "$current_branch" ]; then
  printf '当前处于 detached HEAD，停止同步。请先切换到明确分支。\n' >&2
  exit 2
fi

remote_branch_exists() {
  git -C "$repo_dir" show-ref --verify --quiet "refs/remotes/origin/$current_branch"
}

reject_local_removals() {
  removed_paths=$(
    {
      git -C "$repo_dir" diff --name-status --diff-filter=DR
      git -C "$repo_dir" diff --cached --name-status --diff-filter=DR
    } | sort -u
  )
  if [ -n "$removed_paths" ]; then
    printf '检测到删除或重命名，自动同步已停止。为防止跨设备误删，本脚本只接受新增和修改：\n%s\n' "$removed_paths" >&2
    exit 4
  fi
}

reject_incoming_removals() {
  if ! remote_branch_exists; then
    return
  fi
  merge_base=$(git -C "$repo_dir" merge-base HEAD "origin/$current_branch")
  incoming_removals=$(git -C "$repo_dir" diff --name-status --diff-filter=DR "$merge_base" "origin/$current_branch")
  if [ -n "$incoming_removals" ]; then
    printf '远端包含删除或重命名，自动同步已停止。请人工核对，不能让统一过程传播删除：\n%s\n' "$incoming_removals" >&2
    exit 4
  fi
}

reject_outgoing_removals() {
  if ! remote_branch_exists; then
    return
  fi
  merge_base=$(git -C "$repo_dir" merge-base HEAD "origin/$current_branch")
  outgoing_removals=$(git -C "$repo_dir" diff --name-status --diff-filter=DR "$merge_base" HEAD)
  if [ -n "$outgoing_removals" ]; then
    printf '未推送提交中包含删除或重命名，自动推送已停止。请人工核对：\n%s\n' "$outgoing_removals" >&2
    exit 4
  fi
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
      reject_incoming_removals
      git -C "$repo_dir" merge --ff-only "origin/$current_branch"
    fi
    printf '设备 %s 已取得上下文仓库最新版本。\n' "$device_id"
    ;;
  结束)
    if [ -z "$message" ]; then
      printf '用法：%s 结束 "项目名：任务简述"\n' "$0" >&2
      exit 2
    fi
    reject_local_removals
    "$repo_dir/脚本/检查仓库.sh"
    git -C "$repo_dir" add -- \
      .gitignore README.md AGENTS.md 全局规则 全局技能 项目上下文 历史任务 同步清单 设备 清单 脚本
    reject_local_removals
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
    if ! git -C "$repo_dir" diff --cached --quiet; then
      git -C "$repo_dir" commit -m "context($device_id): $message"
    fi

    git -C "$repo_dir" fetch origin
    if remote_branch_exists; then
      reject_incoming_removals
      if ! git -C "$repo_dir" rebase "origin/$current_branch"; then
        git -C "$repo_dir" rebase --abort >/dev/null 2>&1 || true
        printf '远端更新与本地提交冲突，已中止 rebase 并恢复本地分支。请人工解决后重试。\n' >&2
        exit 5
      fi
      reject_outgoing_removals
      ahead_count=$(git -C "$repo_dir" rev-list --count "origin/$current_branch..HEAD")
    elif git -C "$repo_dir" rev-parse --verify HEAD >/dev/null 2>&1; then
      ahead_count=$(git -C "$repo_dir" rev-list --count HEAD)
    else
      ahead_count=0
    fi

    if [ "$ahead_count" -eq 0 ]; then
      printf '没有需要推送的新上下文，远端已是最新状态。\n'
      exit 0
    fi

    git -C "$repo_dir" push -u origin "$current_branch"
    printf '设备 %s 的最新上下文已经提交并推送：%s\n' "$device_id" "$message"
    ;;
  *)
    printf '用法：%s 开始 | %s 结束 "项目名：任务简述"\n' "$0" "$0" >&2
    exit 2
    ;;
esac
