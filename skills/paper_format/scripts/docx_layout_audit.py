#!/usr/bin/env python3
"""Audit DOCX manuscript layout against common academic-paper rules.

The checker is intentionally conservative:
- Static OOXML checks are dependency-free and good for triage.
- Word COM checks are optional and required for submission-ready layout claims.
- It never edits the input document.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "o": "urn:schemas-microsoft-com:office:office",
    "v": "urn:schemas-microsoft-com:vml",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}

W = "{" + NS["w"] + "}"
M = "{" + NS["m"] + "}"

CAPTION_RE = re.compile(
    r"^\s*((fig\.?|figure|table)\s*[\wIVXivx.-]*|[图表]\s*[\d一二三四五六七八九十IVXivx.-]*)\b",
    re.IGNORECASE,
)
FIGURE_CAPTION_RE = re.compile(r"^\s*((fig\.?|figure)\s*[\wIVXivx.-]*|图\s*[\d一二三四五六七八九十IVXivx.-]*)\b", re.IGNORECASE)
TABLE_CAPTION_RE = re.compile(r"^\s*(table\s*[\wIVXivx.-]*|表\s*[\d一二三四五六七八九十IVXivx.-]*)\b", re.IGNORECASE)
EQUATION_CAPTION_RE = re.compile(r"^\s*((eq\.?|equation|式)\s*[\wIVXivx().-]*)\b", re.IGNORECASE)
DISPLAY_LABEL_RE = re.compile(
    r"^\s*(?P<kind>fig(?:ure)?\.?|table|图|表)\s*"
    r"(?P<label>(?:[A-Za-z]?\d+(?:[.\-–—]\d+)*(?:[A-Za-z])?|[IVXLC]+|[一二三四五六七八九十百]+))"
    r"(?=\s|[.:：、，,；;）)]|$)",
    re.IGNORECASE,
)
LATIN_TEXT_RE = re.compile(r"[A-Za-z]")
NARRATIVE_CALLOUT_VERB_RE = re.compile(
    r"^\s*(?:shows?|illustrates?|presents?|summari[sz]es?|reports?|compares?|depicts?|demonstrates?|"
    r"reveals?|provides?|indicates?|显示|表明|展示|给出|比较|总结|说明)",
    re.IGNORECASE,
)
LEAKAGE_RE = re.compile(
    r"(原稿|原文|改为|修改为|根据审稿人|审稿人指出|track changes|修订|标黄|TODO_CITE|TODO|"
    r"Internal QA|remove before submission|before submission|Draft positioning|Provisional|machine-simulated)",
    re.IGNORECASE,
)

ACADEMIC_PROFILE_NOTES = {
    "generic": "Target journal/template requirements override all defaults; static checks are limited to common DOCX layout defects.",
    "gb7713": "GB/T 7713.2-2022 academic-paper baseline: numbered display equations centered with the number at the far right, table titles above tables, figure titles below figures, continued tables repeat headers.",
    "ieee": "IEEE-style engineering-paper baseline: equation numbers consecutive and flush right; figure captions below figures; table captions above tables; use the exact IEEE template when available.",
    "journal": "Journal-specific profile placeholder: use only with explicit target instructions or a verified template; unresolved target rules remain findings.",
}


def _w(name: str) -> str:
    return W + name


def _m(name: str) -> str:
    return M + name


def _attr(el: Optional[ET.Element], ns_prefix: str, name: str) -> Optional[str]:
    if el is None:
        return None
    return el.attrib.get("{" + NS[ns_prefix] + "}" + name)


def _text(el: ET.Element) -> str:
    chunks: List[str] = []
    for node in el.iter():
        if node.tag == _w("t") and node.text:
            chunks.append(node.text)
        elif node.tag == _w("tab"):
            chunks.append("\t")
        elif node.tag == _w("br"):
            chunks.append("\n")
    return "".join(chunks).strip()


def _half_points(raw: Optional[str]) -> Optional[float]:
    if not raw:
        return None
    try:
        return int(raw) / 2.0
    except ValueError:
        return None


def _spacing_multiple(spacing_el: Optional[ET.Element]) -> Optional[float]:
    if spacing_el is None:
        return None
    line = _attr(spacing_el, "w", "line")
    rule = _attr(spacing_el, "w", "lineRule")
    if not line:
        return None
    try:
        value = float(line)
    except ValueError:
        return None
    if rule in (None, "", "auto"):
        return round(value / 240.0, 3)
    return None


def _alignment_from_ppr(ppr: Optional[ET.Element]) -> Optional[str]:
    if ppr is None:
        return None
    return _attr(ppr.find("w:jc", NS), "w", "val")


def _line_spacing_from_ppr(ppr: Optional[ET.Element]) -> Optional[float]:
    if ppr is None:
        return None
    return _spacing_multiple(ppr.find("w:spacing", NS))


def _font_size_from_rpr(rpr: Optional[ET.Element]) -> Optional[float]:
    if rpr is None:
        return None
    return _half_points(_attr(rpr.find("w:sz", NS), "w", "val"))


def _english_font_from_rpr(rpr: Optional[ET.Element]) -> Optional[str]:
    if rpr is None:
        return None
    fonts = rpr.find("w:rFonts", NS)
    if fonts is None:
        return None
    for key in ("ascii", "hAnsi", "cs"):
        value = _attr(fonts, "w", key)
        if value:
            return " ".join(value.split())
    return None


def _font_matches(actual: Optional[str], expected: str) -> bool:
    if not actual:
        return False
    return actual.casefold() == expected.casefold()


def _mode(values: Iterable[Any]) -> Optional[Any]:
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return Counter(clean).most_common(1)[0][0]


def _near(a: Optional[float], b: float, tol: float = 0.06) -> bool:
    return a is not None and abs(a - b) <= tol


def _parent_map(root: ET.Element) -> Dict[int, ET.Element]:
    return {id(child): parent for parent in root.iter() for child in parent}


def _has_ancestor(el: ET.Element, parent: Dict[int, ET.Element], tag: str) -> bool:
    current = el
    while id(current) in parent:
        current = parent[id(current)]
        if current.tag == tag:
            return True
    return False


def _safe_xml(data: bytes, part_name: str, findings: List[Dict[str, Any]]) -> Optional[ET.Element]:
    try:
        return ET.fromstring(data)
    except ET.ParseError as exc:
        findings.append(
            {
                "severity": "blocker",
                "code": "DOCX_XML_PARSE_ERROR",
                "locator": part_name,
                "message": f"Cannot parse DOCX XML part: {exc}",
                "evidence": None,
            }
        )
        return None


def _style_name(style: Dict[str, Any]) -> str:
    return str(style.get("name") or style.get("style_id") or "")


def _resolve_style_prop(
    styles: Dict[str, Dict[str, Any]],
    style_id: Optional[str],
    prop: str,
    default_value: Any = None,
    max_depth: int = 8,
) -> Any:
    seen = set()
    current = style_id
    depth = 0
    while current and current in styles and current not in seen and depth < max_depth:
        seen.add(current)
        value = styles[current].get(prop)
        if value is not None:
            return value
        current = styles[current].get("based_on")
        depth += 1
    return default_value


def parse_styles(styles_xml: Optional[bytes], findings: List[Dict[str, Any]]) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Any]]:
    styles: Dict[str, Dict[str, Any]] = {}
    defaults: Dict[str, Any] = {}
    if not styles_xml:
        findings.append(
            {
                "severity": "warn",
                "code": "STYLES_XML_MISSING",
                "locator": "word/styles.xml",
                "message": "Cannot inspect inherited font, caption, heading, or spacing rules because styles.xml is missing.",
                "evidence": None,
            }
        )
        return styles, defaults

    root = _safe_xml(styles_xml, "word/styles.xml", findings)
    if root is None:
        return styles, defaults

    default_rpr = root.find(".//w:docDefaults/w:rPrDefault/w:rPr", NS)
    defaults["font_size_pt"] = _font_size_from_rpr(default_rpr)
    defaults["english_font_name"] = _english_font_from_rpr(default_rpr)
    defaults["line_spacing"] = _line_spacing_from_ppr(root.find(".//w:docDefaults/w:pPrDefault/w:pPr", NS))

    for style in root.findall(".//w:style", NS):
        style_id = _attr(style, "w", "styleId")
        if not style_id:
            continue
        style_type = _attr(style, "w", "type")
        if _attr(style, "w", "default") in {"1", "true"} and style_type:
            defaults[f"default_{style_type}_style_id"] = style_id
        name_el = style.find("w:name", NS)
        based_on_el = style.find("w:basedOn", NS)
        ppr = style.find("w:pPr", NS)
        outline = ppr.find("w:outlineLvl", NS) if ppr is not None else None
        styles[style_id] = {
            "style_id": style_id,
            "name": _attr(name_el, "w", "val"),
            "type": style_type,
            "based_on": _attr(based_on_el, "w", "val"),
            "alignment": _alignment_from_ppr(ppr),
            "font_size_pt": _font_size_from_rpr(style.find("w:rPr", NS)),
            "english_font_name": _english_font_from_rpr(style.find("w:rPr", NS)),
            "line_spacing": _line_spacing_from_ppr(ppr),
            "outline_level": _attr(outline, "w", "val") if outline is not None else None,
            "table_alignment": _alignment_from_ppr(style.find("w:tblPr", NS)),
        }
    return styles, defaults


def _paragraph_style_id(p: ET.Element, defaults: Optional[Dict[str, Any]] = None) -> Optional[str]:
    ppr = p.find("w:pPr", NS)
    direct = _attr(ppr.find("w:pStyle", NS), "w", "val") if ppr is not None else None
    if direct:
        return direct
    return defaults.get("default_paragraph_style_id") if defaults else None


def _paragraph_alignment(p: ET.Element, styles: Dict[str, Dict[str, Any]], style_id: Optional[str]) -> Optional[str]:
    direct = _alignment_from_ppr(p.find("w:pPr", NS))
    if direct:
        return direct
    return _resolve_style_prop(styles, style_id, "alignment")


def _paragraph_line_spacing(
    p: ET.Element,
    styles: Dict[str, Dict[str, Any]],
    defaults: Dict[str, Any],
    style_id: Optional[str],
) -> Optional[float]:
    direct = _line_spacing_from_ppr(p.find("w:pPr", NS))
    if direct is not None:
        return direct
    inherited = _resolve_style_prop(styles, style_id, "line_spacing")
    if inherited is not None:
        return inherited
    return defaults.get("line_spacing")


def _paragraph_font_size(
    p: ET.Element,
    styles: Dict[str, Dict[str, Any]],
    defaults: Dict[str, Any],
    style_id: Optional[str],
) -> Optional[float]:
    sizes = []
    for run in p.findall("w:r", NS):
        sizes.append(_font_size_from_rpr(run.find("w:rPr", NS)))
    direct = _mode(sizes)
    if direct is not None:
        return direct
    inherited = _resolve_style_prop(styles, style_id, "font_size_pt")
    if inherited is not None:
        return inherited
    return defaults.get("font_size_pt")


def _paragraph_english_fonts(
    p: ET.Element,
    styles: Dict[str, Dict[str, Any]],
    defaults: Dict[str, Any],
    style_id: Optional[str],
) -> List[str]:
    fonts: List[str] = []
    for run in p.findall("w:r", NS):
        run_text = _text(run)
        if not LATIN_TEXT_RE.search(run_text):
            continue
        rpr = run.find("w:rPr", NS)
        font = _english_font_from_rpr(rpr)
        run_style_id = _attr(rpr.find("w:rStyle", NS), "w", "val") if rpr is not None else None
        if font is None and run_style_id:
            font = _resolve_style_prop(styles, run_style_id, "english_font_name")
        if font is None:
            font = _resolve_style_prop(styles, style_id, "english_font_name")
        if font is None:
            font = defaults.get("english_font_name")
        if font:
            fonts.append(font)
    return fonts


def _has_direct_run_formatting(p: ET.Element) -> bool:
    for run in p.findall("w:r", NS):
        rpr = run.find("w:rPr", NS)
        if rpr is not None and list(rpr):
            return True
    return False


def _style_is_caption(styles: Dict[str, Dict[str, Any]], style_id: Optional[str]) -> bool:
    if not style_id:
        return False
    style = styles.get(style_id, {})
    haystack = f"{style_id} {_style_name(style)}".lower()
    return "caption" in haystack or "题注" in haystack


def _caption_kind(text: str) -> Optional[str]:
    if FIGURE_CAPTION_RE.match(text):
        return "figure"
    if TABLE_CAPTION_RE.match(text):
        return "table"
    if EQUATION_CAPTION_RE.match(text):
        return "equation"
    return None


def _display_label(text: str) -> Optional[Dict[str, str]]:
    match = DISPLAY_LABEL_RE.match(text)
    if not match:
        return None
    raw_kind = match.group("kind")
    kind = "figure" if raw_kind.lower().startswith("fig") or raw_kind == "图" else "table"
    label = match.group("label").upper().replace("–", "-").replace("—", "-")
    return {"kind": kind, "label": label}


def _looks_like_narrative_callout(text: str) -> bool:
    match = DISPLAY_LABEL_RE.match(text)
    if not match:
        return False
    remainder = text[match.end() :].lstrip(" .:：、，,;；-)）")
    return bool(NARRATIVE_CALLOUT_VERB_RE.match(remainder))


def _display_callout_present(text: str, kind: str, label: str) -> bool:
    aliases = r"(?:fig(?:s|ures?)?\.?|图)" if kind == "figure" else r"(?:tables?|表)"
    label_pattern = rf"(?<![A-Za-z0-9]){re.escape(label)}(?![A-Za-z0-9])"
    for alias_match in re.finditer(aliases, text, flags=re.IGNORECASE):
        window = text[alias_match.start() : alias_match.end() + 100].upper().replace("–", "-").replace("—", "-")
        if re.search(label_pattern, window, flags=re.IGNORECASE):
            return True
        if label.isdigit():
            number = int(label)
            for start, end in re.findall(r"(?<!\d)(\d+)\s*-\s*(\d+)(?!\d)", window):
                low, high = sorted((int(start), int(end)))
                if low <= number <= high:
                    return True
    return False


def _style_is_heading(styles: Dict[str, Dict[str, Any]], style_id: Optional[str]) -> Tuple[bool, Optional[int]]:
    if not style_id:
        return False, None
    style = styles.get(style_id, {})
    haystack = f"{style_id} {_style_name(style)}".lower().replace(" ", "")
    m = re.search(r"heading([1-6])", haystack)
    if m:
        return True, int(m.group(1))
    if "标题" in haystack:
        m2 = re.search(r"标题([1-6])", haystack)
        return True, int(m2.group(1)) if m2 else None
    outline = style.get("outline_level")
    if outline is not None:
        try:
            return True, int(outline) + 1
        except ValueError:
            return True, None
    return False, None


def _table_text(tbl: ET.Element) -> str:
    return _text(tbl)


def _table_has_repeated_header(tbl: ET.Element) -> bool:
    first_row = tbl.find("w:tr", NS)
    if first_row is None:
        return False
    trpr = first_row.find("w:trPr", NS)
    return trpr is not None and trpr.find("w:tblHeader", NS) is not None


def _table_rows_allow_break(tbl: ET.Element) -> Optional[bool]:
    values = []
    for row in tbl.findall("w:tr", NS):
        trpr = row.find("w:trPr", NS)
        cant_split = trpr is not None and trpr.find("w:cantSplit", NS) is not None
        values.append(not cant_split)
    if not values:
        return None
    return any(values)


def _table_alignment(tbl: ET.Element, styles: Dict[str, Dict[str, Any]]) -> Optional[str]:
    tbl_pr = tbl.find("w:tblPr", NS)
    direct = _alignment_from_ppr(tbl_pr)
    if direct:
        return direct
    style_id = _attr(tbl_pr.find("w:tblStyle", NS), "w", "val") if tbl_pr is not None else None
    return _resolve_style_prop(styles, style_id, "table_alignment")


def _direct_body_blocks(root: ET.Element) -> List[Dict[str, Any]]:
    body = root.find("w:body", NS)
    if body is None:
        return []
    blocks: List[Dict[str, Any]] = []
    paragraph_number = 0
    table_number = 0
    for child in list(body):
        if child.tag == _w("p"):
            paragraph_number += 1
            text = _text(child)
            has_drawing = child.find(".//w:drawing", NS) is not None or child.find(".//w:pict", NS) is not None
            has_display_math = child.find(".//m:oMathPara", NS) is not None
            kind = _caption_kind(text) if not _looks_like_narrative_callout(text) else None
            blocks.append(
                {
                    "kind": "paragraph",
                    "paragraph": paragraph_number,
                    "text": text[:120],
                    "caption_kind": kind,
                    "has_drawing": has_drawing,
                    "has_display_math": has_display_math,
                }
            )
        elif child.tag == _w("tbl"):
            table_number += 1
            blocks.append({"kind": "table", "table": table_number})
    return blocks


def _audit_caption_placement(args: argparse.Namespace, root: ET.Element, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    expected_by_profile = {
        "gb7713": {"figure": "below", "table": "above"},
        "ieee": {"figure": "below", "table": "above"},
    }
    expected = expected_by_profile.get(args.academic_profile)
    if not expected:
        return []

    blocks = _direct_body_blocks(root)
    samples: List[Dict[str, Any]] = []
    for idx, block in enumerate(blocks):
        cap_kind = block.get("caption_kind")
        if cap_kind not in expected:
            continue
        before = blocks[idx - 1] if idx > 0 else None
        after = blocks[idx + 1] if idx + 1 < len(blocks) else None
        expected_position = expected[cap_kind]
        ok = True
        message = ""
        if cap_kind == "figure" and expected_position == "below":
            ok = bool(before and before.get("kind") == "paragraph" and before.get("has_drawing"))
            message = "Figure caption/title should be placed below the figure for this academic profile."
        elif cap_kind == "table" and expected_position == "above":
            ok = bool(after and after.get("kind") == "table")
            message = "Table caption/title should be placed above the table for this academic profile."
        sample = {
            "paragraph": block.get("paragraph"),
            "caption_kind": cap_kind,
            "text": block.get("text"),
            "expected_position": expected_position,
            "previous_block": before,
            "next_block": after,
            "ok": ok,
        }
        samples.append(sample)
        if not ok:
            add_finding(
                findings,
                "major",
                "CAPTION_PLACEMENT_MISMATCH",
                message,
                f"paragraph {block.get('paragraph')}",
                sample,
            )
    return samples


def add_finding(
    findings: List[Dict[str, Any]],
    severity: str,
    code: str,
    message: str,
    locator: Optional[str] = None,
    evidence: Optional[Any] = None,
) -> None:
    findings.append(
        {
            "severity": severity,
            "code": code,
            "locator": locator,
            "message": message,
            "evidence": evidence,
        }
    )


def audit_static(args: argparse.Namespace) -> Dict[str, Any]:
    docx = Path(args.docx).resolve()
    findings: List[Dict[str, Any]] = []
    result: Dict[str, Any] = {
        "input": str(docx),
        "checked_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "mode": "static_ooxml",
        "academic_profile": args.academic_profile,
        "profile_note": ACADEMIC_PROFILE_NOTES.get(args.academic_profile),
        "counts": {},
        "findings": findings,
        "requires_render_qa": False,
    }

    if not docx.exists():
        add_finding(findings, "blocker", "INPUT_DOCX_MISSING", "Input DOCX does not exist.", str(docx))
        return result
    if docx.suffix.lower() != ".docx":
        add_finding(findings, "blocker", "INPUT_NOT_DOCX", "Input must be a .docx file.", str(docx))
        return result

    try:
        with zipfile.ZipFile(docx) as zf:
            names = set(zf.namelist())
            if "word/document.xml" not in names:
                add_finding(findings, "blocker", "DOCX_DOCUMENT_XML_MISSING", "word/document.xml is missing.", str(docx))
                return result
            document_xml = zf.read("word/document.xml")
            styles_xml = zf.read("word/styles.xml") if "word/styles.xml" in names else None
            all_xml_text = "\n".join(
                zf.read(name).decode("utf-8", errors="ignore")
                for name in names
                if name.endswith(".xml") and name.startswith("word/")
            )
            embedded_parts = sorted(name for name in names if name.startswith("word/embeddings/"))
            comment_parts = sorted(name for name in names if name.startswith("word/comments"))
    except zipfile.BadZipFile:
        add_finding(findings, "blocker", "DOCX_ZIP_INVALID", "DOCX is not a valid zip container.", str(docx))
        return result

    root = _safe_xml(document_xml, "word/document.xml", findings)
    if root is None:
        return result
    styles, defaults = parse_styles(styles_xml, findings)
    parents = _parent_map(root)

    if args.submission_ready and not args.use_word_com:
        add_finding(
            findings,
            "major",
            "WORD_PDF_RENDER_QA_UNVERIFIED",
            "Submission-ready DOCX approval requires Word/PDF render verification; rerun with --use-word-com --export-pdf when Microsoft Word is available.",
            "document",
        )
        result["requires_render_qa"] = True
    elif args.submission_ready and args.use_word_com and not args.export_pdf:
        add_finding(
            findings,
            "major",
            "PDF_EXPORT_NOT_REQUESTED",
            "Submission-ready DOCX approval requires a Word-exported PDF proof; rerun with --export-pdf.",
            "document",
        )
        result["requires_render_qa"] = True

    paragraphs = root.findall(".//w:p", NS)
    body_paragraphs = [p for p in paragraphs if not _has_ancestor(p, parents, _w("tbl"))]
    tables = root.findall(".//w:tbl", NS)
    drawings = root.findall(".//w:drawing", NS)
    omath = root.findall(".//m:oMath", NS)
    omath_para = root.findall(".//m:oMathPara", NS)
    inline_omath = [node for node in omath if not _has_ancestor(node, parents, _m("oMathPara"))]

    result["counts"].update(
        {
            "paragraphs": len(paragraphs),
            "body_paragraphs": len(body_paragraphs),
            "tables": len(tables),
            "drawings": len(drawings),
            "omml_equations": len(omath),
            "omml_display_equations": len(omath_para),
            "omml_inline_equations": len(inline_omath),
            "embedded_parts": len(embedded_parts),
        }
    )

    if comment_parts or "<w:commentRangeStart" in all_xml_text:
        add_finding(
            findings,
            "major",
            "COMMENTS_PRESENT",
            "Comments are present; clean final manuscripts should not contain unresolved comments.",
            "word/comments*.xml",
            {"comment_parts": comment_parts},
        )
    if re.search(r"<w:(ins|del|moveFrom|moveTo)\b", all_xml_text):
        add_finding(
            findings,
            "major",
            "TRACKED_CHANGES_PRESENT",
            "Tracked changes or move markup are present; accept/reject changes before clean final delivery.",
            "word/document.xml",
        )
    if LEAKAGE_RE.search(all_xml_text):
        add_finding(
            findings,
            "major",
            "CLEAN_FINAL_LANGUAGE_HIT",
            "Potential process-language or internal marker hit found in document XML.",
            "word/*.xml",
        )

    mathtype_markers = re.findall(r"(MathType|Equation\.DSMT|Equation\.3|MTEquation)", all_xml_text, flags=re.IGNORECASE)
    result["counts"]["mathtype_markers"] = len(mathtype_markers)
    if args.require_mathtype and not (omath or embedded_parts or mathtype_markers):
        add_finding(
            findings,
            "blocker",
            "MATHTYPE_REQUIRED_BUT_UNAVAILABLE",
            "MathType/Word equation-compatible objects are required, but no OMML equations, embedded OLE equations, or MathType markers were detected.",
            "word/document.xml",
        )
    if args.require_inline_math and len(inline_omath) == 0:
        add_finding(
            findings,
            "major",
            "INLINE_MATH_UNVERIFIED",
            "Inline variables are required as equation-compatible objects, but no inline OMML objects were detected statically.",
            "word/document.xml",
        )
    if omath_para and not args.use_word_com:
        add_finding(
            findings,
            "warn" if not args.submission_ready else "major",
            "EQUATION_ALIGNMENT_RENDER_QA_REQUIRED",
            "Display-equation centering and right-aligned equation numbering require Word/PDF render verification.",
            "display equations",
            {"display_equations": len(omath_para)},
        )
        result["requires_render_qa"] = True

    captions: List[Dict[str, Any]] = []
    headings: List[Dict[str, Any]] = []
    display_labels: List[Dict[str, Any]] = []
    caption_paragraph_ids = set()
    body_spacing_values: List[float] = []
    body_font_values: List[float] = []
    body_english_font_values: List[str] = []
    body_english_font_mismatches: List[Dict[str, Any]] = []
    body_english_font_unresolved: List[Dict[str, Any]] = []
    body_paragraph_ids = {id(p) for p in body_paragraphs}
    expected_english_font = args.english_font_name
    check_english_font = expected_english_font.casefold() != "any"

    for idx, p in enumerate(paragraphs, start=1):
        text = _text(p)
        if not text:
            continue
        style_id = _paragraph_style_id(p, defaults)
        is_caption = _style_is_caption(styles, style_id) or (
            bool(CAPTION_RE.match(text)) and not _looks_like_narrative_callout(text)
        )
        is_heading, heading_level = _style_is_heading(styles, style_id)
        alignment = _paragraph_alignment(p, styles, style_id)
        font_size = _paragraph_font_size(p, styles, defaults, style_id)
        english_fonts = _paragraph_english_fonts(p, styles, defaults, style_id)
        line_spacing = _paragraph_line_spacing(p, styles, defaults, style_id)

        if is_caption:
            caption_paragraph_ids.add(id(p))
            label_info = _display_label(text)
            caption_info = {
                "paragraph": idx,
                "text": text[:120],
                "style_id": style_id,
                "alignment": alignment,
                "font_size_pt": font_size,
                "english_font_names": sorted(set(english_fonts)),
                "display_kind": label_info.get("kind") if label_info else None,
                "display_label": label_info.get("label") if label_info else None,
            }
            captions.append(caption_info)
            if label_info:
                display_labels.append({**label_info, "paragraph": idx, "text": text[:120]})
            if alignment != "center":
                add_finding(
                    findings,
                    "major",
                    "CAPTION_STYLE_MISMATCH",
                    "Figure/table caption is not centered.",
                    f"paragraph {idx}",
                    caption_info,
                )
            if font_size is None:
                add_finding(
                    findings,
                    "warn",
                    "CAPTION_FONT_SIZE_UNRESOLVED",
                    "Caption font size could not be resolved from direct or inherited style formatting.",
                    f"paragraph {idx}",
                    caption_info,
                )
            elif not _near(font_size, args.caption_font_pt, 0.15):
                add_finding(
                    findings,
                    "major",
                    "CAPTION_STYLE_MISMATCH",
                    f"Caption font size is {font_size:g} pt; expected {args.caption_font_pt:g} pt unless target style overrides.",
                    f"paragraph {idx}",
                    caption_info,
                )
            if LATIN_TEXT_RE.search(text) and check_english_font:
                if not english_fonts:
                    add_finding(
                        findings,
                        "warn",
                        "CAPTION_ENGLISH_FONT_UNRESOLVED",
                        "English/Latin caption font could not be resolved from direct, inherited, or default formatting.",
                        f"paragraph {idx}",
                        caption_info,
                    )
                elif any(not _font_matches(font, expected_english_font) for font in english_fonts):
                    add_finding(
                        findings,
                        "major",
                        "ENGLISH_FONT_MISMATCH",
                        f"English/Latin caption text must use {expected_english_font} unless the target style overrides it.",
                        f"paragraph {idx}",
                        caption_info,
                    )
            if not _style_is_caption(styles, style_id):
                add_finding(
                    findings,
                    "warn",
                    "CAPTION_NOT_USING_CAPTION_STYLE",
                    "Caption-like paragraph is not using an explicit caption style.",
                    f"paragraph {idx}",
                    caption_info,
                )

        if is_heading:
            heading_info = {
                "paragraph": idx,
                "text": text[:120],
                "style_id": style_id,
                "level": heading_level,
                "font_size_pt": font_size,
            }
            headings.append(heading_info)
            if _has_direct_run_formatting(p):
                add_finding(
                    findings,
                    "warn",
                    "HEADING_DIRECT_FORMATTING",
                    "Heading contains direct run formatting; use stable heading styles for manuscript structure.",
                    f"paragraph {idx}",
                    heading_info,
                )
        elif p in body_paragraphs and not is_caption:
            if len(text) >= 40:
                if font_size is not None:
                    body_font_values.append(font_size)
                if line_spacing is not None:
                    body_spacing_values.append(line_spacing)
                if LATIN_TEXT_RE.search(text):
                    if english_fonts:
                        body_english_font_values.extend(english_fonts)
                        unexpected = sorted({
                            font for font in english_fonts if check_english_font and not _font_matches(font, expected_english_font)
                        })
                        if unexpected:
                            body_english_font_mismatches.append(
                                {"paragraph": idx, "text": text[:120], "fonts": unexpected}
                            )
                    elif check_english_font:
                        body_english_font_unresolved.append({"paragraph": idx, "text": text[:120]})

    result["counts"]["captions"] = len(captions)
    result["counts"]["headings"] = len(headings)
    result["samples"] = {
        "captions": captions[:20],
        "headings": headings[:30],
    }

    if not captions and (drawings or tables):
        add_finding(
            findings,
            "warn",
            "CAPTIONS_NOT_DETECTED",
            "Figures or tables exist but no caption-like paragraphs were detected.",
            "document",
            {"drawings": len(drawings), "tables": len(tables)},
        )

    placement_samples = _audit_caption_placement(args, root, findings)
    if placement_samples:
        result["samples"]["caption_placement"] = placement_samples[:30]

    callout_candidates: List[Dict[str, Any]] = []
    for p_idx, p in enumerate(paragraphs, start=1):
        if id(p) not in body_paragraph_ids or id(p) in caption_paragraph_ids:
            continue
        text = _text(p)
        if not text:
            continue
        style_id = _paragraph_style_id(p, defaults)
        is_heading, _ = _style_is_heading(styles, style_id)
        if not is_heading:
            callout_candidates.append({"paragraph": p_idx, "text": text})

    callout_samples: List[Dict[str, Any]] = []
    for item in display_labels:
        matching = [
            candidate["paragraph"]
            for candidate in callout_candidates
            if _display_callout_present(candidate["text"], item["kind"], item["label"])
        ]
        sample = {**item, "body_callout_paragraphs": matching[:10], "ok": bool(matching)}
        callout_samples.append(sample)
        if not matching:
            add_finding(
                findings,
                "major",
                "DISPLAY_ITEM_CALLOUT_MISSING",
                f"{item['kind'].title()} {item['label']} has no matching callout in ordinary manuscript body prose.",
                f"paragraph {item['paragraph']}",
                sample,
            )
    result["counts"]["numbered_display_items"] = len(display_labels)
    result["counts"]["uncited_display_items"] = sum(1 for item in callout_samples if not item["ok"])
    result["samples"]["display_item_callouts"] = callout_samples[:50]

    body_font_mode = _mode(body_font_values)
    body_spacing_mode = _mode(body_spacing_values)
    body_english_font_mode = _mode(body_english_font_values)
    result["summary_values"] = {
        "body_font_mode_pt": body_font_mode,
        "body_english_font_mode": body_english_font_mode,
        "expected_english_font": expected_english_font,
        "body_line_spacing_mode": body_spacing_mode,
        "default_font_size_pt": defaults.get("font_size_pt"),
        "default_english_font_name": defaults.get("english_font_name"),
        "default_line_spacing": defaults.get("line_spacing"),
    }
    if body_font_mode is None:
        add_finding(
            findings,
            "warn",
            "BODY_FONT_SIZE_UNRESOLVED",
            "Body font size could not be resolved from sampled paragraphs.",
            "body paragraphs",
        )
    elif not _near(body_font_mode, args.body_font_pt, 0.15):
        add_finding(
            findings,
            "major",
            "BODY_FONT_SIZE_MISMATCH",
            f"Dominant body font size is {body_font_mode:g} pt; expected {args.body_font_pt:g} pt unless target style overrides.",
            "body paragraphs",
        )
    if body_english_font_mismatches:
        add_finding(
            findings,
            "major",
            "ENGLISH_FONT_MISMATCH",
            f"English/Latin body text must use {expected_english_font} unless the target style overrides it.",
            "body paragraphs",
            body_english_font_mismatches[:20],
        )
    if body_english_font_unresolved:
        add_finding(
            findings,
            "warn",
            "BODY_ENGLISH_FONT_UNRESOLVED",
            "English/Latin body font could not be resolved for some sampled paragraphs.",
            "body paragraphs",
            body_english_font_unresolved[:20],
        )
    if body_font_mode is not None:
        for caption in captions:
            caption_size = caption.get("font_size_pt")
            if caption_size is None:
                continue
            actual_delta = body_font_mode - caption_size
            if not _near(actual_delta, args.caption_size_delta_pt, 0.15):
                add_finding(
                    findings,
                    "major",
                    "CAPTION_FONT_HIERARCHY_MISMATCH",
                    f"Caption is {actual_delta:g} pt smaller than body text; expected a {args.caption_size_delta_pt:g} pt difference unless the target style overrides it.",
                    f"paragraph {caption['paragraph']}",
                    caption,
                )
    if body_spacing_mode is None:
        add_finding(
            findings,
            "warn",
            "LINE_SPACING_UNRESOLVED",
            "Line spacing could not be resolved from sampled body paragraphs.",
            "body paragraphs",
        )
    elif not _near(body_spacing_mode, args.line_spacing, 0.04):
        add_finding(
            findings,
            "major",
            "LINE_SPACING_MISMATCH",
            f"Dominant body line spacing is {body_spacing_mode:g}; expected {args.line_spacing:g} unless target style overrides.",
            "body paragraphs",
        )

    previous_level: Optional[int] = None
    for heading in headings:
        level = heading.get("level")
        if isinstance(level, int) and previous_level is not None and level > previous_level + 1:
            add_finding(
                findings,
                "major",
                "HEADING_STYLE_MISMATCH",
                "Heading level jumps over an intermediate level.",
                f"paragraph {heading['paragraph']}",
                {"previous_level": previous_level, "current_level": level, "text": heading["text"]},
            )
        if isinstance(level, int):
            previous_level = level
    if len(body_paragraphs) > 25 and not headings:
        add_finding(
            findings,
            "warn",
            "HEADING_STYLES_NOT_DETECTED",
            "Long manuscript has no detected heading styles; chapter/section titles may be manually formatted.",
            "document",
        )

    figure_summaries: List[Dict[str, Any]] = []
    for p_idx, p in enumerate(paragraphs, start=1):
        if id(p) not in body_paragraph_ids:
            continue
        drawing_count = len(p.findall(".//w:drawing", NS)) + len(p.findall(".//w:pict", NS))
        if not drawing_count:
            continue
        style_id = _paragraph_style_id(p, defaults)
        alignment = _paragraph_alignment(p, styles, style_id)
        floating_count = len(p.findall(".//wp:anchor", NS))
        summary = {
            "paragraph": p_idx,
            "drawing_count": drawing_count,
            "floating_count": floating_count,
            "alignment": alignment,
            "expected_alignment": args.display_item_alignment,
        }
        figure_summaries.append(summary)
        if args.display_item_alignment != "any" and alignment != args.display_item_alignment:
            add_finding(
                findings,
                "major",
                "DISPLAY_ITEM_ALIGNMENT_MISMATCH",
                f"Figure container paragraph alignment is {alignment or 'unresolved/default'}; expected {args.display_item_alignment} unless the target style overrides it.",
                f"paragraph {p_idx}",
                summary,
            )
    result["figures"] = figure_summaries
    result["counts"]["figure_container_paragraphs"] = len(figure_summaries)
    result["counts"]["misaligned_figure_containers"] = sum(
        1
        for item in figure_summaries
        if args.display_item_alignment != "any" and item["alignment"] != args.display_item_alignment
    )

    table_summaries = []
    for t_idx, tbl in enumerate(tables, start=1):
        rows = len(tbl.findall("w:tr", NS))
        cells = len(tbl.findall(".//w:tc", NS))
        chars = len(_table_text(tbl))
        long_table = rows >= args.long_table_rows or chars >= args.long_table_chars
        alignment = _table_alignment(tbl, styles)
        summary = {
            "table": t_idx,
            "rows": rows,
            "cells": cells,
            "characters": chars,
            "has_repeated_header": _table_has_repeated_header(tbl),
            "rows_allow_break_across_pages": _table_rows_allow_break(tbl),
            "likely_long": long_table,
            "alignment": alignment,
            "expected_alignment": args.display_item_alignment,
        }
        table_summaries.append(summary)
        if args.display_item_alignment != "any" and alignment != args.display_item_alignment:
            add_finding(
                findings,
                "major",
                "DISPLAY_ITEM_ALIGNMENT_MISMATCH",
                f"Word table alignment is {alignment or 'unresolved/default'}; expected {args.display_item_alignment} unless the target style overrides it.",
                f"table {t_idx}",
                summary,
            )
        if long_table and not summary["has_repeated_header"]:
            add_finding(
                findings,
                "warn",
                "LONG_TABLE_HEADER_NOT_REPEATED",
                "Likely long table does not statically declare a repeated header row.",
                f"table {t_idx}",
                summary,
            )
        if args.submission_ready and not args.use_word_com:
            add_finding(
                findings,
                "major",
                "TABLE_PAGINATION_UNVERIFIED",
                "Submission-ready table pagination cannot be approved without Word/PDF render verification.",
                f"table {t_idx}",
                summary,
            )
            result["requires_render_qa"] = True
        elif not args.use_word_com and tables:
            result["requires_render_qa"] = True
    result["tables"] = table_summaries
    result["counts"]["misaligned_tables"] = sum(
        1
        for item in table_summaries
        if args.display_item_alignment != "any" and item["alignment"] != args.display_item_alignment
    )

    return result


def audit_word_com(args: argparse.Namespace, result: Dict[str, Any]) -> None:
    docx = Path(args.docx).resolve()
    findings: List[Dict[str, Any]] = result["findings"]
    word_result: Dict[str, Any] = {
        "attempted": True,
        "opened": False,
        "pdf_exported": False,
        "page_count": None,
        "tables": [],
        "equation_counts": {},
    }
    result["word_com"] = word_result

    try:
        import win32com.client  # type: ignore
    except Exception as exc:
        add_finding(
            findings,
            "blocker" if args.submission_ready else "warn",
            "WORD_COM_UNAVAILABLE",
            f"Word COM check requested but pywin32/Word automation is unavailable: {exc}",
            "Word COM",
        )
        return

    word = None
    doc = None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        constants = win32com.client.constants
        def word_constant(name: str, fallback: int) -> int:
            try:
                return int(getattr(constants, name))
            except Exception:
                return fallback

        wd_statistic_pages = word_constant("wdStatisticPages", 2)
        wd_collapse_start = word_constant("wdCollapseStart", 1)
        wd_collapse_end = word_constant("wdCollapseEnd", 0)
        wd_active_end_adjusted_page_number = word_constant("wdActiveEndAdjustedPageNumber", 1)
        wd_export_format_pdf = word_constant("wdExportFormatPDF", 17)
        doc = word.Documents.Open(str(docx), ReadOnly=True, AddToRecentFiles=False, Visible=False)
        word_result["opened"] = True
        try:
            word_result["page_count"] = int(doc.ComputeStatistics(wd_statistic_pages))
        except Exception:
            word_result["page_count"] = None

        try:
            word_result["equation_counts"] = {
                "omaths": int(doc.OMaths.Count),
                "inline_shapes": int(doc.InlineShapes.Count),
                "shapes": int(doc.Shapes.Count),
            }
        except Exception:
            word_result["equation_counts"] = {}

        for idx in range(1, int(doc.Tables.Count) + 1):
            table = doc.Tables(idx)
            info = {"table": idx}
            try:
                info["rows"] = int(table.Rows.Count)
                info["columns"] = int(table.Columns.Count)
            except Exception:
                pass
            try:
                rng_start = table.Range.Duplicate
                rng_start.Collapse(wd_collapse_start)
                rng_end = table.Range.Duplicate
                rng_end.Collapse(wd_collapse_end)
                info["start_page"] = int(rng_start.Information(wd_active_end_adjusted_page_number))
                info["end_page"] = int(rng_end.Information(wd_active_end_adjusted_page_number))
                info["crosses_pages"] = info["end_page"] > info["start_page"]
            except Exception as exc:
                info["page_detection_error"] = str(exc)
            try:
                info["first_row_heading_format"] = bool(table.Rows(1).HeadingFormat)
            except Exception:
                info["first_row_heading_format"] = None
            try:
                info["allow_break_across_pages"] = bool(table.Rows.AllowBreakAcrossPages)
            except Exception:
                info["allow_break_across_pages"] = None
            word_result["tables"].append(info)
            if info.get("crosses_pages") and not info.get("first_row_heading_format"):
                add_finding(
                    findings,
                    "major",
                    "TABLE_PAGINATION_FAILURE",
                    "Rendered table crosses pages but first row is not marked to repeat as heading.",
                    f"table {idx}",
                    info,
                )
            if "page_detection_error" in info:
                add_finding(
                    findings,
                    "major" if args.submission_ready else "warn",
                    "TABLE_PAGINATION_UNVERIFIED",
                    "Could not determine rendered start/end pages for table.",
                    f"table {idx}",
                    info,
                )

        if args.export_pdf:
            out_dir = Path(args.out_dir).resolve()
            out_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = out_dir / (docx.stem + ".layout-audit.pdf")
            doc.ExportAsFixedFormat(str(pdf_path), wd_export_format_pdf)
            word_result["pdf_exported"] = True
            word_result["pdf_path"] = str(pdf_path)
    except Exception as exc:
        add_finding(
            findings,
            "blocker" if args.submission_ready else "warn",
            "WORD_COM_RENDER_FAILED",
            f"Word COM render check failed: {exc}",
            "Word COM",
        )
    finally:
        if doc is not None:
            try:
                doc.Close(False)
            except Exception:
                pass
        if word is not None:
            try:
                word.Quit()
            except Exception:
                pass


def finalize_result(result: Dict[str, Any]) -> Dict[str, Any]:
    counts = Counter(f["severity"] for f in result.get("findings", []))
    result["finding_counts"] = dict(counts)
    if counts.get("blocker", 0):
        status = "blocked"
    elif counts.get("major", 0):
        status = "needs_major_fixes"
    elif counts.get("warn", 0):
        status = "pass_with_warnings"
    else:
        status = "pass"
    result["status"] = status
    return result


def write_outputs(args: argparse.Namespace, result: Dict[str, Any]) -> Tuple[Path, Path]:
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "docx_layout_audit.json"
    md_path = out_dir / "docx_layout_audit_report.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# DOCX Layout Audit Report",
        "",
        f"- Input: `{result.get('input')}`",
        f"- Checked at: `{result.get('checked_at')}`",
        f"- Academic profile: `{result.get('academic_profile')}`",
        f"- Profile note: `{result.get('profile_note')}`",
        f"- Status: `{result.get('status')}`",
        f"- Requires render QA: `{result.get('requires_render_qa')}`",
        f"- Findings: `{result.get('finding_counts', {})}`",
        "",
        "## Key Counts",
        "",
    ]
    for key, value in sorted(result.get("counts", {}).items()):
        lines.append(f"- {key}: {value}")
    for key, value in sorted(result.get("summary_values", {}).items()):
        lines.append(f"- {key}: {value}")
    if result.get("word_com"):
        lines.extend(["", "## Word COM Render Check", ""])
        for key, value in result["word_com"].items():
            if key != "tables":
                lines.append(f"- {key}: {value}")
        lines.append(f"- rendered tables inspected: {len(result['word_com'].get('tables', []))}")
    lines.extend(["", "## Findings", ""])
    if not result.get("findings"):
        lines.append("No findings.")
    else:
        for idx, finding in enumerate(result["findings"], start=1):
            lines.append(
                f"{idx}. **{finding['severity']}** `{finding['code']}`"
                + (f" at `{finding['locator']}`" if finding.get("locator") else "")
            )
            lines.append(f"   - {finding['message']}")
            if finding.get("evidence") is not None:
                evidence = json.dumps(finding["evidence"], ensure_ascii=False)
                if len(evidence) > 800:
                    evidence = evidence[:800] + "..."
                lines.append(f"   - Evidence: `{evidence}`")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Static OOXML checks cannot prove final page layout, MathType editability, table cross-page rendering, or visual overlap.",
            "- For submission-ready DOCX, rerun with `--submission-ready --use-word-com --export-pdf` on a machine with Microsoft Word and inspect the exported PDF.",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit DOCX academic manuscript layout without editing the input file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("docx", help="Input .docx manuscript")
    parser.add_argument("--out-dir", default="layout_audit", help="Directory for JSON/Markdown/PDF outputs")
    parser.add_argument(
        "--academic-profile",
        choices=sorted(ACADEMIC_PROFILE_NOTES),
        default="generic",
        help="Source-backed academic layout profile; target journal/template rules still override defaults",
    )
    parser.add_argument(
        "--english-font-name",
        default="Times New Roman",
        help="Expected English/Latin font family; use 'any' only for a verified target-style override",
    )
    parser.add_argument("--body-font-pt", type=float, default=11.0, help="Expected body font size")
    parser.add_argument("--caption-font-pt", type=float, default=10.0, help="Expected figure/table caption font size")
    parser.add_argument(
        "--caption-size-delta-pt",
        type=float,
        default=1.0,
        help="Expected body-minus-caption font-size difference",
    )
    parser.add_argument(
        "--display-item-alignment",
        choices=("center", "left", "right", "any"),
        default="center",
        help="Expected alignment for inline figure container paragraphs and Word table objects",
    )
    parser.add_argument("--line-spacing", type=float, default=1.25, help="Expected body line spacing multiple")
    parser.add_argument("--long-table-rows", type=int, default=20, help="Rows threshold for likely cross-page tables")
    parser.add_argument("--long-table-chars", type=int, default=2500, help="Text length threshold for likely cross-page tables")
    parser.add_argument("--require-mathtype", action="store_true", help="Require MathType/Word equation-compatible objects")
    parser.add_argument("--require-inline-math", action="store_true", help="Require inline variables as equation objects")
    parser.add_argument("--submission-ready", action="store_true", help="Treat render-dependent gaps as major/blocking issues")
    parser.add_argument("--use-word-com", action="store_true", help="Use Microsoft Word COM automation for render checks")
    parser.add_argument("--export-pdf", action="store_true", help="Export a PDF proof through Word COM")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.export_pdf and not args.use_word_com:
        parser.error("--export-pdf requires --use-word-com")
    if args.caption_size_delta_pt < 0:
        parser.error("--caption-size-delta-pt must be non-negative")

    result = audit_static(args)
    if args.use_word_com:
        audit_word_com(args, result)
    finalize_result(result)
    json_path, md_path = write_outputs(args, result)
    print(f"status={result['status']}")
    print(f"json={json_path}")
    print(f"report={md_path}")
    return 1 if result["status"] in {"blocked", "needs_major_fixes"} else 0


if __name__ == "__main__":
    sys.exit(main())
