# Feature: Check the model's structure and links on every change, as findings, never a stop

## What it does
On every change that writes the model, the structure check reads its pages and its index for their shape and their links and lists what it finds, so a broken page or a link to nothing is seen in the change that made it, and each finding is fixed later without stopping work.
- In its own words: "It enforces SHAPE and LINK INTEGRITY — never content quality".
- What it checks, on the pages and in the index:
  - each page has its kind's headings, in order, with none missing and none made up;
  - no required section is empty or below a floor of words, and no bullet is a bare label;
  - each index entry points at a page that exists and is of its kind, and no page sits on disk with no entry;
  - each ICE entry is for one real capability or feature, names no business intent, and points at an ICE page whose three parts are not empty; each part has one ICE.
- It is one script, with 13 copies kept the same: one in /create-play's references and one in each play that writes the model. The live plays that run it are /discover-intent, /discover-domains, /discover-capabilities and /shape-slice.
- Every change to the ontology runs the model's checks before and after, by the product owner's answer of 2026-11-11: "Yes, every ontology should run the model before and after." The step that runs them is Define what a product is made of's; the checks are this feature's.
- Its run on the whole model on 2026-11-11: not ok, 21 errors and 263 warnings. The errors: 8 in two features of the old capability Build a plan (fn-727 and fn-728), 12 in three features of Specify the product, and 1 in fn-931. The warnings: 249 ask for an ICE section on parts whose ICE is on its own page, 13 say a part has no ICE yet, and 1 says a capability has no domain.
- Examples, in different kinds of project:
  - In a shop's checkout service, a change adds a feature page with no Acceptance criteria section. The check names the page and the section, and the change goes on; the fix is listed as owed.
  - In a clinic's booking app, an ICE entry points at a page with an empty Expectation part. The check names the ICE.
  - In a bank's payments service, a capability is renamed and its old page is left on disk with no entry. The check names the page.
- How it meets the capability: a living map can be trusted only when its shape and its links are checked each time it changes. The product owner: "Managing the model should hold any checks of the model as well."

Status: built, in `lint_grounding.py`, 13 copies kept the same, run by four live plays. It is out of step with the ontology, named below. Not built, or open:
- It still gives 249 warnings that read "no '## Agent intent (ICE)' yet", though since the ontology's version 6 "The ICE is on its own page, never a section of the capability page."
- The model fails it today, with 21 errors.
- It does not check needs or "identified by" links. Link the parts by the map's rules: what each serves, what it needs and what led us to find it (fn-725) is to add it.
- /shape-slice's model check stops the run until it reads valid, and its fix loop cannot clear 7 "thin mark drift" problems on an older slice (#1033). This is a stop with no way past.
- The review of a change has no playbook for model pages: "No installed linter reads the product model, so Layer 1 was a by-hand check" (#870, check-change has no review playbook for product model pages).
- No step in /edit-ontology runs it before and after a change to the ontology.

## Inputs / Outputs
- In: the model's folder and its index, or one page and its kind.
- Out: ok or not ok, each error and each warning with its page and what is wrong, and the count of each kind of part.

## Rules & behavior
- It checks shape and links, never what a page means. The reason: "It enforces SHAPE and LINK INTEGRITY — never content quality (that is the rubric eval's job)."
- It reads files only. The reason: "reads files on disk only; never shells to git/gh or the network."
- A finding never stops work. The reason: "missing links are warnings to fix later, not stops", and "What a rule can stop is work, never a write".
- A thin part is never an error. The reason: "A thin part is never an error."
- Each part has one ICE, and a part with none is a warning. The reason: "each part has exactly one ICE (a part with none is a warning)".
- A new rule never turns an older page's gap into an error. The reason, from the old capability Link the product model: "Old pages still pass. A gap in a page made before these rules is a warning, not an error. A new rule must not break an old model."
- Every play runs the same check. The reason: it is "the SHARED structural linter for product-model grounding docs."
- Not decided: whether /shape-slice's model check keeps its stop, or lists its findings with a way past that records what is owed (#992, every gate has a key).

## Acceptance criteria
- Given a feature page with no Acceptance criteria section, when the check runs, then it names the page and the section as an error.
- Given an ICE entry whose page has an empty Expectation part, when the check runs, then it names the ICE.
- Given a page on disk with no index entry, when the check runs with the index, then it names the page.
- Given a part whose ICE is on its own page, when the check runs, then it gives no warning for a missing ICE section. This is not built.
- Given Garura's own model, when the check runs on it, then it reads ok. This is not built.
- Given a change through /shape-slice that leaves a finding, when its model check runs, then the finding is listed as owed and the run goes on. This is not built.
- Given the review of a change that writes model pages, when it runs, then its first layer runs this check the same way each time. This is not built.

## Out of scope
- Judging whether a page is clear to a stranger. Each play that writes pages does it, with its page judge.
- The rebuild eval of a product's specification. Specify the product, in Product → Spec, owns it.
- The step that runs the checks before and after a change to the ontology. Define what a product is made of, in Product model, owns it.
- The ready answer. Say whether work can start on each part: ready, partly ready or not ready, with the gaps (fn-724) does it.
- Loose parts, one-sided links and duplicates. Find and close the gaps inside the model (fn-close-model-gaps) does it.
- Reviewing a change and its verdict. Check the code against its standards, in Code → Validation, owns it.

## Sources
- core/components/plays/create-play/references/lint_grounding.py, lines 3-26: "the SHARED structural linter for product-model grounding docs.", "It enforces SHAPE and LINK INTEGRITY — never content quality (that is the rubric eval's job).", "each part has exactly one ICE (a part with none is a warning)", "A thin part is never an error.", "reads files on disk only; never shells to git/gh or the network."; its 13 copies under core/components are the same file (compared on 2026-11-11)
- The structure check, run from the repository root on the whole model with its index on 2026-11-11, writing its report outside the repository: not ok, 21 errors, 263 warnings; "no '## Agent intent (ICE)' yet" on 249 parts
- core/components/plays/shape-slice/SKILL.md, lines 607-608: "the run does not go on until it reads valid"
- standards/schemas/product-os/ontology.md, in Phoenix memory, lines 25 and 362: "What a rule can stop is work, never a write", "The ICE is on its own page, never a section of the capability page."
- docs/standards/harness-standard.md, lines 71-72: "missing links are warnings to fix later, not stops"
- .garura/project/issues/1021/context/bi-11-write/old-pages/link-the-product-model.md, the copy of the old page of Link the product model, line 27: "Old pages still pass. A gap in a page made before these rules is a warning, not an error. A new rule must not break an old model."
- .garura/project/issues/1021/context/capabilities.md, line 125: "Yes, every ontology should run the model before and after.", "Managing the model should hold any checks of the model as well."
- GitHub #1033 (open): 7 "thin mark drift" problems, "and the fix loop cannot clear them"
- GitHub #870 (open): "No installed linter reads the product model, so Layer 1 was a by-hand check"
- GitHub #992 (open): every gate has a key
- The stock-take, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, sections 1.4, 1.6, 2.7 and 5, and section 9, questions 3 and 6
