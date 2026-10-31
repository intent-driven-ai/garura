#!/usr/bin/env python3
"""session_files.py — the fixed file steps of an /update-plan session (HS-3).

    python3 session_files.py numbers --plan-file <plans>/<id>.yaml --out <numbers.json>
    python3 session_files.py restore --folder <stm_base><id>/ --repo . --out <restore.json>
    python3 session_files.py guard --model-ops <model-ops.json> --model-record <model-record.json> \
        [--model-record <model-record-story.json>] --product-base <product_base> --out <guard-report.json>
    python3 session_files.py adopt --start <start folder> --work <working> --out <adopt.json>
    python3 session_files.py clear --start <start folder> --work <working> [--keep]

`numbers` writes every issue number of the plan file, the plan's own number first, then the tree
in order, each once: {"plan": "<id>", "issues": [<id>, ...], "csv": "<id>,..."}. Step 4 hands `csv`
to the tracker skill, which reads those issues.

`restore` runs on "abort": it puts the folder back as it was at the branch's last commit — each
changed tracked file restored, each new file deleted (git's ignored files are left alone) — and
writes {"folder", "restored": [...], "deleted": [...], "clean": true|false}. `clean` is true when
git shows nothing changed in the folder afterwards. Exit 0 written; 1 not clean afterwards; 2 bad
input (nothing changed).

`guard` runs the shared scoped-write guard (`scoped_write_guard.py`, beside this script) once, after
the last model write and before the commit (ADR 062): every model path that changed must be a file
a model record names (Step 8's and Step 9's, read as one), or the model index (`_spine.yaml`); any
other changed model path is put back (`--restore`). `model-ops.json` must be there and in shape
(Step 7 always writes it); when it has parts, a record must be given and on disk. A missing or
misshapen file is refused (exit 2) and nothing is put back, so a missing record never reads as
"nothing may change". The guard writes the report; exit 0 when nothing was
out of scope, 1 when it put something back (the landing stops for the person), 2 bad input.

`adopt` and `clear` keep the session's own files in one folder (#1001). Everything the session
makes before the plan is known (the template copies, the start marker, plan.json) is in the start
folder; `adopt` moves it into the plan's session folder (`<working>`) once the plan is known,
replacing the session's own files of an earlier session there and keeping that session's list
(changes.yaml and its old copies), then removes the start folder. `clear` runs at the close: it
removes the start folder and `<working>`, and then the parent folder when nothing else is in it.
`--keep` keeps `<working>` (a landing that stopped part way: its records let the next session carry
on). `adopt` writes {"moved": [...], "left": [...]} to --out; `clear` prints {"removed": [...],
"kept": [...], "left": [...]} and writes no file, since it would be left behind (`left` names what
is still under the parent folder). Exit 0; 2 bad input.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402


def numbers(plan):
    out = [plan.get("id")]

    def walk(nodes):
        for n in nodes or []:
            if isinstance(n, dict):
                if n.get("issue") is not None:
                    out.append(n["issue"])
                walk(n.get("children"))

    walk(plan.get("tree"))
    seen, kept = set(), []
    for n in out:
        if n is not None and str(n) not in seen:
            seen.add(str(n))
            kept.append(int(n))
    return kept


def changed(folder, repo):
    """(tracked files changed or deleted, new files) under the folder, from git status -z."""
    res = subprocess.run(["git", "status", "--porcelain", "-z", "-uall", "--", folder], cwd=repo,
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise ps.Refused(f"git status failed: {res.stderr.strip()}")
    tracked, new = [], []
    parts = res.stdout.split("\0")
    i = 0
    while i < len(parts):
        row = parts[i]
        i += 1
        if len(row) < 4:
            continue
        code, path = row[:2], row[3:]
        if code[0] in "RC":
            i += 1  # the rename's old path follows
        (new if code == "??" else tracked).append(path)
    return tracked, new


def restore(folder, repo):
    if os.path.isabs(folder) or ".." in folder.replace("\\", "/").split("/"):
        raise ps.Refused(f"{folder} must be a folder inside the repository")
    tracked, new = changed(folder, repo)
    if tracked:
        res = subprocess.run(["git", "restore", "--staged", "--worktree", "--source=HEAD", "--", *tracked],
                             cwd=repo, capture_output=True, text=True)
        if res.returncode != 0:
            raise ps.Refused(f"git restore failed: {res.stderr.strip()}")
    for path in new:
        full = os.path.join(repo, path)
        if os.path.isfile(full) or os.path.islink(full):
            os.remove(full)
    left_tracked, left_new = changed(folder, repo)
    return {"folder": folder, "restored": tracked, "deleted": new, "clean": not (left_tracked or left_new)}


def guard(model_ops, model_records, product_base, out):
    ops = ps.read_json(model_ops, "model-ops.json")  # Step 7 always writes it; missing is refused
    if not isinstance(ops, dict) or not isinstance(ops.get("parts") or [], list):
        raise ps.Refused(f"{model_ops} is not a model-ops record ({{parts: [...]}})")
    if (ops.get("parts") or []) and not model_records:
        raise ps.Refused("model-ops.json has parts, but no model record was given; nothing is put back")
    rec = ps.model_records(model_records)
    allow = ["product-os/_spine.yaml"] + rec["files"]
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scoped_write_guard.py")
    cmd = [sys.executable, script, "--product-base", product_base, "--base-ref", "HEAD", "--restore",
           "--out", out]
    for path in allow:
        cmd += ["--allow", path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not os.path.isfile(out):
        raise ps.Refused(f"the scoped-write guard failed: {(res.stderr or res.stdout).strip()}")
    return ps.read_json(out, "guard-report.json")


def adopt(start, work):
    if not os.path.isdir(start):
        raise ps.Refused(f"no start folder {start}")
    os.makedirs(work, exist_ok=True)
    moved = []
    for name in sorted(os.listdir(start)):
        src, dst = os.path.join(start, name), os.path.join(work, name)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        elif os.path.exists(dst):
            os.remove(dst)
        shutil.move(src, dst)
        moved.append(name)
    os.rmdir(start)
    return {"moved": moved, "left": sorted(os.listdir(work))}


def clear(start, work, keep):
    removed, kept = [], []
    for folder in (start, work):
        if not folder or not os.path.isdir(folder):
            continue
        if keep and folder == work:
            kept.append(folder)
            continue
        shutil.rmtree(folder)
        removed.append(folder)
    parent = os.path.dirname(os.path.normpath(work or start))
    left = sorted(os.listdir(parent)) if os.path.isdir(parent) else []
    if os.path.isdir(parent) and not left:
        os.rmdir(parent)
        removed.append(parent)
    return {"removed": removed, "kept": kept, "left": left}


def main(argv=None):
    ap = argparse.ArgumentParser(description="the fixed file steps of an /update-plan session")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("numbers")
    n.add_argument("--plan-file", required=True)
    n.add_argument("--out", required=True)
    r = sub.add_parser("restore")
    r.add_argument("--folder", required=True)
    r.add_argument("--repo", default=".")
    r.add_argument("--out", required=True)
    g = sub.add_parser("guard")
    g.add_argument("--model-ops", required=True)
    g.add_argument("--model-record", action="append", default=[])
    g.add_argument("--product-base", required=True)
    g.add_argument("--out", required=True)
    a = sub.add_parser("adopt")
    a.add_argument("--start", required=True)
    a.add_argument("--work", required=True)
    a.add_argument("--out", required=True)
    c = sub.add_parser("clear")
    c.add_argument("--start", required=True)
    c.add_argument("--work", default=None)
    c.add_argument("--keep", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "adopt":
            ps.write_json(args.out, adopt(args.start, args.work))
            return 0
        if args.cmd == "clear":
            print(json.dumps(clear(args.start, args.work, args.keep), indent=2))
            return 0
        if args.cmd == "guard":
            report = guard(args.model_ops, args.model_record, args.product_base, args.out)
            return 1 if report.get("violations") else 0
        if args.cmd == "numbers":
            plan = ps.load_plan(args.plan_file)
            found = numbers(plan)
            ps.write_json(args.out, {"plan": str(plan.get("id")), "issues": found,
                                     "csv": ",".join(str(n) for n in found)})
            return 0
        rec = restore(args.folder, args.repo)
    except ps.Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    ps.write_json(args.out, rec)
    return 0 if rec["clean"] else 1


if __name__ == "__main__":
    sys.exit(main())
