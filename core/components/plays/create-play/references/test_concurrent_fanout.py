#!/usr/bin/env python3
"""
test_concurrent_fanout.py — fixture tests for the #468 Stage 5 concurrent
read-only fan-out (epic #460). The subject:

  lint_play.py check_fanout_declaration — the convergence-lint that a play
     citing concurrent-fanout.md must declare its join + read-only safety, and a
     play naming the scoped-write fan-out (#615) its write scope + no shared file.

Plain asserts, no wall-clock in the assertions.

    python3 test_concurrent_fanout.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable or "python3"
SCRIPTS = os.path.join(HERE, "..", "scripts")

sys.path.insert(0, os.path.abspath(SCRIPTS))
import lint_play  # noqa: E402

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


# ---------------------------------------------------------------------------
# 1. lint check_fanout_declaration
# ---------------------------------------------------------------------------
def _lint(text):
    """Run just the fan-out check over a play body; return (ok, detail) or None."""
    res = lint_play.check_fanout_declaration({"text": text})
    if not res:
        return None
    ok, _label, detail = res[0]
    return ok, detail


def test_lint_declaration():
    print("test_lint_declaration")
    # Silent when the play never fans out.
    check("no fan-out → check is silent",
          _lint("A plain serial play. No concurrency here.") is None)
    # Passes when the play cites the rule AND declares join + read-only.
    good = ("dispatch a concurrent read-only fan-out "
            "(standards/rules/concurrent-fanout.md): each judge is read-only, "
            "join before gating.")
    r = _lint(good)
    check("cites rule + join + read-only → PASS", r is not None and r[0] is True)
    # Fails when it cites the rule but omits the join barrier.
    no_join = ("see concurrent-fanout.md — each sub-agent is read-only over its "
               "own doc.")
    r = _lint(no_join)
    check("cites rule, no join → FAIL", r is not None and r[0] is False
          and "join" in r[1])
    # Fails when it cites the rule but omits the read-only condition.
    no_ro = "see concurrent-fanout.md — dispatch the batch, then join."
    r = _lint(no_ro)
    check("cites rule, no read-only → FAIL", r is not None and r[0] is False
          and "read-only" in r[1])


def test_scoped_write_declaration():
    print("test_scoped_write_declaration")
    base = ("judges run as a concurrent read-only fan-out "
            "(standards/rules/concurrent-fanout.md), join before gating. ")
    res = lint_play.check_fanout_declaration({"text": base})
    check("read-only fan-out only → no scoped-write result", len(res) == 1)
    good = base + ("Enrich runs as a scoped-write fan-out: each agent writes only inside "
                   "its own write scope, no shared file.")
    res = lint_play.check_fanout_declaration({"text": good})
    check("scoped-write fan-out declared in full → PASS",
          len(res) == 2 and res[1][0] is True)
    no_scope = base + "Enrich runs as a scoped-write fan-out with no shared file."
    res = lint_play.check_fanout_declaration({"text": no_scope})
    check("scoped-write fan-out without its write scope → FAIL",
          res[1][0] is False and "write scope" in res[1][2])
    no_shared = base + "Enrich runs as a scoped-write fan-out inside each write scope."
    res = lint_play.check_fanout_declaration({"text": no_shared})
    check("scoped-write fan-out without the no-shared-file condition → FAIL",
          res[1][0] is False and "shared file" in res[1][2])


def main():
    test_lint_declaration()
    test_scoped_write_declaration()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
