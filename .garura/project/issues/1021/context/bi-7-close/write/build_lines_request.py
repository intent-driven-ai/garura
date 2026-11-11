import json, os, sys
root, copy, out = sys.argv[1], sys.argv[2], sys.argv[3]
D = "It also gets Garura itself into a project, sets the project up for it, keeps it current, and serves whichever coding tool the team works in."
NEWSIT = "It sits in software delivery planning with the other three capabilities of Install and distribute, and the domain's first paragraph says so."
SRC = '- .garura/product/product-os/software-delivery-planning/domain.md: "' + D + '"'
OUT1 = "**Outcome:** A team gets Garura into its project, upgrades it knowing what changes, and uses it on whichever coding tool it has."
OUT2 = OUT1 + " Once Garura is in, the project is set up from the team's own answers, with its own memory, its review rules and its tracker's work-item types, and the team can take Garura out again, keeping its work and its own files."
PROOF = "- After the set-up, the project's own memory and its review hold only what the team's answers call for."
PAGES = {
 "intents/bi-7.md": {"sub": [(OUT1, OUT2)], "add": [("- Each tool gets what it supports.", PROOF)]},
 "software-delivery-planning/domain.md": {"sub": [("where the product owner allows it. It does not release the work or run the product.", "where the product owner allows it. " + D + " It does not release the work or run the product.")], "add": []},
 "software-delivery-planning/install-into-project/capability.md": {"sub": [("For now it sits in software delivery planning, beside Initialize; the domain of Install and distribute is settled once all its capabilities are drafted.", NEWSIT)], "add": "LAST"},
 "software-delivery-planning/upgrade-project/capability.md": {"sub": [("For now it sits in software delivery planning, beside Install into a project and Initialize; the domain of Install and distribute is settled once all its capabilities are drafted.", NEWSIT)], "add": "LAST"},
 "software-delivery-planning/support-coding-tools/capability.md": {"sub": [("For now it sits in software delivery planning, beside Install into a project, Upgrade a project and Initialize; the domain of Install and distribute is settled once all its capabilities are drafted.", NEWSIT)], "add": "LAST"},
 "software-delivery-planning/initialize/capability.md": {"sub": [("For now it sits in software delivery planning, beside Install into a project, Upgrade a project and Support each coding tool; the domain of Install and distribute is settled once all its capabilities are drafted.", NEWSIT)], "add": "LAST"},
}
pages = []; n = 0
for rel, ops in PAGES.items():
    text = open(os.path.join(root, rel), encoding="utf-8").read()
    lines = text.split("\n"); new = list(lines); changes = []
    for o, nw in ops["sub"]:
        hit = [i for i, l in enumerate(lines) if o in l]
        assert len(hit) == 1, (rel, o[:60], len(hit))
        i = hit[0]; assert lines.count(lines[i]) == 1
        new[i] = lines[i].replace(o, nw); changes.append({"old": lines[i], "new": new[i]})
    adds = ops["add"]
    if adds == "LAST":
        last = [l for l in lines if l.strip()][-1]
        assert last.startswith("- Shelf:") and lines.count(last) == 1, rel
        adds = [(last, SRC)]
    for a, b in adds:
        assert lines.count(a) == 1, (rel, a)
        j = new.index(a if a not in [c["old"] for c in changes] else None)
        new.insert(j + 1, b); changes.append({"after": a, "add": b})
    n += len(changes); pages.append({"page": rel, "changes": changes})
    p = os.path.join(copy, rel); open(p, "w", encoding="utf-8").write("\n".join(new))
req = {"by": "product-os-keeper, for #1021 (reorganise the business intents): BI-7 (Install and distribute) close",
       "source": "The product owner's approval of 2026-11-10, reply \"approved\", recorded in .garura/project/issues/1021/context/bi-7-close/approval.md, of the proposal in .garura/project/issues/1021/context/bi-7-close/proposal.md: one sentence added to BI-7's Outcome and one Proof line; one sentence added to the domain page's first paragraph, as the four capabilities of Install and distribute stay in software delivery planning; the domain lines on those four capability pages, each with one Sources line quoting the domain page.",
       "pages": pages}
json.dump(req, open(out, "w"), ensure_ascii=False, indent=1)
print("pages", len(pages), "changes", n)
