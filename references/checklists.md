# Launch checklists

Use these to keep the ADHD operator on track. `status.py` surfaces the next 1–3 items each session.

## Pre-launch (T-14 to T-1)

### Assets
- [ ] OG image at `assets/og-image.png` — 1200×630 PNG
- [ ] Twitter card image — 1200×675 PNG
- [ ] Demo video (30–90s loop, no voiceover OK) — MP4
- [ ] Demo GIF for README — <5MB, <30s
- [ ] Logo / icon — 256×256 PNG + 1024×1024 PNG
- [ ] Favicon — 32×32 and 180×180 ICO/PNG

### Repo / landing page (OSS)
- [ ] README has 3-command Quickstart above the fold
- [ ] README has hero image/GIF
- [ ] GitHub description: 1 concrete sentence, keyword-rich
- [ ] GitHub topics: 14–20 relevant (max 20 allowed)
- [ ] Repo pinned on profile
- [ ] v1.0.0 tagged release (for GitHub Trending)
- [ ] LICENSE file (MIT / Apache2 / BSD standard)
- [ ] `CONTRIBUTING.md` with quickstart for contributors

### Landing page (SaaS)
- [ ] OG / Twitter meta tags set
- [ ] Schema.org markup (Organization, Product) — delegate to `seo-geo-optimizer`
- [ ] Canonical URL set
- [ ] Favicon + apple-touch-icon
- [ ] Demo video top of page
- [ ] Social proof section (users, quotes, numbers)
- [ ] One primary CTA above the fold
- [ ] Signup flow tested on mobile

### ML model
- [ ] HuggingFace model card with complete YAML frontmatter
- [ ] Space demo running (test with 3 different inputs)
- [ ] Quantized variants uploaded (GGUF + original at minimum)
- [ ] Benchmark table vs named baselines
- [ ] License clearly stated
- [ ] Training data source disclosed

### Claude Code plugin
- [ ] `.claude-plugin/plugin.json` at root
- [ ] `hooks/hooks.json` (if hook plugin)
- [ ] Install works via `/plugin marketplace add` + `/plugin install` in a fresh Claude Code session (tested)
- [ ] Manual install fallback documented in README

### Mobile app
- [ ] App Store Connect / Play Console metadata complete
- [ ] Screenshots for every required device size
- [ ] Keywords (100 char limit) optimized
- [ ] TestFlight / Play Internal testing link live
- [ ] App Preview video (30s vertical)
- [ ] Privacy policy URL
- [ ] App Store featuring nomination submitted

### Copy
- [ ] Show HN title drafted and under 60 chars (if applicable)
- [ ] Show HN first comment drafted, under 200 words
- [ ] Product Hunt tagline under 60 chars, no banned words
- [ ] Product Hunt first comment drafted (350–500 words)
- [ ] X thread drafted (4–8 tweets), no link in tweet #1
- [ ] Reddit post(s) drafted per target sub
- [ ] Email announcement drafted, <150 words
- [ ] Newsletter broadcast drafted (if list exists)
- [ ] All copy passed anti-AI-slop ban list

### Distribution setup
- [ ] 5–10 friends DMed privately with launch link + ask for feedback (NOT "please upvote")
- [ ] Existing newsletter list identified (`mailing-list-cli list ls`)
- [ ] xmaster configured — style.voice set (`xmaster config set style.voice "..."`)
- [ ] Hunter lined up (PH, optional; 79% of launches now self-hunted)

---

## Launch day

### Timing (for US / global launches)

| Time (ET) | Action |
|-----------|--------|
| 12:01 AM PT (3:01 AM ET) | Product Hunt goes live (if applicable) |
| 6 AM PT (9 AM ET) | Send launch email to existing list |
| 9 AM ET | Show HN submission |
| 9:15 AM ET | X thread (link in reply #2) |
| 10 AM ET | Reddit: primary sub (pick ONE — r/SideProject or niche) |
| 11 AM ET | LinkedIn post (if B2B relevant) |
| 1 PM ET | Second Reddit sub (different angle) — only if first is getting traction |
| Throughout | Reply to every comment in <15 min for first 6h |

### Execution
- [ ] Status check: `status.py <slug>` — confirm all "pending" channels ready
- [ ] Run `open_tabs.py <slug>` at 8:55 AM ET to queue browser
- [ ] Submit PH first (if applicable)
- [ ] Submit HN — check title one last time
- [ ] Post first comment on HN within 2 min of submission
- [ ] Post X thread; immediately pin to profile
- [ ] Post on r/SideProject (or primary sub)
- [ ] Mark channels done in status.py as you go
- [ ] Keep a text file of commenters + topics for thank-yous

### Anti-patterns (never do)
- ❌ Post on 5+ subs in parallel — looks spammy, gets removed
- ❌ Tweet "please upvote my HN" publicly — ring detection → shadowban
- ❌ Use identical copy across subs — Reddit cross-post filter
- ❌ Copy-paste AI-sounding marketing language — instant HN/Reddit downvotes
- ❌ Ignore negative comments — silence looks worse than engagement
- ❌ Launch on Friday, weekend, last week of month — dead zones

---

## Day 2

- [ ] Retrospective tweet with real numbers (stars, signups, comments, MRR if applicable)
- [ ] Reply to every remaining Show HN / PH comment
- [ ] Thank top 5 supporters by name on X
- [ ] Screenshot top Reddit comments → save for future content
- [ ] Update README if launch feedback revealed quick confusion points

## Day 3

- [ ] Ship ONE bug fix or quick feature from feedback (any, even small). Tweet the diff.
- [ ] Check if Show HN is dead (<10 points). If so, consider second-chance pool via `hn@ycombinator.com`.
- [ ] Submit to second-tier directories (Uneed, Fazier, MicroLaunch) — one per day, not all at once.
- [ ] Post on a second Reddit sub with different angle / fresh copy.

## Day 4

- [ ] Reply to every lingering comment (HN, PH, Reddit, X)
- [ ] Dev.to / Hashnode cross-post article ("How I built X")
- [ ] Email top commenters for 15-min feedback calls (3–5 calls)

## Day 5

- [ ] Run feedback calls; take notes on common themes
- [ ] Submit to one awesome-* list (if applicable) via pre-filled URL
- [ ] First round of "X used by Y company" social proof if you have it

## Day 6

- [ ] Publish public roadmap based on feedback themes (GitHub Projects / Notion)
- [ ] Re-engage supporters — "Here's what you're helping build" email

## Day 7

- [ ] One-page retrospective post ("What worked, what didn't, what's next")
  - Real numbers
  - Traffic by channel
  - Top feedback themes
  - Roadmap link
- [ ] Schedule day-14 and day-30 check-ins

## Week 2–4

- [ ] Indie Hackers Milestones (if SaaS) — first MRR / metric post
- [ ] Pitch 3 podcast hosts in your topic area
- [ ] Reach out to 5 related tool authors — ask for a cross-mention
- [ ] Weekly progress update (X, newsletter, or both)
- [ ] Start collecting user testimonials for landing page

## Month 2–3

- [ ] Press pitch (only if you have a real hook — funding, 10× growth, novel tech)
- [ ] Collab issue with a similar-audience newsletter (newsletter type)
- [ ] v1.1 release → second launch on PH (allowed 6 months after first; requires substantial update)
