Reviewer verdict (human, gate on): reject — fix HA1, MC1 and HC1 in this PR, then raise again

PR #832, round 1. Recommended verdict: reject (1 P1). The P1 (SEC-07, `JSON.parse` of the linter's own output in a test) is a false positive.

To fix in this PR:
- HA1: the edit-ontology change (the agent loads the asking-a-person rule and hands it to the skill) is a flow change. Put it in the play's ICE source (`reference/ice.md`) through /edit-play, so a rebuild keeps it.
- MC1: remove Tether / Orbit / Vanish from the files outside the templates (glossary, fix-bug and refactor-code plays, agents, rules, skills, docs). ADRs stay as written: they record past decisions.
- HC1: one main copy of `lint_grounding.py`, and a check that every play's copy matches it.

Follow-ups unchanged: HB1 and HB2 are handled by #831.
