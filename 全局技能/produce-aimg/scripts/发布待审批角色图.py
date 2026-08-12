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
from typing import Any


FORBIDDEN_PARTS = ("未通过", "失败", "rejected")
ROLE_ID_PATTERN = re.compile(r"角色-\d+")
VERSION_PATTERN = re.compile(r"v\d+")
EXPECTED_CELL_CODES = [
    "V01-F0",
    "V02-B180",
    "V03-L90",
    "V04-R90",
    "V05-LF45",
    "V06-RF45",
    "V07-LB135",
    "V08-RB135",
    "V09-FULL",
]
REQUIRED_COLUMNS = {
    "角色编号",
    "角色名",
    "版本",
    "候选路径",
    "正式路径",
    "用户审批状态",
    "用户审批原话",
    "审批绑定SHA256",
}


def reject(message: str) -> None:
    raise SystemExit(f"拒绝：{message}")


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def contains_forbidden_part(path: Path) -> bool:
    return any(
        forbidden in part.lower()
        for part in path.parts
        for forbidden in FORBIDDEN_PARTS
    )


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


def read_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        reject(f"manifest 不是有效 UTF-8 JSON：{exc}")
    if not isinstance(value, dict):
        reject("manifest 顶层必须是对象")
    return value


def validate_manifest(manifest: dict[str, Any], source: Path, project: Path) -> tuple[str, str, str]:
    if manifest.get("schema") != "aimg-character-grid/v1":
        reject("manifest schema 必须为 aimg-character-grid/v1")
    role_id = str(manifest.get("role_id", "")).strip()
    role_name = str(manifest.get("role_name", "")).strip()
    version = str(manifest.get("version", "")).strip()
    if not ROLE_ID_PATTERN.fullmatch(role_id):
        reject("manifest role_id 必须形如 角色-001")
    if not role_name or role_name in {".", ".."} or any(char in role_name for char in '<>:"/\\|?*'):
        reject("manifest role_name 为空或含有非法路径字符")
    if not VERSION_PATTERN.fullmatch(version):
        reject("manifest version 必须形如 v1")
    if manifest.get("status") != "REVIEW":
        reject("manifest status 必须为 REVIEW")
    if manifest.get("image_file") != source.name:
        reject("manifest image_file 与源 PNG 文件名不一致")
    expected_name = f"{role_id}_{role_name}_九宫格候选_{version}.png"
    if source.name != expected_name:
        reject(f"源 PNG 文件名必须为 {expected_name}")

    actual_hash = sha256(source)
    if str(manifest.get("sha256", "")).lower() != actual_hash:
        reject("manifest SHA-256 与源 PNG 实际哈希不一致")
    width, height = png_size(source)
    if width != height or width < 1200:
        reject(f"九宫格须为至少 1200×1200 的正方形 PNG，当前为 {width}×{height}")
    if manifest.get("width") != width or manifest.get("height") != height:
        reject("manifest 宽高与源 PNG 不一致")
    if manifest.get("direction_basis") != "character_self":
        reject("manifest 未声明以角色自身左右为准")
    if manifest.get("mirror_generated") is not False:
        reject("manifest 必须声明 mirror_generated=false")

    cells = manifest.get("cells")
    if not isinstance(cells, list) or len(cells) != 9 or not all(isinstance(cell, dict) for cell in cells):
        reject("manifest 必须包含九个合法格位")
    actual_cells = [(cell.get("cell"), cell.get("code")) for cell in cells]
    expected_cells = list(enumerate(EXPECTED_CELL_CODES, start=1))
    if actual_cells != expected_cells:
        reject("九格编号、代码或顺序不符合固定协议")
    qa = manifest.get("qa")
    if not isinstance(qa, dict) or qa.get("directions_manually_verified") is not True:
        reject("九个方向尚未人工复核")
    if qa.get("mirror_prohibited_and_verified") is not True:
        reject("禁止镜像规则尚未人工复核")

    for cell in cells:
        source_path = str(cell.get("source_path", "")).strip()
        if not source_path:
            continue
        cell_source = (project / source_path).resolve()
        if not is_within(cell_source, project) or not cell_source.is_file():
            reject("manifest source_path 必须指向项目内已存在的文件")
    return role_id, role_name, version


def read_approval_rows(approval_file: Path, role_id: str, role_name: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with approval_file.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        reject(f"无法读取角色九宫格审批清单：{exc}")
    missing = sorted(REQUIRED_COLUMNS - set(fieldnames))
    if missing:
        reject(f"角色九宫格审批清单缺少列：{', '.join(missing)}")
    by_id = [row for row in rows if row.get("角色编号", "").strip() == role_id]
    by_name = [row for row in rows if row.get("角色名", "").strip() == role_name]
    if len(by_id) != 1:
        reject(f"审批清单中 {role_id} 必须且只能有一行，当前为 {len(by_id)} 行")
    if len(by_name) != 1 or by_name[0] is not by_id[0]:
        reject(f"审批清单中角色名 {role_name} 必须且只能绑定 {role_id}")
    if by_id[0].get("角色名", "").strip() != role_name:
        reject(f"审批清单中 {role_id} 的角色名与 manifest 不一致")
    return fieldnames, rows


def copy_to_temporary(source: Path, target: Path) -> Path:
    descriptor, temporary_name = tempfile.mkstemp(
        dir=target.parent,
        prefix=f".{target.name}.",
        suffix=".tmp",
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copy2(source, temporary)
        if sha256(temporary) != sha256(source):
            reject(f"临时复制校验失败：{target.name}")
        return temporary
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def write_csv_temporary(
    approval_file: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> Path:
    descriptor, temporary_name = tempfile.mkstemp(
        dir=approval_file.parent,
        prefix=f".{approval_file.name}.",
        suffix=".tmp",
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with temporary.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            stream.flush()
            os.fsync(stream.fileno())
        return temporary
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(
        description="把 07 生成审计源的当前 REVIEW 九宫格安全发布到 10_角色基准图/角色目录/00_待审批"
    )
    parser.add_argument("--项目", required=True, help="AIMG 项目根目录")
    parser.add_argument(
        "--源九宫格",
        "--源图",
        dest="源图",
        required=True,
        help="07_素材资源/候选图 内的九宫格 PNG（--源图 为兼容别名）",
    )
    parser.add_argument(
        "--角色目录",
        help="可选交叉校验，必须等于 manifest 推导出的 角色-XXX_角色名",
    )
    parser.add_argument("--清单", help="与源图同名的 manifest；省略时自动取 .manifest.json")
    args = parser.parse_args()

    project = Path(args.项目).expanduser().resolve()
    source = Path(args.源图).expanduser().resolve()
    manifest_path = (
        Path(args.清单).expanduser().resolve()
        if args.清单
        else source.with_suffix(".manifest.json")
    )
    if not project.is_dir():
        reject("项目目录不存在")
    audit_root = (project / "07_素材资源" / "候选图").resolve()
    for item, label in ((source, "源图"), (manifest_path, "manifest")):
        if not is_within(item, project):
            reject(f"{label}不在项目内")
        if not is_within(item, audit_root):
            reject(f"{label}必须位于 07_素材资源/候选图 内")
        if not item.is_file():
            reject(f"{label}不存在")
        if contains_forbidden_part(item):
            reject("失败/未通过路径中的候选不能发布")
    if source.suffix.lower() != ".png":
        reject("源图必须为 PNG")
    if manifest_path != source.with_suffix(".manifest.json"):
        reject("manifest 必须与源 PNG 同名且位于同一目录")

    manifest = read_manifest(manifest_path)
    role_id, role_name, version = validate_manifest(manifest, source, project)
    canonical_role_dir = f"{role_id}_{role_name}"
    if args.角色目录 and args.角色目录 != canonical_role_dir:
        reject(f"--角色目录 必须等于 {canonical_role_dir}")
    approval_file = project / "03_角色设定" / "角色九宫格审批清单.csv"
    if not approval_file.is_file() or not is_within(approval_file.resolve(), project):
        reject("缺少项目内的 03_角色设定/角色九宫格审批清单.csv")
    fieldnames, rows = read_approval_rows(approval_file, role_id, role_name)

    target_root = (project / "10_角色基准图").resolve()
    target_dir = (target_root / canonical_role_dir / "00_待审批").resolve()
    target_image = (target_dir / source.name).resolve()
    target_manifest = target_image.with_suffix(".manifest.json")
    for target in (target_dir, target_image, target_manifest):
        if not is_within(target, project) or not is_within(target, target_root):
            reject("目标路径不在项目的 10_角色基准图 内")
        if contains_forbidden_part(target):
            reject("目标路径含失败/未通过标记")

    if target_dir.exists() and not target_dir.is_dir():
        reject("目标 00_待审批 路径不是目录")
    if target_dir.is_dir():
        other_images = [
            path for path in target_dir.iterdir()
            if path.is_file() and path.suffix.lower() == ".png" and path.resolve() != target_image
        ]
        if other_images:
            reject("00_待审批 已有另一个当前 PNG；请先移入 02_历史待审批 后再发布")
        other_manifests = [
            path for path in target_dir.iterdir()
            if path.is_file() and path.name.endswith(".manifest.json") and path.resolve() != target_manifest
        ]
        if other_manifests:
            reject("00_待审批 已有另一个 manifest；请先移入 02_历史待审批 后再发布")

    source_hash = sha256(source)
    if target_image.exists() and sha256(target_image) != source_hash:
        reject("目标已有同名但哈希不同的 PNG，请使用新版本或先人工处理冲突")
    if target_manifest.exists() and sha256(target_manifest) != sha256(manifest_path):
        reject("目标已有同名但内容不同的 manifest，请先人工处理冲突")

    relative_target = target_image.relative_to(project).as_posix()
    for row in rows:
        if row.get("角色编号", "").strip() == role_id:
            row["版本"] = version
            row["候选路径"] = relative_target
            row["正式路径"] = ""
            row["用户审批状态"] = "REVIEW"
            row["用户审批原话"] = ""
            row["审批绑定SHA256"] = ""

    target_dir.mkdir(parents=True, exist_ok=True)
    csv_temporary: Path | None = None
    image_temporary: Path | None = None
    manifest_temporary: Path | None = None
    try:
        csv_temporary = write_csv_temporary(approval_file, fieldnames, rows)
        if not target_image.exists():
            image_temporary = copy_to_temporary(source, target_image)
        if not target_manifest.exists():
            manifest_temporary = copy_to_temporary(manifest_path, target_manifest)
        if image_temporary is not None:
            os.replace(image_temporary, target_image)
            image_temporary = None
        if manifest_temporary is not None:
            os.replace(manifest_temporary, target_manifest)
            manifest_temporary = None
        os.replace(csv_temporary, approval_file)
        csv_temporary = None
    finally:
        for temporary in (csv_temporary, image_temporary, manifest_temporary):
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    print(f"已发布待审批角色图：{target_image}")
    print(f"审批清单已重置为 REVIEW：{role_id}_{role_name} {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
