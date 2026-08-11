#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


FORBIDDEN_PARTS = ("未通过", "失败", "rejected")


def gate_passed(state_file: Path, gate: str) -> bool:
    pattern = re.compile(rf"^\s*{re.escape(gate)}\s*:\s*PASS\s*$", re.MULTILINE)
    return bool(pattern.search(state_file.read_text(encoding="utf-8")))


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="仅在 G3 通过后晋级角色身份锚点")
    parser.add_argument("--项目", required=True)
    parser.add_argument("--候选", required=True)
    parser.add_argument("--角色目录", required=True)
    parser.add_argument("--文件名", required=True)
    args = parser.parse_args()

    project = Path(args.项目).expanduser().resolve()
    candidate = Path(args.候选).expanduser().resolve()
    if not is_within(candidate, project):
        raise SystemExit("拒绝：候选文件不在项目内")
    if not candidate.is_file():
        raise SystemExit("拒绝：候选文件不存在")
    if any(part in str(candidate).lower() for part in FORBIDDEN_PARTS):
        raise SystemExit("拒绝：失败/未通过候选不能晋级")

    state_file = project / "01_项目总览" / "审批状态.md"
    if not state_file.is_file() or not gate_passed(state_file, "G3"):
        raise SystemExit("拒绝：G3 双主角正脸共同审批尚未 PASS")

    formal_root = (project / "10_角色基准图").resolve()
    destination = (formal_root / args.角色目录 / args.文件名).resolve()
    if not is_within(destination, formal_root):
        raise SystemExit("拒绝：目标路径不在正式角色目录内")
    if destination.exists():
        raise SystemExit("拒绝：目标文件已存在，请使用新版本名")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(candidate, destination)
    print(f"已晋级正式角色锚点：{destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
