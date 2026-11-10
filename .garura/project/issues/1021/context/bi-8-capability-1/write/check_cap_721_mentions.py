"""Before the merge: list every page or ICE page under the model that names cap-721 as a whole word.

Run from the repo root. Reads only; prints JSON. cap-721's own page is listed apart.
"""
import json
import os
import re

ROOT = ".garura/product/product-os"
OWN = "capabilities/cap-721/capability.md"
WORD = re.compile(r"(?<![\w-])cap-721(?![\w-])")
hits, own = [], []
for d, _, files in os.walk(ROOT):
    for f in sorted(files):
        if not f.endswith(".md"):
            continue
        path = os.path.join(d, f)
        rel = os.path.relpath(path, ROOT)
        for n, line in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
            if WORD.search(line):
                (own if rel == OWN else hits).append({"page": rel, "line": n, "text": line})
print(json.dumps({"pages_naming_cap_721": hits, "own_page_lines": own,
                  "clear": not hits}, indent=2))
