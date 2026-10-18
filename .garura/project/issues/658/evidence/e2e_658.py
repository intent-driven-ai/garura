#!/usr/bin/env python3
"""End-to-end run for #658: a gap, a memory update, a person's answer on the approval page, the
write to short-term memory, and the answer from memory.

    python3 e2e_658.py prepare <demo folder> <Phoenix memory clone>
        makes a fresh project, looks up two things no tier holds, and raises one memory
        update for each (one blocks the work). Then a person answers them on the page:
        python3 core/tools/play-reviewer/memory_updates.py --settings <demo folder>/project/memory-settings.json
    python3 e2e_658.py finish <demo folder>
        applies what the person approved, tries the rejected one, and looks again — in the
        same issue and in another issue. Prints a Markdown record.
"""

import json
import os
import subprocess
import sys

TOOL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..",
                                    "core", "tools", "memory", "memory.py"))
GAPS = [
    {"look": "reset link lasts", "missing": "How long a password reset link lasts in this product.",
     "target": "658/context/answers/reset-link.md", "draft": "A password reset link lasts 30 minutes, then it stops working.",
     "source": "web", "blocking": True},
    {"look": "passkey", "missing": "Whether the product offers passkeys at launch.",
     "target": "658/context/answers/passkeys.md", "draft": "Offer passkeys at launch, next to email and password.",
     "source": "model", "blocking": False},
]


def tool(project, *args):
    env = dict(os.environ, MEMORY_SETTINGS=os.path.join(project, "memory-settings.json"))
    for k in ("MEMORY_SHORT_TERM_ROOT", "MEMORY_GARURA_ROOT", "MEMORY_PHOENIX_ROOT", "MEMORY_PHOENIX_REF"):
        env.pop(k, None)
    run = subprocess.run([sys.executable, TOOL, *args], capture_output=True, text=True, env=env, cwd=project)
    return json.loads(run.stdout.splitlines()[0])


def lookup(project, issue, pattern):
    a = tool(project, "search", "--issue", str(issue), "--pattern", pattern, "--ignore-case")
    first = a["hits"][0] if a["hits"] else None
    where = f"`{first['tier']}` `{first['path']}`" if first else "nothing"
    return a, f"looked in {', '.join(a['looked_in'])} → answered by **{a['answered_by'] or 'none'}**; first result: {where}"


def prepare(demo, phoenix_src):
    project = os.path.join(demo, "project")
    os.makedirs(os.path.join(project, ".garura", "project", "issues", "658"), exist_ok=True)
    phoenix = os.path.join(demo, "phoenix-memory")
    if not os.path.isdir(phoenix):
        subprocess.run(["git", "clone", "-q", os.path.expanduser(phoenix_src), phoenix], check=True)
    with open(os.path.join(project, "memory-settings.json"), "w") as fh:
        json.dump({"short-term": ".garura/project/issues", "garura": ".garura",
                   "phoenix": os.path.relpath(phoenix, project), "garura_pull_dir": "core/memory"}, fh)
    ids = []
    for gap in GAPS:
        a, _ = lookup(project, 658, gap["look"])
        assert a["answered_by"] is None, gap["look"]
        u = tool(project, "propose", "--request", json.dumps({
            "issue": 658, "missing": gap["missing"], "target_tier": "short-term", "target_path": gap["target"],
            "draft": gap["draft"], "draft_source": gap["source"], "sources": [], "requested_by": "e2e run (#658)",
            "blocking": gap["blocking"]}))["update"]
        ids.append(u["id"])
        a, _ = lookup(project, 658, gap["look"])
        assert a["answered_by"] is None, "a waiting draft must not be found"
    print(json.dumps({"project": project, "waiting": ids}))


def finish(demo):
    project = os.path.join(demo, "project")
    out = ["# End-to-end run — #658 memory updates\n",
           "A fresh project and a clone of Phoenix memory. Every memory update lands in the issue's "
           "short-term memory. A person answered each one on the local approval page.\n",
           "Before the person answered, each lookup below found nothing in any tier, and still found "
           "nothing once the update was raised: a waiting draft is never used (checked by `prepare`).\n"]
    updates = tool(project, "updates")["updates"]
    for gap in GAPS:
        u = next(x for x in updates if x["target_path"] == gap["target"])
        out.append(f"## {gap['missing']}\n")
        out.append(f"- Raised as `{u['id']}`, drafted from the {gap['source']}, "
                   f"{'blocks the work' if u['blocking'] else 'does not block the work'}.")
        out.append(f"- The person's answer: **{u['status']}** by {u['decided_by']}, in the "
                   f"{u['decided_in']}: \"{u['reply']}\".")
        if u["status"] in ("approved", "applied"):
            if u["status"] == "approved":
                tool(project, "apply", "--id", u["id"])
            out.append(f"- Applied: written to `{gap['target']}`.")
        else:
            a = tool(project, "apply", "--id", u["id"])
            code = a["error"]["code"] if not a["ok"] else "applied"
            written = os.path.exists(os.path.join(project, ".garura", "project", "issues", gap["target"]))
            out.append(f"- Apply refused: `{code}`; anything written: {'yes' if written else 'no'}.")
        _, same = lookup(project, 658, gap["look"])
        _, other = lookup(project, 659, gap["look"])
        out.append(f"- Look up again in issue 658: {same}")
        out.append(f"- Look up in issue 659: {other}\n")
    rejected = [x for x in updates if x["status"] == "rejected"]
    if not rejected:
        out.append("No update was rejected in this run. A rejected update writes nothing and its work stays "
                   "stopped: `test_a_rejected_update_writes_nothing` in `core/tools/memory/test_memory.py`.")
    print("\n".join(out))


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare(sys.argv[2], sys.argv[3])
    else:
        finish(sys.argv[2])
