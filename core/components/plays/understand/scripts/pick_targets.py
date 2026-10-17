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
    the play asks the person for all of them at once, before it opens any change.

It writes nothing to the model. Layer rule: file reads/writes only; no git/gh/network.

    python3 pick_targets.py --spine <product_base>product-os/_spine.yaml \
        --run <working>/run.json --working <working> \
        [--capability <id> ...] --out <working>/targets.json

targets.json: `{targets: [{id, state: directional|absent, seed: <path>|null}], ask: [ids],
refused: [{id, reason}], nothing_pending: bool}`.
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
    domains = {d.get("id") for d in spine.get("domains") or [] if isinstance(d, dict)}
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

    targets, ask, refused = [], [], []
    for cid in ids:
        cap = caps.get(cid)
        if cap is not None:
            if cap.get("detail") == "detailed":
                refused.append({"id": cid, "reason": "already detailed — never re-detailed"})
            else:
                targets.append({"id": cid, "state": "directional", "seed": None})
            continue
        given = seeds.get(cid)
        if isinstance(given, dict) and all(isinstance(given.get(k), str) and given[k].strip()
                                           for k in ("one_line", "why", "domain")) \
                and given["domain"] in domains:
            path = os.path.join(args.working, "caps", cid, "seed.yaml")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                yaml.safe_dump({"seed": {"id": cid, "domain": given["domain"],
                                         "one_line": given["one_line"], "why": given["why"],
                                         "answered_by": "human"}}, fh, sort_keys=False)
            targets.append({"id": cid, "state": "absent", "seed": path})
        else:
            targets.append({"id": cid, "state": "absent", "seed": None})
            ask.append(cid)

    result = {"in_drive": in_drive, "targets": targets, "ask": ask, "refused": refused,
              "nothing_pending": not targets and not refused}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
