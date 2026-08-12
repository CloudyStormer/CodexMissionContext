#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path


CELLS = [
    {"cell": 1, "code": "V01-F0", "view": "正面标准转面"},
    {"cell": 2, "code": "V02-B180", "view": "背面"},
    {"cell": 3, "code": "V03-L90", "view": "角色自身左侧面"},
    {"cell": 4, "code": "V04-R90", "view": "角色自身右侧面"},
    {"cell": 5, "code": "V05-LF45", "view": "角色自身左前3/4"},
    {"cell": 6, "code": "V06-RF45", "view": "角色自身右前3/4"},
    {"cell": 7, "code": "V07-LB135", "view": "角色自身左后3/4"},
    {"cell": 8, "code": "V08-RB135", "view": "角色自身右后3/4"},
    {"cell": 9, "code": "V09-FULL", "view": "正面全身"},
]


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise SystemExit("拒绝：输入不是有效 PNG")
    return struct.unpack(">II", header[16:24])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="为人工复核后的单角色九宫格创建可追溯清单")
    parser.add_argument("--九宫格", required=True)
    parser.add_argument("--角色编号", required=True)
    parser.add_argument("--角色名", required=True)
    parser.add_argument("--版本", required=True)
    parser.add_argument("--输出")
    parser.add_argument("--方向已人工复核", action="store_true")
    parser.add_argument("--禁止镜像已人工复核", action="store_true")
    args = parser.parse_args()

    image = Path(args.九宫格).expanduser().resolve()
    if not image.is_file():
        raise SystemExit("拒绝：九宫格文件不存在")
    if image.suffix.lower() != ".png":
        raise SystemExit("拒绝：九宫格必须为 PNG")
    if not args.方向已人工复核 or not args.禁止镜像已人工复核:
        raise SystemExit("拒绝：必须先完成人工方向与禁止镜像复核")
    width, height = png_size(image)
    if width != height or width < 1200:
        raise SystemExit(f"拒绝：九宫格须为至少 1200×1200 的正方形，当前为 {width}×{height}")

    output = Path(args.输出).expanduser().resolve() if args.输出 else image.with_suffix(".manifest.json")
    if output.exists():
        raise SystemExit("拒绝：输出清单已存在，请显式使用新版本")
    manifest = {
        "schema": "aimg-character-grid/v1",
        "status": "REVIEW",
        "role_id": args.角色编号,
        "role_name": args.角色名,
        "version": args.版本,
        "image_file": image.name,
        "sha256": sha256(image),
        "width": width,
        "height": height,
        "direction_basis": "character_self",
        "mirror_generated": False,
        "cells": CELLS,
        "qa": {
            "directions_manually_verified": True,
            "mirror_prohibited_and_verified": True,
            "user_approval": "REVIEW",
        },
    }
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已创建九宫格清单：{output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
