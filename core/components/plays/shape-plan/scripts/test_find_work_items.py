#!/usr/bin/env python3
"""test_find_work_items.py — find_work_items.py finds the plan's epic and each feature's work before it makes any (C3, C9, C13, C16, C17, C18).

    python3 test_find_work_items.py
"""
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, empty_tracker, finish, full_body, gather, issue,  # noqa: E402
                          make_model, paths, read, read_json, run, set_slice, write)

PLAN = """intent: bi-340
title: Patients book their own appointments online
id: 340
status: Not Started
epic: 10
slices:
- id: sl-self-booking
  status: Not Started
tree:
- issue: 10
  kind: epic
  title: Self-booking
  status: In Progress
  children:
  - issue: 11
    kind: feature
    title: Pick a free slot
    status: Not Started
    represents: ft-pick
  - issue: 13
    kind: feature
    title: Cancel online
    status: Not Started
    represents: ft-cancel
  - issue: 15
    kind: chore
    title: Clean the old slots
    status: Not Started
"""


def find(p):
    code, out, _ = run("find_work_items.py", "--gather", p["gather"], "--plan-file", p["plan_file"],
                       "--tracker-file", p["tracker"], "--out", p["items"])
    items = read_json(p["items"]) if os.path.isfile(p["items"]) else None
    return code, items, {f["feature"]: f for f in (items or {}).get("features") or []}


def main():
    print("find_work_items.py")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        spine = yaml.safe_load(read(os.path.join(root, "_spine.yaml")))
        spine["features"][0]["issue"] = 30  # an old issue number the model must not be read for
        write(os.path.join(root, "_spine.yaml"), spine)
        gather(root, p)
        empty_tracker(p, [issue(30, "Some other work", "Story", "Unrelated.")])
        code, items, fs = find(p)
        check("no plan file: one epic to make, and each feature make (S1)",
              code == 0 and items["plan_file_exists"] is False and items["epic"]["action"] == "make"
              and [f["action"] for f in items["features"]] == ["make"] * 3)
        check("an issue number in the model is never read (ADR 069)",
              fs["ft-pick"]["issue"] is None and fs["ft-pick"]["action"] == "make")

        empty_tracker(p, [
            issue(1, "Patients book online", None, "The business intent.", subs=[21]),
            issue(20, "Pick a free slot", "Feature", "No line here."),
            issue(21, "Pick a free slot", "Feature", full_body("ft-pick")),
            issue(22, "Send a reminder", "Feature", "Represents: ft-remind\n\n## Scope of work\n- old\n",
                  labels=["work-item"]),
            issue(23, "Pay the fee", "Feature", "Old group, no line.")])
        code, items, fs = find(p)
        check("a Feature issue is found by its exact Represents line, never by its title (C3)",
              fs["ft-pick"]["action"] == "use" and fs["ft-pick"]["issue"] == 21
              and fs["ft-pick"]["source"] == "tracker")
        check("a Feature issue under a parent that is not an epic is used, and names the parent it leaves",
              fs["ft-pick"]["attached"] is False and fs["ft-pick"]["parent"]["number"] == 1)
        check("a found Feature issue missing a section is add-sections, naming it, with its labels",
              fs["ft-remind"]["action"] == "add-sections" and fs["ft-remind"]["missing"] == ["Context guidance"]
              and fs["ft-remind"]["labels"] == ["work-item"])
        check("an old issue of type Feature with no exact line is not a match: a new one is filed",
              fs["ft-pay"]["action"] == "make" and fs["ft-pay"]["issue"] is None and code == 0
              and "old" not in fs["ft-pay"] and "move_stories" not in fs["ft-pay"])

        empty_tracker(p, [
            issue(40, "Another plan's epic", "Epic", "Plan: 99", subs=[41]),
            issue(41, "Pick a free slot", "Feature", full_body("ft-pick")),
            issue(42, "Send a reminder", "Feature", full_body("ft-remind"), state="closed", reason="completed")])
        code, items, fs = find(p)
        check("a Feature issue under another plan's epic is held_by that epic, never moved (C3)",
              fs["ft-pick"]["action"] == "held" and fs["ft-pick"]["held_by"] == 40 and code == 0)
        check("a Feature issue closed as completed while the feature is not Completed is closed-by-hand: "
              "not opened again, the tracker does not say built (C16, C17)",
              fs["ft-remind"]["action"] == "closed-by-hand" and fs["ft-remind"]["issue"] == 42
              and fs["ft-remind"]["closed_as"] == "completed")
        check("a feature closed by hand keeps its state: no state change, named as kept (C17, C18)",
              "ft-remind" not in [c["feature"] for c in items["state_changes"]]
              and {"feature": "ft-remind", "state": "Unplanned"} in items["kept_states"])

        empty_tracker(p, [issue(42, "Send a reminder", "Feature", full_body("ft-remind"), state="closed",
                                reason="not_planned")])
        code, items, fs = find(p)
        check("a Feature issue closed as not planned opens again, and the run goes on (C17, S16)",
              code == 0 and items["ok"] is True and fs["ft-remind"]["action"] == "reopen"
              and fs["ft-remind"]["issue"] == 42 and fs["ft-remind"]["closed_as"] == "not planned"
              and items["problems"] == [])
        check("a feature taken in through a reopened issue is set to Planned (C18)",
              {"feature": "ft-remind", "from": "Unplanned", "to": "Planned", "had_no_state": False}
              in items["state_changes"])

        empty_tracker(p, [issue(50, "Pick a free slot", "Feature", full_body("ft-pick")),
                          issue(51, "Pick a slot", "Feature", "Text.\nRepresents: ft-pick\n")])
        code, items, fs = find(p)
        check("two Feature issues name one feature: exit 1, and both are named (S15)",
              code == 1 and items["ok"] is False
              and items["duplicates"] == [{"kind": "Feature issue", "represents": "ft-pick", "issues": [50, 51]}]
              and any("#50" in pr and "#51" in pr for pr in items["problems"]))

        set_slice(root, "sl-self-booking", ["ft-pick", "ft-wait"])
        gather(root, p)
        empty_tracker(p, [issue(80, "Join the waiting list", "Feature", full_body("ft-wait"), state="closed",
                                reason="not_planned")])
        code, items, fs = find(p)
        check("a feature whose ICE is not ready is skip: its closed issue is not opened again, its state "
              "does not change (C9)",
              fs["ft-wait"]["action"] == "skip" and "not ready" in fs["ft-wait"]["reason"]
              and fs["ft-wait"]["issue"] == 80
              and "ft-wait" not in [c["feature"] for c in items["state_changes"]])
    with tempfile.TemporaryDirectory() as tmp:
        root = make_model(tmp, features=("ft-pick", "ft-remind", "ft-pay", "ft-cancel", "ft-wait"),
                          states={"ft-pick": "Completed", "ft-remind": "Dropped", "ft-pay": "Planned",
                                  "ft-cancel": None})
        p = paths(tmp)
        spine = yaml.safe_load(read(os.path.join(root, "_spine.yaml")))
        next(f for f in spine["features"] if f["id"] == "ft-wait")["status"] = "proposed"
        write(os.path.join(root, "_spine.yaml"), spine)
        gather(root, p)
        empty_tracker(p, [issue(90, "Pick a free slot", "Feature", full_body("ft-pick")),
                          issue(91, "Send a reminder", "Feature", full_body("ft-remind"), state="closed",
                                reason="not_planned")])
        code, items, fs = find(p)
        check("a Completed or Dropped feature is left out, read from the model, with no tracker search (C16, S17)",
              code == 0 and fs["ft-pick"]["action"] == "completed" and fs["ft-pick"]["issue"] is None
              and fs["ft-remind"]["action"] == "dropped" and fs["ft-remind"]["issue"] is None)
        check("only an Unplanned feature taken in moves to Planned; a Planned one keeps its state (C18, S18)",
              [c["feature"] for c in items["state_changes"]] == ["ft-cancel"]
              and items["kept_states"] == [{"feature": "ft-pay", "state": "Planned"}])
        check("a feature with no status, or a value outside the five, is Unplanned and named (C16, S19)",
              items["no_state"] == [{"feature": "ft-cancel", "status": None},
                                    {"feature": "ft-wait", "status": "proposed"}]
              and items["state_changes"][0]["had_no_state"] is True)
    with tempfile.TemporaryDirectory() as tmp:
        extra = [{"id": "sl-cancel", "slug": "cancel-online", "feature_refs": ["ft-cancel", "ft-pick"],
                  "intents": ["bi-340"], "vertical": "the booking page"}]
        root, p = make_model(tmp, extra_slices=extra), paths(tmp)
        gather(root, p)
        empty_tracker(p)
        code, items, fs = find(p)
        check("two slices: each feature once, a shared feature with both slices (S12)",
              code == 0 and [f["feature"] for f in items["features"]] == ["ft-pick", "ft-remind", "ft-pay", "ft-cancel"]
              and fs["ft-pick"]["slices"] == ["sl-self-booking", "sl-cancel"]
              and [s["id"] for s in items["slices"]] == ["sl-self-booking", "sl-cancel"])
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp, features=("ft-pick", "ft-remind")), paths(tmp)
        gather(root, p)
        write(p["plan_file"], PLAN)
        empty_tracker(p, [
            issue(10, "Self-booking", "Epic", "Plan: 340", subs=[11, 13, 15]),
            issue(11, "Pick a free slot", "Feature", full_body("ft-pick")),
            issue(13, "Cancel online", "Feature", full_body("ft-cancel")),
            issue(15, "Clean the old slots", None, "")])
        code, items, fs = find(p)
        check("the epic is found by the plan file's epic mark (C3)",
              code == 0 and items["epic"]["action"] == "use" and items["epic"]["issue"] == 10)
        check("a feature node's represents mark finds its Feature issue, already under the epic",
              fs["ft-pick"]["source"] == "plan file" and fs["ft-pick"]["action"] == "use"
              and fs["ft-pick"]["attached"] is True)
        check("a feature node whose feature is in no slice is moved out",
              items["move_out"] == [{"issue": 13, "feature": "ft-cancel", "title": "Cancel online"}])
        check("an item the plan file places under the epic is kept, not misplaced",
              items["misplaced"] == [] and items["epic"]["kept_subs"] == [15])
        data = read_json(p["tracker"])
        data["issues"][0]["sub_issues"] = [11, 13, 15, 40]
        data["issues"].append(issue(40, "Old chore", "Chore", "", state="closed"))
        write(p["tracker"], data)
        code, items, _ = find(p)
        check("work under the epic that the plan does not place: exit 1, named with its title (S8)",
              code == 1 and items["misplaced"] == [{"epic": 10, "issue": 40, "title": "Old chore"}])
    return finish()


if __name__ == "__main__":
    sys.exit(main())
