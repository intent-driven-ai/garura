#!/usr/bin/env python3
"""Run every command in the memory guide, as written, on a throwaway project (#660 item 3).

Usage: python3 run_guide.py <memory tool folder> <Phoenix memory source>

The project's Phoenix memory place starts empty, so the first command that needs it also
proves the download. Placeholders a reader fills in are filled the same way here: the tool's
path, an agent name, a play, and the fingerprint taken from a read. Prints a Markdown record;
exits 1 when any command answers an error.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL_DIR, SOURCE = os.path.abspath(sys.argv[1]), os.path.expanduser(sys.argv[2])
tool = os.path.join(TOOL_DIR, "memory.py")
work = tempfile.mkdtemp(prefix="guide-run-")
project = os.path.join(work, "project")
garura = os.path.join(project, "g")
os.makedirs(os.path.join(garura, "issues", "12"))
settings = os.path.join(project, "memory-settings.json")
with open(settings, "w") as fh:
    json.dump({"short-term": "g/issues", "garura": "g", "phoenix": "../machine/phoenix-memory",
               "phoenix_source": SOURCE, "garura_pull_dir": "core/memory"}, fh)
env = {k: v for k, v in os.environ.items() if not k.startswith("MEMORY_")}
env["MEMORY_SETTINGS"] = settings


def run(script):
    out = subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=env, cwd=project)
    return [json.loads(line) for line in out.stdout.splitlines() if line.strip()], out.stderr


# the fingerprint a reader takes from a read of the line the trace names
answers, _ = run(f"python3 {tool} read --issue 12 --tier phoenix "
                 "--path knowledge/domains/user-management.md --start 62 --end 62")
fingerprint = answers[0]["fingerprint"]

with open(os.path.join(TOOL_DIR, "GUIDE.md"), encoding="utf-8") as fh:
    blocks = re.findall(r"```\n(.*?)```", fh.read(), re.S)

lines, failed = ["# The memory guide, run as written", "",
                 f"Phoenix memory source: `{os.path.basename(SOURCE.rstrip('/'))}`; its place started empty.", ""], 0
for n, block in enumerate(blocks, 1):
    script = (block.replace("{tool}", tool).replace("<your agent name>", "guide-runner")
              .replace("<your play>", "/guide").replace("<from the read answer>", fingerprint))
    answers, err = run(script)
    lines.append(f"## Block {n}")
    for a in answers:
        state = "ok" if a.get("ok") else f"ERROR {a['error']['code']}: {a['error']['message']}"
        extra = {"search": lambda a: f"answered_by {a.get('answered_by')}, {len(a.get('hits', []))} hits",
                 "find": lambda a: f"answered_by {a.get('answered_by')}, {len(a.get('matches', []))} matches",
                 "read": lambda a: f"lines {a.get('start')}–{a.get('end')}, saved_to {a.get('saved_to')}",
                 "propose": lambda a: f"update {a['update']['id']} {a['update']['status']}",
                 "cite": lambda a: f"recorded {a.get('citation_id')}",
                 "citations": lambda a: f"{len(a.get('records', []))} record(s), {len(a.get('problems', []))} problem(s)"}
        detail = extra.get(a["command"], lambda a: "")(a) if a.get("ok") else ""
        lines.append(f"- `{a['command']}`: {state}{' — ' + detail if detail else ''}")
        failed += 0 if a.get("ok") else 1
    if not answers:
        lines.append(f"- no answer: {err.strip()}")
        failed += 1
    lines.append("")
lines.append(f"Phoenix memory downloaded to its place: {os.path.isdir(os.path.join(work, 'machine', 'phoenix-memory', '.git'))}")
lines.append(f"Result: {'every command answered ok' if not failed else f'{failed} error(s)'}")
print("\n".join(lines))
shutil.rmtree(work, ignore_errors=True)
sys.exit(1 if failed else 0)
