#!/usr/bin/env python3
"""
resolve_args.py — what does this start-change run start? (#989)

The change is what the person typed, never the branch the session is on:

  plan <id>              start a plan's work on its own (mode: plan)
  <number> [words]       an issue — the number, as today; any words after it are a note
  <words>                a short description of the change (mode: description); the play
                         finds or files its issue from it, as today
  nothing                nothing is started (mode: none) — the play stops with one line

    python3 resolve_args.py --args="<the play's arguments>" --plans-dir <plans> \
        [--repo .] [--ref origin/main] [--description-out <work-description.txt>] --out <args.json>

For `plan <id>` the plan file is read from git at --ref (the latest main, after a fetch), never
from the checkout: a plan no file names, or one main marks Done or Dropped, gets a plain message
and no start. When the fetch fails, the last fetched copy is read and the record says so.

Writes { mode, issue, plan, description, note, fetched, error }. Exit 0 when there is something
to start; 1 when nothing was typed, or the plan cannot be started (the error is the line to
show); 2 bad input (the plans folder cannot be read from git).
"""
import argparse
import json
import os
import re
import subprocess
import sys

import yaml

TIME_LIMIT = 120  # seconds for the fetch; a stalled server reads as a failed fetch, never a hang
CLOSED = ("Done", "Dropped")
NOTHING = "Tell me what to start: an issue number, a short description, or plan <id>."


def _git(repo, *args):
    try:
        p = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, timeout=TIME_LIMIT,
                           env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    except subprocess.TimeoutExpired:
        return 124, ""
    return p.returncode, p.stdout


def read(args_text):
    text = (args_text or "").strip()
    if not text:
        return {"mode": "none", "error": NOTHING}
    m = re.fullmatch(r"(?i)plan\s+#?(\d+)", text)
    if m:
        return {"mode": "plan", "plan": m.group(1)}
    m = re.fullmatch(r"#?(\d+)(?:\s+(.*))?", text, re.S)
    if m:
        return {"mode": "issue", "issue": m.group(1), "note": (m.group(2) or "").strip() or None}
    return {"mode": "description", "description": text}


def plan_on_main(rec, plans_dir, repo, ref):
    """A plan start needs a plan main names that is not closed; else the error is the line to show."""
    plan = rec["plan"]
    rc, _ = _git(repo, "fetch", "--quiet", "origin")
    rec["fetched"] = rc == 0
    rel = os.path.relpath(os.path.join(plans_dir, f"{plan}.yaml"), repo).replace(os.sep, "/")
    rc, text = _git(repo, "show", f"{ref}:{rel}")
    if rc != 0:
        rec["error"] = (f"No plan {plan} on main. To start a plan, give a plan's number "
                        f"(plan <id>); to start an issue, give its number.")
        return rec
    try:
        status = (yaml.safe_load(text) or {}).get("status")
    except yaml.YAMLError as e:
        raise ValueError(f"the plan file {rel} on {ref} cannot be read: {str(e).splitlines()[0]}")
    if status in CLOSED:
        rec["error"] = f"Plan {plan} is {status} on main; a person sets its status before its work starts again."
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser(description="what does this start-change run start?")
    ap.add_argument("--args", default="")
    ap.add_argument("--plans-dir", default=os.path.join(".garura", "project", "plans"))
    ap.add_argument("--repo", default=".")
    ap.add_argument("--ref", default="origin/main")
    ap.add_argument("--description-out")
    ap.add_argument("--out", required=True)
    ns = ap.parse_args(argv)

    rec = {"mode": None, "issue": None, "plan": None, "description": None, "note": None,
           "fetched": None, "error": None}
    rec.update(read(ns.args))
    try:
        if rec["mode"] == "plan":
            plan_on_main(rec, ns.plans_dir, ns.repo, ns.ref)
    except ValueError as e:
        rec["error"] = str(e)
        code = 2
    else:
        code = 1 if rec["error"] else 0
    if rec["mode"] == "description" and ns.description_out:
        os.makedirs(os.path.dirname(os.path.abspath(ns.description_out)), exist_ok=True)
        with open(ns.description_out, "w", encoding="utf-8") as fh:
            fh.write(rec["description"] + "\n")
    os.makedirs(os.path.dirname(os.path.abspath(ns.out)), exist_ok=True)
    with open(ns.out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=2)
        fh.write("\n")
    print(json.dumps(rec))
    return code


if __name__ == "__main__":
    sys.exit(main())
