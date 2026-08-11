#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DIRECTORIES = [
    "01_项目总览",
    "02_世界观设定",
    "03_角色设定",
    "04_剧集脚本",
    "05_分镜脚本",
    "06_提示词库",
    "07_素材资源/参考图",
    "07_素材资源/候选图",
    "07_素材资源/正式图",
    "07_素材资源/音频",
    "07_素材资源/视频",
    "08_发布物料",
    "09_技术文档",
    "10_角色基准图",
    "11_交付文件",
]

TEMPLATES = {
    "审批状态模板.md": "01_项目总览/审批状态.md",
    "项目简报模板.md": "01_项目总览/项目简报.md",
    "故事逻辑审计模板.md": "02_世界观设定/故事逻辑审计.md",
    "共享画风圣经模板.md": "03_角色设定/共享画风圣经.md",
    "分镜表模板.csv": "05_分镜脚本/分镜表模板.csv",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化不覆盖现有文件的 AIMG 项目结构")
    parser.add_argument("--项目名", required=True)
    parser.add_argument("--输出目录", required=True)
    args = parser.parse_args()

    parent = Path(args.输出目录).expanduser().resolve()
    project = (parent / args.项目名).resolve()
    if project.parent != parent:
        raise SystemExit("项目名不能跳出输出目录")

    project.mkdir(parents=True, exist_ok=True)
    for relative in DIRECTORIES:
        (project / relative).mkdir(parents=True, exist_ok=True)

    assets = Path(__file__).resolve().parent.parent / "assets"
    for source_name, relative_target in TEMPLATES.items():
        source = assets / source_name
        target = project / relative_target
        if not target.exists():
            shutil.copyfile(source, target)

    print(f"AIMG 项目已初始化：{project}")
    print("未覆盖任何已有文件。下一步先完成 G0 故事逻辑门。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
