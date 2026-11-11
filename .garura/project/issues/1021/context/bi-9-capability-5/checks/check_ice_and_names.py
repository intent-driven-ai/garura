#!/usr/bin/env python3
"""Check each draft ICE page's shape, each feature page's parts, every Not decided line, and every draft for
personal paths and names.

Run from the repository root:
    python3 -B <run>/checks/check_ice_and_names.py <run>
Writes <run>/checks/ice-shape.json, <run>/checks/pages.json, <run>/checks/not-decided.json and
<run>/checks/names.json. Exit 1 on any problem.
"""
import json, os, re, sys

run = sys.argv[1]
cap = os.path.join(run, "drafts", "product-os", "software-delivery-planning", "give-every-gate-a-way-past")
THIN = "Thin: proposed from the person's words; deepen with `/discover-capabilities`."
READ = ("Gather it from the memory layer. Look first at the project's existing memory and its existing "
        "implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and "
        "raise a memory update for a person to approve. For this part, look for: ")

def sections(text, level="## "):
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith(level) and not line.startswith(level + "#"):
            cur = line[len(level):].strip(); out[cur] = []
        elif cur is not None and line.strip():
            out[cur].append(line)
    return out

def pages():
    for dirpath, _, files in sorted(os.walk(cap)):
        for fn in sorted(files):
            yield os.path.join(dirpath, fn)

# 1. ICE pages
ice_results = []
for dirpath, _, files in sorted(os.walk(cap)):
    if "ice.md" not in files:
        continue
    page = os.path.join(dirpath, "ice.md")
    is_cap = dirpath == cap
    part = os.path.join(dirpath, "capability.md" if is_cap else "feature.md")
    text = open(page, encoding="utf-8").read()
    lines = text.splitlines()
    sec = sections(text)
    heads = [l for l in lines if l.startswith("## ")]
    count = lambda s, label: sum(1 for l in sec.get(s, []) if l.startswith(f"- {label}:"))
    read = [l for l in sec.get("Context", []) if l.startswith("- Read:")]
    done = [l for l in sec.get("Expectation", []) if l.startswith("- Done means:")]
    part_text = open(part, encoding="utf-8").read() if os.path.exists(part) else ""
    r = {"page": page, "part_page": part, "kind": "capability" if is_cap else "feature",
         "first_line_thin": lines[0] == THIN if lines else False,
         "blank_after_thin": len(lines) > 1 and lines[1] == "",
         "sections": heads,
         "goal": count("Intent", "Goal"), "limit": count("Intent", "Limit"), "fails_if": count("Intent", "Fails if"),
         "read_fixed": bool(read) and read[0].startswith("- Read: " + READ),
         "never_read": count("Context", "Never read"), "persona": count("Context", "Persona"),
         "scope": count("Context", "Scope"), "scenario": count("Expectation", "Scenario"),
         "done_means": len(done), "done_by_other": bool(done) and done[0].startswith("- Done means: Someone other than"),
         "part_page_exists": bool(part_text),
         "part_page_has_ice_section": bool(re.search(r"^## (Agent intent|Intent|Context|Expectation)", part_text, re.M))}
    p = []
    if not r["first_line_thin"]: p.append("the first line is not the exact Thin line")
    if not r["blank_after_thin"]: p.append("no blank line after the Thin line")
    if heads != ["## Intent", "## Context", "## Expectation"]: p.append("sections are not Intent, Context, Expectation")
    if r["goal"] != 1: p.append("not exactly one Goal")
    if not 1 <= r["limit"] <= 3: p.append("Limits are not 1 to 3")
    if not 1 <= r["fails_if"] <= 3: p.append("Fails if lines are not 1 to 3")
    if not r["read_fixed"]: p.append("the Read line does not start with the fixed opening")
    for k in ("never_read", "persona", "scope", "scenario", "done_means"):
        if r[k] != 1: p.append(f"{k} is not exactly one line")
    if not r["done_by_other"]: p.append("Done means is not checked by someone other than the doer")
    if not r["part_page_exists"]: p.append("no part page beside the ICE")
    if r["part_page_has_ice_section"]: p.append("the part's page holds an ICE section")
    r["problems"] = p
    ice_results.append(r)

# 2. Feature pages: the parts the brief asks for
page_results = []
for fn in sorted(os.listdir(cap)):
    page = os.path.join(cap, fn, "feature.md")
    if not os.path.exists(page):
        continue
    text = open(page, encoding="utf-8").read()
    sec = sections(text)
    what = sec.get("What it does", [])
    ex_i = next((i for i, l in enumerate(what) if l.startswith("- Examples, in different kinds of project:")), None)
    examples = []
    if ex_i is not None:
        for l in what[ex_i + 1:]:
            if l.startswith("  - "): examples.append(l)
            elif not l.startswith("    "): break
    status = [l for l in what if l.startswith("Status: ")]
    rules = [l for l in sec.get("Rules & behavior", []) if l.startswith("- ")]
    acc = [l for l in sec.get("Acceptance criteria", []) if l.startswith("- ")]
    oos = [l for l in sec.get("Out of scope", []) if l.startswith("- ")]
    r = {"page": page,
         "headings": [l for l in text.splitlines() if l.startswith("## ")],
         "examples": len(examples),
         "how_it_meets": any(l.startswith("- How it meets the capability:") for l in what),
         "status": status[0] if status else None,
         "rules": len(rules),
         "rules_without_reason": [l for l in rules if not l.startswith("- Not decided:") and "The reason" not in l],
         "acceptance": len(acc),
         "acceptance_not_given_when_then": [l for l in acc if not re.match(r"^- Given .+, when .+, then .+", l)],
         "acceptance_not_marked": [l for l in acc if not l.rstrip().endswith("This is not built.")],
         "out_of_scope": len(oos),
         "out_of_scope_without_owner": [l for l in oos if not re.search(r"\b(owns?|does it|covers them|covers it)\b", l)]}
    p = []
    if r["headings"] != ["## What it does", "## Inputs / Outputs", "## Rules & behavior", "## Acceptance criteria", "## Out of scope", "## Sources"]:
        p.append("headings are not the feature contract plus Sources")
    if r["examples"] < 3: p.append("fewer than three examples")
    if not r["how_it_meets"]: p.append("no 'How it meets the capability'")
    if not r["status"] or not r["status"].startswith("Status: not built (#"): p.append("no Status line 'not built' with its issues")
    if r["rules_without_reason"]: p.append("a rule has no quoted reason")
    if r["acceptance_not_given_when_then"]: p.append("an acceptance line is not Given/When/Then")
    if r["acceptance_not_marked"]: p.append("an acceptance line is not marked 'This is not built.'")
    if r["out_of_scope_without_owner"]: p.append("an Out of scope line names no owner")
    r["problems"] = p
    page_results.append(r)

# 3. Not decided lines: none may lean
LEAN = re.compile(r"\b(lean|leans|leaning|likely|probably|should|ought|recommend\w*|prefer\w*|better|best|"
                  r"suggest\w*|propos\w*|favou?r\w*|default|we think|for now|most|research)\b", re.I)
nd = []
for page in pages():
    for n, line in enumerate(open(page, encoding="utf-8"), 1):
        if "Not decided:" in line:
            hits = sorted(set(m.group(0).lower() for m in LEAN.finditer(line)))
            nd.append({"file": page, "line": n, "text": line.strip(), "lean_words": hits})
nd_problems = [x for x in nd if x["lean_words"]]

# 4. Personal paths and names
PERSONAL = [("home folder", re.compile(r"/Users/|/home/|~/")),
            ("temp folder", re.compile(r"/tmp\b|/private/|/var/folders")),
            ("user name", re.compile("|".join(["ka"+"pil","ahu"+"ja","vi"+"ren"]), re.I)),
            ("a pronoun for a person", re.compile(r"\b(he|his|him|she|her|hers)\b", re.I))]
hits, checked = [], 0
for page in pages():
    checked += 1
    for n, line in enumerate(open(page, encoding="utf-8"), 1):
        for name, rx in PERSONAL:
            if rx.search(line):
                hits.append({"file": page, "line": n, "check": name, "text": line.strip()[:160]})

listed = sorted(set(re.findall(r"\((fn-[a-z0-9-]+)\):", open(os.path.join(cap, "capability.md"), encoding="utf-8").read())))
drafted = sorted(d for d in os.listdir(cap) if d.startswith("fn-") and os.path.exists(os.path.join(cap, d, "feature.md")))
names = {"checked_on": "2026-11-10", "files_checked": checked, "checks": [n for n, _ in PERSONAL], "hits": hits,
         "capability_feature_list": listed, "drafted_features": drafted,
         "listed_with_no_page": sorted(set(listed) - set(drafted)),
         "drafted_not_listed": sorted(set(drafted) - set(listed))}

json.dump({"checked_on": "2026-11-10", "results": ice_results}, open(os.path.join(run, "checks", "ice-shape.json"), "w"), indent=2)
json.dump({"checked_on": "2026-11-10", "results": page_results}, open(os.path.join(run, "checks", "pages.json"), "w"), indent=2)
json.dump({"checked_on": "2026-11-10", "lean_words_checked": LEAN.pattern, "lines": nd, "with_a_lean": nd_problems},
          open(os.path.join(run, "checks", "not-decided.json"), "w"), indent=2)
json.dump(names, open(os.path.join(run, "checks", "names.json"), "w"), indent=2)
for r in ice_results:
    print("ICE", os.path.relpath(r["page"], cap), "limit", r["limit"], "fails_if", r["fails_if"],
          "thin", r["first_line_thin"], "read_fixed", r["read_fixed"], "problems", r["problems"])
for r in page_results:
    print("PAGE", os.path.relpath(r["page"], cap), "examples", r["examples"], "rules", r["rules"],
          "acceptance", r["acceptance"], "out_of_scope", r["out_of_scope"], "problems", r["problems"])
print("NOT DECIDED lines", len(nd), "with a lean", len(nd_problems))
for x in nd_problems: print("  ", os.path.relpath(x["file"], cap), x["line"], x["lean_words"])
print(json.dumps({k: names[k] for k in ("files_checked", "hits", "listed_with_no_page", "drafted_not_listed")}, indent=2))
bad = hits or nd_problems or names["drafted_not_listed"] or names["listed_with_no_page"] \
      or any(r["problems"] for r in ice_results) or any(r["problems"] for r in page_results)
sys.exit(1 if bad else 0)
