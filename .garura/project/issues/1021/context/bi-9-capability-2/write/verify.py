"""Check BI-9 capability 2's write (Run plays as loops) against what the product owner approved.

Run from the repo root after the write. The model before the write is git HEAD (git show). Runs the
structure check into lint-after.json and writes verify.json in this folder.
"""
import getpass
import json
import os
import re
import subprocess

import yaml

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
ISSUE = ".garura/project/issues/1021/context/bi-9-capability-2"
MODEL = ".garura/product/product-os"
C = "software-delivery-planning/run-plays-as-loops"
DRAFTS = f"{ISSUE}/drafts/product-os/{C}"
CAP = "cap-run-plays-as-loops"
FEATURES = ["fn-run-loop", "fn-check-loop-result", "fn-brief-open-points", "fn-show-run-status",
            "fn-loop-per-transition", "fn-start-loop-on-trigger", "fn-run-plays-side-by-side"]
THIN_ICE = {"fn-start-loop-on-trigger", "fn-run-plays-side-by-side"}
THIN = re.compile(r"^\s*(?:>\s*)?\**Thin(?: ICE)?\**\s*:", re.I)
LINT = ".claude/skills/discover-capabilities/scripts/lint_grounding.py"
checks = {}


def check(name, ok):
    checks[name] = bool(ok)


def rb(p):
    with open(p, "rb") as f:
        return f.read()


def git_show(path):
    return subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, check=True).stdout


def ice_id(part):
    return "ice-" + (part[3:] if part.startswith("fn-") else part[4:])


# 1. pages equal the approved drafts
rels = ["capability.md", "ice.md"] + [f"{fn}/{p}" for fn in FEATURES for p in ("feature.md", "ice.md")]
pages = {}
for rel in rels:
    m = f"{MODEL}/{C}/{rel}"
    ok = os.path.isfile(m) and rb(m) == rb(f"{DRAFTS}/{rel}")
    lines = open(m, encoding="utf-8").read().split("\n") if os.path.isfile(m) else []
    thin_lines = [i for i, l in enumerate(lines) if THIN.match(l)]
    part = rel.split("/")[0] if "/" in rel else CAP
    want_thin = rel.endswith("ice.md") and part in THIN_ICE
    check(f"page {C}/{rel} equals its approved draft byte for byte", ok)
    check(f"page {C}/{rel} Thin lines as it should ({'one, first' if want_thin else 'none'})",
          thin_lines == ([0] if want_thin else []))
    pages[rel] = {"equals_draft": ok, "thin_lines": thin_lines}
check("16 pages", len(rels) == 16)
new_files = sorted(os.path.relpath(os.path.join(d, f), f"{MODEL}/{C}") for d, _, fs in os.walk(f"{MODEL}/{C}") for f in fs)
check("the new capability folder holds only its 16 pages", new_files == sorted(rels))

# 2. index
before = yaml.safe_load(git_show(f"{MODEL}/_spine.yaml"))
after = yaml.safe_load(open(f"{MODEL}/_spine.yaml", encoding="utf-8"))


def by_id(s, k):
    return {e["id"]: e for e in (s.get(k) or [])}


caps_b, caps_a = by_id(before, "capabilities"), by_id(after, "capabilities")
feats_b, feats_a = by_id(before, "features"), by_id(after, "features")
ices_b, ices_a = by_id(before, "ices"), by_id(after, "ices")
check("capabilities: new is exactly the one", sorted(set(caps_a) - set(caps_b)) == [CAP])
check("capabilities: none removed or changed", all(caps_a.get(i) == caps_b[i] for i in caps_b))
check("features: new are exactly the seven", sorted(set(feats_a) - set(feats_b)) == sorted(FEATURES))
check("features: none removed or changed", all(feats_a.get(i) == feats_b[i] for i in feats_b))
check("ices: new are exactly the eight", sorted(set(ices_a) - set(ices_b)) == sorted(ice_id(p) for p in [CAP] + FEATURES))
check("ices: none removed or changed", all(ices_a.get(i) == ices_b[i] for i in ices_b))
for k in ("domains", "slices"):
    check(f"{k}: unchanged", before.get(k) == after.get(k))
req = {p["id"]: p for p in json.load(open(f"{HERE}/link-request.json"))["parts"]}
c = caps_a.get(CAP, {})
check(f"{CAP}: under dom-software-delivery-planning, intents [bi-9], its page, its approved one-line, not thin",
      c.get("domain") == "dom-software-delivery-planning" and c.get("intents") == ["bi-9"]
      and c.get("doc") == f"{C}/capability.md" and c.get("one_line") == req[CAP]["one_line"]
      and not (c.get("metadata") or {}).get("thin"))
for fn in FEATURES:
    e = feats_a.get(fn, {})
    check(f"{fn}: under {CAP}, intents [bi-9], page {C}/{fn}/feature.md",
          e.get("capability") == CAP and e.get("intents") == ["bi-9"] and e.get("doc") == f"{C}/{fn}/feature.md")
    check(f"{fn}: its approved one-line", e.get("one_line") == req[fn]["one_line"])
    check(f"{fn}: one-line does not start with Not built", not str(e.get("one_line", "")).startswith("Not built"))
    check(f"{fn}: carries no thin mark", not (e.get("metadata") or {}).get("thin"))
for part in [CAP] + FEATURES:
    iid = ice_id(part)
    e = ices_a.get(iid, {})
    doc = f"{C}/ice.md" if part == CAP else f"{C}/{part}/ice.md"
    thin = bool((e.get("metadata") or {}).get("thin"))
    check(f"{iid}: for {part}, page {doc}, thin {part in THIN_ICE}",
          e.get("for") == part and e.get("doc") == doc and thin == (part in THIN_ICE))
    check(f"{iid}: the only ICE of {part}", [i for i, x in ices_a.items() if x.get("for") == part] == [iid])

# 3. BI-9
bi9 = open(f"{MODEL}/intents/bi-9.md", encoding="utf-8").read().split("\n")
b9 = git_show(f"{MODEL}/intents/bi-9.md").decode("utf-8").split("\n")
ti = bi9.index("**Touches:**")
touches = []
for l in bi9[ti + 1:]:
    if not l.startswith("- ["):
        break
    touches.append(l)
docs, marks, titles_ok = [], [], True
for l in touches:
    m = re.match(r"^- \[([^\]]+)\]\((\.\./[^)\s]+)\) \((capability|feature)\) — (adds|changes)$", l)
    if not m:
        titles_ok = False
        continue
    target = os.path.normpath(os.path.join(MODEL, "intents", m.group(2)))
    head = open(target, encoding="utf-8").readline().rstrip("\n") if os.path.isfile(target) else ""
    titles_ok = titles_ok and head.split(": ", 1)[-1] == m.group(1)
    docs.append(os.path.relpath(target, MODEL))
    marks.append(m.group(4))
old_touches = b9[b9.index("**Touches:**") + 1:b9.index("**Touches:**") + 13]
naming = sorted(e["doc"] for k in ("domains", "capabilities", "features", "slices") for e in (after.get(k) or [])
                if "bi-9" in (e.get("intents") or []))
check("BI-9: 20 Touches lines", len(touches) == 20)
check("BI-9: the 12 old Touches lines first, unchanged", touches[:12] == old_touches)
check("BI-9: each link leads to its page, and each title is its page's title", titles_ok and len(docs) == 20)
check("BI-9: the 8 new lines all adds, capability first", marks[12:] == ["adds"] * 8 and docs[12] == f"{C}/capability.md")
check("BI-9: Touches equal the index entries naming bi-9", sorted(docs) == naming)
check("BI-9: every line it had is kept", all(l in bi9 for l in b9 if l.strip()))
check("BI-9: no line added but the 8 Touches lines", len(bi9) == len(b9) + 8)
check("BI-9: stage kept", next(l for l in bi9 if l.startswith("**Stage:**")) == next(l for l in b9 if l.startswith("**Stage:**")))

# 4. what changed under .garura/product/
status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", ".garura/product/"],
                        capture_output=True, text=True, check=True).stdout.rstrip("\n").split("\n")
allowed = (f"{MODEL}/_spine.yaml", f"{MODEL}/intents/bi-9.md", f"{MODEL}/{C}/")
check("only the spine, BI-9's page and the new folder changed under .garura/product/",
      all(s[3:].startswith(allowed) for s in status if s))

# 5. structure check
la = json.loads(subprocess.run(["python3", LINT, "--root", MODEL, "--spine", f"{MODEL}/_spine.yaml"],
                               capture_output=True, text=True).stdout)
with open(f"{HERE}/lint-after.json", "w", encoding="utf-8") as f:
    json.dump(la, f, indent=2, ensure_ascii=False)
    f.write("\n")
lb = json.load(open(f"{HERE}/lint-before.json"))
new_errors = [e for e in la["errors"] if e not in lb["errors"]]
check("structure check: no new error", not new_errors)
new_warnings = [w for w in la["warnings"] if w not in lb["warnings"]]
check("structure check: every new warning is the in-page ICE section one",
      all("no '## Agent intent (ICE)' yet" in w for w in new_warnings))

# 6. this folder holds no personal path
LOCAL = re.compile("|".join(["/" + w + "/" for w in ("Us" + "ers", "ho" + "me", "pri" + "vate", "t" + "mp")]
                            + ["scratch" + "pad", re.escape(os.path.expanduser("~")), re.escape(getpass.getuser())]), re.I)
bad = [os.path.join(d, f) for d, _, fs in os.walk(HERE) for f in fs
       if f != "verify.json" and LOCAL.search(open(os.path.join(d, f), encoding="utf-8", errors="replace").read())]
check("no file in the write folder names a home, temp or working folder, or a user name", not bad)

failed = [k for k, v in checks.items() if not v]
out = {"before_state": "git HEAD: the model as committed", "pages": pages, "new_folder_files": new_files,
       "bi_9_touches": touches, "git_status_product": status,
       "structure": {"before": [len(lb["errors"]), len(lb["warnings"])], "after": [len(la["errors"]), len(la["warnings"])],
                     "new_errors": new_errors, "new_warnings": new_warnings,
                     "errors_gone": len([e for e in lb["errors"] if e not in la["errors"]])},
       "write_folder_files_naming_local_paths": bad, "failed_checks": failed, "checks_run": len(checks)}
with open(f"{HERE}/verify.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(json.dumps({"failed": failed, "run": len(checks), "structure": out["structure"]["before"] and
                  {"before": out["structure"]["before"], "after": out["structure"]["after"],
                   "new_errors": new_errors, "errors_gone": out["structure"]["errors_gone"],
                   "new_warnings": len(new_warnings)}}, ensure_ascii=False))
