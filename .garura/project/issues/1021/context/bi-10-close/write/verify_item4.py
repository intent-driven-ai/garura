"""Check BI-10's whole close (items 2, 3 and 4): every page touched equals its committed version with exactly the
approved line changes applied, nothing else in the model changed, fn-promote-page's one-line is the approved one, and
the structure check finds no new error. Run from the repo root; writes verify-close.json beside this file.
"""
import json, os, subprocess
import yaml
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
reqs = [json.load(open(f"{HERE}/{n}")) for n in ("lines-request.json", "lines-request-4.json")]
checks = {}
def check(k, ok): checks[k] = bool(ok)
def show(path): return subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True, check=True).stdout
pages = {}
for r in reqs:
    for p in r["pages"]:
        pages.setdefault(p["page"], []).extend(p["changes"])
for rel, changes in pages.items():
    want = show(f"{MODEL}/{rel}").split("\n")
    for c in changes:
        if "old" in c:
            want[want.index(c["old"])] = c["new"]
        else:
            want.insert(want.index(c["after"]) + 1, c["add"])
    got = open(f"{MODEL}/{rel}", encoding="utf-8").read().split("\n")
    check(f"{rel}: its committed version with exactly the approved lines changed", got == want)
st = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", ".garura/product/"], capture_output=True, text=True).stdout
changed = {l[3:] for l in st.splitlines() if l.strip()}
check("only the pages of the close and the spine changed in the model", changed == {f"{MODEL}/{p}" for p in pages} | {f"{MODEL}/_spine.yaml"})
b = yaml.safe_load(show(f"{MODEL}/_spine.yaml")); a = yaml.safe_load(open(f"{MODEL}/_spine.yaml"))
one = json.load(open(f"{HERE}/link-request-4.json"))["parts"][0]["one_line"]
fa = {f["id"]: f for f in a["features"]}; fb = {f["id"]: f for f in b["features"]}
check("fn-promote-page: the approved one-line", fa["fn-promote-page"]["one_line"] == one)
diff_f = [i for i in fb if fa.get(i) != fb[i]]
check("index: only fn-promote-page changed", diff_f == ["fn-promote-page"] and all(a[k] == b[k] for k in a if k != "features"))
LINT = ".claude/skills/discover-capabilities/scripts/lint_grounding.py"
la = json.loads(subprocess.run(["python3", LINT, "--root", MODEL, "--spine", f"{MODEL}/_spine.yaml"], capture_output=True, text=True).stdout)
lb = json.load(open(f"{HERE}/lint-before.json"))
new = [e for e in la["errors"] if e not in lb["errors"]]
check("structure check: no new error", not new)
failed = [k for k, v in checks.items() if not v]
json.dump({"failed": failed, "run": len(checks), "structure": [len(la["errors"]), len(la["warnings"])], "new_errors": new},
          open(f"{HERE}/verify-close.json", "w"), indent=2)
print(json.dumps({"failed": failed, "run": len(checks), "structure_after": [len(la["errors"]), len(la["warnings"])], "new_errors": new}))
