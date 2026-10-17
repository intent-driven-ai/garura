#!/usr/bin/env python3
"""
test_pick_targets.py — fixture tests for pick_targets.py (#615).

Pins how one /understand run picks its targets: with none named, every directional
capability in spine order (and, inside a drive, every capability the contract seeds);
named ones in the order given; an already-detailed target refused; an absent target
asked for unless the drive's contract answered it — then its seed is written verbatim
with answered_by: human; a contract answer naming an unknown domain is asked again.

    python3 test_pick_targets.py
"""

import json
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pick_targets as pt  # noqa: E402

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
        if os.environ.get("PYTEST_CURRENT_TEST"):  # fail loudly under a test collector too
            raise AssertionError(name)


SPINE = {"domains": [{"id": "commerce", "doc": "commerce/domain.md"}],
         "capabilities": [
             {"id": "checkout", "domain": "commerce", "detail": "directional"},
             {"id": "cart", "domain": "commerce", "detail": "detailed"},
             {"id": "refunds", "domain": "commerce", "detail": "directional"}]}
ANSWER = {"one_line": "Let a shopper return an item", "why": "Trust", "domain": "commerce"}


def pick(tmp, run, names=()):
    spine = os.path.join(tmp, "_spine.yaml")
    with open(spine, "w") as fh:
        yaml.safe_dump(SPINE, fh)
    run_path = os.path.join(tmp, "run.json")
    with open(run_path, "w") as fh:
        json.dump(run, fh)
    out = os.path.join(tmp, "targets.json")
    argv = ["--spine", spine, "--run", run_path, "--working", tmp, "--out", out]
    for n in names:
        argv += ["--capability", n]
    code = pt.main(argv)
    with open(out) as fh:
        return code, json.load(fh)


def ids(result):
    return [t["id"] for t in result["targets"]]


def test_all_pending_by_hand():
    with tempfile.TemporaryDirectory() as tmp:
        code, res = pick(tmp, {"in_drive": False})
        check("with none named, every directional capability is a target, in spine order",
              code == 0 and ids(res) == ["checkout", "refunds"])
        check("a detailed capability is not pending", res["refused"] == [] and res["ask"] == [])


def test_named():
    with tempfile.TemporaryDirectory() as tmp:
        code, res = pick(tmp, {"in_drive": False}, ["refunds,checkout"])
        check("named targets keep the order given", ids(res) == ["refunds", "checkout"])
    with tempfile.TemporaryDirectory() as tmp:
        code, res = pick(tmp, {"in_drive": False}, ["cart"])
        check("a named detailed target is refused", [r["id"] for r in res["refused"]] == ["cart"])
    with tempfile.TemporaryDirectory() as tmp:
        code, res = pick(tmp, {"in_drive": False}, ["wishlist"])
        check("a named absent target by hand is asked for", res["ask"] == ["wishlist"])
        check("its seed is not filled in", res["targets"][0]["seed"] is None)


def test_drive_seeds():
    run = {"in_drive": True, "answers": {"seeds": {"returns": ANSWER}}}
    with tempfile.TemporaryDirectory() as tmp:
        code, res = pick(tmp, run)
        check("inside a drive, contract-seeded capabilities join the pending ones",
              ids(res) == ["checkout", "refunds", "returns"])
        seed_path = res["targets"][2]["seed"]
        with open(seed_path) as fh:
            seed = yaml.safe_load(fh)["seed"]
        check("the contract's answers are written verbatim",
              {k: seed[k] for k in ("one_line", "why", "domain")} == ANSWER)
        check("the seed says a person answered", seed["answered_by"] == "human")
        check("nothing is left to ask", res["ask"] == [])
    run = {"in_drive": True, "answers": {"seeds": {"returns": dict(ANSWER, domain="nowhere")}}}
    with tempfile.TemporaryDirectory() as tmp:
        code, res = pick(tmp, run, ["returns"])
        check("an answer naming an unknown domain is asked again", res["ask"] == ["returns"])
    run = {"in_drive": True, "answers": {"seeds": {"returns": {"one_line": "x", "why": ""}}}}
    with tempfile.TemporaryDirectory() as tmp:
        code, res = pick(tmp, run, ["returns"])
        check("an incomplete answer is asked again", res["ask"] == ["returns"])
    with tempfile.TemporaryDirectory() as tmp:
        code, res = pick(tmp, {"in_drive": False, "answers": {"seeds": {"returns": ANSWER}}})
        check("by hand, seed answers in run.json are ignored", "returns" not in ids(res))


def test_nothing_pending():
    with tempfile.TemporaryDirectory() as tmp:
        spine = os.path.join(tmp, "_spine.yaml")
        with open(spine, "w") as fh:
            yaml.safe_dump({"capabilities": [{"id": "cart", "detail": "detailed"}]}, fh)
        run = os.path.join(tmp, "run.json")
        with open(run, "w") as fh:
            json.dump({"in_drive": False}, fh)
        out = os.path.join(tmp, "targets.json")
        code = pt.main(["--spine", spine, "--run", run, "--working", tmp, "--out", out])
        with open(out) as fh:
            res = json.load(fh)
        check("with nothing pending, the pick says so", code == 0 and res["nothing_pending"] is True)


def main():
    for test in (test_all_pending_by_hand, test_named, test_drive_seeds, test_nothing_pending):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
