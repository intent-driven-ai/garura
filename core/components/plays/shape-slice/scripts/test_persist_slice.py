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
    sl = {"id": "sl-self-booking", "slug": "self-booking", "feature_refs": ["ft-1", "ft-2"],
          "vertical": "the booking screen", "intents": ["bi-340"],
          "surface": {"name": "the booking screen", "persona_ref": "patient",
                      "user_action": "books a free slot"}}
    sl.update(over)
    for k, v in list(sl.items()):
        if v is None:
            del sl[k]
    path = os.path.join(root, "slice.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(sl, fh)
    return path


def run(root, spine, sl):
    p = subprocess.run([sys.executable, SCRIPT, "--root", root, "--spine", spine, "--slice", sl],
                       capture_output=True, text=True)
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


def refused(name, **over):
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        sp = model(root)
        before = snapshot(root)
        code, out, err = run(root, sp, slice_file(tmp, **over))
        check(f"refused: {name} (exit 2)", code == 2 and out is not None and out["ok"] is False)
        check(f"refused: {name} — a plain message", bool(err.strip()))
        check(f"refused: {name} — nothing written", snapshot(root) == before)


def main():
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
        check("the record holds the surface with its persona_ref",
              rec.get("slice", {}).get("surface", {}).get("persona_ref") == "patient")
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

    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        sp = model(root)
        code, out, _ = run(root, sp, slice_file(tmp, surface=[{"name": "the booking screen",
                                                                  "persona_ref": "patient"}]))
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
