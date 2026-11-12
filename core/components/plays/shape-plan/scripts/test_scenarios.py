#!/usr/bin/env python3
"""test_scenarios.py — the scenarios S12 to S15 of /shape-plan, end to end with the file tracker.

    python3 test_scenarios.py

Each runs the play's scripts in order (gather, find, drafts, draft check, brief, approval,
tracker write, plan file, plan check, tracker check) on a small clinic model.
"""
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, empty_tracker, finish, flow, full_body, issue, make_model,  # noqa: E402
                          paths, read, read_json)


def tracker(p):
    return {i["number"]: i for i in read_json(p["tracker"])["issues"]}


def main():
    print("S12 — one plan with two slices")
    with tempfile.TemporaryDirectory() as tmp:
        extra = [{"id": "sl-cancel", "slug": "cancel-online", "feature_refs": ["ft-cancel", "ft-pick"],
                  "intents": ["bi-340"], "vertical": "the booking page"}]
        root, p = make_model(tmp, extra_slices=extra), paths(tmp)
        empty_tracker(p)
        codes = flow(root, p)
        rec, its = read_json(p["record"]), tracker(p)
        plan = yaml.safe_load(read(p["plan_file"]))
        check("every step reads ok", all(c == 0 for c in codes.values()))
        check("one epic, and one Feature issue for each pending feature of both slices, the shared one once",
              [c["kind"] for c in rec["created"]] == ["epic"] + ["feature"] * 4
              and sorted(c["represents"] for c in rec["created"][1:]) == ["ft-cancel", "ft-pay", "ft-pick", "ft-remind"]
              and sum(1 for i in its.values() if i["type"] == "Epic") == 1)
        check("the plan file: one epic mark, both slices at Not Started, one feature node each",
              plan["epic"] == rec["epic"]
              and plan["slices"] == [{"id": "sl-self-booking", "status": "Not Started"},
                                     {"id": "sl-cancel", "status": "Not Started"}]
              and len(plan["tree"]) == 1 and len(plan["tree"][0]["children"]) == 4)

    print("S13 — an old open story is found")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        empty_tracker(p, [issue(5, "An old epic", "Epic", "", subs=[6]),
                          issue(6, "Pick a free slot", "Story", "Represents: ft-pick\nOld words.")])
        codes = flow(root, p)
        items, rec, its = read_json(p["items"]), read_json(p["record"]), tracker(p)
        pick = next(f for f in items["features"] if f["feature"] == "ft-pick")
        brief = read(p["brief"])
        new = rec["features"]["ft-pick"]
        check("the find proposes make-and-move, with the story and the parent it leaves",
              pick["action"] == "make-and-move" and pick["move_stories"][0]["issue"] == 6
              and pick["move_stories"][0]["parent"]["number"] == 5)
        check("the brief names the move and that parent",
              "Story #6 \"Pick a free slot\": it leaves its parent #5 \"An old epic\"" in brief)
        check("after the yes, a Feature issue is filed and the story is inside it",
              its[new]["type"] == "Feature" and its[new]["sub_issues"] == [6] and its[5]["sub_issues"] == []
              and rec["moved"] == [{"issue": 6, "title": "Pick a free slot", "to": new, "left": 5}])
        check("the plan and tracker checks read ok", codes["check_plan"] == 0 and codes["check_tracker"] == 0)

    print("S14 — old finished work is found")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        empty_tracker(p, [issue(7, "Send a reminder", "Story", "", state="closed", reason="completed")])
        codes = flow(root, p)
        items, rec, its = read_json(p["items"]), read_json(p["record"]), tracker(p)
        remind = next(f for f in items["features"] if f["feature"] == "ft-remind")
        filed = next(c["issue"] for c in rec["created"] if c["represents"] == "ft-remind")
        plan_text = read(p["plan_file"])
        check("the find proposes make-closed", remind["action"] == "make-closed")
        check("the brief names it as left out", "ft-remind: a Feature issue is filed closed as completed"
              in read(p["brief"]).split("## Left out: built")[1])
        check("the tracker holds a Feature issue with its exact line, closed as completed, under no epic",
              its[filed]["type"] == "Feature" and its[filed]["state"] == "closed"
              and its[filed]["state_reason"] == "completed"
              and "Represents: ft-remind" in its[filed]["body"].splitlines()
              and not any(filed in i["sub_issues"] for i in its.values()))
        check("the feature is left out: no node, no map line",
              "ft-remind" not in plan_text and "ft-remind" not in rec["map"]
              and read_json(os.path.join(p["working"], "plan-check.json"))["left_out"][0]["feature"] == "ft-remind")
        check("the plan and tracker checks read ok", codes["check_plan"] == 0 and codes["check_tracker"] == 0)
        before = read(p["tracker"])
        flow(root, p)
        items = read_json(p["items"])
        check("a later run finds the closed Feature issue: built, nothing written",
              next(f for f in items["features"] if f["feature"] == "ft-remind")["action"] == "built"
              and read(p["tracker"]) == before)

    print("S15 — two Feature issues name one feature")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        empty_tracker(p, [issue(8, "Pick a free slot", "Feature", full_body("ft-pick")),
                          issue(9, "Pick a slot", "Feature", full_body("ft-pick"))])
        before = read(p["tracker"])
        codes = flow(root, p)
        items = read_json(p["items"])
        check("the find stops (exit 1) and names both issues",
              codes["find"] == 1 and items["ok"] is False
              and items["duplicates"] == [{"kind": "Feature issue", "represents": "ft-pick", "issues": [8, 9]}])
        check("no tracker write, no record and no plan file",
              codes["write"] == 2 and read(p["tracker"]) == before and not os.path.exists(p["record"])
              and not os.path.exists(p["plan_file"]))
    print("S16 — a feature not planned")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        empty_tracker(p, [issue(9, "Pay the fee", "Feature", full_body("ft-pay"), state="closed",
                                reason="not_planned")])
        before = tracker(p)[9]
        codes = flow(root, p)
        items, rec, its = read_json(p["items"]), read_json(p["record"]), tracker(p)
        pay = next(f for f in items["features"] if f["feature"] == "ft-pay")
        check("the run goes on: every step reads ok", all(c == 0 for c in codes.values()))
        check("the find lists the feature as not-planned, with its issue", items["ok"] is True
              and pay["action"] == "not-planned" and pay["issue"] == 9)
        check("the brief names it, with its issue number, under its own heading",
              "ft-pay: its Feature issue #9" in read(p["brief"]).split("## Not planned, left out")[1])
        check("its Feature issue stays as it is, and no new Feature issue is filed for it",
              {k: its[9].get(k) for k in before} == before and its[9].get("parent") is None and not any(c["represents"] == "ft-pay" for c in rec["created"]))
        check("the feature is left out: no node, no map line",
              "ft-pay" not in read(p["plan_file"]) and "ft-pay" not in rec["map"]
              and [x["feature"] for x in read_json(os.path.join(p["working"], "plan-check.json"))["left_out"]]
              == ["ft-pay"])
    return finish()


if __name__ == "__main__":
    sys.exit(main())
