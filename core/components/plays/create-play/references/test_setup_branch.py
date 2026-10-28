#!/usr/bin/env python3
"""test_setup_branch.py — setup_branch.py against a real scratch repo and remote (#731).

    python3 test_setup_branch.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "setup_branch.py")
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


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True).stdout.strip()


def commit(cwd, name):
    with open(os.path.join(cwd, name), "w") as fh:
        fh.write(name)
    git(cwd, "add", name)
    git(cwd, "commit", "-q", "-m", name)


def run(cwd, out, *args):
    p = subprocess.run([sys.executable, SCRIPT, *args, "--out", out], cwd=cwd, capture_output=True, text=True)
    return p.returncode, (json.load(open(out)) if p.returncode == 0 else None)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        origin, work = os.path.join(tmp, "origin.git"), os.path.join(tmp, "work")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", origin])
        subprocess.run(["git", "clone", "-q", origin, work], capture_output=True)
        git(work, "config", "user.email", "t@t"); git(work, "config", "user.name", "t")
        git(work, "checkout", "-q", "-b", "main")
        commit(work, "a"); git(work, "push", "-q", "-u", "origin", "main")
        out = os.path.join(tmp, "b.json")

        rc, r = run(work, out, "--issue", "731", "--branch-name", "plan/717/731-x", "--plan-branch", "plan/717/base")
        main_tip = git(work, "rev-parse", "origin/main")
        check("first issue in a plan: the plan branch is cut from latest main",
              rc == 0 and r["plan_branch_created"] and git(work, "rev-parse", "origin/plan/717/base") == main_tip)
        check("the issue branch is a sub-branch, cut from the plan branch",
              git(work, "branch", "--show-current") == "plan/717/731-x" and r["base_sha"] == main_tip)

        git(work, "checkout", "-q", "main"); commit(work, "b"); git(work, "push", "-q", "origin", "main")
        rc, r = run(work, out, "--issue", "673", "--branch-name", "plan/717/673-y", "--plan-branch", "plan/717/base")
        plan_tip = git(work, "rev-parse", "origin/plan/717/base")
        check("the plan already started: it is not cut again", rc == 0 and not r["plan_branch_created"])
        check("the latest main is merged into the plan branch first",
              subprocess.run(["git", "merge-base", "--is-ancestor", "origin/main", "origin/plan/717/base"], cwd=work).returncode == 0)
        check("the next issue branch is cut from the updated plan branch", r["base_sha"] == plan_tip)

        rc, r = run(work, out, "--issue", "999", "--branch-name", "feature/999-z")
        check("an issue in no plan still branches from main",
              rc == 0 and r["plan_branch"] is None and git(work, "merge-base", "HEAD", "origin/main") == git(work, "rev-parse", "origin/main"))

        rc, r = run(work, out, "--issue", "731", "--branch-name", "plan/717/731-x", "--plan-branch", "plan/717/base")
        check("a re-run resumes the issue branch, with no new branch", rc == 0 and git(work, "branch", "--show-current") == "plan/717/731-x")
        git(work, "checkout", "-q", "main"); commit(work, "c"); git(work, "push", "-q", "origin", "main")
        rc, r = run(work, out, "--issue", "731", "--branch-name", "plan/717/731-x", "--plan-branch", "plan/717/base")
        check("a resume records the plan branch tip as its base, not main's (H4)",
              rc == 0 and r["base_sha"] == git(work, "rev-parse", "origin/plan/717/base")
              and r["base_sha"] != git(work, "rev-parse", "origin/main"))

        # The plan paused: its branch merged into main and was deleted on origin; a stale copy stays here.
        git(work, "checkout", "-q", "main")
        git(work, "push", "-q", "origin", "--delete", "plan/717/base")
        stale = git(work, "rev-parse", "plan/717/base")
        commit(work, "d"); git(work, "push", "-q", "origin", "main")
        rc, r = run(work, out, "--issue", "740", "--branch-name", "plan/717/740-w", "--plan-branch", "plan/717/base")
        check("a plan that starts again gets a fresh cut from main, not the stale local copy (H10)",
              rc == 0 and r["plan_branch_created"]
              and git(work, "rev-parse", "origin/plan/717/base") == git(work, "rev-parse", "origin/main")
              and git(work, "rev-parse", "origin/plan/717/base") != stale)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
