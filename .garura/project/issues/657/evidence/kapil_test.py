#!/usr/bin/env python3
"""Kapil's test for #657: a fresh project, a copy of Phoenix memory, two stories, then the
project memory removed. Prints a Markdown record. Usage: python3 kapil_test.py core/tools/memory <Phoenix memory clone>"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

TOOL, PHOENIX_SRC = os.path.abspath(sys.argv[1]), os.path.expanduser(sys.argv[2])
work = tempfile.mkdtemp(prefix="kapil-test-")
project = os.path.join(work, "project")
phoenix = os.path.join(work, "phoenix-memory")
garura = os.path.join(project, ".garura")
short = os.path.join(garura, "project", "issues")
os.makedirs(short)
subprocess.run(["git", "clone", "-q", PHOENIX_SRC, phoenix], check=True)
settings = os.path.join(project, "memory-settings.json")
with open(settings, "w") as fh:
    json.dump({"short-term": ".garura/project/issues", "garura": ".garura",
               "phoenix": os.path.relpath(phoenix, project), "garura_pull_dir": "core/memory"}, fh)
env = dict(os.environ, MEMORY_SETTINGS=settings)
for k in ("MEMORY_SHORT_TERM_ROOT", "MEMORY_GARURA_ROOT", "MEMORY_PHOENIX_ROOT", "MEMORY_PHOENIX_REF"):
    env.pop(k, None)

lines, failures = [], []


def story(issue, text):
    path = os.path.join(short, str(issue), "specs", "story.md")
    os.makedirs(os.path.dirname(path))
    with open(path, "w") as fh:
        fh.write(text + "\n")
    lines.append(f"\n**Short-term memory for issue {issue}:** `{issue}/specs/story.md` — \"{text}\"\n")


def tool(*args):
    run = subprocess.run([sys.executable, os.path.join(TOOL, "memory.py"), *args], capture_output=True,
                         text=True, env=env, cwd=project)
    return [json.loads(x) for x in run.stdout.splitlines()]


def step(title, args, expect=None):
    a = tool(*args)[0]
    if a.get("ok") is False:
        got = f"error `{a['error']['code']}`"
    elif a["command"] in ("find", "search"):
        results = a.get("hits", a.get("matches", []))
        first = results[0] if results else None
        where = f"`{first['tier']}` `{first['path']}`" + (f" line {first['line']}" if first and "line" in first else "") if first else "nothing"
        got = f"looked in {', '.join(a['looked_in'])} → answered by **{a['answered_by']}**; first result: {where}"
    elif a["command"] == "read":
        got = f"read `{a['tier']}` `{a['path']}` lines {a['start']}–{a['end']}"
    else:
        got = json.dumps(a)[:200]
    ok = expect is None or (a.get("answered_by") == expect if a.get("ok") else expect == a["error"]["code"])
    if not ok:
        failures.append(title)
    lines.append(f"- {title}  \n  `memory.py {' '.join(args)}`  \n  {got} {'✓' if ok else '✗ expected ' + str(expect)}")
    return a


def pulled():
    pieces = tool("pulled")[0]["pieces"]
    lines.append(f"- Pulled into Garura memory so far: {', '.join('`' + p['path'] + '`' for p in pieces) or 'nothing'}")


lines.append("# Kapil's test — #657 memory tool\n")
lines.append("A fresh project (empty Garura memory) and a clone of Phoenix memory, read at its approved "
             "version (`origin/main`). Settings: `memory-settings.json` in the project "
             "(short-term `.garura/project/issues`, Garura `.garura`, pulled pieces in `core/memory`).\n")
v = tool("health")[0]["tiers"]
lines.append("Health: " + ", ".join(f"{t['tier']} {'reachable' if t['reachable'] else 'NOT reachable'}"
                                    + (f" at `{t['version']}`" if t['version'] else "") for t in v) + "\n")

lines.append("## 1. Login story")
story(1, "Story: a user signs in to the app with email and password.")
step("Look up how sign-in works", ["search", "--issue", "1", "--pattern", "credential login", "--fixed"], "phoenix")
step("Use it: read the Authentication part", ["read", "--issue", "1", "--tier", "phoenix", "--path",
                                               "knowledge/domains/user-management.md", "--start", "44", "--end", "48"])
pulled()

lines.append("\n## 2. Re-run the login story")
step("The same lookup again", ["search", "--issue", "1", "--pattern", "credential login", "--fixed"], "garura")

lines.append("\n## 3. Change-password story")
story(2, "Story: a signed-in user changes their password.")
step("Look up password reset (pulled during the login story)",
     ["search", "--issue", "2", "--pattern", "Password reset", "--fixed"], "garura")
step("Look up password strength (not pulled yet)",
     ["search", "--issue", "2", "--pattern", "Password strength validation", "--fixed"], "phoenix")
step("Use it: read the password strength rule", ["read", "--issue", "2", "--tier", "phoenix", "--path",
                                                 "standards/rules/kb-extension.md", "--start", "145", "--end", "146"])
pulled()

lines.append("\n## 4. Project memory removed")
shutil.rmtree(os.path.join(garura, "core", "memory"))
lines.append("- Deleted `.garura/core/memory/` (every pulled piece and the pulled list).")
step("The login lookup again", ["search", "--issue", "1", "--pattern", "credential login", "--fixed"], "phoenix")
step("Something no tier holds", ["search", "--issue", "2", "--pattern", "passkey", "--ignore-case"], None)
lines.append("  The empty answer (answered by none, after all three tiers) is the cue to raise a memory "
             "update; raising it is #658, and it lands in short-term memory.")

lines.append("\n## Result")
lines.append("All steps behaved as expected." if not failures else "Failed: " + "; ".join(failures))
print("\n".join(lines))
shutil.rmtree(work)
sys.exit(1 if failures else 0)
