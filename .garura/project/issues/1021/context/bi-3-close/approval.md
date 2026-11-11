# Approval, BI-3's page and the domain page reworded (BI-3 close)

- 2026-11-09, the product owner saw the full diff of BI-3's page (Outcome, Why, Proof, Must not) and of the domain page's first paragraph, with the domain's name and folder kept, and replied: "ok".

BI-3's page, the four lines approved:
- Outcome: The work under any item a person names from the plan becomes working code: it is designed against the project's standards, its evals are written before it is built, and it is built test first by a builder who never sees the tests. Defects are fixed the same way, quickly.
- Why: Left alone, agents build from a guess and check their own work, so a pass proves nothing.
- Proof it is met: The work is designed before it is coded, against the project's standards. / Every expected result has a test that was written and shown to fail before its code. / The builder never sees a test or an eval.
- Must not: Tell the builder the steps, or show the builder the tests.

The domain page's first paragraph, approved:
This domain turns a business intent into working code that a check from the outside can prove. It serves the product owner, who names the work, the technical lead, who designs it, and the developer, who builds it. It specifies the product, sets the project's design, and builds the work test first. It writes the eval that says if the work is met before the work is built, and it never gives a builder the eval or the tests: a check flags each build session that read them. It does not run the evals, release the work, or run the product.

- 2026-11-09, after the write, the check named a clash: BI-3's outcome said "Defects are fixed the same way, quickly", while the approved fix pages say a fix never goes through the full design. The product owner saw the fix and replied: "yes, commit and cp". The outcome's last sentence becomes: "Defects are fixed test first too, quickly and without a full design." The four BI-2 lines that say the domain "prepares the work before agents build it" are left as they are, by his rule of not looping on small points.
