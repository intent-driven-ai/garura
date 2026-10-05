#!/usr/bin/env python3
"""
Regression tests for /next's model read, decision tree and order (C9/C13/C14, F6/F10/F11, #533).

The bugs these guard: /next's scanner once read the pre-ADR-026 layout (profile.yaml,
per-slice record status, lens/<type>.yaml, six lenses, top-level `ice:` files,
epics/*.yaml) and recommended finished work; and the list must finish one slice
before the others advance. This file is /next's scenario validation (Step 4) — it
runs in well under a second.

Each case writes a minimal spine-shaped model to a tempdir, runs scan_model.py,
derive_candidates.derive() and the independent check_model_agreement.py (its own
reader, so a wrong scan cannot confirm itself), and asserts on the result.

Run:  python3 test_derive_candidates.py   (exit 0 = all pass, 1 = a case failed)
No pytest dependency — plain asserts, deterministic, no network/git.
"""

import contextlib
import importlib.util
import io
import json
import os
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


scan = _load("scan_model")
tree = _load("derive_candidates")
agree = _load("check_model_agreement")

DOM = "dom-shop"
SLUG = "shop"
SEVEN = ["quality", "ux", "agentic", "marketing", "architecture", "run", "measure"]


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def build(tmp, profile="set", detail="detailed", slices=(), epics=(), lens_docs=None,
          spine=True, extra_records=()):
    """slices: [(id, status, order)]; lens_docs: {slice_id: [lens types]}."""
    root = os.path.join(tmp, "product-os")
    lens_docs = lens_docs or {}
    for sid, _status, _order in slices:
        _write(os.path.join(root, SLUG, "slices", sid + ".yaml"),
               yaml.safe_dump({"slice": {"id": sid, "name": sid, "status": "proposed",
                                         "functionalities": [{"functionality_ref": "f1"}]}}))
        for lt in lens_docs.get(sid, []):
            _write(os.path.join(root, SLUG, "slices", sid, "lens", lt + ".md"), f"# {lt}\n")
    for sid in extra_records:
        _write(os.path.join(root, SLUG, "slices", sid + ".yaml"),
               yaml.safe_dump({"slice": {"id": sid, "status": "planned"}}))
    _write(os.path.join(root, SLUG, "domain.md"), "# Shop\n")
    if spine:
        doc = {
            "domains": [{"id": DOM, "slug": SLUG, "status": "active"}],
            "capabilities": [{"id": "cap-a", "domain": DOM, "detail": detail,
                              "doc": f"{SLUG}/a/capability.md"}],
            "profile": {"state": profile},
            "slices": [{"id": sid, "slug": sid, "domain_ref": DOM, "status": status,
                        "order": order, "effort": "M" if order else None,
                        "depends_on": [], "functionality_refs": ["f1"],
                        "record": f"{SLUG}/slices/{sid}.yaml"}
                       for sid, status, order in slices],
            "epics": [dict(e) for e in epics],
        }
        _write(os.path.join(root, "_spine.yaml"), yaml.safe_dump(doc, sort_keys=False))
    return tmp


def run_all(tmp):
    out = os.path.join(tmp, "_work", "state.json")
    with contextlib.redirect_stdout(io.StringIO()):
        scan.main(["--product-base", tmp, "--out", out])
    with open(out, encoding="utf-8") as fh:
        state = json.load(fh)
    cands, incons = tree.derive(state)
    with contextlib.redirect_stdout(io.StringIO()):
        agreement = agree.main(["--product-base", tmp, "--state", out])
    return state, cands, incons, agreement, out


def cmds(cands, status=None):
    return [c["command"] for c in cands if status is None or c["status"] == status]


def case_cold_start():
    with tempfile.TemporaryDirectory() as tmp:
        _state, cands, _i, _a, _o = run_all(tmp)
        assert cmds(cands) == ["/vision"], cmds(cands)


def case_griffin_like_s7():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[("s1", "planned", 1), ("s2", "planned", 2),
                           ("s3", "planned", 3), ("s4", "planned", 4)],
              lens_docs={"s2": ["ux", "agentic", "marketing"]})
        state, cands, incons, agreement, _o = run_all(tmp)
        c = cmds(cands)
        assert "/roadmap" not in c and "/understand" not in c, c
        assert not [x for x in cands if x["lane"] == "strategy"], c
        assert f"/ux {SLUG}/s1" in c and f"/arch {SLUG}/s1" in c, c
        s2 = [x for x in cands if x["target"] == f"{SLUG}/s2"]
        assert [x["command"] for x in s2] == [f"/arch {SLUG}/s2"], s2
        assert s2[0]["parallel_lane"] and s2[0]["lane"] == "foundation", s2
        assert any("roadmap order 2" in g for g in s2[0]["gates"]), s2[0]["gates"]
        assert state["domains"][0]["slices"][0]["status"] == "planned"
        assert incons == [], incons
        assert agreement == 0
        # finish-first order: slice 1's two track heads, then slice 2's /arch
        assert c[:3] == [f"/ux {SLUG}/s1", f"/arch {SLUG}/s1", f"/arch {SLUG}/s2"], c
        assert [x["rank"] for x in cands] == list(range(1, len(cands) + 1))
        assert all(len(x["why"]) >= 40 for x in cands), [x["why"] for x in cands]


def case_focus_slice_first():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[("s1", "planned", 1), ("s2", "planned", 2)],
              lens_docs={"s1": ["ux"]})
        _s, cands, _i, _a, _o = run_all(tmp)
        s1 = [x["rank"] for x in cands if x["slice"] == f"{SLUG}/s1"]
        s2 = [x["rank"] for x in cands if x["slice"] == f"{SLUG}/s2"]
        assert s1 and s2 and max(s1) < min(s2), (s1, s2)
        assert all(x["focus"] and not x["parallel_lane"] for x in cands
                   if x["slice"] == f"{SLUG}/s1"), cands
        assert all(x["parallel_lane"] for x in cands if x["slice"] == f"{SLUG}/s2"), cands


def case_ready_epic_outranks_next_slice():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[("s1", "realized", 1), ("s2", "planned", 2)],
              lens_docs={"s1": SEVEN},
              epics=[{"id": "e1", "slug": "e1", "slice_ref": f"{SLUG}/s1",
                      "status": "ready", "order": 1, "surface_type": "library"}])
        _s, cands, _i, _a, _o = run_all(tmp)
        c = cmds(cands)
        assert c[0] == f"/implement --epic {SLUG}/s1/e1", c
        assert c.index(f"/ux {SLUG}/s2") > 0, c


def case_cap_and_cut():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[(f"s{i:02d}", "planned", i) for i in range(1, 13)])
        _s, cands, _i, _a, out = run_all(tmp)
        assert len(cands) == 24, len(cands)
        res = os.path.join(tmp, "_work", "candidates.json")
        with contextlib.redirect_stdout(io.StringIO()):
            tree.main(["--state", out, "--out", res])
        with open(res, encoding="utf-8") as fh:
            doc = json.load(fh)
        assert len(doc["entries"]) == 11, len(doc["entries"])
        assert doc["cut_for_cap"] == [x["id"] for x in doc["candidates"][11:]], doc["cut_for_cap"]
        assert doc["focus_slice"] == f"{SLUG}/s01", doc["focus_slice"]


def case_realized_missing_lens_s1():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[("s1", "realized", 1)],
              lens_docs={"s1": [lt for lt in SEVEN if lt != "run"]},
              epics=[{"id": "e1", "slug": "e1", "slice_ref": f"{SLUG}/s1",
                      "status": "ready", "order": 1, "surface_type": "cli"}])
        _s, cands, incons, agreement, _o = run_all(tmp)
        assert cands[0]["lane"] == "repair" and cands[0]["command"] == f"/run {SLUG}/s1", cands[0]
        blocked = [x for x in cands if x["status"] == "blocked"]
        assert blocked and "run" in blocked[0]["blocker"], blocked
        assert any(i["kind"] == "realized-but-lens-missing" for i in incons), incons
        assert agreement == 0


def case_seven_present_planned_repair_measure():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[("s1", "planned", 1)], lens_docs={"s1": SEVEN})
        _s, cands, incons, _a, _o = run_all(tmp)
        rep = [x for x in cands if x["lane"] == "repair"]
        assert [x["command"] for x in rep] == [f"/measure {SLUG}/s1"], cands
        assert any(i["kind"] == "lenses-complete-but-unstamped" for i in incons), incons


def case_six_present_measure_next():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[("s1", "planned", 1)],
              lens_docs={"s1": [lt for lt in SEVEN if lt != "measure"]})
        _s, cands, incons, _a, _o = run_all(tmp)
        assert cmds(cands) == [f"/measure {SLUG}/s1"], cmds(cands)
        assert incons == [], incons


def case_profile_directional_understand():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, profile="directional", detail="directional")
        _s, cands, _i, agreement, _o = run_all(tmp)
        assert "/understand" in cmds(cands), cmds(cands)
        assert agreement == 0


def case_shape_uses_spine_domain_id():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, profile="set", detail="detailed")
        _s, cands, _i, _a, _o = run_all(tmp)
        assert cmds(cands) == [f"/shape {DOM}"], cmds(cands)


def case_no_spine():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[("s1", "planned", 1)], spine=False)
        _write(os.path.join(tmp, "product-os", "profile.yaml"),
               yaml.safe_dump({"profile": {"state": "directional"}}))
        state, cands, incons, agreement, _o = run_all(tmp)
        assert state["model_exists"] and state["spine_exists"] is False, state
        assert cands == [], cmds(cands)
        assert [i["kind"] for i in incons] == ["model-has-no-spine"], incons
        assert agreement == 0


def case_slice_not_indexed():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[("s1", "planned", 1)], extra_records=["ghost"])
        _s, cands, incons, agreement, _o = run_all(tmp)
        assert any(i["kind"] == "slice-not-indexed" for i in incons), incons
        assert not any("ghost" in x["target"] for x in cands), cmds(cands)
        assert agreement == 0


def case_execute_lane():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[("s1", "realized", 1)], lens_docs={"s1": SEVEN},
              epics=[{"id": "e1", "slug": "e1", "slice_ref": f"{SLUG}/s1",
                      "status": "delivered", "order": 1, "surface_type": "cli",
                      "surface_verified": True},
                     {"id": "e2", "slug": "e2", "slice_ref": f"{SLUG}/s1",
                      "status": "ready", "order": 2, "depends_on": ["e1"],
                      "surface_type": "cli"}])
        _s, cands, incons, agreement, _o = run_all(tmp)
        run = cmds(cands, "runnable")
        assert run == [f"/implement --epic {SLUG}/s1/e2"], cmds(cands)
        assert incons == [], incons
        assert agreement == 0


def case_all_delivered_learn_s5():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[("s1", "realized", 1)], lens_docs={"s1": SEVEN},
              epics=[{"id": "e1", "slug": "e1", "slice_ref": f"{SLUG}/s1",
                      "status": "delivered", "order": 1, "surface_type": "library"}])
        _s, cands, _i, _a, _o = run_all(tmp)
        c = cmds(cands)
        assert "/learn" in c, c


def case_agreement_catches_tamper():
    with tempfile.TemporaryDirectory() as tmp:
        build(tmp, slices=[("s1", "planned", 1)], lens_docs={"s1": ["ux"]})
        _s, _c, _i, agreement, out = run_all(tmp)
        assert agreement == 0
        with open(out, encoding="utf-8") as fh:
            state = json.load(fh)
        state["domains"][0]["slices"][0]["status"] = "proposed"
        state["domains"][0]["slices"][0]["lenses"]["ux"] = False
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(state, fh)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = agree.main(["--product-base", tmp, "--state", out])
        assert rc == 1, buf.getvalue()
        gaps = json.loads(buf.getvalue())["gaps"]
        assert any("status" in g for g in gaps) and any("ux.md" in g for g in gaps), gaps


CASES = [case_cold_start, case_griffin_like_s7, case_realized_missing_lens_s1,
         case_seven_present_planned_repair_measure, case_six_present_measure_next,
         case_profile_directional_understand, case_shape_uses_spine_domain_id,
         case_no_spine, case_slice_not_indexed, case_execute_lane,
         case_all_delivered_learn_s5, case_agreement_catches_tamper,
         case_focus_slice_first, case_ready_epic_outranks_next_slice, case_cap_and_cut]


def main():
    failed = 0
    for case in CASES:
        try:
            case()
            print(f"PASS {case.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"FAIL {case.__name__}: {exc}")
    print(f"{len(CASES) - failed}/{len(CASES)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
