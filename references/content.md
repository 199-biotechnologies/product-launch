# Launch Content Playbook

Copy patterns that convert in 2026. Enforce the ban list on every draft.

## Anti-AI-slop ban list (enforce on every draft)

These words/phrases kill conversion because readers associate them with LLM-written marketing. On HN, they trigger active downvoting.

**Banned verbs**: delve, leverage, utilize, harness, unleash, empower, elevate, streamline, unlock, optimize, facilitate, commence, indicate (as "this indicates"), underscore.

**Banned adjectives**: seamless, robust, holistic, comprehensive, multifaceted, innovative, cutting-edge, state-of-the-art, game-changer, game-changing, revolutionary, transformative, pivotal, crucial (when not actually crucial), paramount.

**Banned nouns**: tapestry, landscape (metaphorical), ecosystem (when just "tools"), paradigm, synergy, solution (as in "our solution is"), offering.

**Banned transitions**: furthermore, moreover, consequently, additionally, importantly, it's important to note, it's worth noting, in conclusion, in summary.

**Banned phrases**: "In today's fast-paced world", "Whether you're X or Y", "Look no further", "Dive into", "Embark on", "Navigate the", "Power of", "The best X", "In the world of X".

**Replacements**:

| Banned | Use instead |
|--------|-------------|
| leverage / utilize | use |
| facilitate | help |
| optimize | speed up / shrink |
| implementation | setup / install |
| comprehensive | covers X, Y, Z (be specific) |
| seamless | "no config", "one command" |
| innovative | a new X / specific mechanism |
| game-changer | say what actually changed |
| empower users to | let you |
| at your fingertips | delete — never reads naturally |

**Read-aloud test**: If it sounds like a press release, cut it. Real people contract, repeat, fragment. "It's fast." beats "It demonstrates exceptional performance characteristics."

**Sentence variety**: Aggressively vary length. One short. Then a longer one that builds context. Then another short punch. Three sentences of the same length = AI-smelling.

**One concrete number per paragraph**. "60 lines of bash", "5ms overhead", "installs in 2 commands" — beats "lightweight and efficient".

---

## Hook patterns that work in 2026

### The "concrete result" hook
> "I shipped 47 commits yesterday. My GitHub graph showed 2. So I built this."

### The "incident" hook
> "Looked at my contribution graph this morning. Gray. Despite pair-coding with Claude for 8 hours yesterday."

### The "technical reveal" hook
> "Spent 3 days wondering why my Claude Code hook did nothing. The field I was using (additionalContext) is silently dropped for Stop hooks. Documented mechanism is exit 2 + stderr."

### The "anti-pattern" hook
> "Stop writing bash hooks that run `git commit` directly. You want to nudge Claude to commit, not commit for it — then the model writes the message."

### The "before/after" hook
> "Before: 2 commits per day. After this hook: 47. Same amount of work."

**Avoid**: "Introducing X", "I'm excited to announce", "Thrilled to share". Skip all preamble — start with the result.

---

## Per-channel copy templates

### Show HN title (under 60 chars)

Formula: `Show HN: <Name> – <concrete what-it-does-one-line>`

✅ Good:
- `Show HN: Commitmaxxing – a Claude Code hook that nudges granular commits`
- `Show HN: Halloy – modern IRC client`
- `Show HN: Doggo – human-friendly DNS client for the CLI`

❌ Bad:
- `Show HN: The future of version control is here` (marketing)
- `Show HN: Commitmaxxing v1.2.0 – release announcement` (version spam)
- `Show HN: I built a REVOLUTIONARY tool 🚀` (emojis + caps)

### Show HN first comment (post within 2 min of submission)

Structure: **What + Why + One technical detail + One question**

```
Author here. Built this after <one-line specific trigger>.

<Technical paragraph — what it does, how it's different. One non-obvious detail that shows you understand the problem space.>

<Constraint / limitation you haven't solved yet — honesty performs.>

Happy to answer questions about <specific topic>.
```

Length: 80–200 words. No marketing verbs. Zero emojis. First-person.

### Product Hunt tagline (60 chars max)

Formula: `<Verb> <what> <how or modifier>`

✅ Good:
- `Schedule Slack messages in advance`
- `AI-powered transcripts for any YouTube video`
- `Nudges Claude Code to commit after every turn`

❌ Bad:
- `The next generation of productivity` (vague)
- `Revolutionary new way to manage tasks` (banned words)

### Product Hunt first comment

```
Hey Product Hunt! Maker here.

<1 paragraph: the incident / problem that made you build this.>

<1 paragraph: what it does, 3 specific features. Concrete, not abstract.>

<1 paragraph: what's next / what you're figuring out.>

Would love feedback on <specific open question>. What would make this useful for your workflow?
```

350–500 words. Ask for feedback, NOT upvotes (rule). Respond to every comment within 1h for first 8h.

### Reddit r/SideProject

Title: `[I built] <thing that does concrete action> — here's what broke` OR `Shipped <thing>. <specific number> in <timeframe>.`

Body (300–500 words):
1. One-paragraph what/why
2. One paragraph on the hardest thing to get right (technical or UX)
3. Real numbers if you have them (users, MRR, downloads — don't make up)
4. Screenshot / demo gif
5. Direct link at the bottom

### Reddit r/SaaS

Title: `How I <specific metric result> in <timeframe>` OR `<specific price/tier decision> — here's what happened`

Body: Metrics-first. CAC, churn, pricing experiments. No pure pitches — they get buried. Share the ugly numbers too.

### Reddit r/MachineLearning

Title: `[P] <thing you built>` or `[R] <research>` or `[N] <news>`

Body: Lead with method, not outcome. Benchmark vs named baseline. Reproducible code link. NO marketing language whatsoever — instant downvote fuel. Direct model weights link.

### Reddit r/LocalLLaMA

Title: `<model name> — <what it does> (<size>, <license>)`

Body: Hardware specs (VRAM, tok/s on M3/4090/etc.), quantization variants, direct GGUF/safetensors links. Self-promo cap ~10%. Proprietary-only releases get downvoted hard.

### Reddit r/ClaudeAI

Title: `<specific use case or problem>` — matter-of-fact, not hypey

Body: Show workflow/screenshot, explain setup. Installation snippet for plugins. Mention version.

### Reddit r/selfhosted

Title: `<Project>: <what it does> (selfhosted alternative to <named SaaS>)`

Body: Docker Compose snippet required. List features. Resource requirements (RAM/disk). Backup story.

### X launch thread (4–8 tweets)

```
1/ <Specific number or visible result hook>. No link in this tweet.

So I built <Name>.

2/ <What happened before — the problem specifically.>

<Link to repo/site>

3/ <Technical detail or non-obvious insight.>

4/ <Limitation / what you haven't solved.>

5/ <CTA to reply, not click>. What's your workflow for X?
```

Rules:
- NO external link in tweet #1 (algorithm penalty).
- Attach video (30–90s loop) or image — 4–5× reach vs text.
- Post Tue/Wed 9–11 AM ET.
- Reply to every comment in first 60 min — replies are weighted ~150× likes.

### README hero block

```markdown
<!-- HERO -->
<div align="center">
  <img src="assets/og-image.png" alt="<Name> hero" width="800">
  
  <h1><Name></h1>
  <p><strong><One-line value prop, concrete.></strong></p>
  
  <a href="#quickstart"><img src="https://img.shields.io/badge/install-2_commands-black?style=for-the-badge"></a>
  <img src="https://img.shields.io/github/stars/{owner}/{repo}?style=for-the-badge">
  <img src="https://img.shields.io/github/license/{owner}/{repo}?style=for-the-badge">
</div>

## Quickstart

```bash
<install command 1>
<install command 2>
```

<1-sentence what happens next>.
```

Then: Why → Features → Docs link → Contributing → License. Order matters.

### Launch announcement email (to existing list)

Subject: `<Result-oriented, <50 chars>` — e.g., `Commitmaxxing is live — your contribution graph is about to change`

Body:
```
<1-sentence hook — same as your Show HN first comment's opener>

<2–3 sentences on what it does and why you built it.>

<Specific ask or offer — beta access, feedback call, discount>

<Link>

<Sign-off first-name>
```

Max 150 words. No images in the body (deliverability). One primary CTA.

### Awesome-list issue body

```markdown
### Resource name
<Name>

### Resource URL
<URL>

### Category
<Category from the list's README>

### One-line description
<60–120 chars, matching the list's style exactly>

### Why this belongs on the list
<1–2 sentences on what's unique, what problem it solves.>

### Confirmations
- [x] I read CONTRIBUTING.md
- [x] I checked this isn't already on the list
- [x] The resource is public and documented
- [x] I'm not using CLI/automation to submit (per CoC)
```

---

## Branding quick wins (for solo founders)

- **2 colors + 1 neutral**, 2 fonts, one mark that reads at 16px favicon
- **OG image**: 1200×630 PNG universal; **Twitter large card**: 1200×675
- Put the product name + 1-line promise on the OG image in 48px+ text
- Favicon + app icon + 400×400 avatar — same mark, same bg color
- 2026 palette trends: jade/teal + cream; plum + persimmon accent; graphite + electric green

Delegate to `canvas-design` or `chatgpt-image` skill for asset generation. Delegate to `design-identity` for brand extraction from a URL.

---

## Launch-day sequencing (one-day wave)

1. **T-7 days** — teaser on X, waitlist live, README polished, OG image up.
2. **T-1 day** — DM 5–10 friends with the launch link (private, not public "please upvote").
3. **12:01 AM PT** — Product Hunt goes live (if saas/mobile).
4. **6 AM PT / 9 AM ET** — post Show HN (if oss/cli/plugin). Different hook from PH tagline.
5. **9 AM ET** — X thread. Drop PH/HN link in reply #2.
6. **10–11 AM ET** — r/SideProject (+ niche sub like r/LocalLLaMA/r/ClaudeAI/r/SaaS — only one primary promo sub, not all).
7. **1 PM ET** — LinkedIn post (founder voice, if B2B relevant).
8. **Rolling** — reply to every comment in <15 min for first 6 hours. Then hourly for next 24h.

## Day 2–7 follow-through

- **Day 2** — retrospective tweet with real numbers (stars, signups, MRR).
- **Day 3** — ship one bug fix from feedback; tweet the diff.
- **Day 4** — reply to every lingering comment. If Show HN <10 points, consider 2nd-chance pool.
- **Day 5** — DM top 10 upvoters/commenters for 15-min feedback calls.
- **Day 6** — publish public roadmap based on themes.
- **Day 7** — one-page retro post ("what worked, what didn't, what's next").

Negative feedback: acknowledge in <2h, never delete, never argue. "You're right, here's what we'll do" beats defense every time.
