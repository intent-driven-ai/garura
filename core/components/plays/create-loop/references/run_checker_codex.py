#!/usr/bin/env python3
"""run_checker_codex.py — the coding-agent checker: Codex judges the bundle (R6).

`loops.<loop>.checker.kind: coding-agent`. Codex runs in a read-only sandbox with the bundle
folder as its working root, gets the `judge-loop-result` skill as its instructions, and must
answer in the skill's verdict schema; its final message is saved as the verdict. It cannot
write anywhere and sees only the bundle — the loop's outputs, never its reasoning. Canonical
copy lives at create-loop/references/run_checker_codex.py and is stamped into each loop's
scripts/.

    python3 run_checker_codex.py --bundle <working>/check/ \
        --skill <skills>/judge-loop-result/SKILL.md [--model M] --out <working>/check/verdict.json

The schema is read from `verdict.schema.json` beside the skill. Exit 0 — Codex answered and the
answer was saved (record_check.py judges its shape); 2 — Codex could not run or gave no answer.
Fixed command, no judgment (#484). Standard library only.
"""
import argparse
import os
import subprocess
import sys

CLI = os.environ.get("GARURA_CODEX_CLI", "codex")  # tests point this at a stand-in

PROMPT = """You are the checker of a finished loop. Follow the instructions below exactly.
Your working folder is the bundle: read only the files in it. Do not change any file.
Your final message must be only the verdict JSON, in the schema you were given.

--- instructions (judge-loop-result) ---
{skill}
"""


def strip_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run Codex as the loop checker.")
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--skill", required=True)
    ap.add_argument("--model")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    schema = os.path.join(os.path.dirname(os.path.abspath(args.skill)), "verdict.schema.json")
    try:
        with open(args.skill, encoding="utf-8") as fh:
            prompt = PROMPT.format(skill=strip_frontmatter(fh.read()))
        if not os.path.isfile(schema):
            raise OSError(f"no verdict schema beside the skill ({schema})")
        out = os.path.abspath(args.out)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        cmd = [CLI, "exec", "--sandbox", "read-only", "--cd", os.path.abspath(args.bundle),
               "--skip-git-repo-check", "--ephemeral", "--output-schema", schema,
               "--output-last-message", out]
        if args.model:
            cmd += ["--model", args.model]
        run = subprocess.run(cmd + ["-"], input=prompt, capture_output=True, text=True)
    except OSError as exc:
        sys.stderr.write(f"run_checker_codex.py: cannot run the checker: {exc}\n")
        return 2
    if run.returncode != 0 or not os.path.isfile(out) or not open(out, encoding="utf-8").read().strip():
        sys.stderr.write(f"run_checker_codex.py: Codex gave no verdict (exit {run.returncode}): "
                         f"{run.stderr.strip()[-800:]}\n")
        return 2
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
