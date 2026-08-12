#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import re
import struct
import sys
from pathlib import Path


REQUIRED_DIRS = [
    "01_项目总览", "02_世界观设定", "03_角色设定", "04_剧集脚本",
    "05_分镜脚本", "06_提示词库", "07_素材资源", "08_发布物料",
    "09_技术文档", "10_角色基准图",
]
RECORD_FIELDS = ["角色编号", "角色名", "基准图路径", "用户确认原话", "SHA256"]
ROLE_FILE_PATTERN = re.compile(r"^(角色-\d+)_(.+)_九宫格\.png$")
EPISODE_DIR_PATTERN = re.compile(r"^第\d{3}集关键帧$")
FRAME_FILE_PATTERN = re.compile(r"^镜头\d{2,3}\.png$")
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
WINDOWS_INVALID_CHARS = set('<>:"/\\|?*')


def parse_gates(path: Path) -> dict[str, str]:
    gates: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*(G\d+)\s*:\s*([A-Z_]+)\s*$", line)
        if match:
            gates[match.group(1)] = match.group(2)
    return gates


def parse_registered_roles(path: Path) -> set[tuple[str, str]]:
    roles: set[tuple[str, str]] = set()
    pattern = re.compile(r"^\|\s*(角色-\d+)\s*\|\s*([^|]+?)\s*\|")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            roles.add((match.group(1).strip(), match.group(2).strip()))
    return roles


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("不是有效 PNG")
    return struct.unpack(">II", header[16:24])


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def safe_role_name(name: str) -> bool:
    return bool(
        name and name not in {".", ".."}
        and not any(char in WINDOWS_INVALID_CHARS or ord(char) < 32 for char in name)
    )


def validate_baselines(
    project: Path,
    gates: dict[str, str],
    roles: set[tuple[str, str]],
    errors: list[str],
    warnings: list[str],
) -> bool:
    baseline_root = project / "10_角色基准图"
    record_file = project / "03_角色设定" / "角色基准图确认记录.csv"
    canonical_images: dict[tuple[str, str], Path] = {}
    other_entries: list[Path] = []

    if baseline_root.is_dir():
        for entry in baseline_root.iterdir():
            if entry.is_file() and entry.name == "README.md":
                continue
            match = ROLE_FILE_PATTERN.fullmatch(entry.name) if entry.is_file() else None
            if match:
                role_id, role_name = match.groups()
                key = (role_id, role_name)
                if not safe_role_name(role_name):
                    errors.append(f"角色基准图文件名不安全：{entry.name}")
                elif key in canonical_images:
                    errors.append(f"角色基准图重复：{role_id}_{role_name}")
                else:
                    canonical_images[key] = entry
            else:
                other_entries.append(entry)

    new_layout = bool(canonical_images or record_file.exists())
    if not new_layout:
        if other_entries:
            warnings.append("检测到旧版角色基准图目录；按只读兼容处理，不强制迁移")
        elif gates.get("G4") == "PASS":
            errors.append("G4 已 PASS，但 10_角色基准图 根目录没有当前角色 PNG")
        return False

    for entry in other_entries:
        errors.append(f"10_角色基准图 根目录只允许当前 PNG 和 README.md：{entry.name}")
    if not (baseline_root / "README.md").is_file():
        errors.append("10_角色基准图 缺少 README.md")

    records: dict[tuple[str, str], dict[str, str]] = {}
    if not record_file.is_file():
        errors.append("缺少内部角色基准图确认记录")
    else:
        try:
            with record_file.open("r", encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream)
                if list(reader.fieldnames or []) != RECORD_FIELDS:
                    errors.append("角色基准图确认记录表头不正确")
                else:
                    for row in reader:
                        key = (row["角色编号"].strip(), row["角色名"].strip())
                        if key in records:
                            errors.append(f"角色基准图确认记录重复：{key[0]}_{key[1]}")
                        records[key] = row
        except (OSError, UnicodeDecodeError, csv.Error) as exc:
            errors.append(f"无法读取角色基准图确认记录：{exc}")

    for key, image in canonical_images.items():
        role_id, role_name = key
        if roles and key not in roles:
            errors.append(f"角色基准图未登记在角色总表：{role_id}_{role_name}")
        try:
            width, height = png_size(image)
        except (OSError, ValueError) as exc:
            errors.append(f"{image.name} 无效：{exc}")
            continue
        if width != height or width < 1200:
            errors.append(f"{image.name} 须为至少 1200×1200 的正方形 PNG，当前 {width}×{height}")
        row = records.get(key)
        if row is None:
            errors.append(f"{image.name} 缺少内部确认记录")
            continue
        expected_relative = image.relative_to(project).as_posix()
        if row["基准图路径"].strip() != expected_relative:
            errors.append(f"{image.name} 的确认记录路径不一致")
        if not row["用户确认原话"].strip():
            errors.append(f"{image.name} 的用户确认原话为空")
        if row["SHA256"].strip().lower() != sha256(image):
            errors.append(f"{image.name} 与内部确认记录哈希不一致")

    for key in records:
        if key not in canonical_images:
            errors.append(f"确认记录指向的角色基准图不存在：{key[0]}_{key[1]}")
    if gates.get("G4") == "PASS" and roles:
        missing = sorted(roles - set(canonical_images))
        if missing:
            errors.append("G4 已 PASS，但缺少角色基准图：" + "、".join(f"{a}_{b}" for a, b in missing))
    if canonical_images and gates.get("G3") != "PASS":
        errors.append("已有当前角色基准图，但 G3 双主角正脸共同确认不是 PASS")
    return True


def validate_keyframes(project: Path, gates: dict[str, str], strict: bool, errors: list[str]) -> None:
    root = project / "07_素材资源"
    if not root.is_dir():
        return
    frames: list[Path] = []
    if strict:
        for entry in root.iterdir():
            if entry.is_file() and entry.name == "关键帧交付清单.md":
                continue
            if entry.is_dir() and EPISODE_DIR_PATTERN.fullmatch(entry.name):
                for child in entry.iterdir():
                    if not child.is_file() or not FRAME_FILE_PATTERN.fullmatch(child.name):
                        errors.append(f"分集关键帧目录只允许最终 PNG：{child.relative_to(project)}")
                    else:
                        frames.append(child)
            else:
                errors.append(f"07_素材资源 根只允许交付清单和第XXX集关键帧目录：{entry.name}")
    else:
        frames = [path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in IMAGE_EXTS]
    if frames and gates and gates.get("G4") != "PASS":
        errors.append("G4 角色基准图未全部确认，但已有正式剧情关键帧")


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

    legacy_shape = not (project / "01_项目总览" / "审批状态.md").is_file()
    for relative in REQUIRED_DIRS:
        if not (project / relative).is_dir():
            if legacy_shape:
                warnings.append(f"旧项目缺少新规范目录，只读兼容：{relative}")
            else:
                errors.append(f"缺少必需目录：{relative}")
    if not (project / "11_交付文件" / "制作历史").is_dir():
        if legacy_shape:
            warnings.append("旧项目没有 11_交付文件/制作历史；只读兼容")
        else:
            errors.append("缺少必需目录：11_交付文件/制作历史")

    state_file = project / "01_项目总览" / "审批状态.md"
    gates = parse_gates(state_file) if state_file.is_file() else {}
    if not state_file.is_file():
        warnings.append("缺少 01_项目总览/审批状态.md；无法自动验证生产门")

    role_file = project / "03_角色设定" / "00_角色总表.md"
    roles = parse_registered_roles(role_file) if role_file.is_file() else set()
    if not role_file.is_file():
        warnings.append("缺少 03_角色设定/00_角色总表.md")
    elif not roles and gates.get("G2") == "PASS":
        errors.append("G2 已 PASS，但角色总表没有可识别的角色记录")

    strict_layout = validate_baselines(project, gates, roles, errors, warnings)
    validate_keyframes(project, gates, strict_layout, errors)

    gate_dependencies = {
        "G1": ("G0",), "G2": ("G0",), "G3": ("G2",), "G4": ("G3",),
        "G5": ("G1", "G4"), "G6": ("G5",), "G7": ("G6",),
        "G8": ("G7",), "G9": ("G8",),
    }
    for gate, dependencies in gate_dependencies.items():
        if gates.get(gate) == "PASS":
            missing = [dependency for dependency in dependencies if gates.get(dependency) != "PASS"]
            if missing:
                errors.append(f"{gate} 已 PASS，但前置生产门未通过：" + "、".join(missing))

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
