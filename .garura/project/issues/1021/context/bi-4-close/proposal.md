# BI-4 close: the proposal shown to the product owner (draft, not applied)

2026-11-10. BI-4 (Code → Validation) has its six capabilities in the model. This is the close, as for BI-3: BI-4's page reworded, the domain's last sentence changed, and the approved pages that BI-4's decisions put out of step brought in line. Nothing is applied before the product owner's yes.

## 1. BI-4's page (`.garura/product/product-os/intents/bi-4.md`)

- Outcome, old: Code is proven to do what the spec asked, by evals its builder never sees, and every change lands the same way.
- Outcome, new: Built code is proven from outside before it moves on: what the product does is tested by evals its builder never sees; its security, performance, accessibility and user experience on each surface are tested in the testing environment against the levels and designs set before the build; and every change and the whole built work are checked against the project's standards.
- Why: kept as it is.
- Proof, kept: Every expected result has a pass or fail from an eval the builder never saw.
- Proof, old: Every change lands reviewed, and a person approves the merge.
- Proof, new (two lines in its place):
  - Every level the product profile sets, and each surface and screen design, has a pass, a fail or a reason it was not tested, from tests run in the testing environment, never in production.
  - Every change is checked against the project's standards, by a part that is not its builder, before it is merged.
- Must not, old: Let a builder grade itself, weaken a check to pass, or merge without a person.
- Must not, new: Let a builder grade itself, weaken a check to pass, or count a check that did not run as a pass.
- Stage, tracker and the 29 Touches lines: kept.

## 2. The domain page (`.garura/product/product-os/software-delivery-planning/domain.md`), last sentence of the first paragraph

- Old: It does not run the evals, release the work, or run the product.
- New: It then tests the built work from outside the builder, by its evals and against the levels, surfaces, designs and standards set before the build. It does not release the work or run the product.

## 3. Lines on approved pages brought in line

a. BI-4's Must not is quoted word for word in the Sources of 22 pages (the six BI-4 capabilities and their features). Each quote is changed to the new wording.

b. "Validate its own code", the name the product owner replaced, still names the capability on 2 BI-3 lines:
- build-work-test-first/capability.md: "Out: checking the code against the project's standards. Check the code against its standards, in Code → Validation, owns it; the build follows the standards while it writes."
- build-work-test-first/fn-build-code-to-pass/feature.md: "Checking the code against the project's standards. Check the code against its standards, in Code → Validation, does it."
- The first line is quoted on 5 pages (Test security, and Check the code against its standards with two of its features); each quote follows, and the capability page's sentence "hands the check here by its old name" loses "by its old name".

c. Testing owners named as they were before BI-3 and BI-4 (security, functional and performance testing under Validation → Run; "Design for evaluation and testing", a capability BI-3 replaced with Write the evals that check the work):
- deployment-design/capability.md: "Out: writing and running the tests. Code → Validation tests the built work: what the product does by its evals, its security, performance, accessibility and the user experience on each surface, and the code against its standards. Validation → Run owns the other testing before user acceptance and user acceptance testing itself. Write the evals that check the work writes each slice's eval. This capability says which tests run in which environment and what a change must pass to move on."
- deployment-design/fn-design-how-project-runs/feature.md: "Writing and running the tests. The testing capabilities of Code → Validation and Validation → Run own them, and Write the evals that check the work writes each slice's eval."
- environment-setup/capability.md: "Out: writing and running the tests. The testing capabilities of Code → Validation and Validation → Run own them, and Write the evals that check the work writes each slice's eval."
- manage-surfaces/capability.md, its sentence "Design for evaluation and testing owns the eval of each slice and the step library of each kind of surface." becomes "Write the evals that check the work owns the eval of each slice and the step library of each kind of surface, and Test the user experience on each surface tests each surface against its properties and guidelines." The old sentence is quoted on 2 write-work-evals pages; each quote follows.
- manage-surfaces/fn-declare-surfaces/feature.md: "The step library of each kind of surface and the eval of each slice. Write the evals that check the work owns them."

## 4. Left as they are

- The older name "Test with evals the builder never sees" on about 12 pages: the new name, "Test what the product does, with evals the builder never sees", holds it, so each reference can still be found.
- BI-5's page (Validation → Run) still lists security, automated functional and performance testing in its outcome: left for BI-5's review, which is next.
