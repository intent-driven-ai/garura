#!/usr/bin/env python3
"""test_check_drafts.py — check_drafts.py keeps failure and recovery text out of the epic and the Feature issues (C5, C6, C9).

    python3 test_check_drafts.py
"""
import copy
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, finish, gather, make_drafts, make_model, paths, read, read_json,  # noqa: E402
                          feature_draft, run, set_slice, write)


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
        check("good drafts: ok", code == 0 and res["ok"] and res["counts"]["features"] == 3)

        def bad(name, change, expect):
            d = copy.deepcopy(good)
            change(d)
            code, res = verdict(p, d)
            check(name, code == 1 and res["ok"] is False and any(expect in pr["problem"] for pr in res["problems"]))

        bad("the words Fails if in a Feature issue",
            lambda d: d["features"][0]["scope_of_work"]["limits"].append("Fails if a slot is lost."),
            '"Fails if"')
        bad("a failure line of its ICE, in other words around it",
            lambda d: d["features"][2]["scope_of_work"]["expectations"].append(
                "Never: a card is charged twice."), "failure line of its ICE")
        bad("a capability ICE line in the epic",
            lambda d: d["epic"].update(delivers="We check that a booking is lost never."),
            "failure line of its ICE")
        bad("a recovery phrase in the Context guidance",
            lambda d: d["features"][1]["context_guidance"].update(persona="a person must decide"),
            "recovery phrase")
        bad("an epic with no title", lambda d: d["epic"].update(title=" "), "no title")
        bad("a ready feature with no draft", lambda d: d["features"].pop(), "has no Feature issue draft")
        bad("two drafts for one feature",
            lambda d: d["features"].append(copy.deepcopy(d["features"][0])), "two Feature issue drafts")
        bad("empty goals", lambda d: d["features"][0]["scope_of_work"].update(goals=[]), "no goals")
        bad("a missing Context guidance line",
            lambda d: d["features"][0]["context_guidance"].pop("never_read"), "'never_read'")
        bad("a Feature issue for a feature in no slice of the plan",
            lambda d: d["features"].append(feature_draft("ft-cancel")), "in no slice of the plan")
        bad("no epic", lambda d: d.pop("epic"), "the epic has no title")

        page = os.path.join(root, "clinic", "payment", "ft-pay", "feature.md")
        write(page, read(page).replace("- Context:", "- Fails if:\n  - the fee is taken twice\n"
                                       "    when the patient pays again\n- Context:"))
        gather(root, p)
        bad("a child line of a nested failure block, in the Feature issue",
            lambda d: d["features"][2]["scope_of_work"]["limits"].append(
                "Check that the fee is taken twice never happens."), "failure line of its ICE")
        bad("a wrapped line of a nested failure block, in the Feature issue",
            lambda d: d["features"][2]["scope_of_work"]["goals"].append(
                "It works when the patient pays again."), "failure line of its ICE")

        extra = [{"id": "sl-cancel", "slug": "cancel-online", "feature_refs": ["ft-pick"],
                  "intents": ["bi-340"], "vertical": "the booking page"}]
        import yaml
        spine = yaml.safe_load(read(os.path.join(root, "_spine.yaml")))
        spine["slices"] += extra
        write(os.path.join(root, "_spine.yaml"), spine)
        gather(root, p)
        code, res = verdict(p, make_drafts(p))
        check("a feature in two slices needs one draft only (S12)", code == 0 and res["counts"]["features"] == 3)
        spine["slices"] = spine["slices"][:1]
        write(os.path.join(root, "_spine.yaml"), spine)
        set_slice(root, "sl-self-booking", ["ft-pick", "ft-wait"])
        gather(root, p)
        d = make_drafts(p)
        code, res = verdict(p, d)
        check("a skipped feature needs no draft", code == 0 and res["ok"])
        d["features"].append(feature_draft("ft-wait"))
        code, res = verdict(p, d)
        check("a draft for a feature that is not ready is refused",
              code == 1 and any("not ready" in pr["problem"] for pr in res["problems"]))
        write(p["drafts"], "not json")
        code, _, _ = run("check_drafts.py", "--drafts", p["drafts"], "--gather", p["gather"],
                         "--out", os.path.join(p["working"], "x.json"))
        check("drafts that cannot be read: exit 2", code == 2)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
