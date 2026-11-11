# How to draft a BI-10 capability: the shared brief

Issue #1021 (the reorganisation of Garura's business intents). Business intent BI-10, "Standards, structure,
settings and memory" (`.garura/product/product-os/intents/bi-10.md`). Six capabilities, each drafted by its own
agent from what Garura has built. Every agent follows this brief.

## The product owner's word

On 2026-11-11, after the stock-take and the proposed list, the product owner wrote: "continue as most of this is
based on built. please proceed with creae pages and ICE as per the process and standards and consider them
approved. show me only when you are ready for commit and cp". The list, the eight answers and how they were taken
are recorded in `.garura/project/issues/1021/context/capabilities.md`, section "Standards, structure, settings and
memory" (read it first). Cite his words from that file, with its line numbers.

## What you read

- The stock-take: `.garura/project/issues/1021/context/bi-10-inventory/inventory.md`. Your capability's own section
  (1 to 6), section 7 (what approved pages hand to the six; your capability's part of it is a list of promises your
  pages must keep), section 8 (the old parts), section 9 (gates with no way past), section 10 (what is new), section
  12 (the leans; your capability's feature list is in Leans 2 to 7) and section 13 (the questions; the answers are
  the product owner's, as recorded in capabilities.md).
- The evidence the stock-take cites: open each file at the line it names before you quote it, and read the issues it
  names with `gh issue view <n>` (reading only). Never write to GitHub.
- Memory only through the memory tool, from the repo root (`python3 .garura/core/tools/memory/memory.py
  search|find|read ...`; `.claude/rules/garura-memory.md`). Never read a memory file by its path. Raise no memory
  update and decide none.
- Never read anything under `.garura/project/plans/*/evals/`.
- No web research. A part that is not built is drafted from the product owner's words, the issues and what is built
  around it, and gets a thin ICE.

## The pages to copy the shape from

Approved pages already in the model, in `.garura/product/product-os/software-delivery-planning/`:
- `manage-adrs/`: a capability with built features (full ICE) and not-built features (thin ICE). Copy its shape.
- `give-every-gate-a-way-past/`: a capability where nothing is built, every ICE thin.
- `track-execution/`, `run-plays-as-loops/`, `orchestrate-agent-work/`: more of the same shape.
Read at least `manage-adrs/capability.md`, `manage-adrs/ice.md`, one built feature with its ice.md and one
not-built feature with its thin ice.md before you write.

## The rules every page follows

**The capability page** (`capability.md`):
- `# Capability: <Title>`, then `## Directional intent`. Its first line is `<Title>: <the agreed line>`, word for
  word. Then: whose words these are; "The words this page uses:" (plain definitions); the jobs it does, built and not
  built; how it sits with the other capabilities; "It matters because ..."; the domain sentence, exactly: "It sits in
  software delivery planning with the other capabilities of Standards, structure, settings and memory. The domain's
  first paragraph does not name them yet; widening it is owed at this intent's close."; then "Features:" with one
  line each, `- <Feature title> (<fn-id>): <what it does>.` (a not-built feature ends with "Not built." or "Not built
  (#n, what it is about)." at the end, never the start); then "What is not built yet:" bullets.
- `### Benefit hypothesis` (Who it serves; What we believe, with its rules; How we will know), `### Boundary (In / Out
  / Never)` (every Out names its owner; every Never has "The reason: " and an exact quote), `### Guiding rules` (each
  with "The reason: " and an exact quote, or a "- Not decided: " line), `## Sources`.
- No ICE on this page: the ICE is its own page.

**The feature page** (`feature.md`):
- `# Feature: <Title>` (a plain sentence of what a person can do, or what happens).
- `## What it does`: the first sentence says what it does and why, in one sentence that can stand alone (its
  opening becomes the part's one-line in the model's index, so it must not start with "Not built"); bullets; then
  `- Examples, in different kinds of project:` with at least three `  - In a <kind of project>, ...` lines from three
  different kinds of project (a clinic's booking app, a bank's payments service, a game studio's build, ...);
  `- How it meets the capability: ...`; then a line starting `Status: built`, `Status: built in part` or `Status: not
  built`, with "Not built, or open:" bullets.
- `## Inputs / Outputs` (`- In:` / `- Out:` lines), `## Rules & behavior` (each `- <rule>. The reason: "<exact
  quote>"`, or `- Not decided: <the open point>` with no lean in it: never "should", "likely", "probably",
  "recommend", "we suggest"), `## Acceptance criteria` (each `- Given ..., when ..., then ...`; a not-built one ends
  "This is not built."), `## Out of scope` (each line names its owner: "X, in Y, owns it." or "<Title> (<fn-id>) does
  it"), `## Sources` (each source with its path and line, or issue number, and the exact words used).
- No ICE on this page.

**The ICE page** (`ice.md`, beside its part's page), exactly three parts:
- `## Intent`: one `- Goal:`, then `- Limit:` lines, then `- Fails if:` lines.
- `## Context`: `- Read: Gather it from the memory layer. Look first at the project's existing memory and its
  existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a
  memory update for a person to approve. For this part, look for: <what this part needs>.`; `- Never read: any memory
  file by its path, and any ICE page.` (add what else this part must never read); `- Persona: ...`; `- Scope: In: ...
  Out: ...`.
- `## Expectation`: one `- Scenario:` (two kinds of project) and one `- Done means: Someone other than the one who
  ... reads ... and finds ...`.
- Built or built in part: a full ICE (no Thin line). Not built (also when only planned in an issue): a thin ICE, whose
  first line is exactly `Thin: proposed from the person's words; deepen with `/discover-capabilities`.`, then a blank
  line, and at most three Limit lines and three Fails if lines.
- The capability's own ICE is full when any of its features is built, thin only when none is.

**Words.** Plain, short sentences (ASD-STE100 style). Personas only: the product owner, the technical lead, the
developer ("a person or an AI agent who builds the code"); never a real person's name; no home, temp or scratch path.
Say "loop", never the old word for it. Every issue number comes with what it is about: "#992 (every gate has a key)".
Every quote is exact, from a file, an issue or the product owner's recorded words, and named in Sources. Nothing is
invented: a claim with no source is not written, or is a "Not decided" line.

**Ids and folders.** The capability is `cap-<slug>` and its folder `software-delivery-planning/<slug>/`. A new
feature is `fn-<short-slug>` in a folder of that name under the capability's folder. Before you use a new id, check
that no part already has it: `grep -n "id: fn-<short-slug>$" .garura/product/product-os/_spine.yaml` finds nothing.
An old feature keeps its id and its folder (`features/<fn-id>/`).

**Where you write.** Only under your own run folder, `.garura/project/issues/1021/context/bi-10-capability-<N>/`:
drafts at `drafts/product-os/software-delivery-planning/<slug>/...` (and, for old features,
`drafts/product-os/features/<fn-id>/feature.md` and `ice.md`). Never change the model, the spine, an issue, or any
other file; never commit.

**The check.** Run, from the repo root, until it exits 0:
`python3 .garura/project/issues/1021/context/bi-10-drafting/check_drafts.py .garura/project/issues/1021/context/bi-10-capability-<N>`

**Return.** The capability's title and id; each feature's title, id, status (built, built in part, not built) and
whether its ICE is full or thin; the check's last line; and the open points you wrote as "Not decided" lines.
