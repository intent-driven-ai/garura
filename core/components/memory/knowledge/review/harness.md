---
id: review/harness
title: "Reviewing harness code (plays, skills, agents, grounding)"
conditions:
  recognises: "the PR changes the MD-defined 'code' of the agentic system"
  signals: ["core/components/plays/**", "core/components/skills/**", "core/components/agents/**", "core/grounding/**", ".claude/skills/**", ".claude/agents/**", ".agents/skills/**", "AGENTS.md scaffolding"]
provenance: "seeded:#443"
---

# Reviewing harness code (plays, skills, agents, grounding)

## Topic
How to review the framework's own "code" — the plays, skills, sub-agents, and grounding
written as Markdown. This is the intellectually central category.

## Recognise
The diff changes a play (`SKILL.md` + its ICE), a skill, an agent definition, or grounding
under `core/components/**` (or a deployed copy). These files *are* the system's behaviour, so
they get the deepest treatment.

## Treatment
- **Reviewer:** human (the design) + tool (conformance).
- **Layers:** Layer 1 **and** Layer 2.
- **Linter (Layer 1):** structural conformance. Run the installed tools only, on the changed
  parts where they sit in the repository under review:
  - When the PR changes `core/components/` (the repository holds Garura's source), use the
    source layout:
    `node .garura/core/tools/lint-components/index.js --layout source --target core/components`
    and, for each changed play:
    `python3 .garura/core/tools/lint-play/lint_play.py core/components/plays/<play>/SKILL.md --next-map <next-map copy>`
  - Else, use the installed layout. The installed target is `.claude`. (The Codex install, to
    `.agents`, is stopped for now, #863.)
    `node .garura/core/tools/lint-components/index.js --layout installed --target .claude`
    and, for each changed play:
    `python3 .garura/core/tools/lint-play/lint_play.py .claude/skills/<play>/SKILL.md --next-map <next-map copy>`
  - `<next-map copy>` is the short-term copy of `standards/rules/pipeline-next.md` that the
    review got from `template-manager`.
  - `lint_play.py` checks a play: every constraint, failure and scenario has an eval, there is
    exactly one recovery for each failure, the required sections are there, the intent
    fingerprint is real, and no reference is an orphan. `lint-components` checks the shape of
    skills and agents, and finds installed parts that name Garura's source
    (`installed-paths/source-path`).
  - Only a violation whose file is in the PR's changed paths is a finding. Count the other
    violations, and record the count as "there before".
  - When a tool is not installed, record `not installed` for that check. When a tool crashes,
    record `did not run: <first error line>`. Neither is a pass, and the review goes on.
  - The ICE-source rule (an intent change traces to the play's ICE source, not to a hand edit
    of the compiled file) applies only where the repository under review holds the plays'
    source. An installed copy has no ICE source to trace.
- **Design-grounding (Layer 2):** **yes.** Reconstruct the harness design principles from
  **committed** sources — `docs/philosophy/**`, `docs/adr/**`, the standards under
  `memory/standards/rules/**` (e.g. user-facing-voice, play-close, evidence-recording), and
  the glossary — never from the branch's own new prose. Then check each changed play/skill/
  agent for conformance to those signed-off principles (agent-first delegation, JSON contracts
  over files, play orchestrates / skills produce / scripts do mechanical work, ICE-source
  discipline).
- **Rubric:** does the change keep the play→agent→skill→script wiring intact; where the
  repository holds the plays' source, does an intent change trace to its ICE source; does it
  hold the standards it is subject to.

## Rationale
A harness PR can be internally consistent and still wrong against the framework's design. The
only way to catch that is to ground the principles externally first, then test conformance —
otherwise the branch grades its own homework. This is the category the whole external-grounding
discipline exists for.

## Provenance
seeded #443 — adapted from the PR Review Approach spec (category C).
