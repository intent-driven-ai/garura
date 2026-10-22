#!/usr/bin/env python3
"""test_edit_ontology_scripts.py — the change check and the checkpoint record (#777).

    python3 core/components/plays/edit-ontology/scripts/test_edit_ontology_scripts.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
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


def page(version, updated, kinds, log):
    out = [f"---\nontology: product\nversion: {version}\nupdated: {updated}\n---\n", "# Product Ontology\n",
           "## Questions it must answer\n\n- **Q1** — a question\n", "## Kinds\n"]
    for name, body in kinds:
        out.append(f"### {name}\n\n{body}\n")
    out.append("## Not yet defined\n\n- Domain — later.\n")
    out.append("## Log\n\n" + "".join(f"- {line}\n" for line in log))
    return "\n".join(out)


def run(script, *args):
    p = subprocess.run([sys.executable, os.path.join(HERE, script), *args], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def main():
    with tempfile.TemporaryDirectory() as d:
        before = os.path.join(d, "before.md")
        after = os.path.join(d, "after.md")
        out = os.path.join(d, "change-check.json")
        base_kinds = [("Business Intent", "What a person wants."), ("Capability", "A part of the product.")]
        open(before, "w").write(page(5, "2026-10-21", base_kinds, ["2026-10-21 — v5."]))

        # A good change: a new kind, version up, date set, one log line.
        open(after, "w").write(page(6, "2026-10-22", base_kinds + [("ICE", "The agent's intent. Example: the ICE for checkout.")],
                                    ["2026-10-21 — v5.", "2026-10-22 — v6: the ICE is its own kind."]))
        rc, _, _ = run("check_ontology_change.py", "--before", before, "--after", after, "--allow-kind", "ICE",
                       "--date", "2026-10-22", "--forbid-name", "Kapil", "--out", out)
        r = json.load(open(out))
        check("a good change passes", rc == 0 and r["scope_ok"] and r["version_ok"] and r["names_ok"])
        check("the new kind is listed as changed", r["changed_kinds"] == ["ICE"])

        # Today's ontology fails when nothing was bumped (the check must fail first).
        rc, _, _ = run("check_ontology_change.py", "--before", before, "--after", before, "--allow-kind", "ICE",
                       "--date", "2026-10-22", "--out", out)
        r = json.load(open(out))
        check("no version bump fails", rc == 1 and not r["version_ok"])

        # A kind outside the need changed.
        open(after, "w").write(page(6, "2026-10-22", [("Business Intent", "What a person wants, now different."),
                                                      ("Capability", "A part of the product."), ("ICE", "x")],
                                    ["2026-10-21 — v5.", "2026-10-22 — v6."]))
        rc, _, _ = run("check_ontology_change.py", "--before", before, "--after", after, "--allow-kind", "ICE",
                       "--date", "2026-10-22", "--out", out)
        r = json.load(open(out))
        check("an out-of-scope kind fails", rc == 1 and not r["scope_ok"] and r["out_of_scope"] == ["Business Intent"])

        # Two new log lines.
        open(after, "w").write(page(6, "2026-10-22", base_kinds + [("ICE", "x")],
                                    ["2026-10-21 — v5.", "2026-10-22 — a.", "2026-10-22 — b."]))
        rc, _, _ = run("check_ontology_change.py", "--before", before, "--after", after, "--allow-kind", "ICE",
                       "--date", "2026-10-22", "--out", out)
        check("two new log lines fail", rc == 1 and not json.load(open(out))["version_ok"])

        # A real name in the text.
        open(after, "w").write(page(6, "2026-10-22", base_kinds + [("ICE", "Asked for by Kapil.")],
                                    ["2026-10-21 — v5.", "2026-10-22 — v6."]))
        rc, _, _ = run("check_ontology_change.py", "--before", before, "--after", after, "--allow-kind", "ICE",
                       "--date", "2026-10-22", "--forbid-name", "Kapil", "--out", out)
        r = json.load(open(out))
        check("a real name fails", rc == 1 and not r["names_ok"] and r["names_found"])

        # The checkpoint record.
        dec = os.path.join(d, "decisions.json")
        draft = os.path.join(d, "draft-questions.md")
        open(draft, "w").write("Q8 …")
        rc, _, _ = run("record_checkpoint.py", "--decisions", dec, "--point", "questions", "--verdict", "yes",
                       "--reply", "yes", "--draft", draft)
        r = json.load(open(dec))
        check("one yes is not all three", rc == 0 and r["all_agreed"] is False)
        rc, _, _ = run("record_checkpoint.py", "--decisions", dec, "--point", "kinds", "--verdict", "change",
                       "--reply", "rename X", "--draft", draft)
        rc, _, _ = run("record_checkpoint.py", "--decisions", dec, "--point", "kinds", "--verdict", "yes",
                       "--reply", "yes", "--draft", draft)
        rc, _, _ = run("record_checkpoint.py", "--decisions", dec, "--point", "links", "--verdict", "yes",
                       "--reply", "approve", "--draft", draft)
        r = json.load(open(dec))
        check("three yes answers are all agreed", r["all_agreed"] is True)
        check("a change before a yes is kept in the history", [e["verdict"] for e in r["history"]].count("change") == 1)
        rc, _, err = run("record_checkpoint.py", "--decisions", dec, "--point", "links", "--verdict", "yes",
                         "--reply", "", "--draft", draft)
        check("an empty reply is refused", rc == 2)
        rc, _, err = run("record_checkpoint.py", "--decisions", dec, "--point", "links", "--verdict", "yes",
                         "--reply", "yes", "--draft", os.path.join(d, "missing.md"))
        check("a yes with no draft shown is refused", rc == 2)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
