#!/usr/bin/env python3
"""Structured form schemas for each launch channel.

Consumable by browser automation agents (browser-use, playwright MCP,
Claude computer-use, etc.). The agent reads the schema, fills each field,
verifies pre_submit_checklist, then either submits (if
human_review_required_before_submit=false) or presents to user for approval.

Usage:
  form_schema.py <slug>                    # all channels, JSON array
  form_schema.py <slug> --channel show-hn  # one channel
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prefill_urls import load_state, read_copy, extract_section, first_line, build_url  # type: ignore

LAUNCHES_DIR = Path.home() / ".claude" / "launches"


def asset(state: dict, key: str) -> str:
    return state.get("assets", {}).get(key, "") or ""


def schema_for(channel_id: str, state: dict) -> dict:
    """Return a form schema for the given channel."""
    copy = read_copy(state["slug"], channel_id)
    name = state.get("name", "")
    tagline = state.get("tagline", "")
    url = state.get("url", "")
    why_story = state.get("why_story", "")

    base = {
        "channel_id": channel_id,
        "platform": channel_id,  # overridden below
        "submission_method": "manual",
        "auth_required": False,
        "url": None,
        "fields": [],
        "assets_required": [],
        "pre_submit_checklist": [],
        "post_submit_actions": [],
        "human_review_required_before_submit": True,
        "notes": []
    }

    # ---- URL-prefill channels (preferred) ----
    prefill = build_url(channel_id, state)
    if prefill and channel_id in {"show-hn", "claudemarketplaces"} or channel_id.startswith("reddit-"):
        base.update({
            "submission_method": "url-prefill",
            "url": prefill,
            "auth_required": True,  # HN and Reddit both need login
            "human_review_required_before_submit": True,
            "notes": ["URL-encoded form. Agent should navigate, verify content, click submit."]
        })
        if channel_id == "show-hn":
            title_section = extract_section(copy, "Title")
            title = first_line(title_section) or f"Show HN: {name} – {tagline}"
            base.update({
                "platform": "Show HN",
                "fields": [
                    {"name": "title", "label": "Title", "value": title, "required": True, "max_length": 80,
                     "selector_hints": ["input[name='title']"]},
                    {"name": "url", "label": "URL", "value": url, "required": True,
                     "selector_hints": ["input[name='url']"]}
                ],
                "pre_submit_checklist": [
                    "URL returns 200 (not a waitlist)",
                    "No signup wall on linked site",
                    "Title <60 chars, no marketing verbs",
                    "First comment ready to paste within 2 min of submit",
                    "Calendar cleared for 4h of replies"
                ],
                "post_submit_actions": [
                    {"action": "post_comment", "delay_seconds": 60, "description": "Post the first comment via /submit"}
                ]
            })
        elif channel_id.startswith("reddit-"):
            title_section = extract_section(copy, "Title")
            title = first_line(title_section) or f"{name} — {tagline}"
            body = extract_section(copy, "Body")
            base.update({
                "platform": f"Reddit {channel_id}",
                "fields": [
                    {"name": "title", "label": "Title", "value": title, "required": True, "max_length": 300,
                     "selector_hints": ["input[name='title']", "textarea[name='title']"]},
                    ({"name": "text", "label": "Post body", "value": body, "required": True, "type": "textarea",
                      "selector_hints": ["textarea[name='text']", "div[role='textbox']"]} if body else
                     {"name": "url", "label": "Link URL", "value": url, "required": True,
                      "selector_hints": ["input[name='url']"]})
                ],
                "pre_submit_checklist": [
                    "Account meets sub's minimum karma/age (see references/platforms.md)",
                    "Self-promo quota not exhausted in this sub (10% rule)",
                    "Post copy passes anti-AI-slop ban list",
                    "Tue/Wed/Thu posting day"
                ],
                "post_submit_actions": [
                    {"action": "reply_to_comments", "delay_seconds": 900, "description": "Start replying within 15 min of every comment for first 2h"}
                ]
            })
        return base

    # ---- Product Hunt (no URL-prefill, full form schema) ----
    if channel_id == "product-hunt":
        tagline_section = extract_section(copy, "Tagline") or tagline
        tagline_val = first_line(tagline_section) or tagline
        first_comment = extract_section(copy, "First comment") or ""
        return {
            **base,
            "platform": "Product Hunt",
            "submission_method": "form",
            "auth_required": True,
            "url": "https://www.producthunt.com/posts/new",
            "fields": [
                {"name": "name", "label": "Product name", "value": name, "required": True, "max_length": 40,
                 "selector_hints": ["input[name='name']", "input[placeholder*='name' i]"]},
                {"name": "tagline", "label": "Tagline", "value": tagline_val[:60], "required": True, "max_length": 60,
                 "selector_hints": ["input[name='tagline']", "input[placeholder*='tagline' i]"]},
                {"name": "description", "label": "Description", "value": extract_section(copy, "Description") or tagline_val,
                 "required": True, "type": "markdown",
                 "selector_hints": ["textarea[name='description']"]},
                {"name": "url", "label": "Product URL", "value": url, "required": True,
                 "selector_hints": ["input[name='url']"]},
                {"name": "categories", "label": "Categories", "value": [], "required": True, "type": "multi-select",
                 "description": "Select 2-3 matching categories from PH's taxonomy"},
                {"name": "makers", "label": "Makers", "value": [state.get("author", {}).get("name", "")], "required": True, "type": "user-list"},
                {"name": "launch_date", "label": "Launch date", "value": state.get("launch_date", ""), "required": True, "type": "date"}
            ],
            "assets_required": [
                {"type": "image", "role": "thumbnail", "path": asset(state, "thumbnail") or f"{LAUNCHES_DIR}/{state['slug']}/assets/ph-thumbnail.png",
                 "constraints": {"width": 1270, "height": 760, "format": "png", "max_size_mb": 2},
                 "required": True},
                {"type": "image", "role": "gallery", "paths": [], "min_count": 3, "max_count": 5,
                 "constraints": {"min_width": 1200}, "required": True},
                {"type": "video", "role": "demo", "path": asset(state, "demo_video"),
                 "constraints": {"max_duration_seconds": 60, "format": "mp4"}, "required": False}
            ],
            "pre_submit_checklist": [
                "Launch scheduled 12:01 AM PT on Tue/Wed/Thu",
                "20-30 supporters DM'd >=24h in advance (privately, no public 'please upvote')",
                "All gallery images + thumbnail + video uploaded",
                "First comment drafted, <500 words",
                "Calendar blocked 12h for comment responses",
                "Email/newsletter launch announcement queued"
            ],
            "post_submit_actions": [
                {"action": "post_first_comment", "delay_seconds": 120, "value": first_comment,
                 "description": "Post as the 1st comment on the PH page"},
                {"action": "notify_supporters", "delay_seconds": 300,
                 "description": "Send DM to pre-notified supporters: 'we're live, if you believe in it your feedback would mean a lot'"},
                {"action": "x_thread_link", "delay_seconds": 1800,
                 "description": "Drop PH link in X thread reply #2"}
            ],
            "human_review_required_before_submit": True,
            "notes": [
                "2026: 79% of featured launches are self-hunted. No hunter required.",
                "Submit between 00:01-00:15 PT Tue/Wed/Thu for max organic window.",
                "Reply to every comment within 1h for first 8h (affects ranking)."
            ]
        }

    # ---- HuggingFace model ----
    if channel_id == "huggingface":
        return {
            **base,
            "platform": "HuggingFace Model Hub",
            "submission_method": "form",
            "auth_required": True,
            "url": "https://huggingface.co/new",
            "fields": [
                {"name": "owner", "label": "Owner (user or org)", "value": state.get("author", {}).get("github", ""), "required": True},
                {"name": "model_name", "label": "Model name", "value": name, "required": True},
                {"name": "license", "label": "License", "value": "apache-2.0", "required": True, "type": "select"},
                {"name": "private", "label": "Private repo", "value": False, "required": True, "type": "bool"}
            ],
            "assets_required": [
                {"type": "file", "role": "model_weights", "paths": [], "required": True,
                 "notes": "Upload via git-lfs or HF hub API after repo creation"},
                {"type": "markdown", "role": "model_card", "path": f"{LAUNCHES_DIR}/{state['slug']}/copy/huggingface.md",
                 "required": True,
                 "notes": "Must have YAML frontmatter: pipeline_tag, library_name, license, datasets, tags"}
            ],
            "pre_submit_checklist": [
                "Model card has complete YAML frontmatter",
                "pipeline_tag set correctly (critical for search)",
                "Quantized variants (GGUF, MLX) uploaded as separate repos or in a Collection",
                "Space demo running and tested with 3 different inputs",
                "Benchmark table vs named baseline in model card",
                "License clearly stated"
            ],
            "post_submit_actions": [
                {"action": "create_space", "description": "Create gradio/streamlit Space for live demo"},
                {"action": "add_to_collection", "description": "Add all model variants to a named Collection"}
            ]
        }

    # ---- Anthropic marketplace ----
    if channel_id == "anthropic-marketplace":
        return {
            **base,
            "platform": "Anthropic Plugin Marketplace",
            "submission_method": "form",
            "auth_required": True,
            "url": "https://platform.claude.com/plugins/submit",
            "fields": [
                {"name": "plugin_name", "label": "Plugin name", "value": name, "required": True},
                {"name": "repo_url", "label": "GitHub repo URL", "value": url, "required": True},
                {"name": "manifest_url", "label": "plugin.json URL", "value": f"{url.rstrip('/')}/blob/main/.claude-plugin/plugin.json", "required": True},
                {"name": "description", "label": "Description", "value": tagline, "required": True},
                {"name": "category", "label": "Category", "value": "", "required": True, "type": "select",
                 "description": "Pick from: productivity, devops, data, security, writing, etc."},
                {"name": "license", "label": "License", "value": "MIT", "required": True}
            ],
            "assets_required": [
                {"type": "image", "role": "icon", "path": asset(state, "logo"),
                 "constraints": {"width": 512, "height": 512}, "required": False},
                {"type": "image", "role": "screenshots", "paths": [], "min_count": 1, "required": False}
            ],
            "pre_submit_checklist": [
                ".claude-plugin/plugin.json exists at repo root",
                "hooks/hooks.json valid (if hook plugin)",
                "README has /plugin install snippet",
                "Tested install from a fresh Claude Code session"
            ],
            "post_submit_actions": [
                {"action": "wait_for_review", "description": "Anthropic review is automatic + manual. Check back in 24-72h."}
            ],
            "notes": [
                "Alternative URL: https://claude.ai/settings/plugins/submit",
                "'Anthropic Verified' badge available for vetted plugins after initial approval"
            ]
        }

    # ---- Generic directory forms ----
    directory_forms = {
        "betalist": {
            "platform": "BetaList", "url": "https://betalist.com/submit",
            "fields_extra": [
                {"name": "waitlist_url", "label": "Waitlist URL", "value": url, "required": True},
                {"name": "expedited_paid", "label": "Expedited ($129, 3-4 days)", "value": False, "type": "bool"}
            ],
            "notes": ["Pre-launch only. Free queue takes 2+ months. Expedited = $129."]
        },
        "uneed": {
            "platform": "Uneed", "url": "https://www.uneed.best/submit",
            "fields_extra": [],
            "notes": ["Weekly cohort. Tier 1 = 'big launcher' paid upgrade."]
        },
        "fazier": {
            "platform": "Fazier", "url": "https://fazier.com/submit",
            "fields_extra": [],
            "notes": ["Weekly launches, lower noise than PH. Great for calm first launches."]
        },
        "microlaunch": {
            "platform": "MicroLaunch", "url": "https://microlaunch.net/submit",
            "fields_extra": [],
            "notes": ["1-month directory run. 50K monthly visitors. 'Roasts/Boosts' feedback mechanic."]
        },
        "peerlist": {
            "platform": "Peerlist Spotlight", "url": "https://peerlist.io/scroll",
            "fields_extra": [],
            "notes": ["188K-209K MAU. Capped at 50 products/week. Submit Monday."]
        },
        "tinylaunch": {
            "platform": "TinyLaunch", "url": "https://tinylaunch.com/submit",
            "fields_extra": [],
            "notes": ["Free weekly rounds. Top-3 badge."]
        },
        "terminal-trove": {
            "platform": "Terminal Trove", "url": "https://terminaltrove.com/submit",
            "fields_extra": [
                {"name": "install_command", "label": "Install command", "value": "", "required": True}
            ],
            "notes": ["CLI tools only. Must be installable via standard package manager."]
        },
        "departures-to": {
            "platform": "departures.to (TestFlight beta)", "url": "https://departures.to/submit",
            "fields_extra": [
                {"name": "testflight_url", "label": "TestFlight public link", "value": "", "required": True}
            ],
            "notes": ["iOS beta testers. Submit weeks before App Store launch."]
        }
    }

    if channel_id in directory_forms:
        d = directory_forms[channel_id]
        return {
            **base,
            "platform": d["platform"],
            "submission_method": "form",
            "auth_required": True,
            "url": d["url"],
            "fields": [
                {"name": "name", "label": "Product name", "value": name, "required": True},
                {"name": "tagline", "label": "Tagline", "value": tagline, "required": True, "max_length": 60},
                {"name": "url", "label": "URL", "value": url, "required": True},
                {"name": "description", "label": "Description", "value": why_story or tagline, "required": True, "type": "textarea"},
                {"name": "email", "label": "Contact email", "value": state.get("author", {}).get("email", ""), "required": True},
                *d["fields_extra"]
            ],
            "assets_required": [
                {"type": "image", "role": "logo", "path": asset(state, "logo"),
                 "constraints": {"min_width": 200}, "required": False},
                {"type": "image", "role": "og_image", "path": asset(state, "og_image"),
                 "constraints": {"width": 1200, "height": 630}, "required": False}
            ],
            "pre_submit_checklist": [
                "Email inbox monitored for directory confirmation links",
                "OG image renders correctly at linked URL"
            ],
            "post_submit_actions": [],
            "notes": d["notes"]
        }

    # ---- X thread — delegated to xmaster skill ----
    if channel_id == "x-thread":
        return {
            **base,
            "platform": "X / Twitter",
            "submission_method": "delegated",
            "auth_required": True,
            "url": None,
            "fields": [
                {"name": "copy_file", "label": "Drafted thread", "value": f"{LAUNCHES_DIR}/{state['slug']}/copy/x-thread.md", "type": "file"}
            ],
            "pre_submit_checklist": [
                "xmaster config set style.voice done",
                "xmaster analyze score >= B on tweet #1",
                "Video or image attached (1x text vs 5x video reach)",
                "No external link in tweet #1 (March 2026 algorithm penalty)"
            ],
            "post_submit_actions": [
                {"action": "reply_cadence", "description": "Reply to every comment within 60 min (replies ~150x likes)"}
            ],
            "notes": [
                "DELEGATE to xmaster skill. Do not attempt to post via web-form automation.",
                "Sequence: xmaster analyze → user approves → xmaster post → reply-chain remaining tweets"
            ],
            "delegated_to": "xmaster"
        }

    # ---- Email channels — delegated ----
    if channel_id in {"email-announcement", "newsletter"}:
        return {
            **base,
            "platform": "Email",
            "submission_method": "delegated",
            "url": None,
            "fields": [
                {"name": "copy_file", "label": "Email draft", "value": f"{LAUNCHES_DIR}/{state['slug']}/copy/{channel_id}.md", "type": "file"}
            ],
            "pre_submit_checklist": [
                "Subject line <50 chars",
                "No images in body (deliverability)",
                "One primary CTA"
            ],
            "notes": [
                "DELEGATE to email-cli (single/small) or mailing-list-cli (broadcast list).",
                "Commands: `email-cli send --to <addr> --subject ... --text ...` OR `mailing-list-cli broadcast create ...`"
            ],
            "delegated_to": "email-cli or mailing-list-cli"
        }

    # ---- Local-only actions (repo work, asset generation) ----
    local_actions = {
        "readme": {"platform": "GitHub README polish", "delegated_to": "github-optimization"},
        "og-image": {"platform": "OG image generation", "delegated_to": "canvas-design or chatgpt-image"},
        "landing-page": {"platform": "Landing page polish", "delegated_to": "seo-geo-optimizer"},
        "plugin-manifest": {"platform": "Plugin manifest check", "delegated_to": None},
        "registry": {"platform": "Package registry publish", "delegated_to": None},
        "welcome-sequence": {"platform": "Newsletter welcome sequence", "delegated_to": "mailing-list-cli"},
        "substack-notes": {"platform": "Substack Notes", "delegated_to": None},
        "beehiiv-recommendations": {"platform": "beehiiv Recommendations", "delegated_to": None},
        "app-store-metadata": {"platform": "App Store Connect metadata", "delegated_to": "app-store-connect"},
        "testflight-public": {"platform": "TestFlight public link", "delegated_to": "app-store-connect"}
    }

    if channel_id in local_actions:
        la = local_actions[channel_id]
        return {
            **base,
            "platform": la["platform"],
            "submission_method": "local-action",
            "url": None,
            "delegated_to": la["delegated_to"],
            "notes": ["Local action; not a web submission. Delegate or handle in-repo."]
        }

    # ---- GitHub issue-template (awesome-list) ----
    if channel_id in {"awesome-claude-code", "awesome-list"}:
        prefill = build_url(channel_id, state)
        return {
            **base,
            "platform": "GitHub issue submission (awesome list)",
            "submission_method": "issue-template",
            "auth_required": True,
            "url": prefill,
            "fields": [
                {"name": "resource-name", "label": "Resource name", "value": name, "required": True},
                {"name": "resource-url", "label": "Resource URL", "value": url, "required": True},
                {"name": "description", "label": "Description", "value": tagline, "required": True, "max_length": 120}
            ],
            "pre_submit_checklist": [
                "Read list's CONTRIBUTING.md",
                "Confirm no CoC bans CLI/programmatic submission (awesome-claude-code DOES)",
                "Repo 1+ week old, public, documented",
                "Check this resource isn't already listed"
            ],
            "notes": [
                "Many awesome lists EXPLICITLY BAN `gh issue create`. Open the pre-filled URL in a browser tab — submit via UI.",
                "If you attempt automated submit and it violates CoC, account may be flagged."
            ]
        }

    # ---- Fallback ----
    return {
        **base,
        "platform": channel_id,
        "notes": ["No schema defined. Check references/platforms.md or handle manually."]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--channel", help="only one channel id")
    parser.add_argument("--json", action="store_true", default=True)
    args = parser.parse_args()

    state = load_state(args.slug)
    ids = [args.channel] if args.channel else [c["id"] for c in state["channels"]]
    out = []
    for cid in ids:
        try:
            out.append(schema_for(cid, state))
        except Exception as e:
            out.append({"channel_id": cid, "error": str(e)})
    if args.channel:
        print(json.dumps(out[0], indent=2))
    else:
        print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
