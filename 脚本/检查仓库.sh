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
全局技能/aidrama/SKILL.md
全局技能/check-projects/SKILL.md
全局技能/check-projects/agents/openai.yaml
全局技能/check-projects/scripts/inspect-project-repos.sh
全局技能/daily-project-sync/SKILL.md
全局技能/daily-project-sync/agents/openai.yaml
全局技能/skillnotes/SKILL.md
同步清单/项目清单.md
同步清单/任务清单.md
同步清单/增量对齐规则.md
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
