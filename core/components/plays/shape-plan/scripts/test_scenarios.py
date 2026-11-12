#!/usr/bin/env python3
"""test_scenarios.py — the scenarios S12 and S15 to S19 of /shape-plan, end to end with the file tracker.

    python3 test_scenarios.py

Each runs the play's scripts in order (gather, find, drafts, draft check, brief, approval,
tracker write, plan file, plan check, tracker check, the Planned request, the model write the
link-model-part skill makes, and the state check) on a small clinic model.
"""
import json
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


def spine_status(root):
    spine = yaml.safe_load(read(os.path.join(root, "_spine.yaml")))
    return {f["id"]: f.get("status") for f in spine["features"]}


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
    print("S16 — a closed Feature issue is opened again")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        empty_tracker(p, [issue(9, "Pay the fee", "Feature", full_body("ft-pay"), state="closed",
                                reason="not_planned")])
        codes = flow(root, p)
        items, rec, its = read_json(p["items"]), read_json(p["record"]), tracker(p)
        pay = next(f for f in items["features"] if f["feature"] == "ft-pay")
        check("the run goes on: every step reads ok", all(c == 0 for c in codes.values()))
        check("the find lists the feature as reopen, with its issue",
              items["ok"] is True and pay["action"] == "reopen" and pay["issue"] == 9)
        check("the brief names it, with its issue number, under Opened again",
              "ft-pay: Feature issue #9" in read(p["brief"]).split("## Opened again")[1].split("##")[0])
        check("after the yes the same issue is open, under the epic, and no second one is filed",
              its[9]["state"] == "open" and 9 in its[rec["epic"]]["sub_issues"]
              and rec["reopened"][0]["issue"] == 9
              and not any(c["represents"] == "ft-pay" for c in rec["created"]))
        check("the feature is in the plan and now Planned",
              rec["map"]["ft-pay"] == 9 and spine_status(root)["ft-pay"] == "Planned")

    print("S17 — Completed and Dropped features are left out")
    with tempfile.TemporaryDirectory() as tmp:
        root = make_model(tmp, states={"ft-remind": "Completed", "ft-pay": "Dropped"})
        p = paths(tmp)
        empty_tracker(p, [issue(30, "Send a reminder", "Feature", full_body("ft-remind"))])
        before = read(p["tracker"])
        codes = flow(root, p)
        items, rec = read_json(p["items"]), read_json(p["record"])
        fs = {f["feature"]: f for f in items["features"]}
        brief = read(p["brief"])
        check("every step reads ok", all(c == 0 for c in codes.values()))
        check("both are left out from the model, with no tracker search (no issue found)",
              fs["ft-remind"]["action"] == "completed" and fs["ft-remind"]["issue"] is None
              and fs["ft-pay"]["action"] == "dropped" and fs["ft-pay"]["issue"] is None)
        check("the brief names each under its heading",
              "ft-remind" in brief.split("## Built, left out")[1].split("##")[0]
              and "ft-pay" in brief.split("## Dropped, left out")[1].split("##")[0])
        check("no node, no map line, and the open issue #30 is not touched",
              "ft-remind" not in read(p["plan_file"]) and "ft-pay" not in read(p["plan_file"])
              and set(rec["map"]) == {"ft-pick"}
              and all(tracker(p)[30].get(k) == v for k, v in json.loads(before)["issues"][0].items()))
        check("their states are as they were; the plan check names both as left out",
              spine_status(root)["ft-remind"] == "Completed" and spine_status(root)["ft-pay"] == "Dropped"
              and sorted(x["feature"] for x in read_json(os.path.join(p["working"], "plan-check.json"))["left_out"])
              == ["ft-pay", "ft-remind"])

    print("S18 — the plan sets Planned")
    with tempfile.TemporaryDirectory() as tmp:
        root = make_model(tmp, states={"ft-remind": "Planned", "ft-pay": "In progress"})
        p = paths(tmp)
        empty_tracker(p)
        codes = flow(root, p)
        items, request = read_json(p["items"]), read_json(p["request"])
        part = read(p["brief"]).split("## State changes in the product model")[1].split("## The plan file")[0]
        check("every step reads ok", all(c == 0 for c in codes.values()))
        check("only the Unplanned feature changes; the brief lists it, and keeps the other two",
              [c["feature"] for c in items["state_changes"]] == ["ft-pick"]
              and "ft-pick: Unplanned → Planned." in part and "ft-remind: stays Planned." in part
              and "ft-pay: stays In progress." in part)
        check("the request asks link-model-part for that one feature, mode update, status Planned",
              request == {"by": "shape-plan (#340)", "parts": [{"id": "ft-pick", "kind": "feature",
                                                               "mode": "update", "status": "Planned"}]})
        check("after the write: Planned, the others kept, and the state check reads ok",
              spine_status(root) == {"ft-pick": "Planned", "ft-remind": "Planned", "ft-pay": "In progress",
                                     "ft-cancel": "Unplanned", "ft-wait": "Unplanned"}
              and read_json(p["state_check"])["ok"] is True)

    print("S19 — a feature with no state")
    with tempfile.TemporaryDirectory() as tmp:
        root = make_model(tmp, states={"ft-remind": None})
        p = paths(tmp)
        empty_tracker(p)
        codes = flow(root, p)
        g = {f["id"]: f for f in read_json(p["gather"])["slices"][0]["features"]}
        rec = read_json(p["record"])
        check("every step reads ok", all(c == 0 for c in codes.values()))
        check("it reads Unplanned, with had_no_state",
              g["ft-remind"]["state"] == "Unplanned" and g["ft-remind"]["had_no_state"] is True)
        check("the brief names it under Had no state",
              "ft-remind: its spine entry has no status" in read(p["brief"]).split("## Had no state")[1])
        check("it is in the plan, and after the write it reads Planned",
              "ft-remind" in rec["map"] and spine_status(root)["ft-remind"] == "Planned"
              and read_json(p["state_check"])["ok"] is True)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
