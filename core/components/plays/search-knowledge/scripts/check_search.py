#!/usr/bin/env python3
"""check_search.py — did the search look before anyone builds or asks? (/search-knowledge)

The knowledge-builder agent takes a round's open questions, already grouped, and looks for
each one in the loop's own sources (for a prototype: its views, journeys and page) and in
memory. This script checks its record mechanically; whether an answer is *right* stays with
the agent.

    python3 check_search.py --search <working>/search.json \
        --groups <working>/question-groups.json --out <working>/search-check.json

search.json:
  {"groups": [{"id", "members": [question ids], "ask": "<the one question, plain words>",
               "found": "answered | partly | open",
               "closed_by": "source | memory",                              # answered, partly
               "answer": "...", "evidence": [{"file", "where", "quote"}],   # source
               "trace": "<cite id>",                                        # memory
               "missing": "<what is still not known>",                      # partly, open
               "not_shown": "should-show | no-screen"}]}                    # open

Checks: every question in question-groups.json is in exactly one group; each group has its
plain question; an answered or partly answered group says how (source with a quote and its
file, or memory with its trace) and gives the answer; a partly answered or open group names
what is still missing; an open group says whether the source should show it or no screen
could. Counts what the search closed and what it leaves for /research-knowledge.

Exit 0 clean; 1 gaps; 2 cannot read an input. Standard library only.
"""
import argparse
import json
import sys

FOUND = ("answered", "partly", "open")


def check(search, groups):
    gaps = []
    asked = [m for g in groups.get("groups", []) for m in g.get("members", [])]
    seen = {}
    for g in search.get("groups") or []:
        gid = g.get("id") or "(no id)"
        for m in g.get("members") or []:
            seen[m] = seen.get(m, 0) + 1
        if not str(g.get("ask") or "").strip():
            gaps.append(f"{gid}: no plain question (`ask`)")
        found = g.get("found")
        if found not in FOUND:
            gaps.append(f"{gid}: found must be one of {', '.join(FOUND)} (found {found!r})")
            continue
        if found in ("answered", "partly"):
            way = g.get("closed_by")
            if way == "source":
                ev = g.get("evidence") or []
                if not ev or not all(str(e.get("quote") or "").strip() and str(e.get("file") or "").strip()
                                     for e in ev):
                    gaps.append(f"{gid}: a source answer needs a quote and the file it came from")
            elif way == "memory":
                if not str(g.get("trace") or "").strip():
                    gaps.append(f"{gid}: a memory answer needs its trace")
            else:
                gaps.append(f"{gid}: an answer must come from `source` or `memory` (found {way!r})")
            if not str(g.get("answer") or "").strip():
                gaps.append(f"{gid}: an answered group needs the answer")
        if found in ("partly", "open") and not str(g.get("missing") or "").strip():
            gaps.append(f"{gid}: say what is still missing")
        if found == "open" and g.get("not_shown") not in ("should-show", "no-screen"):
            gaps.append(f"{gid}: an open group says whether the source should show it (should-show) "
                        f"or no screen could (no-screen)")
    for q in asked:
        if seen.get(q, 0) != 1:
            gaps.append(f"question {q} is in {seen.get(q, 0)} groups of the search (it must be in exactly 1)")
    gs = search.get("groups") or []
    counts = {f: sum(1 for g in gs if g.get("found") == f) for f in FOUND}
    return gaps, {"questions": len(asked), "groups": len(gs), "found": counts,
                  "left_for_build": counts["partly"] + counts["open"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the knowledge search record.")
    ap.add_argument("--search", required=True)
    ap.add_argument("--groups", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.search, encoding="utf-8") as fh:
            search = json.load(fh)
        with open(args.groups, encoding="utf-8") as fh:
            groups = json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"check_search.py: cannot read an input: {exc}\n")
        return 2
    gaps, counts = check(search, groups)
    report = {"ok": not gaps, "gaps": gaps, **counts}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0 if not gaps else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
