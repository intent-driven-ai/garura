#!/usr/bin/env python3
"""check_journeys.py — are a prototype's journeys complete, and do they cover it? (/intent, C15)

The walk-prototype skill writes `journeys.yaml`: who uses the prototype, what each sets out to
do, every step and what it showed, and what they end with. This script checks the record
mechanically; whether a journey is *meaningful* stays with the agent.

    python3 check_journeys.py --journeys <working>/journeys.yaml \
        --source-manifest <working>/source-manifest-<name>.json \
        --evidence-dir <evidence>/journeys [--draft <working>/intent-draft.yaml] \
        --out <working>/journeys-check.json

Checks:
- at least one journey; each has `who`, `sets_out_to`, `ends_with`, and two or more steps;
- each step names what was done (`do`) and what it showed (`shows`), and its `view` files exist
  in the evidence folder;
- coverage — every view the capture kept (the manifest's `view-…` files) is named by some step's
  `covers`, or listed in `not_walked` with why;
- main sections — `main_sections` names the prototype's main sections (its top menu, tabs, the
  parts of its first screen), and each one is the `section` of at least one journey: no main
  section is only a step on another section's journey;
- with `--draft`, every business intent names the journey it came from (`from_journey`), and
  every main section has a business intent of its own — one whose journey serves that
  section, not folded into another section's intent (C15, C17).

Exit 0 clean; 1 gaps (listed in the report); 2 cannot read an input. Standard library + PyYAML.
"""
import argparse
import json
import os
import sys

import yaml


def check(doc, manifest, evidence_dir, draft=None):
    gaps = []
    journeys = (doc or {}).get("journeys") or []
    if not journeys:
        gaps.append("no journeys — a prototype is understood by using it")
    covered = set()
    for j in journeys:
        jid = j.get("id") or "(no id)"
        for key in ("who", "sets_out_to", "ends_with"):
            if not str(j.get(key) or "").strip():
                gaps.append(f"{jid}: no `{key}`")
        steps = j.get("steps") or []
        if len(steps) < 2:
            gaps.append(f"{jid}: fewer than two steps")
        for n, s in enumerate(steps, 1):
            if not str(s.get("do") or "").strip() or not str(s.get("shows") or "").strip():
                gaps.append(f"{jid} step {n}: needs what was done and what it showed")
            for f in s.get("view") or []:
                if not os.path.isfile(os.path.join(evidence_dir, f)):
                    gaps.append(f"{jid} step {n}: view file {f} is not in the evidence")
            covered |= set(s.get("covers") or [])
    sections = [str(x).strip() for x in (doc or {}).get("main_sections") or [] if str(x).strip()]
    if journeys and not sections:
        gaps.append("no `main_sections` — name the prototype's main sections (its menu, tabs, the parts "
                    "of its first screen)")
    section_of = {j.get("id"): str(j.get("section") or "").strip() for j in journeys}
    for sec in sections:
        if sec not in section_of.values():
            gaps.append(f"main section {sec!r} is no journey's `section` — every main section is a "
                        f"journey's goal of its own")
    for jid, sec in section_of.items():
        if sec and sec not in sections:
            gaps.append(f"{jid}: its section {sec!r} is not one of `main_sections`")
    kept = sorted({os.path.splitext(f)[0] for f in manifest.get("files", []) if f.startswith("view-")})
    not_walked = {str(n.get("view")): str(n.get("why") or "").strip()
                  for n in (doc or {}).get("not_walked") or []}
    for v in kept:
        if v not in covered and not not_walked.get(v):
            gaps.append(f"view {v} is on no journey and not listed as not walked (with why)")
    if draft is not None:  # every business intent comes from a journey (C15)
        ids = {j.get("id") for j in journeys}
        for bi in (draft or {}).get("intents") or []:
            if bi.get("from_journey") not in ids:
                gaps.append(f"business intent {bi.get('id')}: names no journey it came from "
                            f"(`from_journey`)")
        served = {section_of.get(bi.get("from_journey")) for bi in (draft or {}).get("intents") or []}
        for sec in sections:
            if sec not in served:
                gaps.append(f"main section {sec!r} has no business intent of its own — each main "
                            f"section's need is its own intent, never folded into another's")
    return gaps, {"journeys": len(journeys), "views": len(kept),
                  "covered": len([v for v in kept if v in covered]), "not_walked": len(not_walked)}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a prototype's journeys.")
    ap.add_argument("--journeys", required=True)
    ap.add_argument("--source-manifest", required=True)
    ap.add_argument("--evidence-dir", required=True)
    ap.add_argument("--draft", help="the intent draft: every business intent names its journey")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.journeys, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
        draft = None
        if args.draft:
            with open(args.draft, encoding="utf-8") as fh:
                draft = yaml.safe_load(fh)
        with open(args.source_manifest, encoding="utf-8") as fh:
            manifest = json.load(fh)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        sys.stderr.write(f"check_journeys.py: cannot read an input: {exc}\n")
        return 2
    gaps, counts = check(doc, manifest, args.evidence_dir, draft)
    report = {"ok": not gaps, "gaps": gaps, **counts}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0 if not gaps else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
