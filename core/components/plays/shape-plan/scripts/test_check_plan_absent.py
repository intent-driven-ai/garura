#!/usr/bin/env python3
"""test_check_plan_absent.py — check_plan_absent.py: /shape-plan stops when the intent already has a plan (#896, C14).

    python3 test_check_plan_absent.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import check, finish, run  # noqa: E402


def git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


def repo_with(tmp, plan_on_main=False):
    repo = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(repo, "plans"))
    git(repo, "init", "--quiet", "-b", "main")
    git(repo, "config", "user.name", "Test")
    git(repo, "config", "user.email", "test@example.com")
    with open(os.path.join(repo, "README"), "w") as fh:
        fh.write("x\n")
    if plan_on_main:
        with open(os.path.join(repo, "plans", "788.yaml"), "w") as fh:
            fh.write("id: 788\ntitle: x\nstatus: In Progress\ntree: []\n")
    git(repo, "add", ".")
    git(repo, "commit", "--quiet", "-m", "start")
    return repo


def absent(repo, plan="788"):
    out = os.path.join(repo, "..", "rec.json")
    code, _, _ = run("check_plan_absent.py", "--plans-dir", "plans", "--plan", plan, "--repo", repo, "--out", out)
    rec = json.load(open(out)) if os.path.isfile(out) else None
    return code, rec


def main():
    print("check_plan_absent.py")
    with tempfile.TemporaryDirectory() as tmp:
        repo = repo_with(tmp)
        code, rec = absent(repo)
        check("no plan file anywhere: go on (exit 0)", code == 0 and rec["exists"] is False and rec["message"] is None)
    with tempfile.TemporaryDirectory() as tmp:
        repo = repo_with(tmp, plan_on_main=True)
        code, rec = absent(repo)
        check("a plan file on main and in the checkout: stop (exit 3) and name /update-plan",
              code == 3 and rec["where"] == ["checkout", "main"] and "/update-plan 788" in rec["message"])
    with tempfile.TemporaryDirectory() as tmp:
        repo = repo_with(tmp, plan_on_main=True)
        git(repo, "checkout", "--quiet", "-b", "feature/1-x", "HEAD~0")
        os.remove(os.path.join(repo, "plans", "788.yaml"))
        git(repo, "commit", "--quiet", "-am", "a branch without the plan file")
        code, rec = absent(repo)
        check("on a branch without the file, the plan on main still stops it",
              code == 3 and rec["where"] == ["main"])
    with tempfile.TemporaryDirectory() as tmp:
        repo = repo_with(tmp)
        with open(os.path.join(repo, "plans", "788.yaml"), "w") as fh:
            fh.write("id: 788\n")
        code, rec = absent(repo)
        check("a plan file only in the checkout still stops it", code == 3 and rec["where"] == ["checkout"])
        code, rec = absent(repo, plan="7x8")
        check("a plan ID that is not digits is refused (exit 2), nothing written", code == 2)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
