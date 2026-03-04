from __future__ import annotations

from io import BytesIO
from pathlib import Path

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile, InputMediaPhoto

_BG_COLOR = "#f4f7fb"
_CARD_COLOR = "#ffffff"
_HEADER_BG = "#1f6feb"
_HEADER_TEXT = "#ffffff"
_TITLE_COLOR = "#0b1f44"
_TEXT_COLOR = "#102a43"
_MUTED_TEXT = "#486581"
_BORDER = "#d9e2ec"
_ROW_ALT = "#f8fbff"


_FONT_PATHS = [
    "DejaVuSans.ttf",
    "Arial.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def _load_font(size: int, bold: bool = False):
    from PIL import ImageFont

    candidates = []
    if bold:
        candidates.extend(
            [
                "DejaVuSans-Bold.ttf",
                "Arial Bold.ttf",
                "arialbd.ttf",
                "C:/Windows/Fonts/arialbd.ttf",
                "C:/Windows/Fonts/seguisb.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            ]
        )

    candidates.extend(_FONT_PATHS)

    for path in candidates:
        if Path(path).is_absolute() and not Path(path).exists():
            continue
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue

    return ImageFont.load_default()


def _text_size(draw, text: str, font) -> tuple[int, int]:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def build_table_image(
    *,
    title: str,
    columns: list[str],
    rows: list[list[str]],
    subtitle: str | None = None,
    footer_lines: list[str] | None = None,
    equal_column_width: bool = False,
    column_width: int | None = None,
    min_rows: int | None = None,
) -> bytes:
    from PIL import Image, ImageDraw

    title_font = _load_font(34, bold=True)
    subtitle_font = _load_font(22)
    header_font = _load_font(23, bold=True)
    body_font = _load_font(22)
    footer_font = _load_font(21, bold=True)

    tmp = Image.new("RGB", (10, 10), _BG_COLOR)
    draw = ImageDraw.Draw(tmp)

    col_widths: list[int] = []
    for col_index, col in enumerate(columns):
        max_width, _ = _text_size(draw, col, header_font)
        for row in rows:
            cell = row[col_index] if col_index < len(row) else ""
            cell_width, _ = _text_size(draw, cell, body_font)
            max_width = max(max_width, cell_width)
        col_widths.append(max_width + 34)

    if equal_column_width and col_widths:
        enforced_width = max(col_widths)
        if column_width is not None:
            enforced_width = max(enforced_width, column_width)
        col_widths = [enforced_width] * len(col_widths)

    side_padding = 34
    cell_padding_y = 18
    table_width = sum(col_widths)
    image_width = max(900, table_width + side_padding * 2)

    title_h = _text_size(draw, title, title_font)[1]
    subtitle_h = _text_size(draw, subtitle or "", subtitle_font)[1] if subtitle else 0
    header_h = _text_size(draw, "Ag", header_font)[1] + cell_padding_y * 2
    row_h = _text_size(draw, "Ag", body_font)[1] + cell_padding_y * 2
    footer_h = (_text_size(draw, "Ag", footer_font)[1] + 12) * len(footer_lines or [])

    top_pad = 28
    text_gap = 16
    table_top = top_pad + title_h + (subtitle_h + 8 if subtitle else 0) + text_gap
    row_count = max(1, len(rows), min_rows or 0)
    table_h = header_h + row_count * row_h
    image_height = table_top + table_h + footer_h + 44

    img = Image.new("RGB", (image_width, image_height), _BG_COLOR)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((12, 12, image_width - 12, image_height - 12), radius=18, fill=_CARD_COLOR, outline=_BORDER, width=2)

    draw.text((side_padding, top_pad), title, font=title_font, fill=_TITLE_COLOR)
    if subtitle:
        draw.text((side_padding, top_pad + title_h + 8), subtitle, font=subtitle_font, fill=_MUTED_TEXT)

    x = side_padding
    y = table_top
    draw.rounded_rectangle((x, y, x + table_width, y + header_h), radius=12, fill=_HEADER_BG)

    cursor_x = x
    for idx, col in enumerate(columns):
        draw.text((cursor_x + 16, y + cell_padding_y), col, font=header_font, fill=_HEADER_TEXT)
        if idx > 0:
            draw.line((cursor_x, y, cursor_x, y + table_h), fill=_BORDER, width=1)
        cursor_x += col_widths[idx]

    y += header_h
    if rows:
        padded_rows = rows
        if min_rows and len(rows) < min_rows:
            padded_rows = rows + [["" for _ in columns] for _ in range(min_rows - len(rows))]

        for row_idx, row in enumerate(padded_rows):
            row_bg = _ROW_ALT if row_idx % 2 == 0 else _CARD_COLOR
            draw.rectangle((x, y, x + table_width, y + row_h), fill=row_bg)
            cursor_x = x
            for col_idx, width in enumerate(col_widths):
                cell = row[col_idx] if col_idx < len(row) else ""
                draw.text((cursor_x + 16, y + cell_padding_y), cell, font=body_font, fill=_TEXT_COLOR)
                cursor_x += width
            draw.line((x, y + row_h, x + table_width, y + row_h), fill=_BORDER, width=1)
            y += row_h
    else:
        draw.rectangle((x, y, x + table_width, y + row_h), fill=_CARD_COLOR)
        draw.text((x + 16, y + cell_padding_y), "Маълумот йўқ", font=body_font, fill=_MUTED_TEXT)
        draw.line((x, y + row_h, x + table_width, y + row_h), fill=_BORDER, width=1)
        y += row_h

    if footer_lines:
        y += 14
        for line in footer_lines:
            draw.text((side_padding, y), line, font=footer_font, fill=_TITLE_COLOR)
            y += _text_size(draw, line, footer_font)[1] + 12

    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


async def send_or_edit_table_image(target, image_bytes: bytes, keyboard, edit: bool):
    file = BufferedInputFile(image_bytes, filename="table.png")

    if edit:
        try:
            await target.edit_media(media=InputMediaPhoto(media=file), reply_markup=keyboard)
            return
        except TelegramBadRequest:
            pass

    await target.answer_photo(photo=file, reply_markup=keyboard)
    if edit:
        try:
            await target.delete()
        except TelegramBadRequest:
            pass
