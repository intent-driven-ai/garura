Reviewer verdict (Kapil, gate on for this run): approve

**What was reviewed (round 2).** 71 changed files in seven kinds: memory (42), code (4), tests (1), config (1), plans (2), run records (11), review records (10). Memory was checked against committed sources (main, ADR 031, 035 and 036, the templates as they are on main).

**Round-1 findings.** All nine memory wording findings (MEM-01 to MEM-09) are resolved by `218a2d54`; the same fixes are in Phoenix memory (`5fcd88e`).

**The one P1.** Rule DATA-18 on `core/tools/memory/test_pull.py:46`: the demo address `t@example.com` for a throwaway test repository. Kapil approved it as an exception: "these are demos emails, and part of tool that is using this as sample data. this is exception that is approved". A comment at the line records it (`9bbada8a`). The machine recommendation was reject on this P1 alone; the reviewer decided approve.

**Left as notes (P4, not blocking).**
- MEM-10: the "no names in memory" rule sits only in `knowledge/_TEMPLATE.md`, and "memory is shared across projects" holds for Phoenix memory, not Garura memory.
- MEM-11: "the team's position", "The person asked me" do not say who is meant; the delegation note is worded two ways.
- MEM-12: the ADR template's gold example copies ADR 031's header but names a made-up person.

**Checks.** `test_pull.py` 12/12; ontology checker 27/27; ruff clean. The PR rules were read from Garura memory's 30 May copy, as configured, so most of the 163 linter notes are prose read as code.

Full record: `.garura/project/issues/656/review/findings.yaml`.
