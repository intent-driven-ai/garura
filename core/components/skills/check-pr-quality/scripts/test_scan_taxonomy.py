#!/usr/bin/env python3
"""
test_scan_taxonomy.py — tests for scan_taxonomy.py (#851).

Covers: BE-19 and SEC-18 of the real taxonomy (pr.md) fire on SQL-shaped and
permission code and not on plain words; SEC-07 fires on an unsafe load and
not on a JSON.parse of a file or a tool's output; a changed ADR gets no finding; a stm-evidence path gets no finding; a
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


PR_MD = os.path.normpath(os.path.join(HERE, "..", "..", "..", "memory", "standards", "rules", "pr.md"))


def _real_hits(rule_id, lines, path="app/service.py"):
    with open(PR_MD, encoding="utf-8") as fh:
        taxonomy = fh.read()
    res = st.scan(taxonomy, _diff(path, lines))
    return [f["line"] for f in res["findings"] if f["standard_id"] == rule_id]


def test_be19_sql_only():
    print("BE-19 fires on SQL-shaped code only")
    sql = ['rows = db.query("SELECT id, name FROM users WHERE id = ?")',
           "q = 'select * from orders'",
           "sql = `SELECT total FROM invoices`",
           "    LEFT JOIN accounts a ON a.id = o.account_id"]
    check("each SQL line is a finding", _real_hits("BE-19", sql) == [1, 2, 3, 4])
    words = ["# take the value from the config",
             "full = path.join(base, name)",
             "items = ', '.join(names)",
             "msg = 'join the team from today'",
             "Select the item you want from the list"]
    check("plain from / join / path.join give no finding", _real_hits("BE-19", words) == [])


def test_sec18_permission_only():
    print("SEC-18 fires on permission code only")
    code = ["if user.isAdmin:",
            "if hasRole(user, 'editor'):",
            "allowed = hasPermission(user, 'write')",
            "if (ability.can('delete', post)) {",
            "if (user.role === 'admin') {",
            "if role == 'owner':"]
    check("each permission line is a finding", _real_hits("SEC-18", code) == [1, 2, 3, 4, 5, 6])
    words = ["# the role of this module is to parse input",
             "class Role:",
             "role_name = form['name']",
             "title = 'Role and duties'"]
    check("the plain word role or Role gives no finding", _real_hits("SEC-18", words) == [])


def test_sec07_unsafe_load_only():
    print("SEC-07 fires on an unsafe load only")
    code = ["obj = pickle.loads(blob)",
            "obj = pickle.load(fh)",
            "code = marshal.loads(raw)",
            "cfg = yaml.load(text)",
            "cfg = yaml.load(fh, Loader=yaml.FullLoader)",
            "cfg = yaml.unsafe_load(text)",
            "const data = JSON.parse(req.body);",
            "const data = JSON.parse(event.body)",
            "const p = JSON.parse(payload)",
            "const q = JSON.parse(ctx.request.query.filter)"]
    check("each unsafe load is a finding",
          _real_hits("SEC-07", code) == list(range(1, len(code) + 1)))
    safe = ["const cfg = JSON.parse(fs.readFileSync(configPath, 'utf8'));",
            "const out = JSON.parse(execSync('git status --porcelain').toString());",
            "const res = JSON.parse(child.stdout)",
            "const meta = JSON.parse(inputFile)",
            "cfg = yaml.safe_load(text)",
            "cfg = yaml.load(fh, Loader=yaml.SafeLoader)",
            "cfg = yaml.load(fh, Loader=CSafeLoader)",
            "rows = json.loads(raw)"]
    check("a file read, a tool's output and a safe load give no finding",
          _real_hits("SEC-07", safe) == [])


if __name__ == "__main__":
    test_adr_skipped()
    test_stm_skipped()
    test_plus_line_in_hunk()
    test_rejected_paths()
    test_keys()
    test_be19_sql_only()
    test_sec18_permission_only()
    test_sec07_unsafe_load_only()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)
