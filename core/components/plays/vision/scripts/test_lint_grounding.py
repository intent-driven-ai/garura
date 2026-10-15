#!/usr/bin/env python3
"""test_lint_grounding.py — fixture tests for lint_grounding.py's spine orphan check (#634).

A lens doc belongs to its slice (`<domain>/slices/<slice>/lens/<type>.md`), not to a spine
node, so the spine never points at it. It must not be reported as an orphan while its slice
is in the spine, and must be reported when its slice is not. The lens contracts themselves are
checked against each lens template's gold example. Every play's copy of lint_grounding.py must
be identical to this one.

    python3 test_lint_grounding.py
"""
import glob
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lint_grounding as lg  # noqa: E402

REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
LENS_TEMPLATES = os.path.join(REPO, "core", "components", "memory", "standards", "schemas", "product-os",
                              "grounding", "lens")

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


def gold(lens):
    """The gold example from a lens template — the first ```markdown block."""
    with open(os.path.join(LENS_TEMPLATES, f"{lens}.md"), encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"```markdown\n(.*?)\n```", text, re.DOTALL)
    return m.group(1) + "\n"


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


SPINE = """domains: []
capabilities: []
functionalities: []
slices:
  - id: slice-checkout
    slug: checkout
"""


def orphans(root):
    errors, warnings = [], []
    lg.check_spine(root, os.path.join(root, "_spine.yaml"), errors, warnings, {})
    return [e for e in errors if "orphan" in e]


def test_lens_docs_and_the_orphan_check():
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        write(os.path.join(root, "_spine.yaml"), SPINE)
        write(os.path.join(root, "shop", "slices", "checkout", "lens", "quality.md"), gold("quality"))
        check("a lens doc under a slice the spine knows is not an orphan", orphans(root) == [])
        write(os.path.join(root, "shop", "slices", "slice-checkout", "lens", "ux.md"), gold("ux"))
        check("the slice may be named by its id as well as its slug", orphans(root) == [])
        write(os.path.join(root, "shop", "slices", "gone", "lens", "run.md"), gold("run"))
        found = orphans(root)
        check("a lens doc under a slice the spine does not know is an orphan",
              len(found) == 1 and "slices/gone/lens/run.md" in found[0] and "slice is not in the spine" in found[0])
        write(os.path.join(root, "shop", "lens", "agentic.md"), gold("agentic"))
        check("a lens doc outside any slice folder is an orphan",
              any("shop/lens/agentic.md" in e for e in orphans(root)))


def test_lens_contracts_match_their_templates():
    for path in sorted(glob.glob(os.path.join(LENS_TEMPLATES, "*.md"))):
        lens = os.path.splitext(os.path.basename(path))[0]
        text = gold(lens)
        title = lg.parse_sections(text)[0]
        kind = lg.infer_kind(title)
        errors, warnings = [], []
        if kind:
            lg.check_doc(path, text, kind, errors, warnings)
        check(f"the {lens} lens template's gold example is a valid {lens} lens doc",
              kind == f"lens-{lens}" and not errors)


def test_every_copy_is_identical():
    mine = open(os.path.join(HERE, "lint_grounding.py"), "rb").read()
    copies = glob.glob(os.path.join(REPO, "core", "components", "plays", "*", "scripts", "lint_grounding.py"))
    different = [c for c in copies if open(c, "rb").read() != mine]
    check(f"every play's lint_grounding.py is identical to this one ({len(copies)} copies)",
          len(copies) >= 12 and not different)


def main():
    for test in (test_lens_docs_and_the_orphan_check, test_lens_contracts_match_their_templates,
                 test_every_copy_is_identical):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
