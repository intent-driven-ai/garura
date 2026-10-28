#!/usr/bin/env python3
"""render_brief.py — write brief.md from brief.json (author-knowledge-brief).

The agent writes the brief's content once, in brief.json. This script lays it out as the page
the person reads, the same way every time, so the page holds exactly what the check reads and
nothing written beside it. The knowledge step's check (check_knowledge.py) renders brief.json
again with this script and fails a brief.md that differs.

    python3 render_brief.py --brief <working>/brief.json --out <working>/brief.md

brief.json: {"title"?, "understood", "built", "gaps": [{"id", "theme", "context", "proposal",
"from"}], "settled": [{"from", "what", "why"}], "pages": [{"update", "name"?, "what", "sources",
"recommend", "why"?}], "prototype_notes": {"count", "where"}}. Text fields may hold several
paragraphs, separated by a blank line.

Exit 0 written; 2 brief.json cannot be read. Standard library only.
"""
import argparse
import json
import sys

TITLE = "Where we are and what we need from you"


def para(text):
    return str(text or "").strip()


def render(brief):
    out = [f"# {para(brief.get('title')) or TITLE}", "",
           "## What we understood", "", para(brief.get("understood")), "",
           "## What we built", "", para(brief.get("built")), "",
           "## Where the gaps are", ""]
    gaps = brief.get("gaps") or []
    if gaps:
        out += ["Each gap gives what we saw and what we would put. If our answer is right, say yes.", ""]
        for g in gaps:
            out += [f"**{para(g.get('id'))}. {para(g.get('theme'))}**", "",
                    f"What we saw: {para(g.get('context'))}", "",
                    f"Our answer: {para(g.get('proposal'))}", ""]
    else:
        out += ["None.", ""]
    settled = brief.get("settled") or []
    if settled:
        out += ["## Settled", ""]
        for s in settled:
            ids = ", ".join(str(f) for f in s.get("from") or [])
            out += [f"{para(s.get('what'))} What settles it: {para(s.get('why'))} "
                    f"(Point {ids}; correct it by that id.)", ""]
    pages = brief.get("pages") or []
    if pages:
        out += ["## Knowledge pages waiting for your approval", "",
                "None of these is used until you approve it.", ""]
        for p in pages:
            name = f" {para(p.get('name'))}." if para(p.get("name")) else ""
            why = f" {para(p.get('why'))}" if para(p.get("why")) else ""
            sources = ", ".join(str(x) for x in p.get("sources") or [])
            out += [f"**{para(p.get('update'))}.{name}** {para(p.get('what'))} Sources: {sources}. "
                    f"Our recommendation: {para(p.get('recommend'))}.{why}", ""]
    notes = brief.get("prototype_notes") or {}
    count = notes.get("count") or 0
    out += ["## Prototype notes", ""]
    if count:
        noun = "note" if count == 1 else "notes"
        out += [f"There {'is' if count == 1 else 'are'} {count} {noun} for the prototype. "
                f"{'It needs' if count == 1 else 'They need'} no answer now. "
                f"The full list is in `{para(notes.get('where'))}`.", ""]
    else:
        out += ["None.", ""]
    ids = [para(g.get("id")) for g in gaps] + [str(f) for s in settled for f in s.get("from") or []] \
        + [para(p.get("update")) for p in pages]
    out += ["## How to reply", "",
            "Say \"yes\" to take every proposal and every recommendation above, or correct any item by "
            f"its id ({', '.join(i for i in ids if i) or 'none'}).", ""]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write brief.md from brief.json.")
    ap.add_argument("--brief", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.brief, encoding="utf-8") as fh:
            brief = json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"render_brief.py: cannot read the brief: {exc}\n")
        return 2
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(render(brief))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
