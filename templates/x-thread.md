# X / Twitter launch thread — {{name}}

## Delegation note

**Post via `xmaster` skill, not pasted into web.** Run this sequence:

```bash
# 1. Analyze the first tweet for algorithm score
xmaster analyze "<tweet 1 text>" --goal replies --json

# 2. Show user score + text; wait for explicit approval
# 3. Post
xmaster post "<tweet 1 text>" --json
# 4. Reply-chain the rest with --reply-to <last-id>
```

## Tweet 1 (hook, NO external link)

<!--
Tweet 1 carries 90% of reach. March 2026 algorithm penalizes external links in tweet #1.
Hook = specific number or visible result. No URL.
-->

[Specific number / result / before-after image].

So I built {{name}}.

## Tweet 2 (link + what)

{{tagline}}

{{url}}

## Tweet 3 (technical detail / how it works)

[One non-obvious detail. Shows depth without jargon.]

## Tweet 4 (limitation / what you haven't solved)

[Honest constraint. Performs better than polish.]

## Tweet 5 (CTA — reply, not click)

What's your workflow for [the problem {{name}} addresses]?

## Media

- Attach video (30–90s loop, silent-first, captioned) = 5× reach
- Or image = 4× reach
- Text-only = 1× reach

## Timing

Tue/Wed 9–11 AM ET or 2–4 PM ET.
Reply to every comment in the first 60 min.

## Pre-post checklist

- [ ] `xmaster config set style.voice` matches this voice
- [ ] `xmaster analyze` score ≥ B
- [ ] Media attached
- [ ] First-hour calendar blocked for replies
- [ ] Pin this thread to profile after posting
