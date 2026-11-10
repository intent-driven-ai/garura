#!/usr/bin/env python3
"""Check every quote on the draft pages, word for word, against the source its Sources line names.

Run from the repository root:
    python3 -B <run>/checks/check_quotes.py <run>
A quote is any text in straight double quotes. Line breaks and runs of spaces are folded to one
space in both the quote and the source, because the sources are hard-wrapped. A Phoenix memory
source is read from this run's short-term copy (<run>/memory/<path>); a GitHub issue from the
copy of its title and text saved in <run>/checks/gh/<n>.txt. Writes <run>/checks/quotes.json.
"""
import json, os, re, sys

run = sys.argv[1]
drafts = os.path.join(run, "drafts", "product-os")
QUOTE = re.compile(r'"([^"\n]+)"')
PATH = re.compile(r'((?:\.garura|core|docs|standards|knowledge)/[^\s,:;()"]+)')
fold = lambda s: re.sub(r"\s+", " ", s).strip()

def source_text(desc):
    gh = re.search(r"GitHub #(\d+)", desc)
    if gh:
        p = os.path.join(run, "checks", "gh", f"{gh.group(1)}.txt")
        return p, (open(p, encoding="utf-8").read() if os.path.exists(p) else None)
    m = PATH.search(desc)
    if not m:
        return None, None
    path = m.group(1).rstrip(".")
    if "in Phoenix memory" in desc:
        path = os.path.join(run, "memory", path)
    if os.path.isdir(path) or not os.path.exists(path):
        return path, None
    return path, open(path, encoding="utf-8").read()

results, problems, total = [], [], 0
for dirpath, _, files in os.walk(drafts):
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
            desc = line[2:].split(': "', 1)[0]
            path, src = source_text(desc)
            if src is not None:
                texts.append(fold(src))
            for q in QUOTE.findall(line[2 + len(desc):]):
                total += 1
                found = src is not None and fold(q) in fold(src)
                src_quotes.append(fold(q))
                results.append({"page": page, "where": "Sources", "source": path, "quote": q, "found": found})
                if not found:
                    problems.append({"page": page, "quote": q, "source": path})
        for q in QUOTE.findall(body):
            total += 1
            fq = fold(q)
            in_sources = any(fq in s for s in src_quotes)
            in_text = any(fq in t for t in texts)
            ok = in_sources or in_text
            results.append({"page": page, "where": "body", "quote": q,
                            "in_a_sources_quote": in_sources, "in_a_named_source": in_text, "found": ok})
            if not ok:
                problems.append({"page": page, "quote": q, "source": "body: in no Sources quote and no named source"})

out = {"checked_on": "2026-11-10", "total": total, "not_found": len(problems), "problems": problems, "results": results}
json.dump(out, open(os.path.join(run, "checks", "quotes.json"), "w"), indent=2)
print(json.dumps({"total": total, "not_found": len(problems), "problems": problems}, indent=2))
sys.exit(1 if problems else 0)
