#!/usr/bin/env python3
"""prepare.py — the brief the rebuild works from: the intents and the model, nothing else.

    python3 prepare.py --product-os <project>/.garura/product/product-os \
        --out <run>/brief [--prototype-name argus.html]

Copies the business intents (`intents/*.md`), the domain, capability and feature pages and
the spine. On the way it takes out what would let a builder find the prototype or the loop's
records: local links (the text stays, the path goes), absolute paths and `.garura/` paths, and
the prototype's file name. Web links stay — they are research sources. What it took out is
listed in `<out>/../brief-manifest.json`, with the counts of what the brief holds and its level:
`intents` (only intents), `domain`, `capabilities` or `features` (the deepest level present).

Exit 0 written; 2 the product model cannot be read. Standard library only. No git, no LLM.
"""
import argparse
import json
import os
import re
import shutil
import sys

PAGES = ("domain.md", "capability.md", "feature.md")
LOCAL_LINK = re.compile(r"\[([^\]]+)\]\((?!https?://)([^)]+)\)")
ABS_PATH = re.compile(r"(?<![\w.])(?:/(?:Users|private|tmp|home|var)/[^\s)\]`'\"]+|\.garura/[^\s)\]`'\"]+)")


def clean(text, prototype_names):
    """Take local links, paths and the prototype's name out of a page; say what went."""
    removed = []

    def unlink(m):
        removed.append(m.group(2))
        return m.group(1)

    text = LOCAL_LINK.sub(unlink, text)

    def unpath(m):
        removed.append(m.group(0))
        return "(path removed)"

    text = ABS_PATH.sub(unpath, text)
    for name in prototype_names:
        if name and name in text:
            removed.append(name)
            text = text.replace(name, "the prototype")
    return text, removed


def level_of(counts):
    for key in ("features", "capabilities", "domain"):
        if counts[key]:
            return key
    return "intents"


def prepare(product_os, out, prototype_names):
    if not os.path.isdir(product_os):
        raise OSError(f"no product model folder at {product_os}")
    if os.path.exists(out):
        shutil.rmtree(out)
    counts = {"intents": 0, "domain": 0, "capabilities": 0, "features": 0}
    kind_of = {"domain.md": "domain", "capability.md": "capabilities", "feature.md": "features"}
    removed, files = [], []
    for root, _dirs, names in os.walk(product_os):
        rel_root = os.path.relpath(root, product_os)
        for name in sorted(names):
            rel = os.path.normpath(os.path.join(rel_root, name))
            if rel.startswith("intents" + os.sep) and name.endswith(".md"):
                counts["intents"] += 1
            elif name in PAGES:
                counts[kind_of[name]] += 1
            elif rel != "_spine.yaml":
                continue
            with open(os.path.join(root, name), encoding="utf-8") as fh:
                text, gone = clean(fh.read(), prototype_names)
            dest = os.path.join(out, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8") as fh:
                fh.write(text)
            files.append(rel)
            removed += [{"file": rel, "removed": g} for g in gone]
    if not counts["intents"]:
        raise OSError(f"no business intents under {product_os}/intents")
    return {"brief": out, "level": level_of(counts), "counts": counts,
            "files": sorted(files), "removed": removed}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Make the rebuild's brief from a product model.")
    ap.add_argument("--product-os", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prototype-name", action="append", default=[],
                    help="a file name of the prototype to take out of the text (repeatable)")
    args = ap.parse_args(argv)
    try:
        manifest = prepare(os.path.abspath(args.product_os), os.path.abspath(args.out), args.prototype_name)
    except OSError as exc:
        sys.stderr.write(f"prepare.py: {exc}\n")
        return 2
    path = os.path.join(os.path.dirname(os.path.abspath(args.out)), "brief-manifest.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps({k: manifest[k] for k in ("level", "counts")} | {"removed": len(manifest["removed"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
