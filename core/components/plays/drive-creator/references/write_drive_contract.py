#!/usr/bin/env python3
"""write_drive_contract.py — write a drive's one contract (Shared Drive Run, step R4).

A drive hands the same contract to every play it runs (`standards/rules/drive-contract.md`).
This script builds it from the drive's facts, the plays' inputs and the answers gathered
first, then checks it with the shared checker's rules, so a play never gets a contract it
would reject. Canonical copy lives at drive-creator/references/write_drive_contract.py and is
stamped into each drive's scripts/ beside check_drive_contract.py.

    python3 write_drive_contract.py --drive kickoff --drive-run-id kickoff-<ts> \
        --branch <branch> --issue <n> --review-dir <dir> --plays intent,vision,understand \
        [--inputs <inputs.json>] [--answers <answers.json>] --out <contract.json>

`--inputs` and `--answers` hold JSON objects keyed by play; a key that names no play of the
drive is an error (a typo would silently drop answers). Exit 0 written; 2 invalid — nothing
written. Reads and writes files only. Standard library only.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # a drive's scripts/ holds the stamped checker beside this script
sys.path.append(os.path.join(HERE, "..", "..", "play-creator", "references"))  # canonical home
from check_drive_contract import Invalid, check  # noqa: E402


def load(path):
    if not path:
        return {}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise Invalid(f"{path} must hold a JSON object keyed by play")
    return data


def build(args, plays, inputs, answers):
    for name, block in (("inputs", inputs), ("answers", answers)):
        stray = sorted(set(block) - set(plays))
        if stray:
            raise Invalid(f"`{name}` names plays the drive does not run: {', '.join(stray)}")
    contract = {"drive_run_id": args.drive_run_id, "drive": args.drive, "branch": args.branch,
                "issue": args.issue, "review_dir": args.review_dir, "plays": plays,
                "inputs": inputs, "answers": answers}
    for play in plays:  # the same check every play runs on the contract
        check(contract, play, args.branch)
    return contract


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write a drive's contract.")
    for flag in ("--drive", "--drive-run-id", "--branch", "--review-dir", "--plays", "--out"):
        ap.add_argument(flag, required=True)
    ap.add_argument("--issue", required=True, type=int)
    ap.add_argument("--inputs")
    ap.add_argument("--answers")
    args = ap.parse_args(argv)
    plays = [p.strip() for p in args.plays.split(",") if p.strip()]
    try:
        if not plays:
            raise Invalid("the drive names no plays")
        contract = build(args, plays, load(args.inputs), load(args.answers))
    except (OSError, ValueError, Invalid) as why:
        msg = why if isinstance(why, Invalid) else f"cannot read an input: {why.__class__.__name__}"
        sys.stderr.write(f"write_drive_contract.py: {msg} — nothing written\n")
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(contract, fh, indent=2)
    print(args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
