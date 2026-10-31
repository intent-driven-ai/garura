#!/usr/bin/env python3
"""test_setup_branch.py — setup_branch.py against a real scratch repo and remote (#731, #953).

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
        check("a resume records the plan branch tip as its base, not main's",
              rc == 0 and r["base_sha"] == git(work, "rev-parse", "origin/plan/717/base")
              and r["base_sha"] != git(work, "rev-parse", "origin/main"))

        # The plan paused: merge-change merged its branch into main and deleted it on origin;
        # a stale copy stays here, every commit of it on main.
        git(work, "checkout", "-q", "main")
        git(work, "merge", "-q", "--no-ff", "--no-edit", "plan/717/base")
        git(work, "push", "-q", "origin", "main")
        git(work, "push", "-q", "origin", "--delete", "plan/717/base")
        stale = git(work, "rev-parse", "plan/717/base")
        commit(work, "d"); git(work, "push", "-q", "origin", "main")
        rc, r = run(work, out, "--issue", "740", "--branch-name", "plan/717/740-w", "--plan-branch", "plan/717/base")
        check("a plan that starts again gets a fresh cut from main, not the stale local copy",
              rc == 0 and r["plan_branch_created"] and r["stale_plan_branch"] == {"deleted": True, "tip": stale, "on_main": True}
              and git(work, "rev-parse", "origin/plan/717/base") == git(work, "rev-parse", "origin/main")
              and git(work, "rev-parse", "origin/plan/717/base") != stale)

        # A stale copy with a commit found nowhere else is kept, and the run stops.
        git(work, "checkout", "-q", "plan/717/base")
        commit(work, "unpushed")
        lost = git(work, "rev-parse", "plan/717/base")
        git(work, "checkout", "-q", "main")
        git(work, "push", "-q", "origin", "--delete", "plan/717/base")
        p = subprocess.run([sys.executable, SCRIPT, "--issue", "741", "--branch-name", "plan/717/741-v",
                            "--plan-branch", "plan/717/base", "--out", out], cwd=work, capture_output=True, text=True)
        check("a stale copy with unpushed work is kept and the run stops, naming the commit",
              p.returncode == 1 and git(work, "rev-parse", "plan/717/base") == lost and "unpushed" in p.stderr)

        # Pushed, then deleted on origin from another clone without a merge: the commit is on no
        # branch anywhere but here, so the copy is kept.
        git(work, "push", "-q", "origin", "plan/717/base")
        other = os.path.join(tmp, "other")
        subprocess.run(["git", "clone", "-q", origin, other], capture_output=True)
        git(other, "push", "-q", "origin", "--delete", "plan/717/base")
        p = subprocess.run([sys.executable, SCRIPT, "--issue", "742", "--branch-name", "plan/717/742-u",
                            "--plan-branch", "plan/717/base", "--out", out], cwd=work, capture_output=True, text=True)
        check("a copy pushed once but never merged is kept, even after its branch went on origin",
              p.returncode == 1 and git(work, "rev-parse", "plan/717/base") == lost)

        # A push that origin refuses stops the run.
        git(work, "checkout", "-q", "main")
        git(work, "branch", "-q", "-D", "plan/717/base")
        hook = os.path.join(origin, "hooks", "pre-receive")
        with open(hook, "w") as fh:
            fh.write("#!/bin/sh\nwhile read old new ref; do case $ref in refs/heads/plan/*) exit 1;; esac; done\n")
        os.chmod(hook, 0o755)
        p = subprocess.run([sys.executable, SCRIPT, "--issue", "744", "--branch-name", "plan/717/744-s",
                            "--plan-branch", "plan/717/base", "--out", out], cwd=work, capture_output=True, text=True)
        check("a push that origin refuses stops the run and names the branch",
              p.returncode == 1 and "pushing plan/717/base" in p.stderr)
        os.remove(hook)

        # origin cannot be reached: nothing is deleted, and the run says why.
        git(work, "checkout", "-q", "main")
        git(work, "remote", "set-url", "origin", os.path.join(tmp, "gone.git"))
        before = git(work, "rev-parse", "plan/717/base")
        p = subprocess.run([sys.executable, SCRIPT, "--issue", "743", "--branch-name", "plan/717/743-t",
                            "--plan-branch", "plan/717/base", "--out", out], cwd=work, capture_output=True, text=True)
        check("a failed lookup on origin stops the run and deletes nothing",
              p.returncode == 1 and git(work, "rev-parse", "plan/717/base") == before
              and "could not be reached" in p.stderr)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
