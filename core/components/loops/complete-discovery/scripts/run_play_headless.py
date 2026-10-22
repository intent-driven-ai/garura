#!/usr/bin/env python3
"""run_play_headless.py — run one play of a loop as a headless session (Shared Loop Run, R5).

The `headless` runner (`loops.<loop>.runner: headless`), for a loop started outside an
interactive session. The default runner is a sub-agent per play; this script is the other
kind. It starts `claude -p "/<play> --contract <contract>"` in the project, waits for it, and
writes the session's JSON result, so the loop can read the play's answer and its session id.
To answer a question the play stopped on, run it again with `--resume <session id>` and
`--message-file` holding the person's answer: the same session goes on, with its context.
Canonical copy lives at create-loop/references/run_play_headless.py and is stamped into each
loop's scripts/.

    python3 run_play_headless.py --play discover-intent --contract <contract.json> \
        [--argument "<inputs.discover-intent.argument>"] --out <run.json>
    python3 run_play_headless.py --play discover-domains --resume <session id> \
        --message-file <answer.txt> --out <run.json>

Exit 0 — the session ended without error. Exit 1 — the session ended with an error (the result
says which). Exit 2 — bad input, or the session could not start. Fixed commands, no judgment
(#484). Standard library only.
"""
import argparse
import json
import os
import subprocess
import sys

CLI = os.environ.get("GARURA_HEADLESS_CLI", "claude")  # tests point this at a stand-in


def command(args):
    if args.resume:
        with open(args.message_file, encoding="utf-8") as fh:
            prompt = fh.read().strip()
        if not prompt:
            raise ValueError("the message file is empty")
        return [CLI, "-p", prompt, "--resume", args.resume, "--output-format", "json"]
    prompt = f"/{args.play} --contract {args.contract}"
    if args.argument:
        prompt += f" {args.argument}"  # inputs.<play>.argument, as a person would type it
    return [CLI, "-p", prompt, "--output-format", "json"]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run one play of a loop headless.")
    ap.add_argument("--play", required=True)
    ap.add_argument("--contract")
    ap.add_argument("--argument", help="the play's own argument (inputs.<play>.argument)")
    ap.add_argument("--resume", help="the session id to continue")
    ap.add_argument("--message-file", help="the person's answer, with --resume")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    if bool(args.resume) == bool(args.contract) or (args.resume and not args.message_file):
        sys.stderr.write("run_play_headless.py: give --contract to start, or --resume with "
                         "--message-file to continue\n")
        return 2
    try:
        cmd = command(args)
        run = subprocess.run(cmd, capture_output=True, text=True)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"run_play_headless.py: cannot start the session: {exc}\n")
        return 2
    try:
        result = json.loads(run.stdout)
    except ValueError:
        result = {"is_error": True, "result": run.stdout[-2000:], "stderr": run.stderr[-2000:]}
    result["play"] = args.play
    result["exit_code"] = run.returncode
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps({"play": args.play, "session_id": result.get("session_id"),
                      "is_error": result.get("is_error", run.returncode != 0)}))
    return 1 if run.returncode != 0 or result.get("is_error") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
