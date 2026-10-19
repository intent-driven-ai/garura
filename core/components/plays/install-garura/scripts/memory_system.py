#!/usr/bin/env python3
"""
memory_system.py — lay Garura's memory system into a project, and check it (ADR 035 §8).

Both install paths call this: the install-garura play (install.py) and the public installer
(installer/install.sh). It lays:

  .garura/tools/memory/     the memory tool, copied from core/tools/memory without its tests
                            and samples, with settings.json beside it
  .garura/project/issues/   short-term memory: one folder per issue
  the memory guide, where the host tool loads it for every agent:
    claude  .claude/rules/garura-memory.md — a rules file with no paths field loads at
            launch, for every session and every custom sub-agent
    codex   one marked block in AGENTS.md — Codex reads AGENTS.md at the start of every
            session; a project's own AGENTS.md keeps its text, and gains only the block

The install brings no memory. Phoenix memory has one place per machine; the tool downloads
it there from its source the first time a command needs it. A re-install replaces the tool
and the guide, and keeps settings a person edited.

The check runs the tool's health command the way an agent runs it: with no MEMORY_* settings,
so the tool reads the settings beside it. It fails when the tool cannot run, or when short-term
or Garura memory cannot be reached. Phoenix memory not downloaded yet is reported, not failed;
the check then asks Phoenix memory's source whether it answers, and notes it when it does not.

    python3 memory_system.py --target <project> --tool claude|codex [--source <garura checkout>]
                             [--phoenix-place PATH] [--phoenix-source URL] [--check-only]

Exit: 0 = laid and checked, 1 = the check failed, 2 = bad input. Standard library only.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

TOOL_DEST = os.path.join(".garura", "tools", "memory")
TOOL_CALL = ".garura/tools/memory/memory.py"  # how the guide tells an agent to run the tool
SHORT_TERM = os.path.join(".garura", "project", "issues")
GUIDE_CLAUDE = os.path.join(".claude", "rules", "garura-memory.md")
AGENTS_MD = "AGENTS.md"
BLOCK_START = ("<!-- garura-memory:start — written by the Garura install; "
               "a re-install replaces this block, uninstall removes it -->")
BLOCK_END = "<!-- garura-memory:end -->"
PHOENIX_PLACE = "~/.garura/phoenix-memory"
PHOENIX_SOURCE = "https://github.com/intent-driven-ai/phoenix-memory.git"
NEEDS_PYTHON = (3, 10)
REACH_SECONDS = 30  # how long the check waits to learn whether Phoenix memory's source answers


def _bad(msg):
    """Bad input: say so and stop with exit 2, never the check's exit 1."""
    print(f"memory_system.py: {msg}", file=sys.stderr)
    raise SystemExit(2)


def _skip(folder, names):
    """What the installed tool leaves out: its tests, the contract's samples, caches, and any
    settings file in the source (an install writes its own)."""
    skip = {n for n in names if n.startswith("test_") or n == "__pycache__" or n == "settings.json"}
    if os.path.basename(folder) == "contract":
        skip |= {n for n in names if n in ("samples", "broken")}
    return skip


def settings_for(phoenix_place, phoenix_source):
    """The tool's settings, relative to the settings file in .garura/tools/memory/."""
    return {"short-term": "../../project/issues", "garura": "../..", "phoenix": phoenix_place,
            "phoenix_source": phoenix_source, "garura_pull_dir": "core/memory"}


def put_block(path, text):
    """Write the guide as one marked block in a file, replacing an earlier block and keeping
    everything else."""
    old = ""
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            old = fh.read()
    rest = strip_block(old).rstrip("\n")
    block = f"{BLOCK_START}\n{text.rstrip()}\n{BLOCK_END}\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write((rest + "\n\n" if rest else "") + block)


def strip_block(text):
    """The text without the guide's block."""
    start = text.find(BLOCK_START)
    end = text.find(BLOCK_END, start) if start >= 0 else -1
    if end < 0:
        return text
    before, after = text[:start].rstrip("\n"), text[end + len(BLOCK_END):].lstrip("\n")
    kept = "\n\n".join(p for p in (before, after.rstrip("\n")) if p)
    return kept + "\n" if kept else ""


def lay(source, target, tool, phoenix_place=PHOENIX_PLACE, phoenix_source=PHOENIX_SOURCE, info=print):
    """Lay the tool, its settings, the short-term folder and the guide. Returns the record the
    install manifest keeps, so uninstall can reverse it."""
    src = os.path.join(source, "core", "tools", "memory")
    if not os.path.isfile(os.path.join(src, "memory.py")):
        _bad(f"{source} has no memory tool (core/tools/memory/memory.py)")
    dest = os.path.join(target, TOOL_DEST)
    settings_path = os.path.join(dest, "settings.json")
    kept = None
    if os.path.isfile(settings_path):
        with open(settings_path, encoding="utf-8") as fh:
            kept = fh.read()
    # the new copy is made whole beside the old one, then swapped in: a copy that stops part
    # way leaves the old tool and its settings where they were
    new = dest + ".new"
    shutil.rmtree(new, ignore_errors=True)
    try:
        shutil.copytree(src, new, ignore=_skip)
        with open(os.path.join(new, "settings.json"), "w", encoding="utf-8") as fh:
            fh.write(kept if kept is not None else json.dumps(settings_for(phoenix_place, phoenix_source), indent=2) + "\n")
    except BaseException:
        shutil.rmtree(new, ignore_errors=True)  # a half copy left in .garura/ would read as memory
        raise
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    os.rename(new, dest)
    info(f"  memory tool: {TOOL_DEST} (settings {'kept' if kept is not None else 'written'})")
    os.makedirs(os.path.join(target, SHORT_TERM), exist_ok=True)

    with open(os.path.join(src, "GUIDE.md"), encoding="utf-8") as fh:
        guide = fh.read().replace("{tool}", TOOL_CALL)
    record = {"tool": TOOL_DEST, "short_term": SHORT_TERM, "guide": None, "agents_md_block": None}
    if tool == "claude":
        path = os.path.join(target, GUIDE_CLAUDE)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(guide)
        record["guide"] = GUIDE_CLAUDE
        info(f"  memory guide: {GUIDE_CLAUDE}")
    elif tool == "codex":
        put_block(os.path.join(target, AGENTS_MD), guide)
        record["agents_md_block"] = AGENTS_MD
        info(f"  memory guide: a marked block in {AGENTS_MD}")
    else:
        _bad(f"unknown tool {tool!r}")
    return record


def check(target, info=print):
    """Run the installed tool the way an agent does and say what it reaches."""
    report = {"ok": True, "python": None, "tiers": {}, "messages": []}
    env = {k: v for k, v in os.environ.items() if not k.startswith("MEMORY_")}
    if not _python_ok(report, env):
        return _say(report, info)
    run = subprocess.run(["python3", TOOL_CALL, "health"], capture_output=True, text=True, env=env, cwd=target)
    try:
        answer = json.loads(run.stdout.splitlines()[0])
    except (IndexError, ValueError):
        _fail(report, f"the memory tool did not run: {(run.stderr.strip().splitlines() or ['no answer'])[-1]}")
        return _say(report, info)
    try:
        if not answer.get("ok"):
            err = answer.get("error") or {}
            _fail(report, f"the memory tool answered {err.get('code', 'not ok')}: "
                          f"{err.get('message', run.stdout.strip())}")
            return _say(report, info)
        tiers = answer.get("tiers", [])
        report["tiers"] = {t["tier"]: t["reachable"] for t in tiers}
    except (AttributeError, KeyError, TypeError):
        _fail(report, f"the memory tool gave an answer the check cannot read: {run.stdout.strip()[:200]}")
        return _say(report, info)
    for tier, name in (("short-term", "Short-term memory"), ("garura", "Garura memory")):
        if report["tiers"].get(tier):
            report["messages"].append(f"{name}: reached.")
        else:
            _fail(report, f"{name} cannot be reached at the place the tool's settings name.")
    phoenix = next((t for t in tiers if t["tier"] == "phoenix"), {})
    report["messages"] += _phoenix_lines(target, phoenix, env)
    return _say(report, info)


def _fail(report, msg):
    report["ok"] = False
    report["messages"].append("FAIL: " + msg)


def _python_ok(report, env):
    """The tool needs python3 at NEEDS_PYTHON or newer."""
    try:
        ver = subprocess.run(["python3", "-c", "import sys; print('%d.%d' % sys.version_info[:2])"],
                             capture_output=True, text=True, env=env)
    except OSError as exc:
        _fail(report, f"the memory tool needs python3, and it cannot be run here: {exc}.")
        return False
    report["python"] = ver.stdout.strip()
    try:
        found = tuple(int(p) for p in report["python"].split("."))
    except ValueError:
        found = (0, 0)
    if found < NEEDS_PYTHON:
        _fail(report, f"the memory tool needs Python {'.'.join(map(str, NEEDS_PYTHON))} or newer; "
                      f"python3 here is {report['python']}.")
        return False
    return True


def _phoenix_lines(target, phoenix, env):
    """What the check says about Phoenix memory. Never a failure: the tool downloads it the
    first time it is needed. When it is not here yet, the check asks its source whether it
    answers, so a machine that cannot reach it hears so now, not at an agent's first lookup."""
    with open(os.path.join(target, TOOL_DEST, "settings.json"), encoding="utf-8") as fh:
        settings = json.load(fh)
    place = settings.get("phoenix") or "(no setting)"
    if phoenix.get("reachable"):
        return [f"Phoenix memory: on this machine, at version {phoenix['version']}."]
    if os.path.exists(os.path.join(target, TOOL_DEST, os.path.expanduser(place))):
        return [f"NOTE: Phoenix memory's place, {place}, holds something the tool cannot read. "
                "Move it away, and the tool downloads Phoenix memory again."]
    lines = [f"Phoenix memory: not on this machine yet. The tool downloads it to {place} the first "
             "time it is needed."]
    source = settings.get("phoenix_source")
    if not source:
        return lines + ["NOTE: the tool's settings name no source for Phoenix memory (phoenix_source), "
                        "so it cannot download it."]
    try:
        run = subprocess.run(["git", "ls-remote", "--exit-code", "--", source, "HEAD"], capture_output=True,
                             text=True, env=dict(env, GIT_TERMINAL_PROMPT="0"), timeout=REACH_SECONDS)
        why = (run.stderr.strip().splitlines() or ["no answer"])[-1] if run.returncode else None
    except (OSError, subprocess.TimeoutExpired) as exc:
        why = str(exc)
    if why:
        lines.append(f"NOTE: Phoenix memory's source, {source}, does not answer from here now ({why}). "
                     "The first memory command that needs Phoenix memory fails until it does.")
    return lines


def _say(report, info):
    for m in report["messages"]:
        info(f"  {m}")
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description="Lay Garura's memory system into a project, and check it.")
    ap.add_argument("--target", required=True)
    ap.add_argument("--tool", default="claude", choices=["claude", "codex"])
    ap.add_argument("--source", default=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                     "..", "..", "..", "..", "..")))
    ap.add_argument("--phoenix-place", default=PHOENIX_PLACE)
    ap.add_argument("--phoenix-source", default=PHOENIX_SOURCE)
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args(argv)
    target = os.path.abspath(args.target)
    if not os.path.isdir(target):
        print(f"memory_system.py: target is not a folder: {target}", file=sys.stderr)
        return 2
    if not args.check_only:
        lay(os.path.abspath(args.source), target, args.tool, args.phoenix_place, args.phoenix_source)
    report = check(target)
    if not report["ok"]:
        print("memory_system.py: the memory check failed (see above).", file=sys.stderr)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
