#!/usr/bin/env python3
"""test_check_drafts.py — check_drafts.py keeps failure and recovery text out of the epic and stories (C5, C6, C9).

    python3 test_check_drafts.py
"""
import copy
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, finish, gather, make_drafts, make_model, paths, read_json,  # noqa: E402
                          run, set_slice, story_draft, write)


def verdict(p, drafts):
    write(p["drafts"], drafts)
    out = os.path.join(p["working"], "drafts-check.json")
    code, _, _ = run("check_drafts.py", "--drafts", p["drafts"], "--gather", p["gather"], "--out", out)
    return code, read_json(out) if os.path.isfile(out) else None


def main():
    print("check_drafts.py")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        gather(root, p)
        good = make_drafts(p)
        code, res = verdict(p, good)
        check("good drafts: ok", code == 0 and res["ok"] and res["counts"]["stories"] == 3)

        def bad(name, change, expect):
            d = copy.deepcopy(good)
            change(d)
            code, res = verdict(p, d)
            check(name, code == 1 and res["ok"] is False and any(expect in pr["problem"] for pr in res["problems"]))

        bad("the words Fails if in a story",
            lambda d: d["slices"][0]["stories"][0]["scope_of_work"]["limits"].append("Fails if a slot is lost."),
            '"Fails if"')
        bad("a failure line of its ICE, in other words around it",
            lambda d: d["slices"][0]["stories"][2]["scope_of_work"]["expectations"].append(
                "Never: a card is charged twice."), "failure line of its ICE")
        bad("a capability ICE line in the epic",
            lambda d: d["slices"][0]["epic"].update(delivers="We check that a booking is lost never."),
            "failure line of its ICE")
        bad("a recovery phrase in the Context guidance",
            lambda d: d["slices"][0]["stories"][1]["context_guidance"].update(persona="a person must decide"),
            "recovery phrase")
        bad("an epic with no title", lambda d: d["slices"][0]["epic"].update(title=" "), "no title")
        bad("a ready feature with no story", lambda d: d["slices"][0]["stories"].pop(), "has no story")
        bad("two stories for one feature",
            lambda d: d["slices"][0]["stories"].append(copy.deepcopy(d["slices"][0]["stories"][0])), "two stories")
        bad("empty goals", lambda d: d["slices"][0]["stories"][0]["scope_of_work"].update(goals=[]), "no goals")
        bad("a missing Context guidance line",
            lambda d: d["slices"][0]["stories"][0]["context_guidance"].pop("never_read"), "'never_read'")
        bad("a story for a feature outside the slice",
            lambda d: d["slices"][0]["stories"].append(story_draft("ft-cancel", [])), "not in the slice")
        bad("no entry for the slice", lambda d: d["slices"].clear(), "no entry")

        set_slice(root, "sl-self-booking", ["ft-pick", "ft-wait"])
        gather(root, p)
        d = make_drafts(p)
        code, res = verdict(p, d)
        check("a skipped feature needs no story", code == 0 and res["ok"])
        d["slices"][0]["stories"].append(story_draft("ft-wait", []))
        code, res = verdict(p, d)
        check("a story for a feature that is not ready is refused",
              code == 1 and any("not ready" in pr["problem"] for pr in res["problems"]))
        write(p["drafts"], "not json")
        code, _, _ = run("check_drafts.py", "--drafts", p["drafts"], "--gather", p["gather"],
                         "--out", os.path.join(p["working"], "x.json"))
        check("drafts that cannot be read: exit 2", code == 2)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
