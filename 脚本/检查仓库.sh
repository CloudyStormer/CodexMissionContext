#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_dir"

required_files="
README.md
AGENTS.md
全局规则/AGENTS.md
项目上下文/项目索引.md
项目上下文/aidrama/项目概览.md
项目上下文/模板/项目概览模板.md
项目上下文/模板/任务记录模板.md
项目上下文/模板/任务语义镜像模板.md
全局技能/aidrama/SKILL.md
全局技能/check-projects/SKILL.md
全局技能/check-projects/agents/openai.yaml
全局技能/check-projects/scripts/inspect-project-repos.sh
全局技能/daily-project-sync/SKILL.md
全局技能/daily-project-sync/agents/openai.yaml
全局技能/skillnotes/SKILL.md
同步清单/项目清单.md
同步清单/任务清单.md
同步清单/完全对齐交接包.md
同步清单/侧边栏布局.md
同步清单/侧边栏布局候选/README.md
同步清单/增量对齐规则.md
同步运行/README.md
设备/A/README.md
设备/A/项目映射.md
设备/A/任务映射.md
设备/A/已应用清单版本.md
设备/B/README.md
设备/B/项目映射.md
设备/B/任务映射.md
设备/B/已应用清单版本.md
设备/B/首次接入指令.md
清单/禁止同步内容.md
脚本/同步上下文.sh
脚本/安装到本机.sh
脚本/检查仓库.sh
"

for file in $required_files; do
  if [ ! -f "$file" ]; then
    printf '缺少必需文件：%s\n' "$file" >&2
    exit 1
  fi
done

alignment_file='同步清单/完全对齐交接包.md'
alignment_line_count=$(grep -Ec '^(projects|tasks)\.(pinned|unpinned)=' "$alignment_file" || true)
if [ "$alignment_line_count" -ne 4 ]; then
  printf '完全对齐交接包的规范化清单必须恰好包含四行，实际为：%s\n' "$alignment_line_count" >&2
  exit 1
fi

declared_alignment_sha=$(sed -n 's/^规范化清单 SHA-256：`\([0-9a-f][0-9a-f]*\)`$/\1/p' "$alignment_file")
if [ "${#declared_alignment_sha}" -ne 64 ]; then
  printf '完全对齐交接包缺少有效的 64 位规范化清单 SHA-256。\n' >&2
  exit 1
fi

if command -v sha256sum >/dev/null 2>&1; then
  actual_alignment_sha=$(grep -E '^(projects|tasks)\.(pinned|unpinned)=' "$alignment_file" | sed 's/\r$//' | sha256sum | awk '{print $1}')
elif command -v shasum >/dev/null 2>&1; then
  actual_alignment_sha=$(grep -E '^(projects|tasks)\.(pinned|unpinned)=' "$alignment_file" | sed 's/\r$//' | shasum -a 256 | awk '{print $1}')
else
  printf '未找到 sha256sum 或 shasum，无法校验完全对齐交接包摘要。\n' >&2
  exit 1
fi

if [ "$actual_alignment_sha" != "$declared_alignment_sha" ]; then
  printf '完全对齐交接包摘要不匹配：声明 %s，实际 %s。\n' "$declared_alignment_sha" "$actual_alignment_sha" >&2
  exit 1
fi

target_project_count=$(sed -n 's/^- 当前目标项目数：`\([0-9][0-9]*\)`$/\1/p' "$alignment_file")
target_task_count=$(sed -n 's/^- 当前目标任务数：`\([0-9][0-9]*\)`$/\1/p' "$alignment_file")
if [ -z "$target_project_count" ] || [ -z "$target_task_count" ]; then
  printf '完全对齐交接包缺少当前目标项目数或任务数。\n' >&2
  exit 1
fi

alignment_project_ids=$(grep -E '^projects\.(pinned|unpinned)=' "$alignment_file" | cut -d= -f2- | tr ',' '\n' | sed '/^$/d')
alignment_task_ids=$(grep -E '^tasks\.(pinned|unpinned)=' "$alignment_file" | cut -d= -f2- | tr ',' '\n' | sed '/^$/d')
actual_project_count=$(printf '%s\n' "$alignment_project_ids" | sed '/^$/d' | wc -l | tr -d ' ')
actual_task_count=$(printf '%s\n' "$alignment_task_ids" | sed '/^$/d' | wc -l | tr -d ' ')
if [ "$actual_project_count" -ne "$target_project_count" ] || [ "$actual_task_count" -ne "$target_task_count" ]; then
  printf '完全对齐交接包目标数量不匹配：项目声明/实际 %s/%s，任务声明/实际 %s/%s。\n' \
    "$target_project_count" "$actual_project_count" "$target_task_count" "$actual_task_count" >&2
  exit 1
fi

duplicate_project_ids=$(printf '%s\n' "$alignment_project_ids" | sort | uniq -d)
duplicate_task_ids=$(printf '%s\n' "$alignment_task_ids" | sort | uniq -d)
if [ -n "$duplicate_project_ids" ] || [ -n "$duplicate_task_ids" ]; then
  printf '完全对齐交接包存在重复逻辑 ID。项目：%s；任务：%s。\n' "$duplicate_project_ids" "$duplicate_task_ids" >&2
  exit 1
fi

project_table_ids=$(awk '
  /^## 必须共同存在的本地项目$/ { in_table=1; next }
  /^设备两端已有显示名称/ { in_table=0 }
  in_table && /^\| `/ {
    line=$0
    sub(/^\| `/, "", line)
    sub(/` \|.*/, "", line)
    print line
  }
' '同步清单/项目清单.md')
task_table_ids=$(sed -n 's/^| `\([^`]*\)` |.*/\1/p' '同步清单/任务清单.md')
if [ "$(printf '%s\n' "$alignment_project_ids" | sort)" != "$(printf '%s\n' "$project_table_ids" | sort)" ]; then
  printf '完全对齐交接包的项目 ID 集合与项目清单不一致。\n' >&2
  exit 1
fi
if [ "$(printf '%s\n' "$alignment_task_ids" | sort)" != "$(printf '%s\n' "$task_table_ids" | sort)" ]; then
  printf '完全对齐交接包的任务 ID 集合与任务清单不一致。\n' >&2
  exit 1
fi

if find . -mindepth 2 -type d -name .git -print | grep -q .; then
  printf '发现嵌套 Git 仓库，本仓库禁止复制项目代码：\n' >&2
  find . -mindepth 2 -type d -name .git -print >&2
  exit 1
fi

if find . -path './.git' -prune -o -type f -size +5M -print | grep -q .; then
  printf '发现超过 5MB 的文件，请确认是否应该进入上下文仓库：\n' >&2
  find . -path './.git' -prune -o -type f -size +5M -print >&2
  exit 1
fi

secret_report=$(mktemp -t codex-mission-context-secrets.XXXXXX)
whitespace_report=$(mktemp -t codex-mission-context-whitespace.XXXXXX)
trap 'rm -f "$secret_report" "$whitespace_report"' EXIT HUP INT TERM

if command -v rg >/dev/null 2>&1; then
  rg -l -i \
    '(BEGIN [A-Z ]*PRIVATE KEY|sk-[A-Za-z0-9_-]{12,}|(api[_-]?key|access[_-]?token|password)[[:space:]]*[:=][[:space:]]*[A-Za-z0-9_./+=-]{12,})' \
    --glob '!.git/**' . >"$secret_report" 2>/dev/null || true
  rg -l '[ \t]+$' --glob '!.git/**' . >"$whitespace_report" 2>/dev/null || true
elif command -v grep >/dev/null 2>&1; then
  grep -RIlE \
    --exclude-dir=.git \
    '(BEGIN [A-Z ]*PRIVATE KEY|sk-[A-Za-z0-9_-]{12,}|(api[_-]?key|access[_-]?token|password)[[:space:]]*[:=][[:space:]]*[A-Za-z0-9_./+=-]{12,})' \
    . >"$secret_report" 2>/dev/null || true
  grep -RIlE --exclude-dir=.git '[[:blank:]]+$' . >"$whitespace_report" 2>/dev/null || true
else
  printf '未找到 rg 或 grep，无法执行敏感信息检查，停止。\n' >&2
  exit 1
fi

if [ -s "$secret_report" ]; then
  printf '发现疑似凭证内容，请检查以下文件：\n' >&2
  sed -n '1,80p' "$secret_report" >&2
  exit 1
fi

if [ -s "$whitespace_report" ]; then
  printf '发现行尾空格，请检查以下文件：\n' >&2
  sed -n '1,80p' "$whitespace_report" >&2
  exit 1
fi

git diff --check
git diff --cached --check
printf '仓库结构、安全边界和 Git 差异检查通过。\n'
