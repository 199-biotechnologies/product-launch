---
name: product-launch
description: "Launch-day operator and tracker for any product — SaaS, open source repos, ML models, Claude Code plugins, CLI tools, mobile apps, newsletters. Recommends the right channels for the product type, drafts platform-specific copy, generates pre-filled submission URLs, opens tabs in batch, delegates to xmaster (X), email-cli (email), mailing-list-cli (newsletter), github-optimization (README), and canvas-design (OG image). Persists launch state so ADHD operators can resume across sessions — one next action at a time. Use when user says 'launch my product', 'launch this repo', 'launch an app', 'Product Hunt launch', 'Show HN', 'launch strategy', 'where should I launch', 'promote my product', 'help me launch', 'go-to-market', 'GTM plan', 'ship it', 'launch this SaaS', 'launch a plugin', 'launch my model', 'launch newsletter', 'launch on reddit', 'launch checklist', 'prep a launch', 'launch day plan', 'what's next for my launch'. Also trigger on 'product-launch' and any `/product-launch` invocation."
---

# Product Launch Orchestrator

Launch-day operator and tracker. Acts as **advisor + preparer + assistant**:

1. **Advise** — ask what the user built, recommend channels that fit the product type. Never "post everywhere" by default.
2. **Prepare** — draft platform-specific copy, generate assets, pre-fill submission URLs, open tabs in batch.
3. **Track** — persist launch state in `~/.claude/launches/<slug>/launch.json` so the next session picks up exactly where it left off.

**Designed for ADHD operators:** one next action at a time. Clear "where am I, what's next". Low typing burden — pre-fill everything that can be pre-filled.

## Triage first: what are they launching?

Ask one question before anything else. Match the answer to a playbook:

| Product type | Playbook keyword | Primary channels |
|--------------|------------------|------------------|
| Open source repo, library, CLI | `oss` | GitHub README → Show HN → awesome lists → niche subs |
| SaaS / commercial web app | `saas` | Product Hunt → BetaList/Uneed/Fazier → r/SaaS → newsletter |
| ML model / dataset / fine-tune | `ml` | HuggingFace → r/LocalLLaMA → r/ML → Papers With Code |
| Claude Code plugin / hook | `claude-plugin` | Anthropic marketplace → awesome-claude-code → r/ClaudeAI → Show HN |
| CLI tool | `cli` | Show HN → Terminal Trove → r/commandline → Homebrew/cargo/npm |
| Mobile app (iOS/Android) | `mobile` | App Store/Play → TestFlight public link → PH Apps → r/iosapps |
| Newsletter / content product | `newsletter` | beehiiv Boosts → Substack Notes → r/SubstackReads → cross-post |

See `references/playbooks.md` for the full per-type sequence.

## Core workflow

### 1. Start a launch (once per product)

```bash
python3 ~/.claude/skills/product-launch/scripts/new_launch.py <slug>
```

Interactive. Collects product name, type, tagline, URL, why-story, launch date. Creates:
- `~/.claude/launches/<slug>/launch.json` — persistent state
- `~/.claude/launches/<slug>/copy/` — drafted copy per channel
- `~/.claude/launches/<slug>/assets/` — place for OG image, demo GIF, logo

Then point the user at the drafted copy, ask them to review, adjust.

### 2. Check status (every session)

```bash
python3 ~/.claude/skills/product-launch/scripts/status.py [slug]
```

Shows timeline + done/pending/scheduled counts + the **next 1–3 actions**. Run this at the start of every session the user mentions the launch. This is the ADHD anchor.

Without a slug, lists every launch in `~/.claude/launches/`.

### 3. Pre-fill submissions

```bash
python3 ~/.claude/skills/product-launch/scripts/prefill_urls.py <slug>
```

Generates pre-filled browser URLs for every submission form (Show HN, Reddit subs, GitHub issue templates for awesome-* lists, Anthropic marketplace, etc.). Prints a markdown table.

### 4. Open tabs in batch

```bash
python3 ~/.claude/skills/product-launch/scripts/open_tabs.py <slug> [--only show-hn,reddit-sideproject]
```

Opens pre-filled URLs in the user's default browser via `open`. User clicks submit in each. Done-by-default filtering: only opens channels marked `pending` or `scheduled`.

### 5. Delegate to other skills

Use these proactively — do NOT re-implement what they do:

| Need | Skill to invoke | Input |
|------|----------------|-------|
| Post X thread | `xmaster` | `copy/x-thread.md` — analyze first, post only after user says "go" |
| Send launch email | `email-cli` | `copy/email-announcement.md` |
| Broadcast to newsletter list | `mailing-list-cli` | `copy/newsletter.md` |
| Polish README / GitHub metadata | `github-optimization` | repo path |
| Generate OG image / logo | `canvas-design` or `chatgpt-image` | brand colors, tagline |
| Extract brand from a URL | `design-identity` | landing page URL |
| SEO / schema for landing page | `seo-geo-optimizer` | HTML path |

### 6. Mark channels done

After the user posts on a channel, update state:

```bash
python3 ~/.claude/skills/product-launch/scripts/status.py <slug> --mark show-hn=done --posted-url https://news.ycombinator.com/item?id=...
```

### 7. Day 2–7 follow-through

`status.py` surfaces day-2, day-3, day-7 post-launch actions (reply to comments, ship a bug fix from feedback, publish retrospective). See `references/checklists.md`.

## Hard rules

1. **Never post publicly without explicit user approval.** Always show drafted copy first, wait for "go" / "yes" / "post it".
2. **Respect platform Codes of Conduct.** awesome-claude-code explicitly bans `gh` CLI submissions → use the pre-filled URL path. Check `references/platforms.md` before auto-submitting anywhere.
3. **No sock-puppet upvote coordination.** Never suggest public "please upvote" tweets — HN/PH ring-detection will ban. Private DMs to 5–10 friends with the link are fine.
4. **Pre-fill, don't auto-submit.** For anything public-facing, open a pre-filled tab. User clicks submit.
5. **Exception — CLI-native channels.** X (via `xmaster analyze` → user approves → `xmaster post`), email (via `email-cli`), newsletter (via `mailing-list-cli`) may be dispatched after explicit approval.
6. **One next action at a time.** Never dump 20 tasks on the user. `status.py` shows 1–3 actions. Defer the rest.
7. **No AI-slop in launch copy.** Ban list in `references/content.md` — enforce it on every draft. "Delve", "leverage", "unlock", "seamless", "game-changer" → rewrite. Read aloud test.

## Advisor mode (no launch created yet)

When the user asks "where should I launch X?" without wanting a full plan:
1. Identify product type from their description (ask if ambiguous)
2. Read `references/playbooks.md` for that type
3. Give 5–8 channels ranked by **reach × fit × effort**, each with one sentence on why
4. Offer: "Want me to scaffold a full launch plan with drafted copy?"

Keep the advisor response under ~200 words. Don't dump every platform at once.

## Readiness check

Before recommending any public submission, verify:

- [ ] Product URL loads (200) and is not a waitlist (HN rejects these)
- [ ] README has a 3-command Quickstart (for OSS/CLI)
- [ ] OG image exists at `assets/og-image.png` (1200×630)
- [ ] Demo video or GIF exists (for PH + X)
- [ ] Author handles configured in launch.json

If any fail, flag them and suggest the delegating skill to fix (e.g., `canvas-design` for OG image).

## Agent-to-agent integration

This skill's outputs are first-class inputs for other agents — browser automation (browser-use, playwright MCP, Claude computer-use), orchestrators, schedulers.

```bash
# Capability manifest (call once to discover)
python3 scripts/agent_info.py

# Structured form schemas — consumable by web-automation agents
python3 scripts/form_schema.py <slug>                    # all channels
python3 scripts/form_schema.py <slug> --channel product-hunt

# Pre-filled URLs (JSON)
python3 scripts/prefill_urls.py <slug> --json

# Current state + next actions (JSON)
python3 scripts/status.py <slug> --json
```

**form_schema.py** is the primary integration point. For each channel it returns:
- `submission_method` — `url-prefill` | `form` | `issue-template` | `delegated` | `local-action`
- `url` — submission URL (if applicable)
- `fields[]` — each with `name`, `label`, `value`, `type`, `required`, `max_length`, `selector_hints[]`, `constraints`
- `assets_required[]` — files the agent should upload (with path + constraints)
- `pre_submit_checklist[]` — gates the agent should verify before submit
- `post_submit_actions[]` — first comment, notify supporters, etc.
- `human_review_required_before_submit` — mostly `true`; automation agents must surface for approval
- `delegated_to` — if another skill owns this channel (e.g., `xmaster` for X)

An automation agent reads this schema, fills each field, verifies the checklist, then presents to the user OR (if `human_review_required_before_submit=false`) submits directly. Selector hints are best-effort — agents should also match by label/placeholder.

## Key references

- `references/platforms.md` — full platform registry: URL templates, submission rules, timing, reach
- `references/content.md` — copy patterns, anti-AI-slop ban list, hook templates per channel
- `references/playbooks.md` — sequenced playbook per product type
- `references/checklists.md` — pre-launch / launch-day / post-launch checklists
- `references/launch-wisdom.md` — curated 2026 insights from real launches (Yongfook, Velo, TextCortex, etc.)

## Templates (drafted copy)

`templates/` holds starter copy for every major channel. `new_launch.py` copies these into `copy/` with `{{variables}}` filled. The user edits from there.

- `templates/show-hn.md`
- `templates/product-hunt.md`
- `templates/reddit-sideproject.md`, `reddit-saas.md`, `reddit-claudeai.md`, `reddit-localllama.md`, `reddit-ml.md`, `reddit-selfhosted.md`
- `templates/x-thread.md`
- `templates/readme-hero.md`
- `templates/email-announcement.md`
- `templates/awesome-list-issue.md`
