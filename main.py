#!/usr/bin/env python3
"""Deliver the 24 November 2026 front page to the grading sandbox.

The page itself is the committed entry.png (a 1024x1024 newspaper front
page built from four AI illustrations and verified 24 November 2026
reporting). This program only places that file where the harness
expects it, after confirming it is really a PNG of the right size.
"""
import hashlib
import os
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
TARGET_DIR = Path("/output")
TARGET = TARGET_DIR / "entry.png"
# The sandbox runs with no network, so the image ships in the repo.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def place_image():
    raw = SOURCE.read_bytes()
    if not raw.startswith(PNG_MAGIC):
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    if len(raw) > MAX_BYTES:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(raw)
    placed = TARGET.read_bytes()
    if hashlib.sha256(placed).hexdigest() != hashlib.sha256(raw).hexdigest():
        print("copy mismatch: /output/entry.png differs", file=sys.stderr)
        return 1
    print("wrote /output/entry.png (%d bytes, sha256 %s)"
          % (len(placed), hashlib.sha256(placed).hexdigest()))
    return 0


if __name__ == "__main__":
    raise SystemExit(place_image())
