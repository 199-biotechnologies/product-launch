#!/usr/bin/env python3
"""Generate pre-filled submission URLs for every pending/scheduled channel.

Pulls drafted copy from launches/<slug>/copy/<channel>.md and URL-encodes
everything into the platform's submit link (where a URL-prefill exists).

Usage:
  prefill_urls.py <slug>                # markdown table
  prefill_urls.py <slug> --json         # JSON { channel_id: url }
  prefill_urls.py <slug> --only show-hn,reddit-sideproject
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, urlencode

LAUNCHES_DIR = Path.home() / ".claude" / "launches"


def load_state(slug: str) -> dict:
    path = LAUNCHES_DIR / slug / "launch.json"
    if not path.exists():
        print(f"error: no launch found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def read_copy(slug: str, channel_id: str) -> str:
    p = LAUNCHES_DIR / slug / "copy" / f"{channel_id}.md"
    if not p.exists():
        return ""
    return p.read_text()


def strip_html_comments(text: str) -> str:
    """Remove <!-- ... --> blocks (including multi-line)."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def extract_section(text: str, heading: str) -> str:
    """Pull text under a `## heading` block until the next ## or end.
    Strips HTML comments from the result."""
    pat = re.compile(rf"^##\s*{re.escape(heading)}\s*$", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return ""
    start = m.end()
    next_h = re.search(r"^##\s", text[start:], re.MULTILINE)
    end = start + next_h.start() if next_h else len(text)
    section = strip_html_comments(text[start:end])
    # Collapse 3+ blank lines to 2
    section = re.sub(r"\n{3,}", "\n\n", section)
    return section.strip()


def first_line(text: str) -> str:
    """First non-blank, non-heading, non-comment line."""
    text = strip_html_comments(text)
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return ""


def build_url(channel_id: str, state: dict) -> str | None:
    url = state.get("url", "")
    slug = state["slug"]
    copy = read_copy(slug, channel_id)

    if channel_id == "show-hn":
        title_section = extract_section(copy, "Title")
        title = first_line(title_section) if title_section else ""
        if not title:
            title = f"Show HN: {state.get('name','')} – {state.get('tagline','')}"
        title = title.replace('"', "").strip()
        if not title.startswith("Show HN:"):
            title = f"Show HN: {state.get('name','')} – {state.get('tagline','')}"
        return f"https://news.ycombinator.com/submitlink?u={quote(url)}&t={quote(title[:80])}"

    if channel_id.startswith("reddit-"):
        sub_map = {
            "reddit-sideproject": "SideProject",
            "reddit-saas": "SaaS",
            "reddit-claudeai": "ClaudeAI",
            "reddit-localllama": "LocalLLaMA",
            "reddit-ml": "MachineLearning",
            "reddit-opensource": "opensource",
            "reddit-selfhosted": "selfhosted",
            "reddit-commandline": "commandline",
            "reddit-coolgithub": "coolgithubprojects",
            "reddit-iosapps": "iosapps",
            "reddit-androidapps": "androidapps",
            "reddit-substackreads": "SubstackReads",
            "reddit-microsaas": "microsaas",
        }
        sub = sub_map.get(channel_id)
        if not sub:
            return None
        title_section = extract_section(copy, "Title")
        title = first_line(title_section) if title_section else first_line(copy)
        if not title:
            title = f"{state.get('name','')} — {state.get('tagline','')}"
        body = extract_section(copy, "Body")
        if body:
            # Use text post (selftext) - Reddit accepts text param in submit URL
            return f"https://www.reddit.com/r/{sub}/submit?" + urlencode({
                "title": title[:300],
                "text": body[:10000],
                "selftext": "true",
            })
        else:
            return f"https://www.reddit.com/r/{sub}/submit?" + urlencode({
                "title": title[:300],
                "url": url,
            })

    if channel_id == "linkedin":
        text = extract_section(copy, "Post") or copy.strip()
        return f"https://www.linkedin.com/feed/?" + urlencode({
            "shareActive": "true",
            "shareUrl": url,
            "text": text[:3000],
        })

    if channel_id == "awesome-claude-code":
        # Pre-fill issue template
        title = f"[Resource]: {state.get('name','')} — {state.get('tagline','')}"
        body_file = LAUNCHES_DIR / slug / "copy" / "awesome-claude-code.md"
        body = body_file.read_text() if body_file.exists() else read_copy(slug, "awesome-list")
        return "https://github.com/hesreallyhim/awesome-claude-code/issues/new?" + urlencode({
            "template": "recommend-resource.yml",
            "title": title[:200],
            "resource-name": state.get("name", ""),
            "resource-url": url,
            "description": state.get("tagline", ""),
        })

    if channel_id == "dev-to" or channel_id == "dev-to-crosspost":
        body = copy
        return f"https://dev.to/new?" + urlencode({"prefill": body[:20000]})

    if channel_id == "email-announcement":
        subject = extract_section(copy, "Subject") or f"{state.get('name','')} is live"
        body = extract_section(copy, "Body") or copy.strip()
        return f"mailto:?" + urlencode({"subject": subject, "body": body})

    if channel_id == "product-hunt":
        # No URL prefill; multi-step form
        return "https://www.producthunt.com/posts/new"

    if channel_id == "anthropic-marketplace":
        return "https://platform.claude.com/plugins/submit"

    if channel_id == "huggingface":
        return "https://huggingface.co/new"

    if channel_id == "terminal-trove":
        return "https://terminaltrove.com/submit"

    if channel_id == "betalist":
        return "https://betalist.com/submit"

    if channel_id == "uneed":
        return "https://www.uneed.best/submit"

    if channel_id == "fazier":
        return "https://fazier.com/submit"

    if channel_id == "peerlist":
        return "https://peerlist.io/scroll"

    if channel_id == "departures-to":
        return "https://departures.to/submit"

    if channel_id == "claudemarketplaces":
        return "https://github.com/claudemarketplaces/claudemarketplaces/issues/new"

    # X / Twitter has NO URL-based prefill for authenticated posting — delegate to xmaster skill.
    if channel_id == "x-thread":
        return None

    # README / assets / registry / landing-page / etc. are local actions
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--only", help="comma-separated channel ids (default: pending + scheduled)")
    parser.add_argument("--include-done", action="store_true", help="include done channels")
    args = parser.parse_args()

    state = load_state(args.slug)

    wanted_ids = None
    if args.only:
        wanted_ids = set(args.only.split(","))

    results = []
    for ch in state["channels"]:
        if wanted_ids and ch["id"] not in wanted_ids:
            continue
        if not wanted_ids and not args.include_done and ch["status"] == "done":
            continue
        if not wanted_ids and ch["status"] == "skip":
            continue
        url = build_url(ch["id"], state)
        results.append({
            "id": ch["id"],
            "platform": ch["platform"],
            "status": ch["status"],
            "submission_url": url,
            "manual_only": url is None,
        })

    if args.json:
        print(json.dumps(results, indent=2))
        return

    # Markdown table
    print(f"# Pre-filled submission URLs — {state.get('name', args.slug)}\n")
    print("| Channel | Status | Link |")
    print("|---------|--------|------|")
    for r in results:
        link = r["submission_url"] or "_(manual — see notes)_"
        if r["submission_url"]:
            link = f"[{r['platform']}]({r['submission_url']})"
        print(f"| {r['platform']} | {r['status']} | {link} |")

    print("\n**Manual-only channels** (delegate or open in app):")
    for r in results:
        if r["manual_only"]:
            hint = ""
            if r["id"] == "x-thread":
                hint = " — use xmaster skill: `xmaster analyze` → approval → `xmaster post`"
            elif r["id"].startswith("readme") or r["id"] == "og-image":
                hint = " — local action in the repo"
            print(f"- {r['platform']}{hint}")


if __name__ == "__main__":
    main()
