# The four P2s of PR #1039, drafted as issues

Drafted after the product owner's verdict on PR #1039: "approve but also record the p2s s that we address hem properly".
Where: intent-driven-ai/garura (the work tracker in `core/config.yaml`, `trackers.work`). No labels. Each is filed on
its own, with no parent: #1021 is a Chore with no parent, and the Story whose skill accepts features (#1019) is closed
under the closed #722. No model part is owed: each is a defect in parts already in the model or in memory, and the fix,
once decided, changes those parts.

---

## 1. Bug: Intent pages list features under "Touches", which the ontology says an intent never names

Severity: P2 — ten intent pages and the intent-page skill disagree with the product ontology on what an intent points at.

**What happens.** The Touches lists on ten intent pages (BI-1 to BI-4, BI-6 to BI-11) name 238 features, beside 40
capabilities. The intent-page skill accepts the kind "feature": `core/components/skills/author-intent-page/scripts/write_page.py`
line 62, `TOUCH_KINDS = ("domain", "capability", "feature")`.

**How to see it.** `grep -c "(feature) —" .garura/product/product-os/intents/bi-*.md` gives 238 lines across ten pages.

**What is expected.** The ontology (`core/components/memory/standards/schemas/product-os/ontology.md`): a business
intent "does not name features; a feature is reached through its parent capability" (line 194); it "points only at its
capabilities, the business intents it was identified by and, loosely, its domains" (line 214); the worked example
lists one domain line and one capability line (lines 243-246).

**Decided first.** Either the feature lines go (the ten pages and the skill), or the ontology and the skill change
together, through `/edit-ontology`.

Found by check-change on PR #1039 (#1021, reorganise the business intents), finding DF-1.

---

## 2. Bug: The ICE rubric demands exactly one goal, while the ontology lets an ICE carry several

Severity: P2 — two memory files that every ICE writer reads disagree on a line every ICE has.

**What happens.** `core/components/memory/standards/rules/ice-rubric.md` line 9: Goal "Exactly one. This is not
negotiable. Two goals mean two parts: split the part, or move one goal down to a feature." Phoenix memory holds the
same rubric (`standards/rules/ice-rubric.md`, version b2e40bff2131).

**What is expected.** The committed ICE design lets goals share an ICE when they share the context: `ontology.md`
lines 482 and 493 ("the goals ..."); `standards/schemas/product-os/ice.yaml` lines 58-65; the capability grounding
schema (`grounding/capability.md` lines 69 and 109-110: at least one Goal, and its example has two). A judge using the
rubric would fail that example. The only committed support for one goal says "usually"
(`docs/philosophy/idd-decision-checklist.md` lines 113-117).

**Decided first.** Either a decision narrows the ontology and `ice.yaml` to one goal and they are aligned, or the
rubric says "usually", with the shared-context test.

Found by check-change on PR #1039 (#1021), finding DG-MEM-02.

---

## 3. Bug: The intent-depth rule lets a part of the source map to no intent, which /discover-intent refuses

Severity: P2 — a draft that follows the new rule fails the play the rule is written for.

**What happens.** `core/components/memory/standards/rules/intent-depth.md` lines 10-11: "Not every part is an intent.
Parts that only connect others are transitional. They are recorded as considered, with the reason they are not an
intent." The rules index names its reader as "any play or skill that specifies intents".

**What is expected.** /discover-intent maps every part of the source to the business intent it serves
(`core/components/plays/discover-intent/reference/ice.md` lines 92-96, C12; lines 179-181, F12), and its checker
rejects a part mapped to no intent (`core/components/plays/discover-intent/scripts/check_intent.py` lines 187-206).
The ontology's Business Intent and Source kinds have no place for "considered".

**Decided first.** Either /discover-intent (through its ICE and `/edit-play`) and its checker change, with a decision
record, or the rule is marked "Not yet wired" until they do. Either way, "considered" gets a home.

Found by check-change on PR #1039 (#1021), finding DG-MEM-01.

---

## 4. Chore: Give the 90 open issues of the deleted plans a home, or record that they stand alone

**What happened.** #1021 deleted the plans 606, 717, 722, 734, 756, 767 and 788 (each Paused or Done, none on a
branch). Five of them still held open issues: 606 (39), 722 (9), 734 (26), 756 (7) and 788 (9), 90 in all: 26
stories, 24 bugs, 19 chores, 16 feature items and 5 spikes. The approval
(`.garura/project/issues/1021/context/cleanup/approval.md`) named no open item.

**What the design says.** ADR 060, decision 2: when a plan pauses, its open issues "stay open and stay in the plan"
(`docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md` lines 101-103). An issue with no plan is still
allowed (`.garura/user-provided/managing-work.md` lines 65-74).

**How to list them.** The deleted plan files are in git: `git show 9db18136^:.garura/project/plans/<id>.yaml`.

**Done when.** Each of the 90 is placed under a plan of the new business intents, closed as no longer needed, or
recorded as standing alone, by the product owner's word.

Found by check-change on PR #1039 (#1021), finding PLAN-1.
