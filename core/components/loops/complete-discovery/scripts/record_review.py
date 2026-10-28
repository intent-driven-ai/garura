#!/usr/bin/env python3
"""record_review.py — record the person's reply to the brief (Shared Loop Run, R5b).

The loop shows the knowledge brief the knowledge-builder agent wrote (R5c) and waits for the
person's typed reply: "yes" (take every proposal and every recommendation), or corrections to
some gaps and pages.
The loop writes that reply as review.json; this script checks it covers the whole brief and
records the answers in the issue's short-term memory, so the next round's plays read them.

    python3 record_review.py --brief <working>/brief.json --reply <working>/review.json \
        --build <working>/build.json --search <working>/search.json --review-dir <review_dir> \
        --issue-dir <stm_base><issue>/ --round <n> --out <working>/review-record.json

review.json:
  {"words": "<the person's reply, verbatim>",
   "gaps": {"G1": "accept" | {"answer": "<the person's own answer>"}},
   "pages": {"<memory update id>": "approve" | "reject"}}
  A bare "yes" is written as every gap "accept" and every page its recommendation.

Writes `<issue-dir>/review/loop/person-answers-round-<n>.json`:
  {"gaps": [{"gap", "theme", "answer", "accepted_proposal": bool, "proposed_by", "basis",
             "from": "person", "words"}],
   "answers": {"<play>": {"<question id>": "<answer>"}}}
`answers` maps each gap back to the open questions it closes (gap → build groups → search
groups → question ids → the play whose `open-<play>.json` asked it), so the loop adds them to
the contract's `answers` and the next round's plays read them as any answer. The record lists
each page's decision for the memory tool's `decide` (ADR 041 §8).
Exit 0 recorded; 1 the reply leaves a gap or page undecided; 2 cannot read an input.
Standard library only.
"""
import argparse
import json
import os
import sys


def question_plays(review_dir):
    """Map each open question id to the play that asked it (from open-<play>.json)."""
    plays = {}
    for name in sorted(os.listdir(review_dir)) if os.path.isdir(review_dir) else []:
        if name.startswith("open-") and name.endswith(".json"):
            with open(os.path.join(review_dir, name), encoding="utf-8") as fh:
                doc = json.load(fh)
            for q in doc.get("questions") or []:
                plays[str(q.get("id"))] = doc.get("play") or name[5:-5]
    return plays


def questions_of(gap, build, search):
    """The open question ids a brief gap closes: gap -> build groups -> search groups -> members."""
    bgroups = {g.get("id"): g for g in build.get("groups") or []}
    sgroups = {g.get("id"): g for g in search.get("groups") or []}
    ids = []
    for b in gap.get("from") or []:
        for s in (bgroups.get(b) or {}).get("from") or []:
            ids.extend(str(m) for m in (sgroups.get(s) or {}).get("members") or [])
    return ids


def by_play(gap_answers, brief, build, search, plays):
    out = {}
    gaps = {g.get("id"): g for g in brief.get("gaps") or []}
    for a in gap_answers:
        for q in questions_of(gaps.get(a["gap"], {}), build, search):
            if q in plays:
                out.setdefault(plays[q], {})[q] = a["answer"]
    return out


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
                            "accepted_proposal": True, "proposed_by": "knowledge-builder",
                            "basis": g.get("basis") or g.get("context"), "from": "person",
                            "words": words})
        elif isinstance(r, dict) and str(r.get("answer") or "").strip():
            answers.append({"gap": gid, "theme": g.get("theme"), "answer": r["answer"],
                            "accepted_proposal": False, "proposed_by": None, "basis": None,
                            "from": "person", "words": words})
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
    ap.add_argument("--build", required=True)
    ap.add_argument("--search", required=True)
    ap.add_argument("--review-dir", required=True)
    ap.add_argument("--issue-dir", required=True)
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.brief, encoding="utf-8") as fh:
            brief = json.load(fh)
        with open(args.reply, encoding="utf-8") as fh:
            reply = json.load(fh)
        with open(args.build, encoding="utf-8") as fh:
            build = json.load(fh)
        with open(args.search, encoding="utf-8") as fh:
            search = json.load(fh)
        plays = question_plays(args.review_dir)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"record_review.py: cannot read an input: {exc}\n")
        return 2
    problems, answers, decisions = record(brief, reply)
    report = {"ok": not problems, "problems": problems, "answers": len(answers),
              "page_decisions": decisions}
    if not problems:
        dest = os.path.join(args.issue_dir, "review", "loop", f"person-answers-round-{args.round}.json")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        mapped = by_play(answers, brief, build, search, plays)
        with open(dest, "w", encoding="utf-8") as fh:
            json.dump({"gaps": answers, "answers": mapped}, fh, indent=2)
        report["written"] = dest
        report["questions_answered"] = sum(len(v) for v in mapped.values())
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
