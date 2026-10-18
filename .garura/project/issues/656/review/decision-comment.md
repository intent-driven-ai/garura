Harness verdict (gate off per gates.plays.review-change): reject

**Why reject.** One P1 finding, and the rule decides it, not a person. Rule DATA-18 fires on the word "email" and asks for proof of encryption. The line is `core/tools/memory/test_pull.py:44`: `git(self.phoenix, "config", "user.email", "t@example.com")`. It sets the author of a throwaway git repository in a temp folder, with a placeholder address. No real personal data is stored or sent. The newer copy of the rules flags the same line, so this is not caused by the old copy.

**What was reviewed.** Six kinds of change, sorted from the diff: memory (41 files, the removal of personal names), code (4: `pull.py`, `install.py`, `check_contract.py`, `pageindex.py`), tests (1), config (1), plans (2), run records (11). Memory is the only design-bearing kind; it was checked against committed sources (the knowledge template and design note, the ADR template, ADR 035 and 036).

**Checks run.**
- `test_pull.py`: 12 of 12 pass. `test_check_contract.py`: 49 pass. `check_contract.py`: ok.
- ruff on the five Python files: clean. `git diff --check`: clean.
- Both plans: valid. 36 knowledge files: structure, ids and links fine.
- No client, company, personal-vault or home-folder text in the added lines.

**Where the rules came from (the test Kapil asked for).** The PR severity rules were read from Garura memory, `./.garura/core/memory/standards/rules/pr.md`, as now configured. That copy is from 30 May and has no section that skips prose, so memory notes were scanned as if they were code. Most of the 168 findings are that noise (P1 1, P2 57, P3 50, P4 60). The review guides were not in Garura memory, so they were read from Phoenix memory, in tier order.

**Memory edits — no blocker, 9 small findings (6 P3, 3 P4).** The scrub keeps every matching field and rule unchanged. The defects are in how names were replaced, for example:
- `standards/templates/adr.md:154` and `standards/schemas/product-os/ontology.md:138` now say "the owner" in fields that must hold a real person.
- "the owner" is a new, undefined term, used six ways; three sentences start in lower case.
- `standards/rules/no-unbacked-recommendation.md:7` quotes "the owner" as its authority.

**Routing.** A harness reject stands as a human reject would: fix the cited finding and re-raise. `review-pr.bypass` is `true` in config, so this reject does not by itself block the merge. Full record: `.garura/project/issues/656/review/findings.yaml`.
