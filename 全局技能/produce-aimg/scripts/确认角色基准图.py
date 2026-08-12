#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import struct
import tempfile
from pathlib import Path


FORBIDDEN_PARTS = ("未通过", "失败", "rejected")
ROLE_ID_PATTERN = re.compile(r"角色-\d+")
WINDOWS_INVALID_CHARS = set('<>:"/\\|?*')
EXPECTED_CELL_CODES = [
    "V01-F0", "V02-B180", "V03-L90", "V04-R90", "V05-LF45",
    "V06-RF45", "V07-LB135", "V08-RB135", "V09-FULL",
]
RECORD_FIELDS = ["角色编号", "角色名", "基准图路径", "用户确认原话", "SHA256"]


def reject(message: str) -> None:
    raise SystemExit(f"拒绝：{message}")


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        reject("源图不是有效 PNG")
    return struct.unpack(">II", header[16:24])


def read_registered_roles(project: Path) -> set[tuple[str, str]]:
    role_file = project / "03_角色设定" / "00_角色总表.md"
    if not role_file.is_file():
        reject("缺少 03_角色设定/00_角色总表.md")
    pattern = re.compile(r"^\|\s*(角色-\d+)\s*\|\s*([^|]+?)\s*\|")
    roles: set[tuple[str, str]] = set()
    for line in role_file.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            roles.add((match.group(1).strip(), match.group(2).strip()))
    return roles


def validate_manifest(source: Path, manifest_path: Path, project: Path, role_id: str, role_name: str) -> None:
    if not manifest_path.is_file() or manifest_path != source.with_suffix(".manifest.json"):
        reject("源九宫格缺少同名 manifest.json")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        reject(f"manifest 无效：{exc}")
    if manifest.get("schema") != "aimg-character-grid/v1":
        reject("manifest schema 不正确")
    if manifest.get("role_id") != role_id or manifest.get("role_name") != role_name:
        reject("manifest 角色与发布目标不一致")
    if manifest.get("sha256") != sha256(source):
        reject("manifest SHA-256 与源 PNG 不一致")
    if manifest.get("direction_basis") != "character_self" or manifest.get("mirror_generated") is not False:
        reject("manifest 未锁定角色自身左右或禁止镜像")
    cells = manifest.get("cells")
    actual_cells = [
        (cell.get("cell"), cell.get("code"))
        for cell in cells if isinstance(cell, dict)
    ] if isinstance(cells, list) else []
    if actual_cells != list(enumerate(EXPECTED_CELL_CODES, start=1)):
        reject("manifest 的九格编号、方向或顺序不正确")
    qa = manifest.get("qa", {})
    if qa.get("directions_manually_verified") is not True:
        reject("九个方向尚未人工复核")
    if qa.get("mirror_prohibited_and_verified") is not True:
        reject("禁止镜像规则尚未复核")
    for cell in cells:
        raw = str(cell.get("source_path", "")).strip() if isinstance(cell, dict) else ""
        if not raw:
            continue
        source_path = (project / raw).resolve()
        if not is_within(source_path, project) or not source_path.is_file():
            reject("manifest source_path 必须指向项目内已存在的源图")


def write_csv_atomic(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with temporary.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=RECORD_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="将聊天中已确认的角色九宫格写入 10_角色基准图根目录")
    parser.add_argument("--项目", required=True)
    parser.add_argument("--源九宫格", "--源图", dest="源图", required=True)
    parser.add_argument("--角色编号", required=True)
    parser.add_argument("--角色名", required=True)
    parser.add_argument("--确认原话", required=True)
    parser.add_argument("--清单", help="可选；默认使用源 PNG 的同名 .manifest.json")
    args = parser.parse_args()

    project = Path(args.项目).expanduser().resolve()
    source = Path(args.源图).expanduser().resolve()
    manifest_path = Path(args.清单).expanduser().resolve() if args.清单 else source.with_suffix(".manifest.json")
    role_id = args.角色编号.strip()
    role_name = args.角色名.strip()
    quote = args.确认原话.strip()

    if not project.is_dir():
        reject("项目目录不存在")
    history_roots = [
        (project / "11_交付文件" / "制作历史" / "角色生成历史").resolve(),
        (project / "07_素材资源" / "候选图").resolve(),  # 旧项目迁移兼容
    ]
    for path, label in ((source, "源图"), (manifest_path, "manifest")):
        if (
            not path.is_file()
            or not is_within(path, project)
            or not any(is_within(path, root) for root in history_roots)
        ):
            reject(f"{label}必须是角色生成历史内已存在的文件")
        if any(mark in part.lower() for part in path.parts for mark in FORBIDDEN_PARTS):
            reject("失败/未通过目录中的图片不能写入角色基准图")
    if source.suffix.lower() != ".png":
        reject("源图必须为 PNG")
    if not ROLE_ID_PATTERN.fullmatch(role_id):
        reject("角色编号必须形如 角色-001")
    if not role_name or role_name in {".", ".."} or any(char in WINDOWS_INVALID_CHARS for char in role_name):
        reject("角色名不合规")
    if not quote:
        reject("用户确认原话为空")
    if (role_id, role_name) not in read_registered_roles(project):
        reject("角色不在 00_角色总表.md 中")

    width, height = png_size(source)
    if width != height or width < 1200:
        reject(f"九宫格须为至少 1200×1200 的正方形 PNG，当前 {width}×{height}")
    validate_manifest(source, manifest_path, project, role_id, role_name)

    baseline_root = (project / "10_角色基准图").resolve()
    destination = (baseline_root / f"{role_id}_{role_name}_九宫格.png").resolve()
    if destination.parent != baseline_root:
        reject("基准图目标路径不安全")
    baseline_root.mkdir(parents=True, exist_ok=True)

    descriptor, temporary_name = tempfile.mkstemp(dir=baseline_root, prefix=f".{destination.name}.", suffix=".tmp")
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copy2(source, temporary)
        if sha256(temporary) != sha256(source):
            reject("基准图临时复制哈希校验失败")
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)

    record_path = project / "03_角色设定" / "角色基准图确认记录.csv"
    rows: list[dict[str, str]] = []
    if record_path.is_file():
        with record_path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if list(reader.fieldnames or []) != RECORD_FIELDS:
                reject("现有角色基准图确认记录表头不正确")
            rows = [row for row in reader if row.get("角色编号", "").strip() != role_id]
    rows.append({
        "角色编号": role_id,
        "角色名": role_name,
        "基准图路径": destination.relative_to(project).as_posix(),
        "用户确认原话": quote,
        "SHA256": sha256(destination),
    })
    rows.sort(key=lambda row: row["角色编号"])
    write_csv_atomic(record_path, rows)

    print(f"已写入当前角色基准图：{destination}")
    print(f"已更新内部确认记录：{record_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
