<div align="center">

# product-launch

**A Claude Code skill that turns launch day into one next action at a time.**

<br />

[![Star this repo](https://img.shields.io/github/stars/199-biotechnologies/product-launch?style=for-the-badge&logo=github&label=%E2%AD%90%20Star%20this%20repo&color=yellow)](https://github.com/199-biotechnologies/product-launch/stargazers)
&nbsp;&nbsp;
[![Follow @longevityboris](https://img.shields.io/badge/Follow_%40longevityboris-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/longevityboris)

<br />

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](https://docs.claude.com/en/docs/agents-and-tools)
&nbsp;
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](./LICENSE)
&nbsp;
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](./CONTRIBUTING.md)
&nbsp;
[![Agent Ready](https://img.shields.io/badge/agent-consumable-6E56CF?style=for-the-badge)](#agent-integration)

---

Drafts platform-specific copy. Pre-fills submission URLs. Tracks state across sessions. Emits structured form schemas so browser-automation agents can fill launches directly. Built for people who've opened 17 tabs and forgotten why.

[Install](#install) | [How It Works](#how-it-works) | [Features](#features) | [Agent Integration](#agent-integration) | [Contributing](#contributing)

</div>

## Why This Exists

Launching is easy to start and hard to finish. Twenty open tabs, five accounts, unclear order, no memory of what's done. Every session you rebuild the whole plan from scratch.

This skill keeps the state for you. It shows **one next action at a time**. It pre-fills every submission form that supports URL parameters. For the ones that don't — Product Hunt, HuggingFace, BetaList — it hands a browser-automation agent a structured JSON schema and tells the agent exactly which fields to fill.

It also enforces the anti-AI-slop ban list on drafted copy, because Hacker News and Reddit can smell "leverage" and "seamlessly" from three subreddits away.

## Before vs After

| Without | With product-launch |
|---|---|
| 20 open tabs, unclear order | One next action at a time |
| Copy that sounds like a press release | Anti-AI-slop ban list enforced |
| Same pitch pasted on every sub | 19 per-channel copy templates |
| "What did I post yesterday?" | Persistent state across sessions |
| Write your own form-filling code | Machine-readable JSON schemas for agents |
| Forget which platforms ban `gh` CLI submissions | Skill knows, uses pre-filled URL path |

## Install

```bash
git clone https://github.com/199-biotechnologies/product-launch.git ~/.claude/skills/product-launch
```

That's it. Claude Code discovers skills in `~/.claude/skills/` automatically. Trigger by typing `/product-launch`, or by saying things like "help me launch my product", "where should I launch", "Show HN prep", or "Product Hunt launch plan".

## How It Works

```
┌───────────────────────────────────────────────────────────────────┐
│  1. You say: "help me launch my Claude plugin"                    │
│                                                                   │
│  2. Skill picks the right playbook:                               │
│     oss · saas · ml · claude-plugin · cli · mobile · newsletter   │
│                                                                   │
│  3. new_launch.py  →  ~/.claude/launches/<slug>/                  │
│                       ├── launch.json                             │
│                       ├── copy/<channel>.md  (drafted per channel)│
│                       └── assets/                                 │
│                                                                   │
│  4. status.py      →  "next 1–3 actions" every session            │
│     prefill_urls.py → pre-filled HN / Reddit / GitHub issue URLs  │
│     open_tabs.py   →  opens them in batch                         │
│                                                                   │
│  5. form_schema.py →  structured JSON for automation agents       │
│     (browser-use, playwright MCP, Claude computer-use)            │
│                                                                   │
│  6. Delegates to existing skills:                                 │
│     xmaster · email-cli · mailing-list-cli · github-optimization  │
│     canvas-design · chatgpt-image · humanise-text · design-identity│
└───────────────────────────────────────────────────────────────────┘
```

Every script supports `--json`. Nothing runs without your explicit "go" on public-facing posts.

## Features

| Area | What you get |
|---|---|
| **Product types** | 7 sequenced playbooks: OSS repo, SaaS, ML model, Claude plugin, CLI, mobile app, newsletter |
| **Channels** | 30+ platforms with rules, timing, karma thresholds, and CoC gotchas documented |
| **Copy templates** | 19 per-channel drafts — Show HN, Product Hunt, 11 Reddit subs, X thread, README hero, launch email, awesome-list issue, LinkedIn, Dev.to |
| **Pre-filled URLs** | HN submit, Reddit submit, GitHub issue templates, Dev.to editor, LinkedIn share, mailto |
| **Persistent state** | `~/.claude/launches/<slug>/launch.json` — resume any session with `status.py` |
| **Agent outputs** | `agent_info.py` (capability manifest), `form_schema.py` (form fields + asset paths + checklists) |
| **Delegation** | Hands X to `xmaster`, email to `email-cli`, newsletters to `mailing-list-cli`, README to `github-optimization`, OG images to `canvas-design` |
| **Anti-AI-slop** | Ban list enforced on drafted copy — "leverage", "seamless", "game-changer", etc. |
| **Launch wisdom** | 13 curated insights from real 2026 launches (Yongfook, Velo, TextCortex, etc.) |

## Agent Integration

Other agents — browser automation, orchestrators, schedulers — can consume this skill without parsing human prose. Every script emits structured JSON.

```bash
python3 scripts/agent_info.py                   # capability manifest
python3 scripts/form_schema.py <slug>           # all channels, agent-ready
python3 scripts/form_schema.py <slug> --channel product-hunt
python3 scripts/status.py <slug> --json         # state + next_actions[]
python3 scripts/prefill_urls.py <slug> --json   # URL-encoded submission links
```

`form_schema.py` returns per channel:

```json
{
  "channel_id": "product-hunt",
  "submission_method": "form",
  "url": "https://www.producthunt.com/posts/new",
  "fields": [
    {"name":"tagline","value":"...","max_length":60,"selector_hints":["input[name='tagline']"]}
  ],
  "assets_required": [
    {"type":"image","role":"thumbnail","path":"/.../ph-thumbnail.png","constraints":{"width":1270,"height":760}}
  ],
  "pre_submit_checklist": ["launch scheduled Tue/Wed/Thu 12:01 AM PT", "..."],
  "post_submit_actions": [{"action":"post_first_comment","delay_seconds":120,"value":"..."}],
  "human_review_required_before_submit": true,
  "delegated_to": null
}
```

A browser-automation agent reads `fields[]` and `assets_required[]`, fills the form, verifies the checklist, and either submits or surfaces for user approval depending on `human_review_required_before_submit`.

## What's Inside

```
product-launch/
├── SKILL.md                    # Skill definition — triggers, workflow, hard rules
├── references/
│   ├── platforms.md            # 30+ platforms: URL templates, rules, timing, reach
│   ├── content.md              # Copy patterns, hook templates, anti-slop ban list
│   ├── playbooks.md            # Sequenced playbook per product type
│   ├── checklists.md           # Pre / day / post launch
│   └── launch-wisdom.md        # Curated 2026 insights from real launches
├── scripts/                    # Python stdlib only — no deps
│   ├── new_launch.py           # Scaffold a launch
│   ├── status.py               # Next-action tracker
│   ├── prefill_urls.py         # Generate pre-filled submission URLs
│   ├── open_tabs.py            # Batch-open pre-filled tabs
│   ├── agent_info.py           # Capability manifest for other agents
│   └── form_schema.py          # Structured form schemas for automation
└── templates/                  # 19 per-channel copy templates
```

## Hard Rules the Skill Enforces

1. Never posts publicly without explicit user approval
2. Respects platform Codes of Conduct — awesome-claude-code bans `gh` CLI submissions, the skill knows this and uses the pre-filled URL path instead
3. No public upvote-ring coordination (HN/PH detect and ban)
4. Pre-fills forms, never auto-submits to public destinations
5. One next action at a time — surfaces 1–3 max, never 20

## Contributing

PRs welcome. Especially: new platform specs in `references/platforms.md`, new channel templates in `templates/`, new form schemas in `scripts/form_schema.py`. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE).

---

<div align="center">

Built by [Boris Djordjevic](https://github.com/longevityboris) at [Paperfoot AI](https://paperfoot.com)

<br />

**If this is useful to you:**

[![Star this repo](https://img.shields.io/github/stars/199-biotechnologies/product-launch?style=for-the-badge&logo=github&label=%E2%AD%90%20Star%20this%20repo&color=yellow)](https://github.com/199-biotechnologies/product-launch/stargazers)
&nbsp;&nbsp;
[![Follow @longevityboris](https://img.shields.io/badge/Follow_%40longevityboris-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/longevityboris)

</div>
