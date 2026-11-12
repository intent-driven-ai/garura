#!/usr/bin/env python3
"""test_write_work_items.py — write_work_items.py writes after a yes only, finds before it makes, keeps a person's lines (C3, C5, C6, C8, C13, C16).

    python3 test_write_work_items.py
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, empty_tracker, finish, flow, full_body, issue, make_model,  # noqa: E402
                          paths, read, read_json, run, set_slice, write, write_items)


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
        check("first plan: exit 0, one epic and three Feature issues filed, no Story (S1)", codes["write"] == 0
              and [c["kind"] for c in rec["created"]] == ["epic", "feature", "feature", "feature"]
              and not any(i["type"] == "Story" for i in its.values()))
        epic = its[rec["epic"]]
        feats = [its[n] for n in rec["map"].values()]
        check("the epic is type Epic with no label, and stands for the plan, not a slice",
              epic["type"] == "Epic" and epic["labels"] == [] and "Plan: 340" in epic["body"]
              and "Represents:" not in epic["body"])
        check("each Feature issue is type Feature with no label, a sub-issue of the epic",
              all(s["type"] == "Feature" and s["labels"] == [] for s in feats)
              and sorted(epic["sub_issues"]) == sorted(s["number"] for s in feats))
        check("each Feature issue has its exact Represents line and its two sections, and no failure words",
              all("## Scope of work" in s["body"] and "## Context guidance" in s["body"]
                  and f"Represents: {f}" in s["body"].splitlines() and "fails if" not in s["body"].lower()
                  for f, s in zip(rec["map"], feats)))
        check("each Feature issue says the two ICE pages it was written from, taken from gather.json",
              all("Written from: " in s["body"] and "feature.md" in s["body"] and "capability.md" in s["body"]
                  for s in feats))
        check("the epic's map has one line for each feature",
              all(f"- {f} → #{n}" in epic["body"] for f, n in rec["map"].items()))

        tracker_before = read(p["tracker"])
        flow(root, p)
        rec = read_json(p["record"])
        check("second run: the plan's epic and Feature issues are found; nothing made, nothing changed",
              rec["created"] == [] and rec["updated"] == [] and read(p["tracker"]) == tracker_before)

        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind", "ft-cancel"])
        flow(root, p)
        rec, its = read_json(p["record"]), issues(p)
        pay = next(c for c in rec["moved_out"] if c["feature"] == "ft-pay")["issue"]
        epic = its[rec["epic"]]
        check("a feature that left: its Feature issue is off the epic and the map, and still open",
              its[pay]["state"] == "open" and pay not in epic["sub_issues"] and "ft-pay" not in epic["body"])
        check("a feature that came in: one new Feature issue and one new map line",
              [c["represents"] for c in rec["created"]] == ["ft-cancel"] and "- ft-cancel → #" in epic["body"])

    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp, features=("ft-pick", "ft-remind", "ft-pay")), paths(tmp)
        person = "A person wrote this.\n\nAnd this line too.\n"
        empty_tracker(p, [
            issue(1, "Patients book online", None, "The business intent.", subs=[11]),
            issue(11, "Pick a free slot", "Feature", "Represents: ft-pick\n" + person, labels=["work-item"]),
            issue(40, "Another plan's epic", "Epic", "", subs=[12]),
            issue(12, "Send a reminder", "Feature", full_body("ft-remind")),
            issue(13, "Pay the fee", "Feature", full_body("ft-pay"), state="closed", reason="completed")])
        codes = flow(root, p)
        rec, its = read_json(p["record"]), issues(p)
        epic = its[rec["epic"]]
        check("found Feature issues: only the epic is new", codes["write"] == 0
              and [c["kind"] for c in rec["created"]] == ["epic"])
        check("a found Feature issue gains only its missing sections, keeps every line a person wrote, "
              "loses its label and moves under the epic",
              its[11]["body"].startswith("Represents: ft-pick\n" + person) and "## Scope of work" in its[11]["body"]
              and "## Context guidance" in its[11]["body"] and its[11]["labels"] == []
              and 11 in epic["sub_issues"] and its[1]["sub_issues"] == [])
        check("a held Feature issue stays under its epic, and the map names that epic",
              its[40]["sub_issues"] == [12] and 12 not in epic["sub_issues"]
              and "- ft-remind → #12 (under Epic #40)" in epic["body"] and rec["held"] == {"ft-remind": 40})
        check("a built feature is left out: no write to its issue, no map line (C16)",
              its[13]["body"] == full_body("ft-pay") and "ft-pay" not in epic["body"]
              and [x["feature"] for x in rec["left_out"]] == ["ft-pay"])
        check("the record lists each change", {u["issue"] for u in rec["updated"]} == {11, rec["epic"]}
              and all(u["lines_kept"] for u in rec["updated"]))
        check("the plan and tracker checks read ok", codes["check_plan"] == 0 and codes["check_tracker"] == 0)
        code, _, _ = run("write_work_items.py", "--work-items", p["items"], "--drafts", os.path.join(tmp, "nope.json"),
                         "--gather", p["gather"], "--approval", p["approval"], "--plan-id", "340",
                         "--tracker-file", p["tracker"], "--out", os.path.join(tmp, "r.json"))
        check("drafts that cannot be read: exit 2, nothing written", code == 2 and not os.path.exists(os.path.join(tmp, "r.json")))

    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        empty_tracker(p)
        flow(root, p)
        tracker_before = read(p["tracker"])
        for name, key in (("drafts.json", "drafts"), ("work-items.json", "items"), ("the brief", "brief")):
            keep = read(p[key])
            write(p[key], keep + " ")
            out = os.path.join(tmp, f"r-{key}.json")
            code = write_items(p, out)
            check(f"{name} changed after the yes: exit 2, nothing written",
                  code == 2 and not os.path.exists(out) and read(p["tracker"]) == tracker_before)
            write(p[key], keep)

    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        write(p["tracker"], {"issues": [], "fail_at_write": 3})
        codes = flow(root, p)
        rec = read_json(p["record"])
        its = issues(p)
        check("a write that fails part way: exit 1, the record keeps what was made and names the step",
              codes["write"] == 1 and rec["ok"] is False and "ft-remind" in rec["failed"]
              and [c["kind"] for c in rec["created"]] == ["epic", "feature"] and len(its) == 2)
        plan = read(p["plan_file"])
        check("the plan file still marks the issues the record lists",
              codes["plan"] == 0 and f"epic: {rec['epic']}" in plan and "represents: ft-pick" in plan)
        data = read_json(p["tracker"])
        data.pop("fail_at_write")
        write(p["tracker"], data)
        codes = flow(root, p)
        rec, its = read_json(p["record"]), issues(p)
        check("the next run uses the epic and Feature issue the first run made, and makes no copy",
              codes["write"] == 0 and [c["represents"] for c in rec["created"]] == ["ft-remind", "ft-pay"]
              and len(its) == 4 and sum(1 for i in its.values() if i["type"] == "Epic") == 1
              and codes["check_plan"] == 0 and codes["check_tracker"] == 0)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
