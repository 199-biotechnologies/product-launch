#!/usr/bin/env python3
"""Machine-readable capability manifest for agent integration.

Usage:
  agent_info.py           # JSON manifest to stdout
  agent_info.py --pretty  # pretty-printed (same, kept for parity with other CLIs)

Other agents (automation agents, orchestrators, web-form fillers) should call
this once to discover what product-launch can do and what its outputs look like.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

MANIFEST = {
    "name": "product-launch",
    "version": "1.0.0",
    "kind": "orchestrator",
    "description": (
        "Launch-day operator and tracker. Maintains persistent launch state "
        "at ~/.claude/launches/<slug>/ and produces agent-consumable outputs "
        "(pre-filled URLs, form schemas, next-action plans) for browser "
        "automation agents and orchestrators."
    ),
    "skill_dir": str(SKILL_DIR),
    "state_dir_template": "~/.claude/launches/<slug>/",
    "state_files": {
        "launch.json": "Persistent launch state: metadata, assets, channels, status, timestamps.",
        "copy/<channel>.md": "Drafted per-channel copy, editable markdown with {{variables}} already rendered.",
        "assets/": "OG image, demo video, logo, thumbnails."
    },
    "commands": [
        {
            "name": "new_launch",
            "script": "scripts/new_launch.py",
            "purpose": "Scaffold a new launch (creates state dir + drafted copy).",
            "args": [
                {"name": "slug", "required": True, "kind": "positional", "description": "kebab-case identifier"},
                {"name": "--json-input", "required": False, "kind": "flag", "description": "Path or '-' for stdin — JSON with launch metadata"},
                {"name": "--force", "required": False, "kind": "flag", "description": "overwrite existing state dir"}
            ],
            "json_input_schema": {
                "name": "string (required)",
                "type": "enum: oss | saas | ml | claude-plugin | cli | mobile | newsletter",
                "tagline": "string <60 chars",
                "url": "string (canonical product URL)",
                "launch_date": "YYYY-MM-DD",
                "why_story": "string (optional, 1-3 sentences)",
                "author_name": "string",
                "author_github": "string",
                "author_x": "string (handle without @)",
                "author_email": "string",
                "long_tagline": "string (optional, longer description)"
            },
            "output_schema": {
                "status": "ok | error",
                "launch_dir": "path",
                "state_path": "path to launch.json",
                "copy_dir": "path to copy/ dir",
                "assets_dir": "path to assets/ dir",
                "slug": "string",
                "type": "product type",
                "channels": "array of channel IDs",
                "drafted_copy": "array of channel IDs with populated copy files",
                "next_actions": "array of human-readable next steps"
            }
        },
        {
            "name": "status",
            "script": "scripts/status.py",
            "purpose": "Read and mutate launch state; surface next 1-3 actions.",
            "args": [
                {"name": "slug", "required": False, "kind": "positional", "description": "omit to list all launches"},
                {"name": "--json", "kind": "flag", "description": "JSON output"},
                {"name": "--mark", "kind": "repeatable", "description": "id=status — pending|scheduled|done|skip|failed"},
                {"name": "--schedule", "kind": "repeatable", "description": "id=ISO-timestamp"},
                {"name": "--posted-url", "kind": "string", "description": "Attach a posted URL to the last --mark'd channel"},
                {"name": "--note", "kind": "string", "description": "append a timestamped note"},
                {"name": "--set-asset", "kind": "repeatable", "description": "key=path — og_image, demo_url, demo_video, logo"},
                {"name": "--set-launch-date", "kind": "string", "description": "YYYY-MM-DD"}
            ],
            "json_output_schema": {
                "slug": "string",
                "state": "full launch.json contents",
                "next_actions": "array[string] of up to 3 prioritized actions"
            }
        },
        {
            "name": "prefill_urls",
            "script": "scripts/prefill_urls.py",
            "purpose": "Generate pre-filled submission URLs for each pending/scheduled channel.",
            "args": [
                {"name": "slug", "required": True, "kind": "positional"},
                {"name": "--json", "kind": "flag", "description": "JSON array"},
                {"name": "--only", "kind": "string", "description": "comma-separated channel ids"},
                {"name": "--include-done", "kind": "flag"}
            ],
            "json_output_schema": {
                "id": "channel id",
                "platform": "display name",
                "status": "channel status",
                "submission_url": "pre-filled URL or null",
                "manual_only": "bool — true if no URL-prefill possible (delegate to automation agent or user)"
            },
            "consumer_hint": "Browser automation: navigate to submission_url, review, submit. URL is URL-encoded."
        },
        {
            "name": "open_tabs",
            "script": "scripts/open_tabs.py",
            "purpose": "Batch-open pre-filled URLs in the local default browser via macOS `open` / `xdg-open` / Windows `start`.",
            "args": [
                {"name": "slug", "required": True, "kind": "positional"},
                {"name": "--only", "kind": "string", "description": "comma-separated channel ids"},
                {"name": "--dry-run", "kind": "flag", "description": "print JSON of what would be opened"},
                {"name": "--delay", "kind": "float", "description": "seconds between tabs (default 0.5)"},
                {"name": "--include-done", "kind": "flag"}
            ]
        },
        {
            "name": "form_schema",
            "script": "scripts/form_schema.py",
            "purpose": "Return structured form-field schemas — consumable by web automation agents (browser-use, playwright, computer-use, etc.).",
            "args": [
                {"name": "slug", "required": True, "kind": "positional"},
                {"name": "--channel", "kind": "string", "description": "one channel id (default: all)"},
                {"name": "--json", "kind": "flag", "description": "JSON (default)"}
            ],
            "json_output_schema": {
                "channel_id": "string",
                "platform": "display name",
                "submission_method": "url-prefill | form | issue-template | manual",
                "auth_required": "bool",
                "url": "submission URL",
                "fields": "array of {name, label, type, value | file_path, required, max_length, constraints, selector_hints[]}",
                "assets_required": "array of {type, role, path, constraints}",
                "pre_submit_checklist": "array[string]",
                "post_submit_actions": "array of {action, delay_seconds, value, description}",
                "human_review_required_before_submit": "bool",
                "notes": "array[string] — platform-specific gotchas"
            },
            "consumer_hint": "This is the primary integration point for automation agents. Read fields[], fill each, verify pre_submit_checklist passes, submit ONLY after human_review_required_before_submit=false or user approval."
        },
        {
            "name": "agent_info",
            "script": "scripts/agent_info.py",
            "purpose": "This manifest. Call once to discover capabilities.",
            "args": []
        }
    ],
    "agent_integrations": {
        "browser_automation": {
            "primary_input": "scripts/form_schema.py <slug>",
            "output": "Structured form fields + asset paths an automation agent uses to fill and submit.",
            "tested_with": ["browser-use", "playwright MCP", "Claude computer-use"],
            "policy": "Most platforms set human_review_required_before_submit=true. Agent must present the filled form for user approval before clicking submit."
        },
        "url_pre_fill": {
            "primary_input": "scripts/prefill_urls.py <slug> --json",
            "output": "URL-encoded submission links; user/agent opens in browser.",
            "policy": "Single-shot, no auth. Preferred when supported (Show HN, Reddit, GitHub issue templates)."
        },
        "orchestrator_resume": {
            "primary_input": "scripts/status.py <slug> --json",
            "output": "Full state + prioritized next_actions[].",
            "policy": "Orchestrators/schedulers poll this on session start to resume work."
        },
        "local_dispatch": {
            "primary_input": "scripts/open_tabs.py <slug>",
            "output": "Opens batch of tabs on the user's machine.",
            "policy": "User-facing. Don't use headless — this is for ADHD operators to click through."
        }
    },
    "delegated_skills": [
        {"name": "xmaster", "purpose": "X/Twitter posting and analysis", "invoke_when": "channel.id == 'x-thread' or 'x-reply'"},
        {"name": "email-cli", "purpose": "Send launch email via Resend", "invoke_when": "channel.id in {'email-announcement'} and no mailing list"},
        {"name": "mailing-list-cli", "purpose": "Broadcast to newsletter list", "invoke_when": "channel.id in {'newsletter', 'email-announcement'} and mailing list exists"},
        {"name": "github-optimization", "purpose": "Polish repo README + metadata", "invoke_when": "channel.id == 'readme'"},
        {"name": "canvas-design", "purpose": "Generate OG images, logos, thumbnails", "invoke_when": "channel.id in {'og-image', 'thumbnail', 'logo'}"},
        {"name": "chatgpt-image", "purpose": "Alternative image generator", "invoke_when": "canvas-design unavailable or user prefers GPT"},
        {"name": "design-identity", "purpose": "Extract brand palette from a live URL", "invoke_when": "no brand guide and site is live"},
        {"name": "seo-geo-optimizer", "purpose": "SEO/GEO schema for landing pages", "invoke_when": "channel.id == 'landing-page'"},
        {"name": "humanise-text", "purpose": "Strip AI tells from drafted copy", "invoke_when": "copy smells like AI — run as pre-submit gate"},
        {"name": "remotion", "purpose": "Programmatic launch videos", "invoke_when": "demo video needed and no existing one"}
    ],
    "product_types": [
        {"id": "oss", "channels": "readme, og-image, show-hn, x-thread, reddit-sideproject, reddit-opensource, dev-to, awesome-list"},
        {"id": "saas", "channels": "landing-page, og-image, product-hunt, email-announcement, newsletter, x-thread, reddit-sideproject, reddit-saas, linkedin, betalist, uneed, fazier, peerlist"},
        {"id": "ml", "channels": "huggingface, og-image, x-thread, reddit-localllama, reddit-ml, papers-with-code, show-hn"},
        {"id": "claude-plugin", "channels": "plugin-manifest, readme, og-image, anthropic-marketplace, awesome-claude-code, show-hn, x-thread, reddit-claudeai, claudemarketplaces"},
        {"id": "cli", "channels": "registry, readme, og-image, show-hn, terminal-trove, x-thread, reddit-commandline, reddit-coolgithub, dev-to"},
        {"id": "mobile", "channels": "app-store-metadata, testflight-public, departures-to, product-hunt, x-thread, reddit-iosapps, linkedin"},
        {"id": "newsletter", "channels": "welcome-sequence, beehiiv-recommendations, substack-notes, x-thread, reddit-substackreads, dev-to-crosspost, linkedin"}
    ],
    "hard_rules": [
        "Never post publicly without explicit user approval. Always show drafted copy, wait for 'go'.",
        "Respect platform Codes of Conduct. awesome-claude-code bans `gh` CLI / programmatic submission.",
        "No public upvote-coordination. HN/PH ring-detection will ban.",
        "Pre-fill, don't auto-submit public-facing forms.",
        "One next action at a time — never dump 20 tasks."
    ],
    "exit_codes": {
        "0": "success",
        "1": "generic error (read stderr)",
        "2": "state not found (slug does not exist)"
    }
}


def main():
    # Both args are acceptable; output is identical JSON for machine consumers.
    print(json.dumps(MANIFEST, indent=2))


if __name__ == "__main__":
    main()
