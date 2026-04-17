# Contributing

Thanks for wanting to make this better. PRs are welcome.

## Where to contribute

Three high-leverage areas:

1. **New platform specs** — `references/platforms.md`. Add a platform with URL template, rules, timing, reach, and CoC notes. Follow the existing format.
2. **New channel copy templates** — `templates/<channel>.md`. Use `{{name}}`, `{{tagline}}`, `{{url}}`, `{{why_story}}`, `{{author.github}}`, `{{author.x_handle}}` as variables. Include a brief HTML comment explaining the channel's voice.
3. **New form schemas** — `scripts/form_schema.py`. Add a `channel_id` branch that returns `fields[]`, `assets_required[]`, `pre_submit_checklist[]`, `post_submit_actions[]`, and `human_review_required_before_submit`.

## Quick start

```bash
git clone https://github.com/199-biotechnologies/product-launch.git
cd product-launch
# Run the scripts against a test launch:
python3 scripts/new_launch.py --json-input - test << EOF
{"name":"Test","type":"oss","tagline":"demo","url":"https://example.com","author_name":"You","author_github":"you"}
EOF
python3 scripts/status.py test
python3 scripts/form_schema.py test --channel show-hn
```

## Ground rules

- **Python stdlib only.** No pip dependencies. Keeps install to `git clone`.
- **Respect platform CoCs.** If a platform bans CLI submission, the skill must use a pre-filled URL path, not automate it. Flag this in the platform's notes.
- **No auto-submit of public content.** Pre-fill forms; humans click submit. Exceptions: X (via `xmaster analyze` gate), email (via `email-cli` after user approval).
- **Anti-AI-slop.** Templates must pass the ban list in `references/content.md`. No "leverage", "seamless", "game-changer".
- **Reference real sources.** When adding rules for a platform, cite where the rule comes from (docs URL, CoC link, or a dated X post).

## Testing

No formal test suite yet. Before opening a PR:

```bash
# Smoke-test every script with a fresh test launch
python3 scripts/new_launch.py --json-input - smoke --force < test.json
python3 scripts/status.py smoke
python3 scripts/prefill_urls.py smoke --json | python3 -m json.tool
python3 scripts/form_schema.py smoke --json | python3 -m json.tool
python3 scripts/agent_info.py | python3 -m json.tool
rm -rf ~/.claude/launches/smoke
```

All commands should exit 0 with valid JSON.

## PR checklist

- [ ] Commit message describes the why, not just the what
- [ ] No new pip dependencies
- [ ] Platform specs cite a source
- [ ] Templates pass the anti-AI-slop ban list
- [ ] Smoke tests above pass locally
- [ ] No breaking changes to existing `scripts/*.py` output schemas (agents depend on these)

## License

By contributing, you agree your contributions will be licensed under MIT.
