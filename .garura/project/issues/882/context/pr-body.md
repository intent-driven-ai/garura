The product model now holds the initialize capability. It says what `initialize` does for a project, and it records the three items the product owner asked for.

Closes #882. Closes #887. Serves #862 (initialize a project for Garura).

## What changes

- **A new capability, "Initialize a project for Garura"**, in the software-delivery-planning domain, with six features:
  - Ask the setup questions
  - Build the project's memory
  - Choose the review rule groups
  - Set up the tracker's work-item types (#881)
  - Give each project its own memory blocks (#883)
  - Run initialize again
- **The memory rule, as the product owner set it.** The Phoenix install lays Phoenix memory once on each machine. The Garura install lays only the pieces, no memory. `initialize` asks the questions and sets up each project's Garura memory, and it can run again to take in changes.
- **Garura memory is never a copy of a Phoenix file (ADR 039, decision 4).** Initialize builds the project's memory only from the part of Phoenix memory the project needs, down to the part of a file. A memory block is the part of Phoenix memory that one answer selects.
- **Three quality needs, each at medium.** Reliability: a second run with the same answers changes nothing. Security: nothing is written to the tracker before a typed yes. Maintainability: a new tracker is added in one place, with no play changed.
- **One accepted decision.** The product's security level moves from none to medium, because `initialize` writes to the tracker (`dec-cap-initialize-security-none-medium`). It was accepted by the product owner through `/record-decision`.
- **Bug #887 fixed.** `/discover-capabilities` dropped the capability's `slug` when it wrote the spine. The save script now keeps the slug the enrich step gives, and never changes a slug that is already set. A test is added.

## Review round 1 (rejected) and what round 2 fixed

- PM-1 (raised to P1 by the product owner): the pages copied whole Phoenix files. Fixed as above.
- PM-2: the capability had no `slug`. Fixed through the script fix (#887).
- PM-5: the decision did not show who accepted it. Fixed through `/record-decision`.
- PM-6: the #881 page answered for how other plays behave. Now a later story owns that.
- PM-7: Business Intent is named as the one product-layer issue type.

## Review round 2 (rejected) and what round 3 fixed

- NP-1: a "part" could be all of a file's sections, which is the whole file. The product owner's rule: "never take the whole file. read it, and build project's memory." Initialize reads a Phoenix file through the memory tool and builds the project's own memory from what it read, even when every section is relevant; it never copies the file.
- NP-2: the tracker-types page quotes ADR 048 word for word.
- NP-4: the accepted decision drops its "pending" and "if rejected" wording.
- Filed from the review: #888 (the plays push with no scan for client, company or personal references), #889 (the review halts on a PR with more than 300 files; this round's context came from GitHub's paged file list), #890 (the review's path table treats scripts in plays and skills as prose).

## Still open (named on the pages)

- #862 has no intent page in the model yet, so the capability links to no intent.
- No committed home yet for the setup-answer records ("product profile" on the pages).
- ADR 038 still says the tool downloads Phoenix memory on first use; the amendment is planned next.

## Checks

| Check | Result |
|---|---|
| Shape check (`lint_grounding.py`) | no error on any initialize page (70 old errors elsewhere stay) |
| Source check | ok |
| Content judge (settled gate, #884) | 7 / 7 pages pass, 0 notes |
| Write guard | ok, only model paths changed |
| Decision lint and business-intent guard | clean; no business intent changes |
| `persist_understand.py` tests | 98 pass |
| Hidden checks for #887 | 6 / 6 pass |
| Product owner checkpoints | approved ("yes" in rounds 1, 2 and 3; "accept" on the decision) |

Lands on `plan/788/base`.
