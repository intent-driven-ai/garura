# Feature: Check what memory holds: pages out of date, sources that changed

## What it does
Before an agent uses a page of memory, a check names the page when it is out of date or its source changed, and every change to a project's memory shows in the review of the change that made it with the result of the memory checks, so agents decide only from memory people trust.
- What #942 (a project's memory can be managed) asks for, among its proofs:
  - "Every change to a project's memory shows in the review of the change that made it, with the result of the memory checks."
  - "A page that is out of date, or whose source changed, is named before an agent uses it."
- Today there is "No linters and no rubric for memory." Two memory index rows that were out of date were found by hand (#937, closed).
- What exists near it, and what it does not do:
  - each piece of text the memory tool returns carries a fingerprint, so an old answer can be seen as stale once its file changes;
  - the trace check reads again the sources of decisions already made, and names each step whose source changed;
  - neither names a page that is out of date before an agent first uses it.
- #942 (a project's memory can be managed) must not "change how agents look memory up (one memory tool, three tiers in order); let memory change without a person."
- Examples, in different kinds of project:
  - In a clinic's booking app, the page on how long a reset link lasts was written from a security rule that has since changed. The check names the page before the developer's agent uses it.
  - In a bank's payments service, a change adds a page to the project's Garura memory. The review of that change shows the page with the result of the memory checks.
  - In a game studio's build, an index page of memory still lists a page that was removed. The check names the row, and no one has to find it by hand.
- How it meets the capability: "people control what enters them" is not enough if a page that was right goes wrong later; the check keeps what is in memory as trusted as what enters it.

Status: not built (#942, a project's memory can be managed, a business intent recorded on 2026-10-28, not shaped and not approved to build).

## Inputs / Outputs
- In: the pages of a tier, with their sources where a page names them.
- In: a change to a project's memory, from the change that made it.
- Out: before use, the name of each page that is out of date or whose source changed, with why.
- Out: in the review of a change, the result of the memory checks on each page it changed.

## Rules & behavior
- A page out of date, or whose source changed, is named before an agent uses it. The reason: "A page that is out of date, or whose source changed, is named before an agent uses it."
- Every change to a project's memory shows in its review with the checks. The reason: "Every change to a project's memory shows in the review of the change that made it, with the result of the memory checks."
- The check does not change how agents look memory up. The reason: #942 (a project's memory can be managed) must not "change how agents look memory up (one memory tool, three tiers in order)".
- The check changes no memory by itself. The reason: #942 (a project's memory can be managed) must not "let memory change without a person."
- Not decided: what makes a page out of date: its age, a newer source, or a rule that replaced it.
- Not decided: whether an agent still reads a page the check names, with a warning, or waits until a person decides.

## Acceptance criteria
- Given a page whose source changed after it was written, when an agent is about to use it, then the check names the page and its source. This is not built.
- Given a change that adds or changes a page of a project's memory, when the change is reviewed, then the review shows the page with the result of the memory checks. This is not built.
- Given an index page of memory that lists a page that is gone, when the check runs, then it names the row. This is not built.

## Out of scope
- Checking the sources of a decision already made. Keep each decision's trace and check its sources (fn-keep-decision-trace) does it.
- The pages that differ between Phoenix memory and Garura's source. Keep Phoenix memory in step with Garura's source, versioned per release with its notes (fn-phoenix-in-step) does it.
- Reviewing a change against its standards. Check the code against its standards, in Code → Validation, owns it.
- Showing what memory holds to a person. Review what agents make (Argus), in Developer tooling, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 114, the list set on 2026-11-11: "people control what enters them"
- GitHub #942 (open), set by the product owner on 2026-10-28: "Every change to a project's memory shows in the review of the change that made it, with the result of the memory checks.", "A page that is out of date, or whose source changed, is named before an agent uses it.", "No linters and no rubric for memory.", and its Must not, "change how agents look memory up (one memory tool, three tiers in order); let memory change without a person."
- GitHub #937 (closed): two memory index rows out of date, found by hand.
- core/tools/memory/README.md, lines 166-168: a fingerprint, so that "When a file changes, an old citation's fingerprint no longer matches, so a stale answer can be seen."
- docs/adr/037-agent-decisions-keep-a-trace-and-the-review-tool-has-five-sections.md, section 2: the check reads every step's source again.
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, section 5.7.
