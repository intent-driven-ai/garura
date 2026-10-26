#!/usr/bin/env python3
"""test_check_tracker.py — check_tracker.py reads each work item back: type, no label, sub-issues, moved out open (D4; C4, C13).

    python3 test_check_tracker.py
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, empty_tracker, finish, flow, make_model, paths, read,  # noqa: E402
                          read_json, run, set_slice, write)


def verdict(p):
    out = os.path.join(p["working"], "tracker-check.json")
    code, _, _ = run("check_tracker.py", "--record", p["record"], "--tracker-file", p["tracker"], "--out", out)
    return code, read_json(out) if os.path.isfile(out) else None


def edit(p, number, **change):
    data = read_json(p["tracker"])
    for it in data["issues"]:
        if it["number"] == number:
            it.update(change)
    write(p["tracker"], data)


def main():
    print("check_tracker.py")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        empty_tracker(p)
        flow(root, p)
        code, res = verdict(p)
        check("after a first plan: ok", code == 0 and res["ok"] and len(res["checked"]) == 4)
        good = read(p["tracker"])
        rec = read_json(p["record"])
        epic = rec["epics"]["sl-self-booking"]
        story = rec["maps"]["sl-self-booking"]["ft-pick"]

        edit(p, story, labels=["work-item"])
        code, res = verdict(p)
        check("a story with a label: not ok", code == 1 and any("label" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))
        edit(p, epic, type="Feature")
        code, res = verdict(p)
        check("an epic whose type is not Epic: not ok", code == 1 and any("not Epic" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))
        edit(p, story, type="Bug")
        code, res = verdict(p)
        check("a story whose type is not Story: not ok", code == 1 and any("not Story" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))
        edit(p, epic, sub_issues=[story])
        code, res = verdict(p)
        check("an epic that lacks a story of its slice: not ok",
              code == 1 and any("is not a sub-issue of epic" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))
        # #879: a work order with its three stories and two closed chores passes, and lists them.
        data = read_json(p["tracker"])
        stories = sorted(rec["maps"]["sl-self-booking"].values())
        data["issues"] += [{"number": 90, "title": "Old chore", "type": "Chore", "labels": [], "state": "closed",
                            "body": "", "sub_issues": []},
                           {"number": 91, "title": "Older chore", "type": "Chore", "labels": [], "state": "closed",
                            "body": "", "sub_issues": []}]
        write(p["tracker"], data)
        edit(p, epic, sub_issues=stories + [90, 91])
        code, res = verdict(p)
        check("an epic with its stories and two closed chores: ok, and the chores are its others",
              code == 0 and res["ok"] and res["others"] == {"sl-self-booking": [90, 91]})
        rec2 = dict(rec, others={"sl-self-booking": [90, 91]})
        write(p["record"], rec2)
        edit(p, epic, sub_issues=stories + [90])
        code, res = verdict(p)
        check("an other child the record names, taken off the epic: not ok",
              code == 1 and any("other child #91" in x for x in res["problems"]))
        write(p["record"], rec)
        write(p["tracker"], json.loads(good))
        edit(p, story, body="Represents: ft-pick\n")
        code, res = verdict(p)
        check("a story with no Scope of work: not ok", code == 1 and any("Scope of work" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))

        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind"])
        flow(root, p)
        code, res = verdict(p)
        moved = read_json(p["record"])["moved_out"][0]["issue"]
        check("a moved-out story that is open and off the epic: ok", code == 0 and res["ok"])
        edit(p, moved, state="closed")
        code, res = verdict(p)
        check("a moved-out story that is closed: not ok", code == 1 and any("not open" in x for x in res["problems"]))
        rec = read_json(p["record"])
        rec["epics"]["sl-x"] = 500
        write(p["record"], rec)
        code, res = verdict(p)
        check("an issue the record names that the tracker lacks: not ok", code == 1 and any("#500" in x for x in res["problems"]))
    return finish()


if __name__ == "__main__":
    sys.exit(main())
