"""Build BI-10's close request, items 2 and 3: one sentence in the domain's first paragraph, and on the six capability
pages the domain sentence settled and one Sources line quoting the domain's new sentence. Run from the repo root.
"""
import json, os
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
root = ".garura/product/product-os"
D = ("It also keeps the foundation every part stands on: the written standards and their checks, the builders a team uses"
     " for its own plays and loops, where everything lives, the settings, three tiers of memory, and the model each part runs on.")
SRC = '- .garura/product/product-os/software-delivery-planning/domain.md: "' + D + '"'
OLD = ("It sits in software delivery planning with the other capabilities of Standards, structure, settings and memory. The"
       " domain's first paragraph does not name them yet; widening it is owed at this intent's close.")
NEW = ("It sits in software delivery planning with the other capabilities of Standards, structure, settings and memory, and"
       " the domain's first paragraph says so.")
S = "software-delivery-planning"
PAGES = {f"{S}/domain.md": {"sub": [("and gives every gate a way past. It does not release the work or run the product.",
                                     "and gives every gate a way past. " + D + " It does not release the work or run the product.")], "add": False}}
for slug in ("standards", "build-your-own-harness", "structure", "settings", "memory", "model-routing"):
    PAGES[f"{S}/{slug}/capability.md"] = {"sub": [(OLD, NEW)], "add": True}
pages, n = [], 0
for rel, ops in PAGES.items():
    lines = open(os.path.join(root, rel), encoding="utf-8").read().split("\n")
    changes = []
    for o, nw in ops["sub"]:
        hit = [i for i, l in enumerate(lines) if o in l]
        assert len(hit) == 1, (rel, len(hit))
        i = hit[0]
        assert lines.count(lines[i]) == 1
        changes.append({"old": lines[i], "new": lines[i].replace(o, nw)})
    if ops["add"]:
        last = [l for l in lines if l.strip()][-1]
        assert lines.count(last) == 1 and last.startswith("- "), rel
        changes.append({"after": last, "add": SRC})
    n += len(changes)
    pages.append({"page": rel, "changes": changes})
json.dump({"by": "product-os-keeper, for #1021 (reorganise the business intents): BI-10 (Standards, structure, settings and memory) close",
           "source": "The product owner's reply of 2026-11-11, recorded in .garura/project/issues/1021/context/bi-10-close/approval.md: \"Yes to domains opening paragraph as Yes to the six capability pages.\"",
           "pages": pages}, open(os.path.join(HERE, "lines-request.json"), "w"), ensure_ascii=False, indent=1)
print("pages", len(pages), "changes", n)
