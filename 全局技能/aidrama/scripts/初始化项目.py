#!/usr/bin/env python3
"""以不覆盖既有文件的方式初始化 AI 漫剧项目。"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"


def safe_name(value: str) -> str:
    cleaned = re.sub(r'[\\\\/:\\x00]', "-", value.strip())
    cleaned = re.sub(r"\\s+", "-", cleaned)
    cleaned = cleaned.strip(".-")
    if not cleaned:
        raise ValueError("项目名至少要包含一个可用字符")
    return cleaned


def copy_if_missing(source: Path, destination: Path, force: bool) -> str:
    if destination.exists() and not force:
        return f"跳过：{destination}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    return f"写入：{destination}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="创建 AI 漫剧项目；默认不覆盖已经存在的模板文件。"
    )
    parser.add_argument("--项目名", required=True, help="新建项目文件夹的名称")
    parser.add_argument(
        "--输出目录", required=True, type=Path, help="用于存放项目的父目录"
    )
    parser.add_argument(
        "--强制覆盖",
        action="store_true",
        help="覆盖由本脚本初始化的模板文件，但保留其他文件",
    )
    args = parser.parse_args()

    project_dir = args.输出目录.expanduser().resolve() / safe_name(args.项目名)
    directories = [
        project_dir / "00-项目简报",
        project_dir / "01-设定库",
        project_dir / "02-单集" / "第001集",
        project_dir / "03-素材" / "参考资料",
        project_dir / "03-素材" / "图片",
        project_dir / "03-素材" / "音频",
        project_dir / "03-素材" / "视频",
        project_dir / "04-交付",
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    operations = [
        copy_if_missing(
            ASSETS_DIR / "项目简报.md",
            project_dir / "00-项目简报" / "项目简报.md",
            args.强制覆盖,
        ),
        copy_if_missing(
            ASSETS_DIR / "角色卡.md",
            project_dir / "01-设定库" / "角色卡.md",
            args.强制覆盖,
        ),
        copy_if_missing(
            ASSETS_DIR / "单集剧本.md",
            project_dir / "02-单集" / "第001集" / "单集剧本.md",
            args.强制覆盖,
        ),
        copy_if_missing(
            ASSETS_DIR / "分镜表模板.csv",
            project_dir / "02-单集" / "第001集" / "分镜表.csv",
            args.强制覆盖,
        ),
    ]

    print(f"项目目录：{project_dir}")
    for operation in operations:
        print(operation)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
