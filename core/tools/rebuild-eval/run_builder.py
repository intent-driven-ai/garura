#!/usr/bin/env python3
"""run_builder.py — a fresh agent rebuilds the product from the brief alone (rebuild eval).

    python3 run_builder.py --brief <run>/brief --build-dir <run>/build \
        --prompt prompts/build.md [--model claude-sonnet-5-5] [--effort high] --out <run>/build.json

A new Claude Code session (`claude -p`) runs in `<build-dir>`, which holds only a copy of the
brief: no prototype, no Garura files. It runs `--restricted` (no settings files, file tools
confined to the build folder, no shell), with `--strict-mcp-config` (no MCP servers) and
`--disable-slash-commands` (no skills), so it builds from the brief and the prompt alone. The
build folder must not sit inside a git work tree — a repository's instruction files would reach
the builder — and the script refuses one that does.

Writes `{ok, app, notes, exit, cli, cost_usd, turns}` to `--out`. Exit 0 the app was built
(`<build-dir>/app/index.html`); 1 the builder ran but built no app; 2 the builder could not
run or the build folder is not isolated. Fixed command, no judgement. Standard library only.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

CLI = os.environ.get("REBUILD_EVAL_CLAUDE_CLI", "claude")  # tests point this at a stand-in
TOOLS = ["Read", "Write", "Edit", "Glob", "Grep"]


def inside_git(path):
    path = os.path.abspath(path)
    while True:
        if os.path.exists(os.path.join(path, ".git")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rebuild the product from the brief with a fresh Claude Code session.")
    ap.add_argument("--brief", required=True)
    ap.add_argument("--build-dir", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    build = os.path.abspath(args.build_dir)
    repo = inside_git(build)
    if repo:
        sys.stderr.write(f"run_builder.py: the build folder is inside a git work tree ({repo}); "
                         f"put the run folder outside any repository\n")
        return 2
    try:
        if os.path.exists(build):
            shutil.rmtree(build)
        shutil.copytree(os.path.abspath(args.brief), os.path.join(build, "brief"))
        os.makedirs(os.path.join(build, "app"))
        with open(args.prompt, encoding="utf-8") as fh:
            prompt = fh.read()
        cmd = [CLI, "-p", prompt, "--model", args.model, "--effort", args.effort, "--restricted",
               "--strict-mcp-config", "--disable-slash-commands", "--tools", ",".join(TOOLS),
               "--permission-mode", "acceptEdits", "--output-format", "json"]
        run = subprocess.run(cmd, cwd=build, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    except OSError as exc:
        sys.stderr.write(f"run_builder.py: cannot run the builder: {exc}\n")
        return 2
    app = os.path.join(build, "app", "index.html")
    notes = os.path.join(build, "app", "NOTES.md")
    built = os.path.isfile(app) and os.path.getsize(app) > 0
    record = {"ok": built, "app": app if built else None,
              "notes": notes if os.path.isfile(notes) else None,
              "exit": run.returncode, "cli": " ".join(c if c != prompt else "<prompt>" for c in cmd),
              "stderr_tail": run.stderr[-800:]}
    try:
        res = json.loads(run.stdout)
        record.update(cost_usd=res.get("total_cost_usd"), turns=res.get("num_turns"))
    except ValueError:
        record["stdout_tail"] = run.stdout[-500:]
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    print(json.dumps({k: record[k] for k in ("ok", "app", "exit")}))
    if run.returncode != 0 and not built:
        return 2
    return 0 if built else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
