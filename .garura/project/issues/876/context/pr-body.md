An install into Garura's own repo now lays the plan play. The harness install keeps a fixed list of plays and skills. #818 built `/shape-plan` and its skill `author-work-items` but did not add them to that list, so after an install `/shape-plan` was not there.

Closes #876.

## What changes

- `install-garura/scripts/install.py`: the harness list names the play `shape-plan` and the skill `author-work-items`.
- `install-garura/scripts/test_install.py`: a test installs with the harness scope and finds both.

## Checks

| Check | Result |
|---|---|
| Hidden acceptance check (4), written before the fix | 4 / 4 pass (1 / 4 before) |
| Install tests | 75 pass |
| Component lint | no new error (36 old errors stay) |
| Self-review | 0 blocking findings |

## Self-review

See `.garura/project/issues/876/context/self-review.md`.
