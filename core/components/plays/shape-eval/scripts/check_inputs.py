#!/usr/bin/env python3
"""check_inputs.py — the input check: the agent and the skill are given only the copies (C1).

    python3 check_inputs.py --contract <working>contract.json --working <working> \
        --out <working>inputs-check.json

The play writes the JSON contract it hands to the agent into contract.json before the dispatch
(and again before each fix round). This check reads it. Every input path must be a file or a
folder inside the run's working folder (the copies of the epic, its stories and the hidden file
in `inputs/`, the template and step-library copies, and, on a fix, the check record and the
drafts); none may name an ICE page (`feature.md`, `capability.md`, `ice.md`), the product model
(`product-os`), a usage guide (`guides/`) or the plans folder itself. Every output path must be
inside `<working>drafts/`. Writes inputs-check.json {ok, problems, inputs, outputs}.
Exit 0 ok, 1 a problem, 2 refused.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eval_common as ec  # noqa: E402

ICE_PAGES = ("feature.md", "capability.md", "ice.md")  # a file named so is an ICE page
FORBIDDEN = ("product-os", "/guides/", ".garura/project/plans")  # parts of a path


def paths_of(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [p for v in value for p in paths_of(v)]
    if isinstance(value, dict):
        return [p for v in value.values() for p in paths_of(v)]
    return []


def inside(path, folder):
    a, b = os.path.abspath(path), os.path.abspath(folder)
    return a == b or a.startswith(b.rstrip(os.sep) + os.sep)


def check(contract, working):
    problems = []
    ins = paths_of(contract.get("inputs") or {})
    outs = paths_of(contract.get("outputs") or {})
    for p in ins:
        low = p.replace(os.sep, "/").lower()
        bad = [f for f in FORBIDDEN if f in low] + [n for n in ICE_PAGES if os.path.basename(low.rstrip("/")) == n]
        if bad:
            problems.append(f"input {p} names {bad[0]}: the agent and the skill get only the copies")
        elif not inside(p, working):
            problems.append(f"input {p} is outside the run's working folder")
    for p in outs:
        if not inside(p, os.path.join(working, "drafts")):
            problems.append(f"output {p} is outside the drafts folder")
    if not ins:
        problems.append("the contract names no input")
    return {"ok": not problems, "problems": problems, "inputs": ins, "outputs": outs}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the agent's contract names only the copies.")
    ap.add_argument("--contract", required=True)
    ap.add_argument("--working", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        res = check(ec.read_json(args.contract, "the contract"), args.working)
    except ec.Refused as exc:
        sys.stderr.write(f"check_inputs.py: {exc}\n")
        print(json.dumps({"ok": False, "reason": str(exc)}))
        return 2
    ec.write_json(args.out, res)
    print(json.dumps({"ok": res["ok"], "problems": res["problems"]}, indent=2))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
