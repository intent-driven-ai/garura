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
MOVE_STEP = "python3 <install-garura>/scripts/migrate_model.py --target <project>"


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
    check(f"{label}: names the script that moves the model", MOVE_STEP in err, err)
    check(f"{label}: does not tell the person to re-install",
          "re-install" not in err.lower() and "reinstall" not in err.lower(), err)
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
    check("lint_grounding names the script that moves the model, not a zero-feature report",
          MOVE_STEP in r.stderr, r.stderr + r.stdout)

print("check_kept and check_sources on an old model")
with tempfile.TemporaryDirectory() as root:
    base = os.path.join(root, "product")
    os.makedirs(os.path.join(base, "product-os"))
    with open(os.path.join(base, "product-os", "_spine.yaml"), "w", encoding="utf-8") as fh:
        fh.write("domains: []\nfunctionalities:\n  - id: f1\n")
    subprocess.run(["git", "-C", root, "init", "-q"], check=True)
    r = subprocess.run([sys.executable, os.path.join(HERE, "check_kept.py"), "--product-base", base,
                        "--base-ref", "HEAD", "--out", os.path.join(root, "kept.json")],
                       capture_output=True, text=True)
    check("check_kept stops on an old spine (exit 2)", r.returncode == 2, f"exit {r.returncode} {r.stderr}")
    check("check_kept names the script that moves the model", MOVE_STEP in r.stderr, r.stderr + r.stdout)
    manifest = os.path.join(root, "enrich-manifest.yaml")
    with open(manifest, "w", encoding="utf-8") as fh:
        fh.write("enrich:\n  capability: {doc: d/c/capability.md}\n  functionalities:\n  - {doc: d/c/f1/f.md}\n")
    caps = os.path.join(HERE, "..", "..", "discover-capabilities", "scripts", "check_sources.py")
    r = subprocess.run([sys.executable, caps, "--manifest", manifest, "--product-base", base,
                        "--out", os.path.join(root, "sources.json")], capture_output=True, text=True)
    check("check_sources stops on an old manifest (exit 2)", r.returncode == 2, f"exit {r.returncode} {r.stderr}")
    check("check_sources names the script that moves the model", MOVE_STEP in r.stderr, r.stderr + r.stdout)

if failures:
    print(f"\n{len(failures)} failed")
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("\nall passed")
