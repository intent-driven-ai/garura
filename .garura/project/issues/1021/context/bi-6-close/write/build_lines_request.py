import json, os, sys
root = sys.argv[1]; copy = sys.argv[2]; out = sys.argv[3]
D = "Once the product is in use, it takes in how the product is used, what people say about it and what its competitors do, works out what consumers want, and turns that into new features or changes to the model, as recommendations to the product owner or on their own where the product owner allows it."
DQ = '- .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into working code that a check from the outside can prove."'
SUB = [
 ("**Outcome:** What happens in use flows back. What happened is compared with what was intended, drift is found, and the intents, model and memory stay true.",
  "**Outcome:** What happens in use flows back. How the product is used, what people say about it and what its competitors do are taken in from the tools and forums the product owner connects; what consumers want and what the competition is doing are drawn from them, each finding resting on the items it came from; and the findings are turned into new features or changes to the product model, each one a recommendation to the product owner unless he allowed its kind to go ahead on its own."),
 ("**Why:** Without this, what is built and what was intended pull apart without anyone noticing.",
  "**Why:** Without this, the product is built from what was intended at the start, while what its consumers want and what its competitors do move on unseen."),
 ("- Drift between the model and the work gets named.",
  "- Every finding on what consumers want or what a competitor is doing names the items it rests on, and the same items give the same findings."),
 ("- Each learning is promoted on purpose.",
  "- Every change drawn from the findings starts only from the product owner's yes, or from a kind he allowed to go ahead on its own, and each one that went ahead was shown to him at once with a way back."),
 ("set before the build. It does not release the work or run the product.",
  "set before the build. " + D + " It does not release the work or run the product."),
 ("The domain's first paragraph does not yet say this; whether this capability stays in the domain, with that paragraph changed when Run → Product closes, or moves to a domain of its own, is not decided.",
  "It sits in that domain with the other two capabilities of Run → Product, and the domain's first paragraph says so: once the product is in use, the domain takes in how it is used, what people say about it and what its competitors do."),
 ("It sits there for now, with the first capability of Run → Product; where the capabilities of Run → Product sit is settled when Run → Product closes.",
  "It sits in that domain with the other two capabilities of Run → Product, and the domain's first paragraph says so: the domain works out what consumers want from what it takes in."),
 ("It sits there for now, with the first two capabilities of Run → Product; where the capabilities of Run → Product sit is settled when Run → Product closes.",
  "It sits in that domain with the other two capabilities of Run → Product, and the domain's first paragraph says so: the domain turns what consumers want into new features or changes to the model."),
]
FULL = {
 "software-delivery-planning/connect-use-and-market/capability.md": (DQ + ', "It does not release the work or run the product."', DQ + ', "It does not release the work or run the product.", "' + D + '"'),
 "software-delivery-planning/understand-consumers-and-competition/capability.md": (DQ, DQ + ', "' + D + '"'),
 "software-delivery-planning/build-or-update-product/capability.md": (DQ, DQ + ', "' + D + '"'),
}
pages = []; hits = {s[0]: 0 for s in SUB}; full_hits = 0
for dp, dn, fn in os.walk(root):
    for f in sorted(fn):
        if not f.endswith(".md"): continue
        p = os.path.join(dp, f); rel = os.path.relpath(p, root)
        lines = open(p, encoding="utf-8").read().split("\n")
        changes = []; newlines = list(lines)
        for i, ln in enumerate(lines):
            new = ln
            if rel in FULL and ln.rstrip() == FULL[rel][0]:
                new = FULL[rel][1]; full_hits += 1
            for o, n in SUB:
                if o in new:
                    hits[o] += new.count(o); new = new.replace(o, n)
            if new != ln:
                assert lines.count(ln) == 1, (rel, ln[:80])
                changes.append({"old": ln, "new": new}); newlines[i] = new
        if changes:
            pages.append({"page": rel, "changes": changes})
            cp = os.path.join(copy, rel); open(cp, "w", encoding="utf-8").write("\n".join(newlines))
req = {"by": "product-os-keeper, for #1021 (reorganise the business intents): BI-6 (Run → Product) close",
       "source": "The product owner's approval of 2026-11-10, reply \"yes, apply and commit and cp\", recorded in .garura/project/issues/1021/context/bi-6-close/approval.md, of the proposal in .garura/project/issues/1021/context/bi-6-close/proposal.md: BI-6's Outcome, Why and Proof it is met; one sentence added to the domain page's first paragraph, as the three capabilities of Run → Product stay in software delivery planning; the domain lines on those three capability pages and their quotes of the domain page.",
       "pages": pages}
json.dump(req, open(out, "w"), ensure_ascii=False, indent=1)
print("pages", len(pages), "line changes", sum(len(p["changes"]) for p in pages), "full-line hits", full_hits)
for o, c in hits.items(): print(c, "x", o[:70])
