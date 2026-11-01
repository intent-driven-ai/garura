#!/usr/bin/env python3
"""
remove_plans.py — delete plans from the plans folder, once a person has approved it (remove-plan).

Git keeps every deleted file. The script never opens a file under a plan's folder, because that
folder holds evals no one here may read: it counts and deletes them by name only. It never touches
the tracker or the product model.

    python3 remove_plans.py --request <working>/remove-plans.json --plans-dir <plans_base> \
        --out <working>/remove-plans-report.json

remove-plans.json:
    {"by": "<the play or run that asks>", "approved_by": "<the person>", "plans": [606, 717]}

Refused, nothing changed: no approved_by; an empty list; a plan id that is not digits only (an int
or a digit string, so no path can leave the folder); the same plan twice; a plan with no
<plans-dir>/<id>.yaml, or one that does not parse as a mapping; a plan whose branch is not null; a
plan that stays and names a plan being removed in its needs_plans (or a plan file that cannot be
read to tell).

All or nothing. Every check runs before the first change. Each plan file and folder
(<plans-dir>/<id>/, when there) then moves into one temporary folder beside the plans folder; only
at the very end is that folder deleted. A file or folder with no permissions gets its owner's
read and write back on the way, with no file opened, so the delete cannot stop on it. On any failure
everything moves back, with the permissions it had, and the exit is 2.

remove-plans-report.json: by, approved_by, removed: one row per plan with id, title, plan_status,
items (tree nodes by status, walking children), folder_files, deleted (relative to the plans
folder's parent). No git, no network. Exit 0 done, 2 refused.
"""

import argparse
import json
import os
import re
import shutil
import stat
import sys
import tempfile

import yaml

PLAN_ID = re.compile(r"[0-9]+")


class Refused(Exception):
    pass


def plan_ids(request):
    plans = request.get("plans")
    if not isinstance(plans, list) or not plans:
        raise Refused("the request names no plans to remove")
    ids = []
    for plan in plans:
        text = str(plan)
        if not isinstance(plan, (int, str)) or not PLAN_ID.fullmatch(text):
            raise Refused(f"the plan id {plan!r} is not digits only")
        if text in ids:
            raise Refused(f"plan {text} is named twice")
        ids.append(text)
    return ids


def read_plan(path):
    """The parsed plan file; Refused when it cannot be read or does not parse."""
    try:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except (OSError, ValueError, yaml.YAMLError) as err:
        raise Refused(f"the plan file {os.path.basename(path)} cannot be read: {err}") from err


def check(plans_dir, request):
    """Every check, before the first change. Returns (by, approved_by, {id: plan})."""
    if not isinstance(request, dict):
        raise Refused("the request is not a JSON object")
    who = request.get("approved_by")
    if not isinstance(who, str) or not who.strip():
        raise Refused("the request names no person who approved it (approved_by); no plan goes without one")
    if not os.path.isdir(plans_dir):
        raise Refused(f"there is no plans folder at {plans_dir}")
    plans = {}
    for pid in plan_ids(request):
        path = os.path.join(plans_dir, f"{pid}.yaml")
        if not os.path.isfile(path):
            raise Refused(f"plan {pid} has no file {pid}.yaml in the plans folder")
        data = read_plan(path)
        if not isinstance(data, dict):
            raise Refused(f"the plan file {pid}.yaml does not hold a mapping")
        if data.get("branch") is not None:
            raise Refused(f"plan {pid} is still on the branch {data['branch']}")
        plans[pid] = data
    for name in sorted(os.listdir(plans_dir)):
        stem, ext = os.path.splitext(name)
        if ext != ".yaml" or not PLAN_ID.fullmatch(stem) or stem in plans:
            continue
        data = read_plan(os.path.join(plans_dir, name))
        needs = data.get("needs_plans") if isinstance(data, dict) else None
        for need in needs if isinstance(needs, list) else [needs]:
            if str(need) in plans:
                raise Refused(f"plan {stem} stays and needs plan {need}, which this request removes")
    return request.get("by") or "a play", who, plans


def count_items(nodes, counts):
    """Count the tree's nodes by status, walking children."""
    for node in nodes if isinstance(nodes, list) else []:
        if isinstance(node, dict):
            status = str(node.get("status") or "no status")
            counts[status] = counts.get(status, 0) + 1
            count_items(node.get("children"), counts)
    return counts


def open_up(path, bits, opened, container):
    """Give the owner these permission bits, and note what the path had, to put it back."""
    mode = stat.S_IMODE(os.lstat(path).st_mode)
    if mode & bits != bits:
        opened.append((os.path.relpath(path, container), mode))
        os.chmod(path, mode | bits)


def open_and_count(folder, opened, container):
    """The number of files under the folder, by names only; every file and folder is left so its
    owner can read and write it. No file is opened."""
    open_up(folder, 0o700, opened, container)
    with os.scandir(folder) as found:
        names = sorted(found, key=lambda e: e.name)
    count = 0
    for item in names:
        if item.is_symlink():
            count += 1
        elif item.is_dir(follow_symlinks=False):
            count += open_and_count(item.path, opened, container)
        else:
            open_up(item.path, 0o600, opened, container)
            count += 1
    return count


def is_folder(path):
    return os.path.isdir(path) and not os.path.islink(path)


def put_back(temp, plans_dir, moved, opened):
    """Move everything back with the permissions it had. Returns what could not be put back."""
    stuck = []
    for name in reversed(moved):
        try:
            os.rename(os.path.join(temp, name), os.path.join(plans_dir, name))
        except OSError:
            stuck.append(name)
    for rel, mode in reversed(opened):
        try:
            os.chmod(os.path.join(plans_dir, rel), mode)
        except OSError:
            if rel not in stuck:
                stuck.append(rel)
    try:
        os.rmdir(temp)
    except OSError:
        stuck.append(temp)
    return stuck


def write_report(out, report):
    """Write the report. Returns what the file held before, or None when it was not there."""
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    before = None
    if os.path.exists(out):
        with open(out, "rb") as fh:
            before = fh.read()
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
        fh.write("\n")
    return before


def take_report_back(out, before):
    if before is None:
        os.remove(out)
    else:
        with open(out, "wb") as fh:
            fh.write(before)


def remove(plans_dir, plans, out, by, who):
    """Move the plans aside, write the report, delete the temporary folder; undo it all on failure."""
    temp = tempfile.mkdtemp(prefix=".garura-remove-plans-", dir=os.path.dirname(plans_dir))
    base = os.path.basename(plans_dir)
    moved, opened = [], []
    report_written, before, deleting = False, None, False
    try:
        for pid in plans:
            for name in (f"{pid}.yaml", pid):
                source = os.path.join(plans_dir, name)
                if os.path.lexists(source):
                    if is_folder(source):
                        open_up(source, 0o700, opened, plans_dir)
                    os.rename(source, os.path.join(temp, name))
                    moved.append(name)
        rows = []
        for pid, data in plans.items():
            folder = os.path.join(temp, pid)
            rows.append({"id": int(pid), "title": data.get("title"), "plan_status": data.get("status"),
                         "items": count_items(data.get("tree"), count_items(data.get("children"), {})),
                         "folder_files": open_and_count(folder, opened, temp) if is_folder(folder) else 0,
                         "deleted": [os.path.join(base, n) for n in (f"{pid}.yaml", pid) if n in moved]})
        report = {"by": by, "approved_by": who, "removed": rows}
        before = write_report(out, report)
        report_written = True
        deleting = True
        shutil.rmtree(temp)
    except OSError as err:
        stuck = put_back(temp, plans_dir, moved, opened)
        if report_written:
            take_report_back(out, before)
        note = ""
        if stuck:
            note = f"; these could not be put back: {', '.join(stuck)}"
        elif deleting:
            note = "; the delete had begun, so any file now missing is in git"
        raise OSError(f"{err}{note}") from err
    return report


def main():
    ap = argparse.ArgumentParser(description="Delete plans from the plans folder, on a person's approval.")
    ap.add_argument("--request", required=True)
    ap.add_argument("--plans-dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    plans_dir = os.path.realpath(a.plans_dir)
    try:
        with open(a.request, encoding="utf-8") as fh:
            request = json.load(fh)
        by, who, plans = check(plans_dir, request)
    except (Refused, OSError, ValueError) as err:
        sys.stderr.write(f"remove_plans.py: refused, nothing changed: {err}\n")
        return 2
    try:
        report = remove(plans_dir, plans, a.out, by, who)
    except OSError as err:
        sys.stderr.write(f"remove_plans.py: a move or delete failed, everything is back as it was: {err}\n")
        return 2
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
