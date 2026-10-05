#!/usr/bin/env python3
"""
check_model_agreement.py — the independent read check for /next (C13, F10, #533).

Not a play step: it runs inside scripts/test_derive_candidates.py (the play's quick
scenario validation). Re-running scan_model.py could only prove the scanner agrees
with itself; this check proves the snapshot agrees with the
MODEL: it carries its own minimal reader over `_spine.yaml` and the slice lens
folders — it does not import scan_model.py — and compares what it reads against
the snapshot /next ranked on.

Asserts:
  - profile state on the spine == snapshot profile state;
  - every spine slice is in the snapshot with the same status, order, effort and
    depends_on, and the snapshot holds no slice the spine does not index;
  - per slice, the seven lens docs (`lens/<type>.md`) present on disk == the
    snapshot's lens presence;
  - every spine epic is in the snapshot (under its slice) with the same status;
  - every spine capability's detail == the snapshot's.
A tree with files but no spine must be recorded in the snapshot as
spine_exists=false.

Layer rule: reads files on disk only; no git/gh/network.

    python3 check_model_agreement.py --product-base <pb> --state <model-state.json>

Prints {ok, gaps[]} JSON. Exit 0 agree, 1 disagreement, 2 usage error.
"""

import argparse
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("check_model_agreement.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

LENS_DOCS = ("quality", "ux", "agentic", "marketing", "architecture", "run", "measure")


def lower(v):
    return v.strip().lower() if isinstance(v, str) else ""


def dicts(v):
    return [x for x in v if isinstance(x, dict)] if isinstance(v, list) else []


def main(argv=None):
    ap = argparse.ArgumentParser(description="Independent spine/snapshot agreement check.")
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--state", required=True)
    try:
        args = ap.parse_args(argv)
    except SystemExit:
        return 2

    try:
        with open(args.state, encoding="utf-8") as fh:
            state = json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"check_model_agreement.py: cannot read state: {exc}\n")
        return 2

    gaps = []
    root = os.path.join(args.product_base, "product-os")
    spine_file = os.path.join(root, "_spine.yaml")

    if not os.path.isfile(spine_file):
        if os.path.isdir(root) and state.get("spine_exists") is not False \
                and state.get("model_exists"):
            gaps.append("F10: the model has no spine but the snapshot does not record "
                        "spine_exists=false")
        print(json.dumps({"ok": not gaps, "gaps": gaps}, indent=2))
        return 0 if not gaps else 1

    with open(spine_file, encoding="utf-8") as fh:
        spine = yaml.safe_load(fh) or {}

    # ---- profile -----------------------------------------------------------
    spine_prof = lower((spine.get("profile") or {}).get("state")) if isinstance(
        spine.get("profile"), dict) else ""
    snap_prof = lower((state.get("profile") or {}).get("state"))
    if spine_prof != snap_prof:
        gaps.append(f"F10: profile state — spine '{spine_prof or None}', "
                    f"snapshot '{snap_prof or None}'")

    snap_domains = state.get("domains") or []
    snap_slices = {}
    for d in snap_domains:
        for s in d.get("slices") or []:
            snap_slices[s.get("id")] = s

    slug_of = {d.get("id"): (d.get("slug") or d.get("id")) for d in dicts(spine.get("domains"))}

    # ---- slices + lens docs --------------------------------------------------
    spine_ids = set()
    for s in dicts(spine.get("slices")):
        sid = s.get("id")
        spine_ids.add(sid)
        snap = snap_slices.get(sid)
        if snap is None:
            if sid in (state.get("orphan_slices") or []):
                continue
            gaps.append(f"F10: spine slice '{sid}' is missing from the snapshot")
            continue
        for field in ("order", "effort"):
            if s.get(field) != snap.get(field):
                gaps.append(f"F10: slice '{sid}' {field} — spine {s.get(field)!r}, "
                            f"snapshot {snap.get(field)!r}")
        if lower(s.get("status")) != lower(snap.get("status")):
            gaps.append(f"F10: slice '{sid}' status — spine '{lower(s.get('status'))}', "
                        f"snapshot '{lower(snap.get('status'))}'")
        if sorted(s.get("depends_on") or []) != sorted(snap.get("depends_on") or []):
            gaps.append(f"F10: slice '{sid}' depends_on disagrees with the spine")
        slug = slug_of.get(s.get("domain_ref"))
        if slug:
            lens_dir = os.path.join(root, slug, "slices", sid, "lens")
            snap_lenses = snap.get("lenses") or {}
            for lt in LENS_DOCS:
                on_disk = os.path.isfile(os.path.join(lens_dir, lt + ".md"))
                if on_disk != bool(snap_lenses.get(lt)):
                    gaps.append(f"F10: slice '{sid}' lens '{lt}.md' — on disk {on_disk}, "
                                f"snapshot {bool(snap_lenses.get(lt))}")
    for sid in sorted(set(snap_slices) - spine_ids, key=str):
        gaps.append(f"F10: snapshot slice '{sid}' is not in the spine slices index")

    # ---- epics ---------------------------------------------------------------
    for e in dicts(spine.get("epics")):
        ref = e.get("slice_ref")
        sid = ref.split("/")[-1] if isinstance(ref, str) else ref
        snap = snap_slices.get(sid)
        snap_e = next((x for x in (snap or {}).get("epics") or []
                       if x.get("id") == e.get("id")), None)
        if snap_e is None:
            gaps.append(f"F10: spine epic '{e.get('id')}' (slice '{sid}') is missing "
                        "from the snapshot")
        elif lower(e.get("status")) != lower(snap_e.get("status")):
            gaps.append(f"F10: epic '{e.get('id')}' status — spine "
                        f"'{lower(e.get('status'))}', snapshot '{lower(snap_e.get('status'))}'")

    # ---- capability detail ---------------------------------------------------
    snap_caps = {}
    for d in snap_domains:
        for c in d.get("capabilities") or []:
            snap_caps[(d.get("id"), c.get("id"))] = c
    for c in dicts(spine.get("capabilities")):
        key = (c.get("domain"), c.get("id"))
        if c.get("domain") not in slug_of:
            continue
        snap_c = snap_caps.get(key)
        spine_detail = lower(c.get("detail")) or "directional"
        if snap_c is None:
            gaps.append(f"F10: spine capability '{c.get('id')}' is missing from the snapshot")
        elif spine_detail != lower(snap_c.get("detail")):
            gaps.append(f"F10: capability '{c.get('id')}' detail — spine '{spine_detail}', "
                        f"snapshot '{lower(snap_c.get('detail'))}'")

    print(json.dumps({"ok": not gaps, "gaps": gaps}, indent=2))
    return 0 if not gaps else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
