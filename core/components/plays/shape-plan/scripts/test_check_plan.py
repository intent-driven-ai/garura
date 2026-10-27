#!/usr/bin/env python3
"""test_check_plan.py — check_plan.py: one story node for each ready feature, and the tree agrees with the map (D1; C1, C4, C6, C9).

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

        story = rec["maps"]["sl-self-booking"]["ft-pay"]
        lines = good.splitlines()
        at = lines.index(f"  - issue: {story}")
        write(p["plan_file"], "\n".join(lines[:at] + lines[at + 5:]) + "\n")
        code, res = verdict(p)
        check("a ready feature with no story node: not ok", code == 1 and any("ft-pay" in x for x in res["problems"]))

        write(p["plan_file"], good.replace("represents: ft-pay", "represents: ft-cancel"))
        code, res = verdict(p)
        check("a story node for a feature outside the slice: not ok",
              code == 1 and any("not a feature of the slice" in x for x in res["problems"]))

        write(p["plan_file"], good)
        bad = dict(rec, maps={"sl-self-booking": dict(rec["maps"]["sl-self-booking"], **{"ft-pay": 999})})
        write(p["record"], bad)
        code, res = verdict(p)
        check("the map and the tree disagree: not ok", code == 1 and any("disagree" in x for x in res["problems"]))
        write(p["record"], rec)

        write(p["plan_file"], good + "# Fails if: nothing\n")
        code, res = verdict(p)
        check("the plan file holds the failure words: not ok", code == 1 and any("Fails if" in x for x in res["problems"]))
        write(p["plan_file"], good)

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
