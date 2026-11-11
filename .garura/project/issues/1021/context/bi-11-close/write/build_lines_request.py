"""Build BI-11's close request: items 2, 3 and 4. Run from the repo root; writes lines-request.json beside this file."""
import json, os
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
root = ".garura/product/product-os"
S = "software-delivery-planning"
D = ("It also defines what a product is made of, and keeps each product's model as a living map: added to, changed and"
     " pruned as work is done, and the source of what to try next.")
SRC = '- .garura/product/product-os/software-delivery-planning/domain.md: "' + D + '"'
OLD = ("It sits in software delivery planning with the other capability of Product model. The domain's first paragraph does"
       " not name it yet; widening it is owed at this intent's close.")
NEW = "It sits in software delivery planning with the other capability of Product model, and the domain's first paragraph says so."
Q = "a feature doesn't need another feature. All of that is managed in the slices."
W = f"{S}/orchestrate-agent-work/fn-work-out-waits-on/feature.md"
PAGES = {
 f"{S}/domain.md": ([("and the model each part runs on. It does not release the work or run the product.",
                      "and the model each part runs on. " + D + " It does not release the work or run the product.")], None),
 f"{S}/define-product/capability.md": ([(OLD, NEW)], SRC),
 f"{S}/manage-model/capability.md": ([(OLD, NEW)], SRC),
 W: ([("\"Needs\" and \"identified by\" link capabilities and features (fn-725) renames it `needs`.",
       "Link the parts by the map's rules (fn-725), in Manage the model, renames it `needs`."),
      ("- Not decided: whether a feature's own needs count too, as the page of fn-725 says, or only the needs of its capability, as the ontology says.",
       f"- Only the needs of a feature's capability count, never a feature's own. The reason, in the product owner's words: \"{Q}\""),
      ("Product model owns them: \"Needs\" and \"identified by\" link capabilities and features (fn-725).",
       "Manage the model, in Product model, owns them: Link the parts by the map's rules (fn-725).")],
     f'- .garura/project/issues/1021/context/capabilities.md, line 125: "{Q}"'),
}
assert Q in open(".garura/project/issues/1021/context/capabilities.md", encoding="utf-8").read().split("\n")[124]
pages, n = [], 0
for rel, (subs, add) in PAGES.items():
    lines = open(os.path.join(root, rel), encoding="utf-8").read().split("\n")
    new, ch = list(lines), []
    for o, nw in subs:
        hit = [i for i, l in enumerate(lines) if o in l]
        assert len(hit) == 1, (rel, o[:60], len(hit))
        i = hit[0]
        assert not any(c.get("old") == lines[i] for c in ch)
        new[i] = new[i].replace(o, nw)
        ch.append({"old": lines[i], "new": new[i]})
    if add:
        last = [l for l in lines if l.strip()][-1]
        assert lines.count(last) == 1 and last.startswith("- "), rel
        ch.append({"after": last, "add": add})
    n += len(ch)
    pages.append({"page": rel, "changes": ch})
json.dump({"by": "product-os-keeper, for #1021 (reorganise the business intents): BI-11 (Product model) close",
           "source": "The product owner's reply of 2026-11-11, recorded in .garura/project/issues/1021/context/bi-11-close/approval.md: \"1 yes, 2 yes, 3 yes, 4 yes, 5 drop\"",
           "pages": pages}, open(os.path.join(HERE, "lines-request.json"), "w"), ensure_ascii=False, indent=1)
print("pages", len(pages), "changes", n)
