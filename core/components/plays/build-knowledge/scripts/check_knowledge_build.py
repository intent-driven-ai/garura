#!/usr/bin/env python3
"""check_knowledge_build.py — is every gap the search left closed one honest way? (/build-knowledge)

/search-knowledge answered what the drive's sources and memory hold. What it left — groups it
found `partly` or `open` — the knowledge-builder agent closes here: a researched knowledge page
raised as a memory update a person approves, our proposed answer with its basis and context, a
note for the prototype, or settled because the context already answers it. This script checks
the record mechanically; whether a proposal is *good* stays with the agent and the person.

    python3 check_knowledge_build.py --search <search working>/search.json \
        --build <working>/build.json --issue <issue> \
        --memory-tool .garura/core/tools/memory/memory.py --out <working>/build-check.json

build.json:
  {"groups": [{"id", "from": [search group ids], "ask": "<the gap, plain words>",
               "closed_by": "update | proposal | prototype-feedback | settled",
               "update": "<memory update id>", "for_project_memory": bool,   # update
               "proposal": {"answer", "basis", "context"},                  # proposal
               "feedback": "<what the prototype should show>",               # prototype-feedback
               "why": "<what in the context settles it>",                   # settled
               "basis": "<the quote, screen or trace it rests on>"}]}         # settled

Checks: every search group found `partly` or `open` is in exactly one build group, and no
answered search group is built again; each build group is closed one known way, with what that
way needs — an update names a memory update the memory tool lists for the issue as waiting
(`updates` — never read from its file); a proposal has
its answer, its basis (the source, memory or reasoning it rests on) and the context a person
needs to judge it; feedback says what the prototype should show; settled says why and what it rests on (it is
shown to the person in the brief, never dropped silently). A search
group the source should show (`should-show`) is closed by prototype feedback.

Exit 0 clean; 1 gaps; 2 cannot read an input. Standard library only.
"""
import argparse
import json
import subprocess
import sys

WAYS = ("update", "proposal", "prototype-feedback", "settled")


def waiting_updates(tool, issue):
    """Ids of the issue's memory updates still waiting, from the memory tool (`updates`)."""
    out = subprocess.run([sys.executable, tool, "updates", "--status", "waiting"],
                         capture_output=True, text=True, check=False)
    answer = json.loads(out.stdout.strip().splitlines()[-1]) if out.stdout.strip() else {}
    if not answer.get("ok"):
        raise ValueError(f"memory tool: {answer.get('message') or out.stderr.strip() or 'no answer'}")
    return {str(u.get("id")) for u in answer.get("updates") or [] if str(u.get("issue")) == str(issue)}


def check(search, build, waiting):
    gaps = []
    sgroups = {g.get("id"): g for g in search.get("groups") or []}
    left = [gid for gid, g in sgroups.items() if g.get("found") in ("partly", "open")]
    seen = {}
    for g in build.get("groups") or []:
        bid = g.get("id") or "(no id)"
        for s in g.get("from") or []:
            seen[s] = seen.get(s, 0) + 1
            if s in sgroups and sgroups[s].get("found") == "answered":
                gaps.append(f"{bid}: search group {s} was already answered — it is not built again")
            if sgroups.get(s, {}).get("not_shown") == "should-show" and g.get("closed_by") != "prototype-feedback":
                gaps.append(f"{bid}: search group {s} is a screen the prototype should show — close it as prototype feedback")
        if not str(g.get("ask") or "").strip():
            gaps.append(f"{bid}: no plain statement of the gap (`ask`)")
        way = g.get("closed_by")
        if way not in WAYS:
            gaps.append(f"{bid}: closed_by must be one of {', '.join(WAYS)} (found {way!r})")
            continue
        if way == "update":
            uid = str(g.get("update") or "")
            if uid not in waiting:
                gaps.append(f"{bid}: memory update `{uid}` is not waiting for this issue (memory tool `updates`)")
        elif way == "proposal":
            p = g.get("proposal") or {}
            missing = [k for k in ("answer", "basis", "context") if not str(p.get(k) or "").strip()]
            if missing:
                gaps.append(f"{bid}: a proposal needs its {', '.join(missing)}")
        elif way == "prototype-feedback":
            if not str(g.get("feedback") or "").strip():
                gaps.append(f"{bid}: feedback must say what the prototype should show")
        elif way == "settled":
            if not str(g.get("why") or "").strip():
                gaps.append(f"{bid}: say what in the context settles it")
            if not str(g.get("basis") or "").strip():
                gaps.append(f"{bid}: a settled gap needs its basis — the quote, screen or trace it rests on")
    for s in left:
        if seen.get(s, 0) != 1:
            gaps.append(f"search group {s} is in {seen.get(s, 0)} build groups (it must be in exactly 1)")
    bg = build.get("groups") or []
    counts = {w: sum(1 for g in bg if g.get("closed_by") == w) for w in WAYS}
    return gaps, {"left_by_search": len(left), "groups": len(bg), "closed": counts}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the knowledge build record.")
    ap.add_argument("--search", required=True)
    ap.add_argument("--build", required=True)
    ap.add_argument("--issue", required=True)
    ap.add_argument("--memory-tool", default=".garura/core/tools/memory/memory.py")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.search, encoding="utf-8") as fh:
            search = json.load(fh)
        with open(args.build, encoding="utf-8") as fh:
            build = json.load(fh)
        waiting = waiting_updates(args.memory_tool, args.issue)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"check_knowledge_build.py: cannot read an input: {exc}\n")
        return 2
    gaps, counts = check(search, build, waiting)
    report = {"ok": not gaps, "gaps": gaps, **counts}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0 if not gaps else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
