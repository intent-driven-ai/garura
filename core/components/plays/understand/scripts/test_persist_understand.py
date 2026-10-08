#!/usr/bin/env python3
"""
test_persist_understand.py — fixture tests for persist_understand.py (#616).

Pins the keyed persist's containment (a sibling capability or a functionality under a
sibling is never written) and the seed path (#616): an absent capability is seeded only
from the person's recorded answers (answered_by: human), under an existing domain, at a
'<domain>/<capability>/capability.md' doc path, then promoted; without a seed it is still
refused; a malformed seed file is refused, not a crash; an already-detailed capability is
never re-detailed.

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
        if os.environ.get("PYTEST_CURRENT_TEST"):  # fail loudly under a test collector too
            raise AssertionError(name)


def read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


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
              read_json(os.path.join(work, "persist.json"))["seeded"] is False)


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
        check("the record says seeded", read_json(os.path.join(work, "persist.json"))["seeded"] is True)


def test_seed_refusals():
    for label, seed in (("missing the why", {k: v for k, v in ANSWERS.items() if k != "why"}),
                        ("not answered by a person", {k: v for k, v in ANSWERS.items() if k != "answered_by"}),
                        ("answered by an agent", dict(ANSWERS, answered_by="agent")),
                        ("with a doc outside its domain", dict(ANSWERS, doc="../../etc/capability.md")),
                        ("with a doc not named capability.md", dict(ANSWERS, doc="commerce/checkout/x.md")),
                        ("an unknown domain", dict(ANSWERS, domain="nowhere")),
                        ("a different capability id", dict(ANSWERS, id="cart"))):
        with tempfile.TemporaryDirectory() as tmp:
            base, root, work = setup(tmp)
            check(f"a seed {label} is refused", run(base, work, seed) == 2)
            check(f"nothing written for a seed {label}", spine(root)["capabilities"] == [])


def test_seed_not_a_mapping():
    for label, body in (("a list", ["checkout"]), ("a string", "checkout")):
        with tempfile.TemporaryDirectory() as tmp:
            base, root, work = setup(tmp)
            path = os.path.join(work, "seed.yaml")
            with open(path, "w") as fh:
                yaml.safe_dump(body, fh)
            argv = ["--enrich-manifest", os.path.join(work, "enrich.yaml"), "--product-base", base,
                    "--proposed-profile", os.path.join(work, "profile.yaml"),
                    "--rollup-report", os.path.join(work, "rollup.json"), "--capability-ref", "checkout",
                    "--date", "2026-10-08", "--out-manifest", os.path.join(work, "persist.json"),
                    "--seed", path]
            check(f"a seed file that is {label} is refused, not a crash", pu.main(argv) == 2)


def test_sibling_containment():
    sibling = {"id": "cart", "domain": "commerce", "status": "proposed", "detail": "directional",
               "doc": "commerce/cart/capability.md"}
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp, [dict(sibling), {"id": "checkout", "domain": "commerce",
                                                        "status": "proposed", "detail": "directional",
                                                        "doc": "commerce/checkout/capability.md"}])
        check("a normal run succeeds next to a sibling", run(base, work) == 0)
        cap = next(c for c in spine(root)["capabilities"] if c["id"] == "cart")
        check("the sibling capability is untouched", cap == sibling)
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp, [dict(sibling)])
        with open(os.path.join(work, "enrich.yaml"), "w") as fh:
            yaml.safe_dump({"enrich": {"capability_ref": "checkout", "capability": {},
                                       "functionalities": [{"id": "x", "capability": "cart"}]}}, fh)
        check("a functionality under a sibling is refused", run(base, work, ANSWERS) == 2)
        check("nothing written when a sibling is targeted",
              [c["id"] for c in spine(root)["capabilities"]] == ["cart"])
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp, [dict(sibling)])
        with open(os.path.join(work, "enrich.yaml"), "w") as fh:
            yaml.safe_dump({"enrich": {"capability_ref": "cart", "capability": {}}}, fh)
        check("a manifest naming a sibling is refused", run(base, work, ANSWERS) == 2)


def test_already_detailed():
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp, [{"id": "checkout", "domain": "commerce", "status": "proposed",
                                        "detail": "detailed", "doc": "commerce/checkout/capability.md"}])
        check("an already-detailed capability is not re-detailed", run(base, work) == 2)


def main():
    for test in (test_existing_seed, test_absent_without_seed, test_absent_with_seed,
                 test_seed_refusals, test_seed_not_a_mapping, test_sibling_containment,
                 test_already_detailed):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
