#!/usr/bin/env python3
"""check_knowledge.py — did the loop's knowledge step close what the round left? (Shared Loop Run, R5c)

When a round stops with open questions, the knowledge-builder agent closes them in one step
(ADR 059): it searches the loop's sources and memory (search.json), closes what the search
left (build.json), and writes the brief the loop shows the person (brief.json, rendered to
brief.md). This script checks the three records mechanically; whether an answer is *right*,
a proposal *good* or the brief *readable* stays with the agent and the person.

    python3 check_knowledge.py --groups <working>/question-groups.json \
        --search <working>/search.json --build <working>/build.json \
        --brief <working>/brief.json --brief-md <working>/brief.md --issue <issue> \
        --memory-tool .garura/core/tools/memory/memory.py \
        --renderer <skills>/author-knowledge-brief/scripts/render_brief.py \
        --out <working>/knowledge-check.json [--max-gaps 7]

search.json:
  {"groups": [{"id", "members": [question ids], "ask": "<the one question, plain words>",
               "found": "answered | partly | open",
               "closed_by": "source | memory",                              # answered, partly
               "answer": "...", "evidence": [{"file", "where", "quote"}],   # source
               "trace": "<cite id>",                                        # memory
               "missing": "<what is still not known>",                      # partly, open
               "not_shown": "should-show | no-screen"}]}                    # open

build.json:
  {"groups": [{"id", "from": [search group ids], "ask": "<the gap, plain words>",
               "closed_by": "update | proposal | prototype-feedback | settled",
               "update": "<memory update id>", "for_project_memory": bool,   # update
               "proposal": {"answer", "basis", "context"},                  # proposal
               "feedback": "<what the prototype should show>",               # prototype-feedback
               "why": "<what in the context settles it>",                   # settled
               "basis": "<the quote, screen or trace it rests on>"}]}         # settled

brief.json:
  {"understood": "<what we understood, a few sentences>",
   "built": "<what we built, a few sentences with counts>",
   "gaps": [{"id": "G1", "theme": "<plain name>", "context": "<what we saw that bears on it>",
             "proposal": "<what we would put>", "from": [build group ids]}],
   "settled": [{"from": [build group ids], "what": "<the point>", "why": "<what settles it>"}],
   "pages": [{"update": "<memory update id>", "what": "<what the page says>",
              "sources": ["<link or reference>"], "recommend": "approve | reject"}],
   "prototype_notes": {"count": n, "where": "<path of the full list>"}}

Checks, search: every question in question-groups.json is in exactly one group; each group has
its plain question; an answered or partly answered group says how (source with a quote and its
file, or memory with its trace) and gives the answer; a partly answered or open group names
what is still missing; an open group says whether the source should show it or no screen could.

Checks, build: every search group found `partly` or `open` is in exactly one build group, and
no answered one is built again; each build group is closed one known way, with what that way
needs — an update names a memory update the memory tool lists for the issue as waiting
(`updates`, never read from its file); a proposal has its answer, its basis and the context a
person needs to judge it; feedback says what the prototype should show; settled says why and
what it rests on. A search group the source should show (`should-show`) is closed by
prototype feedback.

Checks, brief: it has what we understood and what we built; every build group closed by a
proposal is in exactly one gap, and gaps are few (at most --max-gaps); each gap has its context
and a proposed answer, never a bare question; every settled point is shown once, with why;
every memory update the memory tool lists as waiting for the issue is a page with its sources
and a recommendation (ADR 035 §5); the prototype notes count matches the build's; brief.md
carries the three headings, names every gap, and is exactly what the brief skill's renderer
(`render_brief.py`) writes from brief.json.

The memory tool is asked once, read-only; this script never decides, applies or promotes an
update. Exit 0 clean; 1 gaps; 2 cannot read an input. Standard library only.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

FOUND = ("answered", "partly", "open")
WAYS = ("update", "proposal", "prototype-feedback", "settled")
HEADINGS = ("What we understood", "What we built", "Where the gaps are")


def waiting_updates(tool, issue):
    """Ids of the issue's memory updates still waiting, from the memory tool (`updates`)."""
    out = subprocess.run([sys.executable, tool, "updates", "--status", "waiting"],
                         capture_output=True, text=True, check=False)
    answer = json.loads(out.stdout.strip().splitlines()[-1]) if out.stdout.strip() else {}
    if not answer.get("ok"):
        raise ValueError(f"memory tool: {answer.get('message') or out.stderr.strip() or 'no answer'}")
    return {str(u.get("id")) for u in answer.get("updates") or [] if str(u.get("issue")) == str(issue)}


def render(renderer, brief_path):
    """brief.md as the brief skill's renderer writes it from brief.json."""
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "brief.md")
        run = subprocess.run([sys.executable, renderer, "--brief", brief_path, "--out", out],
                             capture_output=True, text=True, check=False)
        if run.returncode != 0 or not os.path.isfile(out):
            raise ValueError(f"renderer: {run.stderr.strip() or 'no brief.md written'}")
        with open(out, encoding="utf-8") as fh:
            return fh.read()


def check_search(search, groups):
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


def check_build(search, build, waiting):
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


def check_brief(brief, md, build, max_gaps, waiting=(), rendered=None):
    problems = []
    if rendered is not None and md.strip() != rendered.strip():
        problems.append("brief.md is not the renderer's output from brief.json — write brief.json and "
                        "render brief.md with render_brief.py; never write or edit brief.md by hand")
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


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the loop's knowledge step: search, build and brief.")
    ap.add_argument("--groups", required=True)
    ap.add_argument("--search", required=True)
    ap.add_argument("--build", required=True)
    ap.add_argument("--brief", required=True)
    ap.add_argument("--brief-md", required=True)
    ap.add_argument("--issue", required=True)
    ap.add_argument("--memory-tool", default=".garura/core/tools/memory/memory.py")
    ap.add_argument("--renderer", required=True, help="the brief skill's scripts/render_brief.py")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-gaps", type=int, default=7)
    args = ap.parse_args(argv)
    try:
        groups, search, build, brief = (load(p) for p in (args.groups, args.search, args.build, args.brief))
        with open(args.brief_md, encoding="utf-8") as fh:
            md = fh.read()
        waiting = waiting_updates(args.memory_tool, args.issue)
        rendered = render(args.renderer, args.brief)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"check_knowledge.py: cannot read an input: {exc}\n")
        return 2
    s_gaps, s_counts = check_search(search, groups)
    b_gaps, b_counts = check_build(search, build, waiting)
    r_gaps, r_counts = check_brief(brief, md, build, args.max_gaps, waiting, rendered)
    report = {"ok": not (s_gaps or b_gaps or r_gaps),
              "search": {"gaps": s_gaps, **s_counts},
              "build": {"gaps": b_gaps, **b_counts},
              "brief": {"gaps": r_gaps, **r_counts}}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
