#!/usr/bin/env python3
"""test_check_ice_workable.py — fixture tests for check_ice_workable.py (#612).

An ICE is workable only when its node's spine `intents` names a confirmed business intent;
no intent, a proposed or dropped one, or a missing page leaves it kept but not workable.

    python3 test_check_ice_workable.py
"""
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_ice_workable as cw  # noqa: E402

PASSED = 0
FAILED = 0


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")
        if os.environ.get("PYTEST_CURRENT_TEST"):
            raise AssertionError(name)


def page(stage):
    return f"# An intent\n\n**Outcome:** something\n**Stage:** {stage} — by Kapil, 2026-10-09\n"


def setup(tmp):
    intents = os.path.join(tmp, "intents")
    os.makedirs(intents)
    for iid, stage in (("confirmed-one", "confirmed"), ("proposed-one", "proposed"),
                       ("dropped-one", "dropped"), ("met-one", "met")):
        with open(os.path.join(intents, f"{iid}.md"), "w") as fh:
            fh.write(page(stage))
    spine = {"capabilities": [
        {"id": "cap-ok", "domain": "", "intents": ["proposed-one", "confirmed-one"]},
        {"id": "cap-none", "domain": "d1"},
        {"id": "cap-proposed", "domain": "d1", "intents": ["proposed-one"]},
        {"id": "cap-dropped", "domain": "d1", "intents": ["dropped-one"]},
        {"id": "cap-missing", "domain": "d1", "intents": ["no-such-intent"]},
        {"id": "cap-met", "domain": "d1", "intents": ["met-one"]}],
        "functionalities": [{"id": "fn-ok", "capability": "cap-ok", "intents": ["confirmed-one"]}]}
    path = os.path.join(tmp, "_spine.yaml")
    with open(path, "w") as fh:
        yaml.safe_dump(spine, fh)
    return path, intents


def main():
    with tempfile.TemporaryDirectory() as tmp:
        spine, intents = setup(tmp)
        args = ["--spine", spine, "--intents-dir", intents]
        check("built from a confirmed intent is workable (one confirmed is enough)",
              cw.main(args + ["--node", "cap-ok"]) == 0)
        check("a functionality is checked the same way", cw.main(args + ["--node", "fn-ok"]) == 0)
        check("built from a met intent stays workable", cw.main(args + ["--node", "cap-met"]) == 0)
        for node, label in (("cap-none", "no intent at all"), ("cap-proposed", "only a proposed intent"),
                            ("cap-dropped", "only a dropped intent"), ("cap-missing", "an intent with no page")):
            check(f"{label} is kept but not workable", cw.main(args + ["--node", node]) == 1)
        check("an unknown node is an error, not a pass", cw.main(args + ["--node", "nope"]) == 2)
        out = os.path.join(tmp, "r.json")
        check("the full report runs and exits 0", cw.main(args + ["--out", out]) == 0)
        import json
        with open(out) as fh:
            r = json.load(fh)
        check("the report counts workable and not workable", r["workable"] == 3 and r["not_workable"] == 4)
        bad = os.path.join(tmp, "bad.yaml")
        with open(bad, "w") as fh:
            fh.write("- not a mapping\n")
        check("an unreadable spine exits 2", cw.main(["--spine", bad, "--intents-dir", intents]) == 2)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
