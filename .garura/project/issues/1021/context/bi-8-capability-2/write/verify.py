"""Verify the write of Review what agents make (Argus), BI-8's second capability.

Run from the repo root after the write. Reads the model, the drafts, the requests and reports in
this folder, and the model as committed at HEAD (git show). Writes verify.json in this folder.
"""
import difflib
import getpass
import json
import os
import re
import subprocess

import yaml

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
ISSUE = ".garura/project/issues/1021/context/bi-8-capability-2"
DRAFTS = f"{ISSUE}/drafts/product-os"
MODEL = ".garura/product/product-os"
C = "software-delivery-planning/review-agent-work"
CAP = "cap-review-agent-work"
ORDER = ["fn-open-review", "fn-read-outcome", "fn-answer-pieces", "fn-review-adrs", "fn-review-memory",
         "fn-check-agent-decisions", "fn-send-back", "fn-apply-answers", "fn-run-tool-apart"]
THIN = re.compile(r"^\s*(?:>\s*)?\**Thin(?: ICE)?\**\s*:", re.I)
AFTER_LINE = ("- [Keep the docs and command pages in step with each change]"
              "(../software-delivery-planning/ship-every-change/fn-keep-docs-in-step/feature.md) (feature) — adds")

checks = {}


def check(name, ok):
    checks[name] = bool(ok)
    return ok


def git_show(path):
    return subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, check=True).stdout


def ice_id(part):
    return "ice-" + (part[3:] if part.startswith("fn-") else part[4:])


def rb(path):
    with open(path, "rb") as f:
        return f.read()


def cap1(t):
    return t[0].upper() + t[1:]


# ---- 1. pages
pages = {}
model_pages = [f"{C}/capability.md", f"{C}/ice.md"]
for fn in ORDER:
    model_pages += [f"{C}/{fn}/feature.md", f"{C}/{fn}/ice.md"]
for p in model_pages:
    page, draft = rb(f"{MODEL}/{p}"), rb(f"{DRAFTS}/{p}")
    lines = page.decode("utf-8").split("\n")
    thin_lines = [i for i, l in enumerate(lines) if THIN.match(l)]
    info = {"equals_draft": page == draft, "bytes": len(page), "thin_lines_on_page": len(thin_lines),
            "ice_section_on_page": "## Agent intent (ICE)" in lines}
    check(f"page {p} equals draft byte for byte", page == draft)
    check(f"page {p} holds no ICE section", not info["ice_section_on_page"])
    if p.endswith("/ice.md"):
        part = p.split("/")[-2]
        copy_path = f"{HERE}/approved/ice.md" if part == "review-agent-work" else f"{HERE}/approved/{part}/ice.md"
        copy = rb(copy_path)
        info.update({"thin_line_first": thin_lines == [0], "blank_after_thin_line": lines[1] == "",
                     "equals_copy_with_thin_line_back": page.split(b"\n", 2)[2] == copy,
                     "copy_has_no_thin_line": not any(THIN.match(l) for l in copy.decode().split("\n"))})
        check(f"{p}: one Thin line, first, blank after, rest = approved copy",
              thin_lines == [0] and lines[1] == "" and info["equals_copy_with_thin_line_back"]
              and info["copy_has_no_thin_line"])
    else:
        check(f"page {p} carries no Thin line", not thin_lines)
    pages[p] = info

new_files = sorted(os.path.relpath(os.path.join(d, f), MODEL) for d, _, fs in os.walk(f"{MODEL}/{C}") for f in fs)
check("new folder holds only the 20 pages", new_files == sorted(model_pages) and len(new_files) == 20)

# ---- 2. index
spine_path = f"{MODEL}/_spine.yaml"
before_text = git_show(spine_path).decode("utf-8")
after_text = open(spine_path, encoding="utf-8").read()
before, after = yaml.safe_load(before_text), yaml.safe_load(after_text)
LISTS = ["domains", "capabilities", "features", "slices", "ices"]


def by_id(s, k):
    return {e["id"]: e for e in (s.get(k) or [])}


asked_new = {"capabilities": [CAP], "features": ORDER, "ices": [ice_id(CAP)] + [ice_id(f) for f in ORDER],
             "domains": [], "slices": []}
spine = {}
all_before_ids = {e["id"] for k in LISTS for e in (before.get(k) or [])}
for k in LISTS:
    b, a = by_id(before, k), by_id(after, k)
    new = [i for i in a if i not in b]
    removed = [i for i in b if i not in a]
    changed = [i for i in b if i in a and b[i] != a[i]]
    kept_order = [i for i in b if i in a] == [i for i in a if i in b]
    spine[k] = {"before": len(b), "after": len(a), "new": new, "removed": removed,
                "old_entries_changed": changed, "old_order_kept": kept_order}
    check(f"spine {k}: new entries are exactly the ones asked, in order", new == asked_new.get(k, []))
    check(f"spine {k}: nothing removed", not removed)
    check(f"spine {k}: no old entry changed", not changed)
    check(f"spine {k}: order of the old entries kept", kept_order)
check("every new id was unused before the write", not ({i for v in asked_new.values() for i in v} & all_before_ids))
check("spine: other top keys unchanged", all(before[k] == after[k] for k in before if k not in LISTS))
check("spine: top key order kept", list(before) == list(after))

cap_page = open(f"{MODEL}/{C}/capability.md", encoding="utf-8").read().split("\n")
cap_one_line = cap_page[cap_page.index("## Directional intent") + 1]
items = {}
for l in cap_page:
    m = re.match(r"^- (.+?) \((fn-[a-z0-9-]+)\): (.+)$", l)
    if m:
        items[m.group(2)] = {"title": m.group(1), "text": m.group(3)}
check("feature list order on the capability page = the nine features in order", list(items) == ORDER)

caps, feats, ices = by_id(after, "capabilities"), by_id(after, "features"), by_id(after, "ices")
entries = {}
c = caps[CAP]
entries[CAP] = c
check("capability entry as asked",
      c["slug"] == "review-agent-work" and c["domain"] == "dom-software-delivery-planning"
      and c["intents"] == ["bi-8"] and c["doc"] == f"{C}/capability.md" and c["status"] == "proposed"
      and not (c.get("metadata") or {}).get("thin"))
check("capability one_line = the line under its Directional intent, word for word", c["one_line"] == cap_one_line)
for fn in ORDER:
    e = feats[fn]
    entries[fn] = e
    check(f"feature {fn} as asked",
          e["slug"] == fn and e["capability"] == CAP and e["intents"] == ["bi-8"]
          and e["doc"] == f"{C}/{fn}/feature.md" and e["status"] == "proposed"
          and not (e.get("metadata") or {}).get("thin"))
    check(f"{fn} one_line = its feature-list text, first letter capitalised", e["one_line"] == cap1(items[fn]["text"]))
ice_entries = {}
expect_ices = [(ice_id(CAP), CAP, "capability", f"{C}/ice.md")] + \
    [(ice_id(fn), fn, "feature", f"{C}/{fn}/ice.md") for fn in ORDER]
for iid, part, kind, doc in expect_ices:
    e = ices[iid]
    thin = bool((e.get("metadata") or {}).get("thin"))
    ice_entries[iid] = {"for": e["for"], "for_kind": e["for_kind"], "doc": e["doc"], "thin": thin,
                        "doc_leads_to_file": os.path.isfile(f"{MODEL}/{e['doc']}")}
    check(f"ICE {iid} as asked, thin", e["for"] == part and e["for_kind"] == kind and e["doc"] == doc
          and thin and ice_entries[iid]["doc_leads_to_file"])
    check(f"ICE {iid}: the only ICE for {part}", [x["id"] for x in after["ices"] if x["for"] == part] == [iid])
    page_thin = any(THIN.match(l) for l in open(f"{MODEL}/{doc}", encoding="utf-8").read().split("\n"))
    check(f"ICE {iid}: thin mark on entry and page agree", page_thin == thin)
check("no part of this write is thin itself", not any((e.get("metadata") or {}).get("thin") for e in entries.values()))

# ---- 3. spine text: only added lines
removed_lines, added_lines = [], []
for l in difflib.ndiff(before_text.split("\n"), after_text.split("\n")):
    if l.startswith("- "):
        removed_lines.append(l[2:])
    elif l.startswith("+ "):
        added_lines.append(l[2:])
spine_text = {"lines_removed_or_replaced": removed_lines, "lines_added": len(added_lines),
              "comment_lines_before": sum(1 for l in before_text.split("\n") if l.lstrip().startswith("#")),
              "comment_lines_after": sum(1 for l in after_text.split("\n") if l.lstrip().startswith("#"))}
check("spine only gained lines", not removed_lines)
check("spine comments kept", spine_text["comment_lines_before"] == spine_text["comment_lines_after"])

# ---- 4. BI-8
bi8 = f"{MODEL}/intents/bi-8.md"
b8 = git_show(bi8).decode("utf-8").split("\n")
a8 = open(bi8, encoding="utf-8").read().split("\n")
ops = [op for op in difflib.SequenceMatcher(a=b8, b=a8, autojunk=False).get_opcodes() if op[0] != "equal"]
inserted = a8[ops[0][3]:ops[0][4]] if ops else []
want = [f"- [Review what agents make (Argus)](../{C}/capability.md) (capability) — adds"] + \
    [f"- [{items[fn]['title']}](../{C}/{fn}/feature.md) (feature) — adds" for fn in ORDER]
check("BI-8's page gained only the ten lines, in one place, right after the docs line",
      len(ops) == 1 and ops[0][0] == "insert" and inserted == want and a8[ops[0][3] - 1] == AFTER_LINE)
check("BI-8's page: every other line byte for byte",
      rb(bi8) == git_show(bi8).replace((AFTER_LINE + "\n").encode(), (AFTER_LINE + "\n" + "\n".join(want) + "\n").encode(), 1))
ti = a8.index("**Touches:**")
touches = []
for l in a8[ti + 1:]:
    if not l.startswith("- ["):
        break
    touches.append(l)
links, titles, marks = {}, {}, []
for l in touches:
    m = re.match(r"^- \[([^\]]+)\]\((\.\./[^)\s]+)\) \((capability|feature)\) — (adds|changes)$", l)
    check(f"Touches line form: {l[:60]}", m)
    if not m:
        continue
    target = os.path.normpath(os.path.join(MODEL, "intents", m.group(2)))
    links[m.group(2)] = os.path.isfile(target)
    head = open(target, encoding="utf-8").readline().rstrip("\n") if links[m.group(2)] else ""
    titles[m.group(2)] = head.split(": ", 1)[1] == m.group(1) if ": " in head else False
    marks.append(m.group(4))
touch_docs = sorted(os.path.relpath(os.path.normpath(os.path.join(MODEL, "intents", k)), MODEL) for k in links)
naming_bi8 = [(e["id"], e["doc"]) for k in LISTS for e in (after.get(k) or []) if "bi-8" in (e.get("intents") or [])]
check("BI-8's Touches: 19 lines", len(touches) == 19)
check("BI-8's Touches: each link leads to a file", all(links.values()))
check("BI-8's Touches: each title is its page's title", all(titles.values()))
check("BI-8's Touches: marks (fn-731 and fn-673 changes, all else adds)",
      marks == ["adds", "changes", "adds", "adds", "changes"] + ["adds"] * 14)
check("the 19 index entries that name bi-8 match the 19 Touches lines one for one",
      len(naming_bi8) == 19 and sorted(d for _, d in naming_bi8) == touch_docs and len(set(touch_docs)) == 19)
bi_8 = {"lines_before": len(b8), "lines_after": len(a8), "added": inserted, "touches_lines": len(touches),
        "index_entries_naming_bi_8": [i for i, _ in naming_bi8]}

# ---- 5. what changed under .garura/product/
status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", ".garura/product/"],
                        capture_output=True, text=True, check=True).stdout.rstrip("\n").split("\n")
ok_status = all(s[3:] in {spine_path, bi8} or s[3:].startswith(f"{MODEL}/{C}/") for s in status if s)
check("under .garura/product/ only the spine, bi-8.md and the new folder changed", ok_status)

# ---- 6. structure check
def load(name):
    return json.load(open(f"{HERE}/{name}"))


lb, la = load("lint-before.json"), load("lint-after.json")
structure = {"before": {"errors": len(lb["errors"]), "warnings": len(lb["warnings"])},
             "after": {"errors": len(la["errors"]), "warnings": len(la["warnings"])},
             "new_errors": [e for e in la["errors"] if e not in lb["errors"]],
             "errors_gone": [e for e in lb["errors"] if e not in la["errors"]],
             "new_warnings": [w for w in la["warnings"] if w not in lb["warnings"]],
             "warnings_gone": [w for w in lb["warnings"] if w not in la["warnings"]]}
check("structure check: no new error", not structure["new_errors"])
check("structure check: each new warning is on one of the ten new part pages",
      len(structure["new_warnings"]) == 10
      and all(any(f"{MODEL}/{p}" in w for p in model_pages if not p.endswith("/ice.md")) for w in structure["new_warnings"]))

# ---- 7. this folder holds repo-relative paths only
# Each pattern is joined at run time, so this file does not match itself.
LOCAL = re.compile("|".join(["/" + w + "/" for w in ("Us" + "ers", "ho" + "me", "pri" + "vate", "t" + "mp")]
                            + ["scratch" + "pad", re.escape(os.path.expanduser("~")),
                               re.escape(getpass.getuser())]), re.I)
bad = []
for d, _, fs in os.walk(HERE):
    for f in fs:
        if LOCAL.search(open(os.path.join(d, f), encoding="utf-8", errors="replace").read()):
            bad.append(os.path.join(d, f))
check("no file in the write folder names a home folder, a temp or working folder, or a user name", not bad)

failed = [k for k, v in checks.items() if not v]
out = {"before_state": "git HEAD 93040c51: the model as committed",
       "page_count": len(model_pages), "pages": pages, "new_folder_files": new_files, "spine": spine,
       "entries": entries, "ice_entries": ice_entries, "spine_text": spine_text, "bi_8": bi_8,
       "git_status_product": status, "structure_check": structure,
       "write_folder_files_naming_local_paths": bad, "failed_checks": failed, "checks_run": len(checks),
       "checks_passed": len(checks) - len(failed), "all_checks_pass": not failed, "checks": checks}
with open(f"{HERE}/verify.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
    f.write("\n")
print(json.dumps({"failed": failed, "run": len(checks), "structure": {k: structure[k] for k in ("before", "after")},
                  "new_warnings": structure["new_warnings"]}, indent=1))
