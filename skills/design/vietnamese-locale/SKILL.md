---
name: vietnamese-locale
description: Build forms, validation, search, sorting and formatting that fit Vietnamese users (vi-VN): names, addresses, phone numbers, money, dates, diacritics. Use when designing or coding any of these for Vietnam, or when Vietnamese text fails to match, sort, or slug.
---

# Vietnamese locale

Product code built on English defaults mishandles Vietnamese data in predictable places. Work through each section that the feature touches; every rule names the default that breaks and the replacement.

## Diacritics in data

- **Store NFC.** Call `s.normalize("NFC")` at every input boundary (form submit, import, file names, API payloads). macOS file names and text pasted from PDFs arrive as NFD, where "hòa" is 4 code points instead of 3 and `===` fails.
- **Fold for search and slugs**, never for storage. Stripping combining marks leaves "đ" intact, because "đ" is its own letter, not "d" plus a mark:

  ```js
  const fold = (s) =>
    s.normalize("NFD").replace(/\p{M}/gu, "").replace(/đ/g, "d").replace(/Đ/g, "D")
      .replace(/\s+/gu, " ").trim().toLowerCase();
  fold("Đường Hà Nội"); // "duong ha noi"
  ```

  Match the folded query against a folded copy of the text, so "ha noi" finds "Hà Nội". Slugs are the folded form with spaces turned to hyphens: "huong-dan-su-dung".
- **Sort with `Intl.Collator("vi")`.** Default sort orders by code point and puts "Âu", "Ăn" and "Đông" after "Zô"; the collator gives a, ă, â, b, c, d, đ, e, ê...
- **Typing input.** Vietnamese is typed in Telex or VNI, and the input method rewrites letters as the user types. Two kinds exist. The macOS built-in input and most mobile keyboards use composition events: skip any value rewrite while `event.isComposing` is true and apply it on `compositionend`. Unikey, EVKey and OpenKey, the usual Windows setup, send Backspace plus the new letter with no composition events. For them, never treat a Backspace keydown as the user deleting, preserve `selectionStart` whenever you rewrite the value, and keep inline autocomplete selections away from the word being typed. Code that reformats the value on every `input` event (masks, auto-capitalise, trimming) is the usual cause of lost or doubled letters; apply it on blur instead.

## Names

A Vietnamese name is family, middle, given: "Nguyễn Thị Minh Khai". People are addressed by the given name, the last word.

- One "Họ và tên" field. When a backend needs parts, take the first word as họ and the last as tên, keep the full string verbatim, and let the user edit the tên they are called by. The split is a guess: compound family names (Tôn Nữ, Âu Dương), two-word given names (Bảo Anh) and some ethnic-minority names (H'Hen Niê, family name last) break it.
- Greet with the given name ("Chào Khai", "Chào chị Khai"), never the family name ("Chào Nguyễn").
- Avatar initials come from the given name ("K", or "MK" from the last two words), not from the first word, since a few family names (Nguyễn, Trần, Lê) cover most of the country.
- Validate after NFC with `/^[\p{L}\p{M}' ’-]+$/u`, never `[A-Za-z]`. Names such as "N'Trang Lơng" carry an apostrophe.
- Lists of people (classes, staff) sort by given name, then middle, then family.

## Addresses

Since 1 July 2025 Vietnam has two levels of local government: 34 province-level units (tỉnh, thành phố) and the commune level below them (xã, phường, đặc khu). The district level (quận, huyện) is gone (Nghị quyết 202/2025/QH15 and Luật Tổ chức chính quyền địa phương số 72/2025/QH15; source: https://xaydungchinhsach.chinhphu.vn/chi-tiet-34-don-vi-hanh-chinh-cap-tinh-tu-12-6-2025-119250612141845533.htm, checked 2026-11-02).

- Form order: tỉnh/thành phố (select), then xã/phường (select filtered by the tỉnh), then the street line (số nhà, đường, thôn, ấp). No district field. Display and print in written order: street, xã/phường, tỉnh/thành phố.
- Pull the unit list from a source dated after July 2025. Any list of 63 provinces, or any field named district/huyện, is stale.
- Users and old documents still write pre-2025 addresses with a district. Accept them as free text; do not reject them.

## Phone numbers

- Mobile: 10 digits, 0 then 3, 5, 7, 8 or 9 ("0912 345 678"; international "+84 912 345 678", where +84 replaces the leading 0).
- Landline: 11 digits starting 02 ("024 3825 1234").
- Hotline: 1800 or 1900 plus 4 or 6 digits, with no +84 form.
- When the type is unknown, accept 8 to 11 digits. Shapes checked 2026-11-02 against the 2017 area-code change.
- Accept spaces, dots, hyphens and +84; normalise to one form before storing.
- Validate the shape, not a carrier prefix list; the prefixes change.

## Money and dates

Use `Intl` with `"vi-VN"`, and know where its output differs from what Vietnamese readers write:

| Call | Output |
| --- | --- |
| `NumberFormat("vi-VN").format(1234567.5)` | `1.234.567,5` |
| `NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(1234567)` | `1.234.567 ₫`, with U+00A0 before ₫ |
| `DateTimeFormat("vi-VN").format(d)` | `2/11/2026` |
| `DateTimeFormat("vi-VN", { dateStyle: "full" }).format(d)` | `Thứ Hai, 2 tháng 11, 2026` |

- VND has no minor unit, and the currency formatter rounds silently (1234567.6 prints `1.234.568 ₫`). Store integers. Set `maximumFractionDigits: 0` when formatting money with `style: "decimal"`.
- Parsing input: users type "1.000.000", "1000000", "500k", "1,5tr" or "1tr2". `parseFloat("1.000.000")` returns 1. Strip the dots before parsing. Either support the k / tr / tỷ suffixes with a comma decimal, or reject them with a message; decide which and test it.
- Tests that compare formatted money must include the U+00A0, or compare after replacing it.
- The `long` and `full` date styles add an English-style comma. For prose, build "ngày 2 tháng 11 năm 2026" from the parts.

## Done when

Every field, search box, list and formatted value the feature touches has been checked against its section above, and each is exercised by at least one test using real Vietnamese input with diacritics and "đ".
