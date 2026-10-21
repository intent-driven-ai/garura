#!/usr/bin/env python3
"""
grounding_check.py — assert every domain /vision wrote is grounded, and nothing else was written (C5).

/vision writes domains only (ADR 043 part 2) and never invents one. Each domain either matched
a KB shelf (recorded by search-kb) or was raised as a propose-kb-node proposal that names it as
the world already names it. This script reads the seed manifest author-vision-seed wrote and
asserts that:

  - the manifest lists at least one domain (`domains`, or the older single `domain`), and each
    carries its grounding — a `kb_shelf`, or a `proposal` whose file exists on disk;
  - every domain the spine-delta adds or updates is listed with its grounding;
  - the spine-delta adds no capability, functionality, slice or epic — those are not /vision's.

With `--product-base`, it also reads each domain page (#689): it must end with `## Sources`
naming the shelf it matched or the research links that show the world recognises it — a domain
is never a name made up for one product.

Layer rule: reads files on disk only; no git/gh/network.

    python3 grounding_check.py --manifest <seed-manifest.yaml> [--proposals-dir <dir>] \
        [--product-base <product_base>]

Prints {ok, errors[], domains} JSON. Exit 0 when every domain is grounded and nothing else was
written, 1 otherwise, 2 on usage/parse error.
"""

import argparse
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("grounding_check.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

WEB = re.compile(r"https?://\S+")
NOT_MINE = ("capabilities", "functionalities", "slices", "epics")


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


def check_domain_page(dom, model, errors):
    doc = str(dom.get("doc") or "")
    if not doc:
        return
    path = os.path.join(model, doc[len("product-os/"):] if doc.startswith("product-os/") else doc)
    src = sources_of(path)
    if src is None:
        errors.append(f"domain page {doc}: no `## Sources` — name the shelf it matched or the research "
                      f"that shows the world recognises it (C5)")
    elif not any(WEB.search(line) or "shelf" in line.lower() for line in src):
        errors.append(f"domain page {doc}: its sources name no shelf and no research link — a domain is "
                      f"never a name made up for one product (C5)")


def grounding_of(dom, proposals_dir, errors):
    name = dom.get("name") or dom.get("id") or "<unnamed>"
    grounding = dom.get("grounding") or {}
    if grounding.get("kb_shelf"):
        return f"shelf: {grounding['kb_shelf']}"
    proposal = grounding.get("proposal")
    if proposal:
        candidate = proposal
        if proposals_dir and not os.path.isabs(proposal):
            candidate = os.path.join(proposals_dir, os.path.basename(proposal))
        if os.path.isfile(candidate) or os.path.isfile(proposal):
            return f"proposal: {proposal}"
        errors.append(f"domain '{name}': proposal named but file not found ({proposal})")
        return "proposal-missing"
    errors.append(f"domain '{name}': neither a KB shelf match nor a KB-node proposal — ungrounded (C5)")
    return "ungrounded"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check /vision's domains are grounded.")
    ap.add_argument("--manifest", required=True, help="seed-manifest.yaml path")
    ap.add_argument("--proposals-dir", default=None,
                    help="folder where propose-kb-node proposals live (to confirm existence)")
    ap.add_argument("--product-base", default=None,
                    help="the live model's base (its product-os/ holds the pages): check their sources")
    args = ap.parse_args(argv)

    try:
        with open(args.manifest, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh) or {}
    except OSError as exc:
        sys.stderr.write(f"grounding_check.py: cannot read manifest: {exc}\n")
        return 2
    except yaml.YAMLError as exc:
        sys.stderr.write(f"grounding_check.py: manifest parse error: {exc}\n")
        return 2

    seed = doc.get("seed", doc) if isinstance(doc, dict) else {}
    domains = [d for d in (seed.get("domains") or []) if isinstance(d, dict)]
    if not domains and isinstance(seed.get("domain"), dict):
        domains = [seed["domain"]]
    errors, report = [], []
    if not domains:
        errors.append("manifest lists no domain — /vision writes at least one")

    delta = seed.get("spine_delta") or {}
    for key in NOT_MINE:
        if delta.get(key):
            errors.append(f"the spine-delta adds `{key}` — /vision writes domains only (ADR 043)")
    listed = {str(d.get("id")) for d in domains}
    touched = [str(d.get("id")) for d in delta.get("domains") or [] if isinstance(d, dict)]
    touched += [str(u.get("id")) for u in delta.get("updates") or []
                if isinstance(u, dict) and u.get("kind") == "domain"]
    for did in dict.fromkeys(touched):
        if did not in listed:
            errors.append(f"domain '{did}' is added or changed by this run but not listed in the manifest's "
                          f"domains — record its KB shelf or proposal (C5)")

    for dom in domains:
        report.append({"name": dom.get("name") or dom.get("id"),
                       "grounding": grounding_of(dom, args.proposals_dir, errors)})
        if args.product_base:
            check_domain_page(dom, os.path.join(args.product_base, "product-os"), errors)

    result = {"ok": not errors, "errors": errors, "domains": report}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
