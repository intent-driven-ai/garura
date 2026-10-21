#!/usr/bin/env python3
"""read_intents.py — read the business intents a /discover-domains run starts from (#637, C10).

/discover-domains may start from business intents — named by id, or through /discover-intent's save record
(`intent-manifest.json`) — and from whatever the product model already holds for them. This
reads, for each named intent, its page (title, outcome, why, stage) and, from the spine, every
domain and capability already linked to it — under a domain or in the holding folder. It
never refuses over another play's work (ontology v4: nothing waits): a `proposed` intent is
accepted like a `confirmed` one (it is never checked for workability), and a missing page or
an unreadable spine is a warning in the record, not a stop.

Layer rule: reads files on disk only; no git/gh/network.

    python3 read_intents.py --product-base <product_base> \
        ( --intent <id> [--intent <id> ...] | --intent-manifest <intent-manifest.json> ) \
        --out <working>/intents.json

Prints and writes {intents[], capabilities[], domains[], warnings[]}. Exit 0 always once
the arguments parse — even with warnings; 2 only on a usage error.
"""
import argparse
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("read_intents.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

HOLDING = "capabilities/"
FIELD = re.compile(r"^\*\*(?P<k>Outcome|Why|Stage):\*\*\s*(?P<v>.*)$")


def read_page(path):
    """Title, outcome, why and stage from an intent page, as /discover-intent writes it."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    out = {"title": next((line[2:].strip() for line in lines if line.startswith("# ")), "")}
    for line in lines:
        m = FIELD.match(line.strip())
        if m:
            out[m.group("k").lower()] = m.group("v").strip()
    stage = out.get("stage", "")
    out["stage"] = next((s for s in ("proposed", "confirmed", "met", "dropped") if stage.startswith(s)), "unknown")
    return out


def ids_from_manifest(path, warnings):
    try:
        with open(path, encoding="utf-8") as fh:
            man = json.load(fh)
        return [str(i["id"]) for i in man.get("intents") or [] if isinstance(i, dict) and i.get("id")]
    except (OSError, ValueError, KeyError, AttributeError) as exc:
        warnings.append(f"could not read /discover-intent's save record {path}: {exc.__class__.__name__}")
        return []


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read the business intents a /discover-domains run starts from.")
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--intent", action="append", default=[], help="a business intent id; repeatable")
    ap.add_argument("--intent-manifest", help="/discover-intent's intent-manifest.json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    warnings = []
    ids = list(args.intent)
    if args.intent_manifest:
        ids += [i for i in ids_from_manifest(args.intent_manifest, warnings) if i not in ids]
    model = os.path.join(args.product_base, "product-os")
    spine = {}
    spine_path = os.path.join(model, "_spine.yaml")
    if os.path.isfile(spine_path):
        try:
            with open(spine_path, encoding="utf-8") as fh:
                spine = yaml.safe_load(fh) or {}
        except (OSError, yaml.YAMLError) as exc:
            warnings.append(f"could not read the spine: {exc.__class__.__name__}")
        if not isinstance(spine, dict):
            warnings.append("the spine is not a mapping — read as empty")
            spine = {}

    intents = []
    for iid in ids:
        page = os.path.join(model, "intents", f"{iid}.md")
        rec = {"id": iid, "path": os.path.relpath(page, model).replace(os.sep, "/"), "exists": os.path.isfile(page)}
        if rec["exists"]:
            try:
                rec.update(read_page(page))
            except (OSError, UnicodeDecodeError) as exc:
                rec.update({"title": "", "stage": "unknown"})
                warnings.append(f"intent `{iid}`: its page could not be read ({exc.__class__.__name__})")
            rec["accepted"] = rec["stage"] != "dropped"
            if rec["stage"] == "dropped":
                warnings.append(f"intent `{iid}` is dropped — /discover-domains does not build on it")
        else:
            rec["accepted"] = False
            warnings.append(f"intent `{iid}` has no page at {rec['path']} — left for alignment")
        intents.append(rec)

    wanted = {i["id"] for i in intents if i["accepted"]}
    caps = []
    for c in spine.get("capabilities") or []:
        if not isinstance(c, dict):
            continue
        linked = sorted(wanted & {str(x) for x in c.get("intents") or []})
        if linked:
            doc = str(c.get("doc") or "")
            caps.append({"id": str(c.get("id")), "domain": str(c.get("domain") or ""), "doc": doc,
                         "detail": c.get("detail"), "intents": linked,
                         "in_holding_folder": doc.startswith(HOLDING) or not c.get("domain")})
    domains = [{"id": str(d.get("id")), "doc": str(d.get("doc") or ""), "detail": d.get("detail"),
                "intents": sorted(wanted & {str(x) for x in d.get("intents") or []})}
               for d in spine.get("domains") or [] if isinstance(d, dict)]

    record = {"intents": intents, "capabilities": caps, "domains": domains, "warnings": warnings}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
