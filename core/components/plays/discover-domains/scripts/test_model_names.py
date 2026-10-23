#!/usr/bin/env python3
"""Tests for model_names.py, the guard that stops on a pre-#807 product model (#813).

Plain script: prints one line per check and exits 1 if any check fails.
    python3 test_model_names.py
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
failures = []


def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        failures.append(f"{label}: {detail}")


def guard(kind, yaml_text):
    """Run model_names.check_<kind> on yaml_text in a child process; return (code, stderr)."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "_spine.yaml" if kind == "spine" else "slice.yaml")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(yaml_text)
        code = (
            "import sys, yaml\n"
            f"sys.path.insert(0, {HERE!r})\n"
            "import model_names\n"
            f"p = {path!r}\n"
            f"model_names.check_{kind}(yaml.safe_load(open(p)) or {{}}, p)\n"
            "print('passed')\n"
        )
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        return r.returncode, r.stderr, r.stdout


def stops(label, kind, text, old):
    code, err, _ = guard(kind, text)
    check(f"{label}: exits 2", code == 2, f"exit {code}, stderr {err!r}")
    check(f"{label}: names the old key '{old}'", old in err, err)
    check(f"{label}: names the upgrade step", "upgrade" in err.lower() and "migrate_model" in err, err)
    check(f"{label}: names the file", ("_spine.yaml" if kind == "spine" else "slice.yaml") in err, err)


print("model_names guard")
stops("old spine list", "spine", "features: []\nfunctionalities:\n  - id: f1\n", "functionalities")
stops("old epic refs", "spine", "epics:\n  - id: e1\n    functionality_refs: [f1]\n", "functionality_refs")
stops("old ICE kind", "spine", "ices:\n  - id: i1\n    for_kind: functionality\n", "for_kind: functionality")
stops("old slice record ref", "slice",
      "slice:\n  id: s1\n  features:\n    - functionality_ref: f1\n", "functionality_ref")
stops("old slice record list", "slice", "slice:\n  id: s1\n  functionalities: []\n", "functionalities")

code, err, out = guard("spine",
                       "features:\n  - id: f1\nepics:\n  - id: e1\n    feature_refs: [f1]\n"
                       "ices:\n  - id: i1\n    for_kind: feature\n")
check("new spine passes", code == 0 and "passed" in out, f"exit {code}, stderr {err!r}")
code, err, out = guard("slice", "slice:\n  id: s1\n  features:\n    - feature_ref: f1\n")
check("new slice record passes", code == 0 and "passed" in out, f"exit {code}, stderr {err!r}")
code, err, out = guard("spine", "")
check("empty spine passes", code == 0, f"exit {code}, stderr {err!r}")

print("lint_grounding on an old spine")
with tempfile.TemporaryDirectory() as root:
    spine = os.path.join(root, "_spine.yaml")
    with open(spine, "w", encoding="utf-8") as fh:
        fh.write("domains: []\ncapabilities: []\nfunctionalities:\n  - id: f1\n    doc: d/c/f1/feature.md\n")
    r = subprocess.run([sys.executable, os.path.join(HERE, "lint_grounding.py"),
                        "--root", root, "--spine", spine], capture_output=True, text=True)
    check("lint_grounding exits non-zero", r.returncode != 0, f"exit {r.returncode}")
    check("lint_grounding prints the upgrade step, not a zero-feature report",
          "migrate_model" in r.stderr and "upgrade" in r.stderr.lower(), r.stderr + r.stdout)

if failures:
    print(f"\n{len(failures)} failed")
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("\nall passed")
