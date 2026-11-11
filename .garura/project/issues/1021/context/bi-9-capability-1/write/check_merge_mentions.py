"""Before the merge: list every .md or .yaml file under the model that names cap-719, cap-720 or
cap-shape-slice as a whole word, other than _spine.yaml and the three capabilities' own pages.

Run from the repo root. Reads only; prints JSON. The own pages' lines are listed apart.
"""
import json
import os
import re

ROOT = ".garura/product/product-os"
IDS = ["cap-719", "cap-720", "cap-shape-slice"]
OWN = {"capabilities/cap-719/capability.md", "capabilities/cap-720/capability.md",
       "software-delivery-planning/shape-slice/capability.md"}
SKIP = {"_spine.yaml"}
WORD = re.compile(r"(?<![\w-])(" + "|".join(re.escape(i) for i in IDS) + r")(?![\w-])")
hits, own = [], []
for d, _, files in os.walk(ROOT):
    for f in sorted(files):
        if not f.endswith((".md", ".yaml", ".yml")):
            continue
        path = os.path.join(d, f)
        rel = os.path.relpath(path, ROOT)
        if rel in SKIP:
            continue
        for n, line in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
            for m in WORD.finditer(line):
                (own if rel in OWN else hits).append({"file": rel, "line": n, "id": m.group(1), "text": line})
print(json.dumps({"ids": IDS, "files_naming_them": hits, "own_page_lines": own,
                  "clear": not hits}, indent=2, ensure_ascii=False))
