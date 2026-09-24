#!/usr/bin/env python3
"""Build the manuscript PDF for the QEC [[14,3,5]] proof.

This deliberately small renderer keeps the manuscript source in Markdown while
making the final artifact deterministic and inspectable with standard PDF
tools.  It is not intended to be a general Markdown implementation.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    HRFlowable,
    LongTable,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    TableStyle,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FONT_ROOT = (
    Path.home()
    / ".cache/codex-runtimes/codex-primary-runtime/dependencies/native/"
    "libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype"
)


def register_fonts() -> None:
    """Register bundled fonts, with a system-font fallback for portability."""

    candidates = [
        FONT_ROOT,
        Path("/System/Library/Fonts/Supplemental"),
        Path("/usr/share/fonts/truetype/liberation2"),
        Path("/usr/share/fonts/truetype/dejavu"),
    ]

    def find(*names: str) -> Path:
        for directory in candidates:
            for name in names:
                path = directory / name
                if path.exists():
                    return path
        raise FileNotFoundError(f"could not find any of {names!r}")

    regular_font = find("LiberationSerif-Regular.ttf", "STIXTwoText.ttf", "DejaVuSerif.ttf")
    pdfmetrics.registerFont(TTFont("QECBody", str(regular_font)))
    pdfmetrics.registerFont(
        TTFont("QECBody-Bold", str(find("LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf")))
    )
    pdfmetrics.registerFont(
        TTFont(
            "QECBody-Italic",
            str(find("LiberationSerif-Italic.ttf", "STIXTwoText-Italic.ttf", "DejaVuSerif-Italic.ttf")),
        )
    )
    math_font = FONT_ROOT / "DejaVuSerif.ttf"
    if not math_font.exists():
        math_font = find("DejaVuSerif.ttf", "LiberationSerif-Regular.ttf")
    pdfmetrics.registerFont(TTFont("QECMath", str(math_font)))
    pdfmetrics.registerFont(TTFont("QECMono", str(find("DejaVuSansMono.ttf"))))
    # A few ReportLab internals can request the legacy default name for an
    # empty text object.  Alias that name to the embedded regular face so the
    # final PDF has no unembedded standard-font resource.
    pdfmetrics.registerFont(TTFont("Helvetica", str(regular_font)))


SUBSCRIPT_DIGITS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUBSCRIPT_LETTERS = str.maketrans({
    "a": "ₐ",
    "e": "ₑ",
    "h": "ₕ",
    "i": "ᵢ",
    "j": "ⱼ",
    "k": "ₖ",
    "l": "ₗ",
    "m": "ₘ",
    "n": "ₙ",
    "o": "ₒ",
    "p": "ₚ",
    "r": "ᵣ",
    "s": "ₛ",
    "t": "ₜ",
    "u": "ᵤ",
    "v": "ᵥ",
    "x": "ₓ",
})
SUPERSCRIPT_CHARS = str.maketrans({
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
    "-": "⁻",
    "+": "⁺",
    "(": "⁽",
    ")": "⁾",
    "a": "ᵃ",
    "e": "ᵉ",
    "h": "ʰ",
    "i": "ⁱ",
    "j": "ʲ",
    "k": "ᵏ",
    "l": "ˡ",
    "m": "ᵐ",
    "n": "ⁿ",
    "o": "ᵒ",
    "p": "ᵖ",
    "r": "ʳ",
    "s": "ˢ",
    "t": "ᵗ",
    "u": "ᵘ",
    "v": "ᵛ",
    "w": "ʷ",
    "x": "ˣ",
    "y": "ʸ",
    "z": "ᶻ",
})


def _subscript(value: str) -> str:
    return value.translate(SUBSCRIPT_DIGITS).translate(SUBSCRIPT_LETTERS)


def _superscript(value: str) -> str:
    return value.translate(SUPERSCRIPT_CHARS)


def unicode_math(value: str) -> str:
    """Make the manuscript's compact source notation readable in the PDF."""

    value = value.replace(">=", "≥").replace("<=", "≤").replace("!=", "≠")
    value = value.replace("^perp", "⊥")
    value = value.replace("->", "→").replace("orthogonal-sum", "⊕")
    value = re.sub(r"\bintersect\b", "∩", value)
    value = re.sub(r"\s+⊥\s+", "⊥", value)
    value = re.sub(r"\bsum\s+H", "∑ H", value)
    value = re.sub(r"\bsum_\(", "∑(", value)
    value = re.sub(r"\bperp\b", "⊥", value)
    value = re.sub(r"\bsum_([A-Za-z0-9]+)", lambda m: "∑" + _subscript(m.group(1)), value)
    value = re.sub(r"\b(lambda|nu|dot|in)\b", lambda m: {
        "lambda": "λ",
        "nu": "ν",
        "dot": "·",
        "in": "∈",
    }[m.group(1)], value)
    value = re.sub(r"_([0-9]+)", lambda m: _subscript(m.group(1)), value)
    value = re.sub(r"_([a-z])", lambda m: _subscript(m.group(1)), value)
    value = re.sub(r"\bN_\{([^{}]+)\}", r"N(\1)", value)
    value = value.replace("_(", "(")
    value = re.sub(r"\^\(([^()]*)\)", lambda m: _superscript(m.group(1)), value)
    value = re.sub(r"\^(-?[0-9]+|[A-Za-z])", lambda m: _superscript(m.group(1)), value)
    value = re.sub(r"<([A-Za-z0-9]+)>", r"⟨\1⟩", value)
    value = re.sub(r"\s\\\s", r" \\ ", value)
    return value


def is_math_fragment(value: str) -> bool:
    """Avoid changing literal paths and package names in inline code."""

    if any(token in value for token in ("/", ".py", ".mjs", ".json", "https://", "requirements-")) and not re.search(
        r"(?:->|\^|\bintersect\b|orthogonal-sum)", value
    ):
        return False
    return bool(re.search(r"(?:>=|<=|!=|->|\^|_\(|_[0-9a-z]|\bsum\s+H|orthogonal-sum|\b(?:lambda|nu|dot|in|perp|sum_)\b|<[A-Za-z0-9]+>)", value))


def math_markup(value: str) -> str:
    """Render compact source math with real subscript/superscript markup."""

    value = value.strip()
    value = value.replace(">=", "≥").replace("<=", "≤").replace("!=", "≠")
    value = value.replace("^perp", "⊥").replace("->", "→")
    value = value.replace("orthogonal-sum", "⊕")
    value = re.sub(r"\bintersect\b", "∩", value)
    value = re.sub(r"\bperp\b", "⊥", value)
    value = re.sub(r"\b(lambda|nu|dot|in)\b", lambda m: {
        "lambda": "λ",
        "nu": "ν",
        "dot": "·",
        "in": "∈",
    }[m.group(1)], value)
    value = re.sub(r"<([A-Za-z0-9]+)>", r"⟨\1⟩", value)
    value = re.sub(r"\s\\\s", r" \\ ", value)
    value = escape(value)
    value = re.sub(r"\bsum\s+H", "∑ H", value)
    value = re.sub(r"\bsum_\(", "∑(", value)
    value = re.sub(r"\bsum_([A-Za-z0-9]+)", r"∑<sub>\1</sub>", value)
    value = re.sub(r"_\{([^{}]+)\}", r"<sub>\1</sub>", value)
    value = re.sub(r"_\(([^()]*)\)", r"<sub>(\1)</sub>", value)
    value = re.sub(r"_([A-Za-z0-9]+)", r"<sub>\1</sub>", value)
    value = re.sub(r"\^\(([^()]*)\)", r"<super>(\1)</super>", value)
    value = re.sub(r"\^(-?[0-9]+|[A-Za-z]+)", r"<super>\1</super>", value)
    return f'<font name="QECMath">{value}</font>'


def inline_markup(text: str) -> str:
    """Convert the small Markdown inline subset used by the manuscript."""

    protected: list[str] = []

    def protect(value: str) -> str:
        token = f"\x00{len(protected)}\x00"
        protected.append(value)
        return token

    # Relative repository links are intentionally rendered as readable labels;
    # external DOI links remain visible through their label in the PDF text.
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: protect(escape(match.group(1))),
        text,
    )
    text = re.sub(
        r"`([^`]+)`",
        lambda match: protect(
            (
                math_markup(match.group(1))
                if is_math_fragment(match.group(1))
                else f'<font name="QECMono">{escape(match.group(1))}</font>'
            )
        ),
        text,
    )
    # Apply only unambiguous mathematical typography to prose outside code
    # spans. Protected code and links contain NUL tokens and are untouched.
    text = text.replace(">=", "≥").replace("<=", "≤").replace("!=", "≠")
    text = text.replace("^perp", "⊥").replace("_(", "(")
    text = text.replace("->", "→").replace("orthogonal-sum", "⊕")
    text = re.sub(r"\bN_\{([^{}]+)\}", r"N(\1)", text)
    text = re.sub(r"\b([A-Za-z]+)_([0-9]+)\b", lambda m: m.group(1) + _subscript(m.group(2)), text)
    text = re.sub(r"\b([A-Za-z]+)_([a-z])\b", lambda m: m.group(1) + _subscript(m.group(2)), text)
    text = re.sub(r"\bsum(?=\s+H(?:\s|=))", "∑", text)
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", text)
    for index, value in enumerate(protected):
        text = text.replace(f"\x00{index}\x00", value)
    return text


def table_row(line: str) -> list[str]:
    value = line.strip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    return [cell.strip() for cell in value.split("|")]


def is_table_separator(line: str) -> bool:
    cells = table_row(line)
    return len(cells) >= 2 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def build_table(lines: list[str], styles: dict[str, ParagraphStyle], width: float) -> LongTable:
    # A five-column, citation-heavy certificate manifest is unreadable on
    # letter paper. Preserve every source cell but display each obligation in
    # two generous columns, with clearly labelled object/files/results.
    raw_rows = [table_row(line) for line in lines]
    if raw_rows and len(raw_rows[0]) == 5 and raw_rows[0][0] == "mathematical obligation":
        formatted = [[
            Paragraph("Proof obligation", styles["ManifestHead"]),
            Paragraph("Certificate and exact result", styles["ManifestHead"]),
        ]]
        for row in raw_rows[1:]:
            if len(row) != 5:
                raise ValueError("Malformed certificate manifest row")
            obligation, finite_object, verifier, saved_data, expected = row
            details = (
                "<b>Object:</b> " + inline_markup(finite_object)
                + "<br/><b>Verifier:</b> " + inline_markup(verifier)
                + "<br/><b>Certificate/data:</b> " + inline_markup(saved_data)
                + "<br/><b>Result:</b> " + inline_markup(expected)
            )
            formatted.append([
                Paragraph(inline_markup(obligation), styles["ManifestLabel"]),
                Paragraph(details, styles["ManifestText"]),
            ])
        table = LongTable(
            formatted, colWidths=[width * 0.25, width * 0.75],
            repeatRows=1, hAlign="LEFT",
        )
        table.setStyle(TableStyle([
            ("LINEABOVE", (0, 0), (-1, 0), 0.65, colors.black),
            ("LINEBELOW", (0, 0), (-1, 0), 0.45, colors.black),
            ("LINEBELOW", (0, -1), (-1, -1), 0.45, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return table
    column_count = max(len(row) for row in raw_rows)
    rows = [row + [""] * (column_count - len(row)) for row in raw_rows]

    formatted = []
    for row_index, row in enumerate(rows):
        cell_style = styles["TableHead"] if row_index == 0 else styles["TableText"]
        formatted.append([Paragraph(inline_markup(cell), cell_style) for cell in row])

    weights = []
    for column in range(column_count):
        longest = max(len(rows[row][column]) for row in range(len(rows)))
        weights.append(max(8, min(42, longest)))
    total = sum(weights)
    widths = [width * weight / total for weight in weights]

    table = LongTable(formatted, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("LINEABOVE", (0, 0), (-1, 0), 0.65, colors.black),
                ("LINEBELOW", (0, 0), (-1, 0), 0.45, colors.black),
                ("LINEBELOW", (0, -1), (-1, -1), 0.45, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return table


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "Title": ParagraphStyle(
            "QECTitle",
            parent=base["Title"],
            fontName="QECBody-Bold",
            fontSize=17.5,
            leading=20.5,
            alignment=TA_CENTER,
            textColor=colors.black,
            spaceAfter=4,
        ),
        "Subtitle": ParagraphStyle(
            "QECSubtitle",
            parent=base["Normal"],
            fontName="QECBody-Italic",
            fontSize=9.2,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.black,
            spaceAfter=7,
        ),
        "Author": ParagraphStyle(
            "QECAuthor",
            parent=base["Normal"],
            fontName="QECBody",
            fontSize=10,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.black,
            spaceAfter=8,
        ),
        "AbstractHeading": ParagraphStyle(
            "QECAbstractHeading",
            parent=base["Heading2"],
            fontName="QECBody-Bold",
            fontSize=9.2,
            leading=11,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceBefore=1,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "Abstract": ParagraphStyle(
            "QECAbstract",
            parent=base["BodyText"],
            fontName="QECBody",
            fontSize=9.8,
            leading=12,
            alignment=TA_JUSTIFY,
            textColor=colors.black,
            spaceAfter=5.5,
            splitLongWords=True,
        ),
        "H1": ParagraphStyle(
            "QECH1",
            parent=base["Heading1"],
            fontName="QECBody-Bold",
            fontSize=11.2,
            leading=13.4,
            textColor=colors.black,
            spaceBefore=11,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "H2": ParagraphStyle(
            "QECH2",
            parent=base["Heading2"],
            fontName="QECBody-Bold",
            fontSize=10,
            leading=12,
            textColor=colors.black,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "H3": ParagraphStyle(
            "QECH3",
            parent=base["Heading3"],
            fontName="QECBody-Bold",
            fontSize=9.2,
            leading=11,
            textColor=colors.black,
            spaceBefore=6,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "H4": ParagraphStyle(
            "QECH4",
            parent=base["Heading3"],
            fontName="QECBody-Bold",
            fontSize=8.7,
            leading=10.4,
            textColor=colors.black,
            spaceBefore=5,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "Body": ParagraphStyle(
            "QECBodyText",
            parent=base["BodyText"],
            fontName="QECBody",
            fontSize=10.5,
            leading=13.8,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceAfter=6.5,
            splitLongWords=True,
        ),
        "List": ParagraphStyle(
            "QECList",
            parent=base["BodyText"],
            fontName="QECBody",
            fontSize=10.1,
            leading=13,
            leftIndent=10,
            firstLineIndent=-7,
            textColor=colors.black,
            spaceAfter=3.5,
        ),
        "Quote": ParagraphStyle(
            "QECQuote",
            parent=base["BodyText"],
            fontName="QECBody-Italic",
            fontSize=10,
            leading=13,
            leftIndent=9,
            rightIndent=4,
            textColor=colors.black,
            spaceAfter=5.5,
        ),
        "Equation": ParagraphStyle(
            "QECEquation",
            parent=base["BodyText"],
            fontName="QECBody",
            fontSize=10,
            # Subscripts and superscripts need more vertical clearance than
            # normal text lines, including when an equation wraps.
            leading=23,
            alignment=TA_CENTER,
            textColor=colors.black,
            leftIndent=2,
            rightIndent=2,
            spaceBefore=2,
            spaceAfter=2,
            splitLongWords=True,
        ),
        "Code": ParagraphStyle(
            "QECCode",
            parent=base["Code"],
            fontName="QECMono",
            fontSize=6.5,
            leading=7.8,
            leftIndent=3,
            rightIndent=3,
            borderColor=colors.HexColor("#777777"),
            borderWidth=0.35,
            borderPadding=3,
            backColor=colors.HexColor("#f7f7f7"),
            textColor=colors.black,
            spaceBefore=2,
            spaceAfter=7,
        ),
        "ManifestHead": ParagraphStyle(
            "QECManifestHead",
            parent=base["BodyText"],
            fontName="QECBody-Bold",
            fontSize=9,
            leading=11.5,
            textColor=colors.black,
        ),
        "ManifestLabel": ParagraphStyle(
            "QECManifestLabel",
            parent=base["BodyText"],
            fontName="QECBody-Bold",
            fontSize=8.6,
            leading=11.8,
            textColor=colors.black,
            splitLongWords=True,
        ),
        "ManifestText": ParagraphStyle(
            "QECManifestText",
            parent=base["BodyText"],
            fontName="QECBody",
            fontSize=8.8,
            leading=12,
            textColor=colors.black,
            splitLongWords=True,
        ),
        "TableHead": ParagraphStyle(
            "QECTableHead",
            parent=base["BodyText"],
            fontName="QECBody-Bold",
            fontSize=6.2,
            leading=7.2,
            textColor=colors.black,
        ),
        "TableText": ParagraphStyle(
            "QECTableText",
            parent=base["BodyText"],
            fontName="QECBody",
            fontSize=6.1,
            leading=7.1,
            textColor=colors.black,
        ),
    }


def parse_markdown(
    source: str,
    styles: dict[str, ParagraphStyle],
    width: float,
    *,
    front: bool = False,
) -> list[object]:
    lines = source.splitlines()
    flowables: list[object] = []
    paragraph: list[str] = []
    index = 0
    heading_count = 0
    paragraph_style = "Body"

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(item.strip() for item in paragraph).strip()
            if text:
                style_name = paragraph_style
                if front and text == "**Brandon Li**":
                    style_name = "Author"
                paragraph_flowable = Paragraph(inline_markup(text), styles[style_name])
                # Keep the final scope paragraph intact so the page break does
                # not leave a one-line fragment at the top of the next page.
                if text.startswith("No `GF(4)`-linear restriction"):
                    flowables.append(PageBreak())
                    flowables.append(paragraph_flowable)
                else:
                    flowables.append(paragraph_flowable)
            paragraph.clear()

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            # A spacer directly after a heading breaks ReportLab's
            # keepWithNext chain and can strand that heading at a page foot.
            # Heading styles already provide their own spaceAfter.
            prior = flowables[-1] if flowables else None
            is_heading = (
                isinstance(prior, Paragraph)
                and prior.style.name in {
                    "QECH1", "QECH2", "QECH3", "QECH4",
                    "QECAbstractHeading",
                }
            )
            if not is_heading:
                flowables.append(Spacer(1, 1.5))
            index += 1
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            language = stripped[3:].strip()
            index += 1
            code_lines = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index].rstrip())
                index += 1
            if index < len(lines):
                index += 1
            if language == "text":
                # Give each source equation line a separate layout box; joining
                # raised/lowered glyphs with <br/> caused visible collisions.
                for code_line in code_lines:
                    if code_line.strip():
                        flowables.append(
                            Paragraph(math_markup(code_line), styles["Equation"])
                        )
                flowables.append(Spacer(1, 5))
            else:
                flowables.append(Preformatted("\n".join(code_lines), styles["Code"]))
            continue

        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            if level == 2 and heading_count == 1:
                style_name = "Subtitle"
            elif front and heading.group(2).strip().casefold() == "abstract":
                style_name = "AbstractHeading"
            else:
                style_name = {1: "Title", 2: "H1", 3: "H2", 4: "H4"}[level]
            if level == 1:
                flowables.append(Spacer(1, 3))
            flowables.append(Paragraph(inline_markup(heading.group(2)), styles[style_name]))
            if front and heading.group(2).strip().casefold() == "abstract":
                paragraph_style = "Abstract"
            heading_count += 1
            index += 1
            continue

        if stripped == "---":
            flush_paragraph()
            flowables.append(Spacer(1, 3))
            flowables.append(HRFlowable(width="100%", thickness=0.7, color=colors.HexColor("#9fb3c8")))
            flowables.append(Spacer(1, 6))
            index += 1
            continue

        if stripped.startswith("|") and index + 1 < len(lines) and is_table_separator(lines[index + 1].strip()):
            flush_paragraph()
            table_lines = [line]
            index += 1
            # Skip the Markdown separator row; the first row remains the table header.
            index += 1
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            table = build_table(table_lines, styles, width)
            # Keep the short predecessor-count table together: the previous
            # render stranded only "10:37" at the top of the next page.
            if table_row(table_lines[0])[0] == "length `n`":
                flowables.append(KeepTogether([table]))
            else:
                flowables.append(table)
            flowables.append(Spacer(1, 5))
            continue

        bullet = re.match(r"^\s*[-*]\s+(.*)$", line)
        numbered = re.match(r"^\s*(\d+)\.\s+(.*)$", line)
        if bullet or numbered:
            flush_paragraph()
            marker = "•" if bullet else f"{numbered.group(1)}."
            content = bullet.group(1) if bullet else numbered.group(2)
            flowables.append(Paragraph(f"{marker} {inline_markup(content)}", styles["List"]))
            index += 1
            continue

        quote = re.match(r"^\s*>\s?(.*)$", line)
        if quote:
            flush_paragraph()
            quote_lines = [quote.group(1).strip()]
            index += 1
            while index < len(lines):
                next_quote = re.match(r"^\s*>\s?(.*)$", lines[index])
                if not next_quote:
                    break
                quote_lines.append(next_quote.group(1).strip())
                index += 1
            flowables.append(Paragraph(inline_markup(" ".join(quote_lines)), styles["Quote"]))
            continue

        paragraph.append(line)
        index += 1

    flush_paragraph()

    # Keep short mathematical subsection introductions with their first
    # displayed formula, not merely with the prose line "use" or "patterns".
    # In particular, the six-site subgroup should not begin at the foot of
    # one page while its defining R appears at the top of the next.
    grouped: list[object] = []
    i = 0
    while i < len(flowables):
        current = flowables[i]
        if isinstance(current, Paragraph) and current.style.name == "QECH4":
            j = i + 1
            while j < len(flowables) and isinstance(flowables[j], Spacer):
                j += 1
            if (j < len(flowables) and isinstance(flowables[j], Paragraph)
                    and flowables[j].style.name == "QECBodyText"):
                k = j + 1
                while k < len(flowables) and isinstance(flowables[k], Spacer):
                    k += 1
                if (k < len(flowables) and isinstance(flowables[k], Paragraph)
                        and flowables[k].style.name == "QECEquation"):
                    while (k < len(flowables) and isinstance(flowables[k], Paragraph)
                           and flowables[k].style.name == "QECEquation"):
                        k += 1
                    grouped.append(KeepTogether(flowables[i:k]))
                    i = k
                    continue
        grouped.append(current)
        i += 1
    return grouped


def draw_page(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont("QECBody", 7.3)
    canvas.setFillColor(colors.black)
    canvas.drawCentredString(letter[0] / 2, 0.30 * inch, f"{canvas.getPageNumber()}")
    canvas.restoreState()


def qec_canvas(filename: str, **kwargs) -> Canvas:
    """Start each page with an embedded font rather than ReportLab's Helvetica."""

    kwargs["initialFontName"] = "QECBody"
    kwargs.setdefault("initialFontSize", 12)
    return Canvas(filename, **kwargs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=REPO_ROOT / "paper/QEC1435_NO_BINARY_14_3_5.md",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "output/pdf/QEC1435_NO_BINARY_14_3_5.pdf",
    )
    args = parser.parse_args()

    register_fonts()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    source = args.source.read_text(encoding="utf-8")
    left_margin = 0.76 * inch
    right_margin = 0.76 * inch
    top_margin = 0.68 * inch
    bottom_margin = 0.66 * inch
    full_width = letter[0] - left_margin - right_margin

    document = SimpleDocTemplate(
        str(args.output),
        pagesize=letter,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
        title="No binary [[14,3,d≥5]] quantum stabilizer code exists",
        author="Brandon Li",
        subject="Original-physical signed-shadow proof and exhaustive additive-code closure",
    )
    styles = make_styles()
    section_one = re.search(r"^## 1\.\s+", source, re.MULTILINE)
    if section_one is None:
        raise ValueError("manuscript is missing the numbered Section 1 heading")
    front_source = source[: section_one.start()]
    body_source = source[section_one.start() :]
    front_story = parse_markdown(front_source, styles, full_width, front=True)
    body_story = parse_markdown(body_source, styles, full_width)
    document.build(front_story + body_story, onFirstPage=draw_page, onLaterPages=draw_page, canvasmaker=qec_canvas)
    print(f"wrote {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
