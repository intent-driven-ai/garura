"""Verify the write of Orchestrate agent work through planning (BI-9 capability 1) and its take-in
of View plans, Manage a plan and Shape a slice.

Run from the repo root after the write. Reads the model, the drafts and the model as committed at
HEAD (git show). Writes verify.json in this folder.
"""
import getpass
import json
import os
import re
import subprocess

import yaml

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
ISSUE = ".garura/project/issues/1021/context/bi-9-capability-1"
DRAFTS = f"{ISSUE}/drafts/product-os"
MODEL = ".garura/product/product-os"
C = "software-delivery-planning/orchestrate-agent-work"
CAP = "cap-orchestrate-agent-work"
NEW = ["fn-go-to-plan-branch", "fn-know-what-next", "fn-remove-plan", "fn-choose-next-item",
       "fn-work-out-waits-on", "fn-pause-plan"]
OLD = ["fn-729", "fn-806", "fn-628", "fn-730"]
THIN_ICE = {"fn-choose-next-item", "fn-work-out-waits-on", "fn-pause-plan"}
GONE = ["cap-719", "cap-720", "cap-shape-slice"]
THIN = re.compile(r"^\s*(?:>\s*)?\**Thin(?: ICE)?\**\s*:", re.I)
WORD = re.compile(r"(?<![\w-])(cap-719|cap-720|cap-shape-slice)(?![\w-])")
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


# 1. pages: (model path, draft path)
pairs = [(f"{C}/capability.md", f"{C}/capability.md"), (f"{C}/ice.md", f"{C}/ice.md")]
for fn in NEW:
    pairs += [(f"{C}/{fn}/feature.md", f"{C}/{fn}/feature.md"), (f"{C}/{fn}/ice.md", f"{C}/{fn}/ice.md")]
for fn in OLD:
    pairs += [(f"features/{fn}/feature.md", f"features/{fn}/feature.md"), (f"features/{fn}/ice.md", f"features/{fn}/ice.md")]
pairs += [(f"{C}/fn-795/feature.md", "software-delivery-planning/shape-slice/fn-795/feature.md"),
          (f"{C}/fn-795/ice.md", "software-delivery-planning/shape-slice/fn-795/ice.md")]
pages = {}
for m, d in pairs:
    ok = os.path.isfile(f"{MODEL}/{m}") and rb(f"{MODEL}/{m}") == rb(f"{DRAFTS}/{d}")
    lines = open(f"{MODEL}/{m}", encoding="utf-8").read().split("\n") if os.path.isfile(f"{MODEL}/{m}") else []
    thin_lines = [i for i, l in enumerate(lines) if THIN.match(l)]
    part = m.split("/")[-2]
    want_thin = m.endswith("ice.md") and part in THIN_ICE
    check(f"page {m} equals its approved draft byte for byte", ok)
    check(f"page {m} Thin lines as it should ({'one, first' if want_thin else 'none'})",
          thin_lines == ([0] if want_thin else []))
    check(f"page {m} holds no ICE section", "## Agent intent (ICE)" not in lines)
    pages[m] = {"equals_draft": ok, "thin_lines": thin_lines}
check("24 pages", len(pairs) == 24)
new_files = sorted(os.path.relpath(os.path.join(d, f), MODEL) for d, _, fs in os.walk(f"{MODEL}/{C}") for f in fs)
check("the new capability folder holds only its 16 pages", new_files == sorted(m for m, _ in pairs if m.startswith(C + "/")))
for fn in OLD:
    check(f"features/{fn} holds only feature.md and ice.md", sorted(os.listdir(f"{MODEL}/features/{fn}")) == ["feature.md", "ice.md"])
for gone in ("capabilities/cap-719", "capabilities/cap-720", "software-delivery-planning/shape-slice"):
    check(f"{gone} is gone", not os.path.exists(f"{MODEL}/{gone}"))

# 2. index
before = yaml.safe_load(git_show(f"{MODEL}/_spine.yaml"))
after = yaml.safe_load(open(f"{MODEL}/_spine.yaml", encoding="utf-8"))


def by_id(s, k):
    return {e["id"]: e for e in (s.get(k) or [])}


caps_b, caps_a = by_id(before, "capabilities"), by_id(after, "capabilities")
feats_b, feats_a = by_id(before, "features"), by_id(after, "features")
ices_a = by_id(after, "ices")
ices_b = by_id(before, "ices")
check("capabilities: new is exactly the new one", sorted(set(caps_a) - set(caps_b)) == [CAP])
check("capabilities: removed are exactly the three old ones", sorted(set(caps_b) - set(caps_a)) == sorted(GONE))
check("capabilities: no other old capability changed",
      all(caps_a[i] == caps_b[i] for i in caps_b if i in caps_a))
check("features: new are exactly the six", sorted(set(feats_a) - set(feats_b)) == sorted(NEW))
check("features: none removed", not (set(feats_b) - set(feats_a)))
changed_f = sorted(i for i in feats_b if i in feats_a and feats_a[i] != feats_b[i])
check("features: changed are exactly the five old ones and fn-931", changed_f == sorted(OLD + ["fn-795", "fn-931"]))
want_ices = sorted([ice_id(CAP)] + [ice_id(f) for f in NEW + OLD + ["fn-795"]])
check("ices: new are exactly the twelve", sorted(set(ices_a) - set(ices_b)) == want_ices)
check("ices: none removed or changed", all(ices_a.get(i) == ices_b[i] for i in ices_b))
c = caps_a.get(CAP, {})
cap_page = open(f"{MODEL}/{C}/capability.md", encoding="utf-8").read().split("\n")
cap_line = cap_page[cap_page.index("## Directional intent") + 1]
check("capability entry as asked", c.get("domain") == "dom-software-delivery-planning" and c.get("intents") == ["bi-9"]
      and c.get("doc") == f"{C}/capability.md" and c.get("one_line") == cap_line
      and not (c.get("metadata") or {}).get("thin"))
items = {}
for l in cap_page:
    m = re.match(r"^- (.+?) \((fn-[a-z0-9-]+)\): (.+)$", l)
    if m:
        items[m.group(2)] = m.group(3)
# The three unbuilt features' one-lines were approved apart from the list (link-request-3.json).
approved_lines = {p["id"]: p["one_line"] for p in json.load(open(f"{HERE}/link-request-3.json"))["parts"]}
items.update(approved_lines)
for fn in NEW + OLD + ["fn-795"]:
    e = feats_a[fn]
    doc = f"features/{fn}/feature.md" if fn in OLD else f"{C}/{fn}/feature.md"
    check(f"{fn}: under the new capability, intents [bi-9], page at {doc}",
          e.get("capability") == CAP and e.get("intents") == ["bi-9"] and e.get("doc") == doc)
    check(f"{fn}: one-line from the capability page's list", e.get("one_line") == items[fn][0].upper() + items[fn][1:])
    check(f"{fn}: carries no thin mark", not (e.get("metadata") or {}).get("thin"))
f931 = feats_a["fn-931"]
check("fn-931: filed under Turn intents into agent work, intents [bi-1], page unmoved",
      f931.get("capability") == "cap-turn-intents-into-work" and f931.get("intents") == ["bi-1"]
      and f931.get("doc") == "features/fn-931/feature.md")
for part in [CAP] + NEW + OLD + ["fn-795"]:
    iid = ice_id(part)
    e = ices_a.get(iid, {})
    fn = part
    doc = f"{C}/ice.md" if part == CAP else (f"features/{fn}/ice.md" if fn in OLD else f"{C}/{fn}/ice.md")
    thin = bool((e.get("metadata") or {}).get("thin"))
    check(f"{iid}: for {part}, page {doc}, thin {part in THIN_ICE}",
          e.get("for") == part and e.get("doc") == doc and thin == (part in THIN_ICE))
    check(f"{iid}: the only ICE of {part}", [i for i, x in ices_a.items() if x.get("for") == part] == [iid])

# 3. the removed ids are named nowhere
mentions = []
for d, _, fs in os.walk(".garura/product"):
    for f in fs:
        if f.endswith((".md", ".yaml")):
            p = os.path.join(d, f)
            for n, line in enumerate(open(p, encoding="utf-8", errors="replace").read().split("\n"), 1):
                if WORD.search(line):
                    mentions.append(f"{p}:{n}")
check("no page or the spine names cap-719, cap-720 or cap-shape-slice", not mentions)

# 4. the five named lines
named = {
    "software-delivery-planning/turn-intents-into-work/capability.md": "fn-931 is filed under this capability, and the rest of Manage a plan merged into Orchestrate agent work through planning (cap-orchestrate-agent-work).",
    "features/fn-725/feature.md": "Work out the plans a plan waits on (fn-work-out-waits-on), in Orchestrate agent work through planning, owns it.",
    "features/fn-726/feature.md": "- Showing plans. Orchestrate agent work through planning (cap-orchestrate-agent-work) shows the plan tree, which has no domain level.",
    "intents/bi-788.md": "- [Orchestrate agent work through planning](../software-delivery-planning/orchestrate-agent-work/capability.md) (capability) — changes",
    "software-delivery-planning/turn-intents-into-work/fn-change-work-items/feature.md": "bi-9-capability-1/research.md, which keeps the earlier page of features/fn-730/feature.md",
}
for p, words in named.items():
    b = git_show(f"{MODEL}/{p}").decode("utf-8").split("\n")
    a = open(f"{MODEL}/{p}", encoding="utf-8").read().split("\n")
    diff = [(x, y) for x, y in zip(b, a) if x != y]
    check(f"{p}: one line changed, to the approved words", len(b) == len(a) and len(diff) == 1 and words in diff[0][1])

# 5. BI-9
bi9 = open(f"{MODEL}/intents/bi-9.md", encoding="utf-8").read().split("\n")
b9 = git_show(f"{MODEL}/intents/bi-9.md").decode("utf-8").split("\n")
ti = bi9.index("**Touches:**") if "**Touches:**" in bi9 else -1
touches = []
for l in bi9[ti + 1:] if ti >= 0 else []:
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
naming = sorted(e["doc"] for k in ("domains", "capabilities", "features", "slices") for e in (after.get(k) or [])
                if "bi-9" in (e.get("intents") or []))
check("BI-9: 12 Touches lines", len(touches) == 12)
check("BI-9: each link leads to its page, and each title is its page's title", titles_ok and len(docs) == 12)
check("BI-9: 7 adds, then 5 changes", marks == ["adds"] * 7 + ["changes"] * 5)
check("BI-9: Touches equal the index entries naming bi-9", sorted(docs) == naming)
kept = [l for l in b9 if l.strip()]
check("BI-9: every line it had is kept", all(l in bi9 for l in kept))
check("BI-9: stage kept", next(l for l in bi9 if l.startswith("**Stage:**")) == next(l for l in b9 if l.startswith("**Stage:**")))

# 6. what changed under .garura/product/
status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", ".garura/product/"],
                        capture_output=True, text=True, check=True).stdout.rstrip("\n").split("\n")
allowed = (f"{MODEL}/_spine.yaml", f"{MODEL}/intents/bi-9.md", f"{MODEL}/intents/bi-788.md",
           f"{MODEL}/features/fn-725/", f"{MODEL}/features/fn-726/", f"{MODEL}/{C}/",
           f"{MODEL}/software-delivery-planning/turn-intents-into-work/capability.md",
           f"{MODEL}/software-delivery-planning/turn-intents-into-work/fn-change-work-items/",
           f"{MODEL}/capabilities/cap-719/", f"{MODEL}/capabilities/cap-720/",
           f"{MODEL}/software-delivery-planning/shape-slice/") + tuple(f"{MODEL}/features/{f}/" for f in OLD)
check("only the named files changed under .garura/product/", all(s[3:].startswith(allowed) for s in status if s))

# 7. structure check
lb, la = json.load(open(f"{HERE}/lint-before.json")), json.load(open(f"{HERE}/lint-after.json"))
new_errors = [e for e in la["errors"] if e not in lb["errors"]]
check("structure check: no new error", not new_errors)

# 8. this folder holds no personal path
LOCAL = re.compile("|".join(["/" + w + "/" for w in ("Us" + "ers", "ho" + "me", "pri" + "vate", "t" + "mp")]
                            + ["scratch" + "pad", re.escape(os.path.expanduser("~")), re.escape(getpass.getuser())]), re.I)
bad = [os.path.join(d, f) for d, _, fs in os.walk(HERE) for f in fs
       if LOCAL.search(open(os.path.join(d, f), encoding="utf-8", errors="replace").read())]
check("no file in the write folder names a home, temp or working folder, or a user name", not bad)

failed = [k for k, v in checks.items() if not v]
out = {"before_state": "git HEAD: the model as committed", "pages": pages, "new_folder_files": new_files,
       "features_changed": changed_f, "mentions_of_removed_ids": mentions, "bi_9_touches": touches,
       "git_status_product": status,
       "structure": {"before": [len(lb["errors"]), len(lb["warnings"])], "after": [len(la["errors"]), len(la["warnings"])],
                     "new_errors": new_errors, "errors_gone": len([e for e in lb["errors"] if e not in la["errors"]])},
       "write_folder_files_naming_local_paths": bad, "failed_checks": failed, "checks_run": len(checks),
       "all_checks_pass": not failed, "checks": checks}
with open(f"{HERE}/verify.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
    f.write("\n")
print(json.dumps({"failed": failed, "run": len(checks), "structure": out["structure"]}, indent=1))
