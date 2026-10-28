#!/usr/bin/env python3
"""test_fetch_pr_context.py — the PR context of check-change Step 1: the diff, and the fallbacks
when the PR changes more than 300 files: the compare diff of its branches, then the host's file
list.

    python3 core/components/plays/check-change/scripts/test_fetch_pr_context.py
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_pr_context as fpc  # noqa: E402

PASSED = 0
FAILED = 0
HEADS = []


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")


FILES = [
    {"filename": "core/a.py", "status": "modified", "patch": "@@ -1 +1 @@\n-x\n+y"},
    {"filename": "docs/new page.md", "status": "added", "patch": "@@ -0,0 +1 @@\n+hello"},
    {"filename": "big/records.jsonl", "status": "added"},
    {"filename": "core/b.py", "previous_filename": "core/old_b.py", "status": "renamed", "patch": ""},
    {"filename": "gone.txt", "status": "removed", "patch": "@@ -1 +0,0 @@\n-bye"},
]


def run_main(responses, tmp):
    """Run main() with the host's answers stubbed; return (exit code, context or None)."""
    calls = []
    fpc.COMPARE_PAUSE = 0

    def dispatch(verb, args, config_path=None):
        calls.append(verb)
        if verb == "compare-diff":
            HEADS.append(args["head"])
        answer = responses[verb]
        return answer.pop(0) if isinstance(answer, list) else answer

    real = fpc.pa.dispatch
    fpc.pa.dispatch = dispatch
    ctx, diff = os.path.join(tmp, "context.yaml"), os.path.join(tmp, "pr.diff")
    try:
        fpc.main(["--config", os.path.join(tmp, "none.yaml"), "--pr-number", "900",
                  "--out-context", ctx, "--out-diff", diff])
    except SystemExit as exc:
        code = exc.code
    finally:
        fpc.pa.dispatch = real
    out = json.load(open(ctx)) if os.path.isfile(ctx) else None
    return code, out, calls


def main():
    text = fpc.diff_from_files("\n".join(json.dumps(f) for f in FILES) + "\n")
    paths = fpc.paths_from_diff(text)
    check("diff from the file list: one header for each file, in the host's order",
          paths == ["core/a.py", "docs/new page.md", "big/records.jsonl", "core/b.py", "gone.txt"])
    check("a file the host gives no patch for keeps its header and a note",
          "diff --git a/big/records.jsonl b/big/records.jsonl" in text
          and "changes not shown" in text)
    check("an added file reads from /dev/null, a removed one to /dev/null, a renamed one from its old path",
          "--- /dev/null\n+++ b/docs/new page.md" not in text  # a path with a space is quoted
          and '--- /dev/null\n+++ "b/docs/new page.md"' in text
          and "--- a/gone.txt\n+++ /dev/null" in text and "--- a/core/old_b.py" in text)
    check("the patch is kept as the host gives it", "@@ -1 +1 @@\n-x\n+y" in text)

    view = {"exit_code": 0, "stdout": json.dumps({"baseRefName": "plan/1/base",
                                                  "headRefName": "feature/1-x", "changedFiles": 5}),
            "stderr": ""}
    too_big = {"exit_code": 1, "stdout": "",
               "stderr": "HTTP 406: Sorry, the diff exceeded the maximum number of files (300)."}
    files = {"exit_code": 0, "stdout": "\n".join(json.dumps(f) for f in FILES) + "\n", "stderr": ""}
    compared = {"exit_code": 0, "stdout": text, "stderr": ""}
    no_compare = {"exit_code": 1, "stdout": "", "stderr": "HTTP 404: Not Found"}
    with tempfile.TemporaryDirectory() as tmp:
        code, ctx, calls = run_main({"view-pr": view, "diff-pr": too_big, "compare-diff": compared,
                                     "pr-files": files}, tmp)
        check("over 300 files: the context is built from the compare diff (exit 0)",
              code == 0 and ctx["diff_source"] == "compare-diff" and len(ctx["changed_paths"]) == 5
              and calls == ["view-pr", "diff-pr", "compare-diff"])
    with tempfile.TemporaryDirectory() as tmp:
        many = [f"records/r{i}.json" for i in range(3192)]
        big_text = "".join(f"diff --git a/{p} b/{p}\n--- /dev/null\n+++ b/{p}\n" for p in many)
        big_view = {"exit_code": 0, "stdout": json.dumps({"baseRefName": "main", "headRefName": "plan/1/base",
                                                         "changedFiles": 3192}), "stderr": ""}
        code, ctx, calls = run_main({"view-pr": big_view, "diff-pr": too_big,
                                     "compare-diff": {"exit_code": 0, "stdout": big_text, "stderr": ""}}, tmp)
        check("over 3000 files (past the file list's limit): every path comes from the compare diff",
              code == 0 and ctx["diff_source"] == "compare-diff" and len(ctx["changed_paths"]) == 3192
              and "pr-files" not in calls)
    with tempfile.TemporaryDirectory() as tmp:
        code, ctx, calls = run_main({"view-pr": view, "diff-pr": too_big, "compare-diff": no_compare,
                                     "pr-files": files}, tmp)
        check("a compare call the host cannot answer (not found) stops at once and falls back to the file list",
              code == 0 and ctx["diff_source"] == "pr-files" and len(ctx["changed_paths"]) == 5
              and calls == ["view-pr", "diff-pr", "compare-diff", "pr-files"])
    with tempfile.TemporaryDirectory() as tmp:
        dropped = {"exit_code": 1, "stdout": "", "stderr": "stream error: stream ID 3; CANCEL"}
        code, ctx, calls = run_main({"view-pr": view, "diff-pr": too_big,
                                     "compare-diff": [dropped, dropped, dropped], "pr-files": files}, tmp)
        check("a compare call that drops three times falls back to the file list",
              code == 0 and ctx["diff_source"] == "pr-files"
              and calls == ["view-pr", "diff-pr"] + ["compare-diff"] * 3 + ["pr-files"])
    with tempfile.TemporaryDirectory() as tmp:
        not_here = {"exit_code": 2, "stdout": "", "stderr": "compare-diff works on GitHub only"}
        code, ctx, calls = run_main({"view-pr": view, "diff-pr": too_big, "compare-diff": not_here,
                                     "pr-files": files}, tmp)
        check("a host without the compare command (exit 2) is not tried again",
              code == 0 and ctx["diff_source"] == "pr-files" and calls.count("compare-diff") == 1)
    with tempfile.TemporaryDirectory() as tmp:
        fork = {"exit_code": 0, "stdout": json.dumps({"baseRefName": "main", "headRefName": "fix-x",
                                                     "isCrossRepository": True,
                                                     "headRepositoryOwner": {"login": "someone"},
                                                     "changedFiles": 5}), "stderr": ""}
        HEADS.clear()
        code, ctx, _ = run_main({"view-pr": fork, "diff-pr": too_big, "compare-diff": compared}, tmp)
        check("a PR from a fork names its head with the fork's owner (someone:fix-x)",
              code == 0 and HEADS == ["someone:fix-x"])
    with tempfile.TemporaryDirectory() as tmp:
        HEADS.clear()
        run_main({"view-pr": view, "diff-pr": too_big, "compare-diff": compared}, tmp)
        check("a PR from the same repository names its head by branch only", HEADS == ["feature/1-x"])
    with tempfile.TemporaryDirectory() as tmp:
        dropped = {"exit_code": 1, "stdout": "", "stderr": "stream error: stream ID 3; CANCEL"}
        code, ctx, calls = run_main({"view-pr": view, "diff-pr": too_big,
                                     "compare-diff": [dropped, dropped, compared]}, tmp)
        check("a dropped compare call is tried again, up to three times",
              code == 0 and ctx["diff_source"] == "compare-diff" and calls.count("compare-diff") == 3
              and "pr-files" not in calls)
    with tempfile.TemporaryDirectory() as tmp:
        no_head = {"exit_code": 0, "stdout": json.dumps({"baseRefName": "main", "changedFiles": 5}),
                   "stderr": ""}
        code, ctx, calls = run_main({"view-pr": no_head, "diff-pr": too_big, "pr-files": files}, tmp)
        check("with no head branch named, the compare call is skipped and the file list is used",
              code == 0 and ctx["diff_source"] == "pr-files" and "compare-diff" not in calls)
    with tempfile.TemporaryDirectory() as tmp:
        short_cmp = {"exit_code": 0, "stdout": fpc.diff_from_files(
            "\n".join(json.dumps(f) for f in FILES[:4]) + "\n"), "stderr": ""}
        code, ctx, _ = run_main({"view-pr": view, "diff-pr": too_big, "compare-diff": short_cmp}, tmp)
        check("the compare diff still has to match the host's count, or no context is written (exit 3)",
              code == 3 and ctx is None)
    with tempfile.TemporaryDirectory() as tmp:
        short = {"exit_code": 0, "stdout": "\n".join(json.dumps(f) for f in FILES[:4]) + "\n", "stderr": ""}
        code, ctx, _ = run_main({"view-pr": view, "diff-pr": too_big, "compare-diff": no_compare,
                                 "pr-files": short}, tmp)
        check("the file list still has to match the host's count, or no context is written (exit 3)",
              code == 3 and ctx is None)
    with tempfile.TemporaryDirectory() as tmp:
        other = {"exit_code": 1, "stdout": "", "stderr": "HTTP 404: Not Found"}
        code, ctx, calls = run_main({"view-pr": view, "diff-pr": other}, tmp)
        check("any other diff failure stops as before, with no fallback (exit 1)",
              code == 1 and ctx is None and "pr-files" not in calls and "compare-diff" not in calls)
    with tempfile.TemporaryDirectory() as tmp:
        ok = {"exit_code": 0, "stdout": text, "stderr": ""}
        code, ctx, calls = run_main({"view-pr": view, "diff-pr": ok}, tmp)
        check("a PR the host gives one diff for uses it (diff_source diff-pr)",
              code == 0 and ctx["diff_source"] == "diff-pr" and "pr-files" not in calls)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
