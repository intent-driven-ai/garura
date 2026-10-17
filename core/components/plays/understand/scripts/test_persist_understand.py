#!/usr/bin/env python3
"""
test_persist_understand.py — fixture tests for persist_understand.py (#616).

Pins the keyed persist's containment (a sibling capability or a functionality under a
sibling is never written) and the seed path (#616): an absent capability is seeded only
from the person's recorded answers (answered_by: human), under an existing domain, at a
'<domain>/<capability>/capability.md' doc path, then promoted; without a seed it is still
refused; a malformed seed file is refused, not a crash; an already-detailed capability is
never re-detailed. Inside a drive (#615) a box-move decision is written `proposed`; by hand
it stays `accepted`. One run details many targets (#615): each manifest is keyed to its own
target, a box-move is linked to the capability it names, and a refusal writes nothing. The
box never goes down (a lowered, unfirmed or regime-dropping profile is refused), a
functionality id is never clashed or left empty, and the record's box_moves carry each
decision's id and status.

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


def run(base, work, seed=None, extra=()):
    argv = ["--enrich-manifest", os.path.join(work, "enrich.yaml"), "--product-base", base,
            "--proposed-profile", os.path.join(work, "profile.yaml"),
            "--rollup-report", os.path.join(work, "rollup.json"), "--capability-ref", "checkout",
            "--date", "2026-10-08", "--out-manifest", os.path.join(work, "persist.json")]
    if seed is not None:
        path = os.path.join(work, "seed.yaml")
        with open(path, "w") as fh:
            yaml.safe_dump({"seed": seed}, fh)
        argv += ["--seed", path]
    return pu.main(argv + list(extra))


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
              read_json(os.path.join(work, "persist.json"))["seeded"] == [])


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
        check("the record says seeded",
              read_json(os.path.join(work, "persist.json"))["seeded"] == ["checkout"])


def test_seed_refusals():
    for label, seed in (("missing the why", {k: v for k, v in ANSWERS.items() if k != "why"}),
                        ("not answered by a person", {k: v for k, v in ANSWERS.items() if k != "answered_by"}),
                        ("answered by an agent", dict(ANSWERS, answered_by="agent")),
                        ("with a doc outside its domain", dict(ANSWERS, doc="../../etc/capability.md")),
                        ("with a doc not named capability.md", dict(ANSWERS, doc="commerce/checkout/x.md")),
                        ("with a doc that is not text", dict(ANSWERS, doc=["commerce", "checkout"])),
                        ("with a domain that is not text", dict(ANSWERS, domain=["commerce"])),
                        ("an unknown domain", dict(ANSWERS, domain="nowhere")),
                        ("a different capability id", dict(ANSWERS, id="cart"))):
        with tempfile.TemporaryDirectory() as tmp:
            base, root, work = setup(tmp)
            check(f"a seed {label} is refused", run(base, work, seed) == 2)
            check(f"nothing written for a seed {label}", spine(root)["capabilities"] == [])


def test_domain_folder_differs_from_id():
    """A domain id like 'dom-commerce' lives in folder 'commerce/' (its doc says so)."""
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp)
        sp = spine(root)
        sp["domains"] = [{"id": "dom-commerce", "doc": "commerce/domain.md"}]
        with open(os.path.join(root, "_spine.yaml"), "w") as fh:
            yaml.safe_dump(sp, fh)
        answers = dict(ANSWERS, domain="dom-commerce")
        check("a seed under a prefixed domain id is accepted", run(base, work, answers) == 0)
        cap = spine(root)["capabilities"][0]
        check("its doc lands in the domain's folder, not a folder named after the id",
              cap["doc"] == "commerce/checkout/capability.md")
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp)
        sp = spine(root)
        sp["domains"] = [{"id": "dom-commerce", "doc": "commerce/domain.md"}]
        with open(os.path.join(root, "_spine.yaml"), "w") as fh:
            yaml.safe_dump(sp, fh)
        bad = dict(ANSWERS, domain="dom-commerce", doc="dom-commerce/checkout/capability.md")
        check("a doc in a folder named after the id is refused", run(base, work, bad) == 2)


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


def test_box_move_status():
    caps = [{"id": "checkout", "domain": "commerce", "status": "proposed",
             "detail": "directional", "doc": "commerce/checkout/capability.md"}]
    move = {"dimension": "security", "from": "high", "to": "xhigh"}
    did = "dec-checkout-security-high-xhigh"
    for label, extra, want in (("by hand", (), "accepted"),
                               ("inside a drive", ("--decision-status", "proposed"), "proposed")):
        with tempfile.TemporaryDirectory() as tmp:
            base, root, work = setup(tmp, caps)
            with open(os.path.join(work, "rollup.json"), "w") as fh:
                json.dump({"box_moves": [move]}, fh)
            check(f"{label}, a box-move persists", run(base, work, extra=extra) == 0)
            with open(os.path.join(root, "decisions", f"{did}.yaml")) as fh:
                status = yaml.safe_load(fh)["decision"]["status"]
            check(f"{label}, its decision reads {want}", status == want)
            check(f"{label}, the decision is linked onto the capability",
                  did in spine(root)["capabilities"][0].get("decisions", []))
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp, caps)
        try:
            refused = run(base, work, extra=("--decision-status", "rejected")) != 0
        except SystemExit as exc:
            refused = exc.code != 0
        check("a status other than accepted or proposed is refused", refused)


def setup_two(tmp, moves):
    """Two directional targets, checkout and refunds, one manifest each."""
    caps = [{"id": cid, "domain": "commerce", "status": "proposed", "detail": "directional",
             "doc": f"commerce/{cid}/capability.md"} for cid in ("checkout", "refunds")]
    base, root, work = setup(tmp, caps)
    paths = []
    for cid in ("checkout", "refunds"):
        path = os.path.join(work, f"enrich-{cid}.yaml")
        with open(path, "w") as fh:
            yaml.safe_dump({"enrich": {"capability_ref": cid,
                                       "capability": {"nfr_needs": {"security": {"level": "xhigh"}}},
                                       "functionalities": [{"id": f"{cid}-main", "capability": cid,
                                                            "doc": f"commerce/{cid}/main/functionality.md"}]}},
                           fh)
        paths.append(path)
    with open(os.path.join(work, "rollup.json"), "w") as fh:
        json.dump({"box_moves": moves}, fh)
    return base, root, work, paths


def run_many(base, work, manifests, refs, extra=()):
    argv = ["--product-base", base, "--proposed-profile", os.path.join(work, "profile.yaml"),
            "--rollup-report", os.path.join(work, "rollup.json"), "--date", "2026-10-17",
            "--out-manifest", os.path.join(work, "persist.json")]
    for m in manifests:
        argv += ["--enrich-manifest", m]
    for r in refs:
        argv += ["--capability-ref", r]
    return pu.main(argv + list(extra))


def test_many_targets():
    moves = [{"capability": "checkout", "dimension": "security", "from": "high", "to": "xhigh"},
             {"capability": "refunds", "dimension": "security", "from": "high", "to": "xhigh"}]
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work, paths = setup_two(tmp, moves)
        check("one run details two targets", run_many(base, work, paths, ["checkout", "refunds"]) == 0)
        caps = {c["id"]: c for c in spine(root)["capabilities"]}
        check("both targets are detailed",
              caps["checkout"]["detail"] == "detailed" and caps["refunds"]["detail"] == "detailed")
        funcs = {f["id"]: f["capability"] for f in spine(root)["functionalities"]}
        check("each target keeps its own functionalities",
              funcs == {"checkout-main": "checkout", "refunds-main": "refunds"})
        for cid in ("checkout", "refunds"):
            did = f"dec-{cid}-security-high-xhigh"
            check(f"{cid} gets its own box-move decision",
                  os.path.isfile(os.path.join(root, "decisions", f"{did}.yaml")))
            check(f"{cid}'s decision is linked onto {cid} only", caps[cid].get("decisions") == [did])
        rec = read_json(os.path.join(work, "persist.json"))
        check("the record lists both targets", rec["changed"]["capabilities"] == ["checkout", "refunds"])


def test_many_targets_refusals():
    move = {"capability": "checkout", "dimension": "security", "from": "high", "to": "xhigh"}
    cases = (
        ("a manifest whose target is not named", lambda p: (p, ["checkout"])),
        ("a named target with no manifest", lambda p: (p[:1], ["checkout", "refunds"])),
        ("a target named twice", lambda p: (p, ["checkout", "refunds", "checkout"])),
        ("two manifests for one target", lambda p: ([p[0], p[0]], ["checkout", "refunds"])),
    )
    for label, pick in cases:
        with tempfile.TemporaryDirectory() as tmp:
            base, root, work, paths = setup_two(tmp, [move])
            manifests, refs = pick(paths)
            check(f"{label} is refused", run_many(base, work, manifests, refs) == 2)
            check(f"nothing written for {label}",
                  all(c["detail"] == "directional" for c in spine(root)["capabilities"])
                  and not os.path.isdir(os.path.join(root, "decisions")))
    with tempfile.TemporaryDirectory() as tmp:
        stray = dict(move, capability="cart")
        base, root, work, paths = setup_two(tmp, [move, stray])
        check("a box-move for a capability outside the run is refused",
              run_many(base, work, paths, ["checkout", "refunds"]) == 2)
        check("nothing written when a box-move is stray",
              all(c["detail"] == "directional" for c in spine(root)["capabilities"])
              and not os.path.isdir(os.path.join(root, "decisions")))


def write_profiles(root, work, live_profile, proposed):
    sp = spine(root)
    sp["profile"] = live_profile
    with open(os.path.join(root, "_spine.yaml"), "w") as fh:
        yaml.safe_dump(sp, fh)
    with open(os.path.join(work, "profile.yaml"), "w") as fh:
        yaml.safe_dump({"profile": proposed}, fh)


def test_profile_never_lowered():
    caps = [{"id": "checkout", "domain": "commerce", "status": "proposed",
             "detail": "directional", "doc": "commerce/checkout/capability.md"}]
    live = {"state": "set", "nfr": {"security": {"level": "high"}}, "compliance": ["gdpr"]}
    for label, proposed in (
            ("a lowered dimension", {"state": "set", "nfr": {"security": {"level": "medium"}},
                                     "compliance": ["gdpr"]}),
            ("a missing dimension", {"state": "set", "nfr": {}, "compliance": ["gdpr"]}),
            ("a dropped regime", {"state": "set", "nfr": {"security": {"level": "high"}},
                                  "compliance": []}),
            ("an empty profile", {}),
            ("a profile not firmed to set", {"state": "directional",
                                             "nfr": {"security": {"level": "high"}},
                                             "compliance": ["gdpr"]})):
        with tempfile.TemporaryDirectory() as tmp:
            base, root, work = setup(tmp, caps)
            write_profiles(root, work, live, proposed)
            check(f"{label} is refused", run(base, work) == 2)
            check(f"nothing written for {label}",
                  spine(root)["capabilities"][0]["detail"] == "directional"
                  and spine(root)["profile"] == live)
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work = setup(tmp, caps)
        write_profiles(root, work, live, {"state": "set", "nfr": {"security": {"level": "xhigh"}},
                                          "compliance": ["gdpr", "pci-dss"]})
        check("a raised profile is saved", run(base, work) == 0
              and spine(root)["profile"]["nfr"]["security"]["level"] == "xhigh")


def test_functionality_ids():
    move = {"capability": "checkout", "dimension": "security", "from": "high", "to": "xhigh"}
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work, paths = setup_two(tmp, [move])
        with open(paths[1]) as fh:
            man = yaml.safe_load(fh)
        man["enrich"]["functionalities"][0]["id"] = "checkout-main"
        with open(paths[1], "w") as fh:
            yaml.safe_dump(man, fh)
        check("a functionality id declared by two targets is refused",
              run_many(base, work, paths, ["checkout", "refunds"]) == 2)
        check("nothing written on an id clash", spine(root)["functionalities"] == [])
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work, paths = setup_two(tmp, [move])
        with open(paths[0]) as fh:
            man = yaml.safe_load(fh)
        del man["enrich"]["functionalities"][0]["id"]
        with open(paths[0], "w") as fh:
            yaml.safe_dump(man, fh)
        check("a functionality with no id is refused",
              run_many(base, work, paths, ["checkout", "refunds"]) == 2)
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work, paths = setup_two(tmp, [move])
        sp = spine(root)
        sp["functionalities"] = [{"id": "refunds-main", "capability": "cart"}]
        with open(os.path.join(root, "_spine.yaml"), "w") as fh:
            yaml.safe_dump(sp, fh)
        check("an id already in the spine under another capability is refused",
              run_many(base, work, paths, ["checkout", "refunds"]) == 2)
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work, paths = setup_two(tmp, [move])
        sp = spine(root)
        kept = {"id": "refunds-main", "capability": "refunds", "doc": "old.md"}
        sp["functionalities"] = [kept]
        with open(os.path.join(root, "_spine.yaml"), "w") as fh:
            yaml.safe_dump(sp, fh)
        check("an id already in the spine under the same capability is accepted",
              run_many(base, work, paths, ["checkout", "refunds"]) == 0)
        check("and the existing entry is left untouched",
              next(f for f in spine(root)["functionalities"] if f["id"] == "refunds-main") == kept)


def test_record_carries_decision_status():
    moves = [{"capability": "checkout", "dimension": "security", "from": "high", "to": "xhigh"},
             {"capability": "refunds", "dimension": "security", "from": "high", "to": "xhigh"}]
    for label, extra, want in (("by hand", (), "accepted"),
                               ("inside a drive", ("--decision-status", "proposed"), "proposed")):
        with tempfile.TemporaryDirectory() as tmp:
            base, root, work, paths = setup_two(tmp, moves)
            run_many(base, work, paths, ["checkout", "refunds"], extra)
            rec = read_json(os.path.join(work, "persist.json"))
            check(f"{label}, every box-move in the record reads {want}",
                  [m["status"] for m in rec["box_moves"]] == [want, want])
            check(f"{label}, each record line names its decision",
                  [m["decision"] for m in rec["box_moves"]]
                  == ["dec-checkout-security-high-xhigh", "dec-refunds-security-high-xhigh"])
    with tempfile.TemporaryDirectory() as tmp:
        base, root, work, paths = setup_two(tmp, [{"capability": "checkout", "dimension": "security"}])
        check("a box-move missing from/to is refused, not a crash",
              run_many(base, work, paths, ["checkout", "refunds"]) == 2)


def main():
    for test in (test_existing_seed, test_absent_without_seed, test_absent_with_seed,
                 test_seed_refusals, test_domain_folder_differs_from_id, test_seed_not_a_mapping,
                 test_sibling_containment,
                 test_already_detailed, test_box_move_status, test_many_targets,
                 test_many_targets_refusals, test_profile_never_lowered, test_functionality_ids,
                 test_record_carries_decision_status):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
