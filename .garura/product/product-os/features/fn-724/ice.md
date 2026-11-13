## Intent
- Goal: Each part, and each ICE, gets one answer each time it is asked, ready, partly ready or not ready, with what stops it and the gaps that do not, from the index, the ICE pages and the intent pages only, so the same model always gives the same answer; a missing domain, a thin ICE and a part found on its own never stop work, a feature is read through its capability, and a need that was not checked is named.
- Limit: The check reads files only, stores no answer, and stops work, never a write.
- Limit: Every copy of the check is the same file, so every play gives the same answer.
- Limit: A part found on its own is not a gap, and a feature's own needs are not read.
- Fails if: The same model gives two different answers, or two copies of the check disagree.
- Fails if: A part with no confirmed intent, or with a need not done, reads ready.
- Fails if: Work on a part stops only because the model is incomplete: a missing domain, a missing "identified by", or an ICE kept in an older shape.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the ontology's ready rules for a capability, a feature and an ICE, the index and its ICE list, the ICE pages and their thin marks, the intent pages' stage lines, the done list, the four copies of the check and their tests, and the open points on the check: saying when needs were not checked, and reading older parts whose ICE is still inside their page.
- Never read: any memory file by its path, any ICE page, and any file in a plan's evals folder.
- Persona: the developer, a person or an AI agent who builds the code, who starts work only on a part that can start; and the technical lead, who reads the gaps.
- Scope: In: the three answers, what stops a part, its gaps, the done list, the exit codes, and the copies kept the same. Out: the links themselves, the gap rule in the ontology, approval, and choosing what to work on next.

## Expectation
- Scenario: In a clinic's booking app, Booking has no domain, serves the confirmed intent "patients book online" and has a full ICE; the check reads it partly ready with the gap "has no domain yet", and work starts. In a shop's checkout service, Refunds needs Payments; with a done list that does not hold Payments it reads not ready and names Payments, and with no done list it reads partly ready with the gap "needs not checked".
- Done means: Someone other than the one who ran it runs the check twice on the same model and gets the same answers, compares the four copies and finds them the same, and finds the clinic's Booking partly ready with only the domain gap, the shop's Refunds not ready naming Payments with the done list and partly ready naming "needs not checked" without it, and no part kept from ready by a missing "identified by".
