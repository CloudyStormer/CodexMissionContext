#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_DIRS = [
    "01_项目总览", "02_世界观设定", "03_角色设定", "04_剧集脚本",
    "05_分镜脚本", "06_提示词库", "07_素材资源", "08_发布物料",
    "09_技术文档", "10_角色基准图", "11_交付文件",
]
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
FORBIDDEN_PARTS = ("未通过", "失败", "rejected")


def parse_gates(path: Path) -> dict[str, str]:
    gates: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*(G\d+)\s*:\s*([A-Z_]+)\s*$", line)
        if match:
            gates[match.group(1)] = match.group(2)
    return gates


def main() -> int:
    if len(sys.argv) != 2:
        print("用法：python 校验AIMG项目.py <项目路径>")
        return 2

    project = Path(sys.argv[1]).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not project.is_dir():
        print(f"错误：项目目录不存在：{project}")
        return 1

    for relative in REQUIRED_DIRS:
        if not (project / relative).is_dir():
            errors.append(f"缺少必需目录：{relative}")

    state_file = project / "01_项目总览" / "审批状态.md"
    gates: dict[str, str] = {}
    if state_file.exists():
        gates = parse_gates(state_file)
    else:
        warnings.append("缺少 01_项目总览/审批状态.md；无法自动验证审批门")

    formal_root = project / "10_角色基准图"
    formal_images = [p for p in formal_root.rglob("*") if p.suffix.lower() in IMAGE_EXTS]
    if formal_images and gates.get("G3") != "PASS":
        errors.append("存在正式角色图，但 G3 双主角正脸共同审批不是 PASS")

    for image in formal_images:
        lower = str(image).lower()
        if any(part in lower for part in FORBIDDEN_PARTS):
            errors.append(f"失败候选混入正式角色目录：{image.relative_to(project)}")

    if gates.get("G4") == "PASS" and gates.get("G3") != "PASS":
        errors.append("G4 多视角通过，但 G3 双主角正脸未通过")
    if gates.get("G7") == "PASS" and gates.get("G6") != "PASS":
        errors.append("G7 无声样片通过，但 G6 静态首尾帧未通过")
    if gates.get("G9") == "PASS" and gates.get("G8") != "PASS":
        errors.append("G9 批量生产已开启，但 G8 正式样片未通过")

    if not formal_images:
        warnings.append("正式角色锚点为空")

    for warning in warnings:
        print(f"警告：{warning}")
    for error in errors:
        print(f"错误：{error}")

    if errors:
        print(f"校验失败：{len(errors)} 个阻塞，{len(warnings)} 个警告")
        return 1
    print(f"校验通过：0 个阻塞，{len(warnings)} 个警告")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
