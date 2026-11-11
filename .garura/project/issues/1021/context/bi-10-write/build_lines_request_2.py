"""Build the second named-lines request for BI-10: the six approved lines that named the three old capabilities by id,
or cited their pages, so the merge into Standards can run. Each keeps its meaning: titles in place of ids, and the
old pages cited from the copies kept in old-pages/ (byte for byte, taken before the merge).

Run from the repo root. Writes lines-request-2.json, and applies the same changes to the drafts so the drafts stay
equal to the model.
"""
import json, os
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
OP = f"{HERE}/old-pages"
CH = {
 "software-delivery-planning/standards/capability.md": [
  ("The harness standard, written down (cap-735), The naming checks, built before any rename (cap-739), and Every name moved to the standard, one family at a time (cap-742).",
   "The harness standard, written down; The naming checks, built before any rename; and Every name moved to the standard, one family at a time."),
  ("- .garura/project/issues/1021/context/capabilities.md, line 117: \"the three old capabilities under bi-734 (cap-735, cap-739, cap-742) and their nine features merge into Standards, each feature kept and rewritten to what was built, fn-741 keeping its id for BI-7's fn-748\"",
   "- .garura/project/issues/1021/context/capabilities.md, line 117: \"and their nine features merge into Standards, each feature kept and rewritten to what was built, fn-741 keeping its id for BI-7's fn-748\""),
  ("- .garura/product/product-os/capabilities/cap-735/capability.md, line 9: \"a rule exists only in code or in a person's head.\"",
   f"- {OP}/harness-standard-written-down.md, which keeps the page of The harness standard, written down, as it was before the merge, line 9: \"a rule exists only in code or in a person's head.\""),
  ("- .garura/product/product-os/capabilities/cap-739/capability.md and cap-742/capability.md: the two other capabilities this one takes in",
   f"- {OP}/naming-checks.md and {OP}/every-name-moved.md, which keep the pages of the two other capabilities this one takes in, as they were before the merge"),
 ],
 "features/fn-737/feature.md": [
  ("under The harness standard, written down (cap-735), which asked",
   "under The harness standard, written down, which asked"),
  ("- .garura/product/product-os/capabilities/cap-735/capability.md, lines 4 and 8: \"in plain words a client can read\", \"Says what and why; how each part is built stays in its own docs.\"",
   f"- {OP}/harness-standard-written-down.md, which keeps that page as it was before the merge, lines 4 and 8: \"in plain words a client can read\", \"Says what and why; how each part is built stays in its own docs.\""),
 ],
}
DRAFT = {"software-delivery-planning/standards/capability.md":
         ".garura/project/issues/1021/context/bi-10-capability-1/drafts/product-os/software-delivery-planning/standards/capability.md",
         "features/fn-737/feature.md": ".garura/project/issues/1021/context/bi-10-capability-1/drafts/product-os/features/fn-737/feature.md"}
pages = []
for rel, subs in CH.items():
    lines = open(f"{MODEL}/{rel}", encoding="utf-8").read().split("\n")
    changes, new = [], list(lines)
    for o, n in subs:
        hit = [i for i, l in enumerate(lines) if o in l]
        assert len(hit) == 1, (rel, o[:60], len(hit))
        i = hit[0]
        new[i] = new[i].replace(o, n)
        changes.append({"old": lines[i], "new": new[i]})
    pages.append({"page": rel, "changes": changes})
    d = DRAFT[rel]
    assert open(d, encoding="utf-8").read() == "\n".join(lines), d
    open(d, "w", encoding="utf-8").write("\n".join(new))
json.dump({"by": "product-os-keeper (reorganise business intents, #1021)",
           "source": f"{HERE}/approval.md: the approved pages, with the old capabilities named by title, not by id, and the old pages cited from the copies kept before the merge, so the approved merge into Standards can run",
           "pages": pages}, open(f"{HERE}/lines-request-2.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("pages", len(pages), "changes", sum(len(p["changes"]) for p in pages))
