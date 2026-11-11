# BI-2 (Spec → Design): the proposed page — draft

Draft only. Nothing here has been written to the product model. It brings the Spec → Design
business intent in line with three decisions the product owner made on 2026-11-08 (recorded in
`.garura/project/issues/1021/context/capabilities.md`, the note under the Spec → Design list):
seeding memory is dropped, the word "lens" is no longer used, and there is no lock and no gate.
Each design can run at any time.

What changes: the Outcome and the Why each lose their last sentence. The Proof loses two of its
three lines. The Must not is rewritten from his words "we are not locking design, we can run this
anytime". Every other line is kept as it is. From the Stage line to the end, the page is byte for
byte the same (checked with `cmp` on a scratch copy): the Stage line, the Tracker line, the
fifteen Touches lines and the What-was-done line.

## Which skill writes it

**enrich-grounding, named lines (`change_lines.py`) on the intent page.** Its five changes are the
first page entry (`intents/bi-2.md`) in `change-lines-request.json`, beside this file. So BI-2 and
the 15 Sources lines that quote its Must not change together, in one all-or-nothing run.

Why not author-intent-page's rewrite:
- A rewrite builds every part again from a full `intent-draft.json`, in its own fixed order
  (`.claude/skills/author-intent-page/scripts/write_page.py`, header lines 21-22 and `render`).
  To change five lines, a draft of the whole page would first have to be made.
- A rewrite writes the Stage line again (`stage_line`, lines 109-116). It is "proposed" unless the
  caller passes `--stage confirmed --confirmed-by` and a date. To keep "confirmed — by the product
  owner, 2026-11-02" byte for byte, the caller would have to say that the 2026-11-02 confirmation
  covers words written on 2026-11-08. `change_lines.py` does not touch the Stage line at all.
- `change_lines.py` changes only the lines it names and keeps every other line with its own line
  ending. It refuses the whole request when a named line is missing or is on the page twice
  (`.claude/skills/enrich-grounding/scripts/change_lines.py`, `find_one` and its header). Its
  SKILL.md step 5 names an intent page as one it may change. The meaning comes from the request's
  source: here, the product owner's own words.
- Dry run: on a scratch copy, the request ran with exit 0. All 71 changes were made on 24 pages,
  and nothing else changed.

## The proposed page, in full

```markdown
# Spec → Design

**Outcome:** The project's positions are set for the whole project: technology and architecture, surfaces, deployment and environments.

**Why:** Without shared positions, each builder invents its own answer.

**Asked by:** the product owner

**Proof it is met:**
- Each position is written down and can change later.

**Must not:** Block other work. Each design can be run at any time.

**Stage:** confirmed — by the product owner, 2026-11-02
**Tracker:** #2

**Touches:**
- [Design the technology and architecture](../software-delivery-planning/design-technology-architecture/capability.md) (capability) — adds
- [Set the project's architecture](../software-delivery-planning/design-technology-architecture/fn-set-architecture/feature.md) (feature) — adds
- [Update the architecture as the project changes](../software-delivery-planning/design-technology-architecture/fn-update-architecture/feature.md) (feature) — adds
- [Manage surfaces](../software-delivery-planning/manage-surfaces/capability.md) (capability) — adds
- [Declare a surface, its properties and its guidelines](../software-delivery-planning/manage-surfaces/fn-declare-surfaces/feature.md) (feature) — adds
- [Update the surfaces as the project changes](../software-delivery-planning/manage-surfaces/fn-update-surfaces/feature.md) (feature) — adds
- [Deployment design](../software-delivery-planning/deployment-design/capability.md) (capability) — adds
- [Design how the project runs](../software-delivery-planning/deployment-design/fn-design-how-project-runs/feature.md) (feature) — adds
- [Prepare a dedicated cartridge for each cloud: AWS, GCP and Azure](../software-delivery-planning/deployment-design/fn-cloud-cartridges/feature.md) (feature) — adds
- [Update the deployment design as the project changes](../software-delivery-planning/deployment-design/fn-update-deployment/feature.md) (feature) — adds
- [Environment setup](../software-delivery-planning/environment-setup/capability.md) (capability) — adds
- [Declare the environments and how each is set up](../software-delivery-planning/environment-setup/fn-declare-environments/feature.md) (feature) — adds
- [Build and manage an environment when a deployment needs it](../software-delivery-planning/environment-setup/fn-build-environment/feature.md) (feature) — adds
- [Update the environments as the project changes](../software-delivery-planning/environment-setup/fn-update-environments/feature.md) (feature) — adds
- [Set up a dev sandbox on a builder's machine](../software-delivery-planning/environment-setup/fn-dev-sandbox/feature.md) (feature) — adds

**What was done:** (nothing yet)
```

## The diff against the page as it is

```diff
--- a/.garura/product/product-os/intents/bi-2.md
+++ b/.garura/product/product-os/intents/bi-2.md
@@ -1,17 +1,15 @@
 # Spec → Design
 
-**Outcome:** The project's positions are set for the whole project: technology and architecture, surfaces, deployment and environments. The memory each lens needs is seeded, and a design is locked before agents take over.
+**Outcome:** The project's positions are set for the whole project: technology and architecture, surfaces, deployment and environments.
 
-**Why:** Without shared positions, each builder invents its own answer. Without the lock, agents drift.
+**Why:** Without shared positions, each builder invents its own answer.
 
 **Asked by:** the product owner
 
 **Proof it is met:**
 - Each position is written down and can change later.
-- Each lens has its memory.
-- No agent builds from a design that isn't locked.
 
-**Must not:** Block on anything except the lock, which is the only gate.
+**Must not:** Block other work. Each design can be run at any time.
 
 **Stage:** confirmed — by the product owner, 2026-11-02
 **Tracker:** #2
```

## One choice to confirm

- The Must not says "Each design can be run at any time." The example given was "Each of these can
  be run at any time." On the page, "these" would have nothing clear to point to: the line before
  it is the Proof, which now holds only "Each position is written down and can change later." His
  words were "we can run this anytime", where "this" means the design. The 19 body lines on the
  capability pages say "each design can run at any time" for the same reason. If "Each of these"
  is wanted, the Must not line in `change-lines-request.json` and the 15 Sources quotes of it change
  together.
