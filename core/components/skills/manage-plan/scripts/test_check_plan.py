#!/usr/bin/env python3
"""
test_check_plan.py — fixture tests for check_plan.py (#619).

check_plan.py alone decides whether an issue's plan is done (ADR 030), so every
rule it enforces is pinned here: the format, the "now" marker, the What line,
done-ness, the parent link (P9), and how unreadable files exit.

    python3 test_check_plan.py
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_plan as cp  # noqa: E402

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


def plan(plan_for=700, kind="story", status="active", now="1", serves=None, items=None, done=None):
    """Build a plan text. items: list of (number, title, has_what, extra_line)."""
    fm = [f"plan_for: {plan_for}", f"kind: {kind}", f'serves: "#{plan_for} — test"',
          f"status: {status}", "updated: 2026-10-08", f"now: {now}"]
    if serves:
        fm += [f"serves_plan: {serves[0]}", f"serves_item: {serves[1]}"]
    body = ["# Plan", "", "## What we are trying to reach", "", "x", "",
            "## When this plan is done", "", "- x", "", "## Where we are now", "", "x", "",
            "## The plan, in order", "", "### Done", ""]
    for line in done or []:
        body.append(f"- {line}")
    body.append("")
    for number, title, has_what, extra in items or []:
        body.append(f"### {number}. {title}")
        body.append("")
        if has_what:
            body.append("**What:** the work.")
        if extra:
            body.append(extra)
        body.append("")
    body += ["## Log", "", "- 2026-10-08 — test."]
    return "---\n" + "\n".join(fm) + "\n---\n\n" + "\n".join(body) + "\n"


def write(stm, number, text):
    path = os.path.join(stm, str(number), "specs", "plan.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def run(path):
    proc = subprocess.run([sys.executable, os.path.join(HERE, "check_plan.py"), "--plan", path],
                          capture_output=True, text=True)
    return proc.returncode


def test_format():
    ok = cp.check(plan(items=[(1, "First — now", True, "")]))
    check("a valid active plan is valid and not done", ok["valid"] and not ok["done"])
    bad = cp.check(plan(now="2", items=[(1, "First — now", True, ""), (2, "Second", True, "")]))
    check("now that disagrees with the marked heading is caught",
          not bad["valid"] and any("'— now' heading is item 1" in p for p in bad["problems"]))
    two = cp.check(plan(items=[(1, "A — now", True, ""), (2, "B — now", True, "")]))
    check("two '— now' headings are caught", any("exactly one" in p for p in two["problems"]))
    nowhat = cp.check(plan(items=[(1, "A — now", True, ""), (2, "B", False, "")]))
    check("an item with no What line is caught", any("item 2 has no" in p for p in nowhat["problems"]))
    missing = cp.check(plan(items=[(1, "A — now", True, "")]).replace("## Log", "## Diary"))
    check("a missing section is caught", any("## Log" in p for p in missing["problems"]))
    kind = cp.check(plan(kind="epic", items=[(1, "A — now", True, "")]))
    check("an unknown kind is caught", any("kind `epic`" in p for p in kind["problems"]))
    status = cp.check(plan(status="paused", items=[(1, "A — now", True, "")]))
    check("an unknown status is caught", any("status `paused`" in p for p in status["problems"]))
    nofm = cp.check("# no front matter\n")
    check("no front matter is not valid", not nofm["valid"] and nofm["problems"] == ["no front matter"])


def test_done():
    early = cp.check(plan(status="done", now="-", items=[(1, "A", True, "")]))
    check("done with open items is caught", not early["valid"] and not early["done"])
    finished = cp.check(plan(status="done", now="-", done=["**Built: A** — #1."]))
    check("a finished plan is valid and done", finished["valid"] and finished["done"])
    dropped = cp.check(plan(status="dropped", now="-"))
    check("a dropped plan with no open items counts as done", dropped["done"])


def test_parent():
    with tempfile.TemporaryDirectory() as stm:
        parent = write(stm, 606, plan(plan_for=606, kind="business-intent",
                                      items=[(1, "Plan mode — now", True, "**Issue:** #619."),
                                             (2, "Other", True, "**Issue:** #616.")]))
        child = write(stm, 619, plan(plan_for=619, serves=(606, 1), items=[(1, "A — now", True, "")]))
        check("a child naming an open parent item that names it is valid",
              cp.check(open(child, encoding="utf-8").read(), child)["valid"])

        wrong_item = write(stm, 619, plan(plan_for=619, serves=(606, 2), items=[(1, "A — now", True, "")]))
        r = cp.check(open(wrong_item, encoding="utf-8").read(), wrong_item)
        check("serves_item pointing at an item that does not name the issue is caught",
              any("serves_item=2" in p for p in r["problems"]))

        prefix = write(stm, 60, plan(plan_for=60, serves=(606, 1), items=[(1, "A — now", True, "")]))
        r = cp.check(open(prefix, encoding="utf-8").read(), prefix)
        check("#60 does not match inside #606 (QF-01)",
              any("does not name #60" in p for p in r["problems"]))

        nowhere = write(stm, 701, plan(plan_for=701, serves=(999, 1), items=[(1, "A — now", True, "")]))
        r = cp.check(open(nowhere, encoding="utf-8").read(), nowhere)
        check("a missing parent plan is caught", any("no plan at" in p for p in r["problems"]))

        bi = cp.check(plan(plan_for=606, kind="business-intent", serves=(1, 1),
                           items=[(1, "A — now", True, "")]), parent)
        check("a business intent naming a parent is caught",
              any("serves no parent" in p for p in bi["problems"]))

        half = cp.check(plan(plan_for=619, serves=("606", "x"), items=[(1, "A — now", True, "")]), child)
        check("a non-number serves_item is caught", any("must both be numbers" in p for p in half["problems"]))

        finished_parent = write(stm, 606, plan(plan_for=606, kind="business-intent",
                                               items=[(2, "Other — now", True, "**Issue:** #616.")],
                                               now="2", done=["**Decided: plan mode** — #619."]))
        child = write(stm, 619, plan(plan_for=619, serves=(606, 1), items=[(1, "A — now", True, "")]))
        check("a child whose parent item is finished is valid when the Done list names it",
              cp.check(open(child, encoding="utf-8").read(), child)["valid"])
        check("the parent plan path is reported",
              cp.check(open(child, encoding="utf-8").read(), child)["serves_plan"] == finished_parent)


def test_exit_codes():
    with tempfile.TemporaryDirectory() as stm:
        active = write(stm, 700, plan(items=[(1, "A — now", True, "")]))
        check("exit 1 for valid, not done", run(active) == 1)
        done = write(stm, 701, plan(plan_for=701, status="done", now="-"))
        check("exit 0 for valid and done", run(done) == 0)
        broken = write(stm, 702, plan(plan_for=702, items=[(1, "A", False, "")]))
        check("exit 2 for not valid", run(broken) == 2)
        binary = os.path.join(stm, "binary.md")
        with open(binary, "wb") as fh:
            fh.write(b"---\nplan_for: 1\n\xff\xfe\xfa\n---\n")
        check("exit 3 for a file that is not UTF-8 (QF-03)", run(binary) == 3)
        check("exit 3 for a missing file", run(os.path.join(stm, "nope.md")) == 3)


def main():
    for test in (test_format, test_done, test_parent, test_exit_codes):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
