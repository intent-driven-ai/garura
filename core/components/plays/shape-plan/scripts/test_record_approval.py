#!/usr/bin/env python3
"""test_record_approval.py — record_approval.py records the typed answer, ties it to the files shown, and gates every write (C8).

    python3 test_record_approval.py
"""
import hashlib
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import check, finish, read_json, run, write  # noqa: E402


def main():
    print("record_approval.py")
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "approval.json")
        shown = [write(os.path.join(tmp, n), f"{n} as shown\n") for n in ("brief.md", "work-items.json", "drafts.json")]
        files = ["--brief", shown[0], "--work-items", shown[1], "--drafts", shown[2]]

        def record(decision, reply, at, *extra, target=out):
            return run("record_approval.py", "--decision", decision, "--reply", reply, "--at", at,
                       *(extra or files), "--out", target)

        code, _, _ = run("record_approval.py", "verify", "--file", out)
        check("verify with no file: exit 2", code == 2)
        code, _, _ = record("change", "change: a shorter title", "2026-10-25T10:00:00Z")
        check("a change is recorded in the person's words", code == 0 and read_json(out)["reply"] == "change: a shorter title")
        code, _, _ = run("record_approval.py", "verify", "--file", out)
        check("verify on a change: exit 1", code == 1)
        record("yes", "yes", "2026-10-25T10:05:00Z")
        rec = read_json(out)
        check("yes is on top and the change is kept in history",
              rec["decision"] == "yes" and rec["history"][0]["decision"] == "change")
        check("the sha256 of the brief, work-items.json and drafts.json is recorded",
              rec["files"]["brief"]["sha256"] == hashlib.sha256(b"brief.md as shown\n").hexdigest()
              and rec["files"]["work_items"]["path"] == shown[1] and len(rec["files"]["drafts"]["sha256"]) == 64)
        code, _, _ = run("record_approval.py", "verify", "--file", out)
        check("verify on yes: exit 0", code == 0)
        record("stop", "stop", "2026-10-25T10:06:00Z")
        code, _, _ = run("record_approval.py", "verify", "--file", out)
        check("verify on stop: exit 1", code == 1)
        other = os.path.join(tmp, "other.json")
        code, _, _ = record("yes", "  ", "x", target=other)
        check("an empty reply is refused and nothing is written", code == 2 and not os.path.exists(other))
        code, _, _ = record("yes", "yes", "x", "--brief", os.path.join(tmp, "none.md"), "--work-items", shown[1],
                            "--drafts", shown[2], target=other)
        check("a brief that cannot be read is refused and nothing is written", code == 2 and not os.path.exists(other))
    return finish()


if __name__ == "__main__":
    sys.exit(main())
