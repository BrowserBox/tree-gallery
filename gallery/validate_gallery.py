#!/usr/bin/env python3
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
BUILT_INDEX = ROOT / "gallery-scripts.json"
PACKAGES_ROOT = ROOT / "collection-scripts"
MAX_BYTES = 12 * 1024
MAX_NONEMPTY_LINES = 300

REQUIRED_FIELDS = {
    "id",
    "title",
    "byline",
    "description",
    "author",
    "usage_count",
    "root_url",
    "script_url",
    "thumbnail_url",
    "thumb_64",
}


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)


def main() -> None:
    if not BUILT_INDEX.exists():
        fail("gallery-scripts.json not found")
    data = json.loads(BUILT_INDEX.read_text())
    if "scripts" not in data or not isinstance(data["scripts"], list):
        fail("gallery-scripts.json must include scripts[]")

    ids = set()
    for i, item in enumerate(data["scripts"]):
        missing = REQUIRED_FIELDS - set(item.keys())
        if missing:
            fail(f"scripts[{i}] missing fields: {sorted(missing)}")
        sid = item["id"]
        if sid in ids:
            fail(f"duplicate script id: {sid}")
        ids.add(sid)

    if not PACKAGES_ROOT.exists():
        fail("gallery/collection-scripts directory not found")

    for author_dir in PACKAGES_ROOT.iterdir():
        if not author_dir.is_dir():
            continue
        for pkg_dir in author_dir.iterdir():
            if not pkg_dir.is_dir():
                continue
            script = pkg_dir / "tree-script.mjs"
            meta = pkg_dir / "metadata.md"
            if not script.exists():
                fail(f"{pkg_dir} missing tree-script.mjs")
            if not meta.exists():
                fail(f"{pkg_dir} missing metadata.md")

            raw = script.read_bytes()
            if len(raw) > MAX_BYTES:
                fail(f"{script.name} exceeds {MAX_BYTES} bytes")
            text = raw.decode("utf-8")
            non_empty = [ln for ln in text.splitlines() if ln.strip()]
            if len(non_empty) > MAX_NONEMPTY_LINES:
                fail(f"{script.name} exceeds {MAX_NONEMPTY_LINES} non-empty lines")
            if "import " in text:
                fail(f"{script.name} uses import (not allowed)")

    print("gallery validation passed")


if __name__ == "__main__":
    main()
