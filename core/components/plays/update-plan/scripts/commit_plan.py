#!/usr/bin/env python3
"""commit_plan.py — one commit on the plan's branch, pushed (C7).

    python3 commit_plan.py --plan <id> --plan-branch plan/<id>/base --plan-file <plans>/<id>.yaml \
        --changes <changes.yaml> [--model-record <model-record.json>] [--records-dir <stm>/<id>/] \
        [--repo R] [--remote origin] --out <commit.json>

It refuses (exit 2, nothing committed) unless the branch checked out is the plan's branch. It
stages and commits only the plan file, the model files the model record names (`files`; each
must be a path inside the repository) and, with
--records-dir, the changed files in the plan's own short-term folder (the decision records the
session's sub-agents wrote there, such as citations.jsonl), and commits them as one commit,
pushed. The plan file keeps no history; this commit is the record. Its message:

    chore(plan): plan <id> — update: <n> changes (#<id>)

    Asked: <each instruction, as the person typed it>
    Override: #<issue>: <the rule it breaks>        (one line each; none when there are none)
    Owed: <what a new feature still needs>          (one line each)

With nothing staged, it makes no commit. The record: {ok, commit, pushed, files, message,
overrides_recorded}. Exit 0 done; 1 the push failed (the commit is kept and named); 2 refused.
"""

import argparse
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_session as ps  # noqa: E402


def git(args, repo, check=True):
    for _ in range(8):
        done = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
        if done.returncode == 0 or "index.lock" not in done.stderr:
            break
        time.sleep(2)
    if check and done.returncode != 0:
        raise ps.Refused(f"git {' '.join(args)} failed: {(done.stderr or done.stdout).strip()}")
    return done


def main(argv=None):
    ap = argparse.ArgumentParser(description="one commit on the plan's branch, pushed")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--plan-branch", required=True)
    ap.add_argument("--plan-file", required=True)
    ap.add_argument("--model-record")
    ap.add_argument("--records-dir")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--changes", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    rec = {"ok": False, "commit": None, "pushed": False, "files": []}
    try:
        changes = ps.load_list(args.changes) or {}
        entries = changes.get("entries") or []
        made = {}
        gh = os.path.join(os.path.dirname(os.path.abspath(args.changes)), "github-record.json")
        if os.path.isfile(gh):
            made = {k: v.get("result") for k, v in (ps.read_json(gh, "the tracker record").get("done") or {}).items()}
        lines = [f"chore(plan): plan {args.plan} — update: {len(entries)} changes (#{args.plan})", ""]
        lines += [f"Asked: {a}" for a in changes.get("asked") or []]
        overrides = []
        for e in entries:
            if e.get("override"):
                n = made.get(f"{e['n']}-create") or e.get("issue")
                overrides.append(f"Override: #{n}: {e['override']}")
        lines += overrides + [f"Owed: {o}" for o in ps.owed_of(changes)]
        rec["message"] = "\n".join(lines).rstrip() + "\n"
        rec["overrides_recorded"] = len(overrides) == len([e for e in entries if e.get("override")])
        on = git(["branch", "--show-current"], args.repo).stdout.strip()
        if on != args.plan_branch:
            raise ps.Refused(f"on {on}, not on the plan's branch {args.plan_branch}; nothing is committed")
        root = os.path.realpath(args.repo)
        files = [args.plan_file]
        if args.model_record and os.path.isfile(args.model_record):
            files += ps.read_json(args.model_record, "the model record").get("files") or []
        for f in files:
            full = os.path.realpath(os.path.join(root, f))
            if os.path.isabs(f) or not full.startswith(root + os.sep):
                raise ps.Refused(f"{f} is not a path inside the repository; nothing is committed")
        if args.records_dir:
            out = git(["status", "--porcelain", "-z", "--untracked-files=all", "--", args.records_dir],
                      args.repo).stdout
            entries, i = out.split("\0"), 0
            while i < len(entries):
                entry = entries[i]
                i += 1
                if len(entry) < 4:
                    continue
                if entry[0] in "RC":
                    i += 1
                files.append(entry[3:])
        git(["add", "--", *files], args.repo)
        if git(["diff", "--cached", "--quiet", "--", *files], args.repo, check=False).returncode == 0:
            rec.update(ok=True, files=[])
            ps.write_json(args.out, rec)
            return 0
        # Only the named files go into the commit, whatever else a person had staged.
        git(["commit", "--quiet", "-m", rec["message"], "--", *files], args.repo)
        rec["commit"] = git(["rev-parse", "HEAD"], args.repo).stdout.strip()
        rec["files"] = files
        remotes = git(["remote"], args.repo).stdout.split()
        if args.remote in remotes:
            if git(["push", "--quiet", args.remote, args.plan_branch], args.repo, check=False).returncode != 0:
                ps.write_json(args.out, rec)
                return 1
            rec["pushed"] = True
        rec["ok"] = True
        ps.write_json(args.out, rec)
        return 0
    except ps.Refused as e:
        rec["error"] = str(e)
        ps.write_json(args.out, rec)
        print(f"refused: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
