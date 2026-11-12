#!/usr/bin/env python3
"""test_find_work_items.py — find_work_items.py finds before it makes, by the plan file's marks (C3, C4, C9, C12).

    python3 test_find_work_items.py
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, empty_tracker, finish, flow, gather, make_model, paths,  # noqa: E402
                          read_json, run, set_issue, set_slice, write)

FULL = "Represents: ft-pick\n\n## Scope of work\n\nGoals:\n- x\n\n## Context guidance\n\n- Read: y\n"
PLAN = """# A plan kept by hand.
id: 340
title: Patients book their own appointments online
status: Not Started
tree:
- issue: 10
  kind: epic
  title: Self-booking
  status: now
  represents: sl-self-booking
  children:
  - issue: 11
    kind: story
    title: Pick a free slot
    status: next
    represents: ft-pick
  - issue: 12
    kind: story
    title: Send a reminder
    status: next
    represents: ft-remind
  - issue: 13
    kind: story
    title: Cancel online
    status: next
    represents: ft-cancel
  - issue: 14
    kind: story
    title: Pay the fee
    status: next
- issue: 20
  kind: epic
  title: Pay the fee
  status: next
"""


def find(p):
    return run("find_work_items.py", "--gather", p["gather"], "--plan-file", p["plan_file"],
               "--tracker-file", p["tracker"], "--out", p["items"])


def main():
    print("find_work_items.py")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        gather(root, p)
        empty_tracker(p, [{"number": 20, "title": "Pay the fee", "type": "Feature", "labels": [],
                           "state": "open", "body": ""}])
        code, out, _ = find(p)
        items = read_json(p["items"])
        sl = items["slices"][0]
        check("no plan file: the epic and every story are make", code == 0 and items["plan_file_exists"] is False
              and sl["epic"]["action"] == "make" and [s["action"] for s in sl["stories"]] == ["make"] * 3)

        write(p["plan_file"], PLAN)
        empty_tracker(p, [
            {"number": 10, "title": "Self-booking", "type": "Epic", "labels": ["work-item"], "state": "open",
             "body": "Hand-made epic.", "sub_issues": [11, 13]},
            {"number": 11, "title": "Pick a free slot", "type": "Story", "labels": [], "state": "open", "body": FULL},
            {"number": 12, "title": "Send a reminder", "type": None, "labels": [], "state": "open",
             "body": "Written by a person.\n## Scope of work\n- old\n"},
            {"number": 13, "title": "Cancel online", "type": "Story", "labels": [], "state": "open", "body": ""},
            {"number": 20, "title": "Pay the fee", "type": "Feature", "labels": [], "state": "open", "body": ""}])
        code, out, _ = find(p)
        sl = read_json(p["items"])["slices"][0]
        st = {s["feature"]: s for s in sl["stories"]}
        check("a marked epic is used, with its type and labels", code == 0 and sl["epic"]["action"] == "use"
              and sl["epic"]["issue"] == 10 and sl["epic"]["type"] == "Epic" and sl["epic"]["labels"] == ["work-item"])
        check("a marked story with both sections is used", st["ft-pick"]["action"] == "use" and st["ft-pick"]["issue"] == 11
              and st["ft-pick"]["attached"] is True and st["ft-pick"]["represents_line"] is True)
        check("a marked story missing a section is add-sections, naming it",
              st["ft-remind"]["action"] == "add-sections" and st["ft-remind"]["missing"] == ["Context guidance"]
              and st["ft-remind"]["attached"] is False)
        check("a feature with no marked story is make, even when a node has its title",
              st["ft-pay"]["action"] == "make" and st["ft-pay"]["issue"] is None)
        check("a marked story whose feature left the slice is moved out",
              sl["move_out"] == [{"issue": 13, "feature": "ft-cancel", "title": "Cancel online"}])
        check("an epic that holds only its stories and a moved-out story has no misplaced work",
              read_json(p["items"])["misplaced"] == [])

        data = read_json(p["tracker"])
        for it in data["issues"]:
            if it["number"] == 10:
                it["sub_issues"] = [11, 13, 40]
        data["issues"].append({"number": 40, "title": "Old chore", "type": "Chore", "labels": [],
                               "state": "closed", "body": ""})
        write(p["tracker"], data)
        code, _, _ = find(p)
        items = read_json(p["items"])
        check("work under the epic that is not its slice's (#879): exit 1, named with its title",
              code == 1 and items["ok"] is False
              and items["misplaced"] == [{"slice": "sl-self-booking", "epic": 10, "issue": 40, "title": "Old chore"}])
        for it in data["issues"]:
            if it["number"] == 10:
                it["sub_issues"] = [11, 13]
        write(p["tracker"], data)

        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind", "ft-wait"])
        gather(root, p)
        find(p)
        st = {s["feature"]: s for s in read_json(p["items"])["slices"][0]["stories"]}
        check("a feature whose ICE is not ready is skip, with its reason",
              st["ft-wait"]["action"] == "skip" and "not ready" in st["ft-wait"]["reason"])

        write(p["plan_file"], PLAN.replace("- issue: 20\n", "- issue: 20\n  represents: sl-self-booking\n"))
        code, out, _ = find(p)
        items = read_json(p["items"])
        check("two epic nodes for one slice: exit 1, the first is kept",
              code == 1 and items["duplicates"][0]["kept"] == 10 and items["duplicates"][0]["copies"] == [20])

        write(p["plan_file"], PLAN.replace("issue: 12", "issue: 99"))
        code, out, _ = find(p)
        check("a marked issue the tracker does not have: exit 1, named",
              code == 1 and any("#99" in pr for pr in read_json(p["items"])["problems"]))

        code, _, _ = run("find_work_items.py", "--gather", os.path.join(tmp, "none.json"), "--plan-file",
                         p["plan_file"], "--tracker-file", p["tracker"], "--out", p["items"])
        check("a missing gather.json: exit 2", code == 2)

    # The story the model names (C3, F14, #1025): no plan file, so the model's `issue` is the link.
    bi = {"number": 1, "title": "Patients book online", "type": None, "labels": [], "state": "open",
          "body": "", "sub_issues": [50]}

    def story(n, body=FULL, state="open", type_="Story"):
        return {"number": n, "title": f"Story {n}", "type": type_, "labels": [], "state": state, "body": body}

    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        set_issue(root, {"ft-pick": 50, "ft-remind": 51})
        gather(root, p)
        empty_tracker(p, [bi, story(50), story(51, body="Written by a person.\n")])
        code, _, _ = find(p)
        items = read_json(p["items"])
        st = {s["feature"]: s for s in items["slices"][0]["stories"]}
        check("no plan file: a feature whose model entry names an open Story uses it, never make",
              code == 0 and st["ft-pick"]["action"] == "use" and st["ft-pick"]["issue"] == 50
              and st["ft-pick"]["source"] == "model" and st["ft-pick"]["attached"] is False)
        check("a model-named story missing its sections is add-sections",
              st["ft-remind"]["action"] == "add-sections" and st["ft-remind"]["issue"] == 51
              and st["ft-remind"]["missing"] == ["Scope of work", "Context guidance"])
        check("a feature the model names no story for is still make",
              st["ft-pay"]["action"] == "make" and st["ft-pay"]["source"] is None)

        for label, issues, words in (
                ("closed", [bi, story(50, state="closed"), story(51)], "#50 is closed"),
                ("not a Story", [bi, story(50, type_="Bug"), story(51)], "#50 is of type Bug"),
                ("not in the tracker", [bi, story(51)], "the tracker has no such issue")):
            empty_tracker(p, issues)
            code, _, _ = find(p)
            items = read_json(p["items"])
            check(f"a model-named issue that is {label}: exit 1, named, never used",
                  code == 1 and items["ok"] is False and any(words in pr for pr in items["problems"])
                  and {s["feature"]: s for s in items["slices"][0]["stories"]}["ft-pick"]["issue"] is None)

        set_issue(root, {"ft-pick": 50, "ft-remind": 50})
        gather(root, p)
        empty_tracker(p, [bi, story(50)])
        code, _, _ = find(p)
        items = read_json(p["items"])
        check("one issue the model names for two features: exit 1, named, used for neither",
              code == 1 and any("more than one feature" in pr for pr in items["problems"])
              and all(s["issue"] is None for s in items["slices"][0]["stories"]))

    # S10 — the whole flow: the story filed before the plan is used and moved under the epic.
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        set_issue(root, {"ft-pick": 50})
        empty_tracker(p, [bi, story(50)])
        codes = flow(root, p)
        rec = read_json(p["record"])
        data = {i["number"]: i for i in read_json(p["tracker"])["issues"]}
        epic = rec["epics"]["sl-self-booking"]
        check("S10: the run goes through and the plan check reads ok",
              codes.get("write") == 0 and codes.get("check_plan") == 0 and codes.get("check_tracker") == 0)
        check("S10: no new story is made for the feature the model names; the others are made",
              sorted(c["represents"] for c in rec["created"] if c["kind"] == "story") == ["ft-pay", "ft-remind"])
        check("S10: the epic's map names the model's story, and the story left its old parent",
              rec["stories"]["ft-pick"] == 50 and 50 in data[epic]["sub_issues"] and 50 not in data[1]["sub_issues"])
        check("S10: the brief says the story is the one the model names",
              "the story the model names for this feature" in open(p["brief"]).read())
    return finish()


if __name__ == "__main__":
    sys.exit(main())
