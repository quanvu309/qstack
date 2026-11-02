import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
from docx import Document
from docx.shared import Mm

LONG_DASH = chr(0x2014)
HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "build_docx.py"
EXAMPLES = HERE.parent / "examples"

sys.path.insert(0, str(HERE))
import build_docx  # noqa: E402


def load(name):
    return json.loads((EXAMPLES / f"{name}.json").read_text(encoding="utf-8"))


def build(tmp_path, spec, name="out"):
    spec_path = tmp_path / f"{name}.json"
    out = tmp_path / f"{name}.docx"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    assert build_docx.main([str(spec_path), str(out)]) == 0
    return Document(out)


def run_cli(tmp_path, spec):
    spec_path = tmp_path / "bad.json"
    out = tmp_path / "bad.docx"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(SCRIPT), str(spec_path), str(out)],
                          capture_output=True, text=True)
    return proc, out


def header_texts(doc):
    table = doc.tables[0]
    return [[p.text for c in row.cells for p in c.paragraphs if p.text] for row in table.rows]


def body_paragraphs(doc):
    return [p for p in doc.paragraphs if p.text.strip()]


def sign_table(doc):
    return doc.tables[1]


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("examples")
    return {n: build(tmp, load(n), n) for n in ("quyet-dinh", "cong-van", "bien-ban")}


@pytest.mark.parametrize("name", ["quyet-dinh", "cong-van", "bien-ban"])
def test_page_setup_and_font(built, name):
    doc = built[name]
    sec = doc.sections[0]
    for actual, mm in ((sec.page_width, 210), (sec.page_height, 297), (sec.top_margin, 20),
                       (sec.bottom_margin, 20), (sec.left_margin, 30), (sec.right_margin, 15)):
        assert abs(actual - Mm(mm)) < Mm(0.1)
    normal = doc.styles["Normal"]
    assert normal.font.name == "Times New Roman"
    rfonts = normal.element.rPr.rFonts
    for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
        assert rfonts.get(f"{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}{attr}") == "Times New Roman"


@pytest.mark.parametrize("name", ["quyet-dinh", "cong-van", "bien-ban"])
def test_every_run_is_times_new_roman_and_black(built, name):
    doc = built[name]
    runs = [r for p in doc.paragraphs for r in p.runs]
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                runs += [r for p in c.paragraphs for r in p.runs]
    assert runs and all(r.font.name == "Times New Roman" for r in runs)
    assert all(str(r.font.color.rgb) == "000000" for r in runs)


def test_quyet_dinh_header(built):
    top, bottom = header_texts(built["quyet-dinh"])
    assert "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" in top
    assert "Độc lập - Tự do - Hạnh phúc" in top
    assert "TỔNG CÔNG TY ABC" in top and "CÔNG TY CỔ PHẦN XYZ" in top
    assert bottom[0] == "Số: 05/QĐ-XYZ"
    assert bottom[1] == "Hà Nội, ngày 02 tháng 11 năm 2026"


def test_blank_number_leaves_form_for_van_thu(tmp_path):
    spec = load("quyet-dinh")
    del spec["number"]
    doc = build(tmp_path, spec)
    assert header_texts(doc)[1][0] == "Số:      /QĐ-XYZ"


def test_cong_van_header(built):
    doc = built["cong-van"]
    _, bottom = header_texts(doc)
    assert bottom[0] == "Số: 12/XYZ-HCNS"
    assert bottom[1].startswith("V/v đề nghị cung cấp")
    texts = [p.text for p in body_paragraphs(doc)]
    assert texts[0] == "Kính gửi: Công ty TNHH DEF"
    assert "CÔNG VĂN" not in " ".join(texts)


@pytest.mark.parametrize("date,expected", [
    ("2026-01-05", "Hà Nội, ngày 05 tháng 01 năm 2026"),
    ("2026-06-15", "Hà Nội, ngày 15 tháng 6 năm 2026"),
    ("2026-11-02", "Hà Nội, ngày 02 tháng 11 năm 2026"),
    ("2026-11", "Hà Nội, ngày      tháng 11 năm 2026"),
])
def test_date_line(tmp_path, date, expected):
    spec = load("quyet-dinh")
    spec["date"] = date
    assert header_texts(build(tmp_path, spec))[1][1] == expected


def test_bien_ban_has_no_date_and_two_signers(built):
    doc = built["bien-ban"]
    _, bottom = header_texts(doc)
    assert bottom == ["Số: 07/BB-XYZ"]
    cells = sign_table(doc).rows[0].cells
    assert cells[0].paragraphs[0].text == "THƯ KÝ"
    assert cells[1].paragraphs[0].text == "CHỦ TỌA"
    assert cells[0].paragraphs[-1].text == "Đỗ Thị Lan"
    assert cells[1].paragraphs[-1].text == "Lê Hoàng Nam"
    left_notes = sign_table(doc).rows[1].cells[0]
    assert left_notes.paragraphs[0].text == "Nơi nhận:"


def test_quyet_dinh_structure(built):
    texts = [p.text for p in body_paragraphs(built["quyet-dinh"])]
    assert texts[0] == "QUYẾT ĐỊNH"
    assert texts[1] == "Về việc bổ nhiệm Trưởng phòng Kinh doanh"
    assert texts[2] == "GIÁM ĐỐC CÔNG TY CỔ PHẦN XYZ"
    basis = [t for t in texts if t.startswith(("Căn cứ", "Xét đề nghị"))]
    assert len(basis) == 4
    assert all(t.endswith(";") for t in basis[:-1]) and basis[-1].endswith(".")
    assert texts.index("QUYẾT ĐỊNH:") == texts.index(basis[-1]) + 1
    assert texts[texts.index("QUYẾT ĐỊNH:") + 1].startswith("Điều 1.")


def test_basis_punctuation_is_normalised(tmp_path):
    spec = load("quyet-dinh")
    spec["basis"] = ["Căn cứ A.", "Căn cứ B;", "Căn cứ C"]
    texts = [p.text for p in body_paragraphs(build(tmp_path, spec))]
    assert texts[3:6] == ["Căn cứ A;", "Căn cứ B;", "Căn cứ C."]


@pytest.mark.parametrize("name", ["quyet-dinh", "cong-van", "bien-ban"])
def test_last_body_paragraph_closes_with_slash_dot(built, name):
    assert body_paragraphs(built[name])[-1].text.endswith("/.")


def test_slash_dot_is_not_doubled(tmp_path):
    spec = load("quyet-dinh")
    spec["body"][-1]["text"] = "Quyết định này có hiệu lực kể từ ngày ký./."
    last = body_paragraphs(build(tmp_path, spec))[-1].text
    assert last.endswith("ký./.") and not last.endswith("/./.")


def test_noi_nhan_entries(built):
    cell = sign_table(built["quyet-dinh"]).rows[0].cells[0]
    texts = [p.text for p in cell.paragraphs]
    assert texts == ["Nơi nhận:", "- Như Điều 4;", "- Ban Giám đốc;", "- Lưu: VT, HCNS."]


def test_signature_block_is_on_the_right(built):
    cell = sign_table(built["quyet-dinh"]).rows[0].cells[1]
    assert [p.text for p in cell.paragraphs] == ["GIÁM ĐỐC", "Lê Hoàng Nam"]


def test_multiple_recipients_in_kinh_gui(tmp_path):
    spec = load("cong-van")
    spec["to"] = ["Công ty TNHH DEF", "Công ty Cổ phần GHI."]
    texts = [p.text for p in body_paragraphs(build(tmp_path, spec))]
    assert texts[0] == "Kính gửi:"
    assert texts[1:3] == ["- Công ty TNHH DEF;", "- Công ty Cổ phần GHI."]


def test_page_number_only_after_first_page(built):
    sec = built["quyet-dinh"].sections[0]
    assert sec.different_first_page_header_footer is True
    assert "PAGE" in sec.header._element.xml
    assert "PAGE" not in sec.first_page_header._element.xml
    assert not sec.first_page_header.is_linked_to_previous


def test_header_table_is_borderless_two_columns(built):
    table = built["quyet-dinh"].tables[0]
    assert len(table.columns) == 2 and len(table.rows) == 2
    assert "w:tblBorders" not in table._tbl.xml
    assert abs(sum(c.width for c in table.rows[0].cells) - Mm(165)) < Mm(0.1)


def test_rules_are_bottom_borders(built):
    xml = built["quyet-dinh"].tables[0]._tbl.xml
    assert xml.count("<w:bottom ") == 2


def test_no_long_dash_in_output_or_sources(built):
    for path in (SCRIPT, HERE / "test_build_docx.py", *EXAMPLES.glob("*.json")):
        assert LONG_DASH not in path.read_text(encoding="utf-8")
    for doc in built.values():
        assert LONG_DASH not in doc.element.xml


@pytest.mark.parametrize("mutate,needle", [
    (lambda s: s.pop("unit"), 'cong-van requires "unit"'),
    (lambda s: s.__setitem__("type", "cong-van"), None),
])
def test_cong_van_validation(tmp_path, mutate, needle):
    spec = load("cong-van")
    mutate(spec)
    proc, out = run_cli(tmp_path, spec)
    if needle:
        assert proc.returncode == 2
        assert f"error: {needle}" in proc.stderr
        assert not out.exists()


def test_quyet_dinh_requires_authority(tmp_path):
    spec = load("quyet-dinh")
    del spec["authority"]
    proc, out = run_cli(tmp_path, spec)
    assert proc.returncode == 2
    assert 'error: quyet-dinh requires "authority"' in proc.stderr
    assert not out.exists()


def test_bien_ban_needs_two_signers(tmp_path):
    spec = load("bien-ban")
    spec["signers"] = spec["signers"][:1]
    proc, out = run_cli(tmp_path, spec)
    assert proc.returncode == 2
    assert '"signers"' in proc.stderr and "exactly 2" in proc.stderr
    assert not out.exists()


def test_to_rejected_on_thong_bao(tmp_path):
    spec = load("quyet-dinh")
    spec.update(type="thong-bao", to=["Công ty TNHH DEF"])
    for key in ("authority",):
        del spec[key]
    proc, out = run_cli(tmp_path, spec)
    assert proc.returncode == 2
    assert 'error: thong-bao does not accept "to"' in proc.stderr
    assert not out.exists()


def test_unknown_type(tmp_path):
    spec = load("quyet-dinh")
    spec["type"] = "hop-dong"
    proc, out = run_cli(tmp_path, spec)
    assert proc.returncode == 2
    assert '"type"' in proc.stderr and "hop-dong" in proc.stderr
    assert not out.exists()


def test_all_problems_reported_one_per_line(tmp_path):
    spec = copy.deepcopy(load("quyet-dinh"))
    del spec["authority"], spec["basis"], spec["place"]
    proc, _ = run_cli(tmp_path, spec)
    lines = proc.stderr.strip().splitlines()
    assert proc.returncode == 2 and len(lines) == 3
    assert all(line.startswith("error: ") for line in lines)


def test_other_types_build(tmp_path):
    base = load("quyet-dinh")
    for code in ("to-trinh", "thong-bao", "bao-cao", "ke-hoach", "giay-moi", "giay-gioi-thieu"):
        spec = {k: v for k, v in base.items() if k not in ("authority", "basis")}
        spec["type"] = code
        if code in ("to-trinh", "bao-cao"):
            spec["to"] = ["Hội đồng quản trị"]
        doc = build(tmp_path, spec, code)
        title = build_docx.TYPES[code].title
        assert title in [p.text for p in doc.paragraphs]
        assert header_texts(doc)[1][0] == f"Số: 05/{build_docx.TYPES[code].abbr}-XYZ"


def test_help_lists_fields_and_type_codes():
    proc = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
    assert proc.returncode == 0
    for word in ("issuer", "unit", "authority", "basis", "recipients", "signers", *build_docx.TYPES):
        assert word in proc.stdout
