#!/usr/bin/env python3
"""Open pre-filled submission URLs in the default browser.

Usage:
  open_tabs.py <slug>                   # open all pending/scheduled
  open_tabs.py <slug> --only show-hn,reddit-sideproject
  open_tabs.py <slug> --dry-run         # just print what it would open
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

# Reuse prefill_urls.py's URL builder
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prefill_urls import load_state, build_url  # type: ignore


def open_url(url: str) -> None:
    sysname = platform.system()
    if sysname == "Darwin":
        subprocess.run(["open", url], check=False)
    elif sysname == "Linux":
        subprocess.run(["xdg-open", url], check=False)
    elif sysname == "Windows":
        subprocess.run(["cmd", "/c", "start", "", url], check=False, shell=False)
    else:
        print(f"warning: don't know how to open URLs on {sysname}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--only", help="comma-separated channel ids")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delay", type=float, default=0.5, help="seconds between tabs")
    parser.add_argument("--include-done", action="store_true")
    args = parser.parse_args()

    state = load_state(args.slug)

    wanted_ids = set(args.only.split(",")) if args.only else None

    to_open = []
    for ch in state["channels"]:
        if wanted_ids and ch["id"] not in wanted_ids:
            continue
        if not wanted_ids and not args.include_done and ch["status"] == "done":
            continue
        if not wanted_ids and ch["status"] == "skip":
            continue
        url = build_url(ch["id"], state)
        if not url:
            continue
        to_open.append((ch["id"], ch["platform"], url))

    if args.dry_run:
        print(json.dumps([{"id": i, "platform": p, "url": u} for i, p, u in to_open], indent=2))
        return

    for cid, platform_name, url in to_open:
        print(f"opening: {platform_name}")
        open_url(url)
        time.sleep(args.delay)

    print(f"\ndone — opened {len(to_open)} tabs. review each, submit what you approve of.")


if __name__ == "__main__":
    main()
