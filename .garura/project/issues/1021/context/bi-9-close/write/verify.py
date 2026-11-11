"""Check BI-9's close against the approved proposal: only the named lines changed, and nothing new broke.

Run from the repo root after the write. The model before is git HEAD. Writes verify.json beside this file.
"""
import json, os, re, subprocess, getpass
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
req = json.load(open(f"{HERE}/lines-request.json"))
checks = {}
def check(k, ok): checks[k] = bool(ok)
for p in req["pages"]:
    rel = p["page"]
    before = subprocess.run(["git", "show", f"HEAD:{MODEL}/{rel}"], capture_output=True, text=True, check=True).stdout.split("\n")
    after = open(f"{MODEL}/{rel}", encoding="utf-8").read().split("\n")
    want = list(before)
    for c in p["changes"]:
        if "old" in c:
            want[want.index(c["old"])] = c["new"]
        else:
            want.insert(want.index(c["after"]) + 1, c["add"])
    check(f"{rel}: equals the page before with only the approved lines changed", after == want)
status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", ".garura/product/"],
                        capture_output=True, text=True, check=True).stdout.rstrip("\n").split("\n")
named = {f"{MODEL}/{p['page']}" for p in req["pages"]}
check("only the six named pages changed under .garura/product/", {s[3:] for s in status if s} == named)
LINT = ".claude/skills/discover-capabilities/scripts/lint_grounding.py"
la = json.loads(subprocess.run(["python3", LINT, "--root", MODEL, "--spine", f"{MODEL}/_spine.yaml"], capture_output=True, text=True).stdout)
json.dump(la, open(f"{HERE}/lint-after.json", "w"), indent=2, ensure_ascii=False)
lb = json.load(open(f"{HERE}/lint-before.json"))
new_errors = [e for e in la["errors"] if e not in lb["errors"]]
new_warnings = [w for w in la["warnings"] if w not in lb["warnings"]]
check("structure check: no new error", not new_errors)
check("structure check: no new warning", not new_warnings)
LOCAL = re.compile("|".join(["/" + w + "/" for w in ("Us" + "ers", "ho" + "me", "pri" + "vate", "t" + "mp")]
                            + ["scratch" + "pad", re.escape(os.path.expanduser("~")), re.escape(getpass.getuser())]), re.I)
bad = [os.path.join(d, f) for d, _, fs in os.walk(os.path.dirname(HERE)) for f in fs
       if f != "verify.json" and LOCAL.search(open(os.path.join(d, f), encoding="utf-8", errors="replace").read())]
check("no file in the close folder names a home, temp or working folder, or a user name", not bad)
failed = [k for k, v in checks.items() if not v]
out = {"failed": failed, "run": len(checks), "structure": {"before": [len(lb["errors"]), len(lb["warnings"])],
       "after": [len(la["errors"]), len(la["warnings"])], "new_errors": new_errors, "new_warnings": new_warnings}}
json.dump(out, open(f"{HERE}/verify.json", "w"), indent=2, ensure_ascii=False)
print(json.dumps({"failed": failed, "run": len(checks), "structure": out["structure"]}, ensure_ascii=False))
