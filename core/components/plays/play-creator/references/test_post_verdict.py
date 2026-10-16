#!/usr/bin/env python3
"""
test_post_verdict.py — fixture tests for post_verdict.py and review-change's Done means (#536).

A run that records a decision with its decider and posts it must hold the stop condition
(the close may read COMPLETED). A run that fails to post, or has no valid decision record,
must leave it unmet (the close reads HALTED). The host and git are stubbed: nothing is
posted and nothing is committed.

    python3 test_post_verdict.py
"""

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable or "python3"
sys.path.insert(0, HERE)
import post_verdict as pv  # noqa: E402

REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
PLAY = os.path.join(REPO, "core", "components", "plays", "review-change")
MANIFEST = os.path.join(PLAY, "stop-condition.yaml")

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
        if os.environ.get("PYTEST_CURRENT_TEST"):
            raise AssertionError(name)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def run_post(base, decision_text, post_ok=True, comment="Harness verdict (gate off): approve"):
    """Run post_verdict.main with the host and git stubbed. Return (exit code, posts made)."""
    review = os.path.join(base, "review")
    write(os.path.join(review, "findings.yaml"), "findings: []\n")
    if decision_text is not None:
        write(os.path.join(review, "decision.yaml"), decision_text)
    write(os.path.join(base, "decision-comment.md"), comment + "\n")
    posts = []

    def fake_dispatch(op, args, config_path=None):
        posts.append(op)
        if post_ok:
            return {"exit_code": 0, "stdout": "https://example.test/pr/1#c1\n", "stderr": ""}
        return {"exit_code": 1, "stdout": "", "stderr": "host refused"}

    real_dispatch, real_git = pv.pa.dispatch, pv._git
    pv.pa.dispatch, pv._git = fake_dispatch, (lambda *a: (0, "", ""))
    try:
        pv.main(["--pr-number", "1", "--comment-file", os.path.join(base, "decision-comment.md"),
                 "--decision", os.path.join(review, "decision.yaml"), "--issue", "536",
                 "--artifacts-dir", review, "--out", os.path.join(review, "posted.json")])
        code = 0
    except SystemExit as exc:
        code = exc.code
    finally:
        pv.pa.dispatch, pv._git = real_dispatch, real_git
    return code, posts


def stop_condition(base):
    proc = subprocess.run([PY, os.path.join(PLAY, "scripts", "check_stop_condition.py"),
                           "--manifest", MANIFEST, "--base", base + os.sep,
                           "--out", os.path.join(base, "verdict-out.yaml")],
                          capture_output=True, text=True)
    return proc.returncode


def test_posted_decision_holds():
    print("test_posted_decision_holds")
    comments = {"harness": "Harness verdict (gate off per gates.plays.review-change): reject",
                "human": "Reviewer's verdict: reject"}
    for decider, comment in comments.items():
        with tempfile.TemporaryDirectory() as base:
            code, posts = run_post(base, f"decision: reject\ndecided_by: {decider}\n", comment=comment)
            with open(os.path.join(base, "review", "posted.json"), encoding="utf-8") as fh:
                posted = json.load(fh)
            check(f"a {decider} decision posts and exits 0", code == 0 and posts == ["comment-pr"])
            check(f"posted.json carries the {decider} decision and its decider",
                  posted["decision"] == "reject" and posted["decided_by"] == decider
                  and posted["decision_recorded"] is True and posted["posted"] is True)
            check(f"the stop condition holds — the close may read COMPLETED ({decider})",
                  stop_condition(base) == 0)


def test_failed_post_stays_unmet():
    print("test_failed_post_stays_unmet")
    with tempfile.TemporaryDirectory() as base:
        code, _ = run_post(base, "decision: approve\ndecided_by: harness\n", post_ok=False)
        check("a failed post exits 1", code == 1)
        check("a failed post writes no posted.json",
              not os.path.exists(os.path.join(base, "review", "posted.json")))
        check("the stop condition is unmet — the close reads HALTED", stop_condition(base) == 1)


def test_no_valid_decision_posts_nothing():
    print("test_no_valid_decision_posts_nothing")
    cases = {
        "no decision record": None,
        "no decider": "decision: approve\n",
        "an unknown decider": "decision: approve\ndecided_by: robot\n",
        "no decision": "decided_by: harness\n",
        "an unknown decision": "decision: maybe\ndecided_by: human\n",
        "a record that is not a mapping": "- approve\n",
    }
    for name, text in cases.items():
        with tempfile.TemporaryDirectory() as base:
            code, posts = run_post(base, text)
            check(f"{name}: exits 2 and posts nothing", code == 2 and posts == [])
            check(f"{name}: the stop condition is unmet", stop_condition(base) == 1)


def test_comment_must_match_the_record():
    print("test_comment_must_match_the_record")
    cases = {
        "a comment that names the other decision": ("decision: reject\ndecided_by: harness\n",
                                                     "Harness verdict (gate off): approve"),
        "a comment that names both decisions": ("decision: approve\ndecided_by: harness\n",
                                                "Harness verdict (gate off): approve or reject"),
        "a harness decision posted as a human one": ("decision: approve\ndecided_by: harness\n",
                                                     "Reviewer's verdict: approve"),
        "a human decision posted as a harness one": ("decision: approve\ndecided_by: human\n",
                                                     "Harness verdict (gate off): approve"),
    }
    for name, (record, comment) in cases.items():
        with tempfile.TemporaryDirectory() as base:
            code, posts = run_post(base, record, comment=comment)
            check(f"{name}: exits 2 and posts nothing", code == 2 and posts == [])
            check(f"{name}: the stop condition is unmet", stop_condition(base) == 1)


def test_a_hand_made_verdict_file_does_not_pass():
    print("test_a_hand_made_verdict_file_does_not_pass")
    with tempfile.TemporaryDirectory() as base:
        write(os.path.join(base, "review", "findings.yaml"), "findings: []\n")
        write(os.path.join(base, "review", "verdict.yaml"), "decision: approve\n")
        write(os.path.join(base, "review", "posted.json"), json.dumps({"posted": True}))
        check("an old-style posted.json with a copied verdict.yaml is unmet",
              stop_condition(base) == 1)


def test_copies_are_identical():
    print("test_copies_are_identical")
    with open(os.path.join(HERE, "post_verdict.py"), "rb") as fh:
        mine = fh.read()
    with open(os.path.join(PLAY, "scripts", "post_verdict.py"), "rb") as fh:
        play_copy = fh.read()
    check("review-change's post_verdict.py is identical to this one", mine == play_copy)


def main():
    for test in (test_posted_decision_holds, test_failed_post_stays_unmet,
                 test_no_valid_decision_posts_nothing, test_comment_must_match_the_record,
                 test_a_hand_made_verdict_file_does_not_pass,
                 test_copies_are_identical):
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
