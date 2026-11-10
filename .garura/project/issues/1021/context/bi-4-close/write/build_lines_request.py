import json, os, sys
root = sys.argv[1]; copy = sys.argv[2]; out = sys.argv[3]
SUB = [
 ("Let a builder grade itself, weaken a check to pass, or merge without a person.",
  "Let a builder grade itself, weaken a check to pass, or count a check that did not run as a pass."),
 ("Validate its own code, in Code → Validation, owns it; the build follows the standards while it writes.",
  "Check the code against its standards, in Code → Validation, owns it; the build follows the standards while it writes."),
 ("Checking the code against the project's standards. Validate its own code, in Code → Validation, does it.",
  "Checking the code against the project's standards. Check the code against its standards, in Code → Validation, does it."),
 ("Build the work test first hands the check here by its old name:",
  "Build the work test first hands the check here:"),
 ("Design for evaluation and testing owns the eval of each slice and the step library of each kind of surface.",
  "Write the evals that check the work owns the eval of each slice and the step library of each kind of surface, and Test the user experience on each surface tests each surface against its properties and guidelines."),
 ("The step library of each kind of surface and the eval of each slice. Design for evaluation and testing owns them.",
  "The step library of each kind of surface and the eval of each slice. Write the evals that check the work owns them."),
 ("through Test with evals the builder never sees and Validate its own code.",
  "through Test with evals the builder never sees and Check the code against its standards."),
 ("It does not run the evals, release the work, or run the product.",
  "It then tests the built work from outside the builder, by its evals and against the levels, surfaces, designs and standards set before the build. It does not release the work or run the product."),
 ("**Outcome:** Code is proven to do what the spec asked, by evals its builder never sees, and every change lands the same way.",
  "**Outcome:** Built code is proven from outside before it moves on: what the product does is tested by evals its builder never sees; its security, performance, accessibility and user experience on each surface are tested in the testing environment against the levels and designs set before the build; and every change and the whole built work are checked against the project's standards."),
 ("- Every change lands reviewed, and a person approves the merge.",
  "- Every level the product profile sets, and each surface and screen design, has a pass, a fail or a reason it was not tested, from tests run in the testing environment, never in production."),
]
FULL = {
 "software-delivery-planning/deployment-design/capability.md": (
  "- Out: writing and running the tests. The testing capabilities of Validation → Run (security, automated functional, performance, other testing and user acceptance testing) and Test with evals the builder never sees (Code → Validation) own the tests, and Design for evaluation and testing designs each slice's eval. This capability says which tests run in which environment and what a change must pass to move on.",
  "- Out: writing and running the tests. Code → Validation tests the built work: what the product does by its evals, its security, performance, accessibility and the user experience on each surface, and the code against its standards. Validation → Run owns the other testing before user acceptance and user acceptance testing itself. Write the evals that check the work writes each slice's eval. This capability says which tests run in which environment and what a change must pass to move on."),
 "software-delivery-planning/deployment-design/fn-design-how-project-runs/feature.md": (
  "- Writing and running the tests. The testing capabilities, Test with evals the builder never sees, and Design for evaluation and testing own them.",
  "- Writing and running the tests. The testing capabilities of Code → Validation and Validation → Run own them, and Write the evals that check the work writes each slice's eval."),
 "software-delivery-planning/environment-setup/capability.md": (
  "- Out: writing and running the tests. The testing capabilities of Validation → Run, Test with evals the builder never sees (Code → Validation), and Design for evaluation and testing own them.",
  "- Out: writing and running the tests. The testing capabilities of Code → Validation and Validation → Run own them, and Write the evals that check the work writes each slice's eval."),
}
ADD = {"intents/bi-4.md": ("- Every change lands reviewed, and a person approves the merge.",
        "- Every change is checked against the project's standards, by a part that is not its builder, before it is merged.")}
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
        if rel in ADD:
            a, b = ADD[rel]; assert lines.count(a) == 1
            changes.append({"after": a, "add": b})
            j = newlines.index(ADD[rel][0].replace("- Every change lands reviewed, and a person approves the merge.", "- Every level the product profile sets, and each surface and screen design, has a pass, a fail or a reason it was not tested, from tests run in the testing environment, never in production."))
            newlines.insert(j + 1, b)
        if changes:
            pages.append({"page": rel, "changes": changes})
            cp = os.path.join(copy, rel); open(cp, "w", encoding="utf-8").write("\n".join(newlines))
req = {"by": "product-os-keeper, for #1021 (reorganise the business intents): BI-4 (Code → Validation) close",
       "source": "The product owner's approval of 2026-11-10, reply \"yes, apply and commit and cp\", recorded in .garura/project/issues/1021/context/bi-4-close/approval.md, of the proposal in .garura/project/issues/1021/context/bi-4-close/proposal.md: BI-4's Outcome, Proof it is met and Must not; the domain page's last sentence; the 22 quotes of BI-4's Must not; \"Validate its own code\" on 2 BI-3 lines with its quotes; the testing owners on 5 BI-2 lines with their quotes.",
       "pages": pages}
json.dump(req, open(out, "w"), ensure_ascii=False, indent=1)
print("pages", len(pages), "line changes", sum(len(p["changes"]) for p in pages), "full-line hits", full_hits)
for o, c in hits.items(): print(c, "x", o[:70])
