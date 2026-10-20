#!/usr/bin/env python3
"""check_memory_build.py — is every open question closed one honest way? (/build-memory)

The memory builder turns a round's open questions into answers, knowledge pages and a few
questions for the person (design: Argus #680, `memory-builder.md`). This script checks its
record mechanically; whether an answer is *right* stays with the agent.

    python3 check_memory_build.py --build <working>/memory-build.json \
        --groups <working>/question-groups.json --issue-dir <stm_base><issue>/ \
        --out <working>/memory-build-check.json

memory-build.json:
  {"groups": [{"id", "members": [question ids], "ask": "<the one question, plain words>",
               "closed_by": "source | memory | update | person | prototype-feedback",
               "answer": "...", "evidence": [{"file", "where", "quote"}],   # source
               "trace": "<cite id>",                                        # memory
               "update": "<memory update id>", "for_project_memory": bool,  # update
               "examples": ["..."],                                         # person
               "feedback": "<what the prototype should show>"}]}            # prototype-feedback

Checks: every question in question-groups.json is in exactly one group of the build; each
group is closed one known way, with what that way needs — a source answer has a quote and the
file it came from; a memory answer its trace; an update names a memory update that exists in
the issue's short-term memory; a person question has its words and 1–3 examples; feedback says
what the prototype should show. Also counts how many questions the person is asked — the point
of the builder is that it is few.

Exit 0 clean; 1 gaps; 2 cannot read an input. Standard library only.
"""
import argparse
import json
import os
import sys

WAYS = ("source", "memory", "update", "person", "prototype-feedback")


def check(build, groups, issue_dir):
    gaps = []
    asked = [m for g in groups.get("groups", []) for m in g.get("members", [])]
    seen = {}
    for g in build.get("groups") or []:
        gid = g.get("id") or "(no id)"
        for m in g.get("members") or []:
            seen[m] = seen.get(m, 0) + 1
        way = g.get("closed_by")
        if way not in WAYS:
            gaps.append(f"{gid}: closed_by must be one of {', '.join(WAYS)} (found {way!r})")
            continue
        if not str(g.get("ask") or "").strip():
            gaps.append(f"{gid}: no plain question (`ask`)")
        if way == "source":
            ev = g.get("evidence") or []
            if not ev or not all(str(e.get("quote") or "").strip() and str(e.get("file") or "").strip() for e in ev):
                gaps.append(f"{gid}: a source answer needs a quote and the file it came from")
            if not str(g.get("answer") or "").strip():
                gaps.append(f"{gid}: a source answer needs the answer")
        elif way == "memory":
            if not str(g.get("trace") or "").strip() or not str(g.get("answer") or "").strip():
                gaps.append(f"{gid}: a memory answer needs the answer and its trace")
        elif way == "update":
            uid = str(g.get("update") or "")
            if not os.path.isfile(os.path.join(issue_dir, "review", "memory-updates", f"{uid}.json")):
                gaps.append(f"{gid}: memory update `{uid}` is not in the issue's short-term memory")
        elif way == "person":
            ex = g.get("examples") or []
            if not 1 <= len(ex) <= 3:
                gaps.append(f"{gid}: a question for the person needs 1 to 3 example answers")
        elif way == "prototype-feedback":
            if not str(g.get("feedback") or "").strip():
                gaps.append(f"{gid}: feedback must say what the prototype should show")
    for q in asked:
        if seen.get(q, 0) != 1:
            gaps.append(f"question {q} is in {seen.get(q, 0)} groups of the build (it must be in exactly 1)")
    counts = {w: sum(1 for g in build.get("groups") or [] if g.get("closed_by") == w) for w in WAYS}
    return gaps, {"questions": len(asked), "groups": len(build.get("groups") or []), "closed": counts,
                  "asked_of_person": counts["person"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the memory builder's record.")
    ap.add_argument("--build", required=True)
    ap.add_argument("--groups", required=True)
    ap.add_argument("--issue-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.build, encoding="utf-8") as fh:
            build = json.load(fh)
        with open(args.groups, encoding="utf-8") as fh:
            groups = json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"check_memory_build.py: cannot read an input: {exc}\n")
        return 2
    gaps, counts = check(build, groups, args.issue_dir)
    report = {"ok": not gaps, "gaps": gaps, **counts}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0 if not gaps else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
