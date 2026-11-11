#!/usr/bin/env python3
"""prepare_check.py — build the bundle the loop's checker judges (Shared Loop Run, R6).

The checker sees the loop's outputs and its criteria, never its reasoning (ADR 029 §2). This
script gathers exactly that into one folder, so the checker — a sub-agent on another model or a
coding agent — can be pointed at the folder and nothing else:

  criteria.md            the loop's goal, constraints and Done means, cut from its ICE
  manifest.json          criteria_ids (every id the checker must judge), issue, base, files
  change.diff            git diff <base>..HEAD, without the issue's own run records
  review/                each play's review record (the issue's review/loop/)
  answers.json, answers-sources.json   the answers gathered first, and their sources
  traces.json            the memory tool's `citations --issue <n> --check` answer
  done/                  each play's <play>-done.json

    python3 prepare_check.py --ice <loop>/reference/ice.md --issue <n> \
        --issue-dir <stm_base><n>/ --working <working> --base <sha> \
        [--memory-tool .garura/core/tools/memory/memory.py] --out-dir <working>/check/

Exit 0 built; 2 the ICE has no goal or criteria, or git cannot diff — nothing to judge. A
missing piece (no review records, no memory tool) is recorded in the manifest, not hidden: the
checker fails a criterion that needs it. Standard library only.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys


def section(text, title, level=2):
    """Body under a `#… <title>` header, up to the next header of the same or higher level."""
    m = re.search(rf"(?m)^#{{{level}}}\s+{re.escape(title)}\b.*$", text)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(rf"(?m)^#{{1,{level}}}\s", rest)
    return rest[: nxt.start()] if nxt else rest


def criteria_of(ice_text):
    """(criteria markdown, ids): the goal as G, the constraints C-n, the Done means D-n."""
    intent = section(ice_text, "Intent")
    goal = re.search(r"\*\*Goal:\*\*\s*(.+?)(?:\n\s*\n|$)", intent, re.S)
    constraints = section(intent, "Constraints", 3)
    done = section(section(ice_text, "Expectation"), "Done means", 3) or section(ice_text, "Done means", 3)
    ids = (["G"] if goal else []) + sorted(set(re.findall(r"(?m)^-\s*(C\d+)\b", constraints)),
                                           key=lambda x: int(x[1:]))
    ids += sorted(set(re.findall(r"(?m)^-\s*(D\d+)\b", done)), key=lambda x: int(x[1:]))
    text = "# Criteria\n\nJudge every id below.\n\n"
    if goal:
        text += f"## G — the goal\n\n{' '.join(goal.group(1).split())}\n\n"
    text += f"## Constraints\n{constraints.rstrip()}\n\n## Done means\n{done.rstrip()}\n"
    return text, ids


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def build(args):
    with open(args.ice, encoding="utf-8") as fh:
        text, ids = criteria_of(fh.read())
    if "G" not in ids or len(ids) < 2:
        raise ValueError("the ICE has no goal, or no constraints and no Done means, to judge")
    out = args.out_dir
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, "review"))
    os.makedirs(os.path.join(out, "done"))
    missing = []
    with open(os.path.join(out, "criteria.md"), "w", encoding="utf-8") as fh:
        fh.write(text)

    issue_dir = args.issue_dir.rstrip("/")
    diff = run(["git", "diff", f"{args.base}..HEAD", "--", ".", f":(exclude){issue_dir}"])
    if diff.returncode != 0:
        raise ValueError(f"git diff failed: {diff.stderr.strip()}")
    with open(os.path.join(out, "change.diff"), "w", encoding="utf-8") as fh:
        fh.write(diff.stdout)

    reviews = sorted(glob.glob(os.path.join(issue_dir, "review", "loop", "*")))
    for path in reviews:
        if os.path.isfile(path):
            shutil.copy(path, os.path.join(out, "review", os.path.basename(path)))
    if not reviews:
        missing.append("review records")
    for name in ("answers.json", "answers-sources.json"):
        src = os.path.join(args.working, name)
        if os.path.isfile(src):
            shutil.copy(src, os.path.join(out, name))
        else:
            missing.append(name)
    for path in sorted(glob.glob(os.path.join(args.working, "*-done.json"))):
        shutil.copy(path, os.path.join(out, "done", os.path.basename(path)))
    if not os.listdir(os.path.join(out, "done")):
        missing.append("done checks")

    traces = {"ok": False, "why": "the memory tool is not installed"}
    if args.memory_tool and os.path.isfile(args.memory_tool):
        t = run([sys.executable, args.memory_tool, "citations", "--issue", str(args.issue), "--check"])
        try:
            traces = json.loads(t.stdout.splitlines()[0]) if t.stdout.strip() else {
                "ok": False, "why": t.stderr.strip()[-500:]}
        except ValueError:
            traces = {"ok": False, "why": "the memory tool's answer could not be read"}
    else:
        missing.append("decision-trace check")
    with open(os.path.join(out, "traces.json"), "w", encoding="utf-8") as fh:
        json.dump(traces, fh, indent=2)

    files = sorted(os.path.relpath(os.path.join(d, f), out)
                   for d, _, fs in os.walk(out) for f in fs)
    manifest = {"criteria_ids": ids, "issue": args.issue, "base": args.base,
                "files": files + ["manifest.json"], "missing": missing}
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    return manifest


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the loop checker's bundle.")
    ap.add_argument("--ice", required=True)
    ap.add_argument("--issue", required=True, type=int)
    ap.add_argument("--issue-dir", required=True)
    ap.add_argument("--working", required=True, help="the loop's run folder")
    ap.add_argument("--base", required=True, help="the commit the loop's branch was cut from")
    ap.add_argument("--memory-tool", default=".garura/core/tools/memory/memory.py")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args(argv)
    try:
        manifest = build(args)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"prepare_check.py: {exc} — nothing to judge\n")
        return 2
    print(json.dumps({"bundle": args.out_dir, "criteria_ids": manifest["criteria_ids"],
                      "missing": manifest["missing"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
