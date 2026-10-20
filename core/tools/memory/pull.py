#!/usr/bin/env python3
"""
pull.py — the memory tool's Phoenix side, on a git repository (contract version 5).

The memory tool's one entry is memory.py. It calls these functions with its settings; this
file has no command line of its own.

Phoenix memory is a git repository on disk, read only at its approved version: the commit
its ref names (default origin/main — a change reaches it when a person merges it, outside
this tool). Working-tree edits and unmerged commits are never read. Its place comes from
the tool's settings — never from a fixed path. When the place is empty, the first command
that needs Phoenix memory downloads it there from its source (download).

The tool reads Phoenix memory and never copies a file from it (ADR 039). A project's Garura
memory is built from only the part it needs, by initialize and by promotion — not here.

Standard library only, Python 3.10 or newer.
"""

import os
import re
import shutil
import signal
import subprocess
import tempfile

CONTRACT_VERSION = "5"
SAFE_PATH = re.compile(r"^(?!/)(?!.*\.\.)[^\\\n\r]+\Z")
DOWNLOAD_SECONDS = 600  # the longest a first-use download may take


class Refusal(Exception):
    """An answer the contract gives as an error."""

    def __init__(self, code, message, tier=None):
        super().__init__(message)
        self.code, self.message, self.tier = code, message, tier


def error(command, refusal):
    return {"ok": False, "contract_version": CONTRACT_VERSION, "command": command,
            "error": {"code": refusal.code, "message": refusal.message, "tier": refusal.tier}}


def glob_regex(pattern):
    """A shell-style glob as a regex over '/'-separated paths: * within one folder,
    ** any depth, ? one character."""
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("".join(out) + r"\Z")


def git(phoenix, *args):
    return subprocess.run(["git", "-C", phoenix, *args], capture_output=True)


def run_limited(cmd, seconds, env):
    """Run a command for at most `seconds`. At the limit it is stopped with every process it
    started (git's network and password helpers too), so none is left waiting. Returns
    (exit code, stderr), or (None, b"") when it hit the limit."""
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=env,
                            start_new_session=True)
    try:
        _, err = proc.communicate(timeout=seconds)
        return proc.returncode, err
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except OSError:
            pass
        proc.communicate()
        return None, b""


def download(source, phoenix):
    """Download Phoenix memory to its place on this machine, the first time it is needed.
    It is cloned beside the place and moved in whole, so a cut-off download never looks like
    Phoenix memory, and two first runs at once keep one copy."""
    parent = os.path.dirname(os.path.abspath(phoenix))
    try:
        os.makedirs(parent, exist_ok=True)
        part = tempfile.mkdtemp(prefix=".phoenix-memory-download-", dir=parent)
    except OSError as exc:
        raise Refusal("tier_missing", f"Phoenix memory is not on this machine, and there is no room "
                      f"to download it: {exc}.", "phoenix") from exc
    # never wait for a password nobody is there to type, nor on a stalled network: fail and say so
    code, err = run_limited(["git", "clone", "--quiet", "--", source, part], DOWNLOAD_SECONDS,
                            dict(os.environ, GIT_TERMINAL_PROMPT="0"))
    if code is None:
        why = [f"no answer from {source} within {DOWNLOAD_SECONDS} seconds"]
    else:
        why = err.decode(errors="replace").strip().splitlines() if code else None
    if why is not None:
        shutil.rmtree(part, ignore_errors=True)
        raise Refusal("tier_missing", "Phoenix memory is not on this machine, and downloading it "
                      f"failed: {why[-1] if why else 'git clone failed'}.", "phoenix")
    try:
        os.rename(part, phoenix)
    except OSError as exc:
        shutil.rmtree(part, ignore_errors=True)
        if not os.path.isdir(phoenix):  # not another first run that got there first: say why
            raise Refusal("tier_missing", "Phoenix memory was downloaded but could not be put in "
                          f"its place, {phoenix}: {exc}.", "phoenix") from exc


def version(phoenix, ref="HEAD"):
    """Phoenix memory's version: the commit its approved ref is at."""
    run = git(phoenix, "rev-parse", "--short=12", "--verify", "--quiet", ref + "^{commit}")
    if run.returncode != 0 or not run.stdout.strip():
        raise Refusal("tier_missing", f"Phoenix memory has no approved version at {ref!r} "
                      "(not a git repository, or no such commit).", "phoenix")
    return run.stdout.decode().strip()


def files(phoenix, ref="HEAD"):
    """Every file in Phoenix memory at the approved ref, as paths relative to its root."""
    run = git(phoenix, "ls-tree", "-r", "--name-only", "-z", ref)
    if run.returncode != 0:
        raise Refusal("tier_missing", f"Phoenix memory cannot be listed at {ref!r}.", "phoenix")
    return sorted(p for p in run.stdout.decode().split("\0") if p)


def show(phoenix, rel, ref="HEAD"):
    """The bytes of one file in Phoenix memory at the approved ref, or None."""
    run = git(phoenix, "cat-file", "blob", f"{ref}:{rel}")
    return run.stdout if run.returncode == 0 else None
