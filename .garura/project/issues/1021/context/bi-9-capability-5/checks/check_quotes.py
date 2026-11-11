#!/usr/bin/env python3
"""Check every quote on the draft pages, word for word, against the source its Sources line names.

Run from the repository root:
    python3 -B <run>/checks/check_quotes.py <run>
A quote is any text in straight double quotes. Line breaks and runs of spaces are folded to one
space in both the quote and the source, because the sources are hard-wrapped.
Each Sources line names one source; every quote after that name on the line must be in it:
  - "GitHub #<n>": the copy of the issue's title, text and comments in <run>/checks/gh/<n>.txt;
  - a path with "in Phoenix memory": this run's short-term copy, <run>/memory/<path>;
  - "1021/context/answers/<file>" with "in short-term memory": this run's copy, <run>/memory/answers/<file>;
  - any other path: the file in the repository.
A quote in the body must be found in a quote of the page's Sources, or in a source the page names.
Writes <run>/checks/quotes.json. Exit 1 when any quote is not found.
"""
import json, os, re, sys

run = sys.argv[1]
drafts = os.path.join(run, "drafts", "product-os")
QUOTE = re.compile(r'"([^"\n]+)"')
PATH = re.compile(r'((?:\.garura|core|docs|standards|knowledge)/[^\s,:;()"]+)')
STM = re.compile(r'(1021/context/answers/[\w.-]+\.md)')
GH = re.compile(r'GitHub #(\d+)')
fold = lambda s: re.sub(r"\s+", " ", s).strip()

def source_of(line):
    """Return (name, text or None, index after the name) for one Sources line."""
    m = GH.search(line)
    if m:
        p = os.path.join(run, "checks", "gh", f"{m.group(1)}.txt")
        return p, (open(p, encoding="utf-8").read() if os.path.exists(p) else None), m.end()
    m = STM.search(line)
    if m and "in short-term memory" in line:
        p = os.path.join(run, "memory", "answers", os.path.basename(m.group(1)))
        return p, (open(p, encoding="utf-8").read() if os.path.exists(p) else None), m.end()
    m = PATH.search(line)
    if not m:
        return None, None, 0
    path = m.group(1).rstrip(".")
    if "in Phoenix memory" in line:
        path = os.path.join(run, "memory", path)
    if os.path.isdir(path) or not os.path.exists(path):
        return path, None, m.end()
    return path, open(path, encoding="utf-8").read(), m.end()

results, problems, total = [], [], 0
for dirpath, _, files in sorted(os.walk(drafts)):
    for fn in sorted(files):
        if not fn.endswith(".md"):
            continue
        page = os.path.join(dirpath, fn)
        text = open(page, encoding="utf-8").read()
        body, _, sources = text.partition("\n## Sources\n")
        src_quotes, texts = [], []
        for line in sources.splitlines():
            if not line.startswith("- "):
                continue
            name, src, at = source_of(line)
            if src is not None:
                texts.append(fold(src))
            for q in QUOTE.findall(line[at:]):
                total += 1
                found = src is not None and fold(q) in fold(src)
                src_quotes.append(fold(q))
                results.append({"page": page, "where": "Sources", "source": name, "quote": q, "found": found})
                if not found:
                    problems.append({"page": page, "where": "Sources", "quote": q, "source": name})
            for q in QUOTE.findall(line[:at]):
                total += 1
                results.append({"page": page, "where": "Sources", "source": None, "quote": q, "found": False})
                problems.append({"page": page, "where": "Sources", "quote": q, "source": "a quote before the source's name"})
        for q in QUOTE.findall(body):
            total += 1
            fq = fold(q)
            in_sources = any(fq in s for s in src_quotes)
            in_text = any(fq in t for t in texts)
            ok = in_sources or in_text
            results.append({"page": page, "where": "body", "quote": q,
                            "in_a_sources_quote": in_sources, "in_a_named_source": in_text, "found": ok})
            if not ok:
                problems.append({"page": page, "where": "body", "quote": q, "source": "in no Sources quote and no named source"})

out = {"checked_on": "2026-11-10", "total": total, "not_found": len(problems), "problems": problems, "results": results}
json.dump(out, open(os.path.join(run, "checks", "quotes.json"), "w"), indent=2)
print(json.dumps({"total": total, "not_found": len(problems), "problems": problems}, indent=2))
sys.exit(1 if problems else 0)
