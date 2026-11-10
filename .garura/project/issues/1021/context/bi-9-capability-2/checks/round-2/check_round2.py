#!/usr/bin/env python3
"""Check the new and changed pages of one BI-9 capability folder (round 2 of the drafts).

Run from the repository root:
    python3 -B <run>/checks/round-2/check_round2.py --run <run> --cap <capability folder> \
        --new <fn-...> [<fn-...> ...] --changed <page> [<page> ...]
A page is named relative to <run>/drafts/product-os/software-delivery-planning/<cap>/.

Checks:
- quotes: every quote in straight double quotes on a page is found word for word. A quote on a
  Sources line is looked for in the file that line names, and inside the lines it names. A
  Phoenix memory file is read from the run's short-term copy (<run>/memory/<path>), a file
  "in short-term memory" from its short-term copy (<run>/memory/<path under the issues
  folder>), a GitHub issue from its saved copy (<run>/checks/gh/<n>.txt). A quote in the page
  text must be in a file one of the page's Sources lines names (for an ICE page, its part
  page's Sources). Runs of whitespace count as one space; bold marks (**) are ignored.
- each new ICE page: the Thin line, exactly, then a blank line; Intent, Context and Expectation
  in that order; one Goal; one to three Limits; one to three Fails if; the Read line with the
  exact opening and something to look for; one Never read, Persona and Scope; one Scenario; one
  Done means checked by someone other than the doer; and the part page holds no ICE section.
- each new feature page: the headings in order; three or more examples from three or more
  kinds of project; How it meets the capability; a Status line that reads not built and gives
  each issue number with what it is about; each rule with a quoted reason, or a Not decided
  line; each criterion Given/When/Then and marked "This is not built."; each Out of scope line
  naming its owner; Sources.
- every new or changed page: no Not decided line holds a lean; no personal path, name or
  pronoun for a person; the old word for a loop only inside a quote or a file name.
Writes <run>/checks/round-2/checks.json. Exit 0 when nothing is wrong, 1 otherwise.
"""
import argparse, datetime, json, os, re, sys

THIN = "Thin: proposed from the person's words; deepen with `/discover-capabilities`."
READ = ("Gather it from the memory layer. Look first at the project's existing memory and its existing "
        "implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and "
        "raise a memory update for a person to approve. For this part, look for: ")
HEADINGS = ["## What it does", "## Inputs / Outputs", "## Rules & behavior", "## Acceptance criteria",
            "## Out of scope", "## Sources"]
PATH = re.compile(r"((?:\.garura|core|docs|standards|knowledge)/[^\s,:;()\"]+)")
QUOTE = re.compile(r'"([^"\n]+)"')
LEAN = re.compile(r"\b(lean|leans|leaning|suggest|suggests|likely|probably|should|recommend|recommends|prefer|"
                  r"preferred|best|ideally|better|default|for now|we think|we propose)\b", re.I)
PERSONAL = [("home folder", re.compile(r"/Users/|/home/|~/")),
            ("temp folder", re.compile(r"/tmp\b|/private/|/var/folders|mktemp")),
            ("a person's name", re.compile("|".join(["ka"+"pil","ahu"+"ja","vi"+"ren","naga"+"rro"]), re.I)),
            ("a pronoun for a person", re.compile(r"\b(he|his|him|she|her|hers)\b", re.I))]
OWNER = re.compile(r"\b(owns?|own them|own it|does it|does them|do them|do it|records it|lays it)\b|\(fn-")


def norm(s):
    return re.sub(r"\s+", " ", s.replace("**", "")).strip()


def load(path):
    """(normalised text, [(offset, line number)]) for a source file."""
    parts, marks, pos = [], [], 0
    for n, raw in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
        s = norm(raw)
        if not s:
            continue
        marks.append((pos, n))
        parts.append(s)
        pos += len(s) + 1
    return " ".join(parts), marks


def line_at(marks, off):
    n = marks[0][1]
    for start, ln in marks:
        if start > off:
            break
        n = ln
    return n


def ranges(desc_after_path):
    m = re.search(r"\blines?\s+([0-9][0-9 ,\-–and]*)", desc_after_path)
    if not m:
        return []
    out = []
    for tok in re.findall(r"\d+(?:\s*[-–]\s*\d+)?", m.group(1)):
        bits = re.split(r"\s*[-–]\s*", tok)
        out.append((int(bits[0]), int(bits[-1])))
    return out


def resolve(run, desc):
    gh = re.search(r"GitHub #(\d+)", desc)
    if gh:
        return os.path.join(run, "checks", "gh", f"{gh.group(1)}.txt"), ""
    m = PATH.search(desc)
    if not m:
        return None, ""
    path = m.group(1).rstrip(".")
    after = desc[m.end():]
    if "in Phoenix memory" in desc:
        return os.path.join(run, "memory", path), after
    if "in short-term memory" in desc and path.startswith(".garura/project/issues/"):
        return os.path.join(run, "memory", path[len(".garura/project/issues/"):]), after
    return path, after


def sources(run, text):
    m = re.search(r"(?ms)^## Sources\n(.*?)(?=^## |\Z)", text)
    out = []
    for line in (m.group(1).splitlines() if m else []):
        if not line.startswith("- "):
            continue
        desc = line[2:].split(': "', 1)[0]
        f, after = resolve(run, desc)
        out.append({"line": line, "file": f, "ranges": ranges(after), "quotes": QUOTE.findall(line[2 + len(desc):])})
    return out


def body_of(text):
    return re.sub(r"(?ms)^## Sources\n.*?(?=^## |\Z)", "", text)


def check_quotes(run, page, part, cache):
    probs, n = [], 0
    srcs = sources(run, open(part, encoding="utf-8").read())
    files = []
    for s in srcs:
        f = s["file"]
        if f is None:
            if s["quotes"]:
                probs.append(f"Sources line with quotes names no file: {s['line'][:80]}")
            continue
        if not os.path.isfile(f):
            probs.append(f"source file not there: {f}")
            continue
        cache.setdefault(f, load(f))
        files.append(f)
        if page != part:
            continue
        text, marks = cache[f]
        for q in s["quotes"]:
            n += 1
            nq = norm(q)
            spots = [m.start() for m in re.finditer(re.escape(nq), text)]
            if not spots:
                probs.append(f"not found word for word in {f}: {q[:90]}")
            elif s["ranges"]:
                places = [(line_at(marks, i), line_at(marks, i + len(nq) - 1)) for i in spots]
                if not any(a <= hi and b >= lo for a, b in places for lo, hi in s["ranges"]):
                    probs.append(f"found in {f} at {places}, outside the lines named {s['ranges']}: {q[:70]}")
    for ln, line in enumerate(body_of(open(page, encoding="utf-8").read()).splitlines(), 1):
        for q in QUOTE.findall(line):
            n += 1
            if not any(cache[f][0].find(norm(q)) >= 0 for f in files):
                probs.append(f"text line {ln}: quote in no source the page lists: {q[:90]}")
    return n, probs


def sections(text):
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur is not None and line.strip():
            out[cur].append(line)
    return out


def check_ice(page, part):
    text = open(page, encoding="utf-8").read()
    lines = text.splitlines()
    sec = sections(text)
    count = lambda s, label: sum(1 for l in sec.get(s, []) if l.startswith(f"- {label}:"))
    read = [l for l in sec.get("Context", []) if l.startswith("- Read: ")]
    done = [l for l in sec.get("Expectation", []) if l.startswith("- Done means:")]
    part_heads = [l for l in open(part, encoding="utf-8").read().splitlines() if l.startswith("## ")]
    r = {"thin_line": len(lines) > 1 and lines[0] == THIN and lines[1] == "",
         "sections": [l for l in lines if l.startswith("## ")],
         "goal": count("Intent", "Goal"), "limit": count("Intent", "Limit"), "fails_if": count("Intent", "Fails if"),
         "read_opening_exact": bool(read) and read[0][len("- Read: "):].startswith(READ),
         "read_names_what": bool(read) and len(read[0]) > len("- Read: ") + len(READ) + 20,
         "never_read": count("Context", "Never read"), "persona": count("Context", "Persona"),
         "scope": count("Context", "Scope"), "scenario": count("Expectation", "Scenario"),
         "done_means": len(done), "done_by_other": bool(done) and done[0].startswith("- Done means: Someone other than"),
         "part_page_has_no_ice_section": not any(h in ("## Intent", "## Context", "## Expectation", "## Agent intent (ICE)") for h in part_heads)}
    p = []
    if not r["thin_line"]: p.append("the first line is not the Thin line followed by a blank line")
    if r["sections"] != ["## Intent", "## Context", "## Expectation"]: p.append("not Intent, Context, Expectation in order")
    if r["goal"] != 1: p.append("not exactly one Goal")
    if not 1 <= r["limit"] <= 3: p.append(f"{r['limit']} Limits, not one to three")
    if not 1 <= r["fails_if"] <= 3: p.append(f"{r['fails_if']} Fails if, not one to three")
    for k in ("read_opening_exact", "read_names_what", "done_by_other", "part_page_has_no_ice_section"):
        if not r[k]: p.append(f"{k} is false")
    for k in ("never_read", "persona", "scope", "scenario", "done_means"):
        if r[k] != 1: p.append(f"{k}: {r[k]}, not 1")
    r["problems"] = p
    return r


def check_feature(page):
    text = open(page, encoding="utf-8").read()
    p, notes = [], {}
    heads = [l for l in text.splitlines() if l.startswith("## ")]
    if not text.startswith("# Feature: "): p.append("no '# Feature:' title")
    if heads != HEADINGS: p.append(f"headings are {heads}")
    sec = {}
    cur = None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip(); sec[cur] = []
        elif cur:
            sec[cur].append(line)
    what = "\n".join(sec.get("What it does", [])) + "\n"
    ex = re.search(r"(?m)^- Examples, in different kinds of project:\n((?:  - .*\n)+)", what)
    kinds = re.findall(r"(?m)^  - In an? ([^,]+),", ex.group(1)) if ex else []
    notes["example_kinds"] = kinds
    if len(kinds) < 3 or len(set(kinds)) < 3: p.append("fewer than three examples from three kinds of project")
    if "- How it meets the capability:" not in what: p.append("no How it meets the capability line")
    status = re.search(r"(?m)^Status: (.*)$", what)
    notes["status"] = status.group(1)[:160] if status else None
    if not status or not status.group(1).startswith("not built"):
        p.append("no Status line that reads not built")
    else:
        unquoted = re.sub(r'"[^"]*"', '""', status.group(0))  # an issue number inside a quote is the source's
        for m in re.finditer(r"#(\d+)", unquoted):
            tail = unquoted[m.end():m.end() + 3]
            if not (tail.startswith(", ") or tail.startswith(" (")):
                p.append(f"Status names #{m.group(1)} without what it is about")
    rules = [l for l in sec.get("Rules & behavior", []) if l.startswith("- ")]
    for l in rules:
        if not (l.startswith("- Not decided:") or re.search(r'The reason[^:]*: .*"', l)):
            p.append(f"a rule has no quoted reason: {l[:70]}")
    crit = [l for l in sec.get("Acceptance criteria", []) if l.startswith("- ")]
    for l in crit:
        if not re.match(r"- Given .*, when .*, then .*", l): p.append(f"a criterion is not Given/When/Then: {l[:70]}")
        if not l.endswith("This is not built."): p.append(f"a criterion is not marked not built: {l[:70]}")
    oos = [l for l in sec.get("Out of scope", []) if l.startswith("- ")]
    for l in oos:
        if not OWNER.search(l): p.append(f"an Out of scope line names no owner: {l[:70]}")
    notes.update({"rules": len(rules), "criteria": len(crit), "out_of_scope": len(oos)})
    return p, notes


def outside_quotes(line):
    line = re.sub(r'"[^"]*"', '""', line)
    return " ".join(t for t in line.split() if "/" not in t and not re.search(r"\.(md|py|yaml|json)\b", t))


def check_every(page):
    p, nd = [], []
    for n, line in enumerate(open(page, encoding="utf-8").read().splitlines(), 1):
        for name, rx in PERSONAL:
            if rx.search(line):
                p.append(f"line {n}: {name}: {line.strip()[:100]}")
        if re.search(r"\bdriv(e|es|ing)\b", outside_quotes(line), re.I):
            p.append(f"line {n}: the old word for a loop outside a quote or a file name")
        for m in re.finditer(r"Not decided: (.*)", line):
            nd.append(m.group(1))
            if LEAN.search(m.group(1)):
                p.append(f"line {n}: a Not decided line holds a lean: {m.group(1)[:100]}")
    return p, nd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--cap", required=True)
    ap.add_argument("--new", nargs="*", default=[])
    ap.add_argument("--changed", nargs="*", default=[])
    a = ap.parse_args()
    base = os.path.join(a.run, "drafts", "product-os", "software-delivery-planning", a.cap)
    cache, results = {}, []
    pages = []
    for fn in a.new:
        pages += [("new", f"{fn}/feature.md", f"{fn}/feature.md"), ("new", f"{fn}/ice.md", f"{fn}/feature.md")]
    for pg in a.changed:
        pages.append(("changed", pg, pg))
    for kind, rel, part_rel in pages:
        page, part = os.path.join(base, rel), os.path.join(base, part_rel)
        r = {"page": rel, "kind": kind, "problems": []}
        n, qp = check_quotes(a.run, page, part, cache)
        r["quotes_checked"], r["quote_problems"] = n, qp
        ep, nd = check_every(page)
        r["not_decided"] = nd
        r["problems"] += qp + ep
        if kind == "new" and rel.endswith("/ice.md"):
            ice = check_ice(page, part)
            r["ice"] = ice
            r["problems"] += ice["problems"]
        if kind == "new" and rel.endswith("/feature.md"):
            fp, notes = check_feature(page)
            r["feature"] = notes
            r["problems"] += fp
        results.append(r)
    out = {"checked_on": datetime.date.today().isoformat(), "run": a.run, "capability": a.cap,
           "pages": len(results), "quotes_checked": sum(r["quotes_checked"] for r in results),
           "pages_with_problems": sum(1 for r in results if r["problems"]), "results": results}
    os.makedirs(os.path.join(a.run, "checks", "round-2"), exist_ok=True)
    json.dump(out, open(os.path.join(a.run, "checks", "round-2", "checks.json"), "w"), indent=2, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in ("pages", "quotes_checked", "pages_with_problems")}))
    for r in results:
        extra = ""
        if "ice" in r:
            extra = f" limits={r['ice']['limit']} fails_if={r['ice']['fails_if']} thin={r['ice']['thin_line']} read={r['ice']['read_opening_exact']}"
        print(("ok  " if not r["problems"] else "FAIL"), r["page"], f"quotes={r['quotes_checked']}" + extra)
        for p in r["problems"]:
            print("     -", p)
    return 0 if not out["pages_with_problems"] else 1


if __name__ == "__main__":
    sys.exit(main())
