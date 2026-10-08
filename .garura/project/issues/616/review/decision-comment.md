**Harness verdict (gate off per gates.plays.review-change): APPROVE — after two rounds**

- **Round 1:** 12 findings (1 P2). Fixed: the enrich skill now writes a seeded capability's first `capability.md`; `/understand` asks for the seed *before* opening any change (no orphan issue or branch on a stop); the persist refuses a seed not marked `answered_by: human`, a malformed file, or a bad doc path; sibling-containment is now tested; edit notes removed; `pipeline-position.md` lists each play's real position. Recorded as a follow-up, not fixed here: skipping the opening inside a drive (#614 / #615).
- **Round 2:** all 12 confirmed; 3 new (1 P2). Fixed: a seed's doc folder comes from the domain's own doc (ids like `dom-commerce` live in `commerce/`), seed fields must be text, and the enrich skill's step 1 reads cleanly.

Final checks: play lint PASS on `/vision` and `/understand`; each `reference/ice.md` matches its fingerprint; persist tests 39/39; ruff clean on changed files; component lint unchanged (113).
