#!/usr/bin/env python3
"""check_brief.py — is the brief one a person can act on? (/review-knowledge)

When a drive must reach the person, it does not send a questionnaire. It sends a brief, as you
would brief someone who can help close the piece: what we understood, what we built, and where
the gaps are — each gap with its context and our proposed answer, so the person only confirms
or corrects. This script checks the brief mechanically against what /build-knowledge left;
whether it reads well stays with the agent.

    python3 check_brief.py --brief <working>/brief.json --brief-md <working>/brief.md \
        --build <build working>/build.json --issue <issue> \
        --memory-tool .garura/core/tools/memory/memory.py --out <working>/brief-check.json [--max-gaps 7]

brief.json:
  {"understood": "<what we understood, a few sentences>",
   "built": "<what we built, a few sentences with counts>",
   "gaps": [{"id": "G1", "theme": "<plain name>", "context": "<what we saw that bears on it>",
             "proposal": "<what we would put>", "from": [build group ids]}],
   "settled": [{"from": [build group ids], "what": "<the point>", "why": "<what settles it>"}],
   "pages": [{"update": "<memory update id>", "what": "<what the page says>",
              "sources": ["<link or reference>"], "recommend": "approve | reject"}],
   "prototype_notes": {"count": n, "where": "<path of the full list>"}}

Checks: the brief has what we understood and what we built; every build group closed by a
proposal is in exactly one gap, and gaps are few (at most --max-gaps; related proposals share a
theme); each gap has its context and a proposed answer — never a bare question; every point
the build closed as settled is shown, with why; every memory update the memory tool lists as
waiting for the issue is a page with its sources and a recommendation, so a "yes" is an
informed approval (ADR 035 §5); the prototype notes count matches the build's; brief.md carries
the three headings and names every gap.

Exit 0 clean; 1 gaps; 2 cannot read an input. Standard library only.
"""
import argparse
import json
import subprocess
import sys

HEADINGS = ("What we understood", "What we built", "Where the gaps are")


def waiting_updates(tool, issue):
    """Ids of the issue's memory updates still waiting, from the memory tool (`updates`)."""
    out = subprocess.run([sys.executable, tool, "updates", "--status", "waiting"],
                         capture_output=True, text=True, check=False)
    answer = json.loads(out.stdout.strip().splitlines()[-1]) if out.stdout.strip() else {}
    if not answer.get("ok"):
        raise ValueError(f"memory tool: {answer.get('message') or out.stderr.strip() or 'no answer'}")
    return {str(u.get("id")) for u in answer.get("updates") or [] if str(u.get("issue")) == str(issue)}


def check(brief, md, build, max_gaps, waiting=()):
    problems = []
    for k in ("understood", "built"):
        if not str(brief.get(k) or "").strip():
            problems.append(f"the brief has no `{k}`")
    bgroups = build.get("groups") or []
    proposals = [g.get("id") for g in bgroups if g.get("closed_by") == "proposal"]
    updates = sorted({str(g.get("update")) for g in bgroups if g.get("closed_by") == "update"} | set(waiting))
    settled = [g.get("id") for g in bgroups if g.get("closed_by") == "settled"]
    feedback = sum(1 for g in bgroups if g.get("closed_by") == "prototype-feedback")
    gaps = brief.get("gaps") or []
    if len(gaps) > max_gaps:
        problems.append(f"{len(gaps)} gaps — at most {max_gaps}: join related proposals under one theme")
    seen = {}
    for g in gaps:
        gid = g.get("id") or "(no id)"
        for f in g.get("from") or []:
            seen[f] = seen.get(f, 0) + 1
        for k in ("theme", "context", "proposal"):
            if not str(g.get(k) or "").strip():
                problems.append(f"{gid}: no `{k}` — a gap carries its context and our proposed answer")
        if str(g.get("proposal") or "").strip().endswith("?"):
            problems.append(f"{gid}: the proposal is a question — say what we would put")
        if gid not in md:
            problems.append(f"{gid}: not named in brief.md")
    for p in proposals:
        if seen.get(p, 0) != 1:
            problems.append(f"build group {p} is in {seen.get(p, 0)} gaps (it must be in exactly 1)")
    listed = {str(p.get("update")) for p in brief.get("pages") or []}
    for u in updates:
        if u not in listed:
            problems.append(f"memory update {u} is not listed as a page")
    for p in brief.get("pages") or []:
        if p.get("recommend") not in ("approve", "reject"):
            problems.append(f"page {p.get('update')}: recommend approve or reject")
        if not [x for x in p.get("sources") or [] if str(x).strip()]:
            problems.append(f"page {p.get('update')}: show its sources, so approving it is informed")
    shown = [f for s_ in brief.get("settled") or [] for f in s_.get("from") or []]
    for s_ in brief.get("settled") or []:
        if not str(s_.get("why") or "").strip():
            problems.append(f"settled {s_.get('from')}: say what settles it")
    for b in settled:
        if shown.count(b) != 1:
            problems.append(f"settled build group {b} is shown {shown.count(b)} times (it must be shown once)")
    notes = (brief.get("prototype_notes") or {}).get("count")
    if notes != feedback:
        problems.append(f"prototype notes count {notes!r} does not match the build's {feedback}")
    for h in HEADINGS:
        if h not in md:
            problems.append(f"brief.md has no `{h}` heading")
    return problems, {"gaps": len(gaps), "proposals": len(proposals), "pages": len(listed),
                      "prototype_notes": feedback}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the knowledge brief.")
    ap.add_argument("--brief", required=True)
    ap.add_argument("--brief-md", required=True)
    ap.add_argument("--build", required=True)
    ap.add_argument("--issue", required=True)
    ap.add_argument("--memory-tool", default=".garura/core/tools/memory/memory.py")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-gaps", type=int, default=7)
    args = ap.parse_args(argv)
    try:
        with open(args.brief, encoding="utf-8") as fh:
            brief = json.load(fh)
        with open(args.brief_md, encoding="utf-8") as fh:
            md = fh.read()
        with open(args.build, encoding="utf-8") as fh:
            build = json.load(fh)
        waiting = waiting_updates(args.memory_tool, args.issue)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"check_brief.py: cannot read an input: {exc}\n")
        return 2
    problems, counts = check(brief, md, build, args.max_gaps, waiting)
    report = {"ok": not problems, "gaps_found": problems, **counts}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
