#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import struct
from pathlib import Path


FORBIDDEN_PARTS = ("未通过", "失败", "rejected")
APPROVED_STATES = {"PASS", "LOCKED", "APPROVED"}
ROLE_DIR_PATTERN = re.compile(r"^(角色-\d+)_(.+)$")
FORMAL_NAME_PATTERN = re.compile(r"^角色基准九宫格_(v\d+)\.png$")
EXPECTED_CELL_CODES = [
    "V01-F0", "V02-B180", "V03-L90", "V04-R90", "V05-LF45",
    "V06-RF45", "V07-LB135", "V08-RB135", "V09-FULL",
]


def gate_passed(state_file: Path, gate: str) -> bool:
    pattern = re.compile(rf"^\s*{re.escape(gate)}\s*:\s*PASS\s*$", re.MULTILINE)
    return bool(pattern.search(state_file.read_text(encoding="utf-8")))


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise SystemExit("拒绝：候选不是有效 PNG")
    return struct.unpack(">II", header[16:24])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def approval_row(project: Path, role_id: str, role_name: str) -> dict[str, str]:
    approval_file = project / "03_角色设定" / "角色九宫格审批清单.csv"
    if not approval_file.is_file():
        raise SystemExit("拒绝：缺少角色九宫格审批清单")
    with approval_file.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        if row.get("角色编号", "").strip() == role_id and row.get("角色名", "").strip() == role_name:
            return row
    raise SystemExit(f"拒绝：审批清单中没有 {role_id}_{role_name}")


def registered_roles(project: Path) -> set[tuple[str, str]]:
    role_file = project / "03_角色设定" / "00_角色总表.md"
    if not role_file.is_file():
        raise SystemExit("拒绝：缺少 03_角色设定/00_角色总表.md")
    roles: set[tuple[str, str]] = set()
    pattern = re.compile(r"^\|\s*(角色-\d+)\s*\|\s*([^|]+?)\s*\|")
    for line in role_file.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            roles.add((match.group(1).strip(), match.group(2).strip()))
    if not roles:
        raise SystemExit("拒绝：角色总表中没有可识别的角色记录")
    return roles


def main() -> int:
    parser = argparse.ArgumentParser(description="仅晋级已获用户批准的单角色高清九宫格")
    parser.add_argument("--项目", required=True)
    parser.add_argument("--候选", required=True)
    parser.add_argument("--清单", required=True)
    parser.add_argument("--角色目录", required=True)
    parser.add_argument("--文件名", required=True)
    args = parser.parse_args()

    project = Path(args.项目).expanduser().resolve()
    candidate = Path(args.候选).expanduser().resolve()
    manifest_path = Path(args.清单).expanduser().resolve()
    if not project.is_dir():
        raise SystemExit("拒绝：项目目录不存在")
    for source in (candidate, manifest_path):
        if not is_within(source, project):
            raise SystemExit("拒绝：候选或清单不在项目内")
        if not source.is_file():
            raise SystemExit("拒绝：候选或清单不存在")
        if any(part in str(source).lower() for part in FORBIDDEN_PARTS):
            raise SystemExit("拒绝：失败/未通过候选不能晋级")

    role_match = ROLE_DIR_PATTERN.fullmatch(args.角色目录)
    name_match = FORMAL_NAME_PATTERN.fullmatch(args.文件名)
    if not role_match:
        raise SystemExit("拒绝：角色目录必须为 角色-001_角色名")
    if not name_match:
        raise SystemExit("拒绝：正式文件名必须为 角色基准九宫格_vN.png")
    role_id, role_name = role_match.groups()
    version = name_match.group(1)

    state_file = project / "01_项目总览" / "审批状态.md"
    if not state_file.is_file() or not gate_passed(state_file, "G3"):
        raise SystemExit("拒绝：G3 双主角正脸共同审批尚未 PASS")

    row = approval_row(project, role_id, role_name)
    if (role_id, role_name) not in registered_roles(project):
        raise SystemExit("拒绝：目标角色不在角色总表中")
    if row.get("需要基准图", "").strip() != "是":
        raise SystemExit("拒绝：该角色未标为需要基准图")
    if row.get("用户审批状态", "").strip().upper() not in APPROVED_STATES:
        raise SystemExit("拒绝：该角色尚未获用户明确审批")
    quote = row.get("用户审批原话", "").strip()
    if not quote:
        raise SystemExit("拒绝：用户审批原话为空，不能证明明确审批")
    expected_candidate = row.get("候选路径", "").strip()
    if expected_candidate and (project / expected_candidate).resolve() != candidate:
        raise SystemExit("拒绝：候选路径与审批清单不一致")

    width, height = png_size(candidate)
    if width != height or width < 1200:
        raise SystemExit(f"拒绝：九宫格须为至少 1200×1200 的正方形 PNG，当前为 {width}×{height}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise SystemExit(f"拒绝：清单不是有效 UTF-8 JSON：{exc}") from exc
    if manifest.get("role_id") != role_id or manifest.get("role_name") != role_name:
        raise SystemExit("拒绝：清单角色与目标角色不一致")
    if manifest.get("schema") != "aimg-character-grid/v1":
        raise SystemExit("拒绝：清单 schema 不正确")
    if manifest.get("version") != version:
        raise SystemExit("拒绝：清单版本与正式文件名不一致")
    if manifest.get("sha256") != sha256(candidate):
        raise SystemExit("拒绝：候选图片哈希与清单不一致")
    if manifest.get("direction_basis") != "character_self":
        raise SystemExit("拒绝：清单未声明以角色自身左右为准")
    cells = manifest.get("cells")
    if not isinstance(cells, list):
        raise SystemExit("拒绝：清单缺少九个固定格位")
    actual_cells = [(cell.get("cell"), cell.get("code")) for cell in cells if isinstance(cell, dict)]
    expected_cells = list(enumerate(EXPECTED_CELL_CODES, start=1))
    if actual_cells != expected_cells:
        raise SystemExit("拒绝：九格编号、代码或顺序不符合固定协议")
    qa = manifest.get("qa", {})
    if qa.get("directions_manually_verified") is not True:
        raise SystemExit("拒绝：九个方向尚未人工复核")
    if qa.get("mirror_prohibited_and_verified") is not True or manifest.get("mirror_generated") is not False:
        raise SystemExit("拒绝：禁止镜像规则尚未确认")

    formal_root = (project / "10_角色基准图").resolve()
    destination_dir = (formal_root / args.角色目录).resolve()
    destination = (destination_dir / args.文件名).resolve()
    destination_manifest = destination.with_suffix(".manifest.json")
    approval_record = destination_dir / f"审批记录_{version}.md"
    for target in (destination, destination_manifest, approval_record):
        if not is_within(target.resolve(), formal_root):
            raise SystemExit("拒绝：目标路径不在正式角色目录内")
        if target.exists():
            raise SystemExit(f"拒绝：目标已存在，请使用新版本：{target.name}")

    destination_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(candidate, destination)
    formal_manifest = dict(manifest)
    formal_manifest["status"] = "LOCKED"
    formal_manifest["image_file"] = destination.name
    formal_manifest["source_candidate"] = candidate.relative_to(project).as_posix()
    formal_manifest["user_approval_status"] = row.get("用户审批状态", "").strip()
    formal_manifest["user_approval_quote"] = quote
    formal_manifest.setdefault("qa", {})["user_approval"] = row.get("用户审批状态", "").strip()
    destination_manifest.write_text(
        json.dumps(formal_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    approval_record.write_text(
        "# 角色九宫格审批记录\n\n"
        f"- 角色：{role_id}_{role_name}\n"
        f"- 版本：{version}\n"
        f"- 用户审批状态：{row.get('用户审批状态', '').strip()}\n"
        f"- 用户审批原话：{quote}\n"
        f"- 源候选：{candidate.relative_to(project).as_posix()}\n"
        f"- 方向基准：角色自身左右；禁止镜像\n",
        encoding="utf-8",
    )

    approval_file = project / "03_角色设定" / "角色九宫格审批清单.csv"
    with approval_file.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if "正式路径" not in fieldnames:
        fieldnames.append("正式路径")
    relative_destination = destination.relative_to(project).as_posix()
    for approval in rows:
        if approval.get("角色编号", "").strip() == role_id and approval.get("角色名", "").strip() == role_name:
            approval["正式路径"] = relative_destination
    temporary = approval_file.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(approval_file)
    print(f"已晋级正式角色九宫格：{destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
