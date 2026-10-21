#!/usr/bin/env python3
"""
grounding_check.py — assert every seeded capability is grounded (C5/F3).

/vision must never invent a capability. Each one either matched a KB shelf
(recorded by search-kb) or was raised as a propose-kb-node proposal. This script
reads the seed manifest author-vision-seed wrote and asserts that every capability
carries one or the other — and, when a proposal path is named, that the proposal
file actually exists on disk. That covers every capability the run adds, places or
changes, its own and another play's (#637): each id in the spine-delta's new
`capabilities` and its capability `updates` must be listed in the manifest's
`capabilities`, with its grounding.

With `--product-base`, it also reads the pages the run wrote (#689): the domain page must end
with `## Sources` naming the shelf it matched or the research links that show the world
recognises it (a domain is never a name made up for one product), and every capability page
the run added must carry `## Sources` saying where it is seen. With `--source-text` (the
prototype's captured text), every quoted string in a capability's sources must be on the
prototype.

Layer rule: reads files on disk only; no git/gh/network.

    python3 grounding_check.py --manifest <seed-manifest.yaml> [--proposals-dir <dir>] \
        [--product-base <product_base>] [--source-text <file or folder of .txt> ...]

Prints {ok, errors[], capabilities} JSON. Exit 0 when every capability is grounded,
1 otherwise, 2 on usage/parse error.
"""

import argparse
import glob
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("grounding_check.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)


QUOTE = re.compile(r"[\"“]([^\"“”]{4,})[\"”]")
WEB = re.compile(r"https?://\S+")
MARKS = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", "\u00a0": " "})


def norm(text):
    return re.sub(r"\s+", " ", text.translate(MARKS)).strip().lower()


def sources_of(path):
    """The lines of a page's `## Sources` section, or None when it has none."""
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return None
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


def check_pages(seed, model, source_text, errors):
    """The domain page names its research; each added capability page names where it is seen."""
    domains = [d for d in (seed.get("domains") or []) if isinstance(d, dict)] or [seed.get("domain") or {}]
    for dom in domains:
        check_domain_page(dom, model, errors)
    check_capability_pages(seed, model, source_text, errors)


def check_domain_page(dom, model, errors):
    doc = str(dom.get("doc") or "")
    if doc:
        path = os.path.join(model, doc[len("product-os/"):] if doc.startswith("product-os/") else doc)
        src = sources_of(path)
        if src is None:
            errors.append(f"domain page {doc}: no `## Sources` — name the shelf it matched or the research "
                          f"that shows the world recognises it (C5)")
        elif not any(WEB.search(l) or "shelf" in l.lower() for l in src):
            errors.append(f"domain page {doc}: its sources name no shelf and no research link — a domain is "
                          f"never a name made up for one product (C5)")


def check_capability_pages(seed, model, source_text, errors):
    for cap in (seed.get("spine_delta") or {}).get("capabilities") or []:
        if not isinstance(cap, dict) or not cap.get("doc"):
            continue
        path = os.path.join(model, str(cap["doc"]))
        src = sources_of(path)
        if not src:
            errors.append(f"capability page {cap['doc']}: no `## Sources` saying where it is seen (C5)")
            continue
        if source_text is not None:
            screen = [l for l in src if not re.search(r"\b(shelf|proposal)\b", l, re.I)]
            for q in QUOTE.findall("\n".join(screen)):
                if norm(q) not in source_text:
                    errors.append(f"capability page {cap['doc']}: \"{q[:80]}\" is not on the prototype")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check /vision seed grounding.")
    ap.add_argument("--manifest", required=True, help="seed-manifest.yaml path")
    ap.add_argument("--proposals-dir", default=None,
                    help="folder where propose-kb-node proposals live (to confirm existence)")
    ap.add_argument("--product-base", default=None,
                    help="the live model's base (its product-os/ holds the pages): check their sources")
    ap.add_argument("--source-text", action="append", default=[],
                    help="the prototype's captured text, a file or a folder of .txt (repeatable)")
    args = ap.parse_args(argv)

    try:
        with open(args.manifest, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh) or {}
    except OSError as exc:
        sys.stderr.write(f"grounding_check.py: cannot read manifest: {exc}\n")
        sys.exit(2)
    except yaml.YAMLError as exc:
        sys.stderr.write(f"grounding_check.py: manifest parse error: {exc}\n")
        sys.exit(2)

    seed = doc.get("seed", doc) if isinstance(doc, dict) else {}
    caps = seed.get("capabilities") or []
    errors = []
    report = []

    if not caps:
        errors.append("manifest lists no capabilities — /vision seeds at least one")

    listed = {str(c.get("id")) for c in caps if isinstance(c, dict)}
    delta = seed.get("spine_delta") or {}
    touched = [str(c.get("id")) for c in delta.get("capabilities") or [] if isinstance(c, dict)]
    touched += [str(u.get("id")) for u in delta.get("updates") or []
                if isinstance(u, dict) and u.get("kind") == "capability"]
    for cid in dict.fromkeys(touched):
        if cid not in listed:
            errors.append(f"capability '{cid}' is added or changed by this run but not listed in the "
                          f"manifest's capabilities — record its KB shelf or proposal (C5)")

    for cap in caps:
        name = cap.get("name") or cap.get("id") or "<unnamed>"
        grounding = cap.get("grounding") or {}
        shelf = grounding.get("kb_shelf")
        proposal = grounding.get("proposal")
        status = "ungrounded"
        if shelf:
            status = f"shelf: {shelf}"
        elif proposal:
            # confirm the proposal file is real
            candidate = proposal
            if args.proposals_dir and not os.path.isabs(proposal):
                candidate = os.path.join(args.proposals_dir, os.path.basename(proposal))
            if os.path.isfile(candidate) or os.path.isfile(proposal):
                status = f"proposal: {proposal}"
            else:
                errors.append(f"capability '{name}': proposal named but file not found "
                              f"({proposal})")
                status = "proposal-missing"
        else:
            errors.append(f"capability '{name}': neither a KB shelf match nor a "
                          f"KB-node proposal — ungrounded (C5/F3)")
        report.append({"name": name, "grounding": status})

    if args.product_base:
        text = None
        if args.source_text:
            parts = []
            for t in args.source_text:
                paths = glob.glob(os.path.join(t, "**", "*.txt"), recursive=True) if os.path.isdir(t) else [t]
                for p in paths:
                    with open(p, encoding="utf-8", errors="ignore") as fh:
                        parts.append(fh.read())
            text = norm("\n".join(parts))
        check_pages(seed, os.path.join(args.product_base, "product-os"), text, errors)

    result = {"ok": not errors, "errors": errors, "capabilities": report}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
