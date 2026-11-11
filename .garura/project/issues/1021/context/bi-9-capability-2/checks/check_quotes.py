#!/usr/bin/env python3
"""Check every quote on the draft pages of Run plays as loops, word for word.

- A quote on a Sources line must be in the file that line names. A Phoenix memory file is read
  from this run's memory copy (copied through the memory tool). When the line names lines, the
  quote must also sit inside those lines.
- A quote in the page text must be in one of the files the page's Sources lines name. An ICE
  page's quotes are looked for in its part page's sources.
Whitespace runs count as one space; bold marks (**) are ignored. Run from the repository root.
Writes checks/quotes.json. Exit 0 when every quote is found, 1 otherwise.
"""
import glob, json, os, re, sys, datetime

RUN = ".garura/project/issues/1021/context/bi-9-capability-2"
DRAFTS = f"{RUN}/drafts/product-os/software-delivery-planning/run-plays-as-loops"
MEMORY = f"{RUN}/memory"
PATH_RE = re.compile(r"((?:\.garura|core|docs|standards)/[^\s,:;]+)")
QUOTE_RE = re.compile(r'"([^"]+)"')


def load(path):
    """(normalised text, list of (start offset, line number)) for a source file."""
    lines = open(path, encoding="utf-8").read().splitlines()
    parts, marks, pos = [], [], 0
    for n, raw in enumerate(lines, 1):
        s = re.sub(r"\s+", " ", raw.replace("**", "")).strip()
        if not s:
            continue
        marks.append((pos, n))
        parts.append(s)
        pos += len(s) + 1
    return " ".join(parts), marks


def line_at(marks, off):
    n = marks[0][1]
    for start, ln in marks:
        if start <= off:
            n = ln
        else:
            break
    return n


def norm(q):
    return re.sub(r"\s+", " ", q.replace("**", "")).strip()


def ranges(text_after_path):
    m = re.match(r"[^:\"]*?\blines?\s+([0-9][0-9 ,\-–and]*)", text_after_path)
    if not m:
        return []
    out = []
    for tok in re.findall(r"\d+(?:\s*-\s*\d+)?", m.group(1)):
        a, _, b = tok.partition("-")
        out.append((int(a), int(b or a)))
    return out


def source_file(path, line):
    if "in Phoenix memory" in line:
        return os.path.join(MEMORY, path)
    return path


def sources_of(text):
    """The Sources section's lines: (line, file or None, line ranges, quotes)."""
    m = re.search(r"(?ms)^## Sources\n(.*?)(?=^## |\Z)", text)
    out = []
    for line in (m.group(1).splitlines() if m else []):
        if not line.startswith("- "):
            continue
        pm = PATH_RE.search(line)
        f = source_file(pm.group(1), line) if pm else None
        rg = ranges(line[pm.end():]) if pm else []
        out.append((line, f, rg, QUOTE_RE.findall(line)))
    return out


def body_quotes(text):
    body = re.sub(r"(?ms)^## Sources\n.*?(?=^## |\Z)", "", text)
    found = []
    for n, line in enumerate(body.splitlines(), 1):
        for q in QUOTE_RE.findall(line.replace("`", "")) if False else QUOTE_RE.findall(line):
            found.append((n, q))
    return found


def main():
    pages = sorted(glob.glob(f"{DRAFTS}/**/*.md", recursive=True))
    cache, problems, checked = {}, [], 0
    for page in pages:
        text = open(page, encoding="utf-8").read()
        part = page if not page.endswith("/ice.md") else (
            os.path.join(os.path.dirname(page), "capability.md") if os.path.dirname(page) == DRAFTS
            else os.path.join(os.path.dirname(page), "feature.md"))
        srcs = sources_of(open(part, encoding="utf-8").read())
        files = []
        for line, f, rg, quotes in srcs:
            if f is None:
                continue
            if not os.path.isfile(f):
                problems.append({"page": page, "source": f, "problem": "the source file is not there"})
                continue
            cache.setdefault(f, load(f))
            files.append(f)
            if page != part:
                continue  # an ICE page lists no sources of its own
            norm_text, marks = cache[f]
            for q in quotes:
                checked += 1
                nq = norm(q)
                spots = [m.start() for m in re.finditer(re.escape(nq), norm_text)]
                if not spots:
                    problems.append({"page": page, "where": "Sources", "source": f, "quote": q, "problem": "not found word for word"})
                    continue
                if rg:
                    places = [(line_at(marks, i), line_at(marks, i + len(nq) - 1)) for i in spots]
                    if not any(a <= hi and b >= lo for a, b in places for lo, hi in rg):
                        problems.append({"page": page, "where": "Sources", "source": f, "quote": q,
                                         "problem": f"found at lines {places}, outside the lines named {rg}"})
        for n, q in body_quotes(text):
            checked += 1
            hits = [f for f in files if cache[f][0].find(norm(q)) >= 0]
            if not hits:
                problems.append({"page": page, "where": f"text line {n}", "quote": q, "problem": "not found in any source the page lists"})
    rec = {"checked_on": datetime.date.today().isoformat(),
           "how": "each quote on a Sources line is looked for in the file that line names (a Phoenix memory file in this run's memory copy, read through the memory tool), and inside the lines it names; each quote in the page text in any source its page lists (for an ICE page, its part page's sources); whitespace and bold marks are ignored",
           "pages": len(pages), "quotes_checked": checked, "not_found": len(problems), "problems": problems}
    json.dump(rec, open(f"{RUN}/checks/quotes.json", "w"), indent=2)
    print(json.dumps({"pages": len(pages), "quotes_checked": checked, "problems": len(problems)}))
    for p in problems:
        print(" -", os.path.relpath(p["page"], DRAFTS), p.get("where"), "|", p.get("quote", p.get("source")), "|", p["problem"])
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
