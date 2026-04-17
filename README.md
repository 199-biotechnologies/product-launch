# product-launch

A Claude Code skill that turns launch day into one next action at a time. Drafts copy, pre-fills submission URLs, tracks progress across sessions, and hands structured form schemas to automation agents.

Works for SaaS, open source repos, ML models, Claude Code plugins, CLI tools, mobile apps, and newsletters.

## Why this exists

Launching is easy to start and hard to finish. Twenty tabs, five accounts, unclear order, no memory of what's done. This skill is an ADHD-friendly launch operator: it keeps the state, shows **one next action at a time**, and pre-fills everything that can be pre-filled.

It also emits machine-readable form schemas, so if you plug a browser-automation agent into your setup (browser-use, playwright MCP, Claude computer-use), it can fill the forms directly.

## Install

```bash
git clone https://github.com/199-biotechnologies/product-launch.git ~/.claude/skills/product-launch
```

That's it. Claude Code discovers skills in `~/.claude/skills/`. Trigger by typing `/product-launch` or by saying "help me launch my product", "where should I launch", "Show HN prep", "Product Hunt launch", etc.

## What it does

### 1. Triage

Ask what you built. Match to a playbook:

| Product type | Primary channels |
|---|---|
| OSS repo / CLI / library | GitHub README → Show HN → awesome lists → niche subs |
| SaaS | Product Hunt → BetaList / Uneed / Fazier → r/SaaS → newsletter |
| ML model | HuggingFace → r/LocalLLaMA → r/MachineLearning → Papers With Code |
| Claude Code plugin | Anthropic marketplace → awesome-claude-code → r/ClaudeAI |
| Mobile app | App Store → TestFlight → Product Hunt Apps → r/iosapps |
| Newsletter | beehiiv Boosts → Substack Notes → r/SubstackReads |

### 2. Scaffold + draft

```bash
python3 scripts/new_launch.py my-product
# → creates ~/.claude/launches/my-product/ with launch.json + drafted copy per channel
```

### 3. Resume every session

```bash
python3 scripts/status.py my-product
# → timeline, done/pending counts, next 1–3 actions
```

### 4. Pre-fill and go

```bash
python3 scripts/prefill_urls.py my-product      # markdown table of links
python3 scripts/open_tabs.py my-product          # opens them in your browser
```

### 5. Agent integration

Every script supports `--json`. For automation agents:

```bash
python3 scripts/agent_info.py                    # capability manifest
python3 scripts/form_schema.py my-product        # structured form fields + asset paths
```

`form_schema.py` returns for each channel: `fields[]` with selector hints, `assets_required[]` with file paths and constraints, `pre_submit_checklist[]`, `post_submit_actions[]`, and `human_review_required_before_submit`. A browser automation agent can fill the form from this directly.

## Delegates to other skills

The skill doesn't reimplement what already exists. It hands off:

- **xmaster** — X/Twitter threads
- **email-cli** — launch emails
- **mailing-list-cli** — newsletter broadcasts
- **github-optimization** — README and repo polish
- **canvas-design** / **chatgpt-image** — OG images, thumbnails
- **design-identity** — brand extraction from live URLs
- **seo-geo-optimizer** — landing page SEO
- **humanise-text** — strip AI tells from drafted copy

## What's inside

```
product-launch/
├── SKILL.md                       # Claude skill definition
├── references/
│   ├── platforms.md               # Every launch platform: URL, rules, timing, reach
│   ├── content.md                 # Copy patterns, anti-AI-slop ban list
│   ├── playbooks.md               # Sequenced playbook per product type
│   ├── checklists.md              # Pre / day / post launch checklists
│   └── launch-wisdom.md           # Curated 2026 insights from real launches
├── scripts/
│   ├── new_launch.py              # Scaffold a launch
│   ├── status.py                  # Next-action tracker
│   ├── prefill_urls.py            # Generate pre-filled submission URLs
│   ├── open_tabs.py               # Batch-open pre-filled tabs
│   ├── agent_info.py              # Capability manifest (for other agents)
│   └── form_schema.py             # Structured form schemas (for automation)
└── templates/                      # Per-channel copy templates (19 channels)
```

## Hard rules the skill enforces

1. Never post publicly without explicit user approval
2. Respect platform Codes of Conduct — awesome-claude-code bans `gh` CLI submissions, the skill knows this and uses the pre-filled URL path
3. No sock-puppet upvote coordination — HN/PH ring-detection will ban
4. Pre-fill, don't auto-submit public-facing forms
5. One next action at a time — never dump 20 tasks on the user

## License

MIT. See [LICENSE](./LICENSE).
