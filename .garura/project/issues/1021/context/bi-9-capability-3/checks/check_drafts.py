"""Check the drafts of Track execution in the team's tracker (BI-9, capability 3).

Run from the repo root. Reads only the drafts, their sources (files, the memory copies in this
folder, and GitHub issues through `gh issue view`, read only) and the settings. Writes
quotes.json, ice-shape.json and paths.json beside this file.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(HERE)
DRAFTS = os.path.join(BASE, "drafts/product-os/software-delivery-planning/track-execution")
MEMORY = os.path.join(BASE, "memory")
READ_OPENING = ("Gather it from the memory layer. Look first at the project's existing memory and its existing "
                "implementation, then Garura memory, then Phoenix memory. If none of them answers, research it "
                "and raise a memory update for a person to approve. For this part, look for: ")
PATH_RE = re.compile(r"(\.garura/[^\s:,]+|core/[^\s:,]+|docs/[^\s:,]+|standards/[^\s:,]+)")
_gh = {}


def norm(s):
    s = s.replace("`", "").replace("**", "")
    s = re.sub(r"^\s*>\s?", " ", s, flags=re.M)
    return re.sub(r"\s+", " ", s).strip()


def gh_issue(n):
    if n not in _gh:
        out = subprocess.run(["gh", "issue", "view", str(n), "--json", "title,body", "-q", '.title + "\n" + .body'],
                             capture_output=True, text=True)
        _gh[n] = out.stdout if out.returncode == 0 else None
    return _gh[n]


def read_source(ref):
    if ref.startswith("#"):
        return gh_issue(int(ref[1:]))
    path = ref
    if ref.startswith("standards/"):
        path = os.path.join(MEMORY, ref)
    if os.path.isdir(path):
        return ""
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def quotes(line):
    return re.findall(r'"([^"]+)"', line)


def pages():
    out = []
    for d, _, fs in os.walk(DRAFTS):
        for f in sorted(fs):
            if f.endswith(".md"):
                out.append(os.path.join(d, f))
    return sorted(out)


def sources_of(page_text):
    lines = page_text.split("\n")
    if "## Sources" not in lines:
        return []
    out = []
    for line in lines[lines.index("## Sources") + 1:]:
        if not line.startswith("- "):
            continue
        refs = []
        if line.startswith("- GitHub "):
            refs = re.findall(r"#\d+", line.split(":")[0])
        else:
            m = re.search(r"\bin (\.garura/[^\s:,]+)", line)
            if m and line.startswith("- The product owner"):
                refs = [m.group(1)]
            else:
                m = PATH_RE.search(line)
                if m:
                    refs = [m.group(1).rstrip(".")]
        out.append((line, refs))
    return out


def main():
    results, problems, example_words = [], [], []
    texts = {p: open(p, encoding="utf-8").read() for p in pages()}
    src_cache = {}

    def src(ref):
        if ref not in src_cache:
            src_cache[ref] = read_source(ref)
        return src_cache[ref]

    for page, text in texts.items():
        part_page = page
        if page.endswith("/ice.md"):
            d = os.path.dirname(page)
            part_page = os.path.join(d, "capability.md" if os.path.basename(d) == "track-execution" else "feature.md")
        srcs = sources_of(texts[part_page])
        all_refs = sorted({r for _, refs in srcs for r in refs})
        for r in all_refs:
            if src(r) is None:
                problems.append({"page": page, "source": r, "problem": "source cannot be read"})
        lines = text.split("\n")
        in_sources = False
        for i, line in enumerate(lines, 1):
            if line == "## Sources":
                in_sources = True
                continue
            for q in quotes(line):
                nq = norm(q)
                if in_sources:
                    refs = next((refs for l, refs in srcs if l == line), [])
                    look = refs or all_refs
                    where = "sources line %d" % i
                else:
                    look = all_refs
                    where = "text line %d" % i
                found = [r for r in look if src(r) and nq in norm(src(r))]
                status = "found" if found else "not found"
                rec = {"page": page, "where": where, "quote": q, "status": status, "in": found}
                results.append(rec)
                if not found:
                    problems.append(rec)
    with open(os.path.join(HERE, "quotes.json"), "w", encoding="utf-8") as fh:
        json.dump({"how": "each quote in a Sources line is looked for in that line's own file, issue (gh issue view: "
                          "title and body) or memory copy; each quote in the page text in any source its page lists "
                          "(for an ICE page, its part's page); whitespace, backticks and bold marks are ignored",
                   "total": len(results), "not_found": len(problems), "problems": problems,
                   "results": results}, fh, indent=2)
        fh.write("\n")

    # ICE shape
    ice = []
    for page, text in texts.items():
        if not page.endswith("/ice.md"):
            continue
        lines = text.split("\n")
        d = os.path.dirname(page)
        part_page = os.path.join(d, "capability.md" if os.path.basename(d) == "track-execution" else "feature.md")
        part_lines = texts[part_page].split("\n")
        heads = [l for l in lines if l.startswith("## ")]
        def count(prefix):
            return sum(1 for l in lines if l.startswith("- " + prefix))
        read = [l for l in lines if l.startswith("- Read: ")]
        done = [l for l in lines if l.startswith("- Done means: ")]
        rec = {"page": page, "sections": heads,
               "goal": count("Goal: "), "limit": count("Limit: "), "fails_if": count("Fails if: "),
               "read_fixed": bool(read) and read[0][len("- Read: "):].startswith(READ_OPENING)
               and len(read[0]) > len("- Read: ") + len(READ_OPENING) + 20,
               "read": len(read), "never_read": count("Never read: "), "persona": count("Persona: "),
               "scope": count("Scope: "), "scenario": count("Scenario: "), "done_means": len(done),
               "done_by_other": bool(done) and done[0].startswith("- Done means: Someone other than"),
               "thin": any(re.match(r"^\s*(?:>\s*)?\**Thin(?: ICE)?\**\s*:", l, re.I) for l in lines),
               "part_page_has_no_ice_section": not any(l.startswith("## Agent intent") or l == "## Intent"
                                                       for l in part_lines)}
        bad = []
        if heads != ["## Intent", "## Context", "## Expectation"]:
            bad.append("sections are not Intent, Context, Expectation in order")
        for k, want in (("goal", 1), ("read", 1), ("never_read", 1), ("persona", 1), ("scope", 1),
                        ("scenario", 1), ("done_means", 1)):
            if rec[k] != want:
                bad.append(f"{k}: {rec[k]}, not {want}")
        for k in ("limit", "fails_if"):
            if rec[k] < 1:
                bad.append(f"no {k}")
        for k in ("read_fixed", "done_by_other", "part_page_has_no_ice_section"):
            if not rec[k]:
                bad.append(f"{k} is false")
        if rec["thin"]:
            bad.append("a Thin line, on a part whose ICE must not be thin")
        rec["problems"] = bad
        ice.append(rec)
    with open(os.path.join(HERE, "ice-shape.json"), "w", encoding="utf-8") as fh:
        json.dump({"results": ice, "problems": sum(len(r["problems"]) for r in ice)}, fh, indent=2)
        fh.write("\n")

    # personal paths, the code-host owner value, and the git user's name
    owner = None
    with open("core/config.yaml", encoding="utf-8") as fh:
        block = False
        for line in fh:
            if re.match(r"^github:\s*$", line):
                block = True
                continue
            if block and re.match(r"^\S", line):
                break
            m = re.match(r"\s+owner:\s*(\S+)", line) if block else None
            if m:
                owner = m.group(1)
    name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.split()
    banned = [r"/Users/", r"/home/", r"~/", r"/tmp\b", r"/private/", r"/var/folders", r"[A-Z]:\\\\"]
    hits = []
    for page, text in texts.items():
        for i, line in enumerate(text.split("\n"), 1):
            for pat in banned:
                if re.search(pat, line):
                    hits.append({"page": page, "line": i, "what": "a home-folder or temp path"})
            if owner and owner in line:
                hits.append({"page": page, "line": i, "what": "the value of github.owner"})
            for w in name:
                if len(w) > 2 and re.search(r"\b" + re.escape(w) + r"\b", line):
                    hits.append({"page": page, "line": i, "what": "a word of the git user's name"})
    with open(os.path.join(HERE, "paths.json"), "w", encoding="utf-8") as fh:
        json.dump({"checked": sorted(texts), "owner_value_checked": bool(owner), "git_name_words_checked": len(name),
                   "hits": hits}, fh, indent=2)
        fh.write("\n")
    print(json.dumps({"quotes": len(results), "quotes_not_found": len(problems),
                      "ice_problems": sum(len(r["problems"]) for r in ice), "path_hits": len(hits)}))
    return 0 if not problems and not hits and not any(r["problems"] for r in ice) else 1


if __name__ == "__main__":
    sys.exit(main())
