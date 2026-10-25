#!/usr/bin/env python3
"""test_write_work_items.py — write_work_items.py writes after a yes only, finds before it makes, keeps a person's lines (C3–C6, C8, C12, C13).

    python3 test_write_work_items.py
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, empty_tracker, finish, flow, make_model, paths, read,  # noqa: E402
                          read_json, run, set_slice, write)


def issues(p):
    return {i["number"]: i for i in read_json(p["tracker"])["issues"]}


def main():
    print("write_work_items.py")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        empty_tracker(p)
        before = read(p["tracker"])
        codes = flow(root, p, decision="stop")
        check("no yes: exit 2, nothing in the tracker, no record",
              codes["write"] == 2 and read(p["tracker"]) == before and not os.path.exists(p["record"]))

        codes = flow(root, p)
        rec, its = read_json(p["record"]), issues(p)
        check("first plan: exit 0, one epic and three stories made", codes["write"] == 0
              and [c["kind"] for c in rec["created"]] == ["story", "story", "story", "epic"])
        epic = its[rec["epics"]["sl-self-booking"]]
        stories = [its[n] for n in rec["maps"]["sl-self-booking"].values()]
        check("the epic is type Feature with no label, and says what it represents",
              epic["type"] == "Feature" and epic["labels"] == [] and "Represents: sl-self-booking" in epic["body"])
        check("each story is type Story with no label, a sub-issue of the epic",
              all(s["type"] == "Story" and s["labels"] == [] for s in stories)
              and sorted(epic["sub_issues"]) == sorted(s["number"] for s in stories))
        check("each story has its two sections and its Represents line, and no failure words",
              all("## Scope of work" in s["body"] and "## Context guidance" in s["body"]
                  and f"Represents: {f}" in s["body"] and "fails if" not in s["body"].lower()
                  for f, s in zip(rec["maps"]["sl-self-booking"], stories)))
        check("the epic's map has one line for each feature",
              all(f"- {f} → #{n}" in epic["body"] for f, n in rec["maps"]["sl-self-booking"].items()))

        tracker_before = read(p["tracker"])
        flow(root, p)
        rec = read_json(p["record"])
        check("second run: nothing made, nothing changed", rec["created"] == [] and rec["updated"] == []
              and read(p["tracker"]) == tracker_before)

        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind", "ft-cancel"])
        flow(root, p)
        rec, its = read_json(p["record"]), issues(p)
        pay = next(c for c in rec["moved_out"] if c["feature"] == "ft-pay")["issue"]
        epic = its[rec["epics"]["sl-self-booking"]]
        check("a feature that left: its story is off the epic and the map, and still open",
              its[pay]["state"] == "open" and pay not in epic["sub_issues"] and "ft-pay" not in epic["body"])
        check("a feature that came in: one new story and one new map line",
              [c["represents"] for c in rec["created"]] == ["ft-cancel"] and "- ft-cancel → #" in epic["body"])

    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp, features=("ft-pick", "ft-remind")), paths(tmp)
        write(p["plan_file"], "id: 340\ntitle: x\nstatus: active\ntree:\n- issue: 10\n  kind: epic\n"
              "  title: Self-booking\n  represents: sl-self-booking\n  children:\n  - issue: 11\n"
              "    kind: story\n    represents: ft-pick\n  - issue: 12\n    kind: story\n    represents: ft-remind\n")
        person = "A person wrote this.\n\nAnd this line too.\n"
        empty_tracker(p, [
            {"number": 10, "title": "Self-booking", "type": "Epic", "labels": ["work-item"], "body": "The epic, by hand."},
            {"number": 11, "title": "Pick a free slot", "type": "Story", "body": person},
            {"number": 12, "title": "Send a reminder", "type": "Story", "body": person + "\n## Scope of work\n\n- kept\n"}])
        codes = flow(root, p)
        rec, its = read_json(p["record"]), issues(p)
        check("items made by hand: nothing new is made", codes["write"] == 0 and rec["created"] == [])
        check("each found story gains only its missing sections, and keeps every line a person wrote",
              its[11]["body"].startswith(person) and "## Scope of work" in its[11]["body"]
              and "## Context guidance" in its[11]["body"]
              and its[12]["body"].count("## Scope of work") == 1 and "- kept" in its[12]["body"]
              and its[12]["body"].startswith(person))
        check("the found epic gets type Feature, loses its label, keeps its text and gains its map",
              its[10]["type"] == "Feature" and its[10]["labels"] == [] and its[10]["body"].startswith("The epic, by hand.")
              and "- ft-pick → #11" in its[10]["body"] and sorted(its[10]["sub_issues"]) == [11, 12])
        check("the record lists each change", {u["issue"] for u in rec["updated"]} == {10, 11, 12}
              and all(u["lines_kept"] for u in rec["updated"]))
        code, _, _ = run("write_work_items.py", "--work-items", p["items"], "--drafts", os.path.join(tmp, "nope.json"),
                         "--approval", p["approval"], "--plan-id", "340", "--tracker-file", p["tracker"],
                         "--out", os.path.join(tmp, "r.json"))
        check("drafts that cannot be read: exit 2, nothing written", code == 2 and not os.path.exists(os.path.join(tmp, "r.json")))
    return finish()


if __name__ == "__main__":
    sys.exit(main())
