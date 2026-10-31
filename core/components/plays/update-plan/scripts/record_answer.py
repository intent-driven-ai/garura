#!/usr/bin/env python3
"""record_answer.py — record the person's answer to the list, tied to the list they saw (C5, C6).

    python3 record_answer.py record --reply "<the person's words>" --changes <changes.yaml> \
        --at <UTC time> --out <answer.json>
    python3 record_answer.py verify --answer <answer.json> --changes <changes.yaml> --out <verify.json>

`record` reads the reply by a fixed rule: only the word "approved" (any case, with or without a
full stop) is `approved`; only "rejected" is `rejected` (nothing lands, and the session goes on:
the person changes the list until it is ready); only "abort" is `abort` (nothing lands, the list
is dropped, a plan branch the session cut is undone, and the session goes back where it
started); anything else — a question, a new instruction,
"approved, but …" — is `other`, and the play answers or follows it, shows the list again and
asks again. An empty reply is refused. The list's sha256 is recorded with the answer;
every earlier answer is kept in `history`.

`verify` is the gate before the landing's first write: exit 0 only when answer.json reads
`approved` and the list still has the recorded sha256; exit 1 otherwise; 2 when a file cannot be
read. It writes its own record, verify.json — {ok, decision, list_sha, answer_sha, why} — on a
pass and on a fail, so an earlier pass never stays behind a later fail.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402


def decide(reply):
    word = re.sub(r"[.!\s]+$", "", reply.strip()).lower()
    if word == "approved":
        return "approved"
    if word == "rejected":
        return "rejected"
    if word == "abort":
        return "abort"
    return "other"


def main(argv=None):
    ap = argparse.ArgumentParser(description="record the person's answer to the list")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("--reply", required=True)
    r.add_argument("--changes", required=True)
    r.add_argument("--at", required=True)
    r.add_argument("--out", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--answer", required=True)
    v.add_argument("--changes", required=True)
    v.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    if args.cmd == "verify":
        try:
            ans = ps.read_json(args.answer, "answer.json")
            sha = ps.sha256_of(args.changes)
        except (ps.Refused, OSError) as e:
            print(f"cannot verify: {e}", file=sys.stderr)
            return 2
        ok = ans.get("decision") == "approved" and ans.get("list_sha") == sha
        why = None if ok else ("the answer is not approved" if ans.get("decision") != "approved"
                               else "the list changed after it was approved")
        ps.write_json(args.out, {"ok": ok, "decision": ans.get("decision"), "list_sha": sha,
                                 "answer_sha": ans.get("list_sha"), "why": why})
        if ok:
            return 0
        print(f"not approved for this list: {why}; nothing may be written", file=sys.stderr)
        return 1
    if not args.reply.strip():
        print("refused: an empty reply is not an answer", file=sys.stderr)
        return 2
    try:
        sha = ps.sha256_of(args.changes)
    except OSError as e:
        print(f"refused: cannot read the list: {e}", file=sys.stderr)
        return 2
    history = []
    if os.path.isfile(args.out):
        old = ps.read_json(args.out, "answer.json")
        history = (old.get("history") or []) + [{k: old.get(k) for k in ("decision", "reply", "at", "list_sha")}]
    ps.write_json(args.out, {"decision": decide(args.reply), "reply": args.reply, "at": args.at,
                             "list_sha": sha, "history": history})
    return 0


if __name__ == "__main__":
    sys.exit(main())
