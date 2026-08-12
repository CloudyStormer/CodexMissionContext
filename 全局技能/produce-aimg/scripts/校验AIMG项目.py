#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import struct
import sys
from pathlib import Path


REQUIRED_DIRS = [
    "01_项目总览", "02_世界观设定", "03_角色设定", "04_剧集脚本",
    "05_分镜脚本", "06_提示词库", "07_素材资源", "08_发布物料",
    "09_技术文档", "10_角色基准图", "11_交付文件",
]
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
FORBIDDEN_PARTS = ("未通过", "失败", "rejected")
APPROVED_STATES = {"PASS", "LOCKED", "APPROVED"}
EXPECTED_CELL_CODES = [
    "V01-F0", "V02-B180", "V03-L90", "V04-R90", "V05-LF45",
    "V06-RF45", "V07-LB135", "V08-RB135", "V09-FULL",
]
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".avi"}
AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"}


def parse_gates(path: Path) -> dict[str, str]:
    gates: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*(G\d+)\s*:\s*([A-Z_]+)\s*$", line)
        if match:
            gates[match.group(1)] = match.group(2)
    return gates


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("不是有效 PNG")
    return struct.unpack(">II", header[16:24])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_registered_roles(path: Path) -> set[tuple[str, str]]:
    roles: set[tuple[str, str]] = set()
    pattern = re.compile(r"^\|\s*(角色-\d+)\s*\|\s*([^|]+?)\s*\|")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            roles.add((match.group(1).strip(), match.group(2).strip()))
    return roles


def validate_grid(
    image: Path,
    manifest_path: Path,
    label: str,
    errors: list[str],
    formal: bool = False,
) -> None:
    try:
        width, height = png_size(image)
    except (OSError, ValueError) as exc:
        errors.append(f"{label}不是有效 PNG：{exc}")
        return
    if width != height or width < 1200:
        errors.append(f"{label}须为至少 1200×1200 的正方形，当前 {width}×{height}")
    if not manifest_path.is_file():
        errors.append(f"{label}缺少配套 manifest.json")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label}的 manifest 无效：{exc}")
        return
    if manifest.get("schema") != "aimg-character-grid/v1":
        errors.append(f"{label}的 manifest schema 不正确")
    if manifest.get("sha256") != sha256(image):
        errors.append(f"{label}与 manifest 哈希不一致")
    if manifest.get("direction_basis") != "character_self":
        errors.append(f"{label}未锁定角色自身左右")
    if manifest.get("mirror_generated") is not False:
        errors.append(f"{label}未声明禁止镜像")
    cells = manifest.get("cells")
    actual_cells = [
        (cell.get("cell"), cell.get("code"))
        for cell in cells
        if isinstance(cell, dict)
    ] if isinstance(cells, list) else []
    if actual_cells != list(enumerate(EXPECTED_CELL_CODES, start=1)):
        errors.append(f"{label}的九格编号、代码或顺序不符合固定协议")
    qa = manifest.get("qa", {})
    if qa.get("directions_manually_verified") is not True:
        errors.append(f"{label}的方向未人工复核")
    if qa.get("mirror_prohibited_and_verified") is not True:
        errors.append(f"{label}的禁止镜像未人工复核")
    if formal:
        if manifest.get("status") != "LOCKED":
            errors.append(f"{label}的 manifest 未锁定为 LOCKED")
        if str(manifest.get("user_approval_status", "")).upper() not in APPROVED_STATES:
            errors.append(f"{label}的 manifest 缺少用户通过状态")
        if not str(manifest.get("user_approval_quote", "")).strip():
            errors.append(f"{label}的 manifest 缺少用户审批原话")


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

    approval_file = project / "03_角色设定" / "角色九宫格审批清单.csv"
    approval_rows: list[dict[str, str]] = []
    if approval_file.is_file():
        with approval_file.open("r", encoding="utf-8-sig", newline="") as stream:
            approval_rows = list(csv.DictReader(stream))
    else:
        warnings.append("缺少角色九宫格审批清单")

    required_rows = [row for row in approval_rows if row.get("需要基准图", "").strip() == "是"]
    if approval_rows and not required_rows:
        warnings.append("九宫格审批清单中没有标为需要基准图的角色")

    row_keys = [(row.get("角色编号", "").strip(), row.get("角色名", "").strip()) for row in required_rows]
    if len(row_keys) != len(set(row_keys)):
        errors.append("九宫格审批清单存在重复角色")
    role_file = project / "03_角色设定" / "00_角色总表.md"
    registered_roles: set[tuple[str, str]] = set()
    if role_file.is_file():
        registered_roles = parse_registered_roles(role_file)
        if not registered_roles:
            if gates.get("G2") == "PASS" or required_rows:
                errors.append("角色总表存在，但没有可识别的角色记录")
            else:
                warnings.append("角色总表尚未填写；进入 G2 前必须登记全部角色")
        elif set(row_keys) != registered_roles:
            missing = registered_roles - set(row_keys)
            extra = set(row_keys) - registered_roles
            details: list[str] = []
            if missing:
                details.append("清单漏列：" + "、".join(f"{item[0]}_{item[1]}" for item in sorted(missing)))
            if extra:
                details.append("清单多列：" + "、".join(f"{item[0]}_{item[1]}" for item in sorted(extra)))
            errors.append("角色总表与九宫格审批清单不一致（" + "；".join(details) + "）")
    elif required_rows:
        errors.append("已有九宫格审批记录，但缺少 03_角色设定/00_角色总表.md")

    for row in required_rows:
        role_id = row.get("角色编号", "").strip()
        role_name = row.get("角色名", "").strip()
        version = row.get("版本", "").strip()
        label = f"{role_id}_{role_name}"
        candidate_relative = row.get("候选路径", "").strip()
        if not candidate_relative:
            errors.append(f"{label}缺少候选路径")
            continue
        candidate = (project / candidate_relative).resolve()
        if not candidate.is_file():
            errors.append(f"{label}候选不存在：{candidate_relative}")
            continue
        validate_grid(candidate, candidate.with_suffix(".manifest.json"), f"{label}候选", errors)

        status = row.get("用户审批状态", "").strip().upper()
        if status in APPROVED_STATES:
            if not row.get("用户审批原话", "").strip():
                errors.append(f"{label}已标记用户通过，但用户审批原话为空")
            formal_relative = row.get("正式路径", "").strip()
            if formal_relative:
                formal = (project / formal_relative).resolve()
            else:
                formal = project / "10_角色基准图" / f"{role_id}_{role_name}" / f"角色基准九宫格_{version}.png"
            if not formal.is_file():
                errors.append(f"{label}已标记用户通过，但正式九宫格不存在")
            else:
                validate_grid(formal, formal.with_suffix(".manifest.json"), f"{label}正式锚点", errors, formal=True)
                if not (formal.parent / f"审批记录_{version}.md").is_file():
                    errors.append(f"{label}正式锚点缺少审批记录_{version}.md")

    formal_root = project / "10_角色基准图"
    formal_images = [p for p in formal_root.rglob("*") if p.suffix.lower() in IMAGE_EXTS]
    if formal_images and gates.get("G3") != "PASS":
        errors.append("存在正式角色图，但 G3 双主角正脸共同审批不是 PASS")
    for image in formal_images:
        lower = str(image).lower()
        if any(part in lower for part in FORBIDDEN_PARTS):
            errors.append(f"失败候选混入正式角色目录：{image.relative_to(project)}")

    generated_frames_root = project / "07_素材资源" / "正式图"
    generated_frames = [p for p in generated_frames_root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS] if generated_frames_root.is_dir() else []
    if generated_frames and gates.get("G4") != "PASS":
        errors.append("G4 全部角色九宫格未通过，但正式剧情静态帧已经生成")
    video_root = project / "07_素材资源" / "视频"
    videos = [p for p in video_root.rglob("*") if p.is_file() and p.suffix.lower() in VIDEO_EXTS] if video_root.is_dir() else []
    if videos and gates.get("G6") != "PASS":
        errors.append("G6 静态首尾帧未通过，但视频素材已经生成")
    audio_root = project / "07_素材资源" / "音频"
    audios = [p for p in audio_root.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTS] if audio_root.is_dir() else []
    if audios and gates.get("G7") != "PASS":
        errors.append("G7 无声样片未通过，但正式音频素材已经生成")

    if gates.get("G4") == "PASS":
        if gates.get("G3") != "PASS":
            errors.append("G4 全部角色九宫格通过，但 G3 双主角正脸未通过")
        if not required_rows:
            errors.append("G4 已 PASS，但没有可核对的必需角色清单")
        unapproved = [
            f"{row.get('角色编号', '')}_{row.get('角色名', '')}"
            for row in required_rows
            if row.get("用户审批状态", "").strip().upper() not in APPROVED_STATES
        ]
        if unapproved:
            errors.append("G4 已 PASS，但以下角色未获用户审批：" + "、".join(unapproved))

    gate_dependencies = {
        "G1": ("G0",),
        "G2": ("G0",),
        "G3": ("G2",),
        "G4": ("G3",),
        "G5": ("G1", "G4"),
        "G6": ("G5",),
        "G7": ("G6",),
        "G8": ("G7",),
        "G9": ("G8",),
    }
    for gate, dependencies in gate_dependencies.items():
        if gates.get(gate) == "PASS":
            missing_dependencies = [dependency for dependency in dependencies if gates.get(dependency) != "PASS"]
            if missing_dependencies:
                errors.append(f"{gate} 已 PASS，但前置审批未通过：" + "、".join(missing_dependencies))

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
