## Intent
- Goal: Every thing the agent found while it gathered a decision's context, that the brief did not ask about, reaches the person who accepts the ADR as a whole point in the section For the Person Who Accepts This, with what and where, what is wrong or worth knowing, why it matters, what this decision does and what the person decides, each with the detail itself; the play checks before it asks the person that the points were gathered, or that none were found, and that each is whole; and the person reads them before answering.
- Limit: A point gives the detail itself, the lines, the names and the dates, never a summary.
- Limit: A point is about something the brief did not ask about; the decision itself stays in the ADR's own sections.
- Limit: The person is not asked to accept while a point misses a part.
- Fails if: The person is asked to accept an ADR whose gathered points are missing, or that does not say none were found.
- Fails if: A point reaches the person without one of its five parts, or with a summary in place of the detail.
- Fails if: A finding is mentioned only in passing in the ADR's Context and not as a point.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the decision brief, what the agent read while it gathered the context and what it found there, the ADR template's section and its rule for a point, the gathered context's points, and the draft's section.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner or the technical lead, who accepts the ADR and was not in the work.
- Scope: In: gathering the points, writing them in the section, checking each point, checking that the points were gathered, and showing them before the answer. Out: the rest of the draft and its checks, the person's answer, the template as a standard and the templates index, and acting on a point.

## Expectation
- Scenario: In a shop's checkout service, the technical lead records a decision on how long carts are kept. While gathering the context, the agent finds that the privacy page still says seven days. The draft's section holds one point: the page and its line, that the decision makes it thirty days, that customers would read the wrong time, that the decision does not change the page, and that the person decides whether it changes in the same change. The play checks that the point is whole before it shows the draft, and the product owner reads it before typing accept. In a hospital's appointment system, a draft whose point leaves out what the person decides is sent back to the skill before anyone is asked.
- Done means: Someone other than the one who drafted it reads the gathered context, the draft and the check report, and finds every point of the context in the draft's section with its five parts and its detail, the play's check of the points on record before the person was asked, and, for the hospital's draft, the check naming the missing part and no question asked of the person until it was fixed.
