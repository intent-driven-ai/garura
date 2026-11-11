#!/usr/bin/env python3
"""test_lint_slice_intents.py — fixture tests for lint_grounding.py's slice "serves" check (#829).

A slice serves one or more business intents (ontology v10). Its spine entry lists them in
`intents`, and each must have a page at `<product-os>/intents/<id>.md`. A slice naming an
intent with no page is an error; a slice naming none is a warning (older spines have no field).

    python3 test_lint_slice_intents.py
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lint_grounding as lg  # noqa: E402

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


SPINE = """domains: []
capabilities: []
features: []
slices:
  - id: slice-checkout
    slug: checkout
%s
"""

INTENT_PAGE = """# Grow online sales without adding sales staff

**Outcome:** More shoppers finish buying online.
"""


def lint(root, intents_line):
    write(os.path.join(root, "_spine.yaml"), SPINE % intents_line)
    errors, warnings = [], []
    lg.check_spine(root, os.path.join(root, "_spine.yaml"), errors, warnings, {})
    return errors, warnings


def test_slice_serves_an_intent():
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        errors, _ = lint(root, "    intents: [grow-online-sales]")
        check("a slice that serves an intent with no page fails",
              len(errors) == 1 and "slice-checkout" in errors[0] and "grow-online-sales" in errors[0])
        write(os.path.join(root, "intents", "grow-online-sales.md"), INTENT_PAGE)
        errors, warnings = lint(root, "    intents: [grow-online-sales]")
        check("a slice that serves an intent whose page exists passes",
              errors == [] and not any("slice-checkout" in w for w in warnings))
        errors, _ = lint(root, "    intents: [grow-online-sales, cut-returns]")
        check("each listed intent is checked: the one with no page is named",
              len(errors) == 1 and "cut-returns" in errors[0])
        write(os.path.join(root, "intents", "42.md"), INTENT_PAGE)
        errors, _ = lint(root, "    intents: [42]")
        check("an intent named by its issue number resolves to intents/<number>.md", errors == [])
        errors, warnings = lint(root, "")
        check("a slice that names no intent is a warning, not an error",
              errors == [] and any("slice-checkout" in w and "business intent" in w for w in warnings))
        check("the intent pages are not counted as orphan grounding docs",
              not any("orphan" in e for e in lint(root, "    intents: [42]")[0]))


def main():
    test_slice_serves_an_intent()
    print(f"\n{PASSED} passed, {FAILED} failed")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
