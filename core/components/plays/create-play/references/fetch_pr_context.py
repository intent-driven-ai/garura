#!/usr/bin/env python3
"""
fetch_pr_context.py — check-change Step 1 as a script (#484).

Fetches the PR diff, changed paths, and base ref (via platform_adapter.py) and
binds the standards_order from config — writing context.yaml + pr.diff. Zero
judgment; the category assessment and design-grounding that follow stay
agent-run. It names no memory folder: the change-reviewer agent fetches the
review playbooks (knowledge/review/*.md) through the memory tool.

    python3 fetch_pr_context.py --config .garura/core/config.yaml \
        [--pr-number N] --out-context <context.yaml> --out-diff <pr.diff>

When the host refuses the one diff because the PR changes more than 300 files, the diff is
read as the compare diff of the PR's base and head branches (`compare-diff`), which has no
file limit; a diff that large can drop the connection, so the call gets three tries. When
all three fail, the diff is built from the host's list of the PR's files
(`pr-files`, at most 3000), each with its patch; a file the host gives no patch for keeps
its header and a note.

context.yaml records: standards_order, changed_paths,
changed_files_reported, base, diff_source (diff-pr, compare-diff or pr-files). changed_paths comes from the diff text: one path
for each `diff --git` header, so a PR of any size gives every path.
changed_files_reported is the count the host gives (null when it gives none).
Exit 0 on success, 1 on a fetch failure, 3 when the host's count and the count
of paths in the diff do not agree (then no context file is written).
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import platform_adapter as pa  # noqa: E402


def _config_value(config_path, dotted):
    """Read a simple scalar or inline list by a shallow 'a.b' path from config yaml.
    Deliberately tiny — avoids a yaml dep; handles the two keys we need."""
    keys = dotted.split(".")
    try:
        with open(config_path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except FileNotFoundError:
        return None
    depth = 0
    for i, line in enumerate(lines):
        stripped = line.rstrip("\n")
        m = re.match(rf"^{'  ' * depth}({re.escape(keys[depth])}):\s*(.*)$", stripped)
        if m:
            if depth == len(keys) - 1:
                val = m.group(2).strip()
                if val.startswith("["):
                    return [v.strip().strip("\"'") for v in
                            val.strip("[]").split(",") if v.strip()]
                return val.strip("\"'").split("#")[0].strip() or None
            depth += 1
    return None


_HEADER = re.compile(r'^diff --git (?:a/(.*?)|"a/((?:[^"\\]|\\.)*)") '
                     r'(?:b/(.*)|"b/((?:[^"\\]|\\.)*)")$')


def _unquote(text):
    """Undo git's C-style quoting of a path in a diff header."""
    raw = text.encode("latin-1", "backslashreplace").decode("unicode_escape")
    try:
        return raw.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return raw


def paths_from_diff(diff_text):
    """Return the b-side path of each `diff --git` header, unique, in diff order."""
    seen, out = set(), []
    for line in diff_text.splitlines():
        if not line.startswith("diff --git "):
            continue
        m = _HEADER.match(line)
        if not m:
            continue
        if m.group(3) is not None:
            path = m.group(3)
        else:
            path = _unquote(m.group(4))
        if path and path not in seen:
            seen.add(path)
            out.append(path)
    return out


TOO_MANY_FILES = ("exceeded the maximum number of files", "too_large")
COMPARE_TRIES = 3


def _side(prefix, path):
    """One side of a diff header, quoted the way git quotes a path with a space."""
    return f'"{prefix}{path}"' if " " in path else f"{prefix}{path}"


def diff_from_files(lines):
    """A unified diff built from the host's file list (one JSON object a line), for a PR
    whose single diff the host refuses: each file's header and its patch, or a note when
    the host gives no patch for it (a very large or binary file)."""
    out = []
    for line in lines.splitlines():
        if not line.strip():
            continue
        f = json.loads(line)
        new = f["filename"]
        old = f.get("previous_filename") or new
        out.append(f"diff --git {_side('a/', old)} {_side('b/', new)}")
        out.append("--- /dev/null" if f.get("status") == "added" else f"--- {_side('a/', old)}")
        out.append("+++ /dev/null" if f.get("status") == "removed" else f"+++ {_side('b/', new)}")
        patch = f.get("patch")
        out.append(patch if patch else "# changes not shown: the host gives no patch for this file "
                   "(it is very large or binary)")
    return "\n".join(out) + "\n"


def reported_count(data):
    """The host's count of changed files, or None when it gives none."""
    value = data.get("changedFiles")
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--pr-number", default="")
    ap.add_argument("--out-context", required=True)
    ap.add_argument("--out-diff", required=True)
    ns = ap.parse_args(argv)

    pr = ns.pr_number
    if not pr:
        res = pa.dispatch("view-pr", {"pr_number": ""}, config_path=ns.config)
        if res["exit_code"] == 0 and res["stdout"].strip():
            pr = str(json.loads(res["stdout"]).get("number", ""))
    if not pr:
        sys.stderr.write("fetch_pr_context.py: no open PR for the branch\n")
        sys.exit(1)

    meta = pa.dispatch("view-pr", {"pr_number": pr}, config_path=ns.config)
    if meta["exit_code"] != 0:
        sys.stderr.write(f"fetch_pr_context.py: view-pr failed: {meta['stderr']}\n")
        sys.exit(1)
    data = json.loads(meta["stdout"])
    base = data.get("baseRefName", "main")
    head = data.get("headRefName")
    changed_files_reported = reported_count(data)

    diff = pa.dispatch("diff-pr", {"pr_number": pr}, config_path=ns.config)
    source = "diff-pr"
    if diff["exit_code"] != 0 and any(s in diff["stderr"] for s in TOO_MANY_FILES):
        # the host gives one diff for at most 300 files; the compare diff of the two
        # branches has no file limit, and the file list (at most 3000) is the second try
        # a diff this large can drop the connection part way, so the call gets three tries
        compared = {"exit_code": 1}
        for _ in range(COMPARE_TRIES if head else 0):
            compared = pa.dispatch("compare-diff", {"base": base, "head": head},
                                   config_path=ns.config)
            if compared["exit_code"] == 0:
                break
        if compared["exit_code"] == 0:
            diff, source = compared, "compare-diff"
        else:
            files = pa.dispatch("pr-files", {"pr_number": pr}, config_path=ns.config)
            if files["exit_code"] != 0:
                sys.stderr.write(f"fetch_pr_context.py: pr-files failed: {files['stderr']}\n")
                sys.exit(1)
            diff, source = {"exit_code": 0, "stdout": diff_from_files(files["stdout"])}, "pr-files"
    if diff["exit_code"] != 0:
        sys.stderr.write(f"fetch_pr_context.py: diff-pr failed: {diff['stderr']}\n")
        sys.exit(1)
    changed_paths = paths_from_diff(diff["stdout"])
    if changed_files_reported is not None and \
            changed_files_reported != len(changed_paths):
        sys.stderr.write(
            f"fetch_pr_context.py: the host says the PR changes "
            f"{changed_files_reported} files, but the diff shows "
            f"{len(changed_paths)} files. The review cannot read every file, "
            f"so no context file is written.\n")
        sys.exit(3)
    with open(ns.out_diff, "w", encoding="utf-8") as fh:
        fh.write(diff["stdout"])

    standards_order = _config_value(ns.config, "review-pr.standards_order") or \
        ["kb", "ltm", "stm"]

    context = {"pr_number": pr, "base": base, "changed_paths": changed_paths,
               "changed_files_reported": changed_files_reported,
               "diff_source": source, "standards_order": standards_order}
    with open(ns.out_context, "w", encoding="utf-8") as fh:
        json.dump(context, fh, indent=2)
    print(json.dumps(context, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
