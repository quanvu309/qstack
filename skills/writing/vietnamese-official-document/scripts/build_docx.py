#!/usr/bin/env python3
"""Build a Vietnamese administrative document (.docx) laid out per Nghi dinh 30/2020/ND-CP.

Run: uv run --with python-docx scripts/build_docx.py SPEC.json OUT.docx
"""
import argparse
import datetime
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

FONT = "Times New Roman"
BLANK = " " * 6
TEXT_W = 165  # mm, A4 210 minus margins 30 + 15 (Phu luc I, Phan I)
COL_L, COL_R = 62, 103  # mm; the right column holds the Quốc hiệu and the longest date line on one line
PAD = 1.5  # mm cell padding on each side, the gutter between the two header columns
MM_PT = 72 / 25.4
# Rendered width of "Độc lập - Tự do - Hạnh phúc" at 13 pt bold; its rule must equal the text (Phu luc I, o 1).
TIEU_NGU_PT = 159
RULE_RATIO = 0.4  # decree allows 1/3 to 1/2 of the line length
INDENT_MM = 12.7  # 1.27 cm first-line indent of the content
SIGN_GAP_PT = 62  # about 4 empty lines for signature and seal
LINE_PT = 16  # one 14 pt line, used to keep two signers' names on the same row
BODY_LINE = 1.15  # decree allows single to 1.5

QUOC_HIEU = "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM"
TIEU_NGU = "Độc lập - Tự do - Hạnh phúc"

# Sizes follow the decree's table V example set.
S_QUOC_HIEU, S_TIEU_NGU, S_ORG, S_SO, S_VV, S_DATE = 12, 13, 12, 13, 12, 13
S_BODY, S_NOI_NHAN, S_LIST, S_PAGE = 14, 12, 11, 14


@dataclass(frozen=True)
class DocType:
    title: str | None
    abbr: str | None
    to: str = "no"  # required | optional | no
    basis: str = "no"
    subject: str = "required"  # required | optional
    show_subject: bool = True
    vv: bool = False  # trich yeu goes under So as "V/v ..."
    authority: bool = False
    unit: bool = False
    dated: bool = True
    signers: int = 1


TYPES = {
    "quyet-dinh": DocType("QUYẾT ĐỊNH", "QĐ", basis="required", authority=True),
    "cong-van": DocType(None, None, to="required", show_subject=False, vv=True, unit=True),
    "to-trinh": DocType("TỜ TRÌNH", "TTr", to="optional", basis="optional"),
    "thong-bao": DocType("THÔNG BÁO", "TB", basis="optional"),
    "bao-cao": DocType("BÁO CÁO", "BC", to="optional", basis="optional"),
    "ke-hoach": DocType("KẾ HOẠCH", "KH", basis="optional"),
    "bien-ban": DocType("BIÊN BẢN", "BB", dated=False, signers=2),
    "giay-moi": DocType("GIẤY MỜI", "GM"),
    "giay-gioi-thieu": DocType("GIẤY GIỚI THIỆU", "GGT", subject="optional", show_subject=False),
}

FIELDS = {"type", "issuer", "unit", "number", "place", "date", "subject", "to", "authority",
          "basis", "body", "recipients", "signers"}


def nfc(value):
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [nfc(v) for v in value]
    if isinstance(value, dict):
        return {nfc(k): nfc(v) for k, v in value.items()}
    return value


def is_text(value):
    return isinstance(value, str) and value.strip() != ""


def parse_date(value):
    m = re.fullmatch(r"(\d{4})-(\d{2})(?:-(\d{2}))?", value) if isinstance(value, str) else None
    if not m:
        return None
    year, month, day = int(m[1]), int(m[2]), int(m[3]) if m[3] else None
    try:
        datetime.date(year, month, day or 1)
    except ValueError:
        return None
    return year, month, day


def validate(spec):
    if not isinstance(spec, dict):
        return ["error: the spec must be a JSON object"]
    code = spec.get("type")
    if code not in TYPES:
        return [f'error: unknown "type" {code!r}, expected one of: {", ".join(TYPES)}']
    dt = TYPES[code]
    errs = [f'error: unknown field "{k}"' for k in spec if k not in FIELDS]

    def text_field(key, required=True):
        if key not in spec:
            if required:
                errs.append(f'error: {code} requires "{key}"')
        elif not is_text(spec[key]):
            errs.append(f'error: "{key}" must be a non-empty string')

    def list_field(key, state, minimum=1):
        if key not in spec:
            if state == "required":
                errs.append(f'error: {code} requires "{key}"')
            return
        if state == "no":
            errs.append(f'error: {code} does not accept "{key}"')
        elif not (isinstance(spec[key], list) and len(spec[key]) >= minimum
                  and all(is_text(v) for v in spec[key])):
            errs.append(f'error: "{key}" must be a list of at least {minimum} non-empty string(s)')

    issuer = spec.get("issuer")
    if not isinstance(issuer, dict):
        errs.append(f'error: {code} requires "issuer" with "name" and "abbr"')
    else:
        for key in ("name", "abbr"):
            if not is_text(issuer.get(key)):
                errs.append(f'error: "issuer.{key}" is required')
        if "parent" in issuer and not is_text(issuer["parent"]):
            errs.append('error: "issuer.parent" must be a non-empty string')

    if dt.unit:
        text_field("unit")
    elif "unit" in spec:
        errs.append(f'error: {code} does not accept "unit"')
    if dt.authority:
        text_field("authority")
    elif "authority" in spec:
        errs.append(f'error: {code} does not accept "authority"')
    text_field("subject", dt.subject == "required")
    list_field("to", dt.to)
    list_field("basis", dt.basis)
    list_field("recipients", "optional")

    if "number" in spec and not (isinstance(spec["number"], int)
                                 and not isinstance(spec["number"], bool) and spec["number"] >= 1):
        errs.append('error: "number" must be a positive integer')
    if dt.dated:
        text_field("place")
        if "date" not in spec:
            errs.append(f'error: {code} requires "date"')
        elif parse_date(spec["date"]) is None:
            errs.append('error: "date" must be a real date as "YYYY-MM-DD" or "YYYY-MM"')

    body = spec.get("body")
    if not isinstance(body, list) or not body:
        errs.append(f'error: {code} requires "body" as a non-empty list')
    else:
        for i, block in enumerate(body):
            ok = is_text(block) or (isinstance(block, dict) and (
                (set(block) == {"heading"} and is_text(block["heading"]))
                or (set(block) == {"lead", "text"} and is_text(block["lead"]) and is_text(block["text"]))))
            if not ok:
                errs.append(f'error: "body[{i}]" must be a string, {{"heading"}} or {{"lead","text"}}')

    signers = spec.get("signers")
    if not isinstance(signers, list) or len(signers) != dt.signers:
        errs.append(f'error: {code} requires exactly {dt.signers} "signers"')
    else:
        for i, s in enumerate(signers):
            pos = s.get("position") if isinstance(s, dict) else None
            if not isinstance(s, dict) or not is_text(s.get("name")):
                errs.append(f'error: "signers[{i}].name" is required')
            elif pos is None and dt.signers == 1:
                errs.append(f'error: "signers[{i}].position" is required')
            elif pos is not None and not (isinstance(pos, list) and all(is_text(p) for p in pos)
                                          and (pos or dt.signers == 2)):
                errs.append(f'error: "signers[{i}].position" must be a list of strings')
    return errs


def so_ky_hieu(spec, dt):
    abbr = spec["issuer"]["abbr"]
    return f"{abbr}-{spec['unit']}" if dt.unit else f"{dt.abbr}-{abbr}"


def format_so(spec, dt):
    ky_hieu = so_ky_hieu(spec, dt)
    n = spec.get("number")
    if n is None:
        return f"Số:{BLANK}/{ky_hieu}"
    return f"Số: {n:02d}/{ky_hieu}"


def format_date(place, date):
    year, month, day = parse_date(date)
    day_text = BLANK if day is None else (f"{day:02d}" if day < 10 else str(day))
    month_text = f"{month:02d}" if month < 3 else str(month)
    sep = "" if day is None else " "
    return f"{place}, ngày{sep}{day_text}{sep}tháng {month_text} năm {year}"


def strip_end(text):
    return re.sub(r"[\s.;,]+$", "", text)


def punctuated(items, prefix=""):
    items = [strip_end(re.sub(r"^\s*-\s*", "", it)) for it in items]
    return [f"{prefix}{it}{'.' if i == len(items) - 1 else ';'}" for i, it in enumerate(items)]


def close_body(text):
    text = text.rstrip()
    if text.endswith("/."):
        return text
    return text + ("/." if text[-1] in ".!?" else "./.")


def est_pt(text, size, bold=False):
    # Calibrated against Liberation Serif (same metrics as Times New Roman): em per character.
    factor = 0.62 if text.isupper() else (0.48 if bold else 0.45)
    return len(text) * size * factor


def run_fonts(run):
    rfonts = run._r.get_or_add_rPr().get_or_add_rFonts()
    for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
        rfonts.set(qn(f"w:{attr}"), FONT)


def add_run(p, text, size, bold=False, italic=False):
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)
    run_fonts(run)
    return run


def add_para(container, runs, align=WD_ALIGN_PARAGRAPH.LEFT, before=0, after=0, line=1.0,
             first=0, left=0, right=0, keep=False):
    p = container.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = align
    pf.space_before, pf.space_after = Pt(before), Pt(after)
    pf.line_spacing = line
    pf.first_line_indent, pf.left_indent, pf.right_indent = Mm(first), Mm(left), Mm(right)
    pf.keep_with_next = keep
    for text, size, bold, italic in runs:
        add_run(p, text, size, bold, italic)
    return p


def add_rule(container, segment_pt, column_pt, after=0):
    p = container.add_paragraph()
    pf = p.paragraph_format
    margin = max(0, (column_pt - min(segment_pt, column_pt)) / 2)
    pf.left_indent = pf.right_indent = Pt(margin)
    pf.space_before, pf.space_after = Pt(3), Pt(after)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(2)
    pf.keep_with_next = True
    ppr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    for key, val in (("val", "single"), ("sz", "6"), ("space", "1"), ("color", "000000")):
        bottom.set(qn(f"w:{key}"), val)
    borders.append(bottom)
    ppr.append(borders)
    mark = OxmlElement("w:rPr")
    size = OxmlElement("w:sz")
    size.set(qn("w:val"), "4")
    mark.append(size)
    ppr.append(mark)
    return p


def finish(cell):
    if len(cell.paragraphs) > 1:
        cell._tc.remove(cell.paragraphs[0]._p)


def make_table(doc, rows, widths_mm):
    table = doc.add_table(rows=rows, cols=len(widths_mm))
    table.autofit = False
    pr = table._tbl.tblPr
    width = pr.find(qn("w:tblW"))
    width.set(qn("w:type"), "dxa")
    width.set(qn("w:w"), str(round(sum(widths_mm) / 25.4 * 1440)))
    indent = OxmlElement("w:tblInd")
    indent.set(qn("w:w"), "0")
    indent.set(qn("w:type"), "dxa")
    width.addnext(indent)
    margins = OxmlElement("w:tblCellMar")
    for side in ("left", "right"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(round(PAD / 25.4 * 1440)))
        el.set(qn("w:type"), "dxa")
        margins.append(el)
    pr.find(qn("w:tblLayout")).addnext(margins)
    for i, w in enumerate(widths_mm):
        table.columns[i].width = Mm(w)
        for cell in table.columns[i].cells:
            cell.width = Mm(w)
    for row in table.rows:
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
    return table


CENTER, JUSTIFY = WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.JUSTIFY


def add_header_block(doc, spec, dt):
    table = make_table(doc, 2, [COL_L, COL_R])
    left, right = table.rows[0].cells
    left.vertical_alignment = WD_ALIGN_VERTICAL.TOP
    issuer = spec["issuer"]
    name = issuer["name"].upper()
    if issuer.get("parent"):
        add_para(left, [(issuer["parent"].upper(), S_ORG, False, False)], CENTER)
    add_para(left, [(name, S_ORG, True, False)], CENTER)
    name_pt = min(est_pt(name, S_ORG, True), (COL_L - 2 * PAD) * MM_PT)
    add_rule(left, RULE_RATIO * name_pt, (COL_L - 2 * PAD) * MM_PT)
    add_para(right, [(QUOC_HIEU, S_QUOC_HIEU, True, False)], CENTER)
    add_para(right, [(TIEU_NGU, S_TIEU_NGU, True, False)], CENTER)
    add_rule(right, TIEU_NGU_PT, (COL_R - 2 * PAD) * MM_PT)

    so_cell, date_cell = table.rows[1].cells
    add_para(so_cell, [(format_so(spec, dt), S_SO, False, False)], CENTER, before=6)
    if dt.vv:
        subject = re.sub(r"^\s*v/v\s*:?\s*", "", spec["subject"], flags=re.I)
        add_para(so_cell, [(f"V/v {subject}", S_VV, False, False)], CENTER, before=6)
    if dt.dated:
        add_para(date_cell, [(format_date(spec["place"], spec["date"]), S_DATE, False, True)],
                 CENTER, before=6)
    for cell in (left, right, so_cell, date_cell):
        finish(cell)


def add_kinh_gui(doc, recipients):
    if len(recipients) == 1:
        text = f"Kính gửi: {strip_end(recipients[0])}"
        add_para(doc, [(text, S_BODY, False, False)], CENTER, before=12, after=6)
        return
    colon_mm = est_pt("Kính gửi", S_BODY) / MM_PT
    items = punctuated(recipients, "- ")
    widest_mm = max(est_pt(i, S_BODY) for i in items) / MM_PT
    left = min(60, max(0, (TEXT_W - colon_mm - widest_mm) / 2))
    add_para(doc, [("Kính gửi:", S_BODY, False, False)], before=12, left=left, keep=True)
    for i, item in enumerate(items):
        add_para(doc, [(item, S_BODY, False, False)], left=left + colon_mm,
                 after=6 if i == len(items) - 1 else 0, keep=i < len(items) - 1)


def add_title_block(doc, spec, dt):
    if dt.title:
        add_para(doc, [(dt.title, 14, True, False)], CENTER, before=12, keep=True)
    if dt.show_subject and "subject" in spec:
        subject = spec["subject"]
        add_para(doc, [(subject, 14, True, False)], CENTER, keep=True)
        width_pt = min(est_pt(subject, 14, True), TEXT_W * MM_PT)
        add_rule(doc, RULE_RATIO * width_pt, TEXT_W * MM_PT, after=6)
    if dt.authority:
        add_para(doc, [(spec["authority"].upper(), 14, True, False)], CENTER, before=12, after=6,
                 keep=True)
    if "basis" in spec:
        for line in punctuated(spec["basis"]):
            add_para(doc, [(line, S_BODY, False, True)], JUSTIFY, after=6, line=BODY_LINE,
                     first=INDENT_MM)
    if dt.authority:
        add_para(doc, [("QUYẾT ĐỊNH:", 14, True, False)], CENTER, before=6, after=6, keep=True)


def add_body(doc, blocks):
    last = len(blocks) - 1
    for i, block in enumerate(blocks):
        lead, heading = "", None
        if isinstance(block, str):
            text = block
        elif "heading" in block:
            text = heading = block["heading"]
        else:
            lead, text = block["lead"], block["text"]
        if i == last:
            text = close_body(text)
            if heading is not None:
                heading = text
        if heading is not None:
            add_para(doc, [(text, S_BODY, True, False)], before=6, after=6, line=BODY_LINE,
                     first=INDENT_MM, keep=True)
            continue
        runs = ([(lead + " ", S_BODY, True, False)] if lead else []) + [(text, S_BODY, False, False)]
        add_para(doc, runs, JUSTIFY, after=6, line=BODY_LINE, first=INDENT_MM, keep=i == last)


def fill_recipients(cell, recipients, before=6):
    add_para(cell, [("Nơi nhận:", S_NOI_NHAN, True, True)], before=before, keep=True)
    items = punctuated(recipients, "- ")
    for i, item in enumerate(items):
        add_para(cell, [(item, S_LIST, False, False)], keep=i < len(items) - 1)
    finish(cell)


def fill_signer(cell, signer, label=None, pad_lines=0):
    if label:
        add_para(cell, [(label, 14, True, False)], CENTER, before=6, keep=True)
    positions = signer.get("position") or []
    for i, line in enumerate(positions):
        add_para(cell, [(line.upper(), 14, True, False)], CENTER,
                 before=6 if i == 0 and not label else 0, keep=True)
    add_para(cell, [(signer["name"], 14, True, False)], CENTER,
             before=SIGN_GAP_PT + pad_lines * LINE_PT)
    finish(cell)


def add_signatures(doc, spec, dt):
    recipients = spec.get("recipients")
    signers = spec["signers"]
    if dt.signers == 2:
        table = make_table(doc, 2 if recipients else 1, [TEXT_W / 2, TEXT_W / 2])
        depth = max(len(sg.get("position") or []) for sg in signers)
        for cell, signer, label in zip(table.rows[0].cells, signers, ("THƯ KÝ", "CHỦ TỌA")):
            fill_signer(cell, signer, label, depth - len(signer.get("position") or []))
        if recipients:
            fill_recipients(table.rows[1].cells[0], recipients, before=12)
        return
    table = make_table(doc, 1, [TEXT_W / 2, TEXT_W / 2])
    left, right = table.rows[0].cells
    if recipients:
        fill_recipients(left, recipients)
    fill_signer(right, signers[0])


def add_field(p, instruction, size):
    for kind in ("begin", None, "separate", "text", "end"):
        run = add_run(p, "", size)
        if kind in ("begin", "separate", "end"):
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        elif kind is None:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = f" {instruction} "
        else:
            el = OxmlElement("w:t")
            el.text = "2"
        run._r.append(el)


def setup_document():
    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.top_margin = sec.bottom_margin = Mm(20)
    sec.left_margin, sec.right_margin = Mm(30), Mm(15)
    sec.header_distance = sec.footer_distance = Mm(10)

    defaults = doc.styles.element.find(qn("w:docDefaults")).find(".//" + qn("w:rFonts"))
    if defaults is not None:
        for attr in list(defaults.attrib):
            del defaults.attrib[attr]
        for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
            defaults.set(qn(f"w:{attr}"), FONT)
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(S_BODY)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_before = normal.paragraph_format.space_after = Pt(0)
    rfonts = normal.element.rPr.rFonts
    for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
        rfonts.set(qn(f"w:{attr}"), FONT)
    lang = OxmlElement("w:lang")
    lang.set(qn("w:val"), "vi-VN")
    lang.set(qn("w:eastAsia"), "vi-VN")
    normal.element.rPr.append(lang)

    # Page number sits centred in the top margin and is hidden on page 1 (Phu luc I).
    sec.different_first_page_header_footer = True
    sec.first_page_header.is_linked_to_previous = False
    sec.header.is_linked_to_previous = False
    page = sec.header.paragraphs[0]
    page.alignment = CENTER
    add_field(page, "PAGE", S_PAGE)
    return doc


def build(spec):
    dt = TYPES[spec["type"]]
    doc = setup_document()
    add_header_block(doc, spec, dt)
    if dt.vv:
        add_kinh_gui(doc, spec["to"])
    add_title_block(doc, spec, dt)
    if not dt.vv and "to" in spec:
        add_kinh_gui(doc, spec["to"])
    add_body(doc, spec["body"])
    add_signatures(doc, spec, dt)
    add_para(doc, [("", 1, False, False)], line=1.0)
    return doc


def build_parser():
    codes = "\n".join(
        f"  {code:<16}{dt.title or '(no title line)':<18}{dt.abbr or '-'}" for code, dt in TYPES.items())
    epilog = f"""\
spec fields (JSON object):
  type        required, one of the codes below
  issuer      required: {{"name", "abbr", "parent" (optional, cơ quan chủ quản)}}
  unit        công văn only, required: drafting-unit abbreviation, ký hiệu = issuer.abbr-unit
  number      optional positive integer; absent leaves "Số:      /..." blank for văn thư
  place       địa danh, required except biên bản
  date        "YYYY-MM-DD" or "YYYY-MM" (day left blank), required except biên bản
  subject     trích yếu, required except giấy giới thiệu; công văn gets the "V/v " prefix
  to          Kính gửi list: required for công văn, optional for tờ trình and báo cáo
  authority   quyết định only, required: người/cơ quan ban hành, rendered uppercase
  basis       căn cứ list: required for quyết định (1+); optional for tờ trình, thông báo,
              báo cáo, kế hoạch; ";" and "." are added for you
  body        required list: "paragraph" | {{"heading": "..."}} | {{"lead": "Điều 1.", "text": "..."}}
  recipients  Nơi nhận list; "- ", ";" and the final "." are added for you
  signers     exactly 1 {{"position": ["KT. GIÁM ĐỐC", "PHÓ GIÁM ĐỐC"], "name": "..."}};
              biên bản takes exactly 2: [THƯ KÝ, CHỦ TỌA] (position optional)

type codes (code, title, ký hiệu):
{codes}

Exit status 2 on an invalid spec (one "error:" line per problem); no file is written.
"""
    ap = argparse.ArgumentParser(
        prog="build_docx.py",
        description="Build a Nghị định 30/2020/NĐ-CP .docx from a JSON spec.",
        epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="path to the JSON spec")
    ap.add_argument("out", help="path of the .docx to write")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        with open(args.spec, encoding="utf-8") as f:
            spec = nfc(json.load(f))
    except (OSError, ValueError) as e:
        print(f"error: cannot read {args.spec}: {e}", file=sys.stderr)
        return 2
    errs = validate(spec)
    if errs:
        print("\n".join(errs), file=sys.stderr)
        return 2
    doc = build(spec)
    partial = f"{args.out}.part"
    try:
        doc.save(partial)
        os.replace(partial, args.out)
    except OSError as e:
        if os.path.exists(partial):
            os.remove(partial)
        print(f"error: cannot write {args.out}: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
