# Launch Platform Registry (2026)

Every platform has: **URL template** (for pre-fill), **applies-to** (product types), **best time**, **rules/gotchas**, **expected reach**. Check each before submitting.

## General tech (any product)

### Show HN (Hacker News)
- **URL template**: `https://news.ycombinator.com/submitlink?u={url}&t={title}`
- **Applies to**: oss, cli, saas, ml, claude-plugin
- **Best time**: Tue–Thu, 8–10 AM ET (13:00–15:00 UTC)
- **Rules**:
  - Must be runnable. NO landing pages, waitlists, or "coming soon" links. If pre-launch, use "Launch HN:" via yclaunch, not Show HN.
  - Title format: `Show HN: <Name> – <concrete what-it-does>`. Under 60 chars. No marketing verbs.
  - No signup wall on the linked site.
  - HN readers aggressively downvote LLM-written copy. Write the title and first comment by hand.
  - Reply to every comment in the first 4 hours. Silence = dead post.
  - Resubmit allowed up to 2–3× if the first attempt got no traction. Email `hn@ycombinator.com` to request the second-chance pool.
- **Expected reach**: Front page = 10K–100K visitors. Median Show HN gets <50 points and fades in 12h.

### X / Twitter (via xmaster CLI)
- **URL template**: N/A (no URL pre-fill — use `xmaster post` via the xmaster skill)
- **Applies to**: all
- **Best time**: Tue–Wed 9–11 AM or 2–4 PM ET
- **Rules**:
  - Thread format: 4–8 tweets. Tweet #1 carries 90% of reach — hook with a specific number or visible result.
  - NO external link in tweet #1 (March 2026 algorithm penalty for non-Premium). Drop link in tweet #2 or pinned reply.
  - Video (30–90s loop) = 5× reach vs text; image = 4×; text = 1×.
  - Replies are weighted ~150× likes. Reply to every comment in the first hour.
  - Run `xmaster analyze "text"` before posting. Use the xmaster skill, don't reimplement.
- **Expected reach**: Varies by author follower count. Specific-number hooks + video = 10×–50× typical reach.

### LinkedIn
- **URL template**: `https://www.linkedin.com/feed/?shareActive=true&shareUrl={url}&text={text}`
- **Applies to**: saas, newsletter, mobile (B2B)
- **Best time**: Tue–Thu 8–10 AM ET or 12–2 PM ET
- **Rules**: Founder voice, first-person story. 1,200–1,500 chars sweet spot. Plain text beats design. No hashtag spam (3 max).

---

## Open source / Developer tools

### GitHub awesome lists (per-category)
- **URL template**: `https://github.com/{owner}/{repo}/issues/new?template={template}&title={title}&body={body}` (where template exists) OR fork + PR (where no template)
- **Applies to**: oss, cli, claude-plugin, ml
- **Rules**:
  - Read the list's `CONTRIBUTING.md` FIRST. Most have strict formatting (alphabetical, specific bullet shape, required description length).
  - Several lists (awesome-claude-code, awesome-selfhosted) **ban `gh` CLI / programmatic submissions** in their Code of Conduct. Use the pre-filled URL in a browser. Never `gh issue create` without reading the CoC.
  - Many require minimum repo age (1 week, 30 days) and min stars (often 100+).
  - PRs for non-`issue`-based lists: fork, add alphabetically, 60–120 char description, PR title `Add: <Name>`.
- **Specific lists to target**:
  - `awesome-claude-code` (hesreallyhim) — issue template submission
  - `awesome-selfhosted` — PR, strict quality bar
  - `awesome-cli-apps` — PR
  - `awesome-python`, `awesome-rust`, `awesome-go`, `awesome-nodejs` — language-specific
  - `awesome-mcp-servers` — MCP-specific
- **Expected reach**: 100–5,000 stars over 3–12 months (long tail)

### Dev.to
- **URL template**: `https://dev.to/new?prefill={markdown}` (supports URL-encoded markdown prefill)
- **Applies to**: oss, cli, saas technical launches
- **Rules**: Canonical URL metadata if cross-posting. Include code blocks + diagrams. 2–5 tags max. Post weekdays morning ET.
- **Expected reach**: 500–10K views per article. ~50 followers gained per strong article.

### Hashnode
- **URL template**: (login-required editor, no URL prefill)
- **Applies to**: oss, cli, saas technical
- **Rules**: Strong SEO indexing. Technical depth wins. Publish on your own blog subdomain for backlinks.

### Terminal Trove
- **URL template**: `https://terminaltrove.com/submit` (form)
- **Applies to**: cli only
- **Rules**: CLI must be documented, installable via standard package manager (brew, cargo, npm, pip).

### Reddit subs (OSS)
- `r/opensource` (210K) — 10% self-promo cap
- `r/programming` — strict no-promo in title, share for discussion only
- `r/selfhosted` — requires Docker Compose + docs
- `r/coolgithubprojects`
- `r/commandline`, `r/rust`, `r/golang`, `r/Python`, `r/javascript`

### Homebrew / package registries
- Submit formula PR to `homebrew-core` or create a tap under your org: `homebrew-tap` repo with a Formula directory.
- Rust: `cargo publish` to crates.io.
- Node: `npm publish` (verify scope).
- Python: `pypi.org` via `twine upload`.

---

## SaaS / Commercial

### Product Hunt
- **URL template**: `https://www.producthunt.com/posts/new` (login + multi-step form — no URL prefill)
- **Applies to**: saas, mobile, some oss with a paid tier
- **Best time**: Launch at **12:01 AM PT, Tue/Wed/Thu**. Avoid Friday/weekend/last-week-of-month.
- **Rules**:
  - 2026 update: 79% of featured and 60% of #1s are **self-hunted** — no hunter needed. If using one, they need a gold badge.
  - Tagline = one concrete sentence (max 60 chars). NOT "The X for Y".
  - First comment = founder story + why you built it + one open question. Ask for feedback, NOT upvotes (rule violation).
  - Assets: 1270×760 thumbnail, 3–5 gallery images, 30–60s demo video at top.
  - Need 200–400 upvotes in first 3 hours to hit Top 5.
  - Respond to every comment within 1 hour.
  - Prep 30 days in advance: notify followers, line up 10–20 supporters, have assets locked.
- **Expected reach**: Top-5 finish = 2K–10K visitors, 300–2,000 signups typical.

### BetaList
- **URL template**: `https://betalist.com/submit` (form)
- **Applies to**: saas (pre-launch only)
- **Rules**: Must be pre-launch with email capture. Free queue takes 2+ months. Expedited $129 = 3–4 days.
- **Expected reach**: 387–1,000 visitors, 46–300 beta signups.

### Uneed
- **URL template**: `https://www.uneed.best/submit` (form)
- **Applies to**: saas
- **Rules**: Weekly cohorts, Tier 1 = "big launcher". Feedback-oriented community.

### Fazier
- **URL template**: `https://fazier.com/submit` (form)
- **Applies to**: saas, ai tools
- **Rules**: Weekly launches, less noise than PH. Good for calm launches.

### MicroLaunch
- **URL template**: `https://microlaunch.net/submit` (form)
- **Applies to**: saas
- **Rules**: 1-month on directory, 50K monthly visitors, "Roasts/Boosts" feedback mechanic.

### Peerlist Spotlight
- **URL template**: `https://peerlist.io/scroll` (form after login)
- **Applies to**: saas, mobile, indie
- **Rules**: 188–209K MAU, capped at 50 products/week. Submit Monday for weekly spotlight.

### TinyLaunch
- **URL template**: `https://tinylaunch.com/submit` (form)
- **Applies to**: saas, indie tools
- **Rules**: Free weekly rounds, top-3 badge.

### Indie Hackers Milestones
- **URL template**: `https://www.indiehackers.com/milestones/new` (login)
- **Applies to**: saas (post-launch MRR/growth posts, NOT launch-day)
- **Rules**: Post real metrics. No marketing. Engage in forum daily.

### Reddit subs (SaaS)
- `r/SaaS` — metrics-first posts, not pitches
- `r/SideProject` — build-in-public story, screenshots, real numbers
- `r/microsaas` (50K) — promo-friendly
- `r/alphaandbetausers` — direct promo OK
- `r/IMadeThis`, `r/EntrepreneurRideAlong`, `r/startups`

---

## ML / AI models

### HuggingFace
- **URL template**: `https://huggingface.co/new` (login)
- **Applies to**: ml
- **Rules**:
  - YAML frontmatter is critical for discovery: `pipeline_tag`, `library_name`, `license`, `datasets`, tags.
  - Pair the model repo with a Space demo (gradio or streamlit).
  - Create a Collection for model variants (GGUF, MLX, original).
  - Model card sections: intended use, training data, evaluation, limitations, bias, environmental impact.
- **Expected reach**: Weekly "Trending" = 5K–50K views.

### Papers With Code
- **URL template**: `https://paperswithcode.com/add-paper` (login)
- **Applies to**: ml (if paper exists)
- **Rules**: arXiv link required. Link leaderboard + code. Re-submit when SOTA.

### Reddit subs (ML)
- `r/LocalLLaMA` — open-weights only. Include hardware (VRAM, tok/s on named GPU), quantizations, direct GGUF/safetensors links. No marketing. 10% self-promo cap.
- `r/MachineLearning` — use [P] (project), [R] (research), [N] (news) tags. Direct promo only in weekly [D] Self-Promotion Thread. Method + benchmarks vs baseline required.
- `r/StableDiffusion` — image gen models
- `r/Oobabooga`, `r/KoboldAI` — LLM UIs

### EleutherAI Discord / LAION Discord
- **Applies to**: research-oriented ML
- **Rules**: Share in `#share-your-work` channels after a few days of lurking.

---

## Claude Code plugins / AI agent plugins

### Anthropic official marketplace
- **URL template**: `https://platform.claude.com/plugins/submit` or `https://claude.ai/settings/plugins/submit`
- **Applies to**: claude-plugin
- **Rules**:
  - Repo must have `.claude-plugin/plugin.json` manifest at root.
  - `hooks/hooks.json` (if hook plugin) with correct event types.
  - Auto-review; "Anthropic Verified" badge available for vetted plugins.
  - Browse at `claude.com/plugins`.

### awesome-claude-code
- **URL template**: `https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml&title={title}&{fields}`
- **Applies to**: claude-plugin, skills
- **Rules**: CoC **explicitly bans** `gh` CLI / programmatic submissions — automatically closed. Open pre-filled URL in browser, tick confirmation boxes, submit manually.
- **Requirements**: Repo 1+ week old, public.

### claudemarketplaces.com
- **URL template**: PR to their marketplace.json (read their repo README)
- **Applies to**: claude-plugin

### aitmpl.com/plugins
- **URL template**: Form submission on the site
- **Applies to**: claude-plugin

### r/ClaudeAI
- **URL template**: `https://www.reddit.com/r/ClaudeAI/submit?title={title}&url={url}` or `?text={text}&selftext=true`
- **Applies to**: claude-plugin, skills, Claude Code workflows

---

## Mobile apps

### App Store / Google Play
- **URL template**: App Store Connect / Play Console (login)
- **Applies to**: mobile
- **Rules**: Apple reviews ~90% within 24h. April 2026 requires latest min SDK.

### TestFlight public link + departures.to
- **URL template**: TestFlight public link, submit at `https://departures.to/submit`
- **Applies to**: mobile (beta)

### Product Hunt "Apps" category
- Same as PH above with `topic=iphone` or `topic=android`.

### Reddit subs (mobile)
- `r/iosapps` (hook: screenshot-heavy)
- `r/androidapps`
- `r/iphone`, `r/iOSBeta`, `r/apple` (editorial standards high)

---

## Newsletters / content

### beehiiv Boosts & Recommendations
- **URL template**: In-app (login)
- **Applies to**: newsletter
- **Rules**: Paid Boosts for subscriber acquisition; free Recommendations for cross-promo with other publishers.

### Substack Notes & Discovery
- **URL template**: In-app
- **Applies to**: newsletter
- **Rules**: Notes feed is now the primary growth surface on Substack. Post 2–4 notes/week.

### Reddit subs (newsletter)
- `r/SubstackReads`, `r/newsletters`, `r/Substack`

### Dev.to / Hashnode cross-post
- Cross-post newsletter issues with canonical URL → SEO backlink to newsletter.

---

## Pre-fill URL templates (quick reference)

Plug values in directly. All parameters URL-encoded.

```
Show HN:       https://news.ycombinator.com/submitlink?u={url}&t={title}
Reddit:        https://www.reddit.com/r/{sub}/submit?title={title}&url={url}
Reddit text:   https://www.reddit.com/r/{sub}/submit?title={title}&text={text}&selftext=true
LinkedIn:      https://www.linkedin.com/feed/?shareActive=true&shareUrl={url}&text={text}
Dev.to:        https://dev.to/new?prefill={url_encoded_markdown}
Mastodon:      https://{instance}/share?text={text}
GH issue:      https://github.com/{owner}/{repo}/issues/new?template={template}&title={title}&{field}={value}
GH new repo:   https://github.com/new?name={name}&description={desc}&visibility=public
Email mailto:  mailto:?subject={subject}&body={body}
```

## Account / karma requirements (Reddit)

Most subs enforce minimums via automod. Typical thresholds:

| Sub | Account age | Comment karma | Post karma | Self-promo cap |
|-----|-------------|---------------|------------|----------------|
| r/SaaS | 30 days | 50 | 10 | 10% |
| r/SideProject | 7 days | 10 | — | 1 post/week |
| r/MachineLearning | 30 days | 100 | 10 | Weekly thread only |
| r/LocalLLaMA | 30 days | 50 | — | 10% |
| r/programming | 90 days | 300 | — | strict |
| r/selfhosted | 30 days | 50 | — | 10% |
| r/opensource | 30 days | 50 | — | 10% |
| r/ClaudeAI | 7 days | 10 | — | moderate |

Check sidebar / automod replies — requirements drift.
