#!/usr/bin/env python3
"""news-image-20261117 entry: copy the pre-drawn front page to /output/entry.png.

The image (assets/entry.png) was drawn programmatically by tools/make_image.py
with Pillow; this program only copies it, so two runs write identical bytes.
Standard library only; no network.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    # fail loudly if the copy came out wrong instead of shipping a bad file
    if os.path.getsize(dst) != os.path.getsize(SRC):
        raise SystemExit("entry.png copy size mismatch")


if __name__ == "__main__":
    main()
