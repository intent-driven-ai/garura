#!/usr/bin/env python3
"""Check each draft ICE page's shape, and every draft for personal paths and names.

Run from the repository root:
    python3 -B <run>/checks/check_ice_and_names.py <run>
Writes <run>/checks/ice-shape.json and <run>/checks/names.json.
"""
import json, os, re, sys

run = sys.argv[1]
cap = os.path.join(run, "drafts", "product-os", "software-delivery-planning", "manage-adrs")
READ = ("Gather it from the memory layer. Look first at the project's existing memory and its existing "
        "implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and "
        "raise a memory update for a person to approve. For this part, look for: ")

def sections(text):
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip(); out[cur] = []
        elif cur is not None and line.strip():
            out[cur].append(line)
    return out

ice_results = []
for dirpath, _, files in os.walk(cap):
    if "ice.md" not in files:
        continue
    page = os.path.join(dirpath, "ice.md")
    part = os.path.join(dirpath, "capability.md" if dirpath == cap else "feature.md")
    text = open(page, encoding="utf-8").read()
    sec = sections(text)
    heads = [l for l in text.splitlines() if l.startswith("## ")]
    count = lambda s, label: sum(1 for l in sec.get(s, []) if l.startswith(f"- {label}:"))
    read = [l for l in sec.get("Context", []) if l.startswith("- Read:")]
    done = [l for l in sec.get("Expectation", []) if l.startswith("- Done means:")]
    part_text = open(part, encoding="utf-8").read() if os.path.exists(part) else ""
    status = re.search(r"^Status: ([^.,]+)", part_text, re.M)
    r = {"page": page, "part_page": part,
         "part_status": status.group(1) if status else ("capability" if dirpath == cap else None),
         "sections": heads, "thin": bool(re.search(r"^Thin:", text, re.M)),
         "goal": count("Intent", "Goal"), "limit": count("Intent", "Limit"), "fails_if": count("Intent", "Fails if"),
         "read_fixed": bool(read) and read[0].startswith("- Read: " + READ),
         "never_read": count("Context", "Never read"), "persona": count("Context", "Persona"),
         "scope": count("Context", "Scope"), "scenario": count("Expectation", "Scenario"),
         "done_means": len(done), "done_by_other": bool(done) and "Someone other than" in done[0],
         "part_page_has_ice_section": "## Agent intent (ICE)" in part_text}
    p = []
    if heads != ["## Intent", "## Context", "## Expectation"]: p.append("sections are not Intent, Context, Expectation")
    if r["thin"]: p.append("marked thin")
    if r["goal"] != 1: p.append("not exactly one Goal")
    if r["limit"] < 1: p.append("no Limit")
    if r["fails_if"] < 1: p.append("no Fails if")
    if not r["read_fixed"]: p.append("Read line does not start with the fixed opening")
    for k in ("never_read", "persona", "scope", "scenario", "done_means"):
        if r[k] != 1: p.append(f"{k} is not exactly one line")
    if not r["done_by_other"]: p.append("Done means is not checked by someone other than the doer")
    if r["part_page_has_ice_section"]: p.append("the part's page holds an ICE section")
    r["problems"] = p
    ice_results.append(r)

PERSONAL = [("home folder", re.compile(r"/Users/|/home/|~/")),
            ("temp folder", re.compile(r"/tmp\b|/private/|/var/folders")),
            ("user name", re.compile("|".join(["ka"+"pil","ahu"+"ja","vi"+"ren"]), re.I)),
            ("a pronoun for a person", re.compile(r"\b(he|his|him|she|her|hers)\b", re.I))]
hits, checked = [], 0
for dirpath, _, files in os.walk(cap):
    for fn in sorted(files):
        p = os.path.join(dirpath, fn); checked += 1
        for n, line in enumerate(open(p, encoding="utf-8"), 1):
            for name, rx in PERSONAL:
                if rx.search(line):
                    hits.append({"file": p, "line": n, "check": name, "text": line.strip()[:160]})

listed = sorted(set(re.findall(r"\((fn-[a-z0-9-]+)\):", open(os.path.join(cap, "capability.md"), encoding="utf-8").read())))
drafted = sorted(d for d in os.listdir(cap) if d.startswith("fn-") and os.path.exists(os.path.join(cap, d, "feature.md")))
names = {"checked_on": "2026-11-10", "files_checked": checked,
         "checks": [n for n, _ in PERSONAL], "hits": hits,
         "capability_feature_list": listed, "drafted_features": drafted,
         "listed_with_no_page": sorted(set(listed) - set(drafted)),
         "drafted_not_listed": sorted(set(drafted) - set(listed))}
json.dump({"checked_on": "2026-11-10", "results": ice_results}, open(os.path.join(run, "checks", "ice-shape.json"), "w"), indent=2)
json.dump(names, open(os.path.join(run, "checks", "names.json"), "w"), indent=2)
for r in ice_results:
    print(os.path.relpath(r["page"], cap), r["part_status"], "goal", r["goal"], "limit", r["limit"], "fails_if", r["fails_if"],
          "read_fixed", r["read_fixed"], "done_by_other", r["done_by_other"], "thin", r["thin"], "problems", r["problems"])
print(json.dumps({k: names[k] for k in ("files_checked", "hits", "listed_with_no_page", "drafted_not_listed")}, indent=2))
sys.exit(1 if hits or any(r["problems"] for r in ice_results) or names["drafted_not_listed"] else 0)
