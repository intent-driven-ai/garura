#!/usr/bin/env python3
"""
plan_land.py — get a plan's branch ready to land on main, and check it before the merge (#991).

The plan's branch is the only place a plan changes. When it lands on main, main's plan file
becomes the branch's plan file, whole (#720 design, "Which copy of a plan counts").

    python3 plan_land.py ready --plan ID --status S --direction D --template <plan-view.md>
                               [--plans-dir D] [--repo R] [--remote origin] [--main main]
                               [--ignore PREFIX ...] [--date YYYY-MM-DD] --out <record.json>
    python3 plan_land.py check --record <record.json> [--repo R] [--remote origin] [--main main]
                               [--out <check.json>]
    python3 plan_land.py landed --check <check.json> [--repo R] [--remote origin] [--main main]
                               [--out <landed.json>]

`ready`, run by /propose-change on `plan/<id>/base` before it raises the branch for main:
  - the Status and Direction are the person's answers. A Status the template's `plan_statuses`
    does not list, or a Direction that is not one of its `directions` or `none`, stops it (exit 2)
    so the person is asked again; nothing is worked out;
  - uncommitted work outside the --ignore folders stops it (exit 3);
  - it names every change main made to the plan file since the branch was cut (the diff from
    where they meet to main);
  - it merges the latest main into the plan's branch, keeping the branch's plan file whole. A
    clash in any other file stops it with the merge taken back (exit 2): a person resolves it;
  - it writes the Status, the Direction and an empty `branch:` (merge-change deletes the branch
    after the merge) and the date on `updated:` into the plan file, and leaves the file changed
    for the play's own commit before the push. Every other line stays as it is.
`check`, run by /merge-change before it merges: main's plan file must be the one `ready` saw.
When main changed it since, it stops (exit 1) and says to run /propose-change again, so a blended
plan file never lands. It also records the plan file on the plan's branch, for `landed`.
`landed`, run by /merge-change after the merge: main's plan file must now equal the branch's
plan file that `check` recorded — the branch's version, whole (exit 1 when it does not).

The ready record: {plan, plan_file, status, direction, main_sha, main_plan_blob, merged,
main_changes: [diff lines], main_changed: bool}. The check record: {plan, plan_file, ok, main_plan_blob_then,
main_plan_blob_now, branch_plan_blob, error}. The landed record: {plan, ok, main_plan_blob,
branch_plan_blob, error}. Exit 0 done; 1 check failed; 2 bad input or a git step failed; 3
uncommitted work.
"""

import argparse
import datetime
import json
import os
import re
import sys

import plan as plan_tool
from plan_branch import Stop, current_branch, git, has_ref, has_remote, uncommitted, write

DEFAULT_PLANS = os.path.join(".garura", "project", "plans")


def answers(template, status, direction):
    """The person's answers, checked against the template's lists; never guessed."""
    li = template["list"]
    if status not in li["plan_statuses"]:
        raise Stop(f"the Status {status!r} is not one of {', '.join(li['plan_statuses'])}; ask again")
    d = str(direction).strip().lower()
    if d in ("none", ""):
        return status, None
    keys = {str(k): k for k in li["directions"]}
    if d not in keys:
        raise Stop(f"the Direction {direction!r} is not one of {', '.join(keys)} or none; ask again")
    return status, keys[d]


def set_fields(text, status, direction, date):
    """Set the top-level status, direction, branch and updated lines; keep every other line."""
    lines = text.split("\n")
    seen = set()
    values = {"status": f"status: {status}",
              "direction": "direction:" if direction is None else f"direction: {direction}",
              "branch": "branch:",
              "updated": f"updated: '{date}'"}
    for i, line in enumerate(lines):
        m = re.match(r"(status|direction|branch|updated):", line)
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            lines[i] = values[m.group(1)]
    if "status" not in seen:
        raise Stop("the plan file has no top-level status line")
    at = next(i for i, ln in enumerate(lines) if ln.startswith("status:"))
    for key in ("branch", "direction"):
        if key not in seen:
            lines.insert(at + 1, values[key])
    return "\n".join(lines)


def ready(args):
    repo, plan = args.repo, str(args.plan)
    plan_branch = f"plan/{plan}/base"
    path = os.path.join(args.plans_dir, f"{plan}.yaml")
    status, direction = answers(plan_tool.load_template(args.template), args.status, args.direction)
    if current_branch(repo) != plan_branch:
        raise Stop(f"not on {plan_branch}; ready runs on the plan's own branch")
    files = uncommitted(repo, args.ignore)
    if files:
        raise Stop(f"{plan_branch} has uncommitted work; commit or clean it, then run again", 3, files)
    if has_remote(args.remote, repo):
        git(["fetch", "--quiet", args.remote], repo)
        main_ref = f"{args.remote}/{args.main}"
    else:
        main_ref = args.main
    if not has_ref(main_ref, repo):
        raise Stop(f"no {main_ref} to land on")
    meet = git(["merge-base", "HEAD", main_ref], repo).stdout.strip()
    changes = git(["diff", meet, main_ref, "--", path], repo).stdout.splitlines()
    kept = git(["rev-parse", f"HEAD:{path}"], repo, check=False).stdout.strip()
    if not kept:
        raise Stop(f"no plan file {path} on {plan_branch}")
    merged = False
    if git(["merge-base", "--is-ancestor", main_ref, "HEAD"], repo, check=False).returncode != 0:
        done = git(["merge", "--no-ff", "--no-commit", main_ref], repo, check=False)
        clashes = git(["diff", "--name-only", "--diff-filter=U"], repo).stdout.split()
        others = [f for f in clashes if f != path.replace(os.sep, "/")]
        if others or (done.returncode != 0 and not clashes):
            git(["merge", "--abort"], repo, check=False)
            raise Stop(f"merging {args.main} into {plan_branch} clashes; resolve it by hand, then run "
                       f"again", 2, others)
        # The branch's plan file, whole: main's changes to it are named, never blended in.
        git(["checkout", "HEAD", "--", path], repo)
        git(["commit", "--quiet", "--no-edit", "-m",
             f"Merge {args.main} into {plan_branch}, keeping the branch's plan file (#{plan})"], repo)
        merged = True
    full = os.path.join(repo, path)
    with open(full, encoding="utf-8", newline="") as fh:
        text = fh.read()
    with open(full, "w", encoding="utf-8", newline="") as fh:
        fh.write(set_fields(text, status, direction, args.date))
    return {"plan": plan, "plan_file": path, "status": status, "direction": direction,
            "main_sha": git(["rev-parse", main_ref], repo).stdout.strip(),
            "main_plan_blob": git(["rev-parse", f"{main_ref}:{path}"], repo, check=False).stdout.strip() or None,
            "merged": merged, "main_changed": bool(changes), "main_changes": changes}


def check(args, rec):
    repo, path = args.repo, rec["plan_file"]
    if has_remote(args.remote, repo):
        git(["fetch", "--quiet", args.remote], repo)
        main_ref = f"{args.remote}/{args.main}"
    else:
        main_ref = args.main
    now = git(["rev-parse", f"{main_ref}:{path}"], repo, check=False).stdout.strip() or None
    branch_ref = f"{args.remote}/plan/{rec['plan']}/base" if has_remote(args.remote, repo) else f"plan/{rec['plan']}/base"
    on_branch = git(["rev-parse", f"{branch_ref}:{path}"], repo, check=False).stdout.strip() or None
    out = {"plan": rec["plan"], "plan_file": path, "ok": now == rec.get("main_plan_blob"),
           "main_plan_blob_then": rec.get("main_plan_blob"), "main_plan_blob_now": now,
           "branch_plan_blob": on_branch, "error": None}
    if not out["ok"]:
        out["error"] = (f"main's plan file {path} changed after the plan's branch was readied; run "
                        f"/propose-change again so the branch's plan file lands whole")
    return out


def landed(args, chk):
    repo, path = args.repo, chk["plan_file"]
    if has_remote(args.remote, repo):
        git(["fetch", "--quiet", args.remote], repo)
        main_ref = f"{args.remote}/{args.main}"
    else:
        main_ref = args.main
    now = git(["rev-parse", f"{main_ref}:{path}"], repo, check=False).stdout.strip() or None
    out = {"plan": chk["plan"], "ok": bool(now) and now == chk.get("branch_plan_blob"),
           "main_plan_blob": now, "branch_plan_blob": chk.get("branch_plan_blob"), "error": None}
    if not out["ok"]:
        out["error"] = f"main's plan file {path} is not the plan branch's plan file after the merge"
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="get a plan's branch ready to land on main, and check it")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("ready")
    r.add_argument("--plan", required=True)
    r.add_argument("--status", required=True)
    r.add_argument("--direction", required=True)
    r.add_argument("--template", required=True)
    r.add_argument("--plans-dir", default=DEFAULT_PLANS)
    r.add_argument("--repo", default=".")
    r.add_argument("--remote", default="origin")
    r.add_argument("--main", default="main")
    r.add_argument("--ignore", action="append", default=[])
    r.add_argument("--date", default=datetime.date.today().isoformat())
    r.add_argument("--out", required=True)
    c = sub.add_parser("check")
    c.add_argument("--record", required=True)
    c.add_argument("--repo", default=".")
    c.add_argument("--remote", default="origin")
    c.add_argument("--main", default="main")
    c.add_argument("--out")
    d = sub.add_parser("landed")
    d.add_argument("--check", required=True)
    d.add_argument("--repo", default=".")
    d.add_argument("--remote", default="origin")
    d.add_argument("--main", default="main")
    d.add_argument("--out")
    args = ap.parse_args(argv)

    if args.cmd == "ready":
        try:
            if not re.fullmatch(r"\d+", str(args.plan)):
                raise Stop("the plan is a number")
            rec = ready(args)
        except (Stop, plan_tool.BadInput) as e:
            rec = {"plan": str(args.plan), "error": str(e), "files": getattr(e, "files", [])}
            write(args.out, rec)
            print(json.dumps(rec, indent=2))
            return getattr(e, "code", 2)
        write(args.out, rec)
        print(json.dumps(rec, indent=2))
        return 0

    source = args.record if args.cmd == "check" else args.check
    try:
        with open(source, encoding="utf-8") as fh:
            rec = json.load(fh)
        out = check(args, rec) if args.cmd == "check" else landed(args, rec)
    except (OSError, ValueError, KeyError, Stop) as e:
        print(f"plan_land.py: cannot read {source}: {e}", file=sys.stderr)
        return 2
    if args.out:
        write(args.out, out)
    print(json.dumps(out, indent=2))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
