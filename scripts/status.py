#!/usr/bin/env python3
"""Show launch status and recommend next 1-3 actions.

Usage:
  status.py                           # List all launches
  status.py <slug>                    # Show one launch
  status.py <slug> --json             # JSON output for agent consumption
  status.py <slug> --mark <id>=<status> [--posted-url URL]
                                      # Update a channel's status
  status.py <slug> --schedule <id>=<ISO-timestamp>
                                      # Schedule a channel
  status.py <slug> --note "text"      # Append to launch notes
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone, date
from pathlib import Path

LAUNCHES_DIR = Path.home() / ".claude" / "launches"

STATUS_EMOJI = {
    "pending": "·",
    "scheduled": "…",
    "done": "✓",
    "skip": "—",
    "failed": "✗",
}

VALID_STATUSES = set(STATUS_EMOJI.keys())


def load_state(slug: str) -> dict:
    path = LAUNCHES_DIR / slug / "launch.json"
    if not path.exists():
        print(f"error: no launch found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def save_state(slug: str, state: dict) -> None:
    state["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    path = LAUNCHES_DIR / slug / "launch.json"
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def list_launches() -> list[dict]:
    if not LAUNCHES_DIR.exists():
        return []
    out = []
    for child in sorted(LAUNCHES_DIR.iterdir()):
        p = child / "launch.json"
        if p.exists():
            try:
                with open(p) as f:
                    s = json.load(f)
                counts = {"done": 0, "scheduled": 0, "pending": 0, "skip": 0, "failed": 0}
                for ch in s.get("channels", []):
                    counts[ch.get("status", "pending")] = counts.get(ch.get("status", "pending"), 0) + 1
                out.append({
                    "slug": s.get("slug"),
                    "name": s.get("name"),
                    "type": s.get("type"),
                    "launch_date": s.get("launch_date"),
                    "counts": counts,
                    "url": s.get("url"),
                })
            except Exception as e:
                out.append({"slug": child.name, "error": str(e)})
    return out


def days_to_launch(launch_date: str | None) -> int | None:
    if not launch_date:
        return None
    try:
        d = datetime.strptime(launch_date, "%Y-%m-%d").date()
        return (d - date.today()).days
    except Exception:
        return None


def next_actions(state: dict) -> list[str]:
    """Return up to 3 next actions based on state."""
    actions = []
    # Asset gaps
    if not state["assets"].get("og_image"):
        actions.append("Generate OG image (1200×630) — invoke canvas-design or chatgpt-image skill. Save to launches/<slug>/assets/og-image.png.")
    # Tagline / why story gaps
    if not state.get("tagline"):
        actions.append("Write tagline (<60 chars, no banned words — see references/content.md).")
    if not state.get("why_story"):
        actions.append("Write why-story (problem → incident → insight → solution, <150 words).")

    days = days_to_launch(state.get("launch_date"))
    copy_dir = LAUNCHES_DIR / state["slug"] / "copy"

    if days is None:
        actions.append(f"Set a launch_date in {LAUNCHES_DIR / state['slug'] / 'launch.json'} — Tue/Wed/Thu recommended.")

    if days is not None and days > 1:
        actions.append(f"T-{days}: review drafted copy in {copy_dir}/ and rewrite anything that sounds like AI. Read-aloud test each.")
        if days >= 7 and state["type"] == "saas":
            actions.append("Prep 20–30 supporters for Product Hunt launch (DM only — never public 'please upvote').")
    elif days == 1:
        actions.append("T-1: DM 5–10 friends privately with launch link + ask for feedback (not 'please upvote').")
        actions.append("T-1: run prefill_urls.py to generate tabs, dry-run open_tabs.py --only show-hn,x-thread.")
    elif days == 0:
        pending = [c for c in state["channels"] if c["status"] == "pending"]
        if pending:
            actions.append(f"Launch day: {len(pending)} channels pending. Run open_tabs.py {state['slug']}.")
        else:
            actions.append("Launch day: all channels addressed. Reply to every comment in <15min for first 6h.")
    elif days is not None and days < 0:
        # Post-launch
        elapsed = -days
        if elapsed == 1:
            actions.append("Day 2: retrospective tweet with real numbers (stars, signups, comments).")
            actions.append("Day 2: reply to every lingering HN/PH comment.")
        elif elapsed == 2:
            actions.append("Day 3: ship ONE bug fix from launch feedback. Tweet the diff.")
        elif 3 <= elapsed <= 4:
            actions.append(f"Day {elapsed+1}: dev.to / hashnode cross-post article. Reddit cross-post with different angle.")
        elif 5 <= elapsed <= 6:
            actions.append(f"Day {elapsed+1}: DM top 10 upvoters/commenters for 15-min feedback calls.")
        elif elapsed == 6:
            actions.append("Day 7: publish one-page retrospective (what worked / didn't / what's next).")
        else:
            # Long tail — recommend any pending channels as next actions
            pending = [c for c in state["channels"] if c["status"] == "pending"]
            if pending:
                actions.append(f"Long-tail: {pending[0]['platform']} still pending. Stagger remaining channels weekly.")

    # Pending channels always get one slot if we have room
    if len(actions) < 3:
        pending = [c for c in state["channels"] if c["status"] == "pending"]
        if pending:
            actions.append(f"Next channel to address: {pending[0]['platform']} ({pending[0]['id']}).")

    return actions[:3]


def render_human(state: dict) -> str:
    lines = []
    name = state.get("name", state["slug"])
    lines.append(f"▎ {name}  [{state['type']}]")
    if state.get("tagline"):
        lines.append(f"▎ {state['tagline']}")
    if state.get("url"):
        lines.append(f"▎ {state['url']}")
    ld = state.get("launch_date") or "(no date set)"
    dtl = days_to_launch(state.get("launch_date"))
    dtl_str = f"T{dtl:+d}" if dtl is not None else "T?"
    lines.append(f"▎ launch_date: {ld}  ({dtl_str})")
    lines.append("")
    # Counts
    counts = {s: 0 for s in VALID_STATUSES}
    for ch in state["channels"]:
        counts[ch["status"]] = counts.get(ch["status"], 0) + 1
    lines.append(f"  {counts['done']} done  ·  {counts['scheduled']} scheduled  ·  {counts['pending']} pending  ·  {counts['skip']} skip  ·  {counts['failed']} failed")
    lines.append("")
    # Channels
    lines.append("  channels:")
    for ch in state["channels"]:
        e = STATUS_EMOJI.get(ch["status"], "?")
        suffix = ""
        if ch.get("scheduled_for"):
            suffix = f"  [{ch['scheduled_for']}]"
        if ch.get("posted_url"):
            suffix = f"  {ch['posted_url']}"
        lines.append(f"  {e}  {ch['platform']:<40} {suffix}")
    lines.append("")
    # Next actions
    actions = next_actions(state)
    lines.append("  next:")
    for i, a in enumerate(actions, 1):
        lines.append(f"  {i}. {a}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug", nargs="?")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--mark", action="append", default=[], help="Set channel status, e.g. show-hn=done")
    parser.add_argument("--schedule", action="append", default=[], help="Schedule channel, e.g. show-hn=2026-04-22T16:00:00Z")
    parser.add_argument("--posted-url", help="Set posted_url on the last --mark'd channel")
    parser.add_argument("--note", help="Append a launch-level note")
    parser.add_argument("--set-asset", action="append", default=[], help="Set asset path, e.g. og_image=/path/to/img.png")
    parser.add_argument("--set-launch-date", help="Set launch_date YYYY-MM-DD")
    args = parser.parse_args()

    if not args.slug:
        launches = list_launches()
        if args.json:
            print(json.dumps(launches, indent=2))
        else:
            if not launches:
                print(f"no launches yet. run scripts/new_launch.py <slug> to create one.")
                return
            for l in launches:
                c = l.get("counts", {})
                dtl = days_to_launch(l.get("launch_date"))
                dtl_str = f"T{dtl:+d}" if dtl is not None else "T?"
                print(f"  {l.get('slug','?'):<24} {l.get('type','?'):<14} {dtl_str:<6} {c.get('done',0)}/{c.get('done',0)+c.get('pending',0)+c.get('scheduled',0)} done")
        return

    state = load_state(args.slug)
    mutated = False

    # Apply --schedule
    for sched in args.schedule:
        if "=" not in sched:
            print(f"error: --schedule expects id=timestamp, got {sched!r}", file=sys.stderr)
            sys.exit(1)
        cid, ts = sched.split("=", 1)
        for ch in state["channels"]:
            if ch["id"] == cid:
                ch["status"] = "scheduled"
                ch["scheduled_for"] = ts
                mutated = True

    # Apply --mark
    last_marked = None
    for mark in args.mark:
        if "=" not in mark:
            print(f"error: --mark expects id=status, got {mark!r}", file=sys.stderr)
            sys.exit(1)
        cid, status = mark.split("=", 1)
        if status not in VALID_STATUSES:
            print(f"error: invalid status {status!r}. Valid: {', '.join(VALID_STATUSES)}", file=sys.stderr)
            sys.exit(1)
        for ch in state["channels"]:
            if ch["id"] == cid:
                ch["status"] = status
                if status == "done":
                    ch["posted_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
                last_marked = ch
                mutated = True

    if args.posted_url and last_marked:
        last_marked["posted_url"] = args.posted_url

    if args.note:
        state.setdefault("notes", []).append({
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "text": args.note,
        })
        mutated = True

    if args.set_launch_date:
        state["launch_date"] = args.set_launch_date
        mutated = True

    for kv in args.set_asset:
        if "=" not in kv:
            continue
        k, v = kv.split("=", 1)
        state["assets"][k] = v
        mutated = True

    if mutated:
        save_state(args.slug, state)

    if args.json:
        print(json.dumps({
            "slug": state["slug"],
            "state": state,
            "next_actions": next_actions(state),
        }, indent=2))
    else:
        print(render_human(state))


if __name__ == "__main__":
    main()
