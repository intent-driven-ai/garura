#!/usr/bin/env python3
"""test_record_approval.py — record_approval.py records the typed answer and gates every write (C8).

    python3 test_record_approval.py
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import check, finish, read_json, run  # noqa: E402


def main():
    print("record_approval.py")
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "approval.json")
        code, _, _ = run("record_approval.py", "verify", "--file", out)
        check("verify with no file: exit 2", code == 2)
        code, rec, _ = run("record_approval.py", "--decision", "change", "--reply", "change: a shorter title",
                           "--at", "2026-10-25T10:00:00Z", "--out", out)
        check("a change is recorded in the person's words", code == 0 and read_json(out)["reply"] == "change: a shorter title")
        code, _, _ = run("record_approval.py", "verify", "--file", out)
        check("verify on a change: exit 1", code == 1)
        run("record_approval.py", "--decision", "yes", "--reply", "yes", "--at", "2026-10-25T10:05:00Z", "--out", out)
        rec = read_json(out)
        check("yes is on top and the change is kept in history",
              rec["decision"] == "yes" and rec["history"][0]["decision"] == "change")
        code, _, _ = run("record_approval.py", "verify", "--file", out)
        check("verify on yes: exit 0", code == 0)
        run("record_approval.py", "--decision", "stop", "--reply", "stop", "--at", "2026-10-25T10:06:00Z", "--out", out)
        code, _, _ = run("record_approval.py", "verify", "--file", out)
        check("verify on stop: exit 1", code == 1)
        code, _, _ = run("record_approval.py", "--decision", "yes", "--reply", "  ", "--at", "x", "--out",
                         os.path.join(tmp, "other.json"))
        check("an empty reply is refused and nothing is written",
              code == 2 and not os.path.exists(os.path.join(tmp, "other.json")))
    return finish()


if __name__ == "__main__":
    sys.exit(main())
