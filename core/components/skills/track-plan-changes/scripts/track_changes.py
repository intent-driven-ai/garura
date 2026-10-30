#!/usr/bin/env python3
"""track_changes.py — read a plan's issues, and make an approved session's tracker writes (#730).

    python3 track_changes.py read  --issues 717,956,720 [--tracker-file <json>]
                                   [--config .garura/core/config.yaml] --out <snapshot.json>
    python3 track_changes.py apply --ops <github-ops.json> --changes <changes.yaml>
                                   --approval <approval.json> [--tracker-file <json>]
                                   [--read 717,956 --before <snapshot-before.json>
                                    --after <snapshot-after.json>]
                                   [--config ...] --out <github-record.json>

`read` writes {"issues": {"<number>": issue}} for each number (an issue the tracker does not have
is listed in "missing"). It writes nothing in the tracker.

`apply` refuses (exit 2, nothing written) unless approval.json reads `decision: approved` and its
`list_sha` is the sha256 of the changes file now — so only the list the person saw lands. Then it
makes each op of github-ops.json, in order:

    {"id": "e1", "op": "close",  "issue": 730, "reason": "completed" | "not planned"}
    {"id": "e2", "op": "reopen", "issue": 909}
    {"id": "e3", "op": "title",  "issue": 931, "title": "..."}
    {"id": "e4", "op": "body",   "issue": 730, "body": "..."}
    {"id": "e5", "op": "type",   "issue": 917, "type": "Chore"}
    {"id": "e6", "op": "parent", "issue": 1001, "from": 730, "to": 720}
    {"id": "e7", "op": "create", "title": "...", "body": "...", "type": "Story", "parent": 720}

An `issue` or `parent` written "@e7" is the number op e7 made. The record is written after every
write, so a run that stops part way names what was done; run again, it skips each op the record
has. Each issue a create makes carries a marker line, "Made by /update-plan (list <12 hex>, op
<id>).", and before a create the tracker is searched for it: an issue an earlier run made (the
run died before its record was written, or the host gave no number back) is found and used, never
made twice. The record is tied to the approved list (`list_sha`): a record from another list is
refused, never skipped over. An op whose result is already in the tracker (a close of a
closed issue with the same reason, a title that already reads so) is recorded as `already`.

With --read, `apply` also reads those issues just before its first write (--before) and again
after its last (--after), so the play can check that nothing else changed.

Record: {"ok", "list_sha", "done": {"<id>": {"op", "issue", "result", "how"}}, "failed": null |
{"id", "error"}}; `how` is done, made, found (an earlier run made it) or already.
Exit 0 every op done; 1 a write failed (the record names it); 2 refused or bad input.
"""

import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tracker import TrackerError, open_tracker  # noqa: E402

REASONS = {"completed": "COMPLETED", "not planned": "NOT_PLANNED"}


class Refused(Exception):
    pass


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def read_json(path, what):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as e:
        raise Refused(f"cannot read {what} ({path}): {e}")


def write_json(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    os.replace(tmp, path)


def snapshot(tr, numbers):
    out = {"issues": {}, "missing": []}
    for raw in [n for n in numbers.split(",") if n.strip()]:
        issue = tr.get(int(raw))
        if issue is None:
            out["missing"].append(int(raw))
        else:
            out["issues"][str(issue["number"])] = issue
    return out


def read(args):
    write_json(args.out, snapshot(open_tracker(args.config, args.tracker_file), args.issues))
    return 0


def resolve(value, done):
    if isinstance(value, str) and value.startswith("@"):
        ref = value[1:]
        if ref not in done or done[ref].get("result") is None:
            raise Refused(f"{value} names an op that has not made an issue")
        return int(done[ref]["result"])
    return None if value is None else int(value)


def marker(list_sha, op_id):
    return f"Made by /update-plan (list {list_sha[:12]}, op {op_id})."


def run_op(tr, op, done, list_sha):
    kind = op["op"]
    if kind == "create":
        parent = resolve(op.get("parent"), done)
        mark = marker(list_sha, op["id"])
        found = tr.find_marked(mark)
        if found:
            return "found", found[0]
        body = (op.get("body") or "").rstrip("\n")
        body = (body + "\n\n" if body else "") + mark + "\n"
        try:
            return "made", tr.create(op["title"], body, op["type"], parent)
        except TrackerError:
            found = tr.find_marked(mark)
            if found:
                return "found", found[0]
            raise
    number = resolve(op["issue"], done)
    now = tr.get(number)
    if now is None:
        raise TrackerError(f"issue #{number} is not in the tracker")
    if kind == "close":
        want = REASONS[op["reason"]]
        if now["state"] == "CLOSED" and now["state_reason"] == want:
            return "already", number
        if now["state"] == "CLOSED":
            tr.reopen(number)
        tr.close(number, op["reason"])
    elif kind == "reopen":
        if now["state"] == "OPEN":
            return "already", number
        tr.reopen(number)
    elif kind == "title":
        if now["title"] == op["title"]:
            return "already", number
        tr.set_title(number, op["title"])
    elif kind == "body":
        if now["body"] == op["body"]:
            return "already", number
        tr.set_body(number, op["body"])
    elif kind == "type":
        if now["type"] == op["type"]:
            return "already", number
        tr.set_type(number, op["type"])
    elif kind == "parent":
        to = resolve(op.get("to"), done)
        if now["parent"] == to:
            return "already", number
        if now["parent"] is not None:
            tr.detach(now["parent"], number)
        if to is not None:
            tr.attach(to, number)
    else:
        raise Refused(f"op {op.get('id')} has an unknown op '{kind}'")
    return "done", number


def apply(args):
    approval = read_json(args.approval, "approval.json")
    if approval.get("decision") != "approved":
        raise Refused("the session is not approved; nothing is written")
    if approval.get("list_sha") != sha256_of(args.changes):
        raise Refused("the list changed after the person approved it; nothing is written")
    ops = read_json(args.ops, "github-ops.json").get("ops") or []
    ids = [o.get("id") for o in ops]
    if len(set(ids)) != len(ids) or None in ids:
        raise Refused("each op needs its own id")
    list_sha = approval["list_sha"]
    rec = {"ok": False, "list_sha": list_sha, "done": {}, "failed": None}
    if os.path.isfile(args.out):
        old = read_json(args.out, "the record")
        if old.get("list_sha") != list_sha:
            raise Refused("the record there is from another list; move it aside, nothing is written")
        rec["done"] = old.get("done") or {}
    tr = open_tracker(args.config, args.tracker_file)
    if args.read and args.before and not os.path.isfile(args.before):
        write_json(args.before, snapshot(tr, args.read))
    for op in ops:
        if op["id"] in rec["done"]:
            continue
        try:
            how, number = run_op(tr, op, rec["done"], list_sha)
        except TrackerError as e:
            rec["failed"] = {"id": op["id"], "error": str(e)}
            write_json(args.out, rec)
            return 1
        rec["done"][op["id"]] = {"op": op["op"], "issue": number,
                                 "result": number if how in ("made", "found") else None, "how": how}
        write_json(args.out, rec)
    rec["ok"] = True
    write_json(args.out, rec)
    if args.read and args.after:
        made = [str(d["result"]) for d in rec["done"].values() if d.get("result")]
        write_json(args.after, snapshot(tr, ",".join([args.read] + made)))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="read a plan's issues, or make an approved session's writes")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("read")
    r.add_argument("--issues", required=True)
    a = sub.add_parser("apply")
    a.add_argument("--ops", required=True)
    a.add_argument("--changes", required=True)
    a.add_argument("--approval", required=True)
    a.add_argument("--read")
    a.add_argument("--before")
    a.add_argument("--after")
    for p in (r, a):
        p.add_argument("--tracker-file")
        p.add_argument("--config", default=".garura/core/config.yaml")
        p.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        return read(args) if args.cmd == "read" else apply(args)
    except Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    except TrackerError as e:
        print(f"tracker: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
