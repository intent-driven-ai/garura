#!/usr/bin/env python3
"""
test_rollup_box.py — fixture tests for rollup_box.py (#615).

Pins the roll-up over one run's many capabilities: every capability is measured against the
box as it stood at the START of the run, so a second capability's box-move never hides
behind a box the first one raised; each move names its capability; the box takes the
highest need and never lowers a dimension; a directional box is established with no moves;
and a single manifest without a capability_ref still works as before.

    python3 test_rollup_box.py
"""

import json
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rollup_box as rb  # noqa: E402

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


def roll(tmp, profile, manifests):
    spine = os.path.join(tmp, "_spine.yaml")
    with open(spine, "w") as fh:
        yaml.safe_dump({"profile": profile}, fh)
    argv = ["--spine", spine, "--out-profile", os.path.join(tmp, "profile.yaml"),
            "--out-report", os.path.join(tmp, "rollup.json")]
    for i, man in enumerate(manifests):
        path = os.path.join(tmp, f"enrich-{i}.yaml")
        with open(path, "w") as fh:
            yaml.safe_dump({"enrich": man}, fh)
        argv += ["--enrich-manifest", path]
    code = rb.main(argv)
    if code != 0:
        return code, None, None
    with open(os.path.join(tmp, "rollup.json")) as fh:
        report = json.load(fh)
    with open(os.path.join(tmp, "profile.yaml")) as fh:
        box = yaml.safe_load(fh)["profile"]
    return code, report, box


SET_BOX = {"state": "set", "nfr": {"security": {"level": "high", "gate": "pen test"},
                                   "latency": {"level": "medium", "gate": "p95"}},
           "compliance": ["gdpr"]}


def test_measured_against_the_start():
    with tempfile.TemporaryDirectory() as tmp:
        code, report, box = roll(tmp, SET_BOX, [
            {"capability_ref": "checkout", "implied_levels": {"security": {"level": "xhigh"}}},
            {"capability_ref": "refunds", "implied_levels": {"security": {"level": "xhigh"}}},
        ])
        check("two capabilities roll up", code == 0)
        check("both box-moves are shown, the second not hidden by the first",
              report["box_moves"] == [
                  {"capability": "checkout", "dimension": "security", "from": "high", "to": "xhigh"},
                  {"capability": "refunds", "dimension": "security", "from": "high", "to": "xhigh"}])
        check("the report lists the run's capabilities", report["capabilities"] == ["checkout", "refunds"])
        check("the box is raised once", box["nfr"]["security"]["level"] == "xhigh")
        check("out_of_box is flagged", report["out_of_box"] is True)


def test_highest_need_wins():
    with tempfile.TemporaryDirectory() as tmp:
        code, report, box = roll(tmp, SET_BOX, [
            {"capability_ref": "checkout", "implied_levels": {"latency": {"level": "high", "gate": "p99"}}},
            {"capability_ref": "refunds", "implied_levels": {"latency": {"level": "xhigh", "gate": "p999"}}},
            {"capability_ref": "search", "implied_levels": {"latency": {"level": "low"},
                                                             "security": {"level": "medium"}}},
        ])
        check("the box takes the highest need", box["nfr"]["latency"] == {"level": "xhigh", "gate": "p999"})
        check("a need inside the box never lowers it", box["nfr"]["security"]["level"] == "high")
        check("each capability over the start box gets its own move, from the start level",
              [(m["capability"], m["from"], m["to"]) for m in report["box_moves"]]
              == [("checkout", "medium", "high"), ("refunds", "medium", "xhigh")])


def test_compliance_per_capability():
    with tempfile.TemporaryDirectory() as tmp:
        code, report, box = roll(tmp, SET_BOX, [
            {"capability_ref": "checkout", "compliance": ["pci-dss", "gdpr"]},
            {"capability_ref": "refunds", "compliance": ["pci-dss"]},
        ])
        check("a new regime is added to the box once", box["compliance"] == ["gdpr", "pci-dss"])
        check("each capability needing the new regime gets its own move",
              [m["capability"] for m in report["box_moves"]] == ["checkout", "refunds"])
        check("a regime already in the box is no move",
              all(m["dimension"] == "compliance:pci-dss" for m in report["box_moves"]))


def test_directional_box():
    with tempfile.TemporaryDirectory() as tmp:
        code, report, box = roll(tmp, {"state": "directional"}, [
            {"capability_ref": "checkout", "implied_levels": {"security": {"level": "high"}}},
            {"capability_ref": "refunds", "implied_levels": {"security": {"level": "xhigh"}}},
        ])
        check("a directional box is established with no moves", report["box_moves"] == [])
        check("it is firmed to set", box["state"] == "set")
        check("it takes the highest need", box["nfr"]["security"]["level"] == "xhigh")


def test_single_manifest_as_before():
    with tempfile.TemporaryDirectory() as tmp:
        code, report, box = roll(tmp, SET_BOX, [{"implied_levels": {"security": {"level": "xhigh"}}}])
        check("one manifest with no capability_ref still rolls up", code == 0)
        check("its move carries no capability field",
              report["box_moves"] == [{"dimension": "security", "from": "high", "to": "xhigh"}])


def test_refusals():
    with tempfile.TemporaryDirectory() as tmp:
        code, _, _ = roll(tmp, SET_BOX, [{"implied_levels": {}}, {"capability_ref": "refunds"}])
        check("many manifests with one lacking capability_ref are refused", code == 2)
    with tempfile.TemporaryDirectory() as tmp:
        code, _, _ = roll(tmp, SET_BOX, [{"capability_ref": "refunds"}, {"capability_ref": "refunds"}])
        check("two manifests for one capability are refused", code == 2)


def main():
    for test in (test_measured_against_the_start, test_highest_need_wins,
                 test_compliance_per_capability, test_directional_box,
                 test_single_manifest_as_before, test_refusals):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
