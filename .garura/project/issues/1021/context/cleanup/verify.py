"""Check #1021's last model work against the approved requests.

Run from the repo root after the model write and the plan removal. The model before the work is git HEAD.
Runs the structure check into lint-after.json and writes verify.json beside this file.
"""
import getpass, json, os, re, subprocess
import yaml

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = os.environ.get("VERIFY_MODEL", ".garura/product/product-os")
PLANS = ".garura/project/plans"
LINT = ".claude/skills/discover-capabilities/scripts/lint_grounding.py"
OLD_BI = ["bi-717", "bi-722", "bi-734", "bi-756", "bi-788"]
OLD_CAPS = {"cap-718": "cap-turn-intents-into-work", "cap-shape-eval": "cap-write-work-evals"}
OLD_DIRS = {"software-delivery-planning/cap-718/": "software-delivery-planning/turn-intents-into-work/",
            "software-delivery-planning/shape-eval/": "software-delivery-planning/write-work-evals/"}
SLICE = "sl-intent-to-design"
PLAN_IDS = [606, 717, 722, 734, 756, 767, 788]
checks = {}


def check(k, ok):
    checks[k] = bool(ok)


def git_show(path):
    r = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def now_path(page):
    for old, new in OLD_DIRS.items():
        if page.startswith(old):
            return new + page[len(old):]
    return page


link = json.load(open(f"{HERE}/link-request.json"))
moved = {p["id"]: p for p in link["parts"]}
lines = json.load(open(f"{HERE}/lines-request.json"))
r1 = json.load(open(f"{HERE}/remove-request-1.json"))

# 1. the named lines: each page is its HEAD text with exactly the named changes; the two merged pages are gone
for pg in lines["pages"]:
    head = git_show(f".garura/product/product-os/{pg['page']}").decode("utf-8").split("\n")
    want = list(head)
    for ch in pg["changes"]:
        if "old" in ch:
            want = [ch["new"] if l == ch["old"] else l for l in want]
        else:
            i = want.index(ch["after"])
            want[i + 1:i + 1] = [ch["add"]]
    cur = now_path(pg["page"])
    gone = pg["page"].endswith("/capability.md") and any(pg["page"].startswith(d) for d in OLD_DIRS)
    if gone:
        check(f"{pg['page']}: gone with its capability's merge", not os.path.exists(f"{MODEL}/{pg['page']}"))
        continue
    got = open(f"{MODEL}/{cur}", encoding="utf-8").read().split("\n") if os.path.isfile(f"{MODEL}/{cur}") else None
    check(f"{cur}: the HEAD page with only its {len(pg['changes'])} named change(s)", got == want)

# 2. the index
before = yaml.safe_load(git_show(f".garura/product/product-os/_spine.yaml"))
after = yaml.safe_load(open(f"{MODEL}/_spine.yaml", encoding="utf-8"))
by_id = lambda s, k: {e["id"]: e for e in (s.get(k) or [])}
cb, ca = by_id(before, "capabilities"), by_id(after, "capabilities")
fb, fa = by_id(before, "features"), by_id(after, "features")
check("capabilities: removed are exactly cap-718 and cap-shape-eval", sorted(set(cb) - set(ca)) == sorted(OLD_CAPS))
check("capabilities: none added", not (set(ca) - set(cb)))
cap_changed = {}
for i in ca:
    if ca[i] != cb[i]:
        diff = {k: (cb[i].get(k), ca[i].get(k)) for k in set(cb[i]) | set(ca[i]) if cb[i].get(k) != ca[i].get(k)}
        cap_changed[i] = diff
for i, diff in cap_changed.items():
    ok = True
    for k, (b, a) in diff.items():
        if k == "depends_on":
            fixed = []
            for x in b or []:
                y = OLD_CAPS.get(x, x)
                if y != i and y not in fixed:
                    fixed.append(y)
            ok = ok and fixed == (a or [])
        elif k == "intents" and i in OLD_CAPS.values():
            ok = ok and set(a) == set(b) | {"bi-1" if i == "cap-turn-intents-into-work" else "bi-3"} and set(b) <= set(a)
        else:
            ok = False
    check(f"{i}: changed only where a merged capability was named", ok)
check("features: none added or removed", set(fa) == set(fb))
feat_changed = sorted(i for i in fb if fa.get(i) != fb[i])
check("features: changed are exactly the five moved ones", feat_changed == sorted(moved))
rp = {x["id"]: x["intents"] for x in r1["repoint"]}
for f, p in moved.items():
    e, b = fa[f], fb[f]
    want_int = []
    for x in b.get("intents") or []:
        y = rp[f].get(x, x)
        if y and y not in want_int:
            want_int.append(y)
    strip = lambda x: {k: ({m: n for m, n in v.items() if m != "updated_by"} if k == "metadata" else v)
                       for k, v in x.items() if k not in ("capability", "doc", "intents")}
    rest_same = {k: v for k, v in strip(e).items() if v} == {k: v for k, v in strip(b).items() if v}
    check(f"{f}: under {p['capability']}, page {p['doc']}, intents {want_int}, nothing else changed",
          e.get("capability") == p["capability"] and e.get("doc") == p["doc"] and e.get("intents") == want_int and rest_same)
    check(f"{f}: its page is in the new folder and gone from the old one",
          os.path.isfile(f"{MODEL}/{p['doc']}") and not os.path.exists(f"{MODEL}/{b['doc']}"))
db, da = by_id(before, "domains"), by_id(after, "domains")
dom = "dom-software-delivery-planning"
check("domain: lost bi-717 and bi-788 from its intents, nothing else",
      set(db) == set(da) and da[dom].get("intents") == [x for x in db[dom].get("intents") or [] if x not in ("bi-717", "bi-788")]
      and {k: v for k, v in da[dom].items() if k != "intents"} == {k: v for k, v in db[dom].items() if k != "intents"})
sb, sa = by_id(before, "slices"), by_id(after, "slices")
check("slices: lost exactly sl-intent-to-design", sorted(set(sb) - set(sa)) == [SLICE] and not (set(sa) - set(sb)))
check("ices: unchanged", before.get("ices") == after.get("ices"))
check("profile: unchanged", before.get("profile") == after.get("profile"))
check("index sections: the same", sorted(before) == sorted(after))
left_int = [k + ":" + e["id"] for k in ("domains", "capabilities", "features", "slices") for e in (after.get(k) or [])
            if set(e.get("intents") or []) & set(OLD_BI)]
check("no index entry names an old intent", not left_int)

# 3. files gone
for b in OLD_BI:
    check(f"intents/{b}.md is gone", not os.path.exists(f"{MODEL}/intents/{b}.md"))
check(f"slices/{SLICE}.yaml is gone", not os.path.exists(f"{MODEL}/slices/{SLICE}.yaml"))
for d in OLD_DIRS:
    check(f"{d} is gone", not os.path.exists(f"{MODEL}/{d}"))

# 4. no page or the index still names a removed id or an old folder
mention = re.compile(r"(?<![\w-])(" + "|".join(OLD_BI + list(OLD_CAPS) + [SLICE]) + r")(?![\w-])|"
                     + "|".join(re.escape(d) for d in OLD_DIRS))
left = []
for d, _, fs in os.walk(os.path.dirname(MODEL)):
    for f in fs:
        if f.endswith((".md", ".yaml")):
            for n, l in enumerate(open(os.path.join(d, f), encoding="utf-8", errors="replace"), 1):
                if mention.search(l):
                    left.append(f"{os.path.join(d, f)}:{n}")
check("no page or the index names a removed id or an old folder", not left)

# 5. BI-1 and BI-3
intent_pages = {}
for bi, draft in (("bi-1", "intent-draft-bi-1.json"), ("bi-3", "intent-draft-bi-3.json")):
    new = open(f"{MODEL}/intents/{bi}.md", encoding="utf-8").read().split("\n")
    old = git_show(f".garura/product/product-os/intents/{bi}.md").decode("utf-8").split("\n")
    d = json.load(open(f"{HERE}/{draft}"))

    def touches(ls):
        i = ls.index("**Touches:**")
        out = []
        for l in ls[i + 1:]:
            if not l.startswith("- ["):
                break
            out.append(l)
        return out
    tn, to = touches(new), touches(old)
    ok, docs = True, []
    for l in tn:
        m = re.match(r"^- \[([^\]]+)\]\((\.\./[^)\s]+)\) \((capability|feature|domain)\) — (adds|changes)$", l)
        if not m:
            ok = False
            continue
        target = os.path.normpath(os.path.join(MODEL, "intents", m.group(2)))
        head = open(target, encoding="utf-8").readline().rstrip("\n") if os.path.isfile(target) else ""
        ok = ok and head.split(": ", 1)[-1] == m.group(1)
        docs.append(os.path.relpath(target, MODEL))
    naming = sorted(e["doc"] for k in ("domains", "capabilities", "features", "slices") for e in (after.get(k) or [])
                    if bi in (e.get("intents") or []))
    added = [l for l in tn if l not in to]
    check(f"{bi}: {len(d['touches'])} Touches lines, each leading to its page with its title", ok and len(tn) == len(d["touches"]))
    old_docs = [os.path.normpath(os.path.join("intents", re.search(r"\]\((\.\./[^)\s]+)\)", l).group(1))) for l in to]
    naming_before = sorted(e["doc"] for k in ("domains", "capabilities", "features", "slices") for e in (before.get(k) or [])
                           if bi in (e.get("intents") or []))
    gap_before = sorted(set(naming_before) - set(old_docs))
    gap_after = sorted(set(naming) - set(docs))
    check(f"{bi}: every Touches line is a part the index ties to {bi}", not (set(docs) - set(naming)))
    check(f"{bi}: no part the index ties to {bi} is missing from Touches that was not missing before", set(gap_after) <= set(gap_before))
    check(f"{bi}: every old Touches line kept; the added ones are the moved features, each 'changes'",
          all(l in tn for l in to) and len(added) == len(tn) - len(to) and all(l.endswith("— changes") for l in added))
    rest_old = [l for l in old if l not in to]
    check(f"{bi}: every other line it had is kept", all(l in new for l in rest_old if l.strip()))
    check(f"{bi}: stage kept", next(l for l in new if l.startswith("**Stage:**")) == next(l for l in old if l.startswith("**Stage:**")))
    intent_pages[bi] = {"touches_before": len(to), "touches_after": len(tn), "added": added,
                        "missing_before": gap_before, "missing_after": gap_after}

# 6. the plans folder
for p in PLAN_IDS:
    check(f"plan {p}: its file is gone", not os.path.exists(f"{PLANS}/{p}.yaml"))
check("plans/788/ is gone", not os.path.exists(f"{PLANS}/788"))
rep = f"{HERE}/remove-plans-report.json"
check("the plan removal report is there", os.path.isfile(rep))

# 7. only the named files changed under .garura/product/ and the plans folder
status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", ".garura/product/", PLANS],
                        capture_output=True, text=True, check=True).stdout.rstrip("\n").split("\n")
allowed = [f"{MODEL}/_spine.yaml", f"{MODEL}/intents/bi-1.md", f"{MODEL}/intents/bi-3.md", f"{MODEL}/slices/{SLICE}.yaml"] + \
          [f"{MODEL}/intents/{b}.md" for b in OLD_BI] + [f"{MODEL}/{d}" for d in OLD_DIRS] + \
          [f"{MODEL}/{now_path(p['page'])}" for p in lines["pages"]] + \
          [f"{MODEL}/{os.path.dirname(p['doc'])}/" for p in moved.values()] + \
          [f"{PLANS}/{p}.yaml" for p in PLAN_IDS] + [f"{PLANS}/788/"]
stray = [s for s in status if s and not any(s[3:].startswith(x) for x in allowed)]
check("only the named files changed under the model and the plans folder", not stray)

# 8. structure check
la = json.loads(subprocess.run(["python3", LINT, "--root", MODEL, "--spine", f"{MODEL}/_spine.yaml"], capture_output=True, text=True).stdout)
json.dump(la, open(f"{HERE}/lint-after.json", "w"), indent=2, ensure_ascii=False)
lb = json.load(open(f"{HERE}/lint-before.json"))
moved_back = lambda x: re.sub("|".join(re.escape(v) for v in OLD_DIRS.values()),
                              lambda m: {v: k for k, v in OLD_DIRS.items()}[m.group(0)], x)
new_errors = [e for e in la["errors"] if e not in lb["errors"] and moved_back(e) not in lb["errors"]]
new_warnings = [x for x in la["warnings"] if x not in lb["warnings"] and moved_back(x) not in lb["warnings"]]
check("structure check: no new error", not new_errors)
check("structure check: no new warning (a moved page's old warning counts as old)", not new_warnings)

# 9. no personal path in the cleanup folder
LOCAL = re.compile("|".join(["/" + x + "/" for x in ("Us" + "ers", "ho" + "me", "pri" + "vate", "t" + "mp")]
                            + ["scratch" + "pad", re.escape(os.path.expanduser("~")), re.escape(getpass.getuser())]), re.I)
bad = [os.path.join(d, f) for d, _, fs in os.walk(HERE) for f in fs
       if f != "verify.json" and LOCAL.search(open(os.path.join(d, f), encoding="utf-8", errors="replace").read())]
check("no file in the cleanup folder names a home, temp or working folder, or a user name", not bad)

failed = [k for k, v in checks.items() if not v]
out = {"failed": failed, "run": len(checks), "capabilities_changed": cap_changed, "features_changed": feat_changed,
       "left_mentions": left, "left_intents": left_int, "stray_files": stray, "personal_paths": bad, "intent_pages": intent_pages,
       "structure": {"before": [len(lb["errors"]), len(lb["warnings"])], "after": [len(la["errors"]), len(la["warnings"])],
                     "new_errors": new_errors, "new_warnings": new_warnings,
                     "errors_gone": len([e for e in lb["errors"] if e not in la["errors"] and e not in map(moved_back, la["errors"])])}}
json.dump(out, open(f"{HERE}/verify.json", "w"), indent=2, ensure_ascii=False, default=str)
print(json.dumps({"failed": failed, "run": len(checks), "structure": out["structure"]}, ensure_ascii=False, default=str)[:3000])
