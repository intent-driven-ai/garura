#!/usr/bin/env python3
"""
rollup_box.py — roll the run's capabilities' NFR needs into the product profile box.

The deterministic core of /discover-capabilities's governance. The enrich skill made the
judgment call (what level each concrete need implies); this script does the pure
threshold math the orchestrator must never re-reason. One run details every target
capability (#615), so it takes one enrich manifest per capability:

  - Monotonic-up: each dimension's committed level becomes max(current box, every need).
    A dimension is NEVER lowered (C7/F6) — structurally guaranteed by max().
  - Measured against the box as it stood at the START of the run: each capability is
    compared with the starting box, never with a box another capability in the same run
    already raised, so no capability's box-move hides behind another's.
  - Establish vs move (the box-state distinction):
      * state == directional -> ESTABLISH the box from the rolled-up levels and firm
        it to `set`. No box-moves, no decisions (the directional box was never a
        committed ceiling).
      * state == set -> for each capability, any dimension whose need exceeds the
        starting level, or any regime not in the starting compliance list, is an
        OUT-OF-BOX move -> one box_move per capability per dimension (it names the
        capability), each needing its own product-level decision; out_of_box is flagged
        (the play halts for approval).
  - Never writes `locked` (that is /shape-scope's gate).

Layer rule: reads the current profile (from the live spine `_spine.yaml`) + the enrich
manifests from disk; writes a proposed profile + a roll-up report. No git/gh/network.

    python3 rollup_box.py --spine <_spine.yaml> \
                          --enrich-manifest <cap-a/enrich-manifest.yaml> [--enrich-manifest ...] \
                          --out-profile <proposed-profile.yaml> --out-report <rollup.json>

Exit 0 on success, 2 on usage/parse error (or, with more than one manifest, a manifest
with no capability_ref or two manifests for one capability). A non-zero exit never means
"out of box" — out_of_box is reported in the JSON; halting is the play's policy.
"""

import argparse
import json
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("rollup_box.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

SCALE = ["none", "low", "medium", "high", "xhigh"]


def rank(level):
    """Index on the none<low<medium<high<xhigh scale; unknown -> none (0)."""
    try:
        return SCALE.index((level or "none").strip().lower())
    except ValueError:
        return 0


def load(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Roll NFR needs into the profile box.")
    ap.add_argument("--spine", required=True, help="live _spine.yaml (its profile block is the box)")
    ap.add_argument("--enrich-manifest", required=True, action="append",
                    help="enrich-manifest.yaml of one target capability (repeat once per capability)")
    ap.add_argument("--out-profile", required=True, help="where to write the proposed profile")
    ap.add_argument("--out-report", required=True, help="where to write the roll-up report JSON")
    args = ap.parse_args(argv)

    try:
        spine_doc = load(args.spine)
        man_docs = [load(p) for p in args.enrich_manifest]
    except (OSError, yaml.YAMLError) as exc:
        sys.stderr.write(f"rollup_box.py: cannot read input: {exc}\n")
        return 2

    profile = (spine_doc.get("profile") or {}) if isinstance(spine_doc, dict) else {}
    enriches = []
    for path, doc in zip(args.enrich_manifest, man_docs):
        enrich = doc.get("enrich", doc) if isinstance(doc, dict) else {}
        enriches.append(enrich if isinstance(enrich, dict) else {})
    refs = [e.get("capability_ref") for e in enriches]
    if len(enriches) > 1:
        if not all(isinstance(r, str) and r for r in refs):
            sys.stderr.write("rollup_box.py: with more than one manifest, each must name its "
                             "capability_ref\n")
            return 2
        if len(set(refs)) != len(refs):
            sys.stderr.write("rollup_box.py: two manifests name the same capability\n")
            return 2

    state_before = (profile.get("state") or "directional").strip().lower()
    establishing = state_before == "directional"
    start_nfr = dict(profile.get("nfr") or {})
    start_compliance = list(profile.get("compliance") or [])
    nfr = {dim: dict(spec) if isinstance(spec, dict) else {"level": spec}
           for dim, spec in start_nfr.items()}
    compliance = list(start_compliance)

    box_moves = []
    compliance_added = []

    for ref, enrich in zip(refs, enriches):
        implied = enrich.get("implied_levels") or {}
        # --- monotonic-up per dimension, measured against the STARTING box -------------
        for dim, spec in implied.items():
            if isinstance(spec, dict):
                need_level, need_gate = spec.get("level"), spec.get("gate")
            else:                       # tolerate a bare level string
                need_level, need_gate = spec, None
            start_level = (start_nfr.get(dim) or {}).get("level") \
                if isinstance(start_nfr.get(dim), dict) else start_nfr.get(dim)
            cur = nfr.get(dim) or {}
            if rank(need_level) > rank(start_level) and not establishing:
                move = {"dimension": dim, "from": start_level or "none", "to": need_level}
                if ref:
                    move = {"capability": ref, **move}
                box_moves.append(move)
            if rank(need_level) > rank(cur.get("level")):
                nfr[dim] = {"level": need_level, "gate": need_gate or cur.get("gate") or ""}
            else:
                # need is within the box — keep the (higher-or-equal) current level
                nfr[dim] = {"level": cur.get("level"), "gate": cur.get("gate") or need_gate or ""}

        # --- compliance union, measured against the STARTING list ----------------------
        for regime in enrich.get("compliance") or []:
            if regime not in compliance:
                compliance.append(regime)
                compliance_added.append(regime)
            if regime not in start_compliance and not establishing:
                move = {"dimension": f"compliance:{regime}", "from": "absent", "to": "required"}
                if ref:
                    move = {"capability": ref, **move}
                box_moves.append(move)

    state_after = "set"             # /discover-capabilities always firms to set, never locked
    out_of_box = (not establishing) and bool(box_moves)

    proposed = dict(profile)
    proposed["state"] = state_after
    proposed["nfr"] = nfr
    proposed["compliance"] = compliance

    with open(args.out_profile, "w", encoding="utf-8") as fh:
        yaml.safe_dump({"profile": proposed}, fh, sort_keys=False)

    report = {
        "capabilities": [r for r in refs if r],
        "state_before": state_before,
        "state_after": state_after,
        "establishing": establishing,
        "out_of_box": out_of_box,
        "box_moves": box_moves,
        "compliance_added": compliance_added,
    }
    with open(args.out_report, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
