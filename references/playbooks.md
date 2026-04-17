# Per-product-type launch playbooks

Sequenced channel plans. Pick the matching playbook in `new_launch.py` via the `type` field. Each lists channels in recommended execution order.

---

## `oss` — Open source repo / library

**Goal**: GitHub stars, contributors, adoption.

### Pre-launch (T-7 to T-1)
1. README polish — delegate to `github-optimization` skill
2. OG image (1280×640) — delegate to `canvas-design` or `chatgpt-image`
3. Demo GIF in README (asciinema or terminalizer for CLI; screen recording for UI)
4. GitHub repo metadata: description, topics (14–20 relevant), homepage URL
5. Pin the repo on your profile
6. Tag a v1.0.0 release so GitHub Trending picks it up

### Launch day
1. **Show HN** — 8–10 AM ET, Tue–Thu. Title: `Show HN: <Name> – <what>`. First comment within 2 min.
2. **X thread** — 9–11 AM ET. Hook = specific number. Video or image. Link in tweet #2.
3. **r/SideProject** — 10 AM ET. Story + screenshots.
4. **r/opensource** — if broadly applicable. 10% promo cap; frame as "I made this".
5. **Niche sub** — one of: r/commandline (CLI), r/selfhosted (hostable), r/rust / r/golang / r/Python / r/javascript.
6. **Dev.to article** — "How I built X" or "The design choices behind X". Tag the repo.

### Long tail (weeks)
1. Awesome-list PRs — find 3–5 relevant `awesome-*` lists via `awesome.re`. Follow each CONTRIBUTING.md precisely.
2. Hashnode / Medium cross-post with canonical URL.
3. Submit to directories: `openalternative.co`, `beta.opengraph.dev`, `producthunt.com` (if applicable).
4. Sponsor / mention from related tools in your space (email the maintainers).

---

## `saas` — Commercial SaaS product

**Goal**: Signups, MRR, press, inbound.

### Pre-launch (T-30 to T-7)
1. **Build a waitlist** and pre-launch on BetaList ($129 expedited = 3–4 days) → ~500 signups baseline.
2. **Product Hunt prep** — 30 days out. Line up 20–30 supporters (not public upvote rings — real users). Ensure account + ship badges.
3. **Landing page** — delegate to `seo-geo-optimizer` for schema/metadata. OG image, Twitter card.
4. **Demo video** (30–60s, no voiceover needed) for PH + X.
5. **Newsletter audience** — grow from blog posts / waitlist.

### Launch day (PH primary)
1. **12:01 AM PT** — Product Hunt goes live. First comment within 2 min.
2. **6 AM PT** — email existing waitlist + newsletter (delegate to `email-cli` / `mailing-list-cli`).
3. **9 AM ET** — X thread with PH link in reply #2.
4. **10 AM ET** — r/SideProject (build-in-public framing) or r/SaaS (metrics framing).
5. **11 AM ET** — LinkedIn post, founder voice.
6. **Throughout day** — reply to every PH comment within 1h; DM hunter + top commenters.

### Post-launch (T+1 to T+30)
1. **BetaList** (if didn't pre-launch there)
2. **Uneed, Fazier, MicroLaunch, Peerlist, TinyLaunch** — stagger across weeks, one per week.
3. **Indie Hackers Milestones** — post first-month MRR.
4. **r/microsaas, r/alphaandbetausers, r/IMadeThis** — each with unique copy.
5. **Press pitch** — TechCrunch, The Information, niche press. Only if you have a hook (funding, 10x growth, novel tech).
6. **Podcast pitches** — find 5 podcasts in your space; pitch host personally.

---

## `ml` — ML model, dataset, or fine-tune

**Goal**: Downloads, citations, community adoption.

### Pre-launch
1. **HuggingFace model repo** — full YAML frontmatter (`pipeline_tag`, `library_name`, `license`, `datasets`, `tags`).
2. **Model card** — intended use, training data, evaluation, limitations, bias, environmental impact sections.
3. **Space demo** (gradio or streamlit) — people need to try it in one click.
4. **Quantized variants** — GGUF, MLX, GPTQ. Put them in a Collection.
5. **Benchmark table** vs named baselines. Reproducible eval code.
6. **arXiv paper** if research-oriented. Cross-post to Papers With Code.

### Launch day
1. **HuggingFace post** — tweet from the model card. Announce the Space.
2. **r/LocalLLaMA** — hardware specs (VRAM, tok/s), quant links, license. NO marketing.
3. **r/MachineLearning** — [P] or [R] tag. Method + benchmarks + code.
4. **X thread** — quote the main benchmark result with visual. Tag `@huggingface`.
5. **EleutherAI Discord `#share-your-work`** (after lurking a few days).

### Long tail
1. **Papers With Code** leaderboard
2. Integration PRs — llama.cpp, ollama, LM Studio presets, text-generation-webui.
3. Tutorials / fine-tuning notebook — as follow-up content.

---

## `claude-plugin` — Claude Code plugin / skill / hook

**Goal**: Installs, visibility within Claude Code community.

### Pre-launch
1. **Plugin manifest** — `.claude-plugin/plugin.json` at repo root with `name`, `description`, `version`, `author`, `repository`, `homepage`, `keywords`.
2. **Hook manifest** (if hook plugin) — `hooks/hooks.json` with correct event types (`Stop`, `SubagentStop`, `UserPromptSubmit`, etc.).
3. **README** with two install paths: (a) `/plugin marketplace add` + `/plugin install`, (b) manual copy-to-hooks.
4. **Demo GIF** showing Claude Code actually using the plugin.

### Launch day
1. **Anthropic marketplace** — submit at `platform.claude.com/plugins/submit` or `claude.ai/settings/plugins/submit`.
2. **Show HN** — technical angle (e.g., "how hooks actually work"). Tue–Thu 9 AM ET.
3. **awesome-claude-code** — pre-filled issue URL (never `gh` CLI — banned in CoC).
4. **r/ClaudeAI** — screenshot-driven, workflow framing.
5. **X** — tag `@bcherny`, `@AnthropicAI`. Ship video of Claude using the plugin.

### Long tail
1. `claudemarketplaces.com` PR
2. `aitmpl.com/plugins` submission
3. Dev.to article — "Every Claude Code Stop hook gotcha I hit"

---

## `cli` — Command-line tool

**Goal**: Installs, GitHub stars, package registry presence.

### Pre-launch
1. Publish to registries: `cargo publish` / `npm publish` / `pypi` / homebrew formula or tap.
2. `asciinema` or `terminalizer` GIF in README.
3. `--help` clean and complete.
4. Installation via ONE command (brew/cargo/curl installer) top of README.
5. `agent-info` JSON capability manifest (if agent-facing — see `agent-cli-framework` skill).

### Launch day
1. **Show HN** — prime channel for CLIs. "Show HN: X – human-friendly Y"
2. **Terminal Trove** submission (`terminaltrove.com/submit`).
3. **r/commandline** + **r/coolgithubprojects**.
4. **Language sub**: r/rust, r/golang, r/Python, r/javascript.
5. **X thread** with asciinema loop.
6. **dev.to** — "Building a CLI in <lang> — lessons learned"

### Long tail
1. Homebrew-core PR (once you have 100+ stars and 30 days of stable releases).
2. Awesome lists for CLI tools.
3. Package manager categories (brew tap listings).

---

## `mobile` — iOS or Android app

**Goal**: Downloads, App Store featuring, revenue.

### Pre-launch (T-30 to T-1)
1. App Store Connect metadata — screenshots, keywords (100 char limit), description, subtitle.
2. TestFlight public link (iOS) or Google Play internal testing track.
3. **departures.to** — submit TestFlight for beta testers (weeks before launch).
4. Press kit with mockups, app icon PSD, screenshots at every device size.
5. App Store **featuring nomination** via Apple form (Google Play equivalent).
6. Feature video / App Preview (30s, vertical).

### Launch day
1. **Product Hunt Apps category** — 12:01 AM PT launch.
2. **r/iosapps** / **r/androidapps** — screenshot-heavy post.
3. **r/iphone**, **r/apple**, **r/iOSBeta** — only if TestFlight still open or genuinely relevant.
4. **X thread** with 30s vertical video.
5. **LinkedIn** — for B2B apps, founder angle.

### Long tail
1. **App Store Optimization** — delegate to `app-store-connect` skill.
2. Featuring pitch to editorial teams (Apple Design Awards, etc. — niche, use if genuinely world-class UX).
3. **Chinese markets** — Xiaohongshu / WeChat / Weibo have separate launch mechanics.

---

## `newsletter` — Newsletter / content product

**Goal**: Subscribers, opens, paid conversion.

### Pre-launch
1. 3–5 issues already published publicly (ideal archive).
2. Sample issue as the "why subscribe" proof.
3. Welcome sequence (first 3 emails).
4. Landing page with preview + signup.

### Launch day
1. **beehiiv Recommendations** — set up cross-promo with 5–10 similar-topic newsletters.
2. **Substack Notes** (if on Substack) — 4–6 notes drawing traffic to the sub page.
3. **r/SubstackReads**, **r/newsletters**.
4. **X thread** — "Why I'm writing about X. First 3 issues live."
5. **Dev.to / Hashnode** cross-post of best issue with canonical URL back to newsletter.
6. LinkedIn post for B2B / professional-topic newsletters.

### Long tail
1. **beehiiv Boosts** (paid subscriber acquisition) once budget allows.
2. Podcast guest appearances in your topic area.
3. Collaborative issues (swap with another newsletter).
4. Pitch sponsor section to relevant tools.

---

## Decision tree when the type is ambiguous

Ask the user:

1. **Does it have a paid tier?** Yes → `saas`. No → keep asking.
2. **Is the source code public on GitHub?** Yes → `oss` or `cli` (CLI if it's a command).
3. **Does it produce AI outputs from user prompts?** Yes → likely `ml` (if model) or `saas` (if product wrapping models).
4. **Is it a file that goes in `~/.claude/plugins/` or `.claude-plugin/`?** Yes → `claude-plugin`.
5. **Does it go in an App Store?** Yes → `mobile`.
6. **Is it primarily email-delivered content?** Yes → `newsletter`.

Most projects map cleanly. Rare cases (e.g., "an OSS CLI with a paid cloud tier") → run `oss` playbook first, add `saas` PH launch at month 3.
