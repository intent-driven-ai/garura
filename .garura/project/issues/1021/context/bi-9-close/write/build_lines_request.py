"""Build BI-9's close request (sections 2 and 3 of the proposal).

Run from the repo root: python3 build_lines_request.py. Writes lines-request.json beside this file.
"""
import json, os
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
root = ".garura/product/product-os"
D = ("It also orchestrates the work: it chooses and orders what runs next, runs plays as loops, tracks the work in the team's tracker,"
     " records each decision on how the project is built as an ADR, and gives every gate a way past.")
SRC = '- .garura/product/product-os/software-delivery-planning/domain.md: "' + D + '"'
NEW = "It sits in software delivery planning with the other capabilities of Orchestration, and the domain's first paragraph says so."
S = "software-delivery-planning"
OLD45 = ("It sits in software delivery planning with the other capabilities of Orchestration. The domain's first paragraph does not name"
         " Orchestration yet; widening it is owed at this intent's close.")
PAGES = {
 f"{S}/domain.md": {"sub": [("and gives people one tool to review what agents made. It does not release the work or run the product.",
                             "and gives people one tool to review what agents made. " + D + " It does not release the work or run the product.")], "add": []},
 f"{S}/orchestrate-agent-work/capability.md": {"sub": [("It sits in software delivery planning for now. The domain's first paragraph does not yet say that"
     " the domain also runs the work; that is owed at the close of Orchestration.", NEW)], "add": "LAST"},
 f"{S}/run-plays-as-loops/capability.md": {"sub": [("It sits in software delivery planning. The domain's opening does not say yet that the domain"
     " runs its work in loops; that line is owed at BI-9's close.", NEW)], "add": "LAST"},
 f"{S}/track-execution/capability.md": {"sub": [("It sits in software delivery planning for now; the domain's first paragraph is widened at"
     " BI-9's close.", NEW)], "add": "LAST"},
 f"{S}/manage-adrs/capability.md": {"sub": [(OLD45, NEW)], "add": "LAST"},
 f"{S}/give-every-gate-a-way-past/capability.md": {"sub": [(OLD45, NEW)], "add": "LAST"},
}
pages = []; n = 0
for rel, ops in PAGES.items():
    lines = open(os.path.join(root, rel), encoding="utf-8").read().split("\n"); changes = []
    for o, nw in ops["sub"]:
        hit = [i for i, l in enumerate(lines) if o in l]
        assert len(hit) == 1, (rel, o[:60], len(hit))
        i = hit[0]; assert lines.count(lines[i]) == 1 and lines[i].count(o) == 1
        changes.append({"old": lines[i], "new": lines[i].replace(o, nw)})
    if ops["add"] == "LAST":
        last = [l for l in lines if l.strip()][-1]
        assert last.startswith("- Shelf:") and lines.count(last) == 1, rel
        changes.append({"after": last, "add": SRC})
    n += len(changes); pages.append({"page": rel, "changes": changes})
req = {"by": "product-os-keeper, for #1021 (reorganise the business intents): BI-9 (Orchestration) close",
       "source": "The product owner's approval of 2026-11-11, reply \"approved\", recorded in .garura/project/issues/1021/context/bi-9-close/approval.md, of the proposal in .garura/project/issues/1021/context/bi-9-close/proposal.md: one sentence added to the domain page's first paragraph, as the five capabilities of Orchestration stay in software delivery planning; and the domain sentence on those five capability pages, each with one Sources line quoting the domain page. BI-9's page is kept as it is.",
       "pages": pages}
json.dump(req, open(os.path.join(HERE, "lines-request.json"), "w"), ensure_ascii=False, indent=1)
print("pages", len(pages), "changes", n)
