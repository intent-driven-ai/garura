#!/usr/bin/env python3
"""test_scoped_write_guard.py — fixture tests for the shared post-write containment guard.

Builds a throwaway git repo with a product-os tree, makes changes, and checks which ones
the guard calls in scope for each kind of glob: --allow, --add-only, --modify-only,
--remove-only. A move is a removal plus an addition, never a hidden rename. Every play's
stamped copy of scoped_write_guard.py must be identical to this canonical one.

    python3 test_scoped_write_guard.py
"""
import glob
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "scoped_write_guard.py")
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))

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
        if os.environ.get("PYTEST_CURRENT_TEST"):
            raise AssertionError(name)


def sh(cwd, *args):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def make_repo(tmp):
    """A repo with a committed model: one intent page, one holding-folder capability."""
    sh(tmp, "git", "init", "-q")
    sh(tmp, "git", "config", "user.email", "t@example.com")
    sh(tmp, "git", "config", "user.name", "t")
    model = os.path.join(tmp, "product", "product-os")
    write(os.path.join(model, "_spine.yaml"), "domains: []\n")
    write(os.path.join(model, "intents", "guest.md"), "# Guest\n[cap](../capabilities/checkout/capability.md)\n")
    write(os.path.join(model, "capabilities", "checkout", "capability.md"), "# Capability: Checkout\n")
    sh(tmp, "git", "add", "-A")
    sh(tmp, "git", "commit", "-q", "-m", "base")
    return model


def guard(tmp, *flags, stage=False):
    if stage:
        sh(tmp, "git", "add", "-A")
    proc = subprocess.run([sys.executable, GUARD, "--product-base", os.path.join(tmp, "product") + "/",
                           "--base-ref", "HEAD", *flags], cwd=tmp, capture_output=True, text=True)
    return proc.returncode, json.loads(proc.stdout)


def move_checkout(model):
    old = os.path.join(model, "capabilities", "checkout", "capability.md")
    new = os.path.join(model, "commerce", "checkout", "capability.md")
    os.makedirs(os.path.dirname(new), exist_ok=True)
    os.rename(old, new)
    write(os.path.join(model, "intents", "guest.md"), "# Guest\n[cap](../commerce/checkout/capability.md)\n")


PLACE = ["--add-only", "product-os/*/*/capability.md",
         "--remove-only", "product-os/capabilities/*/capability.md",
         "--modify-only", "product-os/intents/*.md"]


def test_a_move_out_of_the_holding_folder():
    for stage in (False, True):
        with tempfile.TemporaryDirectory() as tmp:
            model = make_repo(tmp)
            move_checkout(model)
            rc, rep = guard(tmp, *PLACE, stage=stage)
            when = "staged" if stage else "unstaged"
            check(f"a move out of the holding folder plus a fixed link is in scope ({when})",
                  rc == 0 and rep["ok"] and rep["violations"] == [])
            statuses = {c["path"].split("product-os/")[1]: c["status"] for c in rep["changed"]}
            check(f"the move is seen as a removal plus an addition ({when})",
                  statuses.get("capabilities/checkout/capability.md") == "D"
                  and statuses.get("commerce/checkout/capability.md") == "A")


def test_each_only_kind_admits_one_change():
    with tempfile.TemporaryDirectory() as tmp:
        model = make_repo(tmp)
        write(os.path.join(model, "capabilities", "checkout", "capability.md"), "# Capability: Changed\n")
        rc, rep = guard(tmp, *PLACE)
        check("changing a remove-only path is a violation",
              rc == 1 and rep["violations"][0]["reason"] == "modification of an add-only/remove-only path")
    with tempfile.TemporaryDirectory() as tmp:
        model = make_repo(tmp)
        write(os.path.join(model, "intents", "new.md"), "# New\n")
        rc, rep = guard(tmp, *PLACE)
        check("adding a modify-only path is a violation",
              rc == 1 and rep["violations"][0]["reason"] == "addition of a modify-only path")
    with tempfile.TemporaryDirectory() as tmp:
        model = make_repo(tmp)
        os.remove(os.path.join(model, "intents", "guest.md"))
        rc, rep = guard(tmp, *PLACE)
        check("removing a modify-only path is a violation",
              rc == 1 and rep["violations"][0]["reason"] == "removal of a modify-only path")
    with tempfile.TemporaryDirectory() as tmp:
        model = make_repo(tmp)
        write(os.path.join(model, "_spine.yaml"), "domains: [x]\n")
        rc, rep = guard(tmp, *PLACE)
        check("a path matching no glob is out of scope",
              rc == 1 and rep["violations"][0]["reason"] == "out-of-scope")
        rc, rep = guard(tmp, *PLACE, "--allow", "product-os/_spine.yaml")
        check("--allow admits it", rc == 0 and rep["ok"])


def test_restore_reverts_a_move():
    with tempfile.TemporaryDirectory() as tmp:
        model = make_repo(tmp)
        move_checkout(model)
        rc, rep = guard(tmp, "--restore")
        check("restore with an empty allow set puts a move back",
              rc == 0 and os.path.isfile(os.path.join(model, "capabilities", "checkout", "capability.md"))
              and not os.path.exists(os.path.join(model, "commerce", "checkout", "capability.md")))


def test_every_copy_is_identical():
    mine = open(GUARD, "rb").read()
    copies = glob.glob(os.path.join(REPO, "core", "components", "plays", "*", "scripts", "scoped_write_guard.py"))
    different = [c for c in copies if open(c, "rb").read() != mine]
    check(f"every play's scoped_write_guard.py is identical to the canonical one ({len(copies)} copies)",
          len(copies) >= 14 and not different)


def main():
    for test in (test_a_move_out_of_the_holding_folder, test_each_only_kind_admits_one_change,
                 test_restore_reverts_a_move, test_every_copy_is_identical):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
