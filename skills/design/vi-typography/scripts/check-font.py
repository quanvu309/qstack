#!/usr/bin/env python3
"""Report which characters Vietnamese text needs that a font file is missing.

Usage: uv run --with fonttools check-font.py FONT [FONT ...]
       (or: pip install fonttools && python3 check-font.py FONT ...)

Exits 1 when any font misses a character, so it works as a CI gate.
"""

import sys

from fontTools.ttLib import TTCollection, TTFont

LOWER = (
    "aàảãáạăằẳẵắặâầẩẫấậbcdđeèẻẽéẹêềểễếệghiìỉĩíịklmn"
    "oòỏõóọôồổỗốộơờởỡớợpqrstuùủũúụưừửữứựvxyỳỷỹýỵ"
)
# Decomposed (NFD) text still reaches the page, so the combining tone marks count too.
COMBINING = "\u0300\u0301\u0303\u0309\u0323"
# Vietnamese prose also needs the đồng sign, curly quotes and the ellipsis.
SYMBOLS = "\u20ab\u201c\u201d\u2018\u2019\u2026"
REQUIRED = sorted(set(LOWER + LOWER.upper() + COMBINING + SYMBOLS))


def faces(path):
    if path.lower().endswith((".ttc", ".otc")):
        return list(TTCollection(path).fonts)
    return [TTFont(path, lazy=True)]


def main(paths):
    if not paths:
        print(__doc__.strip())
        return 2
    failed = False
    for path in paths:
        for index, font in enumerate(faces(path)):
            label = path if index == 0 else f"{path}#{index}"
            cmap = font.getBestCmap() or {}
            missing = [c for c in REQUIRED if ord(c) not in cmap]
            if missing:
                failed = True
                shown = " ".join(f"U+{ord(c):04X}" if c in COMBINING + SYMBOLS else c for c in missing)
                print(f"FAIL {label}: missing {len(missing)}/{len(REQUIRED)}: {shown}")
            else:
                print(f"OK   {label}: all {len(REQUIRED)} required characters present")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
