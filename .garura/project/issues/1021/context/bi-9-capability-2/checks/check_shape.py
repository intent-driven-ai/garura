#!/usr/bin/env python3
"""Check the ICE pages and the page rules of the Run plays as loops drafts.

ICE pages: the three parts in order (Intent, Context, Expectation); exactly one Goal, at least one
Limit and one Fails if; the Read line with the exact opening, Never read, Persona and Scope; a
Scenario and a Done means checked by someone other than the doer; no Thin line (none is thin).
Part pages: no ICE section on the page. Feature pages: What it does, Status, examples from at least
three kinds of project, How it meets the capability, Inputs / Outputs, each rule with its quoted
reason (or a Not decided line), Given/When/Then criteria, Out of scope naming an owner, Sources.
Every page: no home-folder or temp path, no real name, and the word for a loop only, never the
old word, outside a quote or a file name. Run from the repository root; writes checks/ice-shape.json
and checks/page-rules.json. Exit 0 when nothing is wrong, 1 otherwise.
"""
import glob, json, os, re, sys, datetime

RUN = ".garura/project/issues/1021/context/bi-9-capability-2"
DRAFTS = f"{RUN}/drafts/product-os/software-delivery-planning/run-plays-as-loops"
READ = ("Gather it from the memory layer. Look first at the project's existing memory and its existing "
        "implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and "
        "raise a memory update for a person to approve. For this part, look for: ")
PERSONAL = [r"/Users/", r"~/", r"/home/", r"/tmp\b", r"/private/", r"/var/folders", r"[A-Z]:\\\\", r"mktemp",
            r"\b(" + "|".join(["Ka" + "pil", "Ahu" + "ja", "Vi" + "ren" + "ahu" + "ja"]) + r")\b", "ka" + "pil" + "vi" + "ren" + "ahu" + "ja", "naga" + "rro"]


def sections(text):
    out, cur = [], None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = [line[3:].strip(), []]
            out.append(cur)
        elif cur is not None:
            cur[1].append(line)
    return out


def check_ice(page):
    text = open(page, encoding="utf-8").read()
    secs = sections(text)
    names = [s[0] for s in secs]
    body = {s[0]: [l for l in s[1] if l.startswith("- ")] for s in secs}
    count = lambda sec, label: sum(1 for l in body.get(sec, []) if l.startswith(f"- {label}:"))
    read = [l for l in body.get("Context", []) if l.startswith("- Read: ")]
    done = [l for l in body.get("Expectation", []) if l.startswith("- Done means:")]
    part = os.path.join(os.path.dirname(page), "capability.md" if os.path.dirname(page) == DRAFTS else "feature.md")
    part_secs = [s[0] for s in sections(open(part, encoding="utf-8").read())]
    r = {"page": page, "thin": bool(re.search(r"(?mi)^\s*(> )?\**thin\b", text)),
         "sections": names, "goal": count("Intent", "Goal"), "limit": count("Intent", "Limit"),
         "fails_if": count("Intent", "Fails if"), "read_fixed": bool(read) and read[0][len("- Read: "):].startswith(READ),
         "read_names_what": bool(read) and len(read[0]) > len("- Read: ") + len(READ) + 20,
         "never_read": count("Context", "Never read"), "persona": count("Context", "Persona"),
         "scope": count("Context", "Scope"), "scenario": count("Expectation", "Scenario"),
         "done_means": len(done), "done_by_other": bool(done) and "Someone other than" in done[0],
         "part_page_has_no_ice_section": not any(n in ("Agent intent (ICE)", "Intent", "Context", "Expectation") for n in part_secs)}
    p = []
    if names != ["Intent", "Context", "Expectation"]: p.append("the three parts are not there in order")
    if r["goal"] != 1: p.append("not exactly one Goal")
    if r["limit"] < 1: p.append("no Limit")
    if r["fails_if"] < 1: p.append("no Fails if")
    for k in ("read_fixed", "read_names_what", "done_by_other", "part_page_has_no_ice_section"):
        if not r[k]: p.append(f"{k} is false")
    for k in ("never_read", "persona", "scope", "scenario", "done_means"):
        if r[k] != 1: p.append(f"{k}: {r[k]}, not 1")
    if r["thin"]: p.append("marked thin")
    r["problems"] = p
    return r


def outside_quotes(line):
    line = re.sub(r'"[^"]*"', '""', line)
    return " ".join(t for t in line.split() if "/" not in t and not re.search(r"\.(md|py|yaml|json)\b", t))


def check_page(page):
    text = open(page, encoding="utf-8").read()
    p, notes = [], {}
    for n, line in enumerate(text.splitlines(), 1):
        for pat in PERSONAL:
            if re.search(pat, line, re.I if pat.startswith(r"\b") or ("naga" + "rro") in pat else 0):
                p.append(f"line {n}: names a personal path or name ({pat})")
        if re.search(r"\bdriv(e|es|ing)\b", outside_quotes(line), re.I):
            p.append(f"line {n}: uses the old word outside a quote or a file name")
    nd = [l.strip() for l in text.splitlines() if l.strip().startswith("- Not decided:")]
    for l in nd:
        if re.search(r"\b(lean|we suggest|likely|probably|should|recommend)\b", l, re.I):
            p.append(f"a Not decided line carries a lean: {l}")
    notes["not_decided"] = nd
    if page.endswith("/feature.md"):
        secs = {s[0]: s[1] for s in sections(text)}
        what = "\n".join(secs.get("What it does", []))
        ex = re.search(r"(?ms)^- Examples, in different kinds of project:\n((?:  - .*\n)+)", what + "\n")
        n_ex = len(re.findall(r"(?m)^  - ", ex.group(1))) if ex else 0
        notes["examples"] = n_ex
        if n_ex < 3: p.append("fewer than three examples")
        kinds = re.findall(r"(?m)^  - In an? ([^,]+),", ex.group(1)) if ex else []
        notes["example_kinds"] = kinds
        if len(set(kinds)) < 3: p.append("examples do not come from three different kinds of project")
        if "- How it meets the capability:" not in what: p.append("no How it meets the capability line")
        if not re.search(r"(?m)^Status: ", what): p.append("no Status line")
        elif not re.search(r"(?m)^Status: (built|not built)", what): p.append("the Status line does not say built or not")
        rules = [l for l in secs.get("Rules & behavior", []) if l.startswith("- ")]
        for l in rules:
            if not (l.startswith("- Not decided:") or re.search(r'The reason[^:]*: .*"', l)):
                p.append(f"a rule has no quoted reason: {l[:70]}")
        crit = [l for l in secs.get("Acceptance criteria", []) if l.startswith("- ")]
        for l in crit:
            if not re.match(r"- Given .*, when .*, then ", l): p.append(f"a criterion is not Given/When/Then: {l[:70]}")
        oos = [l for l in secs.get("Out of scope", []) if l.startswith("- ")]
        for l in oos:
            if not re.search(r"\b(owns?|own them|does it|do it|does them|records it|lays it)\b|\(fn-", l):
                p.append(f"an Out of scope line names no owner: {l[:70]}")
        if "Sources" not in secs: p.append("no Sources section")
        notes["rules"], notes["criteria"], notes["out_of_scope"] = len(rules), len(crit), len(oos)
    return {"page": page, "problems": p, **notes}


def main():
    ices = [check_ice(p) for p in sorted(glob.glob(f"{DRAFTS}/**/ice.md", recursive=True))]
    pages = [check_page(p) for p in sorted(glob.glob(f"{DRAFTS}/**/*.md", recursive=True))]
    today = datetime.date.today().isoformat()
    json.dump({"checked_on": today, "results": ices}, open(f"{RUN}/checks/ice-shape.json", "w"), indent=2)
    json.dump({"checked_on": today, "results": pages}, open(f"{RUN}/checks/page-rules.json", "w"), indent=2)
    bad = [r for r in ices + pages if r["problems"]]
    print(json.dumps({"ice_pages": len(ices), "pages": len(pages), "with_problems": len(bad)}))
    for r in bad:
        print(" -", os.path.relpath(r["page"], DRAFTS), r["problems"])
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
