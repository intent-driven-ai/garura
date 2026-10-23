#!/usr/bin/env python3
"""
grounding_check.py — assert every domain /discover-domains wrote is grounded, and nothing else was written (C5).

/discover-domains writes domains only (ADR 043 part 2) and never invents one. Each domain either matched
a KB shelf (recorded by find-work-placement) or was raised as a propose-kb-node proposal that names it as
the world already names it. This script reads the seed manifest author-domains wrote and
asserts that:

  - the manifest lists at least one domain (`domains`, or the older single `domain`), and each
    carries its grounding — a `kb_shelf`, or a `proposal` whose file exists on disk;
  - every domain the spine-delta adds or updates is listed with its grounding;
  - the spine-delta adds no capability, feature, slice or epic — those are not /discover-domains's.

With `--product-base`, it also reads each domain page (#689): it must end with `## Sources`
naming the shelf it matched or the research links that show the world recognises it — a domain
is never a name made up for one product.

With `--journeys` (a prototype's capture, C12), it also checks the manifest's `areas`: every main
section of the prototype (`main_sections` in the capture's journeys) sits in a domain the
manifest lists, with the line from that domain's shelf or research (`evidence`) that shows the
field does this kind of work, and where it is from (`source`: a link or the shelf). Every domain
the run adds holds at least one main section: a field named after one feature many products
share — and no main section's work — is not a domain the product sits in.

Layer rule: reads files on disk only; no git/gh/network.

    python3 grounding_check.py --manifest <seed-manifest.yaml> [--proposals-dir <dir>] \
        [--product-base <product_base>] [--journeys <capture>/journeys.yaml]

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
NOT_MINE = ("capabilities", "features", "slices", "epics")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model_names  # noqa: E402  (stamped from create-play/references)


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


def check_areas(seed, domains, added, journeys_path, errors):
    """Every main section sits in a listed domain, by that domain's own research; every added
    domain holds one."""
    try:
        with open(journeys_path, encoding="utf-8") as fh:
            sections = [str(x).strip() for x in (yaml.safe_load(fh) or {}).get("main_sections") or []
                        if str(x).strip()]
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read journeys: {exc}")
    ids = {str(d.get("id")) for d in domains}
    areas = [a for a in seed.get("areas") or [] if isinstance(a, dict)]
    held = {}
    for a in areas:
        sec, dom = str(a.get("section") or "").strip(), str(a.get("domain") or "").strip()
        if dom not in ids:
            errors.append(f"area {sec!r}: its domain {dom!r} is not a domain the manifest lists (C12)")
            continue
        if not str(a.get("evidence") or "").strip():
            errors.append(f"area {sec!r}: no `evidence` — quote the line from {dom}'s shelf or research "
                          f"that shows the field does this kind of work (C12)")
        source = str(a.get("source") or "")
        if not (WEB.search(source) or "shelf" in source.lower()):
            errors.append(f"area {sec!r}: its `source` is no research link and no shelf (C12)")
        held.setdefault(sec, set()).add(dom)
    for sec in sections:
        if sec not in held:
            errors.append(f"main section {sec!r} sits in no domain — find, by research, the field that "
                          f"does this kind of work; the product may sit in more than one (C12)")
    holding = {d for doms in held.values() for d in doms}
    for did in added:
        if did not in holding:
            errors.append(f"domain {did!r} holds no main section of the prototype — a domain the product sits in holds at least one; a field named after "
                          f"one feature many products share is not a domain the product sits in (C5)")
    return {s: sorted(held.get(s, [])) for s in sections}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check /discover-domains's domains are grounded.")
    ap.add_argument("--manifest", required=True, help="seed-manifest.yaml path")
    ap.add_argument("--proposals-dir", default=None,
                    help="folder where propose-kb-node proposals live (to confirm existence)")
    ap.add_argument("--product-base", default=None,
                    help="the live model's base (its product-os/ holds the pages): check their sources")
    ap.add_argument("--journeys", default=None,
                    help="a prototype capture's journeys.yaml: check every main section sits in a domain")
    args = ap.parse_args(argv)

    try:
        with open(args.manifest, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh) or {}
        model_names.check_model(doc, args.manifest)
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
        errors.append("manifest lists no domain — /discover-domains writes at least one")

    delta = seed.get("spine_delta") or {}
    for key in NOT_MINE:
        if delta.get(key):
            errors.append(f"the spine-delta adds `{key}` — /discover-domains writes domains only (ADR 043)")
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

    areas = None
    if args.journeys:
        added = [str(d.get("id")) for d in delta.get("domains") or [] if isinstance(d, dict)]
        try:
            areas = check_areas(seed, domains, added, args.journeys, errors)
        except ValueError as exc:
            sys.stderr.write(f"grounding_check.py: {exc}\n")
            return 2

    result = {"ok": not errors, "errors": errors, "domains": report}
    if areas is not None:
        result["areas"] = areas
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
