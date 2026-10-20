#!/usr/bin/env python3
"""record_review.py — record the person's reply to the brief (Shared Drive Run, R5b).

The drive shows the brief /review-knowledge wrote and waits for the person's typed reply:
"yes" (take every proposal and every recommendation), or corrections to some gaps and pages.
The drive writes that reply as review.json; this script checks it covers the whole brief and
records the answers in the issue's short-term memory, so the next round's plays read them.

    python3 record_review.py --brief <working>/brief.json --reply <working>/review.json \
        --issue-dir <stm_base><issue>/ --round <n> --out <working>/review-record.json

review.json:
  {"words": "<the person's reply, verbatim>",
   "gaps": {"G1": "accept" | {"answer": "<the person's own answer>"}},
   "pages": {"<memory update id>": "approve" | "reject"}}
  A bare "yes" is written as every gap "accept" and every page its recommendation.

Writes `<issue-dir>/review/drive/person-answers-round-<n>.json`
`[{"gap", "theme", "answer", "accepted_proposal": bool, "from": "person", "words"}]` and
lists, in the record, each page's decision for the memory tool's `decide` (ADR 041 §8).
Exit 0 recorded; 1 the reply leaves a gap or page undecided; 2 cannot read an input.
Standard library only.
"""
import argparse
import json
import os
import sys


def record(brief, reply):
    problems, answers, decisions = [], [], []
    words = str(reply.get("words") or "").strip()
    if not words:
        problems.append("the reply has no `words` (the person's reply, verbatim)")
    rgaps = reply.get("gaps") or {}
    for g in brief.get("gaps") or []:
        gid = g.get("id")
        r = rgaps.get(gid)
        if r == "accept":
            answers.append({"gap": gid, "theme": g.get("theme"), "answer": g.get("proposal"),
                            "accepted_proposal": True, "from": "person", "words": words})
        elif isinstance(r, dict) and str(r.get("answer") or "").strip():
            answers.append({"gap": gid, "theme": g.get("theme"), "answer": r["answer"],
                            "accepted_proposal": False, "from": "person", "words": words})
        else:
            problems.append(f"gap {gid}: no decision (accept, or the person's own answer)")
    rpages = reply.get("pages") or {}
    for p in brief.get("pages") or []:
        uid = str(p.get("update"))
        d = rpages.get(uid)
        if d in ("approve", "reject"):
            decisions.append({"update": uid, "decision": d, "decided_in": "session", "words": words})
        else:
            problems.append(f"page {uid}: no decision (approve or reject)")
    return problems, answers, decisions


def main(argv=None):
    ap = argparse.ArgumentParser(description="Record the person's reply to the brief.")
    ap.add_argument("--brief", required=True)
    ap.add_argument("--reply", required=True)
    ap.add_argument("--issue-dir", required=True)
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.brief, encoding="utf-8") as fh:
            brief = json.load(fh)
        with open(args.reply, encoding="utf-8") as fh:
            reply = json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"record_review.py: cannot read an input: {exc}\n")
        return 2
    problems, answers, decisions = record(brief, reply)
    report = {"ok": not problems, "problems": problems, "answers": len(answers),
              "page_decisions": decisions}
    if not problems:
        dest = os.path.join(args.issue_dir, "review", "drive", f"person-answers-round-{args.round}.json")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            json.dump(answers, fh, indent=2)
        report["written"] = dest
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
