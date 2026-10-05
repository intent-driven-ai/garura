#!/usr/bin/env python3
"""
scan_model.py — read-only product-model state snapshot for /next (C1/C2/C13).

Walks {product_base}/product-os/ and emits ONE JSON snapshot of everything the
candidate derivation needs, read the way the model-writing plays write it
(ADR 026, direct-model-write):

  - the spine `_spine.yaml` is the index of record — profile state, domains
    (id + slug → folder), capability detail, slices (status / order / effort /
    depends_on), and epics (status / order / depends_on / issue_ref /
    surface_type / surface_verified);
  - lens presence is the slice's `lens/<type>.md` grounding docs — the seven
    lenses /measure lines up (quality, ux, agentic, marketing, architecture,
    run, measure);
  - a slice record is read only for what the spine does not carry (name,
    functionalities) — its own `status` is never read (it goes stale after
    /roadmap writes the spine).

Also records a content hash of the whole product-os tree — the model basis the
recommendation was derived from (carried into the evidence record).

A missing model is NOT an error — it is the /vision branch of the decision
tree: the snapshot says model_exists=false and exits 0. A product-os/ tree with
files but no spine is recorded as spine_exists=false (never read from legacy
per-node files) — the derivation reports it as an inconsistency.

Layer rule: reads files on disk only; no git/gh/network. Deterministic: same
tree, same snapshot (no timestamps, sorted everything).

    python3 scan_model.py --product-base <pb> --out <model-state.json>

Exit 0 always (scan errors are recorded in the snapshot's `scan_errors`),
2 on usage error.
"""

import argparse
import glob
import hashlib
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("scan_model.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

# The seven lens docs /measure lines up (measure/scripts/lines_up.py).
LENS_TYPES = ["quality", "ux", "agentic", "marketing", "architecture", "run", "measure"]


def load(path, errors):
    try:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"unreadable: {path} ({exc})")
        return {}


def tree_hash(root):
    """sha256 over sorted relative paths + bytes of every file under root."""
    h = hashlib.sha256()
    for path in sorted(glob.glob(os.path.join(root, "**", "*"), recursive=True)):
        if not os.path.isfile(path):
            continue
        rel = os.path.relpath(path, root)
        h.update(rel.encode("utf-8"))
        try:
            with open(path, "rb") as fh:
                h.update(fh.read())
        except OSError:
            h.update(b"<unreadable>")
    return "sha256:" + h.hexdigest()


def norm(value):
    return (value or "").strip().lower() if isinstance(value, str) else ""


def slice_id_of(ref):
    """The slice id from a slice_ref that may be 'domain/slice-id' or 'slice-id'."""
    return ref.split("/")[-1] if isinstance(ref, str) and ref else ref


def as_list(value):
    return [x for x in value if isinstance(x, dict)] if isinstance(value, list) else []


def scan_slice(root, slug, entry, epics_by_slice, errors):
    sid = entry.get("id")
    slice_dir = os.path.join(root, slug, "slices", sid)
    record_rel = entry.get("record") or os.path.join(slug, "slices", sid + ".yaml")
    record_path = os.path.join(root, record_rel)
    record = {}
    if os.path.isfile(record_path):
        record = load(record_path, errors).get("slice") or {}
    else:
        errors.append(f"slice record missing: {record_path} (spine slice '{sid}')")

    lens_dir = os.path.join(slice_dir, "lens")
    lenses = {lt: os.path.isfile(os.path.join(lens_dir, lt + ".md")) for lt in LENS_TYPES}

    epics = []
    for e in sorted(epics_by_slice.get(sid, []), key=lambda e: str(e.get("id"))):
        epics.append({
            "id": e.get("id"),
            "doc": e.get("doc"),
            "status": norm(e.get("status")),
            "order": e.get("order"),
            "depends_on": sorted(e.get("depends_on") or []),
            "issue_ref": e.get("issue_ref"),
            "title": e.get("title") or e.get("slug"),
            # surface contract (ADR 022): declared at the cut on the spine epics
            # index, read here so the derivation can detect surface debt.
            "surface_type": norm(e.get("surface_type")),
            # /validate stamps surface_verified: true on the spine entry when the
            # surface-parity check passed.
            "surface_verified": bool(e.get("surface_verified")),
        })

    funcs = []
    for fn in (record.get("functionalities") or []):
        fn = fn or {}
        funcs.append({"functionality_ref": fn.get("functionality_ref"),
                      "ice_ref": fn.get("ice_ref")})

    return {
        "id": sid,
        "file": record_path,
        "has_epics": bool(epics),
        "deferrals_exists": os.path.isfile(os.path.join(slice_dir, "epics", "deferrals.yaml")),
        "name": record.get("name") or entry.get("slug"),
        "status": norm(entry.get("status")),
        "order": entry.get("order"),
        "effort": entry.get("effort"),
        "depends_on": sorted(entry.get("depends_on") or []),
        "functionalities": funcs or [{"functionality_ref": f, "ice_ref": None}
                                     for f in (entry.get("functionality_refs") or [])],
        "lenses": lenses,
        "lens_dir": lens_dir,
        "epics": epics,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Product-model state snapshot for /next.")
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    errors = []
    root = os.path.join(args.product_base, "product-os")
    spine_path = os.path.join(root, "_spine.yaml")
    has_files = os.path.isdir(root) and any(
        os.path.isfile(p) for p in glob.glob(os.path.join(root, "**", "*"), recursive=True))
    state = {"product_base": args.product_base, "root": root,
             "model_exists": has_files, "spine_exists": os.path.isfile(spine_path),
             "spine": spine_path, "scan_errors": errors,
             "profile": None, "domains": [], "orphan_slices": [], "model_hash": None}

    if state["model_exists"]:
        state["model_hash"] = tree_hash(root)

    if state["model_exists"] and not state["spine_exists"]:
        errors.append(f"no spine at {spine_path} — the model has files but no index of "
                      "record; legacy per-node files are not read (C13)")

    if state["model_exists"] and state["spine_exists"]:
        spine = load(spine_path, errors)

        prof = spine.get("profile")
        if isinstance(prof, dict):
            state["profile"] = {"file": spine_path, "state": norm(prof.get("state"))}

        domains = as_list(spine.get("domains"))
        caps = as_list(spine.get("capabilities"))
        spine_slices = as_list(spine.get("slices"))
        epics_by_slice = {}
        for e in as_list(spine.get("epics")):
            epics_by_slice.setdefault(slice_id_of(e.get("slice_ref")), []).append(e)

        known_domains = {d.get("id") for d in domains}
        for s in spine_slices:
            if s.get("domain_ref") not in known_domains:
                state["orphan_slices"].append(s.get("id"))
        state["orphan_slices"].sort(key=str)

        for d in sorted(domains, key=lambda d: str(d.get("id"))):
            did = d.get("id")
            slug = d.get("slug") or did
            domain_dir = os.path.join(root, slug)
            slices_dir = os.path.join(domain_dir, "slices")

            capabilities = sorted(
                ({"id": c.get("id"), "detail": norm(c.get("detail")) or "directional",
                  "doc": c.get("doc")} for c in caps if c.get("domain") == did),
                key=lambda c: str(c["id"]))

            indexed = sorted((s for s in spine_slices if s.get("domain_ref") == did),
                             key=lambda s: str(s.get("id")))
            indexed_ids = {s.get("id") for s in indexed}
            slices = [scan_slice(root, slug, s, epics_by_slice, errors) for s in indexed]

            deferred, unindexed = None, []
            for sf in sorted(glob.glob(os.path.join(slices_dir, "*.yaml"))):
                base = os.path.splitext(os.path.basename(sf))[0]
                if base == "_deferred":
                    dd = (load(sf, errors).get("deferred") or {})
                    deferred = {"functionalities": sorted(dd.get("functionalities") or []),
                                "reason": dd.get("reason")}
                elif base not in indexed_ids:
                    unindexed.append(base)

            state["domains"].append({
                "id": did, "slug": slug, "dir": domain_dir,
                "capabilities": capabilities,
                "slices": slices,
                "unindexed_slices": sorted(unindexed),
                "deferred": deferred,
            })

        # a spine with no domains is still a cold start
        if not state["domains"]:
            state["model_exists"] = False

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, sort_keys=True)
    print(json.dumps({"ok": True, "model_exists": state["model_exists"],
                      "spine_exists": state["spine_exists"],
                      "domains": len(state["domains"]),
                      "model_hash": state["model_hash"],
                      "scan_errors": len(errors), "out": args.out}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
