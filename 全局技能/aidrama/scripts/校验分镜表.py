#!/usr/bin/env python3
"""检查 aidrama 分镜表的确定性结构。"""

from __future__ import annotations

import argparse
import csv
import math
import re
from pathlib import Path


REQUIRED_COLUMNS = [
    "镜头编号",
    "时长秒",
    "场次",
    "景别",
    "机位",
    "画面",
    "动作",
    "对白或旁白",
    "图片提示词",
    "视频提示词",
    "连续性引用",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="检查 aidrama 分镜表。")
    parser.add_argument("分镜表路径", type=Path)
    args = parser.parse_args()

    path = args.分镜表路径.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_file():
        print(f"错误：找不到文件：{path}")
        return 1

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        missing = [column for column in REQUIRED_COLUMNS if column not in columns]
        if missing:
            errors.append("缺少字段：" + "、".join(missing))
        rows = list(reader)

    if not rows:
        errors.append("分镜表没有任何镜头")

    seen_ids: set[str] = set()
    total_duration = 0.0
    for line_number, row in enumerate(rows, start=2):
        shot_id = (row.get("镜头编号") or "").strip()
        if not shot_id:
            errors.append(f"第 {line_number} 行：镜头编号为空")
        elif shot_id in seen_ids:
            errors.append(f"第 {line_number} 行：镜头编号重复：{shot_id}")
        else:
            seen_ids.add(shot_id)
            if not re.fullmatch(r"第\d{3}集-镜头\d{3}", shot_id):
                errors.append(
                    f"第 {line_number} 行：镜头编号必须使用“第001集-镜头001”格式"
                )

        raw_duration = (row.get("时长秒") or "").strip()
        try:
            duration = float(raw_duration)
            if not math.isfinite(duration) or duration <= 0:
                raise ValueError
            total_duration += duration
        except ValueError:
            errors.append(f"第 {line_number} 行：时长秒必须是正数")

        for field in ("场次", "画面", "动作", "图片提示词"):
            if not (row.get(field) or "").strip():
                errors.append(f"第 {line_number} 行：{field}为空")

        for field in ("视频提示词", "连续性引用"):
            if not (row.get(field) or "").strip():
                warnings.append(f"第 {line_number} 行：{field}为空")

    print(f"文件：{path}")
    print(f"镜头数：{len(rows)}")
    print(f"计划总时长：{total_duration:g} 秒")
    for warning in warnings:
        print(f"警告：{warning}")
    for error in errors:
        print(f"错误：{error}")

    if errors:
        print(f"未通过：{len(errors)} 个错误，{len(warnings)} 个警告")
        return 1

    print(f"通过：{len(warnings)} 个警告")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
