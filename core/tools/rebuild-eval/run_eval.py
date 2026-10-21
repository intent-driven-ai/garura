#!/usr/bin/env python3
"""run_eval.py — run the rebuild eval: check the output, rebuild the prototype from it, score the drift.

    python3 run_eval.py --product-os <project>/.garura/product/product-os \
        --prototype <project>/prototype/argus.html --out <run folder> \
        [--inventory <an earlier inventory.json>] [--stage all | <stage>[,<stage>…]] \
        [--claude-model claude-sonnet-5-5] [--effort high] [--claude-bare]

Stages, in order (README.md): prepare → inventory → check → build → review → compare → score.
`all` runs every stage; a stage run alone reads what the earlier ones left in `<run folder>`.
`--inventory` reuses an inventory made earlier from the same prototype and skips that stage.

The run folder must be outside any git work tree, so no repository's instruction files reach the
agents. The Claude stages (inventory, review, compare) run `claude -p` from the run folder;
`--claude-bare` adds `--bare` (no user instructions or memory at all; it needs an API key). The
build is a fresh, restricted Claude Code session in a folder holding only the brief
(`run_builder.py`). Every agent runs on `--claude-model` at `--effort` (Sonnet 5.5, high). Every agent's command, exit and cost go to `run.json`.

Exit 0 every asked stage finished; 1 a stage finished without its output; 2 bad input.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WALKER = os.path.normpath(os.path.join(HERE, "..", "..", "components", "plays", "intent", "scripts",
                                       "walk_prototype.py"))
CLAUDE = os.environ.get("REBUILD_EVAL_CLAUDE_CLI", "claude")  # tests point this at a stand-in
STAGES = ("prepare", "inventory", "check", "build", "review", "compare", "score")
TOOLS = ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]


def script(name):
    return os.path.join(HERE, name)


def prompt(name, **values):
    with open(os.path.join(HERE, "prompts", name), encoding="utf-8") as fh:
        return fh.read().format(**values)


class Run:
    def __init__(self, args):
        self.args = args
        self.out = os.path.abspath(args.out)
        self.p = lambda *parts: os.path.join(self.out, *parts)
        self.log_path = self.p("run.json")
        self.log = json.load(open(self.log_path)) if os.path.isfile(self.log_path) else {"stages": {}}

    def record(self, stage, **facts):
        self.log["stages"][stage] = facts
        with open(self.log_path, "w", encoding="utf-8") as fh:
            json.dump(self.log, fh, indent=2)

    def py(self, stage, name, *argv):
        run = subprocess.run([sys.executable, script(name), *argv], capture_output=True, text=True)
        self.record(stage, command=name, exit=run.returncode, stdout=run.stdout.strip()[-1500:],
                    stderr=run.stderr.strip()[-800:])
        return run.returncode

    def claude(self, stage, text, expect):
        cmd = [CLAUDE, "-p", text, "--model", self.args.claude_model, "--effort", self.args.effort,
               "--permission-mode", "acceptEdits",
               "--allowedTools", *TOOLS, "--output-format", "json"]
        if self.args.claude_bare:
            cmd.insert(1, "--bare")
        run = subprocess.run(cmd, cwd=self.out, stdin=subprocess.DEVNULL, capture_output=True, text=True)
        facts = {"command": [c if c != text else "<prompt>" for c in cmd], "exit": run.returncode}
        try:
            res = json.loads(run.stdout)
            facts.update(cost_usd=res.get("total_cost_usd"), turns=res.get("num_turns"),
                         result=str(res.get("result"))[-500:])
        except ValueError:
            facts["stdout_tail"] = run.stdout[-500:]
        ok = os.path.isfile(expect)
        if ok:
            try:
                json.load(open(expect, encoding="utf-8"))
            except ValueError:
                ok, facts["error"] = False, f"{os.path.basename(expect)} is not JSON"
        facts["output"] = expect if ok else None
        self.record(stage, **facts)
        return 0 if ok else 1


def inside_git(path):
    while True:
        if os.path.exists(os.path.join(path, ".git")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run the rebuild eval.")
    ap.add_argument("--product-os", required=True)
    ap.add_argument("--prototype", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--inventory")
    ap.add_argument("--source-text", action="append", default=[],
                    help="more text the output may quote: a capture's view texts, the write-up, the journeys (repeatable)")
    ap.add_argument("--stage", default="all")
    ap.add_argument("--claude-model", default="claude-sonnet-5-5")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--claude-bare", action="store_true")
    args = ap.parse_args(argv)
    stages = list(STAGES) if args.stage == "all" else [s.strip() for s in args.stage.split(",")]
    bad = [s for s in stages if s not in STAGES]
    if bad:
        sys.stderr.write(f"run_eval.py: unknown stage(s): {bad}\n")
        return 2
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    repo = inside_git(out)
    if repo:
        sys.stderr.write(f"run_eval.py: the run folder is inside a git work tree ({repo}); "
                         f"put it outside any repository\n")
        return 2
    prototype = os.path.abspath(args.prototype)
    if not os.path.exists(prototype):
        sys.stderr.write(f"run_eval.py: no prototype at {prototype}\n")
        return 2
    run = Run(args)
    p = run.p
    if args.inventory:
        shutil.copyfile(args.inventory, p("inventory.json"))
        walk = os.path.join(os.path.dirname(os.path.abspath(args.inventory)), "inventory-work", "walk")
        if os.path.isdir(walk):
            args.source_text.append(walk)
        stages = [s for s in stages if s != "inventory"]
    captures = p("inventory-work", "walk")
    status = 0
    for stage in stages:
        if stage == "prepare":
            rc = run.py(stage, "prepare.py", "--product-os", os.path.abspath(args.product_os),
                        "--out", p("brief"), "--prototype-name", os.path.basename(prototype))
        elif stage == "inventory":
            os.makedirs(p("inventory-work"), exist_ok=True)
            rc = run.claude(stage, prompt("inventory.md", prototype=prototype, walker=WALKER,
                                          work=p("inventory-work"), out=p("inventory.json")),
                            p("inventory.json"))
        elif stage == "check":
            extra = ["--prototype-text", captures] if os.path.isdir(captures) else []
            for t in args.source_text:
                extra += ["--prototype-text", os.path.abspath(t)]
            rc = run.py(stage, "check_output.py", "--brief", p("brief"), "--prototype", prototype,
                        *extra, "--out", p("check.json"))
            rc = 0 if rc in (0, 1) else rc  # findings are a result, not a failed stage
        elif stage == "build":
            rc = run.py(stage, "run_builder.py", "--brief", p("brief"), "--build-dir", p("build"),
                        "--prompt", os.path.join(HERE, "prompts", "build.md"),
                        "--model", args.claude_model, "--effort", args.effort,
                        "--out", p("build.json"))
        elif stage == "review":
            rc = run.claude(stage, prompt("review.md", brief=p("brief"), inventory=p("inventory.json"),
                                          out=p("review.json")), p("review.json"))
        elif stage == "compare":
            os.makedirs(p("compare-work"), exist_ok=True)
            rc = run.claude(stage, prompt("compare.md", inventory=p("inventory.json"),
                                          rebuild=p("build", "app", "index.html"), brief=p("brief"),
                                          walker=WALKER, work=p("compare-work"), out=p("compare.json")),
                            p("compare.json"))
        else:  # score
            review = ["--review", p("review.json")] if os.path.isfile(p("review.json")) else []
            rc = run.py(stage, "score_drift.py", "--inventory", p("inventory.json"),
                        "--compare", p("compare.json"), "--check", p("check.json"), *review,
                        "--manifest", p("brief-manifest.json"),
                        "--out-json", p("report.json"), "--out-md", p("report.md"))
        print(f"{stage}: exit {rc}")
        if rc != 0:
            status = 1 if rc == 1 else 2
            break
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
