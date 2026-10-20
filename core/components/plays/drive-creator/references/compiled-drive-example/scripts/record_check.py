#!/usr/bin/env python3
"""record_check.py — check the checker's verdict and write the drive's check.yaml (R6).

Whichever checker ran (a sub-agent on another model, or a coding agent), its verdict is JSON in
the shape `judge-drive-result` defines. This script checks that shape against the bundle's
manifest — every criterion judged, no other, each with evidence, the verdict agreeing with the
criteria, a reason for each failure — and writes `check.yaml`, the file the drive's stop
condition reads. Canonical copy lives at drive-creator/references/record_check.py and is
stamped into each drive's scripts/.

    python3 record_check.py --verdict <working>/check/verdict.json \
        --manifest <working>/check/manifest.json --kind subagent|coding-agent [--model M] \
        --out <working>/check.yaml

Exit 0 pass; 1 reject (the drive halts: checker_reject); 2 the verdict is missing or does not
match the shape — never a pass (the drive halts). Standard library only.
"""
import argparse
import json
import os
import sys


class Bad(Exception):
    """Why the verdict cannot be used, in plain words."""


def check(verdict, ids):
    if not isinstance(verdict, dict):
        raise Bad("the verdict is not a JSON object")
    if verdict.get("verdict") not in ("pass", "reject"):
        raise Bad("`verdict` must be pass or reject")
    crit = verdict.get("criteria")
    if not isinstance(crit, list):
        raise Bad("`criteria` must be a list")
    seen = {}
    for c in crit:
        if not isinstance(c, dict) or c.get("result") not in ("pass", "fail"):
            raise Bad("each criterion needs a result of pass or fail")
        if not str(c.get("evidence", "")).strip():
            raise Bad(f"criterion {c.get('id')} has no evidence")
        seen[str(c.get("id"))] = c["result"]
    if sorted(seen) != sorted(ids):
        lacking = sorted(set(ids) - set(seen))
        extra = sorted(set(seen) - set(ids))
        raise Bad("the criteria judged do not match the criteria asked"
                  + (f"; not judged: {', '.join(lacking)}" if lacking else "")
                  + (f"; not asked: {', '.join(extra)}" if extra else ""))
    failed = sorted(i for i, r in seen.items() if r == "fail")
    if verdict["verdict"] == "pass" and failed:
        raise Bad(f"the verdict says pass, but these failed: {', '.join(failed)}")
    if verdict["verdict"] == "reject":
        if not failed:
            raise Bad("the verdict says reject, but no criterion failed")
        reasons = [r for r in verdict.get("reasons") or [] if str(r).strip()]
        if not reasons:
            raise Bad("a reject must give its reasons")
    return failed


def as_yaml(verdict, kind, model, failed):
    q = json.dumps  # a JSON string is a valid YAML scalar
    lines = [f"verdict: {verdict['verdict']}", "checker:", f"  kind: {kind}",
             f"  model: {q(model) if model else 'null'}", "criteria:"]
    for c in verdict["criteria"]:
        lines += [f"  - id: {q(str(c['id']))}", f"    result: {c['result']}",
                  f"    evidence: {q(str(c['evidence']))}"]
    lines.append("failed: [" + ", ".join(q(f) for f in failed) + "]")
    lines.append("reasons:" + ("" if verdict.get("reasons") else " []"))
    lines += [f"  - {q(str(r))}" for r in verdict.get("reasons") or []]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Record the drive checker's verdict.")
    ap.add_argument("--verdict", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--kind", required=True, choices=("subagent", "coding-agent"))
    ap.add_argument("--model")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        with open(args.manifest, encoding="utf-8") as fh:
            ids = [str(i) for i in json.load(fh)["criteria_ids"]]
        with open(args.verdict, encoding="utf-8") as fh:
            verdict = json.load(fh)
        failed = check(verdict, ids)
    except (OSError, ValueError, KeyError, Bad) as why:
        msg = why if isinstance(why, Bad) else f"cannot read the verdict: {why.__class__.__name__}"
        sys.stderr.write(f"record_check.py: {msg} — not a pass\n")
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(as_yaml(verdict, args.kind, args.model, failed))
    print(json.dumps({"verdict": verdict["verdict"], "failed": failed}))
    return 0 if verdict["verdict"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
