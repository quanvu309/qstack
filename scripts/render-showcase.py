#!/usr/bin/env python3
"""Render the README showcase images from the example specs.

Usage: uv run --with python-docx --with pymupdf --with pillow scripts/render-showcase.py [OUT_DIR]

Needs LibreOffice (set SOFFICE to its `soffice` binary when it is not on PATH) and network
access on the first run to fetch the background photo into dist/.
Writes OUT_DIR/<name>.png (default dist/showcase). scripts/release.sh attaches them to each GitHub release.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import urllib.request

import pymupdf
from PIL import Image, ImageEnhance, ImageFilter

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills/writing/vietnamese-official-document"
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else REPO / "dist/showcase"

# image name -> pages shown side by side, each as (example spec, 1-based page)
SHOWCASE = {
    "official-documents": [("quyet-dinh", 1), ("cong-van", 1)],
    "one-pager": [("to-trinh", 1), ("to-trinh", 3)],
}

DPI = 110
PAD_X, PAD_Y, GAP = 240, 130, 110
# "Serene Landscape of Ha Long Bay" by Yagyaansh Khaneja, Pexels License (free, no attribution required).
# https://www.pexels.com/photo/serene-landscape-of-ha-long-bay-vietnam-36164068/
BACKGROUND_URL = "https://images.pexels.com/photos/36164068/pexels-photo-36164068.jpeg?auto=compress&cs=tinysrgb&w=3200"
BACKGROUND_CACHE = REPO / "dist/background-36164068.jpg"


def soffice():
    path = os.environ.get("SOFFICE") or shutil.which("soffice")
    if not path:
        sys.exit("error: LibreOffice not found; set SOFFICE to its soffice binary")
    return path


def to_pdf(example, workdir):
    docx = workdir / f"{example}.docx"
    subprocess.run([sys.executable, str(SKILL / "scripts/build_docx.py"),
                    str(SKILL / "examples" / f"{example}.json"), str(docx)], check=True)
    # A private profile lets this run beside another LibreOffice instance.
    subprocess.run([soffice(), f"-env:UserInstallation=file://{workdir}/profile", "--headless",
                    "--convert-to", "pdf", "--outdir", str(workdir), str(docx)],
                   check=True, capture_output=True)
    return pymupdf.open(workdir / f"{example}.pdf")


def page_image(pdf, number):
    pix = pdf[number - 1].get_pixmap(dpi=DPI)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def background(size):
    if not BACKGROUND_CACHE.exists():
        BACKGROUND_CACHE.parent.mkdir(parents=True, exist_ok=True)
        # The CDN refuses requests without a browser-like User-Agent.
        request = urllib.request.Request(BACKGROUND_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request) as response:
            BACKGROUND_CACHE.write_bytes(response.read())
    photo = Image.open(BACKGROUND_CACHE).convert("RGB")
    scale = max(size[0] / photo.width, size[1] / photo.height)
    photo = photo.resize((round(photo.width * scale), round(photo.height * scale)), Image.LANCZOS)
    left, top = (photo.width - size[0]) // 2, (photo.height - size[1]) // 2
    photo = photo.crop((left, top, left + size[0], top + size[1]))
    # Soften and darken the photo so the white pages carry the attention.
    return ImageEnhance.Brightness(photo.filter(ImageFilter.GaussianBlur(1.5))).enhance(0.9)


def compose(pages):
    w, h = pages[0].size
    size = (PAD_X * 2 + w * len(pages) + GAP * (len(pages) - 1), PAD_Y * 2 + h)
    canvas = background(size)
    shadow = Image.new("L", size, 0)
    for i in range(len(pages)):
        x = PAD_X + i * (w + GAP)
        shadow.paste(150, (x + 4, PAD_Y + 14, x + w + 4, PAD_Y + h + 14))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.composite(Image.new("RGB", size, (0, 0, 0)), canvas, shadow)
    for i, page in enumerate(pages):
        canvas.paste(page, (PAD_X + i * (w + GAP), PAD_Y))
    return canvas


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        pdfs = {}
        for name, pages in SHOWCASE.items():
            for example, _ in pages:
                if example not in pdfs:
                    pdfs[example] = to_pdf(example, workdir)
            image = compose([page_image(pdfs[example], n) for example, n in pages])
            image.save(OUT / f"{name}.png", optimize=True)
            print(f"wrote {OUT / name}.png from {pages}")


if __name__ == "__main__":
    main()
