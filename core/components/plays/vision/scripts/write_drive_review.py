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
        [--attach name=<path> ...] [--decisions <citations.json>] --ts <run ts>

--decisions takes the memory tool's answer to `citations --issue N --play P --check` (ADR 035
§6): the record then carries every decision the play made, each with its trace — the steps the
agent took, each with the memory lines it read and the lines around them — and any step whose
source changed or is missing, so the drive's review shows what each decision rested on.

Writes `<review_dir>/<play>-<ts>.md` (the summary, as shown) and `<review_dir>/<play>-<ts>.json`
(the record) and prints the record. Exit 0 written · 2 usage error, the run is not in a drive
or lacks a field, the timestamp is not plain, or a named file is missing (nothing written).
Re-running with the same timestamp overwrites the same two files.
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
    ap.add_argument("--decisions", help="the memory tool's citations answer for this play (records and problems)")
    ap.add_argument("--ts", required=True, help="the run's UTC timestamp")
    args = ap.parse_args(argv)

    try:
        with open(args.run, encoding="utf-8") as fh:
            run = json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"write_drive_review.py: cannot read {args.run}: {exc.__class__.__name__}\n")
        return 2
    if not isinstance(run, dict) or run.get("in_drive") is not True:
        sys.stderr.write("write_drive_review.py: this run is not inside a drive — the play's own "
                         "checkpoint applies\n")
        return 2
    lacking = [k for k in ("play", "drive_run_id", "branch", "review_dir")
               if not isinstance(run.get(k), str) or not run[k].strip()]
    if lacking:
        sys.stderr.write(f"write_drive_review.py: run.json lacks {', '.join(lacking)} — nothing written\n")
        return 2
    if not args.ts.strip() or any(c in args.ts for c in "/\\") or args.ts.startswith("."):
        sys.stderr.write(f"write_drive_review.py: --ts `{args.ts}` must be a plain timestamp\n")
        return 2
    attached = {}
    for item in args.attach:
        name, sep, path = item.partition("=")
        if not sep or not name or not path:
            sys.stderr.write(f"write_drive_review.py: --attach wants name=path, got `{item}`\n")
            return 2
        attached[name] = path
    missing = [p for p in [args.summary, *attached.values(), *([args.decisions] if args.decisions else [])]
               if not os.path.isfile(p)]
    if missing:
        sys.stderr.write(f"write_drive_review.py: missing {', '.join(missing)} — nothing written\n")
        return 2
    decisions, problems = [], []
    if args.decisions:
        try:
            with open(args.decisions, encoding="utf-8") as fh:
                answer = json.load(fh)
        except ValueError:
            answer = None
        if not (isinstance(answer, dict) and answer.get("ok") is True and answer.get("command") == "citations"
                and answer.get("contract_version") == "4" and isinstance(answer.get("records"), list)
                and isinstance(answer.get("problems"), list)):
            sys.stderr.write(f"write_drive_review.py: {args.decisions} is not the memory tool's citations "
                             "answer (contract version 4) — nothing written\n")
            return 2
        decisions, problems = answer["records"], answer["problems"]
        # only this play's decisions, for this run's issue: another play's would read as this one's
        play = "/" + run["play"].lstrip("/")
        foreign = [r.get("citation_id") if isinstance(r, dict) else repr(r) for r in decisions
                   if not isinstance(r, dict) or r.get("play") != play
                   or (run.get("issue") is not None and str(r.get("issue")) != str(run["issue"]))]
        if foreign:
            sys.stderr.write(f"write_drive_review.py: {args.decisions} holds decisions of another play or issue "
                             f"({', '.join(map(str, foreign))}) — nothing written\n")
            return 2

    base = os.path.join(run["review_dir"], f"{run['play']}-{args.ts}")
    if os.path.abspath(args.summary) == os.path.abspath(base + ".md"):
        sys.stderr.write("write_drive_review.py: --summary is the record's own file — nothing written\n")
        return 2
    os.makedirs(run["review_dir"], exist_ok=True)
    shutil.copyfile(args.summary, base + ".md")
    record = {"play": run["play"], "drive_run_id": run["drive_run_id"], "drive": run.get("drive"),
              "issue": run.get("issue"), "branch": run["branch"], "recorded_at": args.ts,
              "summary": os.path.basename(base + ".md"), "attachments": attached,
              "decisions": decisions, "decision_problems": problems, "decided": False}
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
