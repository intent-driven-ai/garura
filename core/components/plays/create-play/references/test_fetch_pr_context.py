#!/usr/bin/env python3
"""
test_fetch_pr_context.py — tests for fetch_pr_context.py (#841).

A fake adapter answers view-pr and diff-pr, so no host is called. The tests
cover a PR of more than 100 files, a quoted diff header, and the count
mismatch (exit 3, no context file).

    python3 test_fetch_pr_context.py
"""

import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_pr_context as fpc  # noqa: E402

PASSED = 0
FAILED = 0


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")


def _diff_for(paths):
    parts = []
    for p in paths:
        parts.append(f"diff --git a/{p} b/{p}\nindex 1111111..2222222 100644\n"
                     f"--- a/{p}\n+++ b/{p}\n@@ -1 +1 @@\n-old\n+new\n")
    return "".join(parts)


def _run(view_data, diff_text):
    """Run main() with a fake adapter. Return (exit code, context or None, stderr)."""
    def fake_dispatch(verb, args, config_path=None):
        if verb == "view-pr":
            return {"exit_code": 0, "stdout": json.dumps(view_data), "stderr": ""}
        if verb == "diff-pr":
            return {"exit_code": 0, "stdout": diff_text, "stderr": ""}
        return {"exit_code": 1, "stdout": "", "stderr": "unexpected verb"}

    real = fpc.pa.dispatch
    fpc.pa.dispatch = fake_dispatch
    tmp = tempfile.mkdtemp()
    ctx_path = os.path.join(tmp, "context.yaml")
    diff_path = os.path.join(tmp, "pr.diff")
    err = io.StringIO()
    code = None
    try:
        with redirect_stdout(io.StringIO()), redirect_stderr(err):
            fpc.main(["--config", os.path.join(tmp, "none.yaml"), "--pr-number", "7",
                      "--out-context", ctx_path, "--out-diff", diff_path])
    except SystemExit as exc:
        code = exc.code
    finally:
        fpc.pa.dispatch = real
    ctx = None
    if os.path.exists(ctx_path):
        with open(ctx_path, encoding="utf-8") as fh:
            ctx = json.load(fh)
    return code, ctx, err.getvalue()


def test_large_pr():
    print("A PR of 150 files gives all 150 paths")
    paths = [f"core/dir{i // 10}/file{i}.md" for i in range(150)]
    # The host's file list stops at 100; the paths must come from the diff.
    view = {"number": 7, "baseRefName": "main", "changedFiles": 150,
            "files": [{"path": p} for p in paths[:100]]}
    code, ctx, _ = _run(view, _diff_for(paths))
    check("exit 0", code == 0)
    check("150 changed paths", ctx is not None and len(ctx["changed_paths"]) == 150)
    check("paths in diff order", ctx is not None and ctx["changed_paths"] == paths)
    check("changed_files_reported is 150",
          ctx is not None and ctx["changed_files_reported"] == 150)
    check("context names no memory folder (#860)",
          ctx is not None and "review_shelf" not in ctx
          and ".garura/core/memory" not in json.dumps(ctx))


def test_mismatch():
    print("A count that does not agree stops the script")
    paths = [f"a{i}.txt" for i in range(5)]
    view = {"number": 7, "baseRefName": "main", "changedFiles": 6}
    code, ctx, err = _run(view, _diff_for(paths))
    check("exit 3", code == 3)
    check("no context file", ctx is None)
    check("message names both numbers", "6" in err and "5" in err)


def test_no_count():
    print("A host that gives no count gives null")
    view = {"number": 7, "baseRefName": "main"}
    code, ctx, _ = _run(view, _diff_for(["x.py", "y.py"]))
    check("exit 0", code == 0)
    check("changed_files_reported is null",
          ctx is not None and ctx["changed_files_reported"] is None)


def test_header_forms():
    print("Header forms: quoted, rename, repeat")
    diff = ('diff --git "a/docs/my file\\303\\251.md" "b/docs/my file\\303\\251.md"\n'
            "--- a/x\n+++ b/x\n"
            "diff --git a/old/name.py b/new/name.py\n"
            "diff --git a/x.py b/x.py\n"
            "diff --git a/x.py b/x.py\n")
    got = fpc.paths_from_diff(diff)
    check("quoted header read", got[0] == "docs/my fileé.md")
    check("b side of a rename", got[1] == "new/name.py")
    check("unique", got == ["docs/my fileé.md", "new/name.py", "x.py"])


if __name__ == "__main__":
    test_large_pr()
    test_mismatch()
    test_no_count()
    test_header_forms()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)
