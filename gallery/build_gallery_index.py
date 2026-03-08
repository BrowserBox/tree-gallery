#!/usr/bin/env python3
import base64
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKAGES = ROOT / "collection-scripts"
OUT_PRIMARY = ROOT / "gallery-scripts.json"
OUT_COMPAT = ROOT / "gallery-index.json"
RAW_BASE = "https://raw.githubusercontent.com/BrowserBox/tree-gallery/main/gallery/collection-scripts"


def parse_script_meta(text: str) -> dict:
    def grab(name: str) -> str:
        m = re.search(rf"{name}\s*:\s*\"([^\"]+)\"", text)
        return m.group(1).strip() if m else ""

    return {"id": grab("id"), "version": grab("version"), "title": grab("title")}


def parse_metadata_md(text: str) -> tuple[str, str]:
    lines = [ln.rstrip() for ln in text.splitlines()]
    title = ""
    for ln in lines:
        if ln.startswith("# "):
            title = ln[2:].strip()
            break
    description = ""
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#") or s.startswith("-"):
            continue
        description = s
        break
    return title, description


def main() -> None:
    records = []
    for author_dir in sorted(PACKAGES.iterdir()):
        if not author_dir.is_dir():
            continue
        author = author_dir.name
        for pkg_dir in sorted(author_dir.iterdir()):
            if not pkg_dir.is_dir():
                continue

            script_name = pkg_dir.name
            script_path = pkg_dir / "tree-script.mjs"
            md_path = pkg_dir / "metadata.md"
            thumb_path = pkg_dir / "thumbnail.png"
            if not (script_path.exists() and md_path.exists()):
                continue

            script_src = script_path.read_text(encoding="utf-8")
            script_meta = parse_script_meta(script_src)
            md_title, md_description = parse_metadata_md(md_path.read_text(encoding="utf-8"))

            title = script_meta["title"] or md_title or script_name
            description = md_description or title
            byline = description if len(description) <= 90 else description[:89] + "…"
            rid = script_meta["id"]
            if script_meta["version"]:
                rid = f"{rid}@{script_meta['version']}"

            root_url = f"{RAW_BASE}/{author}/{script_name}"
            script_url = f"{root_url}/tree-script.mjs"
            thumbnail_url = f"{root_url}/thumbnail.png" if thumb_path.exists() else ""
            thumb_64 = ""
            if thumb_path.exists():
                thumb_64 = base64.b64encode(thumb_path.read_bytes()).decode("ascii")

            records.append(
                {
                    "id": rid,
                    "title": title,
                    "byline": byline,
                    "description": description,
                    "author": author,
                    "usage_count": 0,
                    "root_url": root_url,
                    "script_url": script_url,
                    "thumbnail_url": thumbnail_url,
                    "thumb_64": thumb_64,
                }
            )

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scripts": records,
    }

    OUT_PRIMARY.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    OUT_COMPAT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PRIMARY}")
    print(f"wrote {OUT_COMPAT}")


if __name__ == "__main__":
    main()
