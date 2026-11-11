"""Build section 4 of BI-8's close (BI-4's three lines that name the dropped self-review) and a tested copy.

Run from the repo root: python3 build_lines_request_s4.py <model root> <copy root> <request out>.
"""
import json, os, sys
root, copy, out = sys.argv[1], sys.argv[2], sys.argv[3]
S = "software-delivery-planning/check-code-against-standards"
PAGES = {
 f"{S}/capability.md": [
  ("Opening the branch, committing, raising the change with its self-review, and merging it with a person's yes stay with",
   "Opening the branch, committing, raising the change and merging it with a person's yes stay with"),
  ("- Out: opening the branch, committing, raising the change with its self-review, and merging it with a person's yes.",
   "- Out: opening the branch, committing, raising the change and merging it with a person's yes.")],
 f"{S}/fn-review-each-change/feature.md": [
  ("- Raising the change, its self-review, and merging it with a person's yes. Ship every change the same way, in Developer tooling, does them.",
   "- Raising the change and merging it with a person's yes. Ship every change the same way, in Developer tooling, does them.")],
}
pages = []; n = 0
for rel, subs in PAGES.items():
    lines = open(os.path.join(root, rel), encoding="utf-8").read().split("\n"); new = list(lines); changes = []
    for o, nw in subs:
        hit = [i for i, l in enumerate(lines) if o in l]
        assert len(hit) == 1, (rel, o[:60], len(hit))
        i = hit[0]; assert lines.count(lines[i]) == 1 and lines[i].count(o) == 1
        new[i] = lines[i].replace(o, nw); changes.append({"old": lines[i], "new": new[i]})
    n += len(changes); pages.append({"page": rel, "changes": changes})
    open(os.path.join(copy, rel), "w", encoding="utf-8").write("\n".join(new))
req = {"by": "product-os-keeper, for #1021 (reorganise the business intents): BI-8 (Developer tooling) close, section 4",
       "source": "The product owner's choice of 2026-11-10, \"Let's go with dropped.\", recorded in .garura/project/issues/1021/context/bi-8-close/approval.md, which releases section 4 of the proposal in .garura/project/issues/1021/context/bi-8-close/proposal.md: BI-4's three lines that name the self-review he dropped on 2026-11-10 (\"yes, record it with self-review dropped\") lose those words, the rest of each line kept.",
       "pages": pages}
json.dump(req, open(out, "w"), ensure_ascii=False, indent=1)
print("pages", len(pages), "changes", n)
