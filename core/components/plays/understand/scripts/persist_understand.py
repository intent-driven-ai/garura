#!/usr/bin/env python3
"""
persist_understand.py — /understand's deterministic keyed persist, in place on the live model.

Direct-model-write remnant of the old apply_understand.py (ADR 026,
standards/rules/direct-model-write.md). There is NO draft tree and NO doc copy: the LLM
enrichment skill already wrote the per-node docs (capability.md, functionality.md) straight
to the live model. This script owns every SHARED file and applies the manifests' structured
spine-deltas to the live model IN PLACE, keyed to the run's target capabilities — one
--capability-ref and one --enrich-manifest per target (one run details every pending
capability, #615):

  0. (only with --seed, #616) when a target capability is ABSENT from the live spine, a thin
     seed entry from the person's recorded answers: id, domain (must already exist), status
     proposed, detail directional, one_line, doc — exactly what /vision would have written,
     nothing invented. It is then promoted by step 1 like any seed. Without a seed for it, an
     absent target is still refused.
  1. each target capability's spine entry: detail -> detailed, + nfr_needs + compliance_needs
     (+ doc/one_line if its manifest carries them). It refuses to mutate any capability that
     is not a target — this is the node-level containment the file-level scoped guard
     cannot provide.
  2. the new `functionalities` entries from each manifest (each must carry an id and
     capability == that manifest's target; additive — an id already present under the same
     capability is left untouched; an id declared twice in the run, or already present under
     another capability, is refused).
  3. the rolled-up `profile` (the firmed box) from the proposed-profile. It refuses a
     profile that is not `set`, lowers a dimension the live box holds, or drops a
     compliance regime — the box only ever goes up (C7).
  4. one decision record per box-move (ADR, level product, status accepted), each linked onto
     the `decisions` list of the capability the move names. Inside a drive (#615) the play
     passes --decision-status proposed: no person has said yes, so the drive's review
     accepts or drops each move. The persist record's `box_moves` carry each move's
     decision id and status, so the run's record shows what was written.

Every check runs before anything is written: a refusal leaves the model untouched.
It reads the manifests (STM, non-model) + the roll-up output; it does NOT read a draft tree
and does NOT copy docs. Layer rule: pure file writes from disk inputs; no git/gh/network.

    python3 persist_understand.py \
        --enrich-manifest <cap-a/enrich-manifest.yaml> [--enrich-manifest ...] \
        --capability-ref <cap-a> [--capability-ref ...] \
        --product-base <product_base> --proposed-profile <proposed-profile.yaml> \
        --rollup-report <rollup.json> --decided-by /understand --date <YYYY-MM-DD> \
        --out-manifest <persist-manifest.json> \
        [--seed <cap-a/seed.yaml> ...] [--decision-status accepted|proposed]

Exit 0 on success, 2 on usage/parse/containment error (nothing written).
"""

import argparse
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("persist_understand.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)


def slug(text):
    return "".join(c if c.isalnum() else "-" for c in str(text).lower()).strip("-")


def load(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def find(entries, eid):
    for e in entries:
        if isinstance(e, dict) and e.get("id") == eid:
            return e
    return None


def refuse(msg):
    sys.stderr.write(f"persist_understand.py: {msg}\n")
    return 2


def read_seed(path, cap_ids):
    """Return (seed, error) for one seed file; the seed must carry the person's answers."""
    if not os.path.isfile(path):
        return None, f"missing input {path}"
    raw = load(path)
    seed = raw.get("seed") if isinstance(raw, dict) else None
    if not isinstance(seed, dict):
        return None, "seed file must be a mapping with a 'seed' mapping — refusing"
    missing = [k for k in ("id", "domain", "one_line", "why", "answered_by") if not seed.get(k)]
    not_text = [k for k in ("id", "domain", "one_line", "why", "answered_by", "doc")
                if k in seed and seed[k] is not None and not isinstance(seed[k], str)]
    if not_text:
        return None, f"seed fields {not_text} must be text — refusing"
    if missing:
        return None, (f"seed is missing {missing} — refusing "
                      f"(a seed carries the person's answers, never invented ones)")
    if seed["answered_by"] != "human":
        return None, (f"seed answered_by is '{seed['answered_by']}', "
                      f"not 'human' — refusing (only the person's answers may seed)")
    if seed["id"] not in cap_ids:
        return None, (f"seed id '{seed['id']}' is not a --capability-ref of this run "
                      f"— refusing (containment)")
    return seed, None


SCALE = ["none", "low", "medium", "high", "xhigh"]


def rank(level):
    try:
        return SCALE.index((level or "none").strip().lower())
    except (AttributeError, ValueError):
        return 0


def profile_error(live_profile, proposed):
    """Why the proposed profile may not replace the live one, or None (C7: never lower)."""
    if not isinstance(proposed, dict) or proposed.get("state") != "set":
        return "the proposed profile is not firmed to `set`"
    live_nfr = (live_profile or {}).get("nfr") or {}
    new_nfr = proposed.get("nfr") or {}
    for dim, spec in live_nfr.items():
        old = spec.get("level") if isinstance(spec, dict) else spec
        new = new_nfr.get(dim)
        new = new.get("level") if isinstance(new, dict) else new
        if rank(new) < rank(old):
            return f"the proposed profile lowers {dim} from {old} to {new or 'nothing'}"
    dropped = [r for r in (live_profile or {}).get("compliance") or []
               if r not in (proposed.get("compliance") or [])]
    if dropped:
        return f"the proposed profile drops compliance {dropped}"
    return None


def seed_entry(seed, live):
    """Return (entry, error): the thin spine entry for an absent capability."""
    cap_id = seed["id"]
    domain = find(live.get("domains") or [], seed["domain"])
    if domain is None:
        return None, (f"domain '{seed['domain']}' is not in the spine "
                      f"— refusing (a seed joins an existing domain)")
    # The domain's folder comes from its own doc (e.g. id 'dom-order-mgmt' lives in
    # 'order-management/'); fall back to the id only when the domain records no doc.
    dom_doc = domain.get("doc") if isinstance(domain.get("doc"), str) else ""
    dom_dir = dom_doc.split("/")[0] if "/" in dom_doc else seed["domain"]
    doc = seed.get("doc") or f"{dom_dir}/{slug(cap_id)}/capability.md"
    parts = doc.split("/")
    if (doc.startswith("/") or ".." in parts or len(parts) != 3
            or parts[0] != dom_dir or parts[-1] != "capability.md"):
        return None, f"seed doc '{doc}' is not '{dom_dir}/<capability>/capability.md' — refusing"
    return {"id": cap_id, "domain": seed["domain"], "status": "proposed",
            "detail": "directional", "one_line": seed["one_line"], "doc": doc}, None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Keyed in-place persist for /understand (ADR 026).")
    ap.add_argument("--enrich-manifest", required=True, action="append",
                    help="enrich-manifest.yaml of one target (STM, non-model); repeat per target")
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--proposed-profile", required=True, help="rolled-up profile yaml ({profile: ...})")
    ap.add_argument("--rollup-report", required=True)
    ap.add_argument("--capability-ref", required=True, action="append",
                    help="a capability this run may mutate; repeat per target — no other is touched")
    ap.add_argument("--decided-by", default="/understand")
    ap.add_argument("--date", required=True, help="decision date (play passes it; never auto-generated)")
    ap.add_argument("--out-manifest", required=True)
    ap.add_argument("--decision-status", choices=("accepted", "proposed"), default="accepted",
                    help="box-move decision status; proposed inside a drive (#615)")
    ap.add_argument("--seed", action="append", default=[],
                    help="seed.yaml with the person's answers for one ABSENT target (#616); repeatable")
    args = ap.parse_args(argv)

    cap_ids = list(args.capability_ref)
    if len(set(cap_ids)) != len(cap_ids):
        return refuse("a --capability-ref is named twice")
    live_root = os.path.join(args.product_base, "product-os")
    live_spine_path = os.path.join(live_root, "_spine.yaml")
    for p in (*args.enrich_manifest, live_spine_path, args.proposed_profile, args.rollup_report):
        if not os.path.isfile(p):
            return refuse(f"missing input {p}")

    # --- containment: one manifest per target, each about its target and nothing else --
    enriches = {}
    for path in args.enrich_manifest:
        man = load(path)
        enrich = man.get("enrich", man) if isinstance(man, dict) else {}
        enrich = enrich if isinstance(enrich, dict) else {}
        ref = enrich.get("capability_ref")
        if not ref and len(args.enrich_manifest) == 1 and len(cap_ids) == 1:
            ref = cap_ids[0]
        if ref not in cap_ids:
            return refuse(f"manifest {path} names capability_ref '{ref}', which is not a "
                          f"--capability-ref of this run — refusing (containment)")
        if ref in enriches:
            return refuse(f"two manifests name capability '{ref}' — refusing")
        enriches[ref] = enrich
    lacking = [c for c in cap_ids if c not in enriches]
    if lacking:
        return refuse(f"no enrich manifest for {lacking} — refusing")

    seeds = {}
    for path in args.seed:
        seed, err = read_seed(path, cap_ids)
        if err:
            return refuse(err)
        if seed["id"] in seeds:
            return refuse(f"two seeds name capability '{seed['id']}' — refusing")
        seeds[seed["id"]] = seed

    live = load(live_spine_path)
    proposed_profile = (load(args.proposed_profile).get("profile") or {})
    live_caps = live.setdefault("capabilities", [])
    live_funcs = live.setdefault("functionalities", [])
    have = {f.get("id"): f.get("capability") for f in live_funcs if isinstance(f, dict)}
    declared = set()

    written, seeded = [], []
    changed = {"capabilities": [], "functionalities_added": [], "profile": False, "decisions": []}
    targets = {}

    for cap_id in cap_ids:
        # --- 0. seed an ABSENT target from the person's answers (#616 D1) -------------
        live_cap = find(live_caps, cap_id)
        if live_cap is None:
            if cap_id not in seeds:
                return refuse(f"live spine has no capability '{cap_id}' to detail "
                              f"(pass --seed with the person's answers to seed it)")
            live_cap, err = seed_entry(seeds[cap_id], live)
            if err:
                return refuse(err)
            live_caps.append(live_cap)
            seeded.append(cap_id)
            written.append(f"seed:{cap_id}")
        elif live_cap.get("detail") == "detailed":
            return refuse(f"capability '{cap_id}' is already detailed — refusing to re-detail it")
        targets[cap_id] = live_cap

        # --- 1. the target capability entry: apply its manifest delta, keyed to cap_id -
        enrich = enriches[cap_id]
        cap_delta = enrich.get("capability") or {}
        for field in ("detail", "nfr_needs", "compliance_needs", "one_line", "doc"):
            if field in cap_delta:
                live_cap[field] = cap_delta[field]
        if live_cap.get("detail") != "detailed":
            live_cap["detail"] = "detailed"      # promotion is guaranteed by construction
        changed["capabilities"].append(cap_id)

        # --- 2. new functionality entries (additive; every one under this target) -----
        for f in enrich.get("functionalities") or []:
            if not isinstance(f, dict):
                continue
            fid = f.get("id")
            if not isinstance(fid, str) or not fid.strip():
                return refuse(f"a functionality under '{cap_id}' has no id — refusing")
            if f.get("capability") != cap_id:
                return refuse(f"functionality '{fid}' is not under '{cap_id}' "
                              f"— refusing (containment)")
            if fid in declared:
                return refuse(f"functionality '{fid}' is declared twice in this run — refusing")
            declared.add(fid)
            if fid in have and have[fid] != cap_id:
                return refuse(f"functionality '{fid}' already exists under '{have[fid]}' "
                              f"— refusing (containment)")
            if fid not in have:
                live_funcs.append(f)
                have[fid] = cap_id
                changed["functionalities_added"].append(fid)

    # --- 3. the rolled-up profile (replace the box; never lower it, C7) ---------------
    err = profile_error(live.get("profile"), proposed_profile)
    if err:
        return refuse(f"{err} — refusing (the box only ever goes up)")
    live["profile"] = proposed_profile
    changed["profile"] = True

    # --- 4. one decision per box-move, linked onto the capability the move names -------
    report = json.load(open(args.rollup_report, encoding="utf-8"))
    moves = report.get("box_moves", [])
    decisions, recorded_moves = [], []
    for mv in moves:
        if not isinstance(mv, dict) or not all(mv.get(k) for k in ("dimension", "from", "to")):
            return refuse(f"box-move {mv} lacks a dimension, from or to — refusing")
        cap_id = mv.get("capability") or (cap_ids[0] if len(cap_ids) == 1 else None)
        if cap_id not in targets:
            return refuse(f"box-move {mv} names no target capability of this run — refusing")
        dim, frm, to = mv["dimension"], mv["from"], mv["to"]
        did = f"dec-{slug(cap_id)}-{slug(dim)}-{slug(frm)}-{slug(to)}"
        recorded_moves.append({**mv, "capability": cap_id, "decision": did,
                               "status": args.decision_status})
        decisions.append((cap_id, did, {"decision": {
            "id": did, "node_ref": cap_id, "level": "product",
            "title": f"Move {dim} box {frm} -> {to} for {cap_id}",
            "reason": (f"The {cap_id} capability's need on {dim} ({to}) exceeds the "
                       f"committed box ({frm}); the box is raised to admit it."),
            "alternatives": [{"name": f"keep {dim} at {frm}",
                              "why_not": f"would block {cap_id}'s required {dim} level"}],
            "status": args.decision_status, "superseded_by": None,
            "metadata": {"decided_by": args.decided_by, "date": args.date, "version": 1},
        }}))

    # --- every check passed: write the decisions, then the spine -----------------------
    if decisions:
        dec_dir = os.path.join(live_root, "decisions")
        os.makedirs(dec_dir, exist_ok=True)
        for cap_id, did, decision in decisions:
            with open(os.path.join(dec_dir, f"{did}.yaml"), "w", encoding="utf-8") as fh:
                yaml.safe_dump(decision, fh, sort_keys=False)
            written.append(f"decision:{did}")
            changed["decisions"].append(did)
            cap_decisions = targets[cap_id].setdefault("decisions", [])
            if did not in cap_decisions:
                cap_decisions.append(did)

    with open(live_spine_path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(live, fh, sort_keys=False, allow_unicode=True)
    written.append("spine:_spine.yaml")

    manifest = {"written": written, "capability_refs": cap_ids, "seeded": seeded,
                "changed": changed, "box_moves": recorded_moves}
    with open(args.out_manifest, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
