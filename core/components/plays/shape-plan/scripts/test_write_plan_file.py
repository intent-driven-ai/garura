#!/usr/bin/env python3
"""test_write_plan_file.py — write_plan_file.py makes or updates the one plan file and keeps every other line (C1, C4, C6, C7).

    python3 test_write_plan_file.py
"""
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan_common as pc  # noqa: E402
from test_support import (check, empty_tracker, finish, flow, make_model, paths, read,  # noqa: E402
                          read_json, run, set_slice, write)

HAND = """# Plan 340 — kept by hand.
# A note a person wrote.
id: 340
title: Patients book their own appointments online
status: active
branch: plan/340/base
tree:
- issue: 5
  kind: chore
  title: Set up the clinic data
  status: done
  # a comment inside a node
- issue: 10
  kind: capability
  title: 'Self-booking: the slice'
  status: now
  represents: sl-self-booking
  children:
  - issue: 11
    kind: feature
    title: Pick a free slot
    status: done
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
        plan = yaml.safe_load(read(p["plan_file"]))
        epic = plan["tree"][0]
        check("no plan file: it is made with id, title, status and tree", codes["plan"] == 0 and res["made"]
              and plan["id"] == 340 and plan["status"] == "active"
              and plan["title"] == "Patients book their own appointments online")
        check("one epic node for the slice, with one story node for each feature",
              epic["kind"] == "epic" and epic["represents"] == "sl-self-booking"
              and [c["represents"] for c in epic["children"]] == ["ft-pick", "ft-remind", "ft-pay"]
              and all(c["kind"] == "story" and c["issue"] and c["title"] for c in epic["children"]))
        before = read(p["plan_file"])
        flow(root, p)
        res = read_json(os.path.join(p["working"], "plan-write.json"))
        check("second run with no change: the file is byte for byte the same",
              res["changed"] is False and read(p["plan_file"]) == before)
        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind"])
        flow(root, p)
        plan = yaml.safe_load(read(p["plan_file"]))
        check("a moved-out story's node is taken out of the tree",
              [c["represents"] for c in plan["tree"][0]["children"]] == ["ft-pick", "ft-remind"])
        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind", "ft-cancel"])
        spine = yaml.safe_load(read(os.path.join(root, "_spine.yaml")))
        spine["slices"].append({"id": "sl-cancel", "slug": "cancel-online", "feature_refs": ["ft-pay"],
                                "intents": ["bi-340"], "vertical": "the booking page"})
        write(os.path.join(root, "_spine.yaml"), spine)
        flow(root, p)
        plan = yaml.safe_load(read(p["plan_file"]))
        check("a second slice: the same plan file gains a second epic node",
              len(os.listdir(p["plans"])) == 1 and [n["represents"] for n in plan["tree"]] == ["sl-self-booking", "sl-cancel"]
              and [c["represents"] for c in plan["tree"][1]["children"]] == ["ft-pay"]
              and plan["tree"][0]["children"][-1]["represents"] == "ft-cancel")

    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp, features=("ft-pick", "ft-remind")), paths(tmp)
        write(p["plan_file"], HAND)
        empty_tracker(p, [{"number": 10, "title": "Self-booking", "type": "Feature", "body": "x"},
                          {"number": 11, "title": "Pick a free slot", "type": "Story",
                           "body": "## Scope of work\n## Context guidance\nRepresents: ft-pick\n"}])
        codes = flow(root, p)
        text = read(p["plan_file"])
        plan = yaml.safe_load(text)
        check("a hand-kept plan: every line a person wrote stays, in its order",
              codes["plan"] == 0 and pc.lines_kept(HAND, text))
        kids = plan["tree"][1]["children"]
        check("the new story node is added under the marked epic, after the old ones",
              [c["represents"] for c in kids] == ["ft-pick", "ft-remind"] and kids[1]["kind"] == "story"
              and kids[0]["needs"] == [5] and plan["notes"] == "kept as it is")

    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp, features=("ft-pick",)), paths(tmp)
        hand = "id: 340\ntitle: x\nstatus: active\ntree:\n  - issue: 10\n    kind: epic\n    represents: sl-self-booking\n"
        write(p["plan_file"], hand)
        empty_tracker(p, [{"number": 10, "title": "Self-booking", "type": "Feature", "body": ""}])
        codes = flow(root, p)
        plan = yaml.safe_load(read(p["plan_file"]))
        check("an epic node with no children and an indented tree gains its children",
              codes["plan"] == 0 and plan["tree"][0]["children"][0]["represents"] == "ft-pick"
              and read(p["plan_file"]).startswith(hand))
        write(p["record"], {"ok": False})
        code, _ = plan_write(p)
        check("a record that is not ok: exit 2, the file is not written", code == 2)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
