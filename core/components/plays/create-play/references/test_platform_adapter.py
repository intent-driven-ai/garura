#!/usr/bin/env python3
"""
test_platform_adapter.py — fixture tests for platform_adapter.py (#484).

Tests the DETERMINISTIC layer: platform + repo resolution from config, argv
construction per verb, and dispatch()'s view-issue version probe with the command
runner stubbed. No live gh/glab call runs — no network/auth in a fixture run. The argv-list construction is exactly what
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
    check("pr-files lists every file of the PR through the api, page by page",
          pa._gh("pr-files", {"pr_number": 900}, repo)
          == [["gh", "api", "repos/o/n/pulls/900/files", "--paginate", "--jq", ".[] | @json"]])
    check("compare-diff asks the compare api for the plain diff of the two branches",
          pa._gh("compare-diff", {"base": "main", "head": "plan/788/base"}, repo)
          == [["gh", "api", "repos/o/n/compare/main...plan/788/base",
               "-H", "Accept: application/vnd.github.diff"]])
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


def test_view_issue_version_probe():
    """dispatch() probes `gh --version` and picks the field list (QF-13)."""
    real_run, real_repo = pa._run, pa.resolve_repo
    for version_line, want_tree in (("gh version 2.102.0 (2026-09-30)", True),
                                    ("gh version 2.83.2 (2025-12-10)", False),
                                    ("", False)):
        calls = []

        def fake_run(argv, _v=version_line):
            calls.append(argv)
            if argv[:2] == ["gh", "--version"]:
                return (0 if _v else 1), _v, ""
            return 0, "{}", ""
        pa._run, pa.resolve_repo = fake_run, (lambda _cfg: ("o", "r"))
        try:
            res = pa.dispatch("view-issue", {"issue_number": 7}, platform="github")
        finally:
            pa._run, pa.resolve_repo = real_run, real_repo
        view = calls[-1]
        label = version_line or "no gh version"
        check(f"{label}: probes gh --version first", calls[0][:2] == ["gh", "--version"])
        check(f"{label}: tree fields {'asked' if want_tree else 'not asked'}",
              ("issueType" in view[-1]) == want_tree)
        check(f"{label}: tree_available is {want_tree}", res["tree_available"] is want_tree)

    calls = []

    def fake_glab(argv):
        calls.append(argv)
        return 0, "{}", ""
    pa._run, pa.resolve_repo = fake_glab, (lambda _cfg: ("o", "r"))
    try:
        res = pa.dispatch("view-issue", {"issue_number": 7}, platform="gitlab")
    finally:
        pa._run, pa.resolve_repo = real_run, real_repo
    check("gitlab: no gh --version probe", all(c[:1] != ["gh"] for c in calls))
    check("gitlab: tree_available is False", res["tree_available"] is False)


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
    check("VERBS has exactly 23", len(pa.VERBS) == 23)


def _fake(replies):
    """A runner that records each argv and answers from `replies` (a list of (rc, out))."""
    calls = []

    def run(argv):
        calls.append(argv)
        rc, out = replies.pop(0) if replies else (0, "")
        return rc, out, "" if rc == 0 else "it broke"
    return calls, run


def test_github_only_verbs():
    print("test_github_only_verbs")
    real_run, real_repo = pa._run, pa.resolve_repo
    pa.resolve_repo = lambda _cfg: ("o", "r")
    try:
        types = ('{"data":{"repository":{"id":"R1","issueTypes":{"nodes":'
                 '[{"id":"T-story","name":"Story"},{"id":"T-feat","name":"Feature"}]}}}}')
        calls, pa._run = _fake([(0, types), (0, "N-10\n"), (0, "41\n")])
        res = pa.dispatch("create-issue-typed", {"title": "A patient picks a slot", "body": "b $(x)",
                                                 "issue_type": "Story", "parent_number": "10"},
                          platform="github")
        make = calls[-1]
        check("create-issue-typed: one createIssue call with the type and the parent",
              res["exit_code"] == 0 and res["stdout"].strip() == "41" and len(calls) == 3
              and "type=T-story" in make and "parent=N-10" in make and "repo=R1" in make
              and any("createIssue" in a and "issueTypeId" in a and "parentIssueId" in a for a in make))
        check("create-issue-typed: the body is one argv element, as written", "body=b $(x)" in make)
        calls, pa._run = _fake([(0, types), (0, "7\n")])
        res = pa.dispatch("create-issue-typed", {"title": "t", "body": "b", "issue_type": "Feature"},
                          platform="github")
        check("create-issue-typed with no parent: no parent look-up, no parent field",
              res["exit_code"] == 0 and len(calls) == 2 and not any(a.startswith("parent=") for a in calls[-1]))
        calls, pa._run = _fake([(0, types)])
        res = pa.dispatch("create-issue-typed", {"title": "t", "body": "b", "issue_type": "Epic"},
                          platform="github")
        check("create-issue-typed with an unknown type: exit 1, nothing made",
              res["exit_code"] == 1 and len(calls) == 1 and "no issue type 'Epic'" in res["stderr"])
        calls, pa._run = _fake([(0, "")])
        res = pa.dispatch("set-issue-type", {"issue_number": 5, "issue_type": "Feature"}, platform="github")
        check("set-issue-type argv", calls == [["gh", "api", "-X", "PATCH", "repos/o/r/issues/5", "-f", "type=Feature"]])
        calls, pa._run = _fake([(0, "")])
        pa.dispatch("edit-issue-body", {"issue_number": 5, "body": "new `text`"}, platform="github")
        check("edit-issue-body argv", calls == [["gh", "api", "-X", "PATCH", "repos/o/r/issues/5", "-f", "body=new `text`"]])
        calls, pa._run = _fake([(0, "")])
        pa.dispatch("remove-label", {"issue_number": 5, "label": "work item"}, platform="github")
        check("remove-label argv", calls == [["gh", "issue", "edit", "5", "--remove-label", "work item"]])
        calls, pa._run = _fake([(0, "999\n"), (0, "")])
        res = pa.dispatch("remove-sub-issue", {"parent_number": 10, "child_number": 12}, platform="github")
        check("remove-sub-issue reads the child's id, then takes it off",
              res["exit_code"] == 0 and calls[0][-2:] == ["--jq", ".id"]
              and calls[1] == ["gh", "api", "/repos/o/r/issues/10/sub_issue", "-X", "DELETE", "-F", "sub_issue_id=999"])
        for verb in sorted(pa.GITHUB_ONLY_VERBS):
            calls, pa._run = _fake([])
            res = pa.dispatch(verb, {}, platform="gitlab")
            check(f"gitlab: {verb} stops with a plain message and runs nothing",
                  res["exit_code"] == 2 and calls == [] and "GitHub only" in res["stderr"])
        calls, pa._run = _fake([])
        res = pa.dispatch("compare-diff", {"base": "main", "head": "x"}, platform="gitlab")
        check("gitlab: compare-diff stops with a plain message and runs nothing",
              res["exit_code"] == 2 and calls == [] and "GitHub only" in res["stderr"])
    finally:
        pa._run, pa.resolve_repo = real_run, real_repo


def main():
    test_resolve_platform()
    test_github_argv()
    test_view_issue_fields()
    test_view_issue_version_probe()
    test_gitlab_argv()
    test_unknown_verb()
    test_github_only_verbs()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
