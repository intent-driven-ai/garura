#!/usr/bin/env python3
"""
test_check_ontology.py — fixture tests for check_ontology.py.

Pins every rule the check enforces: front matter, sections, question shape, the parts
every kind must carry, relationships and questions pointing only at known kinds, and the
exit codes.

    python3 test_check_ontology.py
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_ontology as co  # noqa: E402

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


KIND = """### Business Intent

**What it is:** What a person or the organisation wants — an outcome.
**Who reads it:** person
**Lives at:** `product-os/intents/<id>.md`

**Properties**

| Property | What it holds | Required |
|----------|---------------|----------|
| outcome | What should be true, in the person's words | yes |

**Relationships**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| other → this | Prototype | many | A prototype shows what is wanted |

**Rules**

- It points at nothing; things point at it.

**Example**

Grow repeat orders by 10% this year.
"""


def doc(kinds=KIND, questions=None, pending="- **Prototype** — a runnable example.", fm=True):
    if questions is None:
        questions = ("- **Q1** — Can a business reader tell what was asked?\n"
                     "  **Answered by:** Business Intent\n  **Status:** answered\n")
    head = "---\nontology: product\nversion: 1\nupdated: 2026-10-08\n---\n" if fm else ""
    return (head + "\n# Product Ontology\n\nText.\n\n## Questions it must answer\n\n" + questions +
            "\n## Kinds\n\n" + kinds + "\n## Not yet defined\n\n" + pending + "\n\n## Log\n\n- 2026-10-08 — first.\n")


def problems(text):
    return co.check(text)["problems"]


def test_valid():
    r = co.check(doc())
    check("a complete ontology is valid", r["valid"])
    check("it lists the defined kind", r["kinds"] == ["Business Intent"])
    check("it lists the not-yet-defined kind", r["not_yet_defined"] == ["Prototype"])


def test_structure():
    check("no front matter is caught", problems(doc(fm=False)) == ["no front matter"])
    check("a missing section is caught",
          any("## Log" in p for p in problems(doc().replace("## Log", "## Diary"))))
    check("no questions is caught", any("no questions" in p for p in problems(doc(questions=""))))


def test_kind_parts():
    for label, cut in (("What it is", "**What it is:** What a person or the organisation wants — an outcome.\n"),
                       ("Lives at", "**Lives at:** `product-os/intents/<id>.md`\n"),
                       ("Example", "**Example**\n\nGrow repeat orders by 10% this year.\n")):
        check(f"a kind with no {label} is caught",
              any(label in p for p in problems(doc(kinds=KIND.replace(cut, "")))))
    check("a bad reader is caught",
          any("Who reads it" in p for p in problems(doc(kinds=KIND.replace("**Who reads it:** person", "**Who reads it:** robots")))))
    no_rules = KIND.replace("- It points at nothing; things point at it.\n", "")
    check("a kind with no rules is caught", any("rule" in p for p in problems(doc(kinds=no_rules))))
    no_props = KIND.replace("| outcome | What should be true, in the person's words | yes |\n", "")
    check("a kind with an empty properties table is caught",
          any("Properties" in p for p in problems(doc(kinds=no_props))))
    no_rel = KIND.split("**Relationships**")[0] + "**Relationships**\n\nNone yet.\n\n**Rules**" + KIND.split("**Rules**")[1]
    check("'None yet.' is accepted for relationships", co.check(doc(kinds=no_rel))["valid"])


def test_references():
    unknown = KIND.replace("| other → this | Prototype |", "| other → this | Gizmo |")
    check("a relationship to an unknown kind is caught",
          any("unknown kind `Gizmo`" in p for p in problems(doc(kinds=unknown))))
    q = ("- **Q1** — Which prototype shows it?\n  **Answered by:** Prototype\n  **Status:** answered\n")
    check("a question marked answered that leans on a not-yet kind is caught",
          any("not yet defined" in p for p in problems(doc(questions=q))))
    q2 = ("- **Q1** — Which prototype shows it?\n  **Answered by:** Prototype\n  **Status:** not yet\n")
    check("the same question marked 'not yet' is fine", co.check(doc(questions=q2))["valid"])
    q3 = ("- **Q1** — Something?\n  **Status:** answered\n")
    check("a question with no Answered by is caught", any("Answered by" in p for p in problems(doc(questions=q3))))
    q4 = ("- **Q1** — Something?\n  **Answered by:** Business Intent\n  **Status:** maybe\n")
    check("a bad status is caught", any("Status" in p for p in problems(doc(questions=q4))))
    both = doc(pending="- **Business Intent** — dup.\n- **Prototype** — a runnable example.")
    check("a kind both defined and pending is caught", any("both defined" in p for p in problems(both)))
    q5 = "- **Q1** — Can a reader tell?\n  **Answered by:** Nothing we know\n  **Status:** partly\n"
    check("an Answered by that names no known kind is caught",
          any("names no known kind" in p for p in problems(doc(questions=q5))))


def test_front_matter_and_headings():
    no_field = doc().replace("updated: 2026-10-08\n", "")
    check("a missing front-matter field is caught",
          any("missing `updated`" in p for p in problems(no_field)))
    bad_version = doc().replace("version: 1\n", "version: one\n")
    check("a version that is not a whole number is caught",
          any("whole number" in p for p in problems(bad_version)))
    no_rel_heading = KIND.split("**Relationships**")[0] + "**Rules**" + KIND.split("**Rules**")[1]
    check("a kind with no Relationships heading is caught",
          any("no **Relationships** heading" in p for p in problems(doc(kinds=no_rel_heading))))


def test_exit_codes():
    with tempfile.TemporaryDirectory() as tmp:
        good = os.path.join(tmp, "good.md")
        bad = os.path.join(tmp, "bad.md")
        binary = os.path.join(tmp, "bin.md")
        with open(good, "w") as fh:
            fh.write(doc())
        with open(bad, "w") as fh:
            fh.write(doc(questions=""))
        with open(binary, "wb") as fh:
            fh.write(b"\xff\xfe\xfa")
        run = lambda p: subprocess.run([sys.executable, os.path.join(HERE, "check_ontology.py"),  # noqa: E731
                                        "--ontology", p], capture_output=True).returncode
        check("exit 0 for valid", run(good) == 0)
        check("exit 2 for not valid", run(bad) == 2)
        check("exit 3 for unreadable", run(binary) == 3)
        check("exit 3 for missing", run(os.path.join(tmp, "nope.md")) == 3)


def main():
    for test in (test_valid, test_structure, test_kind_parts, test_references, test_exit_codes, test_front_matter_and_headings):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
