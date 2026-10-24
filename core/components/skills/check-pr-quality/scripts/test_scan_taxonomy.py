#!/usr/bin/env python3
"""
test_scan_taxonomy.py — tests for scan_taxonomy.py (#851).

Covers: a changed ADR gets no finding; a stm-evidence path gets no finding; a
`+++` line inside a hunk is an added line, not a file header; a `--paths` entry
that is not a path is dropped and listed in rejected_paths. It also checks that
scan() keeps its result keys.

    python3 test_scan_taxonomy.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scan_taxonomy as st  # noqa: E402

PASSED = 0
FAILED = 0

TAXONOMY = """
**Classification table — first match wins, top to bottom (pure globs, no judgment):**

| Artifact type | Path globs |
|---|---|
| `stm-evidence` | `.garura/project/**`, `.garura/core/**` |
| `docs-planning` | `docs/**`, `**/*.md` |
| `runtime-code` | everything else (the default) |

## Severity Table

| ID | Sev | Match rule | Evidence |
|---|---|---|---|
| DOC-05 | P4 | `path:docs/adr/**` | file |
| DOC-09 | P4 | `path:**/*.md` | file |
| SEC-01 | P1 | `grep:secret` | line |
"""


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")


def _diff(path, added):
    body = "".join(f"+{a}\n" for a in added)
    return (f"diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n"
            f"@@ -0,0 +1,{len(added)} @@\n{body}")


def test_adr_skipped():
    print("A changed ADR gets no finding")
    res = st.scan(TAXONOMY, _diff("docs/adr/053-x.md", ["text"]))
    check("ADR path is in changed", "docs/adr/053-x.md" in res["changed"])
    check("no finding on the ADR", res["findings"] == [])
    res = st.scan(TAXONOMY, _diff("docs/guide.md", ["text"]))
    check("other docs still get a finding",
          [f["standard_id"] for f in res["findings"]] == ["DOC-09"])


def test_stm_skipped():
    print("A stm-evidence path gets no finding")
    res = st.scan(TAXONOMY, _diff(".garura/project/issues/9/run.md", ["text"]) +
                  _diff(".garura/core/memory/x.md", ["text"]))
    check("both paths in changed", len(res["changed"]) == 2)
    check("no finding", res["findings"] == [])


def test_plus_line_in_hunk():
    print("A +++ line inside a hunk is an added line")
    diff = ("diff --git a/app.py b/app.py\n--- a/app.py\n+++ b/app.py\n"
            "@@ -0,0 +1,2 @@\n+x = 1\n+++ not a header secret\n")
    changed, added = st.parse_diff(diff)
    check("one changed path", changed == ["app.py"])
    check("two added lines", [a[2] for a in added] == ["x = 1", "++ not a header secret"])
    check("added line keeps its file", all(a[0] == "app.py" for a in added))
    diff2 = ("diff --git a/app.py b/app.py\n--- a/app.py\n+++ b/app.py\n"
             "@@ -1,2 +1,1 @@\n--- removed\n x\n")
    changed2, _ = st.parse_diff(diff2)
    check("a --- line inside a hunk is not a header", changed2 == ["app.py"])
    res = st.scan(TAXONOMY, diff)
    check("grep fires on the ++ line in app.py",
          [(f["standard_id"], f["file"]) for f in res["findings"]] == [("SEC-01", "app.py")])


def test_rejected_paths():
    print("A --paths entry that is not a path is dropped")
    override = ["app.py", "+added line", "-removed", " context", '"key": "value"']
    res = st.scan(TAXONOMY, _diff("app.py", ["ok"]), override)
    check("only the path is kept", res["changed"] == ["app.py"])
    check("rejected_paths lists the rest",
          res["rejected_paths"] == ["+added line", "-removed", " context", '"key": "value"'])
    res = st.scan(TAXONOMY, _diff("app.py", ["ok"]))
    check("rejected_paths is empty without --paths", res["rejected_paths"] == [])


def test_keys():
    print("scan() keeps its result keys")
    res = st.scan(TAXONOMY, _diff("app.py", ["ok"]))
    for key in ("changed", "findings", "counts", "catchall", "errors",
                "scan_coverage", "standards_relevant", "rejected_paths"):
        check(f"key {key}", key in res)


if __name__ == "__main__":
    test_adr_skipped()
    test_stm_skipped()
    test_plus_line_in_hunk()
    test_rejected_paths()
    test_keys()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)
