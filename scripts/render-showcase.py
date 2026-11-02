#!/usr/bin/env python3
"""Render the README showcase images from the example specs.

Usage: uv run --with python-docx --with pymupdf --with pillow scripts/render-showcase.py

Needs LibreOffice. Set SOFFICE to its `soffice` binary when it is not on PATH.
Writes docs/images/<name>.png; rerun after any change to the builder or the examples.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills/writing/vietnamese-official-document"
OUT = REPO / "docs/images"

# image name -> pages shown side by side, each as (example spec, 1-based page)
SHOWCASE = {
    "official-documents": [("quyet-dinh", 1), ("cong-van", 1)],
    "one-pager": [("to-trinh", 1), ("to-trinh", 3)],
}

DPI = 110
PAD, GAP = 40, 32
BACKGROUND, BORDER = (238, 240, 243), (201, 206, 214)


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


def compose(pages):
    w, h = pages[0].size
    canvas = Image.new("RGB", (PAD * 2 + w * len(pages) + GAP * (len(pages) - 1), PAD * 2 + h),
                       BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    for i, page in enumerate(pages):
        x = PAD + i * (w + GAP)
        canvas.paste(page, (x, PAD))
        draw.rectangle([x - 1, PAD - 1, x + w, PAD + h], outline=BORDER)
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
            print(f"wrote docs/images/{name}.png from {pages}")


if __name__ == "__main__":
    main()
