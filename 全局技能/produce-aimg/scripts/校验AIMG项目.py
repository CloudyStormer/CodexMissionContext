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
ROLE_DIR_PATTERN = re.compile(r"^(角色-\d+)_(.+)$")
VERSION_PATTERN = re.compile(r"^v\d+$")
WINDOWS_INVALID_COMPONENT_CHARS = set('<>:"/\\|?*')
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


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def project_path(project: Path, raw: str, label: str, errors: list[str]) -> Path | None:
    if not raw:
        errors.append(f"{label}为空")
        return None
    resolved = (project / raw).resolve()
    if not is_within(resolved, project):
        errors.append(f"{label}不在项目内：{raw}")
        return None
    return resolved


def safe_role_name(name: str) -> bool:
    return bool(
        name
        and name not in {".", ".."}
        and "." not in name
        and not any(char in WINDOWS_INVALID_COMPONENT_CHARS or ord(char) < 32 for char in name)
        and not name.endswith(" ")
    )


def safe_role_root(formal_root: Path, label: str, role_name: str) -> Path | None:
    if not safe_role_name(role_name):
        return None
    role_root = (formal_root / label).resolve()
    if role_root.parent != formal_root or role_root.name != label:
        return None
    return role_root


def parse_registered_roles(path: Path) -> set[tuple[str, str]]:
    roles: set[tuple[str, str]] = set()
    pattern = re.compile(r"^\|\s*(角色-\d+)\s*\|\s*([^|]+?)\s*\|")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            roles.add((match.group(1).strip(), match.group(2).strip()))
    return roles


def validate_grid(
    project: Path,
    image: Path,
    manifest_path: Path,
    label: str,
    errors: list[str],
    formal: bool = False,
    expected_role_id: str = "",
    expected_role_name: str = "",
    expected_version: str = "",
    history: bool = False,
) -> None:
    for path, path_kind in ((image, "图片"), (manifest_path, "manifest")):
        if not is_within(path.resolve(), project):
            errors.append(f"{label}的{path_kind}不在项目内")
            return
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
    if manifest.get("role_id") != expected_role_id:
        errors.append(f"{label}的 manifest 角色编号与审批清单不一致")
    if manifest.get("role_name") != expected_role_name:
        errors.append(f"{label}的 manifest 角色名与审批清单不一致")
    if manifest.get("version") != expected_version:
        errors.append(f"{label}的 manifest 版本与审批清单不一致")
    if manifest.get("image_file") != image.name:
        errors.append(f"{label}的 manifest image_file 与实际图片文件名不一致")
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
    elif history:
        if manifest.get("status") != "SUPERSEDED":
            errors.append(f"{label}的历史 manifest 必须为 SUPERSEDED")
    elif manifest.get("status") != "REVIEW":
        errors.append(f"{label}的候选 manifest 必须为 REVIEW")

    path_values: list[tuple[str, str]] = []
    for cell in cells if isinstance(cells, list) else []:
        if isinstance(cell, dict) and str(cell.get("source_path", "")).strip():
            path_values.append((f"{label}的 source_path", str(cell["source_path"]).strip()))
    if str(manifest.get("source_candidate", "")).strip():
        path_values.append((f"{label}的 source_candidate", str(manifest["source_candidate"]).strip()))
    for path_label, raw_path in path_values:
        referenced = project_path(project, raw_path, path_label, errors)
        if referenced is not None and not referenced.is_file():
            errors.append(f"{path_label}指向的文件不存在：{raw_path}")


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

    if approval_rows and "审批绑定SHA256" not in approval_rows[0]:
        errors.append("九宫格审批清单缺少审批绑定SHA256列")

    row_keys = [(row.get("角色编号", "").strip(), row.get("角色名", "").strip()) for row in required_rows]
    if len(row_keys) != len(set(row_keys)):
        errors.append("九宫格审批清单存在重复角色")
    role_ids = [
        row.get("角色编号", "").strip()
        for row in approval_rows
        if row.get("角色编号", "").strip()
    ]
    if len(role_ids) != len(set(role_ids)):
        errors.append("九宫格审批清单存在同角色编号重复行")
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

    declared_candidates: set[Path] = set()
    declared_formals: set[Path] = set()
    declared_formal_files: set[Path] = set()
    formal_root = (project / "10_角色基准图").resolve()
    for row in required_rows:
        role_id = row.get("角色编号", "").strip()
        role_name = row.get("角色名", "").strip()
        version = row.get("版本", "").strip()
        label = f"{role_id}_{role_name}"
        if not ROLE_DIR_PATTERN.fullmatch(label) or not safe_role_name(role_name):
            errors.append(f"{label}的角色编号或角色名不合规")
            continue
        role_root = safe_role_root(formal_root, label, role_name)
        if role_root is None:
            errors.append(f"{label}必须是 10_角色基准图 下的单一安全目录组件")
            continue
        if not VERSION_PATTERN.fullmatch(version):
            errors.append(f"{label}的版本必须为 vN")
        candidate_relative = row.get("候选路径", "").strip()
        candidate = project_path(project, candidate_relative, f"{label}候选路径", errors)
        if candidate is None:
            continue
        candidate_dir = (role_root / "00_待审批").resolve()
        if candidate.parent != candidate_dir:
            errors.append(f"{label}当前候选必须物理位于 10_角色基准图/{label}/00_待审批/")
        if not candidate.is_file():
            errors.append(f"{label}候选不存在：{candidate_relative}")
            continue
        declared_candidates.add(candidate)
        candidate_manifest = candidate.with_suffix(".manifest.json")
        if candidate_dir.is_dir():
            current_images = sorted(
                path.resolve() for path in candidate_dir.iterdir()
                if path.is_file() and path.suffix.lower() in IMAGE_EXTS
            )
            current_manifests = sorted(
                path.resolve() for path in candidate_dir.iterdir()
                if path.is_file() and path.name.endswith(".manifest.json")
            )
            if current_images != [candidate]:
                errors.append(f"{label}的 00_待审批 只允许保留审批清单当前一张候选")
            if current_manifests != [candidate_manifest]:
                errors.append(f"{label}的 00_待审批 只允许保留当前候选的一份 manifest")
        validate_grid(
            project,
            candidate,
            candidate_manifest,
            f"{label}候选",
            errors,
            expected_role_id=role_id,
            expected_role_name=role_name,
            expected_version=version,
        )

        status = row.get("用户审批状态", "").strip().upper()
        candidate_hash = sha256(candidate)
        approval_hash = row.get("审批绑定SHA256", "").strip().lower()
        if approval_hash and approval_hash != candidate_hash:
            errors.append(f"{label}的审批绑定SHA256与当前候选不一致")
        formal_relative = row.get("正式路径", "").strip()
        role_formal_dir = (role_root / "01_正式锚点").resolve()
        if formal_relative and status not in APPROVED_STATES:
            errors.append(f"{label}未获用户通过却已填写正式路径")
        if formal_relative:
            project_path(project, formal_relative, f"{label}正式路径", errors)
        if status in APPROVED_STATES:
            if not row.get("用户审批原话", "").strip():
                errors.append(f"{label}已标记用户通过，但用户审批原话为空")
            if not approval_hash:
                errors.append(f"{label}已标记用户通过，但审批绑定SHA256为空")
            expected_formal = (
                role_formal_dir / f"角色基准九宫格_{version}.png"
            ).resolve()
            formal = project_path(project, formal_relative, f"{label}正式路径", errors)
            if formal is None:
                continue
            if formal != expected_formal:
                errors.append(f"{label}正式锚点必须位于 01_正式锚点 且使用当前版本标准文件名")
            declared_formals.add(expected_formal)
            expected_formal_manifest = expected_formal.with_suffix(".manifest.json")
            expected_approval_record = role_formal_dir / f"审批记录_{version}.md"
            expected_formal_files = {
                expected_formal,
                expected_formal_manifest.resolve(),
                expected_approval_record.resolve(),
            }
            declared_formal_files.update(expected_formal_files)
            if not formal.is_file():
                errors.append(f"{label}已标记用户通过，但正式九宫格不存在")
            else:
                validate_grid(
                    project,
                    formal,
                    expected_formal_manifest,
                    f"{label}正式锚点",
                    errors,
                    formal=True,
                    expected_role_id=role_id,
                    expected_role_name=role_name,
                    expected_version=version,
                )
                formal_hash = sha256(formal)
                if formal_hash != candidate_hash:
                    errors.append(f"{label}正式锚点与当前候选 PNG 的 SHA256 不一致")
                if formal_hash != approval_hash:
                    errors.append(f"{label}正式锚点与审批绑定SHA256不一致")
                try:
                    formal_manifest = json.loads(expected_formal_manifest.read_text(encoding="utf-8"))
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    formal_manifest = None
                if isinstance(formal_manifest, dict):
                    if formal_manifest.get("source_candidate") != candidate_relative:
                        errors.append(f"{label}正式 manifest source_candidate 必须精确等于 CSV 候选路径")
                    expected_status = row.get("用户审批状态", "").strip()
                    expected_quote = row.get("用户审批原话", "").strip()
                    if formal_manifest.get("user_approval_status") != expected_status:
                        errors.append(f"{label}正式 manifest user_approval_status 与 CSV 不一致")
                    if formal_manifest.get("user_approval_quote") != expected_quote:
                        errors.append(f"{label}正式 manifest user_approval_quote 与 CSV 不一致")
                if not expected_approval_record.is_file():
                    errors.append(f"{label}正式锚点缺少审批记录_{version}.md")
            if role_formal_dir.is_dir():
                actual_formal_files = {
                    path.resolve() for path in role_formal_dir.iterdir() if path.is_file()
                }
                nested_formal_dirs = [path for path in role_formal_dir.iterdir() if path.is_dir()]
                if actual_formal_files != expected_formal_files or nested_formal_dirs:
                    errors.append(f"{label}的 01_正式锚点 只允许保留当前版本 PNG、manifest 和审批记录")
        elif role_formal_dir.is_dir() and any(role_formal_dir.iterdir()):
            errors.append(f"{label}未获用户通过，01_正式锚点 必须为空")

    all_baseline_images = [
        path for path in formal_root.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS
    ]
    formal_images: list[Path] = []
    candidate_images: list[Path] = []
    for image in all_baseline_images:
        relative_parts = image.relative_to(formal_root).parts
        role_dir_valid = bool(relative_parts and ROLE_DIR_PATTERN.fullmatch(relative_parts[0]))
        if len(relative_parts) == 3 and role_dir_valid and relative_parts[1] == "00_待审批":
            candidate_images.append(image)
        elif len(relative_parts) == 3 and role_dir_valid and relative_parts[1] == "01_正式锚点":
            formal_images.append(image)
        elif len(relative_parts) >= 2 and relative_parts[1] == "02_历史锚点":
            continue
        else:
            errors.append(f"角色图未放入规范的待审批、正式或历史锚点目录：{image.relative_to(project)}")
    for image in candidate_images:
        if image.resolve() not in declared_candidates:
            errors.append(f"00_待审批 中存在审批清单未登记的候选：{image.relative_to(project)}")
    for image in formal_images:
        if image.resolve() not in declared_formals:
            errors.append(f"01_正式锚点 中存在未绑定当前审批记录的图片：{image.relative_to(project)}")
    for active_dir in formal_root.rglob("01_正式锚点"):
        if not active_dir.is_dir():
            continue
        for entry in active_dir.iterdir():
            if entry.resolve() not in declared_formal_files:
                errors.append(f"01_正式锚点 只允许当前正式包：{entry.relative_to(project)}")

    for role_root in (path for path in formal_root.iterdir() if path.is_dir()):
        role_match = ROLE_DIR_PATTERN.fullmatch(role_root.name)
        if not role_match:
            continue
        role_id, role_name = role_match.groups()
        expected_role_root = safe_role_root(formal_root, role_root.name, role_name)
        if expected_role_root is None or expected_role_root != role_root.resolve():
            errors.append(f"历史锚点所在的角色目录不安全：{role_root.relative_to(project)}")
            continue
        history_root = role_root / "02_历史锚点"
        if not history_root.exists():
            continue
        if not history_root.is_dir():
            errors.append(f"02_历史锚点必须是目录：{history_root.relative_to(project)}")
            continue
        for entry in history_root.iterdir():
            if not entry.is_dir() or not VERSION_PATTERN.fullmatch(entry.name):
                errors.append(f"02_历史锚点只允许 vN 版本目录：{entry.relative_to(project)}")
                continue
            history_version = entry.name
            expected_image = entry / f"角色基准九宫格_{history_version}.png"
            expected_manifest = expected_image.with_suffix(".manifest.json")
            expected_record = entry / f"审批记录_{history_version}.md"
            expected_files = {
                expected_image.resolve(),
                expected_manifest.resolve(),
                expected_record.resolve(),
            }
            actual_files = {path.resolve() for path in entry.iterdir() if path.is_file()}
            nested_dirs = [path for path in entry.iterdir() if path.is_dir()]
            if actual_files != expected_files or nested_dirs:
                errors.append(f"历史锚点 {role_root.name}/{history_version} 必须恰有标准 PNG、manifest 和审批记录")
                continue
            validate_grid(
                project,
                expected_image,
                expected_manifest,
                f"{role_root.name}历史锚点 {history_version}",
                errors,
                expected_role_id=role_id,
                expected_role_name=role_name,
                expected_version=history_version,
                history=True,
            )
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
