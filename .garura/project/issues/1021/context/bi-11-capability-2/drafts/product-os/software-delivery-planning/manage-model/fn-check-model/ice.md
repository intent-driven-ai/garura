## Intent
- Goal: On every change that writes the model, one shared structure check reads its pages and its index for their shape and their links, and lists each finding with its page and what is wrong, so a broken page, a page with no entry, an entry with no page or an ICE with an empty part is seen in the change that made it; it reads the ICE on its own page as the ontology says, and a finding is fixed later and never stops work.
- Limit: The check judges shape and links only, never what a page means.
- Limit: It reads files only, and every copy is the same file.
- Limit: A finding never stops work or a write, and a thin part is never an error.
- Fails if: A page with a missing section, an entry with no page, or an ICE with an empty part passes with no finding.
- Fails if: The check asks for an ICE section on a part whose ICE is on its own page.
- Fails if: A play stops a person's work on a finding with no way past that records what is owed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the page templates and the content standard each kind follows, the ontology's rule that the ICE has its own page, the index and its ICE list, the 13 copies of the check and the plays that run it, its last run on the model, /shape-slice's model check, and the open issues on it (#870, #1033).
- Never read: any memory file by its path, any ICE page, and any file in a plan's evals folder.
- Persona: the technical lead, who reads the findings of a change; and the developer, a person or an AI agent who builds the code, who fixes what the check names.
- Scope: In: the shape and link checks of pages, index entries and ICE entries, their findings, the copies kept the same, and the plays that run them. Out: the page judge, the rebuild eval, the ontology change step, the ready answer, loose parts and duplicates, and reviewing a change.

## Expectation
- Scenario: In a shop's checkout service, a change adds a feature page with no Acceptance criteria section and an ICE page with its three parts; the check names the missing section as a finding, gives no warning for an ICE section on the feature page, and the change goes on with the fix listed as owed. In a bank's payments service, an old capability page is left on disk with no entry after a rename, and the check names it.
- Done means: Someone other than the one who made the change runs the check on the model and reads its report, and finds the shop's missing section named, no ICE-section warning for a part whose ICE is on its own page, the change not stopped and the fix listed as owed, the bank's orphan page named, and every copy of the check the same file.
