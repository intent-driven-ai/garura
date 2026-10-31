#!/usr/bin/env python3
"""test_resolve_plan.py — fixture tests for resolve_plan.py and the branch-name issue reader (#731, #779).

    python3 test_resolve_plan.py
"""
import json
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import preflight  # noqa: E402
import resolve_plan as rp  # noqa: E402

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


def write(d, name, plan):
    with open(os.path.join(d, name), "w") as fh:
        yaml.safe_dump(plan, fh)


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True).stdout.strip()


def put_plan(cwd, plan, message):
    os.makedirs(os.path.join(cwd, "plans"), exist_ok=True)
    write(os.path.join(cwd, "plans"), "40.yaml", plan)
    git(cwd, "add", "plans/40.yaml")
    git(cwd, "commit", "-q", "-m", message)


def lookup(work, issue):
    out = os.path.join(work, "..", "plan.json")
    code = rp.main(["--plans-dir", "plans/", "--issue", str(issue), "--slug", "x", "--repo", work, "--out", out])
    return code, (json.load(open(out)) if code == 0 else None)


def lookup_dir(work, plans_dir, repo):
    out = os.path.join(work, "..", "plan.json")
    code = rp.main(["--plans-dir", plans_dir, "--issue", "77", "--slug", "x", "--repo", repo, "--out", out])
    return code, (json.load(open(out)) if code == 0 else None)


def from_git():
    """#779: the plan is read from main and the plan's own branch on origin, never the checkout."""
    with tempfile.TemporaryDirectory() as tmp:
        origin, work = os.path.join(tmp, "origin.git"), os.path.join(tmp, "work")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", origin])
        subprocess.run(["git", "clone", "-q", origin, work], capture_output=True)
        git(work, "config", "user.email", "t@t")
        git(work, "config", "user.name", "t")
        git(work, "checkout", "-q", "-b", "main")
        put_plan(work, {"id": 40, "tree": [{"issue": 41}]}, "plan 40")
        git(work, "push", "-q", "-u", "origin", "main")
        git(work, "checkout", "-q", "-b", "older-work")                  # the checkout keeps the old file
        git(work, "checkout", "-q", "main")
        put_plan(work, {"id": 40, "tree": [{"issue": 41}, {"issue": 77}]}, "add #77 on main")
        git(work, "push", "-q", "origin", "main")
        git(work, "checkout", "-q", "-b", "plan/40/base")
        put_plan(work, {"id": 40, "tree": [{"issue": 41}, {"issue": 77}, {"issue": 88}]}, "a plan session adds #88")
        git(work, "push", "-q", "-u", "origin", "plan/40/base")
        git(work, "checkout", "-q", "older-work")
        code, r = lookup(work, 77)
        check("an issue added on main is found from a checkout with an older plan file",
              code == 0 and r["plan_id"] == "40" and r["issue_branch"] == "plan/40/77-x" and r["source"]["fetched"])
        code, r = lookup(work, 88)
        check("an issue only on the plan's own branch is found too",
              code == 0 and r["plan_id"] == "40" and r["source"]["plan_branches_read"] == ["plan/40/base"])
        git(work, "remote", "set-url", "origin", os.path.join(tmp, "gone.git"))
        code, r = lookup(work, 77)
        check("with no network the last fetched copies are read, and the record says so",
              code == 0 and r["plan_id"] == "40" and r["source"]["fetched"] is False)
        code, r = lookup(work, 99)
        check("an issue in no plan, read from git, gets feature/<issue>-<slug>",
              code == 0 and r["plan_id"] is None and r["issue_branch"] == "feature/99-x")
        code, r = lookup_dir(work, os.path.join(work, "plans"), work)
        check("an absolute plans folder inside the repository is read the same way", code == 0 and r["plan_id"] == "40")
        sub = os.path.join(work, "sub")
        os.makedirs(sub)
        code, r = lookup_dir(work, "../plans", sub)
        check("a run from a sub-folder reads the same plans", code == 0 and r["plan_id"] == "40")
        check("a plans folder outside the repository is an error, not 'no plan'",
              rp.main(["--plans-dir", tmp, "--issue", "77", "--slug", "x", "--repo", work]) == 2)
        bare = os.path.join(tmp, "bare")
        subprocess.run(["git", "init", "-q", bare])
        check("no origin/main to read from is an error, not a guess",
              rp.main(["--plans-dir", "plans/", "--issue", "77", "--slug", "x", "--repo", bare]) == 2)


def main():
    with tempfile.TemporaryDirectory() as d:
        write(d, "717.yaml", {"id": 717, "tree": [
            {"issue": 721, "children": [{"issue": 731}, {"issue": 673}]},
            {"issue": 718, "children": [{"issue": 727}]}]})
        write(d, "722.yaml", {"id": 722, "tree": [{"issue": 723, "children": [{"issue": 724}]}]})
        r = rp.resolve(rp.plans_on_disk(d), 731, "plan-branches")
        check("an issue in a plan gets a sub-branch of its plan",
              r["plan_branch"] == "plan/717/base" and r["issue_branch"] == "plan/717/731-plan-branches")
        check("a capability in a plan is found too", rp.resolve(rp.plans_on_disk(d), 721, "x")["plan_id"] == "717")
        check("the business intent itself belongs to its own plan", rp.resolve(rp.plans_on_disk(d), 722, "x")["plan_id"] == "722")
        r = rp.resolve(rp.plans_on_disk(d), 999, "one-off")
        check("an issue in no plan gets feature/<issue>-<slug> from main",
              r["plan_id"] is None and r["issue_branch"] == "feature/999-one-off")
        write(d, "800.yaml", {"id": 800, "tree": [{"issue": 731}]})
        check("an issue in two plans is an error, not a guess", rp.main(["--plans-dir", d, "--issue", "731", "--slug", "x", "--local"]) == 2)
        os.remove(os.path.join(d, "800.yaml"))
        check("the command exits 0 for a found issue", rp.main(["--plans-dir", d, "--issue", "724", "--slug", "x", "--local"]) == 0)
    with tempfile.TemporaryDirectory() as d:
        check("an empty plans folder means no plan", rp.resolve(rp.plans_on_disk(d), 5, "x")["plan_id"] is None)
    cfg = {}
    for branch, want in (("feature/731-plan-branches", "731"), ("plan/717/731-plan-branches", "731"),
                         ("plan/717/base", "717"), ("fix/42-typo", "42"), ("main", None)):
        got = preflight.resolve(cfg, "start-change", branch, "")["issue"]
        check(f"pre-flight reads issue {want} from {branch}", got == want)
    check("pre-flight reports the plan files' folder from the settings",
          preflight.resolve({"plans": {"base-path": "work/plans/"}}, "start-change", "main", "")["plans_base"] == "work/plans/")
    check("pre-flight reports the default plan folder when the setting is missing",
          preflight.resolve({}, "start-change", "main", "")["plans_base"] == ".garura/project/plans/")
    import resolve_target as rt
    check("pre-flight and the landing script read the same issue from a plan's own branch",
          preflight.resolve(cfg, "commit-change", "plan/717/base", "")["issue"] == rt.classify("plan/717/base")["issue"])
    from_git()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
