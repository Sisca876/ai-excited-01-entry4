"""Copy the bundled entry image to the output directory, byte for byte."""

import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
SOURCE = HERE / "entry.png"


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not SOURCE.is_file():
        print(f"missing bundled image: {SOURCE}", file=sys.stderr)
        raise SystemExit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "entry.png"
    shutil.copyfile(SOURCE, target)
    if sha256(SOURCE) != sha256(target):
        print("output bytes differ from bundled image", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
