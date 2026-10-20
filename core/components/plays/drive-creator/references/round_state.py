#!/usr/bin/env python3
"""round_state.py — after a round of the drive's plays: done, again, or ask? (Shared Drive Run, R5)

A drive runs its plays "in order and repeatedly, until its intent is met" (glossary, Drive;
ADR 029). A question one play cannot answer is the drive's question, not a stop: the other
plays may answer it, and the play fills it on the next round (Kapil, 2026-10-20). The drive
asks the person only what no play of the drive can answer. This script makes that call after
each round, mechanically:

- **done** — no question is open: go on to the checker.
- **again** — something moved since the last round (the product model changed, or the open
  questions changed) and the round limit is not reached: run another round.
- **ask** — nothing moved (same model, same open questions), or the round limit is reached:
  the open questions are the drive's — ask the person, all at once, then run another round.

Open questions are read from two places in the issue's short-term memory:
- `<review_dir>/open-<play>.json` — what a play could not answer
  (`{"play", "round", "questions": [{"id", "ask", "blocks", "for_person", "examples"}]}`);
- `<issue_dir>/review/memory-updates/*.json` still `pending` — answers memory lacked, drafted
  for a person to approve (ADR 035 §5); they wait for that approval, never used before it.

    python3 round_state.py --round <n> --max-rounds <m> --working <working> \
        --review-dir <review_dir> --issue-dir <stm_base><issue>/ --model-path <product_base> \
        --out <working>/round-<n>.json

Writes `round-<n>.json` (`{round, decision, open, model, moved, why}`) and `rounds.json` (the
latest, with `open_left`). Exit 0 always when it could decide; 2 when an input cannot be read.
Reads files and one `git rev-parse`; writes only its two records. Standard library only.
"""
import argparse
import glob
import hashlib
import json
import os
import subprocess
import sys


def open_questions(review_dir, issue_dir):
    found = []
    for path in sorted(glob.glob(os.path.join(review_dir, "open-*.json"))):
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
        for q in doc.get("questions") or []:
            found.append({"from": doc.get("play") or os.path.basename(path)[5:-5],
                          "id": str(q.get("id")), "ask": str(q.get("ask", "")),
                          "for_person": bool(q.get("for_person", True))})
    for path in sorted(glob.glob(os.path.join(issue_dir, "review", "memory-updates", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            mu = json.load(fh)
        if str(mu.get("status", "pending")).lower() == "pending":
            found.append({"from": "memory-update", "id": str(mu.get("id") or os.path.basename(path)[:-5]),
                          "ask": str(mu.get("question") or mu.get("title") or ""), "for_person": True})
    return found


def model_hash(path):
    """The product model's tree in the last commit: it moves only when the model changed."""
    run = subprocess.run(["git", "rev-parse", f"HEAD:{path.rstrip('/')}"], capture_output=True, text=True)
    return run.stdout.strip() if run.returncode == 0 else "none"


def decide(rnd, max_rounds, open_now, model_now, last):
    if not open_now:
        return "done", "no question is open"
    if last is None:
        moved = True
    else:
        moved = model_now != last.get("model") or \
            sorted(q["id"] for q in open_now) != sorted(q["id"] for q in last.get("open", []))
    if rnd >= max_rounds:
        return "ask", f"the round limit ({max_rounds}) is reached with questions open"
    if not moved:
        return "ask", "a whole round answered nothing new: these questions are the drive's"
    return "again", "the model or the open questions moved — another round may answer more"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Decide the drive's next move after a round.")
    ap.add_argument("--round", required=True, type=int)
    ap.add_argument("--max-rounds", type=int, default=3)
    ap.add_argument("--working", required=True)
    ap.add_argument("--review-dir", required=True)
    ap.add_argument("--issue-dir", required=True)
    ap.add_argument("--model-path", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        open_now = open_questions(args.review_dir, args.issue_dir)
        last_path = os.path.join(args.working, f"round-{args.round - 1}.json")
        last = None
        if args.round > 1 and os.path.isfile(last_path):
            with open(last_path, encoding="utf-8") as fh:
                last = json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"round_state.py: cannot read an input: {exc}\n")
        return 2
    model_now = model_hash(args.model_path)
    decision, why = decide(args.round, args.max_rounds, open_now, model_now, last)
    record = {"round": args.round, "decision": decision, "why": why, "open": open_now,
              "model": model_now, "open_left": len(open_now),
              "fingerprint": hashlib.sha256(json.dumps([model_now, open_now], sort_keys=True).encode()).hexdigest()[:16]}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    for path in (args.out, os.path.join(args.working, "rounds.json")):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(record, fh, indent=2)
    print(json.dumps({k: record[k] for k in ("round", "decision", "why", "open_left")}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
