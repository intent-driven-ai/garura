#!/usr/bin/env python3
"""
pick_targets.py — pick the capabilities one /understand run details (#615).

One run details every pending capability, not one capability per run. This script makes
that pick mechanically, so the play never re-reasons it:

  - Named capabilities (the play argument, `--capability`, repeatable or comma-separated)
    are the targets, in the order given.
  - With none named, the targets are every capability in the live spine that /vision
    seeded and nobody has detailed yet (`detail: directional`), in spine order — and,
    inside a drive, every capability the contract carries seed answers for
    (`answers.seeds.<capability>`).
  - A target already `detailed` is refused (it is never re-detailed); the play halts.
  - A target absent from the spine needs the person's answers (what it is, why it
    matters, its domain). Inside a drive, the contract's answers are written verbatim to
    `<working>/caps/<capability>/seed.yaml` with `answered_by: human` (a person gave them
    before the drive started). An absent target with no answers, or whose answered domain
    is not in the spine, is listed under `ask`:
    the play asks the person for all of them at once, before it opens any change, records
    the answers in `<working>/caps/<capability>/seed.yaml`, and runs this script again: a
    seed file already there (`answered_by: human`) counts as the answers.
  - Each target gets its write scope — its own folder in the model, `product-os/<cap-dir>/`
    (from its doc, or for a seed from its domain's folder and its id). The detailing runs
    as a scoped-write fan-out (standards/rules/concurrent-fanout.md), so two targets that
    share a folder, or one whose folder sits inside another's, are refused.

It writes nothing to the model. Layer rule: file reads/writes only; no git/gh/network.

    python3 pick_targets.py --spine <product_base>product-os/_spine.yaml \
        --run <working>/run.json --working <working> \
        [--capability <id> ...] --out <working>/targets.json

targets.json: `{targets: [{id, state: directional|absent, seed: <path>|null,
scope: "product-os/<cap-dir>/"|null}], ask: [ids], refused: [{id, reason}],
nothing_pending: bool}`. A scope is null only while the target's answers are still missing.
Exit 0 picked (read `refused`, `ask` and `nothing_pending` — halting is the play's policy) ·
2 usage or parse error.
"""

import argparse
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("pick_targets.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)


def slug(text):
    return "".join(c if c.isalnum() else "-" for c in str(text).lower()).strip("-")


def doc_dir(doc):
    """The capability's folder from its doc path ('a/b/capability.md' -> 'a/b')."""
    if not isinstance(doc, str) or "/" not in doc:
        return None
    return doc.rsplit("/", 1)[0].strip("/") or None


def read_seed_file(path, cid):
    try:
        with open(path, encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
    except (OSError, yaml.YAMLError):
        return None
    seed = raw.get("seed") if isinstance(raw, dict) else None
    if (isinstance(seed, dict) and seed.get("id") == cid and seed.get("answered_by") == "human"
            and all(isinstance(seed.get(k), str) and seed[k].strip()
                    for k in ("one_line", "why", "domain"))):
        return seed
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pick the capabilities one /understand run details.")
    ap.add_argument("--spine", required=True)
    ap.add_argument("--run", required=True, help="run.json from check_drive_contract.py")
    ap.add_argument("--working", required=True, help="the run's working root")
    ap.add_argument("--capability", action="append", default=[], help="a named target (repeatable)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    try:
        with open(args.spine, encoding="utf-8") as fh:
            spine = yaml.safe_load(fh) or {}
        with open(args.run, encoding="utf-8") as fh:
            run = json.load(fh)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        sys.stderr.write(f"pick_targets.py: cannot read input: {exc.__class__.__name__}: {exc}\n")
        return 2
    if not isinstance(spine, dict) or not isinstance(run, dict):
        sys.stderr.write("pick_targets.py: spine and run.json must be mappings\n")
        return 2

    caps = {c["id"]: c for c in spine.get("capabilities") or []
            if isinstance(c, dict) and isinstance(c.get("id"), str)}
    domains = {d.get("id"): d for d in spine.get("domains") or [] if isinstance(d, dict)}
    in_drive = run.get("in_drive") is True
    answers = run.get("answers") if in_drive else {}
    seeds = (answers or {}).get("seeds") or {}
    if not isinstance(seeds, dict):
        sys.stderr.write("pick_targets.py: the contract's answers.seeds must be a mapping\n")
        return 2

    named = [n.strip() for item in args.capability for n in item.split(",") if n.strip()]
    if named:
        ids = list(dict.fromkeys(named))
    else:
        ids = [cid for cid, c in caps.items() if c.get("detail") == "directional"]
        ids += [cid for cid in seeds if cid not in caps and cid not in ids]

    def seed_dir(seed):
        dom_doc = domains[seed["domain"]].get("doc")
        dom_dir = dom_doc.split("/")[0] if isinstance(dom_doc, str) and "/" in dom_doc \
            else seed["domain"]
        return doc_dir(seed.get("doc")) or f"{dom_dir}/{slug(seed['id'])}"

    targets, ask, refused = [], [], []
    for cid in ids:
        cap = caps.get(cid)
        if cap is not None:
            if cap.get("detail") == "detailed":
                refused.append({"id": cid, "reason": "already detailed — never re-detailed"})
            else:
                targets.append({"id": cid, "state": "directional", "seed": None,
                                "dir": doc_dir(cap.get("doc"))})
            continue
        path = os.path.join(args.working, "caps", cid, "seed.yaml")
        seed = read_seed_file(path, cid) if os.path.isfile(path) else None
        given = seeds.get(cid)
        if seed is None and isinstance(given, dict) and all(
                isinstance(given.get(k), str) and given[k].strip()
                for k in ("one_line", "why", "domain")):
            seed = {"id": cid, "domain": given["domain"], "one_line": given["one_line"],
                    "why": given["why"], "answered_by": "human"}
            if seed["domain"] in domains:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as fh:
                    yaml.safe_dump({"seed": seed}, fh, sort_keys=False)
        if seed is not None and seed["domain"] in domains:
            targets.append({"id": cid, "state": "absent", "seed": path, "dir": seed_dir(seed)})
        else:
            targets.append({"id": cid, "state": "absent", "seed": None, "dir": None})
            ask.append(cid)

    # --- write scopes: each target's own folder, distinct and not nested --------------
    for t in targets:
        if t["state"] == "directional" and t["dir"] is None:
            refused.append({"id": t["id"], "reason": "its spine entry has no doc folder — "
                                                     "no write scope for the fan-out"})
    for i, a in enumerate(targets):
        for b in targets[:i]:
            if a["dir"] and b["dir"] and (a["dir"] == b["dir"]
                                          or a["dir"].startswith(b["dir"] + "/")
                                          or b["dir"].startswith(a["dir"] + "/")):
                refused.append({"id": a["id"], "reason": f"its folder {a['dir']} overlaps "
                                                         f"{b['id']}'s folder {b['dir']}"})
    for t in targets:
        d = t.pop("dir")
        t["scope"] = f"product-os/{d}/" if d else None

    result = {"in_drive": in_drive, "targets": targets, "ask": ask, "refused": refused,
              "nothing_pending": not targets and not refused}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
