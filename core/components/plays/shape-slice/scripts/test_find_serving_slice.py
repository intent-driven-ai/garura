#!/usr/bin/env python3
"""test_find_serving_slice.py — a slice that already serves the intent is found (#795, C7).

    python3 core/components/plays/shape-slice/scripts/test_find_serving_slice.py
"""
import json
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "find_serving_slice.py")

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


def run(*args):
    p = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)
    out = json.loads(p.stdout) if p.returncode == 0 and p.stdout.strip() else None
    return p.returncode, out, p.stderr


def spine_file(root, data, name="_spine.yaml"):
    path = os.path.join(root, name)
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh)
    return path


SPINE = {"slices": [
    {"id": "sl-a", "slug": "a", "feature_refs": ["ft-1", "ft-2"], "vertical": "the booking screen",
     "intents": ["bi-10"]},
    {"id": "sl-b", "slug": "b", "feature_refs": ["ft-3"], "vertical": "the checkout",
     "intents": ["bi-20", "bi-30"]},
]}


def main():
    with tempfile.TemporaryDirectory() as root:
        sp = spine_file(root, SPINE)

        code, out, _ = run("--spine", sp, "--intent", "bi-30")
        check("a slice that lists the intent is a match", code == 0 and out["match"] == "sl-b")
        check("the reason says it lists the intent", out is not None and "lists" in out["reason"])

        code, out, _ = run("--spine", sp, "--intent", "bi-99")
        check("no slice lists the intent: match is null", code == 0 and out["match"] is None)
        check("a null match still has a reason", out is not None and out["reason"])

        code, out, _ = run("--spine", sp, "--intent", "bi-99", "--features", "ft-1,ft-2",
                           "--surface", "the booking screen")
        check("same features in the same order and the same surface is a match",
              code == 0 and out["match"] == "sl-a")
        check("the reason names the same features and surface",
              out is not None and "same features" in out["reason"])

        code, out, _ = run("--spine", sp, "--intent", "bi-99", "--features", "ft-2,ft-1",
                           "--surface", "the booking screen")
        check("the same features in another order is no match", code == 0 and out["match"] is None)

        code, out, _ = run("--spine", sp, "--intent", "bi-99", "--features", "ft-1",
                           "--surface", "the booking screen")
        check("a different feature set is no match", code == 0 and out["match"] is None)

        code, out, _ = run("--spine", sp, "--intent", "bi-99", "--features", "ft-1,ft-2",
                           "--surface", "the mobile app")
        check("the same features on another surface is no match", code == 0 and out["match"] is None)

        code, out, _ = run("--spine", sp, "--intent", "bi-10", "--features", "ft-3",
                           "--surface", "the checkout")
        check("a slice that lists the intent wins over a feature match",
              code == 0 and out["match"] == "sl-a")

        code, out, _ = run("--spine", sp, "--intent", "bi-99", "--features", "ft-1,ft-2")
        check("--features without --surface is a usage error", code == 2)

        shaped = os.path.join(root, "slice.json")
        with open(shaped, "w", encoding="utf-8") as fh:
            json.dump({"id": "sl-new", "slug": "new", "feature_refs": ["ft-1", "ft-2"]}, fh)
        code, out, _ = run("--spine", sp, "--intent", "bi-99", "--features", "ft-1,ft-2",
                           "--surface", "the booking screen")
        check("a match gives the persist_slice reuse arguments (--reuse <id>)",
              code == 0 and out["reuse_args"] == ["--reuse", "sl-a"])
        with open(shaped, encoding="utf-8") as fh:
            got = json.load(fh)
        check("the serving check never changes the shaped slice.json", got["id"] == "sl-new")
        code, out, _ = run("--spine", sp, "--intent", "bi-99")
        check("no match gives no reuse arguments", code == 0 and out["reuse_args"] == [])
        code, out, err = run("--spine", sp, "--intent", "bi-99", "--reuse-into", shaped)
        check("the old --reuse-into flag is gone (usage error)", code == 2)

        empty = spine_file(root, {"domains": []}, "empty.yaml")
        code, out, _ = run("--spine", empty, "--intent", "bi-10")
        check("a spine with no slices gives no match", code == 0 and out["match"] is None)

        old = spine_file(root, {"functionalities": [{"id": "f"}], "slices": []}, "old.yaml")
        code, out, err = run("--spine", old, "--intent", "bi-10")
        check("an old-name spine stops (model_names guard)", code == 2 and "functionalities" in err)

        code, out, _ = run("--spine", os.path.join(root, "missing.yaml"), "--intent", "bi-10")
        check("a missing spine is a usage error", code == 2)

        busy = spine_file(root, dict(SPINE, epics=[{"id": "ep-a", "slice_ref": "sl-a",
                                                    "status": "in_delivery"},
                                                   {"id": "ep-b", "slice_ref": "sl-b",
                                                    "status": "ready"}]), "busy.yaml")
        code, out, _ = run("--spine", busy, "--intent", "bi-10")
        check("a slice in progress (its epic past ready) is never a match",
              code == 0 and out["match"] is None and out["reuse_args"] == []
              and "in progress" in out["reason"])
        check("the result names the slices in progress", out["in_progress"] == ["sl-a"])
        code, out, _ = run("--spine", busy, "--intent", "bi-20")
        check("a slice whose epic is only ready is still a match",
              code == 0 and out["match"] == "sl-b" and out["in_progress"] == ["sl-a"])
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
