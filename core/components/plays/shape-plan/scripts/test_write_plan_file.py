#!/usr/bin/env python3
"""test_write_plan_file.py — write_plan_file.py makes or updates the one plan file and keeps every other line (C1, C3, C6, C7).

    python3 test_write_plan_file.py
"""
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan_common as pc  # noqa: E402
from test_support import (check, empty_tracker, finish, flow, full_body, issue, make_model,  # noqa: E402
                          paths, read, read_json, run, set_slice, write)

HAND = """# Plan 340 — kept by hand.
# A note a person wrote.
intent: bi-340
title: Patients book their own appointments online
id: 340
status: Not Started
branch: plan/340/base
tree:
- issue: 5
  kind: chore
  title: Set up the clinic data
  status: Done
  # a comment inside a node
- issue: 10
  kind: epic
  title: 'Self-booking: the plan'
  status: In Progress
  children:
  - issue: 11
    kind: feature
    title: Pick a free slot
    status: Done
    represents: ft-pick
    needs:
    - 5
notes: kept as it is
"""


def plan_write(p):
    out = os.path.join(p["working"], "plan-write.json")
    code, _, _ = run("write_plan_file.py", "--plan-file", p["plan_file"], "--gather", p["gather"],
                     "--record", p["record"], "--out", out)
    return code, read_json(out) if os.path.isfile(out) else None


def main():
    print("write_plan_file.py")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        empty_tracker(p)
        codes = flow(root, p)
        res = read_json(os.path.join(p["working"], "plan-write.json"))
        text = read(p["plan_file"])
        plan = yaml.safe_load(text)
        rec = read_json(p["record"])
        epic = plan["tree"][0]
        check("no plan file: it is made, the business intent on its first lines, then id, status and direction",
              codes["plan"] == 0 and res["made"] and text.splitlines()[0] == "intent: bi-340"
              and text.splitlines()[1] == "title: Patients book their own appointments online"
              and plan["id"] == 340 and plan["status"] == "Not Started" and plan.get("direction") is None)
        check("the epic mark names the plan's one epic, and the slices list holds the slice at Not Started",
              plan["epic"] == rec["epic"] and plan["slices"] == [{"id": "sl-self-booking", "status": "Not Started"}])
        check("one epic node, with one feature node for each Feature issue",
              len(plan["tree"]) == 1 and epic["kind"] == "epic" and epic["issue"] == rec["epic"]
              and "represents" not in epic
              and [c["represents"] for c in epic["children"]] == ["ft-pick", "ft-remind", "ft-pay"]
              and all(c["kind"] == "feature" and c["issue"] and c["title"] for c in epic["children"]))
        before = read(p["plan_file"])
        flow(root, p)
        res = read_json(os.path.join(p["working"], "plan-write.json"))
        check("second run with no change: the file is byte for byte the same",
              res["changed"] is False and read(p["plan_file"]) == before)
        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind"])
        flow(root, p)
        plan = yaml.safe_load(read(p["plan_file"]))
        check("a moved-out feature's node is taken out of the tree",
              [c["represents"] for c in plan["tree"][0]["children"]] == ["ft-pick", "ft-remind"])
        spine = yaml.safe_load(read(os.path.join(root, "_spine.yaml")))
        spine["slices"].append({"id": "sl-cancel", "slug": "cancel-online", "feature_refs": ["ft-cancel", "ft-pick"],
                                "intents": ["bi-340"], "vertical": "the booking page"})
        write(os.path.join(root, "_spine.yaml"), spine)
        flow(root, p)
        plan = yaml.safe_load(read(p["plan_file"]))
        check("a second slice: the same plan and the same epic; the slice joins the list, its new feature the tree",
              len(os.listdir(p["plans"])) == 1 and len(plan["tree"]) == 1
              and [s["id"] for s in plan["slices"]] == ["sl-self-booking", "sl-cancel"]
              and [c["represents"] for c in plan["tree"][0]["children"]] == ["ft-pick", "ft-remind", "ft-cancel"])

    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp, features=("ft-pick", "ft-remind")), paths(tmp)
        write(p["plan_file"], HAND)
        empty_tracker(p, [issue(10, "Self-booking", "Epic", "x", subs=[5, 11]),
                          issue(5, "Set up the clinic data", None, "", state="closed"),
                          issue(11, "Pick a free slot", "Feature", full_body("ft-pick"))])
        write(p["plan_file"], HAND.replace("branch: plan/340/base", "branch: plan/340/base\nepic: 10"))
        hand = read(p["plan_file"])
        codes = flow(root, p)
        text = read(p["plan_file"])
        plan = yaml.safe_load(text)
        check("a hand-kept plan: every line a person wrote stays, in its order",
              codes["plan"] == 0 and pc.lines_kept(hand, text))
        kids = plan["tree"][1]["children"]
        check("the new feature node is added under the epic the mark names, after the old ones",
              [c["represents"] for c in kids] == ["ft-pick", "ft-remind"] and kids[1]["kind"] == "feature"
              and kids[0]["needs"] == [5] and plan["notes"] == "kept as it is")
        check("the slices list is added before the tree", plan["slices"] == [{"id": "sl-self-booking",
                                                                             "status": "Not Started"}])

    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp, features=("ft-pick",)), paths(tmp)
        hand = ("intent: bi-340\ntitle: x\nid: 340\nstatus: Not Started\nepic: 10\nslices: []\ntree:\n"
                "  - issue: 10\n    kind: epic\n    title: Self-booking\n    status: Not Started\n")
        write(p["plan_file"], hand)
        empty_tracker(p, [issue(10, "Self-booking", "Epic", "")])
        codes = flow(root, p)
        plan = yaml.safe_load(read(p["plan_file"]))
        check("an epic node with no children and an indented tree gains its children; an empty slices list fills",
              codes["plan"] == 0 and plan["tree"][0]["children"][0]["represents"] == "ft-pick"
              and plan["slices"] == [{"id": "sl-self-booking", "status": "Not Started"}])
        rec = read_json(p["record"])
        rec["held"] = {"ft-pick": 77}
        write(p["record"], rec)
        os.remove(p["plan_file"])
        code, _ = plan_write(p)
        kid = yaml.safe_load(read(p["plan_file"]))["tree"][0]["children"][0]
        check("a held Feature issue's node carries held_by: <epic>", code == 0 and kid["held_by"] == 77)
        write(p["record"], {"ok": False})
        code, _ = plan_write(p)
        check("a record with no map or slices: exit 2, the file is not written", code == 2)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
