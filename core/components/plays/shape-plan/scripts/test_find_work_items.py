#!/usr/bin/env python3
"""test_find_work_items.py — find_work_items.py finds the plan's epic and each feature's work before it makes any (C3, C9, C13, C15, C16).

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
              fs["ft-pick"]["issue"] is None and fs["ft-pick"]["move_stories"] == [])

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
        check("an old issue of type Feature with no exact line is not a match: it is named, and a new one is filed",
              fs["ft-pay"]["action"] == "make" and fs["ft-pay"]["issue"] is None
              and [g["issue"] for g in fs["ft-pay"]["old"]["old_groups"]] == [23] and code == 0)

        empty_tracker(p, [
            issue(40, "Another plan's epic", "Epic", "Plan: 99", subs=[41]),
            issue(41, "Pick a free slot", "Feature", full_body("ft-pick")),
            issue(42, "Send a reminder", "Feature", full_body("ft-remind"), state="closed", reason="completed")])
        code, items, fs = find(p)
        check("a Feature issue under another plan's epic is held_by that epic, never moved (C3)",
              fs["ft-pick"]["action"] == "held" and fs["ft-pick"]["held_by"] == 40 and code == 0)
        check("a Feature issue closed as completed is built and left out (C16)",
              fs["ft-remind"]["action"] == "built" and fs["ft-remind"]["issue"] == 42
              and "closed as completed" in fs["ft-remind"]["reason"])

        empty_tracker(p, [issue(42, "Send a reminder", "Feature", full_body("ft-remind"), state="closed",
                                reason="not_planned")])
        code, items, fs = find(p)
        check("a Feature issue closed as not planned does not stop the run: the feature is left out (C16, S16)",
              code == 0 and items["ok"] is True and fs["ft-remind"]["action"] == "not-planned"
              and fs["ft-remind"]["issue"] == 42 and "not planned" in fs["ft-remind"]["reason"]
              and items["problems"] == [] and fs["ft-remind"]["move_stories"] == [])

        empty_tracker(p, [issue(50, "Pick a free slot", "Feature", full_body("ft-pick")),
                          issue(51, "Pick a slot", "Feature", "Text.\nRepresents: ft-pick\n")])
        code, items, fs = find(p)
        check("two Feature issues name one feature: exit 1, and both are named (S15)",
              code == 1 and items["ok"] is False
              and items["duplicates"] == [{"kind": "Feature issue", "represents": "ft-pick", "issues": [50, 51]}]
              and any("#50" in pr and "#51" in pr for pr in items["problems"]))

        empty_tracker(p, [
            issue(60, "Old plan epic", "Epic", "", subs=[61]),
            issue(61, "Pick a free slot", "Story", "Represents: ft-pick\nOld story."),
            issue(62, "Send a reminder", "Story", "", state="closed", reason="completed"),
            issue(63, "Send a reminder by text", "Story", "", state="closed", reason="not_planned")])
        code, items, fs = find(p)
        check("an old open story is found: make-and-move, with the parent it leaves (S13)",
              code == 0 and fs["ft-pick"]["action"] == "make-and-move"
              and [s["issue"] for s in fs["ft-pick"]["move_stories"]] == [61]
              and fs["ft-pick"]["move_stories"][0]["parent"]["number"] == 60)
        check("only finished old work is found: make-closed, left out (S14)",
              fs["ft-remind"]["action"] == "make-closed" and "built" in fs["ft-remind"]["reason"]
              and [s["issue"] for s in fs["ft-remind"]["old"]["done_stories"]] == [62])
        check("nothing old is found: make", fs["ft-pay"]["action"] == "make")

        empty_tracker(p, [issue(70, "Pick a free slot and send a reminder", "Story", "ft-pick, ft-remind")])
        code, items, _ = find(p)
        check("one old story that two features claim stops the run, named (C15)",
              code == 1 and any("#70" in pr for pr in items["problems"]))

        set_slice(root, "sl-self-booking", ["ft-pick", "ft-wait"])
        gather(root, p)
        empty_tracker(p, [issue(80, "Join the waiting list", "Story", "Represents: ft-wait")])
        code, items, fs = find(p)
        check("a feature whose ICE is not ready is skip, and no old work is searched or moved for it (C9)",
              fs["ft-wait"]["action"] == "skip" and "not ready" in fs["ft-wait"]["reason"]
              and fs["ft-wait"]["move_stories"] == [])
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
