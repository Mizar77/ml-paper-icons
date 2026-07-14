#!/usr/bin/env python3
"""Reproducibly download all icons listed in manifest.json from their upstream CDNs.

Usage:
    python3 scripts/fetch_icons.py            # download everything in the manifest
    python3 scripts/fetch_icons.py --check    # only report missing/extra, do not write

Sources (all permissively licensed, see THIRD_PARTY_LICENSES.md):
    lucide    -> lucide-static (ISC)         https://github.com/lucide-icons/lucide
    tabler    -> @tabler/icons (MIT)         https://github.com/tabler/tabler-icons
    phosphor  -> @phosphor-icons/core (MIT)  https://github.com/phosphor-icons/core
    duotone   -> @phosphor-icons/core (MIT)  (duotone weight)
    brand     -> @lobehub/icons (MIT)        https://github.com/lobehub/lobe-icons
"""
import argparse
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, "icons")
MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manifest.json")

JSDELIVR = "https://cdn.jsdelivr.net/npm"

# Map: (folder, local_filename) -> upstream URL
def build_url_map(manifest):
    urls = {}
    for name in manifest["lucide"]:
        urls[("lucide", name)] = f"{JSDELIVR}/lucide-static@latest/icons/{name}.svg"
    for name in manifest["tabler"]:
        urls[("tabler", name)] = f"{JSDELIVR}/@tabler/icons@latest/icons/outline/{name}.svg"
    for name in manifest["phosphor"]["regular"]:
        urls[("phosphor", f"r-{name}")] = f"{JSDELIVR}/@phosphor-icons/core@latest/assets/regular/{name}.svg"
    for name in manifest["phosphor"]["fill"]:
        urls[("phosphor", f"f-{name}")] = f"{JSDELIVR}/@phosphor-icons/core@latest/assets/fill/{name}-fill.svg"
    for name in manifest["duotone"]:
        urls[("duotone", f"d-{name}")] = f"{JSDELIVR}/@phosphor-icons/core@latest/assets/duotone/{name}-duotone.svg"
    for name in manifest["brand"]:
        urls[("brand", name)] = f"{JSDELIVR}/@lobehub/icons-static-svg@latest/icons/{name}.svg"
    return urls


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "ml-paper-icons/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    if b"<svg" not in data[:200]:
        raise ValueError("not an SVG")
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report only, do not download")
    args = ap.parse_args()

    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    urls = build_url_map(manifest)

    if args.check:
        missing = [(d, n) for (d, n) in urls if not os.path.exists(os.path.join(ICONS, d, n + ".svg"))]
        print(f"manifest entries: {len(urls)}, missing locally: {len(missing)}")
        for d, n in missing:
            print(f"  MISSING {d}/{n}")
        return 0 if not missing else 1

    ok = fail = 0
    failed = []
    for (folder, name), url in sorted(urls.items()):
        dest_dir = os.path.join(ICONS, folder)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, name + ".svg")
        try:
            data = fetch(url)
            with open(dest, "wb") as f:
                f.write(data)
            ok += 1
        except Exception as e:
            fail += 1
            failed.append(f"{folder}/{name} <- {url} ({e})")
    print(f"downloaded OK={ok} FAIL={fail}")
    for line in failed:
        print("  FAIL", line)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
