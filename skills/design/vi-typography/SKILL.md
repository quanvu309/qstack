---
name: vi-typography
description: Set Vietnamese type that renders whole: font coverage, diacritic clipping, line height, line breaks. Use when choosing or loading fonts for a Vietnamese (tiếng Việt) interface, styling Vietnamese text, or when dấu look clipped, misplaced, or in a different font.
---

# Vietnamese typography

Vietnamese stacks up to two marks on one letter (ấ, ẫ, Ữ) and hangs one below the baseline (ạ, ộ). Layouts tuned on English text break in three ways: a fallback font draws some letters (**mixed glyphs**), the line box cuts off marks (**clipping**), or a line breaks inside a word. Check each in order.

## 1. Font coverage

A font that has "á" can still lack "ơ, ư, ạ, ẫ". The browser then draws only those letters in a fallback font, and the word looks pasted together from two typefaces.

- Google Fonts: filter the catalog by Language → Vietnamese. The `css2` API already serves a `vietnamese` block for families that have one. `next/font` preloads only the subsets you list, so add `subsets: ["latin", "vietnamese"]` or Vietnamese letters swap in late from a fallback. `@fontsource`: import the full weight file, or the `vietnamese` subset file next to `latin`.
- Self-hosted or commercial font: run `uv run --with fonttools scripts/check-font.py <font-files>` from this skill's folder. It lists every missing Vietnamese letter, tone mark, ₫ and curly quote, and exits 1, so it can gate CI.
- Subsetting tools (glyphhanger, fonttools `pyftsubset`) drop Vietnamese unless you pass its ranges: `U+0000-00FF, U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+2000-206F, U+20AB`. The U+2000-206F block carries “ ” ‘ ’ … and dashes.
- Coverage is not quality. Render the test block below at body and display size and look at: the tone mark beside or above the circumflex (ấ ầ ẩ ẫ ậ) without touching it, the horn of ơ ư joined to the letter, and the đ crossbar clear of the bowl.

```
Ở Huế, mưa dầm suốt tháng Mười; người ta vẫn ngồi quán cà phê bên sông Hương.
ẤẦẨẪẬ ẮẰẲẴẶ ẾỀỂỄỆ ỐỒỔỖỘ ỚỜỞỠỢ ỨỪỬỮỰ ỲỶỸỴ Đđ
Ơ Ư Ĩĩ Ũũ ẢẠÃ ẺẸẼ ỈỊ ỎỌ ỦỤ ạ ẹ ị ọ ụ ₫ “ ” …
ấầẩẫậ ắằẳẵặ ếềểễệ ốồổỗộ ớờởỡợ ứừửữự ỳỷỹỵ ơư
```

## 2. Clipping

Stacked marks on capitals rise above the font's cap height, and dấu nặng drops below the baseline.

- Body text: `line-height` 1.5 or more. Headings: 1.2 or more; at 1.0 the marks on "Ữ" collide with the line above, and any box that clips (next bullet) cuts them off.
- Any `overflow: hidden` on text (single-line ellipsis, `line-clamp`, fixed-height buttons, chips, table cells) clips marks unless the box has vertical room. Give it `padding-block` or a taller line-height, then check the test block inside it.
- `background-clip: text` gradients and masks clip the same way. Extend the painted box with padding.
- Underlines cross dấu nặng: set `text-underline-offset: 0.2em` or more and keep `text-decoration-skip-ink: auto`.
- All caps stacks every mark on top. Keep long labels in sentence case; reserve `text-transform: uppercase` for one or two words.

## 3. Line breaks and length

Vietnamese words are syllables separated by spaces, so the browser may break "Hà / Nội" or "250.000 / đ" across lines.

- Keep numbers with units, money, and short names in headings on one line: wrap them in a `white-space: nowrap` span, or put a no-break space (U+00A0) between the parts. Code that searches or slugs that text must treat U+00A0 as a space.
- `text-wrap: balance` on headings, `text-wrap: pretty` on body. Do not rely on `hyphens: auto`; browsers ship no Vietnamese hyphenation, and Vietnamese does not hyphenate syllables.
- Set `lang="vi"` on the root element so screen readers pick a Vietnamese voice, spellcheck uses Vietnamese, and the browser does not offer to translate the page.
- Vietnamese UI strings usually run longer than their English source ("Add to cart" → "Thêm vào giỏ hàng"). Size buttons, tabs and table headers on the longest real Vietnamese string, never on English or lorem ipsum.

## Done when

The font check passes for every face in use (each weight and style is a separate file), the test block renders uncut inside every component that sets `overflow`, line height, or a fixed height, and no Vietnamese text shows a letter from a fallback font.
