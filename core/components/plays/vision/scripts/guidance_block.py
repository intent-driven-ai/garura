#!/usr/bin/env python3
"""guidance_block.py — cut a grounding template's `## Per-section guidance` block.

A content-quality judge is handed only its doc (and parent doc) and the kind's per-section
guidance — never the template's gold example (standards/rules/grounding-eval.md; the
judge-grounding skill). template-manager puts the whole kind template in short-term memory;
this script cuts the guidance block out of that copy, so the judge gets nothing else.

    python3 guidance_block.py --template <kind template copy> --out <guidance.md>

Each block runs from a heading that starts `## Per-section guidance` (for example
`## Per-section guidance (detailed stage)`) to the next `## ` heading outside a code fence;
every such block is kept, in order. Exit 0 written; 2 the template has no such block, or
cannot be read — nothing written. Standard library only.
"""
import argparse
import os
import sys

HEADING = "## Per-section guidance"


def cut(text):
    """The guidance block of a template, or None when it has none."""
    out, inside, fence = [], False, False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and line.startswith(HEADING):
            inside = True  # every guidance block (a template may hold one per stage)
        elif inside and not fence and line.startswith("## "):
            inside = False
        if inside:
            out.append(line)
    return "\n".join(out).rstrip() + "\n" if out else None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cut a template's per-section guidance block.")
    ap.add_argument("--template", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.template, encoding="utf-8") as fh:
            block = cut(fh.read())
    except OSError as exc:
        sys.stderr.write(f"guidance_block.py: cannot read {args.template}: {exc} — nothing written\n")
        return 2
    if block is None:
        sys.stderr.write(f"guidance_block.py: {args.template} has no '{HEADING}' block — nothing written\n")
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(block)
    return 0


if __name__ == "__main__":
    sys.exit(main())
