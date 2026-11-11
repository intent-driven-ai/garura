#!/usr/bin/env python3
"""Check one BI-10 capability's drafts against the page and ICE rules of the product model.

Usage, from the repository root:
    python3 .garura/project/issues/1021/context/bi-10-drafting/check_drafts.py <run folder>

<run folder> is a capability's working folder, such as
.garura/project/issues/1021/context/bi-10-capability-1. Its drafts are under drafts/product-os/.
Writes <run folder>/checks/drafts-check.json. Exit 0 when nothing is wrong, 1 otherwise.

ICE pages (ice.md): Intent, Context, Expectation in order; exactly one Goal, at least one Limit and
one Fails if; the Read line with the fixed opening and what to look for; one Never read, Persona,
Scope, Scenario and Done means, checked by someone other than the doer. A thin ICE starts with the
Thin line and a blank line, and holds at most three Limits and three Fails if lines.
Capability pages: Directional intent, Benefit hypothesis, Boundary (In / Out / Never), Guiding rules
and Sources, and no ICE section. Feature pages: What it does with a Status line, examples from three
kinds of project and How it meets the capability; Inputs / Outputs; each rule with a quoted reason
or a Not decided line; Given/When/Then criteria; Out of scope naming an owner; Sources; no ICE section.
Every page: no home or temp path, no real name, no old word for a loop outside a quote or file name,
and no lean in a Not decided line.
"""
import glob, json, os, re, sys, datetime

READ = ("Gather it from the memory layer. Look first at the project's existing memory and its existing "
        "implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and "
        "raise a memory update for a person to approve. For this part, look for: ")
THIN = "Thin: proposed from the person's words; deepen with `/discover-capabilities`."
PERSONAL = [r"/Us" + r"ers/", r"~/", r"/home/", r"/tmp\b", r"/private/", r"/var/folders", r"[A-Z]:\\\\", r"mktemp",
            r"\b(" + "|".join(["Ka" + "pil", "Ahu" + "ja", "Vi" + "ren"]) + r")\b",
            "ka" + "pil" + "vi" + "ren", "naga" + "rro"]
ICE_HEADS = ("Agent intent (ICE)", "Intent", "Context", "Expectation")


def sections(text, level="## "):
    out, cur = [], None
    for line in text.splitlines():
        if line.startswith(level) and not line.startswith(level + "#"):
            cur = [line[len(level):].strip(), []]
            out.append(cur)
        elif cur is not None:
            cur[1].append(line)
    return out


def check_ice(page):
    text = open(page, encoding="utf-8").read()
    lines = text.split("\n")
    thin = lines[0].strip() == THIN
    secs = sections(text)
    names = [s[0] for s in secs]
    body = {s[0]: [l for l in s[1] if l.startswith("- ")] for s in secs}
    count = lambda sec, label: sum(1 for l in body.get(sec, []) if l.startswith(f"- {label}:"))
    read = [l for l in body.get("Context", []) if l.startswith("- Read: ")]
    done = [l for l in body.get("Expectation", []) if l.startswith("- Done means:")]
    p = []
    if names != ["Intent", "Context", "Expectation"]:
        p.append("the three parts are not there in order")
    if count("Intent", "Goal") != 1:
        p.append("not exactly one Goal")
    lim, fails = count("Intent", "Limit"), count("Intent", "Fails if")
    if lim < 1:
        p.append("no Limit")
    if fails < 1:
        p.append("no Fails if")
    if thin:
        if len(lines) < 2 or lines[1] != "":
            p.append("the Thin line is not followed by a blank line")
        if lim > 3 or fails > 3:
            p.append(f"a thin ICE holds {lim} Limits and {fails} Fails if lines; at most three of each")
    if sum(1 for l in lines if l.strip().startswith("Thin:")) > (1 if thin else 0):
        p.append("a Thin line that is not the first line")
    if not (read and read[0][len("- Read: "):].startswith(READ) and len(read[0]) > len("- Read: ") + len(READ) + 20):
        p.append("the Read line does not have the fixed opening and what to look for")
    for label, sec in (("Never read", "Context"), ("Persona", "Context"), ("Scope", "Context"),
                       ("Scenario", "Expectation"), ("Done means", "Expectation")):
        if count(sec, label) != 1:
            p.append(f"{label}: {count(sec, label)}, not 1")
    if not (done and "Someone other than" in done[0]):
        p.append("Done means is not checked by someone other than the doer")
    return {"page": page, "thin": thin, "limits": lim, "fails_if": fails, "problems": p}


def outside_quotes(line):
    line = re.sub(r'"[^"]*"', '""', line)
    return " ".join(t for t in line.split() if "/" not in t and not re.search(r"\.(md|py|yaml|json)\b", t))


def check_page(page):
    text = open(page, encoding="utf-8").read()
    p, notes = [], {}
    for n, line in enumerate(text.splitlines(), 1):
        for pat in PERSONAL:
            if re.search(pat, line, re.I):
                p.append(f"line {n}: names a personal path or name ({pat})")
        if re.search(r"\bdriv(e|es|ing)\b", outside_quotes(line), re.I):
            p.append(f"line {n}: uses the old word for a loop outside a quote or a file name")
    nd = [l.strip() for l in text.splitlines() if l.strip().startswith("- Not decided:")]
    for l in nd:
        if re.search(r"\b(lean|we suggest|likely|probably|should|recommend)\b", l, re.I):
            p.append(f"a Not decided line carries a lean: {l[:80]}")
    notes["not_decided"] = len(nd)
    if page.endswith("/ice.md"):
        return {"page": page, "problems": p, **notes}
    heads = [s[0] for s in sections(text)]
    if any(h in ICE_HEADS for h in heads):
        p.append("the page holds an ICE section; the ICE has its own page")
    if page.endswith("/capability.md"):
        if not text.startswith("# Capability: "):
            p.append("the title is not '# Capability: ...'")
        for h in ("Directional intent", "Sources"):
            if h not in heads:
                p.append(f"no '## {h}' section")
        subs = [s[0] for s in sections(text, "### ")]
        for h in ("Benefit hypothesis", "Boundary (In / Out / Never)", "Guiding rules"):
            if h not in subs:
                p.append(f"no '### {h}' section")
        di = "\n".join(dict((s[0], s[1]) for s in sections(text)).get("Directional intent", []))
        feats = re.findall(r"(?m)^- .+ \((fn-[a-z0-9-]+)\): ", di)
        notes["features_listed"] = feats
        if not feats:
            p.append("the Directional intent lists no feature as '- Title (fn-id): ...'")
    elif page.endswith("/feature.md"):
        if not text.startswith("# Feature: "):
            p.append("the title is not '# Feature: ...'")
        secs = {s[0]: s[1] for s in sections(text)}
        what = "\n".join(secs.get("What it does", []))
        ex = re.search(r"(?ms)^- Examples, in different kinds of project:\n((?:  - .*\n)+)", what + "\n")
        kinds = re.findall(r"(?m)^  - In an? ([^,]+),", ex.group(1)) if ex else []
        notes["example_kinds"] = kinds
        if len(set(kinds)) < 3:
            p.append("examples do not come from three different kinds of project")
        if "- How it meets the capability:" not in what:
            p.append("no How it meets the capability line")
        if not re.search(r"(?m)^Status: (built|not built)", what):
            p.append("no Status line that says built or not built")
        for h in ("Inputs / Outputs", "Rules & behavior", "Acceptance criteria", "Out of scope", "Sources"):
            if h not in secs:
                p.append(f"no '## {h}' section")
        for l in [l for l in secs.get("Rules & behavior", []) if l.startswith("- ")]:
            if not (l.startswith("- Not decided:") or re.search(r'The reason[^:]*: .*"', l)):
                p.append(f"a rule has no quoted reason: {l[:70]}")
        for l in [l for l in secs.get("Acceptance criteria", []) if l.startswith("- ")]:
            if not re.match(r"- Given .*, when .*, then ", l):
                p.append(f"a criterion is not Given/When/Then: {l[:70]}")
        for l in [l for l in secs.get("Out of scope", []) if l.startswith("- ")]:
            if not re.search(r"\b(owns?|own them|does it|do it|does them|records it|lays it)\b|\(fn-", l):
                p.append(f"an Out of scope line names no owner: {l[:70]}")
    return {"page": page, "problems": p, **notes}


def main():
    run = sys.argv[1].rstrip("/")
    drafts = f"{run}/drafts/product-os"
    pages = sorted(glob.glob(f"{drafts}/**/*.md", recursive=True))
    ices = [check_ice(x) for x in pages if x.endswith("/ice.md")]
    rules = [check_page(x) for x in pages]
    # every part page has its ice.md beside it, and nothing else is in a part's folder
    pairs = []
    for x in pages:
        if x.endswith(("/capability.md", "/feature.md")):
            if not os.path.isfile(os.path.join(os.path.dirname(x), "ice.md")):
                pairs.append(f"{x}: no ice.md beside it")
    os.makedirs(f"{run}/checks", exist_ok=True)
    out = {"checked_on": datetime.date.today().isoformat(), "pages": len(pages), "ice": ices,
           "rules": rules, "missing_ice": pairs}
    json.dump(out, open(f"{run}/checks/drafts-check.json", "w"), indent=2)
    bad = [r for r in ices + rules if r["problems"]]
    print(json.dumps({"pages": len(pages), "ice_pages": len(ices), "thin_ice": sum(1 for r in ices if r["thin"]),
                      "with_problems": len(bad), "missing_ice": len(pairs)}))
    for r in bad:
        print(" -", os.path.relpath(r["page"], drafts), r["problems"])
    for m in pairs:
        print(" -", m)
    return 0 if not bad and not pairs else 1


if __name__ == "__main__":
    sys.exit(main())
