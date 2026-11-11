"""Check the three new, not-built features of Track execution in the team's tracker (BI-9, capability 3).

Run from the repo root. Reads only the three drafts, their sources (files in the repo, memory through
the memory tool, GitHub issues through `gh issue view`, read only) and the settings. Writes
new-features-lint.json, new-features-quotes.json, new-features-ice.json, new-features-page.json,
new-features-not-decided.json and new-features-paths.json beside this file. Prints a summary.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(HERE)
DRAFTS = os.path.join(BASE, "drafts/product-os/software-delivery-planning/track-execution")
FEATURES = ["fn-one-tool-knows-tracker", "fn-link-work-across-trackers", "fn-say-what-each-type-means"]
LINT = ".claude/skills/discover-capabilities/scripts/lint_grounding.py"
MEMORY = ".garura/core/tools/memory/memory.py"
THIN = "Thin: proposed from the person's words; deepen with `/discover-capabilities`."
READ_OPENING = ("Gather it from the memory layer. Look first at the project's existing memory and its existing "
                "implementation, then Garura memory, then Phoenix memory. If none of them answers, research it "
                "and raise a memory update for a person to approve. For this part, look for: ")
LEAN_WORDS = ["lean", "leans", "likely", "probably", "should", "prefer", "preferred", "recommend", "recommended",
              "best", "better", "simplest", "ideally", "suggest", "suggested", "default", "we think", "the way to go",
              "most fitting", "obvious"]
PATH_RE = re.compile(r"(\.garura/[^\s:,]+|core/[^\s:,]+|docs/[^\s:,]+)")
_cache = {}


def norm(s):
    s = s.replace("`", "").replace("**", "")
    return re.sub(r"\s+", " ", s).strip()


def run(cmd):
    out = subprocess.run(cmd, capture_output=True, text=True)
    return out.returncode, out.stdout


def gh_issue(n):
    code, out = run(["gh", "issue", "view", str(n), "--json", "title,body,comments",
                     "-q", '.title + "\n" + .body + "\n" + ([.comments[].body] | join("\n"))'])
    return out if code == 0 else None


def memory_read(tier, path):
    code, out = run(["python3", MEMORY, "read", "--issue", "1021", "--tier", tier, "--path", path])
    try:
        d = json.loads(out)
    except ValueError:
        return None
    return d.get("text") if d.get("ok") else None


def read_ref(ref):
    if ref in _cache:
        return _cache[ref]
    kind, val = ref
    if kind == "gh":
        text = gh_issue(val)
    elif kind in ("short-term", "phoenix"):
        text = memory_read(kind, val)
    elif kind == "dir":
        text = "" if os.path.isdir(val) else None
    else:
        try:
            with open(val, encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            text = None
    _cache[ref] = text
    return text


def refs_of(line):
    """The source a Sources line names."""
    if line.startswith("- GitHub "):
        return [("gh", int(n[1:])) for n in re.findall(r"#\d+", line.split(":")[0])]
    m = re.match(r"- (1021/context/answers/\S+), in short-term memory", line)
    if m:
        return [("short-term", m.group(1).rstrip(","))]
    m = re.match(r"- ((?:standards|knowledge)/\S+), in Phoenix memory", line)
    if m:
        p = m.group(1).rstrip(",")
        return [("dir", None)] if p.endswith("/") else [("phoenix", p)]
    m = PATH_RE.search(line)
    if m:
        p = m.group(1).rstrip(".,")
        return [("dir", p)] if p.endswith("/") else [("file", p)]
    return []


def section(lines, head):
    out, on = [], False
    for l in lines:
        if l.startswith("## "):
            on = l == head
            continue
        if on:
            out.append(l)
    return out


def main():
    root_ok = os.path.isfile(LINT) and os.path.isfile(MEMORY)
    if not root_ok:
        print("run from the repo root")
        return 2
    pages = {f: {"feature": os.path.join(DRAFTS, f, "feature.md"), "ice": os.path.join(DRAFTS, f, "ice.md")}
             for f in FEATURES}
    text = {}
    for f, p in pages.items():
        for k, path in p.items():
            with open(path, encoding="utf-8") as fh:
                text[(f, k)] = fh.read()

    # 1. structure check
    lint = []
    for f in FEATURES:
        code, out = run(["python3", LINT, "--kind", "feature", "--stage", "detailed", "--doc", pages[f]["feature"]])
        res = json.loads(out)
        lint.append({"doc": pages[f]["feature"], "args": ["--kind", "feature", "--stage", "detailed"],
                     "ok": res.get("ok"), "errors": res.get("errors"), "warnings": res.get("warnings")})
    with open(os.path.join(HERE, "new-features-lint.json"), "w", encoding="utf-8") as fh:
        json.dump({"checked_on": "2026-11-10", "tool": LINT, "results": lint}, fh, indent=2)
        fh.write("\n")

    # 2. quotes
    results, problems, unreadable = [], [], []
    for f in FEATURES:
        flines = text[(f, "feature")].split("\n")
        srcs = [(l, refs_of(l)) for l in section(flines, "## Sources") if l.startswith("- ")]
        all_refs = sorted({r for _, rs in srcs for r in rs if r[0] != "dir"}, key=str)
        for r in all_refs:
            if read_ref(r) is None:
                unreadable.append({"feature": f, "source": list(r)})
        for kind in ("feature", "ice"):
            in_sources = False
            for i, line in enumerate(text[(f, kind)].split("\n"), 1):
                if line.startswith("## "):
                    in_sources = line == "## Sources"
                    continue
                for q in re.findall(r'"([^"]+)"', line):
                    nq = norm(q)
                    if in_sources:
                        look = [r for r in refs_of(line) if r[0] != "dir"]
                        where = "sources line %d" % i
                    else:
                        look = all_refs
                        where = "text line %d" % i
                    found = [list(r) for r in look if read_ref(r) and nq in norm(read_ref(r))]
                    rec = {"page": pages[f][kind], "where": where, "quote": q,
                           "status": "found" if found else "not found", "in": found}
                    results.append(rec)
                    if not found:
                        problems.append(rec)
    with open(os.path.join(HERE, "new-features-quotes.json"), "w", encoding="utf-8") as fh:
        json.dump({"how": "each quote in a Sources line is looked for word for word in that line's own source: "
                          "a repo file, a GitHub issue (gh issue view: title, body and comments), or memory read "
                          "through the memory tool; each quote in the page text, or in its ICE, in any source the "
                          "feature page lists; whitespace and backticks are ignored",
                   "total": len(results), "not_found": len(problems), "unreadable_sources": unreadable,
                   "problems": problems, "results": results}, fh, indent=2)
        fh.write("\n")

    # 3. ICE shape
    ice = []
    for f in FEATURES:
        t = text[(f, "ice")]
        lines = t.split("\n")
        heads = [l for l in lines if l.startswith("## ")]

        def count(prefix):
            return sum(1 for l in lines if l.startswith("- " + prefix))
        read = [l for l in lines if l.startswith("- Read: ")]
        done = [l for l in lines if l.startswith("- Done means: ")]
        flines = text[(f, "feature")].split("\n")
        rec = {"page": pages[f]["ice"],
               "thin_first_line": lines[0] == THIN, "blank_after_thin": len(lines) > 1 and lines[1] == "",
               "sections": heads, "goal": count("Goal: "), "limit": count("Limit: "), "fails_if": count("Fails if: "),
               "read": len(read),
               "read_opening_exact": bool(read) and read[0][len("- Read: "):].startswith(READ_OPENING)
               and len(read[0]) > len("- Read: ") + len(READ_OPENING) + 20,
               "never_read": count("Never read: "), "persona": count("Persona: "), "scope": count("Scope: "),
               "scenario": count("Scenario: "), "done_means": len(done),
               "done_by_other": bool(done) and done[0].startswith("- Done means: Someone other than"),
               "feature_page_has_no_ice_section": not any(l.startswith("## Agent intent") or l in
                                                          ("## Intent", "## Context", "## Expectation")
                                                          for l in flines)}
        bad = []
        if not rec["thin_first_line"]:
            bad.append("first line is not the Thin line")
        if not rec["blank_after_thin"]:
            bad.append("no blank line after the Thin line")
        if heads != ["## Intent", "## Context", "## Expectation"]:
            bad.append("sections are not Intent, Context, Expectation in order")
        for k in ("goal", "read", "never_read", "persona", "scope", "scenario", "done_means"):
            if rec[k] != 1:
                bad.append(f"{k}: {rec[k]}, not 1")
        for k in ("limit", "fails_if"):
            if not 1 <= rec[k] <= 3:
                bad.append(f"{k}: {rec[k]}, not 1 to 3")
        for k in ("read_opening_exact", "done_by_other", "feature_page_has_no_ice_section"):
            if not rec[k]:
                bad.append(f"{k} is false")
        rec["problems"] = bad
        ice.append(rec)
    with open(os.path.join(HERE, "new-features-ice.json"), "w", encoding="utf-8") as fh:
        json.dump({"results": ice, "problems": sum(len(r["problems"]) for r in ice)}, fh, indent=2)
        fh.write("\n")

    # 4. the page's own parts
    page = []
    for f in FEATURES:
        lines = text[(f, "feature")].split("\n")
        what = section(lines, "## What it does")
        ex_i = next((i for i, l in enumerate(what) if l.startswith("- Examples")), None)
        examples = 0
        if ex_i is not None:
            for l in what[ex_i + 1:]:
                if l.startswith("  - "):
                    examples += 1
                elif l.startswith("- ") or not l.strip():
                    break
        status = [l for l in what if l.startswith("Status:")]
        ac = [l for l in section(lines, "## Acceptance criteria") if l.startswith("- ")]
        rules = [l for l in section(lines, "## Rules & behavior") if l.startswith("- ")]
        rec = {"page": pages[f]["feature"], "examples": examples,
               "how_it_meets": any(l.startswith("- How it meets the capability:") for l in what),
               "status_not_built": bool(status) and status[0].startswith("Status: not built"),
               "status_issue_numbers": re.findall(r"#\d+", " ".join(what[what.index(status[0]):]) if status else ""),
               "acceptance": len(ac),
               "acceptance_not_built_marked": all(l.endswith("This is not built.") for l in ac),
               "acceptance_given_when_then": all(re.match(r"- Given .+, when .+, then .+", l) for l in ac),
               "rules_without_reason": [l[:80] for l in rules
                                        if not l.startswith("- Not decided:") and "The reason" not in l],
               "rule_reasons_quoted": all('"' in l for l in rules
                                          if not l.startswith("- Not decided:") and "The reason" in l),
               "out_of_scope": len([l for l in section(lines, "## Out of scope") if l.startswith("- ")]),
               "sources": len([l for l in section(lines, "## Sources") if l.startswith("- ")])}
        bad = []
        if rec["examples"] < 3:
            bad.append("fewer than three examples")
        for k in ("how_it_meets", "status_not_built", "acceptance_not_built_marked", "acceptance_given_when_then",
                  "rule_reasons_quoted"):
            if not rec[k]:
                bad.append(f"{k} is false")
        if rec["rules_without_reason"]:
            bad.append("a rule with no reason")
        rec["problems"] = bad
        page.append(rec)
    with open(os.path.join(HERE, "new-features-page.json"), "w", encoding="utf-8") as fh:
        json.dump({"results": page, "problems": sum(len(r["problems"]) for r in page)}, fh, indent=2)
        fh.write("\n")

    # 5. Not decided lines hold no lean
    nd = []
    for f in FEATURES:
        for kind in ("feature", "ice"):
            for i, line in enumerate(text[(f, kind)].split("\n"), 1):
                if "Not decided:" not in line:
                    continue
                body = re.sub(r'"[^"]*"', '""', line)  # a quoted source's words are not the page's lean
                hits = [w for w in LEAN_WORDS if re.search(r"\b" + re.escape(w) + r"\b", body, re.I)]
                nd.append({"page": pages[f][kind], "line": i, "text": line.strip(), "lean_words": hits})
    with open(os.path.join(HERE, "new-features-not-decided.json"), "w", encoding="utf-8") as fh:
        json.dump({"words_looked_for": LEAN_WORDS, "lines": nd,
                   "with_a_lean": sum(1 for r in nd if r["lean_words"])}, fh, indent=2)
        fh.write("\n")

    # 6. personal paths, the settings' owner values, and the git user's name
    owners = []
    with open("core/config.yaml", encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"\s*#?\s*owner:\s*(\S+)", line)
            if m and m.group(1) not in ("your-org", "your-group"):
                owners.append(m.group(1).strip("\"'"))
    name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.split()
    banned = [r"/Users/", r"/home/", r"~/", r"/tmp\b", r"/private/", r"/var/folders", r"[A-Z]:\\"]
    hits = []
    for (f, kind), t in text.items():
        for i, line in enumerate(t.split("\n"), 1):
            for pat in banned:
                if re.search(pat, line):
                    hits.append({"page": pages[f][kind], "line": i, "what": "a home-folder or temp path"})
            for o in owners:
                if o and o in line:
                    hits.append({"page": pages[f][kind], "line": i, "what": "an owner value from the settings"})
            for w in name:
                if len(w) > 2 and re.search(r"\b" + re.escape(w) + r"\b", line):
                    hits.append({"page": pages[f][kind], "line": i, "what": "a word of the git user's name"})
    with open(os.path.join(HERE, "new-features-paths.json"), "w", encoding="utf-8") as fh:
        json.dump({"checked": sorted(p for d in pages.values() for p in d.values()),
                   "owner_values_checked": len(owners), "git_name_words_checked": len(name), "hits": hits},
                  fh, indent=2)
        fh.write("\n")

    summary = {"lint_ok": all(r["ok"] for r in lint), "quotes": len(results), "quotes_not_found": len(problems),
               "unreadable_sources": len(unreadable), "ice_problems": sum(len(r["problems"]) for r in ice),
               "page_problems": sum(len(r["problems"]) for r in page),
               "not_decided_lines": len(nd), "not_decided_with_lean": sum(1 for r in nd if r["lean_words"]),
               "path_owner_name_hits": len(hits)}
    print(json.dumps(summary))
    ok = (summary["lint_ok"] and not problems and not unreadable and not summary["ice_problems"]
          and not summary["page_problems"] and not summary["not_decided_with_lean"] and not hits)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
