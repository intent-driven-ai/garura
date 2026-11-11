"""Check BI-10's write against the approved drafts and requests.

Run from the repo root after the write. The model before the write is git HEAD. Runs the structure check into
lint-after.json and writes verify.json beside this file.
"""
import getpass, json, os, re, subprocess
import yaml

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
LINT = ".claude/skills/discover-capabilities/scripts/lint_grounding.py"
THIN = re.compile(r"^\s*(?:>\s*)?\**Thin(?: ICE)?\**\s*:", re.I)
OLD = ["fn-736", "fn-737", "fn-738", "fn-740", "fn-741", "fn-743", "fn-744", "fn-745", "fn-746"]
OLD_CAPS = ["cap-735", "cap-739", "cap-742"]
checks = {}


def check(k, ok):
    checks[k] = bool(ok)


def git_show(path):
    return subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, check=True).stdout


approved = json.load(open(f"{HERE}/approved-request.json"))
link = json.load(open(f"{HERE}/link-request.json"))
parts = {p["id"]: p for p in link["parts"]}
new_caps = [p["id"] for p in link["parts"] if p["kind"] == "capability"]
new_feats = [p["id"] for p in link["parts"] if p["kind"] == "feature" and p["mode"] == "new"]
ices = [p for p in link["parts"] if p["kind"] == "ice"]
thin_for = {p["for"] for p in ices if p["thin"]}

# 1. pages: each equals its draft, with the Thin line only on a thin ICE
for pg in approved["pages"]:
    m = f"{MODEL}/{pg['page']}"
    if pg["from"].startswith(f"{HERE}/approved/"):
        # a thin ICE: the page is the draft as approved, its Thin line put back by the index tool
        want =b"Thin: proposed from the person's words; deepen with `/discover-capabilities`.\n\n" + open(pg["from"], "rb").read()
    else:
        want = open(pg["from"], "rb").read()
    got = open(m, "rb").read() if os.path.isfile(m) else b""
    check(f"page {pg['page']} equals its approved draft", got == want)
    lines = got.decode("utf-8", "replace").split("\n")
    thin_lines = [i for i, l in enumerate(lines) if THIN.match(l)]
    is_thin_ice = pg["page"].endswith("ice.md") and pg["from"].startswith(f"{HERE}/approved/")
    check(f"page {pg['page']}: Thin line {'first only' if is_thin_ice else 'none'}", thin_lines == ([0] if is_thin_ice else []))

# 2. the index
before = yaml.safe_load(git_show(f"{MODEL}/_spine.yaml"))
after = yaml.safe_load(open(f"{MODEL}/_spine.yaml", encoding="utf-8"))
by_id = lambda s, k: {e["id"]: e for e in (s.get(k) or [])}
cb, ca = by_id(before, "capabilities"), by_id(after, "capabilities")
fb, fa = by_id(before, "features"), by_id(after, "features")
ib, ia = by_id(before, "ices"), by_id(after, "ices")
check("capabilities: new are exactly the six", sorted(set(ca) - set(cb)) == sorted(new_caps))
check("capabilities: removed are exactly the three old ones", sorted(set(cb) - set(ca)) == sorted(OLD_CAPS))
check("capabilities: no other capability changed", all(ca[i] == cb[i] for i in cb if i in ca))
check("features: new are exactly the drafted ones", sorted(set(fa) - set(fb)) == sorted(new_feats))
check("features: none removed", not (set(fb) - set(fa)))
changed = sorted(i for i in fb if i in fa and fa[i] != fb[i])
check("features: changed are exactly the nine old ones", changed == sorted(OLD))
check("ices: new are exactly the requested ones", sorted(set(ia) - set(ib)) == sorted(p["id"] for p in ices))
check("ices: none removed or changed", all(ia.get(i) == ib[i] for i in ib))
for k in ("domains", "slices"):
    check(f"{k}: unchanged", before.get(k) == after.get(k))
for c in new_caps:
    e, r = ca.get(c, {}), parts[c]
    check(f"{c}: domain, intents, page and one-line as requested, not thin",
          e.get("domain") == r["domain"] and e.get("intents") == r["intents"] and e.get("doc") == r["doc"]
          and e.get("one_line") == r["one_line"] and not (e.get("metadata") or {}).get("thin"))
    check(f"{c}: depends on no capability that is gone, nor on itself",
          not (set(e.get("depends_on") or []) & (set(OLD_CAPS) | {c})))
for f in new_feats:
    e, r = fa.get(f, {}), parts[f]
    check(f"{f}: capability, intents, page and one-line as requested, not thin",
          e.get("capability") == r["capability"] and e.get("intents") == r["intents"] and e.get("doc") == r["doc"]
          and e.get("one_line") == r["one_line"] and not (e.get("metadata") or {}).get("thin"))
for f in OLD:
    e = fa.get(f, {})
    check(f"{f}: now under Standards, intents [bi-10], page unmoved, new one-line",
          e.get("capability") == "cap-standards" and e.get("intents") == ["bi-10"]
          and e.get("doc") == f"features/{f}/feature.md" and e.get("one_line") == parts[f]["one_line"])
for p in ices:
    e = ia.get(p["id"], {})
    check(f"{p['id']}: for {p['for']}, its page, thin {p['thin']}",
          e.get("for") == p["for"] and e.get("doc") == p["doc"] and bool((e.get("metadata") or {}).get("thin")) == p["thin"])
    check(f"{p['id']}: the only ICE of {p['for']}", [i for i, x in ia.items() if x.get("for") == p["for"]] == [p["id"]])
names_734 = [k + ":" + e["id"] for k in ("capabilities", "features") for e in (after.get(k) or []) if "bi-734" in (e.get("intents") or [])]
check("no capability or feature still names bi-734", not names_734)
mention = re.compile(r"(?<![\w-])(cap-735|cap-739|cap-742)(?![\w-])")
left = [f"{d}/{f}" for d, _, fs in os.walk(".garura/product") for f in fs if f.endswith((".md", ".yaml"))
        and mention.search(open(os.path.join(d, f), encoding="utf-8", errors="replace").read())]
check("no page or the spine names cap-735, cap-739 or cap-742", not left)
for c in OLD_CAPS:
    check(f"capabilities/{c} is gone", not os.path.exists(f"{MODEL}/capabilities/{c}"))

# 3. BI-10's page
b10 = open(f"{MODEL}/intents/bi-10.md", encoding="utf-8").read().split("\n")
o10 = git_show(f"{MODEL}/intents/bi-10.md").decode("utf-8").split("\n")
draft = json.load(open(f"{HERE}/intent-draft.json"))
ti = b10.index("**Touches:**")
tl = []
for l in b10[ti + 1:]:
    if not l.startswith("- ["):
        break
    tl.append(l)
docs, ok = [], True
for l in tl:
    m = re.match(r"^- \[([^\]]+)\]\((\.\./[^)\s]+)\) \((capability|feature)\) — (adds|changes)$", l)
    if not m:
        ok = False
        continue
    target = os.path.normpath(os.path.join(MODEL, "intents", m.group(2)))
    head = open(target, encoding="utf-8").readline().rstrip("\n") if os.path.isfile(target) else ""
    ok = ok and head.split(": ", 1)[-1] == m.group(1)
    docs.append(os.path.relpath(target, MODEL))
naming = sorted(e["doc"] for k in ("domains", "capabilities", "features", "slices") for e in (after.get(k) or [])
                if "bi-10" in (e.get("intents") or []))
check(f"BI-10: {len(draft['touches'])} Touches lines, each leading to its page with its title", ok and len(tl) == len(draft["touches"]))
check("BI-10: Touches equal the index entries naming bi-10", sorted(docs) == naming)
check("BI-10: every line it had is kept", all(l in b10 for l in o10 if l.strip()))
check("BI-10: stage kept", next(l for l in b10 if l.startswith("**Stage:**")) == next(l for l in o10 if l.startswith("**Stage:**")))

# 4. the named line on fn-725
lr = json.load(open(f"{HERE}/lines-request.json"))["pages"][0]
a = open(f"{MODEL}/{lr['page']}", encoding="utf-8").read().split("\n")
b = git_show(f"{MODEL}/{lr['page']}").decode("utf-8").split("\n")
diff = [(x, y) for x, y in zip(b, a) if x != y]
check("fn-725: one line changed, to the requested words", len(a) == len(b) and diff == [(lr["changes"][0]["old"], lr["changes"][0]["new"])])

# 5. what changed under .garura/product/
status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", ".garura/product/"],
                        capture_output=True, text=True, check=True).stdout.rstrip("\n").split("\n")
allowed = [f"{MODEL}/_spine.yaml", f"{MODEL}/intents/bi-10.md", f"{MODEL}/features/fn-725/feature.md"] + \
          [f"{MODEL}/capabilities/{c}/" for c in OLD_CAPS] + [f"{MODEL}/features/{f}/" for f in OLD] + \
          [f"{MODEL}/software-delivery-planning/{p['slug']}/" for p in link["parts"] if p["kind"] == "capability"]
check("only the named files changed under .garura/product/", all(any(s[3:].startswith(x) for x in allowed) for s in status if s))

# 6. structure check
la = json.loads(subprocess.run(["python3", LINT, "--root", MODEL, "--spine", f"{MODEL}/_spine.yaml"], capture_output=True, text=True).stdout)
json.dump(la, open(f"{HERE}/lint-after.json", "w"), indent=2, ensure_ascii=False)
lb = json.load(open(f"{HERE}/lint-before.json"))
new_errors = [e for e in la["errors"] if e not in lb["errors"]]
new_warnings = [x for x in la["warnings"] if x not in lb["warnings"]]
check("structure check: no new error", not new_errors)
check("structure check: every new warning is the in-page ICE section one", all("no '## Agent intent (ICE)' yet" in x for x in new_warnings))

# 7. no personal path in the write folder
LOCAL = re.compile("|".join(["/" + x + "/" for x in ("Us" + "ers", "ho" + "me", "pri" + "vate", "t" + "mp")]
                            + ["scratch" + "pad", re.escape(os.path.expanduser("~")), re.escape(getpass.getuser())]), re.I)
bad = [os.path.join(d, f) for d, _, fs in os.walk(HERE) for f in fs
       if f != "verify.json" and LOCAL.search(open(os.path.join(d, f), encoding="utf-8", errors="replace").read())]
check("no file in the write folder names a home, temp or working folder, or a user name", not bad)

failed = [k for k, v in checks.items() if not v]
out = {"failed": failed, "run": len(checks), "features_changed": changed, "left_mentions": left, "names_734": names_734,
       "structure": {"before": [len(lb["errors"]), len(lb["warnings"])], "after": [len(la["errors"]), len(la["warnings"])],
                     "new_errors": new_errors, "errors_gone": len([e for e in lb["errors"] if e not in la["errors"]]),
                     "new_warnings": len(new_warnings)}}
json.dump(out, open(f"{HERE}/verify.json", "w"), indent=2, ensure_ascii=False)
print(json.dumps({"failed": failed, "run": len(checks), "structure": out["structure"]}, ensure_ascii=False)[:3000])
