#!/usr/bin/env python3
"""test_persist_slice.py — the slice is written to the spine and its record (#795, C6, C7, C9).

    python3 core/components/plays/shape-slice/scripts/test_persist_slice.py
"""
import json
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "persist_slice.py")
LINT = os.path.join(HERE, "lint_grounding.py")

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


def model(root, extra=None):
    os.makedirs(root, exist_ok=True)
    spine = {"features": [{"id": "ft-1"}, {"id": "ft-2"}, {"id": "ft-3"}], "slices": []}
    spine.update(extra or {})
    path = os.path.join(root, "_spine.yaml")
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(spine, fh, sort_keys=False)
    return path


def slice_file(root, **over):
    sl = {"id": "sl-self-booking", "slug": "self-booking", "name": "Self booking",
          "outcome": "A patient books a visit with no phone call.",
          "feature_refs": ["ft-1", "ft-2"],
          "vertical": "the booking screen", "intents": ["bi-340"],
          "surface": {"id": "sf-booking", "name": "the booking screen", "persona_ref": "patient",
                      "user_action": "books a free slot"}}
    sl.update(over)
    for k, v in list(sl.items()):
        if v is None:
            del sl[k]
    path = os.path.join(root, "slice.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(sl, fh)
    return path


def run(root, spine, sl, *extra):
    p = subprocess.run([sys.executable, SCRIPT, "--root", root, "--spine", spine, "--slice", sl,
                        *extra], capture_output=True, text=True)
    out = json.loads(p.stdout) if p.stdout.strip() else None
    return p.returncode, out, p.stderr


def slice_errors(root, spine):
    """The linter's errors about spine slices (the fixture has no feature docs, so other
    errors are expected and ignored here)."""
    p = subprocess.run([sys.executable, LINT, "--root", root, "--spine", spine],
                       capture_output=True, text=True)
    out = json.loads(p.stdout)
    return [e for e in out.get("errors", []) if e.startswith("spine slice")]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def snapshot(root):
    files = {}
    for here, _d, names in os.walk(root):
        for n in names:
            if n == "slice.json":
                continue
            p = os.path.join(here, n)
            with open(p, encoding="utf-8") as fh:
                files[os.path.relpath(p, root)] = fh.read()
    return files


def refused(label, **over):
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        sp = model(root)
        before = snapshot(root)
        code, out, err = run(root, sp, slice_file(tmp, **over))
        check(f"refused: {label} (exit 2)", code == 2 and out is not None and out["ok"] is False)
        check(f"refused: {label} — a plain message", bool(err.strip()))
        check(f"refused: {label} — nothing written", snapshot(root) == before)


def test_reuse():
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        sp = model(root)
        run(root, sp, slice_file(tmp))
        os.makedirs(os.path.join(root, "intents"), exist_ok=True)
        rec_path = os.path.join(root, "slices", "sl-self-booking.yaml")
        rec_before = load(rec_path)
        shaped = slice_file(tmp, id="sl-new", slug="new", feature_refs=["ft-1", "ft-3"],
                            vertical="the mobile app", intents=["bi-77"],
                            surface={"id": "sf-app", "name": "the mobile app",
                                     "persona_ref": "nurse", "user_action": "checks a slot"})
        code, out, err = run(root, sp, shaped, "--reuse", "sl-self-booking")
        spine = load(sp)
        entry = spine["slices"][0]
        rec = load(rec_path)
        check("reuse: exit 0, no second slice", code == 0 and len(spine["slices"]) == 1, )
        check("reuse: the intent is appended to the existing slice",
              entry["intents"] == ["bi-340", "bi-77"] and out["added_intents"] == ["bi-77"])
        check("reuse: the existing slice keeps its features and vertical",
              entry["feature_refs"] == ["ft-1", "ft-2"] and entry["vertical"] == "the booking screen")
        check("reuse: the record gets the intent and keeps its surface",
              rec["slice"]["intents"] == ["bi-340", "bi-77"]
              and rec["surface"] == rec_before["surface"]
              and rec["slice"]["feature_refs"] == ["ft-1", "ft-2"])
        check("reuse: no record is written for the shaped id",
              not os.path.exists(os.path.join(root, "slices", "sl-new.yaml")))
        diffs = " ".join(out.get("differences") or [])
        check("reuse: the result lists how the new shape differs",
              "differ" in diffs and "ft-3" in diffs and "the mobile app" in diffs
              and "nurse" in diffs)
        check("reuse: a shape for another intent leaves the record's tester action as it was, and says so",
              rec["surface"]["user_action"] == "books a free slot"
              and "tester's action differs" in diffs and "the record keeps its text" in diffs)
        check("reuse: the result says it reused", out["reused"] is True and out["id"] == "sl-self-booking")
        code, out, _ = run(root, sp, shaped, "--reuse", "sl-self-booking")
        check("reuse: a second run adds no duplicate intent",
              code == 0 and load(sp)["slices"][0]["intents"] == ["bi-340", "bi-77"]
              and load(rec_path)["slice"]["intents"] == ["bi-340", "bi-77"]
              and out["action"] == "unchanged")
        code, out, _ = run(root, sp, shaped, "--reuse", "sl-missing")
        check("reuse: a slice not in the spine is refused", code == 2)
        code, out, _ = run(root, sp, shaped, "--reuse", "../x")
        check("reuse: a reuse id that leaves the model folder is refused", code == 2)

    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        old = {"id": "sl-old", "slug": "old", "status": "realized", "feature_refs": ["ft-1"],
               "vertical": "the booking screen", "intents": ["bi-1"], "order": 2}
        sp = model(root, {"slices": [old]})
        code, out, _ = run(root, sp, slice_file(tmp, intents=["bi-2"]), "--reuse", "sl-old")
        entry = load(sp)["slices"][0]
        check("reuse: an older entry is written back with the six fields only",
              code == 0 and list(entry) == ["id", "slug", "feature_refs", "vertical", "intents",
                                            "record"]
              and set(out["dropped_fields"]) == {"status", "order"})
        rec = load(os.path.join(root, "slices", "sl-old.yaml"))
        check("reuse: a missing record is written from the existing slice (same surface)",
              rec["slice"]["feature_refs"] == ["ft-1"] and rec["slice"]["intents"] == ["bi-1", "bi-2"]
              and rec["surface"]["persona_ref"] == "patient")


def test_rerun_same_result():
    """A step run twice with the same input gives the same result: a second run never takes text
    the first run kept, because the new intent is read from the spine at the run's start (C7)."""
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        kept = {"id": "sl-old", "slug": "old", "feature_refs": ["ft-1", "ft-3"],
                "vertical": "the booking screen", "intents": ["bi-10"], "record": "slices/sl-old.yaml"}
        sp = model(root, {"features": [{"id": "ft-1"}, {"id": "ft-3"}], "slices": [kept]})
        os.makedirs(os.path.join(root, "slices"))
        with open(os.path.join(root, "slices", "sl-old.yaml"), "w", encoding="utf-8") as fh:
            yaml.safe_dump({"slice": {"id": "sl-old", "slug": "old", "name": "Old", "outcome": "x",
                                      "feature_refs": ["ft-1", "ft-3"], "vertical": "the booking screen",
                                      "intents": ["bi-10"]},
                            "surface": {"id": "sf-booking", "name": "the booking screen",
                                        "persona_ref": "patient", "user_action": "books"}}, fh)
        start = os.path.join(tmp, "spine-at-start.yaml")
        with open(sp, encoding="utf-8") as fh, open(start, "w", encoding="utf-8") as out_fh:
            out_fh.write(fh.read())
        shaped = slice_file(tmp, feature_refs=["ft-1", "ft-3"], intents=["bi-20"], name="New name",
                            surface={"id": "sf-booking", "name": "the booking screen",
                                     "persona_ref": "patient", "user_action": "books"})
        names = []
        for _ in range(2):
            code, out, _ = run(root, sp, shaped, "--reuse", "sl-old", "--spine-at-start", start,
                               "--at", "2026-10-27")
            names.append((code, load(os.path.join(root, "slices", "sl-old.yaml"))["slice"]["name"],
                          out["replaced"]))
        check("re-run: a run that adds an intent keeps the kept slice's name, the first time and the second",
              names == [(0, "Old", []), (0, "Old", [])])
        check("re-run: neither run writes a history line",
              "edits" not in load(os.path.join(root, "slices", "sl-old.yaml")))


def test_atomic():
    sys.path.insert(0, HERE)
    import persist_slice as ps
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "_spine.yaml")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("slices: []\n")
        real = ps.os.replace
        calls = []

        def boom(src, dst):
            calls.append((src, dst))
            raise OSError("disk full")
        ps.os.replace = boom
        try:
            try:
                ps.atomic_dump(path, {"slices": [{"id": "x"}]})
            except OSError:
                pass
        finally:
            ps.os.replace = real
        with open(path, encoding="utf-8") as fh:
            kept = fh.read()
        check("atomic: the spine is written through a temp file and os.replace",
              len(calls) == 1 and calls[0][1] == path)
        check("atomic: a failed replace leaves the old spine whole and no temp file",
              kept == "slices: []\n" and os.listdir(tmp) == ["_spine.yaml"])


def test_round2():
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        sp = model(root)
        legacy = {"id": "sl-old", "slug": "old", "status": "built", "feature_refs": ["ft-1"],
                  "vertical": "the booking screen", "intents": ["bi-339"]}
        with open(sp, "w", encoding="utf-8") as fh:
            fh.write("# The clinic spine. Keep this note.\n")
            yaml.safe_dump({"features": [{"id": "ft-1"}, {"id": "ft-2"}], "slices": [legacy]}, fh,
                           sort_keys=False)
        rec = os.path.join(root, "slices", "sl-old.yaml")
        os.makedirs(os.path.dirname(rec))
        with open(rec, "w", encoding="utf-8") as fh:
            yaml.safe_dump({"slice": {"id": "sl-old", "slug": "old", "intents": ["bi-339"],
                                      "surface": {"id": "sf-booking", "name": "the booking screen",
                                                  "persona_ref": "patient"}}}, fh)
        code, out, err = run(root, sp, slice_file(tmp), "--reuse", "sl-old")
        got = load(rec)
        check("pre-v2 record: reuse brings it to v2 (exit 0, the fields it set are named)",
              code == 0 and "slice.name" in out["upgraded_to_v2"]
              and "surface.user_action" in out["upgraded_to_v2"])
        check("pre-v2 record: the surface moves to the top level, filled from the shaped surface",
              "surface" not in got["slice"] and got["surface"]["user_action"] == "books a free slot"
              and got["slice"]["name"] == "Self booking")
        chk = os.path.join(tmp, "check.json")
        subprocess.run([sys.executable, os.path.join(os.path.dirname(SCRIPT), "slice_check.py"),
                        "--root", root, "--spine", sp, "--slice-id", "sl-old", "--intent", "bi-340",
                        "--out", chk], capture_output=True, text=True)
        with open(chk, encoding="utf-8") as fh:
            problems = [x for x in json.load(fh)["problems"] if x.startswith("slice '")]
        check("pre-v2 record: the reused slice has no problem in the slice check", problems == [])
        with open(sp, encoding="utf-8") as fh:
            check("the spine keeps its comments after a write", "Keep this note." in fh.read())
        with open(rec, "w", encoding="utf-8") as fh:
            yaml.safe_dump({"slice": {"id": "sl-old", "slug": "old", "intents": ["bi-339"]}}, fh)
        before = snapshot(root)
        code, _, err = run(root, sp, slice_file(tmp, vertical="the command line",
                                                surface={"id": "sf-cli", "name": "the command line",
                                                         "persona_ref": "clerk", "user_action": "runs"}),
                           "--reuse", "sl-old")
        check("pre-v2 record with no surface and another shaped surface is refused, nothing written",
              code == 2 and "before slice.yaml v2" in err and snapshot(root) == before)


def test_change_reused():
    """A slice in use may pull a feature in or push one out; a slice in progress is never touched."""
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        kept = {"id": "sl-old", "slug": "old", "feature_refs": ["ft-1", "ft-3"],
                "vertical": "the booking screen", "intents": ["bi-10"], "record": "slices/sl-old.yaml"}
        sp = model(root, {"features": [{"id": "ft-1"}, {"id": "ft-2"}, {"id": "ft-3"}, {"id": "ft-4"}],
                          "slices": [kept],
                          "epics": [{"id": "ep-old", "slice_ref": "sl-old", "status": "ready"}]})
        os.makedirs(os.path.join(root, "slices"))
        with open(os.path.join(root, "slices", "sl-old.yaml"), "w", encoding="utf-8") as fh:
            yaml.safe_dump({"slice": {"id": "sl-old", "slug": "old", "name": "Old", "outcome": "x",
                                      "feature_refs": ["ft-1", "ft-3"], "vertical": "the booking screen",
                                      "intents": ["bi-10"]},
                            "surface": {"id": "sf-booking", "name": "the booking screen",
                                        "persona_ref": "patient", "user_action": "books"}}, fh)
        shaped = slice_file(tmp, feature_refs=["ft-1", "ft-2", "ft-3"])
        code, out, _ = run(root, sp, shaped, "--reuse", "sl-old", "--pull-in", "ft-2")
        entry = load(sp)["slices"][0]
        rec = load(os.path.join(root, "slices", "sl-old.yaml"))
        check("pull-in: the feature takes its place in the shaped order",
              code == 0 and entry["feature_refs"] == ["ft-1", "ft-2", "ft-3"]
              and rec["slice"]["feature_refs"] == ["ft-1", "ft-2", "ft-3"])
        check("pull-in: the result names it, and the slice keeps its surface and tester",
              out["pulled_in"] == ["ft-2"] and out["pushed_out"] == []
              and entry["vertical"] == "the booking screen" and rec["surface"]["persona_ref"] == "patient")
        reshaped = slice_file(tmp, feature_refs=["ft-1", "ft-2", "ft-3"], intents=["bi-10"],
                              outcome="A patient books a visit and gets a reminder.",
                              surface={"id": "sf-booking", "name": "the booking screen",
                                       "persona_ref": "patient", "user_action": "books, then reads the reminder"})
        start = os.path.join(tmp, "spine-at-start.yaml")
        with open(sp, encoding="utf-8") as fh, open(start, "w", encoding="utf-8") as out_fh:
            out_fh.write(fh.read())
        before = snapshot(root)
        code, _, err = run(root, sp, reshaped, "--reuse", "sl-old", "--at", "2026-10-27")
        check("reshape: a run that would take new text with no start copy is refused, nothing written",
              code == 2 and "--spine-at-start" in err and snapshot(root) == before)
        code, _, err = run(root, sp, reshaped, "--reuse", "sl-old", "--spine-at-start", start)
        check("reshape: taking a kept slice's new text without --at is refused, nothing written (C7)",
              code == 2 and "--at" in err and snapshot(root) == before)
        for bad in ("banana", " ", "2026-13-01", "27-10-2026"):
            code, _, err = run(root, sp, reshaped, "--reuse", "sl-old", "--spine-at-start", start,
                               "--at", bad)
            check(f"reshape: --at {bad!r} is not a date, refused, nothing written",
                  code == 2 and "not a date" in err and snapshot(root) == before)
        code, out, _ = run(root, sp, reshaped, "--reuse", "sl-old", "--spine-at-start", start,
                           "--at", "2026-10-27")
        rec = load(os.path.join(root, "slices", "sl-old.yaml"))
        diffs = " ".join(out.get("differences") or [])
        check("reshape: the record keeps a history line naming what a shaping run took (C7)",
              rec["edits"][-1]["by"] == "a shaping run" and rec["edits"][-1]["at"] == "2026-10-27"
              and rec["edits"][-1]["changed"] == ["slice.name", "slice.outcome", "surface.user_action"]
              and list(rec)[-1] == "edits")
        check("reshape: the result names the parts taken and the slice's epic as out of date",
              out["replaced"] == ["slice.name", "slice.outcome", "surface.user_action"]
              and out["out_of_date"] == [{"id": "ep-old", "status": "ready"}])
        check("reshape for an intent it serves: the record takes the new outcome and tester action",
              code == 0 and rec["slice"]["outcome"] == "A patient books a visit and gets a reminder."
              and rec["surface"]["user_action"] == "books, then reads the reminder"
              and out["action"] == "updated")
        check("reshape: the result lists both differences for the brief",
              "outcome differs" in diffs and "tester's action differs" in diffs
              and "the record takes the new text" in diffs)
        renamed = slice_file(tmp, feature_refs=["ft-1", "ft-2", "ft-3"], intents=["bi-10"],
                             name="A patient books a visit online",
                             outcome="A patient books a visit and gets a reminder.",
                             surface={"id": "sf-booking", "name": "the booking screen",
                                      "persona_ref": "patient", "user_action": "books, then reads the reminder"})
        code, out, _ = run(root, sp, renamed, "--reuse", "sl-old", "--spine-at-start", start,
                           "--at", "2026-10-28")
        rec = load(os.path.join(root, "slices", "sl-old.yaml"))
        diffs = " ".join(out.get("differences") or [])
        check("reshape: the record takes the new name, and the result lists it for the brief",
              code == 0 and rec["slice"]["name"] == "A patient books a visit online"
              and "name differs" in diffs and "outcome differs" not in diffs)
        check("reshape: a second run adds a second history line and keeps the first",
              [e["changed"] for e in rec["edits"]] == [["slice.name", "slice.outcome", "surface.user_action"],
                                                        ["slice.name"]])
        code, out, _ = run(root, sp, renamed, "--reuse", "sl-old", "--spine-at-start", start)
        check("reshape: a run that takes no new text needs no --at and adds no history line",
              code == 0 and out["replaced"] == [] and out["out_of_date"] == []
              and len(load(os.path.join(root, "slices", "sl-old.yaml"))["edits"]) == 2)
        code, out, _ = run(root, sp, shaped, "--reuse", "sl-old", "--push-out", "ft-3")
        check("push-out: the feature leaves the slice",
              code == 0 and load(sp)["slices"][0]["feature_refs"] == ["ft-1", "ft-2"]
              and out["pushed_out"] == ["ft-3"])
        before = snapshot(root)
        code, _, err = run(root, sp, shaped, "--reuse", "sl-old", "--push-out", "ft-1",
                           "--push-out", "ft-2")
        check("push-out: a slice left with no feature is refused, nothing written",
              code == 2 and "no feature" in err and snapshot(root) == before)
        code, _, err = run(root, sp, shaped, "--reuse", "sl-old", "--pull-in", "ft-9")
        check("pull-in: a feature not in the spine is refused", code == 2 and "not in the spine" in err)
        code, _, err = run(root, sp, shaped, "--pull-in", "ft-4")
        check("pull-in without --reuse is refused", code == 2 and "--reuse" in err)
        busy = load(sp)
        busy["epics"] = [{"id": "ep-old", "slice_ref": "sl-old", "status": "validated"}]
        with open(sp, "w", encoding="utf-8") as fh:
            yaml.safe_dump(busy, fh, sort_keys=False)
        before = snapshot(root)
        code, _, err = run(root, sp, shaped, "--reuse", "sl-old")
        check("a slice in progress is never reused, nothing written",
              code == 2 and "in progress" in err and snapshot(root) == before)
        code, _, err = run(root, sp, slice_file(tmp, id="sl-old", slug="old",
                                                feature_refs=["ft-1", "ft-2"]))
        check("a new slice with the id of a slice in progress is refused",
              code == 2 and "in progress" in err)


def main():
    test_change_reused()
    test_rerun_same_result()
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        sp = model(root)
        code, out, _ = run(root, sp, slice_file(tmp))
        spine = load(sp)
        entry = spine["slices"][0] if spine["slices"] else {}
        check("a new slice is written (exit 0, created)", code == 0 and out["action"] == "created")
        check("the spine entry holds exactly id, slug, feature_refs, vertical, intents, record",
              list(entry) == ["id", "slug", "feature_refs", "vertical", "intents", "record"])
        check("record points to slices/<id>.yaml, relative to the product-os folder",
              entry.get("record") == "slices/sl-self-booking.yaml")
        check("no status, order, effort, depends_on or domain_ref",
              not any(k in entry for k in ("status", "order", "effort", "depends_on", "domain_ref")))
        check("features keep their build order", entry.get("feature_refs") == ["ft-1", "ft-2"])
        check("the intent is in intents", entry.get("intents") == ["bi-340"])
        rec_path = os.path.join(root, "slices", "sl-self-booking.yaml")
        rec = load(rec_path) if os.path.isfile(rec_path) else {}
        check("the record is at slices/<id>.yaml", os.path.isfile(rec_path))
        check("the record holds the top-level surface {id, name, persona_ref, user_action}",
              rec.get("surface") == {"id": "sf-booking", "name": "the booking screen",
                                     "persona_ref": "patient", "user_action": "books a free slot"})
        check("the record's slice holds id, slug, name, outcome, feature_refs, vertical, intents",
              list(rec.get("slice", {})) == ["id", "slug", "name", "outcome", "feature_refs",
                                             "vertical", "intents"]
              and rec["slice"]["name"] == "Self booking" and rec["slice"]["intents"] == ["bi-340"])
        check("no temp file is left beside the spine or the record",
              not [n for d in (root, os.path.join(root, "slices")) for n in os.listdir(d)
                   if n.endswith(".tmp")])
        os.makedirs(os.path.join(root, "intents"), exist_ok=True)
        for bi in ("bi-340", "bi-51"):
            with open(os.path.join(root, "intents", f"{bi}.md"), "w", encoding="utf-8") as fh:
                fh.write(f"# {bi}\n")
        check("the grounding linter accepts the record pointer", slice_errors(root, sp) == [])

        code, out, _ = run(root, sp, slice_file(tmp, intents=["bi-340", "bi-51"]))
        spine = load(sp)
        check("an existing id makes no second entry", code == 0 and len(spine["slices"]) == 1)
        check("an existing id gets the new intent appended, order kept",
              spine["slices"][0]["intents"] == ["bi-340", "bi-51"])
        check("the result says updated and names the added intent",
              out["action"] == "updated" and out["added_intents"] == ["bi-51"])
        check("the record's intents get the new intent too",
              load(rec_path)["slice"]["intents"] == ["bi-340", "bi-51"])

        code, out, _ = run(root, sp, slice_file(tmp, intents=["bi-51"]))
        spine = load(sp)
        check("an intent already listed is not added twice",
              code == 0 and spine["slices"][0]["intents"] == ["bi-340", "bi-51"]
              and out["action"] == "unchanged")

        code, out, _ = run(root, sp, slice_file(tmp, feature_refs=["ft-2", "ft-1"]))
        check("an existing id with other features is refused", code == 2)

        os.remove(rec_path)
        check("the linter flags a record pointer whose file is gone",
              any("record not found" in e for e in slice_errors(root, sp)))

    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        old = {"id": "sl-self-booking", "slug": "self-booking", "feature_refs": ["ft-1", "ft-2"],
               "vertical": "the booking screen", "intents": ["bi-340"]}
        sp = model(root, {"slices": [old]})
        code, out, _ = run(root, sp, slice_file(tmp))
        spine = load(sp)
        check("an older entry with no record pointer gets one (updated)",
              code == 0 and out["action"] == "updated"
              and spine["slices"][0].get("record") == "slices/sl-self-booking.yaml")
        check("that run also writes the missing record file",
              os.path.isfile(os.path.join(root, "slices", "sl-self-booking.yaml")))

    refused("no vertical", vertical="")
    refused("no surface", surface=None)
    refused("a surface with no name", surface={"persona_ref": "patient"})
    refused("no persona_ref", surface={"name": "the booking screen"})
    refused("more than one surface", surface=[{"name": "a", "persona_ref": "p"},
                                              {"name": "b", "persona_ref": "p"}])
    refused("no features", feature_refs=[])
    refused("no intents", intents=[])
    refused("a feature not in the spine", feature_refs=["ft-1", "ft-9"])
    refused("no name", name="")
    refused("no outcome", outcome=None)
    refused("a surface with no id", surface={"name": "the booking screen", "persona_ref": "patient",
                                             "user_action": "books"})
    refused("a surface with no user_action", surface={"id": "sf", "name": "the booking screen",
                                                      "persona_ref": "patient"})
    refused("an id with '..' (leaves the model folder)", id="../escape")
    refused("an id with a path in it", id="x/y")
    refused("an absolute id", id="/tmp/escape")

    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        sp = model(root)
        outside = os.path.join(tmp, "outside")
        os.makedirs(outside)
        os.symlink(outside, os.path.join(root, "slices"))
        before = snapshot(root)
        code, out, err = run(root, sp, slice_file(tmp))
        check("refused: a slices folder that links outside the model (exit 2)",
              code == 2 and "leaves the model folder" in err)
        check("refused: the symlink case writes nothing", snapshot(root) == before
              and os.listdir(outside) == [])

    test_reuse()
    test_atomic()
    test_round2()

    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        sp = model(root)
        code, out, _ = run(root, sp, slice_file(tmp, surface=[{"id": "sf-booking", "name": "the booking screen",
                                                                  "persona_ref": "patient",
                                                                  "user_action": "books"}]))
        check("a list with exactly one surface is accepted", code == 0 and out["ok"] is True)

    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        sp = model(root, {"functionalities": [{"id": "x"}]})
        code, out, err = run(root, sp, slice_file(tmp))
        check("an old-name spine stops (model_names guard)", code == 2 and "functionalities" in err)
        check("the old-name spine writes no record",
              not os.path.exists(os.path.join(root, "slices")))
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
