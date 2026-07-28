#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_dir"

required_files="
README.md
AGENTS.md
全局规则/AGENTS.md
项目上下文/项目索引.md
项目上下文/模板/项目概览模板.md
项目上下文/模板/任务记录模板.md
全局技能/aidrama/SKILL.md
全局技能/skillnotes/SKILL.md
同步清单/项目清单.md
同步清单/任务清单.md
同步清单/增量对齐规则.md
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

if command -v rg >/dev/null 2>&1; then
  secret_report=$(mktemp -t codex-mission-context-secrets.XXXXXX)
  trap 'rm -f "$secret_report"' EXIT HUP INT TERM
  rg -l -i \
    '(BEGIN [A-Z ]*PRIVATE KEY|sk-[A-Za-z0-9_-]{12,}|(api[_-]?key|access[_-]?token|password)[[:space:]]*[:=][[:space:]]*[A-Za-z0-9_./+=-]{12,})' \
    --glob '!.git/**' . >"$secret_report" 2>/dev/null || true
  if [ -s "$secret_report" ]; then
    printf '发现疑似凭证内容，请检查以下文件：\n' >&2
    sed -n '1,80p' "$secret_report" >&2
    exit 1
  fi
fi

git diff --check
printf '仓库结构、安全边界和 Git 差异检查通过。\n'
