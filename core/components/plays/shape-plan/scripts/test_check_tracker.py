#!/usr/bin/env python3
"""test_check_tracker.py — check_tracker.py reads each work item back: type, no label, the exact line, sub-issues, moved out open, opened again (D4; C3, C13, C16, C17).

    python3 test_check_tracker.py
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, empty_tracker, finish, flow, full_body, make_model, paths,  # noqa: E402
                          read, read_json, run, set_slice, write)


def verdict(p):
    out = os.path.join(p["working"], "tracker-check.json")
    code, _, _ = run("check_tracker.py", "--record", p["record"], "--work-items", p["items"],
                     "--tracker-file", p["tracker"], "--out", out)
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
        epic = rec["epic"]
        feat = rec["map"]["ft-pick"]

        edit(p, feat, labels=["work-item"])
        code, res = verdict(p)
        check("a Feature issue with a label: not ok", code == 1 and any("label" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))
        edit(p, epic, type="Feature")
        code, res = verdict(p)
        check("an epic whose type is not Epic: not ok", code == 1 and any("not Epic" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))
        edit(p, feat, type="Story")
        code, res = verdict(p)
        check("a Feature issue whose type is not Feature: not ok",
              code == 1 and any("not Feature" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))
        edit(p, feat, body=full_body("ft-pick").replace("Represents: ft-pick", "Represents: ft-pick."))
        code, res = verdict(p)
        check("a Feature issue whose Represents line is not exact: not ok",
              code == 1 and any("has no line \"Represents: ft-pick\"" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))
        edit(p, epic, sub_issues=[feat])
        code, res = verdict(p)
        check("an epic that lacks a Feature issue of the plan: not ok, named",
              code == 1 and any("is not a sub-issue of epic" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))
        data = read_json(p["tracker"])
        data["issues"].append({"number": 90, "title": "Old chore", "type": "Chore", "labels": [],
                               "state": "closed", "body": "", "sub_issues": []})
        write(p["tracker"], data)
        edit(p, epic, sub_issues=sorted(rec["map"].values()) + [90])
        code, res = verdict(p)
        check("an epic that holds work the plan does not place: not ok, named with its title (C13)",
              code == 1 and any("#90 \"Old chore\", which the plan does not place" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))
        edit(p, feat, body="Represents: ft-pick\n")
        code, res = verdict(p)
        check("a Feature issue with no Scope of work: not ok", code == 1 and any("Scope of work" in x for x in res["problems"]))
        write(p["tracker"], json.loads(good))
        bad = dict(rec, created=rec["created"] + [{"issue": feat, "kind": "story", "represents": "ft-pick"}])
        edit(p, feat, type="Story")
        write(p["record"], bad)
        code, res = verdict(p)
        check("a Story the run filed: not ok", code == 1 and any("files no Stories" in x for x in res["problems"]))
        write(p["record"], rec)
        write(p["tracker"], json.loads(good))

        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind"])
        flow(root, p)
        code, res = verdict(p)
        moved = read_json(p["record"])["moved_out"][0]["issue"]
        check("a moved-out Feature issue that is open and off the epic: ok", code == 0 and res["ok"])
        edit(p, moved, state="closed")
        code, res = verdict(p)
        check("a moved-out item that is closed: not ok", code == 1 and any("not open" in x for x in res["problems"]))
        edit(p, moved, state="open")
        epic_no = read_json(p["record"])["epic"]
        subs = [it for it in read_json(p["tracker"])["issues"] if it["number"] == epic_no][0]["sub_issues"]
        edit(p, epic_no, sub_issues=subs + [moved])
        code, res = verdict(p)
        check("a moved-out item that is still a sub-issue of the epic: not ok",
              code == 1 and any("still a sub-issue" in x for x in res["problems"]))
        rec = read_json(p["record"])
        rec["map"]["ft-x"] = 500
        write(p["record"], rec)
        code, res = verdict(p)
        check("an issue the record names that the tracker lacks: not ok", code == 1 and any("#500" in x for x in res["problems"]))
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp, features=("ft-pick", "ft-remind")), paths(tmp)
        empty_tracker(p, [{"number": 20, "title": "Send a reminder", "type": "Feature", "labels": [],
                           "state": "closed", "state_reason": "not_planned", "body": full_body("ft-remind"),
                           "sub_issues": []}])
        flow(root, p)
        code, res = verdict(p)
        check("a Feature issue opened again, under the epic: ok (C17)", code == 0 and 20 in res["checked"])
        edit(p, 20, state="closed")
        code, res = verdict(p)
        check("a Feature issue the run was to open again is closed: not ok",
              code == 1 and any("open again" in x for x in res["problems"]))
        edit(p, 20, state="open")
        rec = read_json(p["record"])
        write(p["record"], dict(rec, created=rec["created"] + [{"issue": 21, "kind": "feature",
                                                               "represents": "ft-remind", "title": "x",
                                                               "state": "open"}]))
        code, res = verdict(p)
        check("a second Feature issue filed for a feature whose issue opened again: not ok",
              code == 1 and any("second Feature issue" in x for x in res["problems"]))
        write(p["record"], dict(rec, left_out=[{"feature": "ft-pick", "issue": None, "reason": "Completed",
                                                "kind": "completed"}]))
        code, res = verdict(p)
        check("a Feature issue filed for a feature left out as Completed: not ok (C16)",
              code == 1 and any("left out" in x for x in res["problems"]))
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp, features=("ft-pick", "ft-remind")), paths(tmp)
        empty_tracker(p, [{"number": 30, "title": "Send a reminder", "type": "Feature", "labels": [],
                           "state": "closed", "state_reason": "completed", "body": full_body("ft-remind"),
                           "sub_issues": []}])
        flow(root, p)
        code, res = verdict(p)
        check("a Feature issue closed as completed by hand, left as it is and not under the epic: ok (C17)",
              code == 0 and 30 in res["checked"])
        edit(p, 30, state="open", state_reason="reopened")
        code, res = verdict(p)
        check("a Feature issue closed by hand that is open now: not ok",
              code == 1 and any("by hand" in x for x in res["problems"]))
        edit(p, 30, state="closed", state_reason="completed")
        rec = read_json(p["record"])
        write(p["record"], dict(rec, reopened=[{"issue": 30, "feature": "ft-remind", "closed_as": "completed"}]))
        code, res = verdict(p)
        check("a run that opened again an issue closed by hand: not ok",
              code == 1 and any("stays closed" in x for x in res["problems"]))
    return finish()


if __name__ == "__main__":
    sys.exit(main())
