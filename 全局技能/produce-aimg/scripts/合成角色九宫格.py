#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import warnings
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageCms, ImageColor, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError


CELL_SIZE = 1024
GRID_SIZE = CELL_SIZE * 3
ROLE_ID_PATTERN = re.compile(r"^角色-\d+$")
VERSION_PATTERN = re.compile(r"^v\d+$")
MIRRORED_EXIF_ORIENTATIONS = {2, 4, 5, 7}
ROTATED_EXIF_ORIENTATIONS = {3, 6, 8}
CELLS = [
    {"cell": 1, "arg": "V01", "code": "V01-F0", "view": "正面标准转面"},
    {"cell": 2, "arg": "V02", "code": "V02-B180", "view": "背面"},
    {"cell": 3, "arg": "V03", "code": "V03-L90", "view": "角色自身左侧面"},
    {"cell": 4, "arg": "V04", "code": "V04-R90", "view": "角色自身右侧面"},
    {"cell": 5, "arg": "V05", "code": "V05-LF45", "view": "角色自身左前3/4"},
    {"cell": 6, "arg": "V06", "code": "V06-RF45", "view": "角色自身右前3/4"},
    {"cell": 7, "arg": "V07", "code": "V07-LB135", "view": "角色自身左后3/4"},
    {"cell": 8, "arg": "V08", "code": "V08-RB135", "view": "角色自身右后3/4"},
    {"cell": 9, "arg": "V09", "code": "V09-FULL", "view": "正面全身"},
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_unit_interval(value: str) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("必须是 0—1 之间的数字") from exc
    if not 0.0 <= number <= 1.0:
        raise argparse.ArgumentTypeError("必须是 0—1 之间的数字")
    return number


def parse_rgb(value: str) -> tuple[int, int, int]:
    try:
        color = ImageColor.getrgb(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"无效颜色：{value}") from exc
    if len(color) == 4:
        return color[:3]
    return color


def normalized_path_key(path: Path) -> str:
    return os.path.normcase(os.path.normpath(str(path)))


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def reject_duplicate_files(paths: list[Path]) -> None:
    seen: dict[str, Path] = {}
    for path in paths:
        key = normalized_path_key(path)
        if key in seen:
            raise SystemExit(f"拒绝：重复源文件：{seen[key]} 与 {path}")
        seen[key] = path

    for index, left in enumerate(paths):
        for right in paths[index + 1 :]:
            try:
                if left.samefile(right):
                    raise SystemExit(f"拒绝：两个参数指向同一文件：{left} 与 {right}")
            except OSError:
                # 路径均已通过 is_file；某些文件系统不支持 samefile 时仍由路径键与 SHA 保护。
                continue


def inspect_source(path: Path) -> dict[str, int | str | bool]:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                width, height = image.size
                orientation = int(image.getexif().get(274, 1))
                mode = image.mode
                image_format = image.format or "UNKNOWN"
    except (OSError, UnidentifiedImageError, Image.DecompressionBombWarning) as exc:
        raise SystemExit(f"拒绝：无法解码源图 {path}：{exc}") from exc
    if width <= 0 or height <= 0:
        raise SystemExit(f"拒绝：源图尺寸无效：{path}")
    if orientation in MIRRORED_EXIF_ORIENTATIONS:
        raise SystemExit(
            f"拒绝：源图含镜像 EXIF Orientation={orientation}，脚本不会翻转修补：{path}"
        )
    return {
        "width": width,
        "height": height,
        "mode": mode,
        "format": image_format,
        "exif_orientation": orientation,
        "rotation_normalized": orientation in ROTATED_EXIF_ORIENTATIONS,
    }


def srgb_profile_bytes() -> bytes:
    return ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()


def convert_to_srgb(image: Image.Image, background: tuple[int, int, int]) -> Image.Image:
    alpha: Image.Image | None = None
    if image.mode in {"RGBA", "LA"} or (image.mode == "P" and "transparency" in image.info):
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        color_image = rgba.convert("RGB")
    else:
        color_image = image

    embedded_profile = image.info.get("icc_profile")
    if embedded_profile:
        try:
            source_profile = ImageCms.ImageCmsProfile(BytesIO(embedded_profile))
            color_image = ImageCms.profileToProfile(
                color_image,
                source_profile,
                ImageCms.createProfile("sRGB"),
                outputMode="RGB",
            )
        except (ImageCms.PyCMSError, OSError, ValueError) as exc:
            raise SystemExit(f"拒绝：源图 ICC 色彩配置无法转换到 sRGB：{exc}") from exc
    else:
        color_image = color_image.convert("RGB")

    if alpha is None:
        return color_image
    flattened = Image.new("RGB", color_image.size, background)
    flattened.paste(color_image, mask=alpha)
    return flattened


def load_source(path: Path, background: tuple[int, int, int]) -> Image.Image:
    try:
        with Image.open(path) as opened:
            orientation = int(opened.getexif().get(274, 1))
            if orientation in MIRRORED_EXIF_ORIENTATIONS:
                raise SystemExit(
                    f"拒绝：源图含镜像 EXIF Orientation={orientation}，脚本不会翻转修补：{path}"
                )
            normalized = ImageOps.exif_transpose(opened)
            normalized.load()
            return convert_to_srgb(normalized, background)
    except (OSError, UnidentifiedImageError) as exc:
        raise SystemExit(f"拒绝：无法读取源图 {path}：{exc}") from exc


def render_portrait_cell(image: Image.Image, focus_x: float, focus_y: float) -> Image.Image:
    return ImageOps.fit(
        image,
        (CELL_SIZE, CELL_SIZE),
        method=Image.Resampling.LANCZOS,
        centering=(focus_x, focus_y),
    )


def render_full_body_cell(image: Image.Image, background: tuple[int, int, int]) -> Image.Image:
    fitted = ImageOps.contain(image, (CELL_SIZE, CELL_SIZE), method=Image.Resampling.LANCZOS)
    cell = Image.new("RGB", (CELL_SIZE, CELL_SIZE), background)
    offset_x = (CELL_SIZE - fitted.width) // 2
    offset_y = (CELL_SIZE - fitted.height) // 2

    # Full-body sources are usually portrait. Preserve head and shoes with contain,
    # then extend the source's own boundary pixels into any letterbox area. This
    # avoids white pillarbox seams without cropping, flipping, or regenerating the
    # character. The extension remains deterministic and changes background only.
    if offset_x > 0:
        left_edge = fitted.crop((0, 0, 1, fitted.height)).resize(
            (offset_x, fitted.height), Image.Resampling.NEAREST
        )
        right_width = CELL_SIZE - offset_x - fitted.width
        right_edge = fitted.crop((fitted.width - 1, 0, fitted.width, fitted.height)).resize(
            (right_width, fitted.height), Image.Resampling.NEAREST
        )
        cell.paste(left_edge, (0, offset_y))
        cell.paste(right_edge, (offset_x + fitted.width, offset_y))
    if offset_y > 0:
        top_edge = fitted.crop((0, 0, fitted.width, 1)).resize(
            (fitted.width, offset_y), Image.Resampling.NEAREST
        )
        bottom_height = CELL_SIZE - offset_y - fitted.height
        bottom_edge = fitted.crop((0, fitted.height - 1, fitted.width, fitted.height)).resize(
            (fitted.width, bottom_height), Image.Resampling.NEAREST
        )
        cell.paste(top_edge, (offset_x, 0))
        cell.paste(bottom_edge, (offset_x, offset_y + fitted.height))
    cell.paste(fitted, (offset_x, offset_y))
    return cell


def font_candidates(explicit: str | None) -> list[Path]:
    if explicit:
        return [Path(explicit).expanduser().resolve()]
    candidates: list[Path] = []
    windows_dir = Path(os.environ.get("WINDIR", r"C:\Windows"))
    candidates.extend(
        [
            windows_dir / "Fonts" / "msyhbd.ttc",
            windows_dir / "Fonts" / "msyh.ttc",
            windows_dir / "Fonts" / "msyhl.ttc",
            Path("/System/Library/Fonts/PingFang.ttc"),
            Path("/System/Library/Fonts/STHeiti Medium.ttc"),
            Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
            Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
            Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
        ]
    )
    return candidates


def load_label_font(explicit: str | None, size: int) -> tuple[ImageFont.FreeTypeFont, Path]:
    errors: list[str] = []
    for candidate in font_candidates(explicit):
        if not candidate.is_file():
            continue
        try:
            return ImageFont.truetype(str(candidate), size=size), candidate
        except OSError as exc:
            errors.append(f"{candidate}: {exc}")
    detail = f"（{' ; '.join(errors)}）" if errors else ""
    raise SystemExit(
        "拒绝：未找到可靠中文字体。请安装微软雅黑，或用 --字体 显式指定中文 TTF/TTC 文件"
        f"{detail}"
    )


def draw_label(cell: Image.Image, label: str, font_path: Path, requested_size: int) -> None:
    overlay = Image.new("RGBA", cell.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    margin = 24
    horizontal_padding = 22
    vertical_padding = 13
    font_size = requested_size
    while True:
        font = ImageFont.truetype(str(font_path), size=font_size)
        left, top, right, bottom = draw.textbbox((0, 0), label, font=font, stroke_width=1)
        text_width = right - left
        text_height = bottom - top
        if text_width + horizontal_padding * 2 <= CELL_SIZE - margin * 2:
            break
        font_size -= 2
        if font_size < 20:
            raise SystemExit(f"拒绝：标签过长，无法可靠绘制：{label}")

    box_width = text_width + horizontal_padding * 2
    box_height = text_height + vertical_padding * 2
    x0 = margin
    y0 = CELL_SIZE - margin - box_height
    draw.rounded_rectangle(
        (x0, y0, x0 + box_width, y0 + box_height),
        radius=14,
        fill=(0, 0, 0, 205),
        outline=(255, 255, 255, 190),
        width=2,
    )
    text_x = x0 + horizontal_padding - left
    text_y = y0 + vertical_padding - top
    draw.text(
        (text_x, text_y),
        label,
        font=font,
        fill=(255, 255, 255, 255),
        stroke_width=1,
        stroke_fill=(0, 0, 0, 255),
    )
    cell.paste(overlay.convert("RGB"), mask=overlay.getchannel("A"))


def output_sha_from_temporary(path: Path) -> str:
    return sha256(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="按 AIMG 固定方向协议合成 3072×3072 单角色九宫格及兼容 manifest",
        allow_abbrev=False,
    )
    for cell in CELLS:
        parser.add_argument(
            f"--{cell['arg']}",
            required=True,
            metavar="图片路径",
            help=f"{cell['code']} {cell['view']}",
        )
    parser.add_argument("--角色编号", required=True, help="例如：角色-001")
    parser.add_argument("--角色名", required=True)
    parser.add_argument("--版本", required=True, help="例如：v1")
    parser.add_argument("--输出", required=True, help="输出 PNG；manifest 自动写到同名 .manifest.json")
    parser.add_argument(
        "--项目根目录",
        help="可选；提供后要求九张源图和输出均位于项目内，并在 manifest 写项目相对路径",
    )
    parser.add_argument(
        "--人像重心X",
        "--portrait-focus-x",
        dest="portrait_focus_x",
        type=parse_unit_interval,
        default=0.50,
        metavar="0..1",
        help="V01–V08 共用水平裁切重心，默认 0.50",
    )
    parser.add_argument(
        "--人像重心Y",
        "--portrait-focus-y",
        dest="portrait_focus_y",
        type=parse_unit_interval,
        default=0.08,
        metavar="0..1",
        help="V01–V08 共用垂直裁切重心，0 为顶部，默认偏上 0.08",
    )
    parser.add_argument("--背景色", type=parse_rgb, default=parse_rgb("#F2F2F2"), help="V09 完整适配留白色")
    parser.add_argument("--字体", help="中文 TTF/TTC；默认优先微软雅黑")
    parser.add_argument("--标签字号", type=int, default=44, help="默认 44")
    parser.add_argument("--方向已人工复核", action="store_true")
    parser.add_argument("--禁止镜像已人工复核", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.方向已人工复核 or not args.禁止镜像已人工复核:
        raise SystemExit("拒绝：必须显式传入 --方向已人工复核 和 --禁止镜像已人工复核")
    if not ROLE_ID_PATTERN.fullmatch(args.角色编号.strip()):
        raise SystemExit("拒绝：角色编号必须为 角色-001 格式")
    if not args.角色名.strip():
        raise SystemExit("拒绝：角色名不能为空")
    if not VERSION_PATTERN.fullmatch(args.版本.strip()):
        raise SystemExit("拒绝：版本必须为 v1、v2 等 v+数字格式")
    if not 20 <= args.标签字号 <= 96:
        raise SystemExit("拒绝：标签字号必须在 20—96 之间")

    output = Path(args.输出).expanduser().resolve()
    if output.suffix.lower() != ".png":
        raise SystemExit("拒绝：输出必须是 .png")
    manifest_path = output.with_suffix(".manifest.json")
    if output.exists() or manifest_path.exists():
        raise SystemExit("拒绝：输出 PNG 或 manifest 已存在，请显式使用新版本路径")

    sources = [Path(getattr(args, cell["arg"])).expanduser().resolve() for cell in CELLS]
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise SystemExit("拒绝：缺少源图：\n- " + "\n- ".join(missing))
    if normalized_path_key(output) in {normalized_path_key(path) for path in sources}:
        raise SystemExit("拒绝：输出路径不能与任一源图相同")
    project_root = Path(args.项目根目录).expanduser().resolve() if args.项目根目录 else None
    if project_root is not None:
        if not project_root.is_dir():
            raise SystemExit("拒绝：项目根目录不存在")
        outside = [path for path in [*sources, output] if not is_within(path, project_root)]
        if outside:
            raise SystemExit("拒绝：源图或输出不在项目根目录内：\n- " + "\n- ".join(map(str, outside)))
    reject_duplicate_files(sources)

    source_hashes = [sha256(path) for path in sources]
    hashes_to_cells: dict[str, list[str]] = {}
    for cell, digest in zip(CELLS, source_hashes):
        hashes_to_cells.setdefault(digest, []).append(cell["code"])
    duplicate_hashes = {digest: codes for digest, codes in hashes_to_cells.items() if len(codes) > 1}
    if duplicate_hashes:
        details = "; ".join(f"{','.join(codes)}={digest}" for digest, codes in duplicate_hashes.items())
        raise SystemExit(f"拒绝：不同参数的源图 SHA256 重复：{details}")

    source_info = [inspect_source(path) for path in sources]
    _, font_path = load_label_font(args.字体, args.标签字号)
    output.parent.mkdir(parents=True, exist_ok=True)
    grid = Image.new("RGB", (GRID_SIZE, GRID_SIZE), args.背景色)
    manifest_cells: list[dict[str, object]] = []

    for index, (cell_spec, source, digest, info) in enumerate(
        zip(CELLS, sources, source_hashes, source_info)
    ):
        source_image = load_source(source, args.背景色)
        if index < 8:
            rendered = render_portrait_cell(
                source_image,
                args.portrait_focus_x,
                args.portrait_focus_y,
            )
            render_manifest: dict[str, object] = {
                "mode": "portrait_smart_crop_fill_v1",
                "target_width": CELL_SIZE,
                "target_height": CELL_SIZE,
                "focus_x": args.portrait_focus_x,
                "focus_y": args.portrait_focus_y,
                "resampling": "LANCZOS",
                "flip": False,
            }
        else:
            rendered = render_full_body_cell(source_image, args.背景色)
            render_manifest = {
                "mode": "contain_no_crop_edge_extend_v1",
                "target_width": CELL_SIZE,
                "target_height": CELL_SIZE,
                "background_rgb": list(args.背景色),
                "resampling": "LANCZOS",
                "crop": False,
                "flip": False,
                "letterbox_fill": "source_boundary_pixel_extension",
            }
        draw_label(rendered, f"{cell_spec['code']} | {cell_spec['view']}", font_path, args.标签字号)
        column = index % 3
        row = index // 3
        grid.paste(rendered, (column * CELL_SIZE, row * CELL_SIZE))
        manifest_cells.append(
            {
                "cell": cell_spec["cell"],
                "code": cell_spec["code"],
                "view": cell_spec["view"],
                "source_path": (
                    source.relative_to(project_root).as_posix()
                    if project_root is not None
                    else source.as_posix()
                ),
                "source_sha256": digest,
                "source_width": info["width"],
                "source_height": info["height"],
                "source_mode": info["mode"],
                "source_format": info["format"],
                "source_exif_orientation": info["exif_orientation"],
                "source_rotation_normalized": info["rotation_normalized"],
                "render": render_manifest,
            }
        )

    image_temp: Path | None = None
    manifest_temp: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{output.stem}.", suffix=".png.tmp", dir=output.parent, delete=False
        ) as stream:
            image_temp = Path(stream.name)
        grid.save(
            image_temp,
            format="PNG",
            icc_profile=srgb_profile_bytes(),
            compress_level=6,
            optimize=False,
        )
        output_digest = output_sha_from_temporary(image_temp)
        manifest = {
            "schema": "aimg-character-grid/v1",
            "status": "REVIEW",
            "role_id": args.角色编号.strip(),
            "role_name": args.角色名.strip(),
            "version": args.版本.strip(),
            "image_file": output.name,
            "sha256": output_digest,
            "width": GRID_SIZE,
            "height": GRID_SIZE,
            "cell_width": CELL_SIZE,
            "cell_height": CELL_SIZE,
            "direction_basis": "character_self",
            "mirror_generated": False,
            "color_space": "sRGB",
            "source_path_basis": "project_relative" if project_root is not None else "absolute",
            "label_font": font_path.as_posix(),
            "cells": manifest_cells,
            "qa": {
                "directions_manually_verified": True,
                "mirror_prohibited_and_verified": True,
                "user_approval": "REVIEW",
            },
        }
        manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=f".{output.stem}.",
            suffix=".manifest.json.tmp",
            dir=output.parent,
            delete=False,
        ) as stream:
            manifest_temp = Path(stream.name)
            stream.write(manifest_text)
            stream.flush()
            os.fsync(stream.fileno())

        image_temp.replace(output)
        image_temp = None
        try:
            manifest_temp.replace(manifest_path)
            manifest_temp = None
        except OSError:
            output.unlink(missing_ok=True)
            raise
    finally:
        if image_temp is not None:
            image_temp.unlink(missing_ok=True)
        if manifest_temp is not None:
            manifest_temp.unlink(missing_ok=True)

    print(f"已合成角色九宫格：{output}")
    print(f"已创建兼容清单：{manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
