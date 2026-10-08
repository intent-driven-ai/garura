#!/usr/bin/env python3
"""
test_persist_understand.py — fixture tests for persist_understand.py (#616).

Pins the keyed persist's containment and the new seed path: an absent capability is
seeded only from the person's recorded answers, under an existing domain, then promoted;
without a seed it is still refused; an already-detailed capability is never re-detailed.

    python3 test_persist_understand.py
"""

import json
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import persist_understand as pu  # noqa: E402

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


def setup(tmp, caps=None):
    base = os.path.join(tmp, "product") + os.sep
    root = os.path.join(base, "product-os")
    os.makedirs(root)
    spine = {"domains": [{"id": "commerce", "doc": "commerce/domain.md"}],
             "capabilities": caps or [], "functionalities": [], "profile": {"state": "directional"}}
    with open(os.path.join(root, "_spine.yaml"), "w") as fh:
        yaml.safe_dump(spine, fh)
    work = os.path.join(tmp, "work")
    os.makedirs(work)
    with open(os.path.join(work, "enrich.yaml"), "w") as fh:
        yaml.safe_dump({"enrich": {"capability_ref": "checkout",
                                   "capability": {"nfr_needs": {"latency": {"level": "high"}}},
                                   "functionalities": [{"id": "pay", "capability": "checkout",
                                                        "doc": "commerce/checkout/pay/functionality.md"}]}}, fh)
    with open(os.path.join(work, "profile.yaml"), "w") as fh:
        yaml.safe_dump({"profile": {"state": "set"}}, fh)
    with open(os.path.join(work, "rollup.json"), "w") as fh:
        json.dump({"box_moves": []}, fh)
    return base, root, work


def run(base, work, seed=None):
    argv = ["--enrich-manifest", os.path.join(work, "enrich.yaml"), "--product-base", base,
            "--proposed-profile", os.path.join(work, "profile.yaml"),
            "--rollup-report", os.path.join(work, "rollup.json"), "--capability-ref", "checkout",
            "--date", "2026-10-08", "--out-manifest", os.path.join(work, "persist.json")]
    if seed is not None:
        path = os.path.join(work, "seed.yaml")
        with open(path, "w") as fh:
            yaml.safe_dump({"seed": seed}, fh)
        argv += ["--seed", path]
    return pu.main(argv)


def spine(root):
    with open(os.path.join(root, "_spine.yaml")) as fh:
        return yaml.safe_load(fh)


ANSWERS = {"id": "checkout", "domain": "commerce", "one_line": "Let a shopper pay for a cart",
           "why": "No sale without it", "answered_by": "human"}


def test_existing_seed():
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp, [{"id": "checkout", "domain": "commerce", "status": "proposed",
                                        "detail": "directional", "doc": "commerce/checkout/capability.md"}])
        check("a directional seed is detailed", run(base, work) == 0)
        cap = spine(root)["capabilities"][0]
        check("it is promoted to detailed", cap["detail"] == "detailed")
        check("the record says it was not seeded here",
              json.load(open(os.path.join(work, "persist.json")))["seeded"] is False)


def test_absent_without_seed():
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp)
        check("an absent capability with no seed is refused", run(base, work) == 2)
        check("nothing was written", spine(root)["capabilities"] == [])


def test_absent_with_seed():
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp)
        check("an absent capability with the person's answers is seeded", run(base, work, ANSWERS) == 0)
        cap = spine(root)["capabilities"][0]
        check("the seed joins the named domain", cap["domain"] == "commerce")
        check("the seed is then detailed in the same run", cap["detail"] == "detailed")
        check("the seed keeps status proposed", cap["status"] == "proposed")
        check("the record says seeded", json.load(open(os.path.join(work, "persist.json")))["seeded"] is True)


def test_seed_refusals():
    for label, seed in (("missing the why", {k: v for k, v in ANSWERS.items() if k != "why"}),
                        ("not answered by a person", {k: v for k, v in ANSWERS.items() if k != "answered_by"}),
                        ("an unknown domain", dict(ANSWERS, domain="nowhere")),
                        ("a different capability id", dict(ANSWERS, id="cart"))):
        with tempfile.TemporaryDirectory() as tmp:
            base, root, work = setup(tmp)
            check(f"a seed {label} is refused", run(base, work, seed) == 2)
            check(f"nothing written for a seed {label}", spine(root)["capabilities"] == [])


def test_already_detailed():
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp, [{"id": "checkout", "domain": "commerce", "status": "proposed",
                                        "detail": "detailed", "doc": "commerce/checkout/capability.md"}])
        check("an already-detailed capability is not re-detailed", run(base, work) == 2)


def main():
    for test in (test_existing_seed, test_absent_without_seed, test_absent_with_seed,
                 test_seed_refusals, test_already_detailed):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
