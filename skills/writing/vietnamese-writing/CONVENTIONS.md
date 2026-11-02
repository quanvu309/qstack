# Vietnamese formatting conventions

Written conventions for prose and UI text. A `## Vietnamese voice` section in the project's `AGENTS.md` overrides any default here. Where two forms are both correct, the rule is one form per project, never both.

## Tone marks and spelling

- **Text is Unicode NFC** (precomposed: "ộ" is one code point). Text pasted from PDFs, Word or macOS file names can arrive decomposed (NFD) and then fails search and equality. Normalise before saving.
- **Proper names keep their own spelling.** Never respell a person, brand or place name to match the project style: "Thuỷ", "Vy", "Lý", "Nguyễn Vỹ" stay exactly as their owner writes them.
- **Tone mark placement** on "oa, oe, uy" with no final consonant has two styles: old (hòa, khỏe, thủy) and new (hoà, khoẻ, thuỷ). Default to old: Unikey types it by default and much of the press prints it. Words with a final consonant never vary: "hoàng", "khuyết".
- **i or y** as the lone vowel after an initial consonant (kỹ / kĩ, lý / lí, mỹ / mĩ, tỷ / tỉ): default to y. The y in "uy", in "yê", and at the start of a syllable ("y tá", "ý kiến", "yêu") never changes.
- **Education products** (textbooks, edtech, school material) follow QĐ 1989/QĐ-BGDĐT (2018) instead: new tone style (hoà, thuỷ), i after a consonant (kĩ, lí, mĩ, tỉ lệ), and digits grouped by spaces (1 234 567).
- **Regional words** (bát / chén, lợn / heo, ô / dù, nghìn / ngàn): use the forms the audience uses. For a national audience, keep one set throughout.

## Capitalisation

- Headings, page titles, buttons and menu items are sentence case: "Cài đặt tài khoản", not "Cài Đặt Tài Khoản".
- Personal and place names capitalise every syllable: "Nguyễn Thị Minh Khai", "Hà Nội", "Bà Rịa".
- Organisation names capitalise the first syllable of each component (NĐ 30/2020/NĐ-CP, Phụ lục II): "Bộ Giáo dục và Đào tạo", "Ngân hàng Nhà nước Việt Nam", "Công ty Cổ phần Sữa Việt Nam".

## Punctuation

- No space before `, . : ; ? !`, one space after.
- Prose quotes use “ ” (and ‘ ’ inside). UI strings may use straight quotes when the codebase already does.
- Dialogue in fiction opens with a dash at the start of the line.
- Ellipsis is "..." with no space before.

## Numbers

| Kind | Form | Example |
| --- | --- | --- |
| Thousands, decimals | dot groups, comma decimal | 1.250.000; 3,5 |
| Percent | no space | 3,5% |
| Money | one currency form per surface | 250.000 đ, 250.000đ, 250.000 ₫, 250.000 VND |
| Large money in prose | words for the unit | 1,2 tỷ đồng; 350 triệu đồng |
| Units | space before the unit | 5 km, 20 kg, 30 m² |

VND has no minor unit: never write "250.000,00 đ". "250k" is chat register only.

## Dates and times

| Kind | Form | Example |
| --- | --- | --- |
| Short date | day/month/year | 2/11/2026 or 02/11/2026, one per project |
| Long date | words, no comma | ngày 2 tháng 11 năm 2026 |
| Official documents | leading 0 on days 1-9 and months 1-2 | ngày 02 tháng 01 năm 2026 |
| With weekday | weekday, then date | Thứ Hai, 2/11/2026 |
| Time | 24-hour, or spoken form | 14:30; 14h30; 14 giờ 30; 2 giờ chiều |
| Month name | "tháng" + number | tháng 11 (never "tháng Mười Một" in UI) |

Never month/day order. `Intl.DateTimeFormat("vi-VN", { dateStyle: "long" })` prints "2 tháng 11, 2026" with an English-style comma; build the long form by hand.
