"""Build BI-8's close request (sections 1, 2, 3 and 5 of the proposal) and a tested copy.

Run from the repo root: python3 build_lines_request.py <model root> <copy root> <request out>.
The copy root holds a copy of the model; the changed pages are written there for checking.
"""
import json, os, sys
root, copy, out = sys.argv[1], sys.argv[2], sys.argv[3]
D = "It also lands every change the same way, with an outside review and a person's yes, and gives people one tool to review what agents made."
SRC = '- .garura/product/product-os/software-delivery-planning/domain.md: "' + D + '"'
OUT_OLD = "People judge what agents made at the level of the outcome, reviewing ADRs, memories, domains, capabilities and ICE in tools that ship with Garura. Argus comes first."
OUT_NEW = ("People judge what agents made at the level of the outcome, reviewing business intents, ADRs, memories, domains, capabilities, ICE and agent decisions in tools that ship with Garura. Argus comes first."
           " Every change goes from opening to merge through the same steps, with an outside review and a person's yes.")
WHY_OLD = "**Why:** Agents now make more in one run than a pull request can show."
WHY_NEW = WHY_OLD + " Every change must also land the same way, so each one can be traced from its issue to its merge."
PROOF = "- Every change that lands went through the same steps, and none merged without the outside review's approval and a person's yes."
OUT3_OLD = "- Out: opening the branch, committing, reviewing and landing the change. Ship every change the same way, in Developer tooling, owns them."
OUT3_NEW = ("- Out: opening the branch, committing and landing the change, and reviewing it. Ship every change the same way, in Developer tooling, owns the first three,"
            " and Check the code against its standards, in Code → Validation, reviews the change.")
S = "software-delivery-planning"
PAGES = {
 "intents/bi-8.md": {"sub": [(OUT_OLD, OUT_NEW), (WHY_OLD, WHY_NEW)], "add": [("- Their answers become part of the work.", PROOF)]},
 f"{S}/domain.md": {"sub": [("and serves whichever coding tool the team works in. It does not release the work or run the product.",
                             "and serves whichever coding tool the team works in. " + D + " It does not release the work or run the product.")], "add": []},
 f"{S}/ship-every-change/capability.md": {"sub": [("It sits in software delivery planning for now; where Developer tooling sits is settled when its two capabilities are drafted.",
                                                   "It sits in software delivery planning with Review what agents make (Argus), and the domain's first paragraph says so.")], "add": "LAST"},
 f"{S}/review-agent-work/capability.md": {"sub": [("It sits in software delivery planning for now; its domain is settled at BI-8's close.",
                                                   "It sits in software delivery planning with Ship every change the same way, and the domain's first paragraph says so.")], "add": "LAST"},
 f"{S}/build-work-test-first/capability.md": {"sub": [(OUT3_OLD, OUT3_NEW)], "add": []},
 f"{S}/fix-defects-test-first/capability.md": {"sub": [(OUT3_OLD, OUT3_NEW)], "add": []},
 f"{S}/fix-defects-test-first/fn-fix-defect-code/feature.md": {"sub": [(
     "- Committing, reviewing and landing the change. Ship every change the same way does them.",
     "- Committing, reviewing and landing the change. Ship every change the same way commits and lands it, and Check the code against its standards reviews it.")], "add": []},
}
pages = []; n = 0
for rel, ops in PAGES.items():
    text = open(os.path.join(root, rel), encoding="utf-8").read()
    lines = text.split("\n"); new = list(lines); changes = []
    for o, nw in ops["sub"]:
        hit = [i for i, l in enumerate(lines) if o in l]
        assert len(hit) == 1, (rel, o[:60], len(hit))
        i = hit[0]; assert lines.count(lines[i]) == 1 and lines[i].count(o) == 1
        new[i] = lines[i].replace(o, nw); changes.append({"old": lines[i], "new": new[i]})
    adds = ops["add"]
    if adds == "LAST":
        last = [l for l in lines if l.strip()][-1]
        assert last.startswith("- Shelf:") and lines.count(last) == 1, rel
        adds = [(last, SRC)]
    for a, b in adds:
        assert lines.count(a) == 1, (rel, a)
        j = new.index(a)
        new.insert(j + 1, b); changes.append({"after": a, "add": b})
    n += len(changes); pages.append({"page": rel, "changes": changes})
    open(os.path.join(copy, rel), "w", encoding="utf-8").write("\n".join(new))
req = {"by": "product-os-keeper, for #1021 (reorganise the business intents): BI-8 (Developer tooling) close",
       "source": "The product owner's approval of 2026-11-10, reply \"Self-review is supposed to be a configuration. rest yes apply\", recorded in .garura/project/issues/1021/context/bi-8-close/approval.md, of sections 1, 2, 3 and 5 of the proposal in .garura/project/issues/1021/context/bi-8-close/proposal.md: BI-8's Outcome widened to the agreed capability line with one sentence added, one sentence added to its Why and one Proof line; one sentence added to the domain page's first paragraph, as both capabilities of Developer tooling stay in software delivery planning; the domain sentence on those two capability pages, each with one Sources line quoting the domain page; and the three lines of Build the work test first and Fix defects test first that gave the review of a change to Ship every change the same way. Section 4 is held.",
       "pages": pages}
json.dump(req, open(out, "w"), ensure_ascii=False, indent=1)
print("pages", len(pages), "changes", n)
