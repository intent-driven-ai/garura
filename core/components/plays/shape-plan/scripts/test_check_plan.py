#!/usr/bin/env python3
"""test_check_plan.py — check_plan.py: the business intent, the epic mark, the slices list, one feature node for each Feature issue, and the tree agrees with the map (D1; C1, C3, C6, C9, C16).

    python3 test_check_plan.py
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, empty_tracker, finish, flow, make_model, paths, read,  # noqa: E402
                          read_json, run, set_slice, write)


def verdict(p):
    out = os.path.join(p["working"], "plan-check.json")
    code, _, _ = run("check_plan.py", "--plan-file", p["plan_file"], "--gather", p["gather"],
                     "--record", p["record"], "--out", out)
    return code, read_json(out) if os.path.isfile(out) else None


def main():
    print("check_plan.py")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        empty_tracker(p)
        codes = flow(root, p)
        code, res = verdict(p)
        check("after a first plan: ok", codes["check_plan"] == 0 and code == 0 and res["ok"])
        good = read(p["plan_file"])
        rec = read_json(p["record"])

        lines = good.splitlines()
        fissue = rec["map"]["ft-pay"]
        at = lines.index(f"  - issue: {fissue}")
        write(p["plan_file"], "\n".join(lines[:at] + lines[at + 5:]) + "\n")
        code, res = verdict(p)
        check("a Feature issue with no feature node: not ok", code == 1 and any("ft-pay" in x for x in res["problems"]))

        write(p["plan_file"], good.replace("represents: ft-pay", "represents: ft-cancel"))
        code, res = verdict(p)
        check("a feature node for a feature in no slice of the plan: not ok",
              code == 1 and any("in no slice of the plan" in x for x in res["problems"]))

        write(p["plan_file"], good.replace("intent: bi-340\n", ""))
        code, res = verdict(p)
        check("no business intent at the top: not ok", code == 1 and any("business intent" in x for x in res["problems"]))

        write(p["plan_file"], good.replace(f"epic: {rec['epic']}\n", ""))
        code, res = verdict(p)
        check("no epic mark: not ok", code == 1 and any("epic mark" in x for x in res["problems"]))

        write(p["plan_file"], good.replace("  status: Not Started\ntree:", "  status: Later\ntree:"))
        code, res = verdict(p)
        check("a slice with a status a person cannot set: not ok",
              code == 1 and any("sl-self-booking" in x and "Later" in x for x in res["problems"]))

        write(p["plan_file"], good)
        write(p["record"], dict(rec, map=dict(rec["map"], **{"ft-pay": 999})))
        code, res = verdict(p)
        check("the map and the tree disagree: not ok", code == 1 and any("disagree" in x for x in res["problems"]))
        write(p["record"], rec)

        write(p["plan_file"], good + "# Fails if: nothing\n")
        code, res = verdict(p)
        check("the plan file holds the failure words: not ok", code == 1 and any("Fails if" in x for x in res["problems"]))
        write(p["plan_file"], good)

        write(p["record"], dict(rec, left_out=[{"feature": "ft-pay", "issue": None, "reason": "Completed",
                                                 "kind": "completed"}]))
        code, res = verdict(p)
        check("a Completed feature with a node in the plan: not ok (C16)",
              code == 1 and any("left out" in x for x in res["problems"]))
        write(p["record"], rec)

        write(p["record"], dict(rec, left_out=[{"feature": "ft-pay", "issue": None, "reason": "Dropped",
                                                 "kind": "dropped"}]))
        code, res = verdict(p)
        check("a Dropped feature with a node in the plan: not ok (C16)",
              code == 1 and any("left out" in x for x in res["problems"]))
        write(p["record"], rec)

        write(p["record"], dict(rec, closed_by_hand={"ft-pay": rec["map"]["ft-pay"]}))
        code, res = verdict(p)
        check("a feature closed by hand whose node is not at Done: not ok (C17)",
              code == 1 and any("not Done" in x for x in res["problems"]))
        write(p["record"], rec)

        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind", "ft-pay", "ft-wait"])
        flow(root, p)
        code, res = verdict(p)
        check("a skipped feature is listed, not failed",
              code == 0 and [s["feature"] for s in res["skipped"]] == ["ft-wait"] and "not ready" in res["skipped"][0]["reason"])
        os.remove(p["plan_file"])
        code, res = verdict(p)
        check("no plan file: not ok", code == 1 and res["ok"] is False)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
