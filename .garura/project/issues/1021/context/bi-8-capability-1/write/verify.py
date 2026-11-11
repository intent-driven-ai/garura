"""Verify the write of Ship every change the same way (BI-8) and the merge of cap-721 into it.

Run from the repo root after the write. Reads the model, the drafts, the requests and reports in
this folder, and the model as committed at HEAD (git show). Writes verify.json in this folder.
"""
import difflib
import json
import os
import re
import subprocess

import yaml

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
ISSUE = ".garura/project/issues/1021/context/bi-8-capability-1"
DRAFTS = f"{ISSUE}/drafts/product-os"
MODEL = ".garura/product/product-os"
C = "software-delivery-planning/ship-every-change"
ORDER = ["fn-731", "fn-commit-by-concern", "fn-raise-change", "fn-673", "fn-land-plan-with-evidence",
         "fn-land-several-issues", "fn-scan-every-push", "fn-keep-docs-in-step"]
OLD = {"fn-731", "fn-673"}
NEW_FEATURES = [f for f in ORDER if f not in OLD]
THIN_FEATURES = {"fn-land-plan-with-evidence", "fn-land-several-issues", "fn-scan-every-push", "fn-keep-docs-in-step"}
THIN = re.compile(r"^\s*(?:>\s*)?\**Thin(?: ICE)?\**\s*:", re.I)
CAP721 = re.compile(r"(?<![\w-])cap-721(?![\w-])")

checks = {}


def check(name, ok):
    checks[name] = bool(ok)
    return ok


def git_show(path):
    return subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, check=True).stdout


def folder(fn):
    return f"features/{fn}" if fn in OLD else f"{C}/{fn}"


def ice_id(fn):
    return "ice-" + fn[3:]


def rb(path):
    with open(path, "rb") as f:
        return f.read()


# ---- 1. pages
pages = {}
model_pages = [f"{C}/capability.md", f"{C}/ice.md"]
for fn in ORDER:
    model_pages += [f"{folder(fn)}/feature.md", f"{folder(fn)}/ice.md"]
for p in model_pages:
    page, draft = rb(f"{MODEL}/{p}"), rb(f"{DRAFTS}/{p}")
    text = page.decode("utf-8")
    lines = text.split("\n")
    thin_lines = [i for i, l in enumerate(lines) if THIN.match(l)]
    info = {"equals_draft": page == draft, "bytes": len(page), "thin_lines_on_page": len(thin_lines),
            "ice_section_on_page": "## Agent intent (ICE)" in lines}
    check(f"page {p} equals draft byte for byte", page == draft)
    check(f"page {p} holds no ICE section", not info["ice_section_on_page"])
    fn = p.split("/")[-2]
    if p.endswith("/ice.md") and fn in THIN_FEATURES:
        copy = rb(f"{HERE}/approved/{fn}/ice.md")
        info.update({"thin_line_first": thin_lines == [0], "blank_after_thin_line": lines[1] == "",
                     "equals_copy_with_thin_line_back": page.split(b"\n", 2)[2] == copy,
                     "copy_has_no_thin_line": not any(THIN.match(l) for l in copy.decode().split("\n"))})
        check(f"{fn}/ice.md: one Thin line, first, blank after, rest = approved copy",
              thin_lines == [0] and lines[1] == "" and info["equals_copy_with_thin_line_back"]
              and info["copy_has_no_thin_line"])
    else:
        check(f"page {p} carries no Thin line", not thin_lines)
    pages[p] = info

new_files = sorted(os.path.relpath(os.path.join(d, f), MODEL)
                   for d, _, fs in os.walk(f"{MODEL}/{C}") for f in fs)
expect_new = sorted(p for p in model_pages if p.startswith(C + "/"))
check("new folder holds only the 14 pages", new_files == expect_new and len(new_files) == 14)
for fn in OLD:
    check(f"{fn} folder holds only feature.md and ice.md",
          sorted(os.listdir(f"{MODEL}/features/{fn}")) == ["feature.md", "ice.md"])

# ---- 2. fn-725
f725 = f"{MODEL}/features/fn-725/feature.md"
before_725 = git_show(f725).decode("utf-8").split("\n")
after_725 = open(f725, encoding="utf-8").read().split("\n")
req725 = json.load(open(f"{HERE}/lines-request-fn-725.json"))["pages"][0]["changes"][0]
changed_725 = [{"line": i + 1, "old": a, "new": b} for i, (a, b) in enumerate(zip(before_725, after_725)) if a != b]
approvals = open(f"{ISSUE}/page-approvals.md", encoding="utf-8").read()
check("fn-725's page changed in line 54 only, to the approved words",
      len(before_725) == len(after_725) and len(changed_725) == 1 and changed_725[0]["line"] == 54
      and changed_725[0]["old"] == req725["old"] and changed_725[0]["new"] == req725["new"])
check("fn-725's old and new line are the words in the approvals record",
      f'from "{req725["old"]}" to "{req725["new"]}"' in approvals)

# ---- 3. index
spine_path = f"{MODEL}/_spine.yaml"
before_text = git_show(spine_path).decode("utf-8")
after_text = open(spine_path, encoding="utf-8").read()
before, after = yaml.safe_load(before_text), yaml.safe_load(after_text)
LISTS = ["domains", "capabilities", "features", "slices", "ices"]


def by_id(s, k):
    return {e["id"]: e for e in (s.get(k) or [])}


asked_new = {"capabilities": ["cap-ship-every-change"], "features": NEW_FEATURES,
             "ices": ["ice-ship-every-change"] + [ice_id(f) for f in ORDER], "domains": [], "slices": []}
asked_removed = {"capabilities": ["cap-721"]}
asked_changed = {"features": ["fn-731", "fn-673"]}
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
    check(f"spine {k}: new entries are exactly the ones asked", new == asked_new.get(k, []))
    check(f"spine {k}: only the asked entries removed", removed == asked_removed.get(k, []))
    check(f"spine {k}: of the old entries only the asked ones changed", changed == asked_changed.get(k, []))
    check(f"spine {k}: order of the kept entries kept", kept_order)
check("every new id was unused before the write",
      not ({i for v in asked_new.values() for i in v} & all_before_ids))
check("spine: other top keys unchanged",
      all(before[k] == after[k] for k in before if k not in LISTS))
check("spine: top key order kept", list(before) == list(after))

cap_page = open(f"{MODEL}/{C}/capability.md", encoding="utf-8").read().split("\n")
di = cap_page.index("## Directional intent")
cap_one_line = cap_page[di + 1]
items = {}
for l in cap_page:
    m = re.match(r"^- (.+?) \((fn-[a-z0-9-]+)\): (.+)$", l)
    if m:
        items[m.group(2)] = m.group(3)
check("feature list order on the capability page = the eight features in order", list(items) == ORDER)


def cap1(t):
    return t[0].upper() + t[1:]


caps, feats, ices = by_id(after, "capabilities"), by_id(after, "features"), by_id(after, "ices")
entries = {}
c = caps["cap-ship-every-change"]
entries["cap-ship-every-change"] = c
check("capability cap-ship-every-change as asked",
      c["slug"] == "ship-every-change" and c["domain"] == "dom-software-delivery-planning"
      and c["intents"] == ["bi-8"] and c["doc"] == f"{C}/capability.md" and c["status"] == "proposed"
      and not (c.get("metadata") or {}).get("thin"))
check("capability one_line = first line of its Directional intent, word for word", c["one_line"] == cap_one_line)
check("cap-ship-every-change's intents are [bi-8] only", c["intents"] == ["bi-8"])
for fn in NEW_FEATURES:
    e = feats[fn]
    entries[fn] = e
    check(f"feature {fn} as asked",
          e["slug"] == fn and e["capability"] == "cap-ship-every-change" and e["intents"] == ["bi-8"]
          and e["doc"] == f"{C}/{fn}/feature.md" and e["status"] == "proposed"
          and not (e.get("metadata") or {}).get("thin"))
    check(f"{fn} one_line = its feature-list text, first letter capitalised", e["one_line"] == cap1(items[fn]))
old_entries = {}
bf = by_id(before, "features")
for fn in sorted(OLD):
    a, b = feats[fn], bf[fn]
    entries[fn] = a
    keys = sorted(set(a) | set(b))
    changed_keys = [k for k in keys if a.get(k) != b.get(k)]
    meta_b, meta_a = b.get("metadata") or {}, a.get("metadata") or {}
    old_entries[fn] = {"changed_keys": changed_keys, "capability_before": b["capability"],
                       "capability_after": a["capability"], "intents_before": b["intents"],
                       "intents_after": a["intents"], "one_line_before": b["one_line"],
                       "one_line_after": a["one_line"], "metadata_before": meta_b, "metadata_after": meta_a,
                       "issue": a.get("issue"), "depends_on": a.get("depends_on")}
    check(f"feature {fn} under cap-ship-every-change, intents [bi-8], its new one-line",
          a["capability"] == "cap-ship-every-change" and a["intents"] == ["bi-8"]
          and a["one_line"] == cap1(items[fn]))
    check(f"feature {fn}: every other field kept (metadata.updated_by aside, which link_part.py sets on an update)",
          set(changed_keys) <= {"capability", "intents", "one_line", "metadata"}
          and {k: v for k, v in meta_a.items() if k != "updated_by"} == {k: v for k, v in meta_b.items() if k != "updated_by"}
          and not meta_a.get("thin"))
ice_entries = {}
expect_ices = [("ice-ship-every-change", "cap-ship-every-change", "capability", f"{C}/ice.md")] + \
    [(ice_id(fn), fn, "feature", f"{folder(fn)}/ice.md") for fn in ORDER]
for iid, part, kind, doc in expect_ices:
    e = ices[iid]
    thin = bool((e.get("metadata") or {}).get("thin"))
    want_thin = part in THIN_FEATURES
    ice_entries[iid] = {"for": e["for"], "for_kind": e["for_kind"], "doc": e["doc"], "thin": thin,
                        "doc_leads_to_file": os.path.isfile(f"{MODEL}/{e['doc']}")}
    check(f"ICE {iid} as asked", e["for"] == part and e["for_kind"] == kind and e["doc"] == doc
          and thin == want_thin and ice_entries[iid]["doc_leads_to_file"])
    check(f"ICE {iid}: the only ICE for {part}", [x["id"] for x in after["ices"] if x["for"] == part] == [iid])
    page_thin = any(THIN.match(l) for l in open(f"{MODEL}/{doc}", encoding="utf-8").read().split("\n"))
    check(f"ICE {iid}: thin mark on entry and page agree", page_thin == thin)
check("only the four named ICE are thin among the nine",
      sorted(i for i, v in ice_entries.items() if v["thin"]) == sorted(ice_id(f) for f in THIN_FEATURES))
check("no part of this write is thin itself",
      not any((e.get("metadata") or {}).get("thin") for e in entries.values()))

# cap-721
def names_721(obj):
    if isinstance(obj, dict):
        return any(names_721(k) or names_721(v) for k, v in obj.items())
    if isinstance(obj, list):
        return any(names_721(v) for v in obj)
    return isinstance(obj, str) and bool(CAP721.search(obj))


check("cap-721 gone from the spine's data", not names_721(after))
check("cap-721's page and folder gone", not os.path.exists(f"{MODEL}/capabilities/cap-721"))
mentions = []
for d, _, fs in os.walk(".garura/product"):
    for f in fs:
        p = os.path.join(d, f)
        try:
            for n, line in enumerate(open(p, encoding="utf-8").read().split("\n"), 1):
                if CAP721.search(line):
                    mentions.append(f"{p}:{n}")
        except UnicodeDecodeError:
            pass
check("no file in the model names cap-721 (pages, ICE pages and the spine's text)", not mentions)
check("no feature is under cap-721", not any(e.get("capability") == "cap-721" for e in after["features"]))
check("nothing in the spine was identified by or depends on cap-721 before the merge",
      not any(e.get("identified_by") == "cap-721" or "cap-721" in (e.get("depends_on") or [])
              for k in LISTS for e in (before.get(k) or []) if e["id"] != "cap-721"))
remove_report = json.load(open(f"{HERE}/remove-report.json"))
merge = {k: remove_report[k] for k in ("repointed", "merged", "moved_features", "needs_to_review", "deleted")}
merge["cap_721_before"] = by_id(before, "capabilities")["cap-721"]
check("merge report: cap-721 into cap-ship-every-change, fn-731 and fn-673 moved, nothing to review",
      remove_report["merged"] == [{"id": "cap-721", "into": "cap-ship-every-change"}]
      and sorted(remove_report["moved_features"]) == ["fn-673", "fn-731"] and remove_report["needs_to_review"] == [])

# ---- 4. spine text
removed_lines, added_lines = [], []
for l in difflib.ndiff(before_text.split("\n"), after_text.split("\n")):
    if l.startswith("- "):
        removed_lines.append(l[2:])
    elif l.startswith("+ "):
        added_lines.append(l[2:])
cap_721_block = []
bl = before_text.split("\n")
s0 = bl.index("- id: cap-721")
for l in bl[s0:]:
    if l != "- id: cap-721" and l.startswith("- id: "):
        break
    cap_721_block.append(l)
allowed = list(cap_721_block)
for fn in sorted(OLD):
    allowed += ["  capability: cap-721", "  - bi-717"]
allowed += ["  one_line: start-change cuts a plan's branch, and each issue's branch from it",
            "  one_line: merge-change lands an issue on its plan branch, and a plan on main whenever",
            "    it pauses",
            "    updated_by: 'product-os-keeper (#779, review finding DM-1 of PR #1010)'"]
left = list(allowed)
unexplained = []
for l in removed_lines:
    if l in left:
        left.remove(l)
    else:
        unexplained.append(l)
spine_text = {"lines_removed_or_replaced": len(removed_lines), "removed_or_replaced": removed_lines,
              "lines_added": len(added_lines), "unexplained_removed_lines": unexplained,
              "comment_lines_before": sum(1 for l in before_text.split("\n") if l.lstrip().startswith("#")),
              "comment_lines_after": sum(1 for l in after_text.split("\n") if l.lstrip().startswith("#"))}
check("spine only gained lines, apart from the lines the merge and the two one-line updates replace or remove",
      not unexplained)
check("spine comments kept", spine_text["comment_lines_before"] == spine_text["comment_lines_after"])

# ---- 5. BI-8
bi8 = f"{MODEL}/intents/bi-8.md"
b8 = git_show(bi8).decode("utf-8").split("\n")
a8 = open(bi8, encoding="utf-8").read().split("\n")
ops = [op for op in difflib.SequenceMatcher(a=b8, b=a8, autojunk=False).get_opcodes() if op[0] != "equal"]
inserted = a8[ops[0][3]:ops[0][4]] if ops else []
draft = json.load(open(f"{HERE}/intent-draft.json"))
want_block = ["**Touches:**"] + [f"- [{t['title']}]({t['link']}) ({t['kind']}) — {t['mark']}" for t in draft["touches"]] + [""]
links, titles = {}, {}
for t in draft["touches"]:
    target = os.path.normpath(os.path.join(MODEL, "intents", t["link"]))
    links[t["link"]] = os.path.isfile(target)
    head = open(target, encoding="utf-8").readline().rstrip("\n") if links[t["link"]] else ""
    titles[t["link"]] = head.split(": ", 1)[1] == t["title"] if ": " in head else False
touch_docs = [os.path.relpath(os.path.normpath(os.path.join(MODEL, "intents", t["link"])), MODEL) for t in draft["touches"]]
naming_bi8_before = [e["id"] for k in LISTS for e in (before.get(k) or []) if "bi-8" in (e.get("intents") or [])]
naming_bi8 = [(e["id"], e["doc"]) for k in LISTS for e in (after.get(k) or []) if "bi-8" in (e.get("intents") or [])]
expect_order = ["cap-ship-every-change"] + ORDER
bi_8 = {"lines_before": len(b8), "lines_after": len(a8),
        "only_insertions": all(op[0] == "insert" for op in ops), "insert_blocks": len(ops),
        "lines_added": len(inserted), "added": inserted,
        "added_as_asked_in_order": inserted == want_block,
        "line_before_block": a8[ops[0][3] - 1] if ops else None,
        "line_two_before_block": a8[ops[0][3] - 2] if ops else None,
        "line_after_block": a8[ops[0][4]] if ops else None,
        "stage_line": next(l for l in a8 if l.startswith("**Stage:**")),
        "stage_line_unchanged": next(l for l in a8 if l.startswith("**Stage:**")) == next(l for l in b8 if l.startswith("**Stage:**")),
        "touches_lines": len(draft["touches"]), "links": links, "titles_match_page_titles": titles,
        "index_entries_naming_bi_8_before": naming_bi8_before,
        "index_entries_naming_bi_8": [i for i, _ in naming_bi8]}
check("BI-8's page gained only the Touches block, in one place, as asked",
      bi_8["only_insertions"] and len(ops) == 1 and inserted == want_block
      and bi_8["line_two_before_block"] == "**Tracker:** #8" and bi_8["line_after_block"] == "**What was done:** (nothing yet)")
check("BI-8's page: every other line byte for byte",
      open(bi8, "rb").read() == git_show(bi8).replace(b"\n**What was done:**", ("\n" + "\n".join(want_block) + "\n**What was done:**").encode("utf-8"), 1))
check("BI-8's stage line keeps its person and date", bi_8["stage_line_unchanged"]
      and bi_8["stage_line"] == "**Stage:** confirmed — by the product owner, 2026-11-02")
check("BI-8's Touches: 9 lines", len(draft["touches"]) == 9)
check("BI-8's Touches: each link leads to a file", all(links.values()))
check("BI-8's Touches: each title is its page's title", all(titles.values()))
check("BI-8's Touches: marks as asked (seven adds; fn-731 and fn-673 changes)",
      [t["mark"] for t in draft["touches"]] == ["adds", "changes", "adds", "adds", "changes", "adds", "adds", "adds", "adds"])
check("BI-8's Touches form matches BI-7's page",
      all(re.match(r"^- \[[^\]]+\]\(\.\./[^)\s]+\) \((capability|feature)\) — (adds|changes)$", l) for l in want_block[1:-1])
      and any(re.match(r"^- \[[^\]]+\]\(\.\./[^)\s]+\) \((capability|feature)\) — (adds|changes)$", l)
              for l in open(f"{MODEL}/intents/bi-7.md", encoding="utf-8").read().split("\n")))
check("the 9 index entries that name bi-8 match the 9 Touches lines one for one",
      len(naming_bi8) == 9 and sorted(i for i, _ in naming_bi8) == sorted(expect_order)
      and sorted(d for _, d in naming_bi8) == sorted(touch_docs) and len(set(touch_docs)) == 9)

# ---- 6. what changed under .garura/product/
status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", ".garura/product/"],
                        capture_output=True, text=True, check=True).stdout.rstrip("\n").split("\n")
allowed_paths = {f"{MODEL}/_spine.yaml", f"{MODEL}/intents/bi-8.md", f"{MODEL}/features/fn-725/feature.md",
                 f"{MODEL}/capabilities/cap-721/capability.md"}
ok_status = True
for s in status:
    p = s[3:]
    if not (p in allowed_paths or p.startswith(f"{MODEL}/{C}/") or p.startswith(f"{MODEL}/features/fn-731/")
            or p.startswith(f"{MODEL}/features/fn-673/")):
        ok_status = False
check("under .garura/product/ only the spine, bi-8.md, fn-725's page, the fn-731 and fn-673 folders, "
      "the cap-721 folder and the new folder changed", ok_status)

# ---- 7. structure check
def load(name):
    return json.load(open(f"{HERE}/{name}"))


lb, la = load("lint-before.json"), load("lint-after.json")
structure = {"command": "python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py --root .garura/product/product-os --spine .garura/product/product-os/_spine.yaml",
             "before": {"errors": len(lb["errors"]), "warnings": len(lb["warnings"]), "counts": lb["counts"],
                        "file": f"{HERE}/lint-before.json"},
             "after": {"errors": len(la["errors"]), "warnings": len(la["warnings"]), "counts": la["counts"],
                       "file": f"{HERE}/lint-after.json"},
             "new_errors": [e for e in la["errors"] if e not in lb["errors"]],
             "errors_gone": [e for e in lb["errors"] if e not in la["errors"]],
             "new_warnings": [w for w in la["warnings"] if w not in lb["warnings"]],
             "warnings_gone": [w for w in lb["warnings"] if w not in la["warnings"]]}
check("structure check: no new error", not structure["new_errors"])

# ---- 8. this folder holds repo-relative paths only
import getpass  # noqa: E402
# Each pattern is joined at run time, so this file does not match itself.
LOCAL = re.compile("|".join(["/" + w + "/" for w in ("Us" + "ers", "ho" + "me", "pri" + "vate", "t" + "mp")]
                            + ["scratch" + "pad", re.escape(os.path.expanduser("~")),
                               re.escape(getpass.getuser())]), re.I)
bad = []
for d, _, fs in os.walk(HERE):
    for f in fs:
        t = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
        if LOCAL.search(t):
            bad.append(os.path.join(d, f))
check("no file in the write folder names a home folder, a temp or working folder, or a user name", not bad)

failed = [k for k, v in checks.items() if not v]
out = {"status": "done: steps 1 to 5 written, each skill on its first run" if not failed else "checks failed",
       "before_state": "git HEAD 65cb83fc: the model as committed (no uncommitted model change before this write)",
       "steps": [
           {"step": "lint-before", "file": f"{HERE}/lint-before.json"},
           {"step": "1 pages", "skill": "enrich-grounding (write_approved.py)", "exit": 0, "report": f"{HERE}/approved-report.json"},
           {"step": "2 fn-725 line", "skill": "enrich-grounding (change_lines.py)", "exit": 0, "report": f"{HERE}/lines-report-fn-725.json"},
           {"step": "3 index", "skill": "link-model-part (link_part.py)", "exit": 0, "report": f"{HERE}/link-report.json"},
           {"step": "4 check before the merge", "file": f"{HERE}/cap-721-mentions-before-merge.json", "pages_naming_cap_721": []},
           {"step": "4 merge", "skill": "remove-model-part (remove_part.py)", "exit": 0, "report": f"{HERE}/remove-report.json"},
           {"step": "5 BI-8 Touches block", "skill": "author-intent-page (write_page.py --rewrite, stage confirmed by the product owner, 2026-11-02)", "exit": 0, "report": f"{HERE}/intent-page.json"},
           {"step": "lint-after", "file": f"{HERE}/lint-after.json"}],
       "page_count": len(model_pages), "pages": pages, "new_folder_files": new_files,
       "fn_725_changed_lines": changed_725, "spine": spine, "entries": entries, "old_entries": old_entries,
       "ice_entries": ice_entries, "merge": merge, "model_lines_naming_cap_721": mentions,
       "spine_text": spine_text, "bi_8": bi_8, "git_status_product": status, "structure_check": structure,
       "write_folder_files_naming_local_paths": bad,
       "failed_checks": failed, "checks_run": len(checks), "checks_passed": len(checks) - len(failed),
       "all_checks_pass": not failed, "checks": checks}
with open(f"{HERE}/verify.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
    f.write("\n")
print(json.dumps({"failed": failed, "run": len(checks)}, indent=1))
