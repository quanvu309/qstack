# Layout (thể thức) of an official document

Source: Nghị định 30/2020/NĐ-CP, Phụ lục I and Phụ lục III (https://datafiles.chinhphu.vn/cpp/files/vbpq/2020/03/30.signed.pdf), in force and unamended as of 2026-11-02. It binds state bodies and state-owned enterprises (Điều 2); private companies use it by convention. `scripts/build_docx.py` implements every value below; use this file when formatting by hand (Word, Google Docs, HTML) or answering a layout question.

## Page

A4 portrait. Margins: top 20-25 mm, bottom 20-25 mm, left 30-35 mm, right 15-20 mm. Times New Roman, Unicode, black. Page numbers from page 2, top centre, 13-14 pt; page 1 shows none. Sizes scale together: when the Quốc hiệu is 13, the Tiêu ngữ and date are 14.

## Header (page 1)

Two columns. The left holds who issued it and the number; the right holds the national motto and the date. "Số" and the date share one row.

| Element | Column | Text | Size and style |
| --- | --- | --- | --- |
| Cơ quan chủ quản (if any) | left | "TỔNG CÔNG TY ABC" | 12-13, caps, regular |
| Cơ quan ban hành | left | "CÔNG TY CỔ PHẦN XYZ" | 12-13, caps, bold; rule below, 1/3 to 1/2 of the line, centred |
| Số, ký hiệu | left | "Số: 05/QĐ-XYZ" | 13; number zero-padded below 10; no spaces around / and - |
| Trích yếu of a công văn | left, under Số, 6 pt gap | "V/v cung cấp hồ sơ năng lực" | 12-13, regular |
| Quốc hiệu | right | "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" | 12-13, caps, bold, one line |
| Tiêu ngữ | right | "Độc lập - Tự do - Hạnh phúc" | 13-14, bold; spaces around each hyphen; rule below exactly as long as the text |
| Địa danh, ngày | right, same row as Số | "Hà Nội, ngày 05 tháng 01 năm 2026" | 13-14, italic |

Date: day below 10 and months 1 and 2 take a leading zero ("ngày 05 tháng 01", "ngày 15 tháng 6", "ngày 02 tháng 11"). Địa danh is the province or city where the issuer sits.

Ký hiệu: `{type abbreviation}-{issuer abbreviation}` ("TB-XYZ"). A công văn has no type abbreviation: `{issuer abbreviation}-{drafting unit}` ("XYZ-HCNS"). Numbers restart at 01 on 1 January.

| Type | Abbr. | Type | Abbr. |
| --- | --- | --- | --- |
| Quyết định | QĐ | Kế hoạch | KH |
| Thông báo | TB | Biên bản | BB |
| Tờ trình | TTr | Giấy mời | GM |
| Báo cáo | BC | Giấy giới thiệu | GGT |
| Hướng dẫn | HD | Chương trình | CTr |
| Quy chế | QC | Quy định | QyĐ |

## Title block

Centred under the header: the type name ("QUYẾT ĐỊNH", 13-14, caps, bold), then the trích yếu ("Về việc...", 13-14, bold) with a rule of 1/3 to 1/2 of its line below. A công văn has no type name; its trích yếu sits in the header.

## Body

Justified, 13-14 pt, first-line indent 1 cm or 1.27 cm, at least 6 pt between paragraphs, line spacing single to 1.5.

- Căn cứ lines: italic, one per line, each ending ";", the last ending ".".
- Điều: "Điều 1." in bold, same size as the text.
- Khoản: "1.", "2."; điểm: "a)", "b)", lettered in the Vietnamese alphabet, so "d)" is followed by "đ)" and "e)" by "g)".
- Báo cáo and kế hoạch sections: "I. KẾT QUẢ THỰC HIỆN" in bold caps, then "1. Về doanh thu" in bold.
- The last body line ends with "/." right after its final period ("...kể từ ngày ký./."). Every Phụ lục III template shows it; the decree states no separate rule.

## Kính gửi

Công văn, and tờ trình or báo cáo to a superior. 13-14 pt. One recipient: "Kính gửi: Công ty TNHH DEF" on one line. Several: "Kính gửi:" then one per line, "- " aligned under the colon, ";" at each end, "." at the last.

## Signature and Nơi nhận

A two-column row under the body.

- Right: authority and position in caps bold 13-14 ("KT. GIÁM ĐỐC" / "PHÓ GIÁM ĐỐC"), space for signature and seal, then the full name in bold 13-14, no academic title before it. TM. signs for a collective, KT. for the head, Q. as acting head, TL. by order, TUQ. by authorisation.
- Left, level with the position line: "Nơi nhận:" in bold italic 12, then entries in 11, each "- ..." ending ";", the last always "- Lưu: VT, {drafting unit}." Công văn, tờ trình and báo cáo start the list with "- Như trên;".
- Paper signatures use blue ink; the seal is red and covers about a third of the signature on its left.

## Phụ lục

Each phụ lục starts on a new page and numbers its own pages from 1, hidden on its first page. Centred at its top:

- "Phụ lục" alone when there is one, "Phụ lục I", "Phụ lục II" when there are several: 14 pt, bold.
- Its title in caps, 13-14 pt, bold.
- In italic: "(Kèm theo Tờ trình số 08/TTr-XYZ ngày 05 tháng 01 năm 2027 của Công ty Cổ phần XYZ)".

The decree sets no table style. The builder draws single borders and a bold header row that repeats on each page.

## Biên bản differences

No địa danh and date line in the header. Two signature blocks side by side, "THƯ KÝ" on the left and "CHỦ TỌA" on the right, with Nơi nhận below them on the left.
