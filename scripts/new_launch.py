#!/usr/bin/env python3
"""Scaffold a new product launch.

Creates ~/.claude/launches/<slug>/launch.json with initial state + copy/ dir
with drafted per-channel copy pulled from templates/.

Usage:
  new_launch.py <slug> [--json-input path-or-dash]

Interactive by default. If --json-input is provided, reads a JSON object with
the initial values (useful for agent invocation without typing prompts).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
LAUNCHES_DIR = Path.home() / ".claude" / "launches"

# Channel defaults per product type. Order = execution order.
DEFAULT_CHANNELS = {
    "oss": [
        ("readme", "GitHub README polish"),
        ("og-image", "Social preview image"),
        ("show-hn", "Show HN"),
        ("x-thread", "X / Twitter thread"),
        ("reddit-sideproject", "r/SideProject"),
        ("reddit-opensource", "r/opensource"),
        ("dev-to", "Dev.to article"),
        ("awesome-list", "Awesome-* list submission"),
    ],
    "saas": [
        ("landing-page", "Landing page polish"),
        ("og-image", "Social preview image"),
        ("product-hunt", "Product Hunt launch"),
        ("email-announcement", "Email to existing list"),
        ("newsletter", "Newsletter broadcast"),
        ("x-thread", "X / Twitter thread"),
        ("reddit-sideproject", "r/SideProject"),
        ("reddit-saas", "r/SaaS"),
        ("linkedin", "LinkedIn founder post"),
        ("betalist", "BetaList"),
        ("uneed", "Uneed"),
        ("fazier", "Fazier"),
        ("peerlist", "Peerlist Spotlight"),
    ],
    "ml": [
        ("huggingface", "HuggingFace model card + Space"),
        ("og-image", "Social preview image"),
        ("x-thread", "X / Twitter thread"),
        ("reddit-localllama", "r/LocalLLaMA"),
        ("reddit-ml", "r/MachineLearning"),
        ("papers-with-code", "Papers With Code"),
        ("show-hn", "Show HN (optional)"),
    ],
    "claude-plugin": [
        ("plugin-manifest", "Plugin manifest check (.claude-plugin/plugin.json)"),
        ("readme", "GitHub README polish"),
        ("og-image", "Social preview image"),
        ("anthropic-marketplace", "Anthropic official marketplace"),
        ("awesome-claude-code", "awesome-claude-code submission"),
        ("show-hn", "Show HN"),
        ("x-thread", "X / Twitter thread"),
        ("reddit-claudeai", "r/ClaudeAI"),
        ("claudemarketplaces", "claudemarketplaces.com"),
    ],
    "cli": [
        ("registry", "Publish to registry (brew/cargo/npm/pypi)"),
        ("readme", "GitHub README polish"),
        ("og-image", "Social preview image (optional)"),
        ("show-hn", "Show HN"),
        ("terminal-trove", "Terminal Trove"),
        ("x-thread", "X / Twitter thread"),
        ("reddit-commandline", "r/commandline"),
        ("reddit-coolgithub", "r/coolgithubprojects"),
        ("dev-to", "Dev.to article"),
    ],
    "mobile": [
        ("app-store-metadata", "App Store Connect / Play Console metadata"),
        ("testflight-public", "TestFlight public link / Play internal"),
        ("departures-to", "departures.to (TestFlight beta discovery)"),
        ("product-hunt", "Product Hunt Apps category"),
        ("x-thread", "X / Twitter thread"),
        ("reddit-iosapps", "r/iosapps or r/androidapps"),
        ("linkedin", "LinkedIn founder post"),
    ],
    "newsletter": [
        ("welcome-sequence", "Welcome sequence live"),
        ("beehiiv-recommendations", "beehiiv Recommendations cross-promo"),
        ("substack-notes", "Substack Notes"),
        ("x-thread", "X / Twitter thread"),
        ("reddit-substackreads", "r/SubstackReads"),
        ("dev-to-crosspost", "Dev.to cross-post of best issue"),
        ("linkedin", "LinkedIn founder post"),
    ],
}

# Mapping: channel_id -> template filename (inside templates/). Missing = no template copy.
CHANNEL_TEMPLATES = {
    "show-hn": "show-hn.md",
    "product-hunt": "product-hunt.md",
    "reddit-sideproject": "reddit-sideproject.md",
    "reddit-saas": "reddit-saas.md",
    "reddit-claudeai": "reddit-claudeai.md",
    "reddit-localllama": "reddit-localllama.md",
    "reddit-ml": "reddit-ml.md",
    "reddit-opensource": "reddit-opensource.md",
    "reddit-commandline": "reddit-commandline.md",
    "reddit-selfhosted": "reddit-selfhosted.md",
    "reddit-coolgithub": "reddit-coolgithub.md",
    "reddit-iosapps": "reddit-iosapps.md",
    "reddit-substackreads": "reddit-substackreads.md",
    "x-thread": "x-thread.md",
    "readme": "readme-hero.md",
    "email-announcement": "email-announcement.md",
    "newsletter": "email-announcement.md",
    "awesome-list": "awesome-list-issue.md",
    "awesome-claude-code": "awesome-list-issue.md",
    "linkedin": "linkedin.md",
    "dev-to": "dev-to.md",
    "dev-to-crosspost": "dev-to.md",
}


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "launch"


def prompt(msg: str, default: str | None = None) -> str:
    label = f"{msg}"
    if default:
        label += f" [{default}]"
    label += ": "
    val = input(label).strip()
    return val or (default or "")


def render_template(text: str, vars: dict) -> str:
    """Simple {{var}} replacement. Missing vars left as {{var}} for user to fill."""
    def replace(match):
        key = match.group(1).strip()
        return str(vars.get(key, match.group(0)))
    return re.sub(r"\{\{\s*([\w\.]+)\s*\}\}", replace, text)


def flatten_vars(state: dict) -> dict:
    """Flatten nested state into dotted keys for template rendering."""
    out = {}
    for k, v in state.items():
        if isinstance(v, dict):
            for sk, sv in v.items():
                out[f"{k}.{sk}"] = sv
            out[k] = v
        else:
            out[k] = v
    return out


def build_channels(product_type: str, launch_date: str | None) -> list:
    channels = []
    for cid, platform in DEFAULT_CHANNELS.get(product_type, DEFAULT_CHANNELS["oss"]):
        channels.append({
            "id": cid,
            "platform": platform,
            "status": "pending",
            "scheduled_for": None,
            "submission_url": None,
            "posted_url": None,
            "posted_at": None,
            "notes": [],
        })
    return channels


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new product launch")
    parser.add_argument("slug", nargs="?", help="Launch slug (kebab-case)")
    parser.add_argument("--json-input", help="Read values from JSON (path or - for stdin)")
    parser.add_argument("--force", action="store_true", help="Overwrite if exists")
    args = parser.parse_args()

    # Load JSON input if provided
    initial = {}
    if args.json_input:
        if args.json_input == "-":
            initial = json.load(sys.stdin)
        else:
            with open(args.json_input) as f:
                initial = json.load(f)

    slug = args.slug or initial.get("slug")
    if not slug:
        slug = prompt("slug (kebab-case)")
    slug = slugify(slug)

    launch_dir = LAUNCHES_DIR / slug
    if launch_dir.exists() and not args.force:
        print(f"error: {launch_dir} already exists. Pass --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    # Collect fields — prompt for anything missing
    def get(key, label, default=None):
        val = initial.get(key)
        if val is None and sys.stdin.isatty():
            val = prompt(label, default)
        return val or default or ""

    name = get("name", "product name", slug.replace("-", " ").title())
    product_type = get("type", "type (oss/saas/ml/claude-plugin/cli/mobile/newsletter)", "oss")
    tagline = get("tagline", "one-line tagline (<60 chars)")
    url = get("url", "product URL")
    launch_date = get("launch_date", "launch date (YYYY-MM-DD)", "")
    why_story = get("why_story", "why you built it (1-3 sentences, optional)", "")

    author_name = get("author_name", "your name")
    author_github = get("author_github", "GitHub username")
    author_x = get("author_x", "X handle (without @, optional)", "")
    author_email = get("author_email", "contact email (optional)", "")

    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    # Derive repo from github URL if possible
    repo = ""
    m = re.match(r"https?://github\.com/([\w\-]+/[\w\-]+)/?", url)
    if m:
        repo = m.group(1)

    state = {
        "slug": slug,
        "name": name,
        "type": product_type,
        "tagline": tagline,
        "long_tagline": initial.get("long_tagline", ""),
        "url": url,
        "repo": repo,
        "why_story": why_story,
        "author": {
            "name": author_name,
            "github": author_github,
            "x_handle": author_x,
            "email": author_email,
        },
        "assets": {
            "og_image": "",
            "demo_url": "",
            "demo_video": "",
            "logo": "",
        },
        "launch_date": launch_date,
        "channels": build_channels(product_type, launch_date),
        "notes": [],
        "created_at": now,
        "updated_at": now,
    }

    # Write state
    launch_dir.mkdir(parents=True, exist_ok=True)
    copy_dir = launch_dir / "copy"
    assets_dir = launch_dir / "assets"
    copy_dir.mkdir(exist_ok=True)
    assets_dir.mkdir(exist_ok=True)

    state_path = launch_dir / "launch.json"
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    # Copy templates → copy/, render {{variables}}
    vars = flatten_vars(state)
    vars["tagline"] = tagline
    vars["name"] = name
    vars["url"] = url
    vars["why_story"] = why_story or "[fill in the why story — see references/content.md]"
    vars["author.name"] = author_name
    vars["author.github"] = author_github
    vars["author.x_handle"] = author_x
    vars["repo"] = repo

    channels_with_templates = []
    for ch in state["channels"]:
        tpl = CHANNEL_TEMPLATES.get(ch["id"])
        if not tpl:
            continue
        tpl_path = TEMPLATES_DIR / tpl
        if not tpl_path.exists():
            continue
        out_name = f"{ch['id']}.md"
        with open(tpl_path) as f:
            rendered = render_template(f.read(), vars)
        with open(copy_dir / out_name, "w") as f:
            f.write(rendered)
        channels_with_templates.append(ch["id"])

    print(json.dumps({
        "status": "ok",
        "launch_dir": str(launch_dir),
        "state_path": str(state_path),
        "copy_dir": str(copy_dir),
        "assets_dir": str(assets_dir),
        "slug": slug,
        "type": product_type,
        "channels": [c["id"] for c in state["channels"]],
        "drafted_copy": channels_with_templates,
        "next_actions": [
            f"Review drafted copy in {copy_dir}/ — edit until it doesn't sound like AI",
            "Generate OG image (delegate to canvas-design or chatgpt-image skill)",
            f"Run status.py {slug} to see next 1-3 actions",
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
