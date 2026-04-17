# Email announcement — {{name}}

## Delegation

Send via **`email-cli`** (single recipient / personal list) or **`mailing-list-cli`** (broadcast to newsletter list).

```bash
# Single / small list
email-cli send --to addr --subject "..." --text "..." --json

# Broadcast via mailing-list-cli
mailing-list-cli broadcast create --name "..." --template <template> --to list:<name>
mailing-list-cli broadcast preview <id> --to test@example.com
# after user approves:
mailing-list-cli broadcast send <id>
```

## Subject

<!-- <50 chars, result-oriented, no emojis, lowercase optional -->

{{name}} is live — {{tagline}}

<!-- Alternatives:
- the thing I've been building is ready
- {{name}}: [specific concrete outcome]
-->

## Body

[1-sentence hook — same opener as your Show HN first comment]

[2–3 sentences: what it does and the specific problem it solves. No marketing verbs.]

[Specific ask: beta access / feedback call / early-access discount / just "check it out"]

{{url}}

[First name]

P.S. [Optional — one concrete stat or non-obvious detail that rewards the reader]

<!--
Length: max 150 words.
No images in the body (deliverability).
One primary CTA.
Send 9 AM ET on launch day.
-->

## Subject-line A/B options

If your list is >500, send A to half, B to the other:

A. {{name}} is live — {{tagline}}
B. [result-oriented] — e.g., "the thing that fixes [problem] is here"

Pick the winner for any future announcements.
