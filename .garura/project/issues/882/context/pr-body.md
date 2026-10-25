The product model now holds the initialize capability. It says what `initialize` does for a project, and it records the three items the product owner asked for.

Closes #882. Serves #862 (initialize a project for Garura).

## What changes

- **A new capability, "Initialize a project for Garura"**, in the software-delivery-planning domain, with six features:
  - Ask the setup questions
  - Build the project's memory
  - Choose the review rule groups
  - Set up the tracker's work-item types (#881)
  - Give each project its own memory blocks (#883)
  - Run initialize again
- **The memory rule, as the product owner set it.** The Phoenix install lays Phoenix memory once on each machine. The Garura install lays only the pieces, no memory. `initialize` asks the questions and sets up each project's Garura memory, and it can run again to take in changes.
- **Three quality needs, each at medium.** Reliability: a second run with the same answers changes nothing. Security: nothing is written to the tracker before a typed yes. Maintainability: a new tracker is added in one place, with no play changed.
- **One decision.** The product's security level moves from none to medium, because `initialize` writes to the tracker (`dec-cap-initialize-security-none-medium`).

## Still open (named on the pages)

- #862 has no intent page in the model yet, so the capability links to no intent.
- No source lists every review rule group.
- Garura's own answer to "does it have permissions?" is not recorded.

## Checks

| Check | Result |
|---|---|
| Shape check (`lint_grounding.py`) | clean |
| Source check (every quote is in #862, #881, #883 or the seed answers) | ok |
| Content judge (settled gate, #884) | 7 / 7 pages pass, 0 notes |
| Write guard | ok, only model paths changed |
| Spine lint | clean |
| Product owner checkpoint | approved ("yes", 2026-10-25) |
| Self-review | 0 blocking findings |

Lands on `plan/788/base`.
