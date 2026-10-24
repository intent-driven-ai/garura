#!/usr/bin/env python3
"""
tools_system.py — lay Garura's tools into a project (decision 6 of #860).

Both install paths call this: the install-garura play (install.py) and the public installer
(installer/install.sh). Plays, loops, agents and skills run the tools after the install, so
every tool goes to the project's install folder, and an installed part names only that place:

  .garura/core/tools/<name>/   one folder for each tool of the Garura checkout

The memory tool is laid by memory_system.py (it also writes settings and the guide), so this
script leaves it out. The play-reviewer prototype is never laid. Test files (test_*.py,
*.test.js, a tool's own test/ folder) and caches are not laid. A tool's node_modules is
laid as it is, so a Node tool runs with no install step.

A re-install replaces each tool whole. The install manifest records each tool's folder, so a
re-install removes a tool that left the source, and uninstall removes them all.

    python3 tools_system.py --target <project> [--source <garura checkout>]

Prints the laid folders as JSON. Exit: 0 = laid, 2 = bad input. Standard library only.
"""

import argparse
import json
import os
import shutil
import sys

TOOLS_DEST = os.path.join(".garura", "core", "tools")
NOT_LAID = {"memory", "play-reviewer"}  # memory: memory_system.py; play-reviewer: a prototype
CACHES = {"__pycache__", ".ruff_cache", ".pytest_cache", ".mypy_cache"}


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


def lay(source, target, info=print):
    """Lay every tool; return the project-relative folder of each, for the install manifest."""
    laid = []
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
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        os.rename(new, dest)
        laid.append(os.path.join(TOOLS_DEST, name))
    if laid:
        info(f"  tools: {', '.join(os.path.basename(p) for p in laid)} in {TOOLS_DEST}")
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
    print(json.dumps(lay(source, target, info=lambda m: print(m, file=sys.stderr))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
