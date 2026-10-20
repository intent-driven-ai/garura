#!/usr/bin/env python3
"""guidance_block.py — cut a grounding template's guidance for one stage.

A content-quality judge is handed only its doc (and parent doc) and the kind's per-section
guidance — never the template's gold example (standards/rules/grounding-eval.md; the
judge-grounding skill). template-manager puts the whole kind template in short-term memory;
this script cuts the guidance out of that copy, so the judge gets nothing else.

    python3 guidance_block.py --template <kind template copy> --out <guidance.md> \
        [--stage directional|detailed]

The judge must judge a doc against its own stage: /vision writes a capability at the
directional stage, /understand at the detailed one (#662). With --stage, the cut keeps, in
template order, every `## ` block whose heading is:
  - `## Per-section guidance`, with no stage named or naming this stage;
  - `## Heading contract — <STAGE> stage …` for this stage (it says what each section holds);
  - a section that applies "at every stage" (the agent intent).
Without --stage it keeps every `## Per-section guidance…` block, as before. A block runs to
the next `## ` heading outside a code fence. A gold example is never kept. Exit 0 written;
2 nothing to keep, or the template cannot be read — nothing written. Standard library only.
"""
import argparse
import os
import re
import sys

HEADING = "## Per-section guidance"
STAGES = ("directional", "detailed")


def wanted(heading, stage):
    """True when a `## ` heading opens a block the judge of this stage should see."""
    h = heading.lower()
    if "gold example" in h:
        return False
    named = [s for s in STAGES if s in h]
    if stage is None:
        return heading.startswith(HEADING)
    if heading.startswith(HEADING):
        return not named or stage in named
    if h.startswith("## heading contract"):
        return stage in named
    return "at every stage" in h


def cut(text, stage=None):
    """The guidance for a stage (every guidance block when stage is None), or None."""
    out, inside, fence = [], False, False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        elif not fence and re.match(r"^## ", line):
            inside = wanted(line, stage)
        if inside:
            out.append(line)
    return "\n".join(out).rstrip() + "\n" if out else None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cut a template's guidance for one stage.")
    ap.add_argument("--template", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stage", choices=STAGES)
    args = ap.parse_args(argv)
    try:
        with open(args.template, encoding="utf-8") as fh:
            block = cut(fh.read(), args.stage)
    except OSError as exc:
        sys.stderr.write(f"guidance_block.py: cannot read {args.template}: {exc} — nothing written\n")
        return 2
    if block is None:
        sys.stderr.write(f"guidance_block.py: {args.template} has no guidance for "
                         f"{args.stage or 'any'} stage — nothing written\n")
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(block)
    return 0


if __name__ == "__main__":
    sys.exit(main())
