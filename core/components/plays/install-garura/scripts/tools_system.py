#!/usr/bin/env python3
"""
tools_system.py — lay Garura's tools into a project (decision 6 of #860).

Both install paths call this: the install-garura play (install.py) and the public installer
(installer/install.sh). Plays, loops, agents and skills run the tools after the install, so
every tool goes to the project's install folder, and an installed part names only that place:

  .garura/core/tools/<name>/   one folder for each tool of the Garura checkout

The memory tool is laid by memory_system.py (it also writes settings and the guide), so this
script leaves it out. The play-reviewer prototype is never laid, and the naming tool is not
either: it checks Garura's own repository only (decision 23). Test files (test_*.py,
*.test.js, a tool's own test/ folder) and caches are not laid.

A laid tool must run (decision 20):
  - packages: a tool with a package.json keeps the source's node_modules when the source has
    one; else the install runs `npm ci --omit=dev` (or `npm install --omit=dev` when the tool
    has no package-lock.json) in the laid folder. GARURA_NPM names another npm command.
  - smoke check: after it lays the tools, the install loads each one. A Node tool loads each
    of its packages and its main file is read (`node --check`); a Python tool imports each of
    its scripts. A tool that does not load stops the install with a message that names it.

It writes .garura/core/tools/.gitignore (node_modules/, __pycache__/), so the tools' packages
and caches stay out of a project's git (decision 24).

A re-install replaces each tool whole. The install manifest records each tool's folder and the
ignore file, so a re-install removes a tool that left the source, and uninstall removes them all.

    python3 tools_system.py --target <project> [--source <garura checkout>]

Prints the laid folders as JSON. Exit: 0 = laid, 1 = a tool did not get its packages or did
not load, 2 = bad input. Standard library only.
"""

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys

TOOLS_DEST = os.path.join(".garura", "core", "tools")
# memory: memory_system.py lays it; play-reviewer: a prototype; naming: Garura's repository only
NOT_LAID = {"memory", "play-reviewer", "naming"}
CACHES = {"__pycache__", ".ruff_cache", ".pytest_cache", ".mypy_cache"}
GITIGNORE = os.path.join(TOOLS_DEST, ".gitignore")
GITIGNORE_TEXT = ("# The tools' packages and caches, which the install lays or makes: never part of a change.\n"
                  "node_modules/\n"
                  "__pycache__/\n")
# A Node tool loads when each of its packages loads and its main file reads (node --check).
NODE_LOAD = ("const p = require('./package.json');"
             "for (const d of Object.keys(p.dependencies || {})) require(d);")


class ToolFailed(Exception):
    """A laid tool did not get its packages or did not load. `laid` is what was laid."""

    def __init__(self, failures, laid):
        self.failures = failures
        self.laid = laid
        super().__init__("; ".join(failures))


def _bad(msg):
    print(f"tools_system.py: {msg}", file=sys.stderr)
    raise SystemExit(2)


def _skip_for(tool_root):
    """The ignore function for one tool: tests and caches stay out; node_modules is kept whole."""
    def skip(folder, names):
        if f"{os.sep}node_modules" in folder or os.path.basename(folder) == "node_modules":
            return set()
        out = {n for n in names
               if n in CACHES or n.startswith("test_") or n.endswith(".test.js")}
        if os.path.abspath(folder) == tool_root:
            out |= {n for n in names if n in ("test", "tests")}
        return out
    return skip


def tool_names(source):
    """Every tool folder of the checkout that the install lays, in name order."""
    src = os.path.join(source, "core", "tools")
    if not os.path.isdir(src):
        return []
    return sorted(n for n in os.listdir(src)
                  if os.path.isdir(os.path.join(src, n)) and n not in NOT_LAID
                  and not n.startswith((".", "_")))


def npm_command():
    """The npm command (GARURA_NPM names another one, for a test or a machine without npm)."""
    return shlex.split(os.environ.get("GARURA_NPM", "npm"))


_ERROR_LINE = re.compile(r"^(?:[\w.]*(?:Error|Exception)\b|npm ERR!|npm error\b)")


def _error_line(text):
    """The line of a tool's output that says what went wrong: the first error line, else the last."""
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    return next((ln for ln in lines if _ERROR_LINE.match(ln)), lines[-1] if lines else "no message")


def get_packages(name, folder, info=print, run=subprocess.run):
    """Make sure a laid Node tool has its packages. Return None when it has them, else why not."""
    if not os.path.isfile(os.path.join(folder, "package.json")):
        return None
    if os.path.isdir(os.path.join(folder, "node_modules")):
        return None  # the source's packages were laid with the tool
    verb = "ci" if os.path.isfile(os.path.join(folder, "package-lock.json")) else "install"
    cmd = npm_command() + [verb, "--omit=dev"]
    try:
        done = run(cmd, cwd=folder, capture_output=True, text=True)
    except OSError as exc:
        return f"the tool {name} has no packages and npm cannot run ({exc})"
    if done.returncode != 0:
        return (f"the tool {name} did not get its packages: npm {verb} --omit=dev exited "
                f"{done.returncode} ({_error_line(done.stderr or done.stdout)})")
    info(f"  tools: {name}: packages from npm {verb} --omit=dev")
    return None


def smoke_commands(folder):
    """The short commands that exit 0 when the tool in `folder` loads (none for a tool with no code)."""
    if os.path.isfile(os.path.join(folder, "package.json")):
        try:
            with open(os.path.join(folder, "package.json"), encoding="utf-8") as fh:
                main = json.load(fh).get("main") or "index.js"
        except (OSError, ValueError):
            main = "index.js"
        return [["node", "-e", NODE_LOAD], ["node", "--check", main]]
    mods = sorted(n[:-3] for n in os.listdir(folder)
                  if n.endswith(".py") and not n.startswith("test_") and n[:-3].isidentifier())
    if not mods:
        return []
    return [["python3", "-B", "-c", "import sys; sys.path.insert(0, '.'); import " + ", ".join(mods)]]


def smoke(name, folder, run=subprocess.run):
    """Run the tool's smoke check. Return None when it loads, else why not."""
    for cmd in smoke_commands(folder):
        try:
            done = run(cmd, cwd=folder, capture_output=True, text=True)
        except OSError as exc:
            return f"the tool {name} does not load: {cmd[0]} cannot run ({exc})"
        if done.returncode != 0:
            return f"the tool {name} does not load: {_error_line(done.stderr or done.stdout)}"
    return None


def lay(source, target, info=print, run=subprocess.run):
    """Lay every tool, get its packages, write the ignore file and run each smoke check; return
    the project-relative folder of each tool, for the install manifest. Raise ToolFailed (after
    every tool is laid and checked) when a tool did not get its packages or does not load."""
    laid, failures = [], []
    for name in tool_names(source):
        src = os.path.abspath(os.path.join(source, "core", "tools", name))
        dest = os.path.join(target, TOOLS_DEST, name)
        new = dest + ".new"
        shutil.rmtree(new, ignore_errors=True)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            shutil.copytree(src, new, ignore=_skip_for(src), symlinks=True)
        except BaseException:
            shutil.rmtree(new, ignore_errors=True)  # never leave a half copy behind
            raise
        why = get_packages(name, new, info, run)
        if why:
            shutil.rmtree(new, ignore_errors=True)  # an older laid copy, if any, stays
            failures.append(why)
            continue
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        os.rename(new, dest)
        laid.append(os.path.join(TOOLS_DEST, name))
    os.makedirs(os.path.join(target, TOOLS_DEST), exist_ok=True)
    with open(os.path.join(target, GITIGNORE), "w", encoding="utf-8") as fh:
        fh.write(GITIGNORE_TEXT)
    if laid:
        info(f"  tools: {', '.join(os.path.basename(p) for p in laid)} in {TOOLS_DEST}")
    for rel in laid:
        why = smoke(os.path.basename(rel), os.path.join(target, rel), run)
        if why:
            failures.append(why)
    if failures:
        raise ToolFailed(failures, laid)
    info(f"  tools: each one loads (smoke check); wrote {GITIGNORE}")
    return laid


def main(argv=None):
    ap = argparse.ArgumentParser(description="Lay Garura's tools into a project.")
    ap.add_argument("--target", required=True)
    ap.add_argument("--source", default=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                     "..", "..", "..", "..", "..")))
    args = ap.parse_args(argv)
    target = os.path.abspath(args.target)
    if not os.path.isdir(target):
        _bad(f"target is not a folder: {target}")
    source = os.path.abspath(args.source)
    if not os.path.isdir(os.path.join(source, "core", "tools")):
        _bad(f"{source} has no tools folder (core/tools)")
    try:
        laid = lay(source, target, info=lambda m: print(m, file=sys.stderr))
    except ToolFailed as exc:
        for why in exc.failures:
            print(f"tools_system.py: stopped: {why}", file=sys.stderr)
        return 1
    print(json.dumps(laid))
    return 0


if __name__ == "__main__":
    sys.exit(main())
