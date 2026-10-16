#!/usr/bin/env python3
"""write_drive_review.py — keep a play's checkpoint as a review record for the drive (#614).

Inside a drive a play does not stop at its own checkpoint (ADR 029; drive-contract.md).
Instead it writes what the checkpoint would have shown — the rendered summary, and the
files the decision stands on — into the drive's `review_dir`, so the drive's end review
can read every play's record in one place. Nothing here decides anything: the record
reads `decided: false` until the drive's review answers it.

Canonical copy lives at play-creator/references/write_drive_review.py and is stamped into
each play that can run inside a drive. Layer rule: file reads/writes only; no git/gh/network.

    python3 write_drive_review.py --run <working>/run.json --summary <checkpoint.md> \
        [--attach name=<path> ...] --ts <run ts>

Writes `<review_dir>/<play>-<ts>.md` (the summary, as shown) and `<review_dir>/<play>-<ts>.json`
(the record) and prints the record. Exit 0 written · 2 usage error, or the run is not in a
drive, or a named file is missing (nothing written).
"""
import argparse
import json
import os
import shutil
import sys


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write a play's review record for the drive.")
    ap.add_argument("--run", required=True, help="run.json from check_drive_contract.py")
    ap.add_argument("--summary", required=True, help="the checkpoint as it would have been shown")
    ap.add_argument("--attach", action="append", default=[], help="name=path of a file the decision stands on")
    ap.add_argument("--ts", required=True, help="the run's UTC timestamp")
    args = ap.parse_args(argv)

    try:
        with open(args.run, encoding="utf-8") as fh:
            run = json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"write_drive_review.py: cannot read {args.run}: {exc.__class__.__name__}\n")
        return 2
    if not isinstance(run, dict) or not run.get("in_drive"):
        sys.stderr.write("write_drive_review.py: this run is not inside a drive — the play's own "
                         "checkpoint applies\n")
        return 2
    attached = {}
    for item in args.attach:
        name, sep, path = item.partition("=")
        if not sep or not name or not path:
            sys.stderr.write(f"write_drive_review.py: --attach wants name=path, got `{item}`\n")
            return 2
        attached[name] = path
    missing = [p for p in [args.summary, *attached.values()] if not os.path.isfile(p)]
    if missing:
        sys.stderr.write(f"write_drive_review.py: missing {', '.join(missing)} — nothing written\n")
        return 2

    base = os.path.join(run["review_dir"], f"{run['play']}-{args.ts}")
    os.makedirs(run["review_dir"], exist_ok=True)
    shutil.copyfile(args.summary, base + ".md")
    record = {"play": run["play"], "drive_run_id": run["drive_run_id"], "drive": run.get("drive"),
              "issue": run.get("issue"), "branch": run["branch"], "recorded_at": args.ts,
              "summary": os.path.basename(base + ".md"), "attachments": attached,
              "decided": False}
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
