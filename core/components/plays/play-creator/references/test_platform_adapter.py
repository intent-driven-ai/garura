#!/usr/bin/env python3
"""
test_platform_adapter.py — fixture tests for platform_adapter.py (#484).

Tests the DETERMINISTIC layer: platform + repo resolution from config and argv
construction per verb (the live gh/glab calls in dispatch() are not exercised —
no network/auth in a fixture run). The argv-list construction is exactly what
makes the script correct and injection-safe, so that is what we pin.

    python3 test_platform_adapter.py
"""

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import platform_adapter as pa  # noqa: E402

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


def _cfg(text):
    fd, path = tempfile.mkstemp(suffix=".yaml")
    os.write(fd, text.encode())
    os.close(fd)
    return path


def test_resolve_platform():
    print("test_resolve_platform")
    gh = _cfg("project:\n  name: X\nplatform: github\ngithub:\n  owner: o\n  name: n\n")
    gl = _cfg("platform: gitlab\ngitlab:\n  owner: g/sub\n  name: proj\n")
    none = _cfg("project:\n  name: X\n")
    check("reads github", pa.resolve_platform(gh) == "github")
    check("reads gitlab", pa.resolve_platform(gl) == "gitlab")
    check("defaults github when absent", pa.resolve_platform(none) == "github")
    check("missing file → github", pa.resolve_platform("/no/such") == "github")
    check("repo owner/name parsed", pa.resolve_repo(gh) == ("o", "n"))
    # trailing inline comment must be stripped
    c = _cfg("github:\n  owner: kapilvirenahuja   # handle\n  name: garura\n")
    check("owner strips inline comment", pa.resolve_repo(c) == ("kapilvirenahuja", "garura"))
    for p in (gh, gl, none, c):
        os.unlink(p)


def test_github_argv():
    print("test_github_argv")
    repo = ("o", "n")
    check("view-pr argv",
          pa._gh("view-pr", {"pr_number": 489}, repo)[0][:4]
          == ["gh", "pr", "view", "489"])
    check("merge-pr argv",
          pa._gh("merge-pr", {"pr_number": "489"}, repo)
          == [["gh", "pr", "merge", "489", "--merge"]])
    check("comment-pr keeps body as ONE argv element (injection-safe)",
          pa._gh("comment-pr", {"pr_number": 1, "body": 'a "$(rm -rf /)" b'}, repo)[0]
          == ["gh", "pr", "comment", "1", "--body", 'a "$(rm -rf /)" b'])
    # create-pr optional flags
    base = pa._gh("create-pr", {"title": "t", "body": "b", "base": "main"}, repo)[0]
    check("create-pr without options has no --draft/--label",
          "--draft" not in base and "--label" not in base and base[:3] == ["gh", "pr", "create"])
    full = pa._gh("create-pr", {"title": "t", "body": "b", "base": "main",
                                "draft": "true", "label": "L", "assignee": "@me"}, repo)[0]
    check("create-pr with options appends them",
          "--draft" in full and "L" in full and "@me" in full)
    check("close-issue default reason completed",
          "completed" in pa._gh("close-issue", {"issue_number": 5}, repo)[0])
    check("update-comment uses repo api path",
          pa._gh("update-comment", {"comment_id": 9, "body": "x"}, repo)[0][2]
          == "repos/o/n/issues/comments/9")


def test_view_issue_fields():
    repo = ("o", "r")
    tree = pa._gh("view-issue", {"issue_number": 7}, repo)[0]
    check("view-issue asks for the tree fields by default",
          tree[-1] == pa.ISSUE_BASE_FIELDS + "," + pa.ISSUE_TREE_FIELDS)
    base = pa._gh("view-issue", {"issue_number": 7, "_tree": False}, repo)[0]
    check("view-issue falls back to base fields on an old gh",
          base[-1] == pa.ISSUE_BASE_FIELDS)
    check("tree fields name type, parent and sub-issues",
          all(f in pa.ISSUE_TREE_FIELDS for f in ("issueType", "parent", "subIssues")))
    check("parse gh 2.102.0", pa.parse_gh_version("gh version 2.102.0 (2026-09-30)\n") == (2, 102, 0))
    check("unparseable version is None", pa.parse_gh_version("nonsense") is None)
    check("gh 2.94.0 supports the tree", pa.gh_supports_issue_tree((2, 94, 0)))
    check("gh 2.83.2 does not", not pa.gh_supports_issue_tree((2, 83, 2)))
    check("unknown version does not", not pa.gh_supports_issue_tree(None))


def test_gitlab_argv():
    print("test_gitlab_argv")
    repo = ("g", "p")
    check("view-pr → glab mr view",
          pa._glab("view-pr", {"pr_number": 7}, repo)
          == [["glab", "mr", "view", "7", "--output", "json"]])
    check("request-changes → two commands (draft + note)",
          len(pa._glab("request-changes", {"pr_number": 7, "body": "b"}, repo)) == 2)
    check("close-issue has no --reason (gap)",
          "--reason" not in pa._glab("close-issue", {"issue_number": 5}, repo)[0])


def test_unknown_verb():
    print("test_unknown_verb")
    try:
        pa._gh("no-such", {}, (None, None))
        check("unknown verb raises", False)
    except KeyError:
        check("unknown verb raises", True)
    check("VERBS has exactly 16", len(pa.VERBS) == 16)


def main():
    test_resolve_platform()
    test_github_argv()
    test_view_issue_fields()
    test_gitlab_argv()
    test_unknown_verb()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
