#!/usr/bin/env python3
"""check_sources.py — does every page /discover-capabilities wrote say where it is seen? (C16, #689)

Reads each target's `enrich-manifest.yaml` and the pages it names — the detailed
`capability.md` and every new `functionality.md` — and checks, mechanically:

- every page ends its content with `## Sources` (before its agent intent), listing at least one
  source;
- with `--source-text` (the prototype's captured text — a file, or a folder of `.txt`), every
  quoted string (in double quotes) on a source line is on the prototype; a line naming a
  knowledge shelf quotes the shelf's terms, not the prototype, and is not checked;
- no page leaves a question open: a line that says it is "recorded as an open question", "to
  be confirmed" or "not shown … ask" is a gap the skill should have filled with a marked
  default (C16).

Whether a functionality is a whole function or only one panel of a screen is judgement — the
agent's, and the rebuild eval's review. This script checks only what can be counted.

    python3 check_sources.py --manifest <working>/caps/<cap>/enrich-manifest.yaml [--manifest …] \
        --product-base <product_base> [--source-text <file or folder>]... --out <working>/sources-check.json

Exit 0 clean; 1 gaps (listed in the report); 2 an input cannot be read. Standard library + PyYAML.
"""
import argparse
import glob
import json
import os
import re
import sys

import yaml

QUOTE = re.compile(r"[\"“]([^\"“”]{4,})[\"”]")
MARKS = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "})
OPEN = re.compile(r"recorded as an open question|open question for the person|to be confirmed by the person"
                  r"|\bTBD\b|left open for the person", re.I)
SHELF = re.compile(r"\b(shelf|proposal)\b", re.I)


def norm(text):
    return re.sub(r"\s+", " ", text.translate(MARKS)).strip().lower()


def read(path):
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def sources_of(text):
    """The lines of the page's `## Sources` section, or None when it has none."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "## Sources":
            out = []
            for nxt in lines[i + 1:]:
                if nxt.startswith("## "):
                    break
                if nxt.strip():
                    out.append(nxt.strip())
            return out
    return None


def pages(manifest, model):
    enrich = (manifest or {}).get("enrich", manifest) or {}
    docs = []
    cap = enrich.get("capability") or {}
    if cap.get("doc"):
        docs.append(str(cap["doc"]))
    docs += [str(f["doc"]) for f in enrich.get("functionalities") or [] if isinstance(f, dict) and f.get("doc")]
    return [(d, os.path.join(model, d)) for d in docs]


def check(manifests, model, source_text):
    gaps, counts = [], {"pages": 0, "quotes": 0, "quotes_found": 0}
    for m in manifests:
        for doc, path in pages(m, model):
            counts["pages"] += 1
            if not os.path.isfile(path):
                gaps.append(f"{doc}: the manifest names it but the page is not there")
                continue
            text = read(path)
            src = sources_of(text)
            if not src:
                gaps.append(f"{doc}: no `## Sources` saying where it is seen (C16)")
            else:
                for line in src:
                    if SHELF.search(line) or source_text is None:
                        continue
                    for q in QUOTE.findall(line):
                        counts["quotes"] += 1
                        if norm(q) in source_text:
                            counts["quotes_found"] += 1
                        else:
                            gaps.append(f"{doc}: \"{q[:80]}\" is not on the prototype")
            for line in text.splitlines():
                if OPEN.search(line):
                    gaps.append(f"{doc}: leaves a question open (\"{line.strip()[:90]}\") — write our "
                                f"default, marked as ours, instead (C16)")
                    break
    return gaps, counts


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the sources of the pages /discover-capabilities wrote.")
    ap.add_argument("--manifest", action="append", required=True)
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--source-text", action="append", default=[])
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        manifests = [yaml.safe_load(read(p)) for p in args.manifest]
        text = None
        if args.source_text:
            parts = []
            for t in args.source_text:
                paths = glob.glob(os.path.join(t, "**", "*.txt"), recursive=True) if os.path.isdir(t) else [t]
                parts += [read(p) for p in paths]
            text = norm("\n".join(parts))
    except (OSError, yaml.YAMLError) as exc:
        sys.stderr.write(f"check_sources.py: cannot read an input: {exc}\n")
        return 2
    gaps, counts = check(manifests, os.path.join(args.product_base, "product-os"), text)
    report = {"ok": not gaps, "gaps": gaps, **counts}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0 if not gaps else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
