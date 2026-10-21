#!/usr/bin/env python3
"""check_loop_contract.py — check a loop's contract and record how this run starts (#614).

The single shared checker for `standards/rules/loop-contract.md`. A play that can run
inside a loop calls it first. With `--contract`, it checks the contract — valid JSON,
every required field present, and the current branch equal to the loop's branch — and
writes `run.json` with `in_loop: true` and the play's own inputs and answers. With no
`--contract`, it writes `in_loop: false`: the play runs by hand, unchanged.

Canonical copy lives at play-creator/references/check_loop_contract.py and is stamped into
each play that can run inside a loop. Layer rule: reads files only; the current branch is
passed in; no git/gh/network.

    python3 check_loop_contract.py --play vision --branch "$(git branch --show-current)" \
        [--contract <contract.json>] --out <working>/run.json

Exit 0 — run.json written (in a loop, or by hand). Exit 2 — the contract is invalid, the
branch does not match, or run.json cannot be written: the play halts and says why.
"""
import argparse
import json
import os
import sys

REQUIRED = ("loop_run_id", "loop", "branch", "issue", "review_dir")


class Invalid(Exception):
    """A reason the contract cannot be used, in plain words."""


def check(contract, play, branch):
    if not isinstance(contract, dict):
        raise Invalid("the contract is not a JSON object")
    missing = [k for k in REQUIRED if contract.get(k) in (None, "")]
    if missing:
        raise Invalid(f"the contract is missing {', '.join(missing)}")
    issue = contract["issue"]
    if not isinstance(issue, int) or isinstance(issue, bool) or issue < 1:
        raise Invalid("the contract's `issue` must be a positive issue number")
    rnd = contract.get("round", 1)
    if not isinstance(rnd, int) or isinstance(rnd, bool) or rnd < 1:
        raise Invalid("the contract's `round` must be a positive number")
    for key in ("loop_run_id", "loop", "branch", "review_dir"):
        if not isinstance(contract[key], str) or not contract[key].strip():
            raise Invalid(f"the contract's `{key}` must be a non-empty text")
    for key in ("inputs", "answers"):
        if contract.get(key) is not None and not isinstance(contract[key], dict):
            raise Invalid(f"the contract's `{key}` must be an object keyed by play")
        mine = (contract.get(key) or {}).get(play)
        if mine is not None and not isinstance(mine, dict):
            raise Invalid(f"the contract's `{key}.{play}` must be an object")
    if str(contract["branch"]) != branch:
        raise Invalid(f"the current branch is `{branch}`, but the loop's branch is "
                      f"`{contract['branch']}` — switch to it first")
    return {"in_loop": True, "play": play,
            "loop_run_id": str(contract["loop_run_id"]), "loop": str(contract["loop"]),
            "branch": branch, "issue": issue, "round": rnd,
            "review_dir": str(contract["review_dir"]),
            "inputs": (contract.get("inputs") or {}).get(play) or {},
            "answers": (contract.get("answers") or {}).get(play) or {}}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a loop contract (loop-contract.md).")
    ap.add_argument("--play", required=True)
    ap.add_argument("--branch", required=True, help="the current git branch")
    ap.add_argument("--contract", help="the loop's contract; absent ⇒ run by hand")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    if not args.contract:
        run = {"in_loop": False, "play": args.play, "branch": args.branch}
    else:
        try:
            with open(args.contract, encoding="utf-8") as fh:
                contract = json.load(fh)
            run = check(contract, args.play, args.branch)
        except (OSError, ValueError, Invalid) as why:
            msg = why if isinstance(why, Invalid) else f"cannot read the contract: {why.__class__.__name__}"
            sys.stderr.write(f"check_loop_contract.py: {msg}\n")
            return 2
    try:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(run, fh, indent=2)
    except OSError as exc:
        sys.stderr.write(f"check_loop_contract.py: cannot write {args.out}: {exc.__class__.__name__}\n")
        return 2
    print(json.dumps(run, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
