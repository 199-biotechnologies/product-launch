# Dev.to article — {{name}}

## Title

<!-- Good formats:
- How I built {{name}} in [X time/lines]
- The [specific design choice] behind {{name}}
- Building {{name}}: what I got wrong the first time
- [Specific tech problem] — how {{name}} solves it
Avoid: "Introducing X", "Announcing X"
-->

How I built {{name}}: {{tagline}}

## Front matter

```yaml
---
title: How I built {{name}}: {{tagline}}
published: false        # flip to true when ready
tags: [tag1, tag2, tag3, tag4]  # max 4
cover_image: https://raw.githubusercontent.com/{{author.github}}/{{slug}}/main/assets/og-image.png
canonical_url: {{url}}
---
```

## Article skeleton

### The problem

[2–3 paragraphs. Specific incident/pain. Concrete details. Avoid abstract framing.]

### What I tried first

[What naive solution did you build first? Why didn't it work? Show code or config — makes this real.]

### The insight

[The non-obvious thing you figured out. This is the takeaway readers share with coworkers.]

### How {{name}} works

[Code snippets. Architecture. Trade-offs. 3–5 subsections.]

```[lang]
# Show code, not just describe it
```

### What I'd do differently

[Honest retrospective. Builds credibility.]

### Try it

[Direct install instructions — copy-pasteable commands]

```bash
[install command]
```

→ Repo: {{url}}

### Questions I'm still figuring out

[Open problems. Invites comments. Drives engagement.]

## Publishing checklist

- [ ] `canonical_url` set to your own site if cross-posting (SEO)
- [ ] 4 tags, relevant and trending
- [ ] Cover image set (1000×420 PNG)
- [ ] Code blocks have language tags
- [ ] Internal TOC if >1500 words
- [ ] Published Tue/Wed/Thu morning ET

## Expected reach

500–10K views per strong article. ~50 followers gained per post.
Dev.to indexes fast — Google traffic kicks in within 48h.
