# Test security: research and drafts (issue 1021, BI-4 capability 2)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-4-capability-2/drafts/product-os/software-delivery-planning/test-security/`: the capability page and its ICE page, and four feature pages, each with its ICE page. All five ICE pages carry the thin mark, because no part of this capability is built.

In one line: Garura sets a security level for a product and never tests the product against it. The one security check that runs is the review of each change, which matches the review's security rules against the lines a change adds; it belongs to capability 6 (Check the code against its standards), runs no scan, and has three open defects. The old slice check, /validate-epic, tested security at the level of the code only and is stale. Nothing tests a running build, no testing environment exists, and no memory tier says what a security test must cover.

What this run did besides reading:
- It copied the memory files it decided from into `bi-4-capability-2/memory/`, with `manifest.json`, all from Phoenix memory: the review's severity table (`standards/rules/pr.md`), the product profile schema, the spine schema, the ontology, the recovery rule (expectation generation), the builder isolation rule, the surface contract, the review shelves for code and tests, the self-review and commit rules, the product rules, the note that the profile floor is the bar, the note on one-shot cleanliness, the notes on environments and secrets and on the GCP runtime's security baseline, the Node.js note, the agentic guardrails note, the user-management shelf, and the quality design's schema for runnable checks (read, not used on the pages).
- It read Garura memory through the memory tool: the spine's product profile and the decision that raised the security level (`dec-cap-initialize-security-none-medium`).
- It searched every tier for security standards (`**/security/**`, `**/knowledge/quality/**`): no tier holds any.
- It read GitHub #438, #890, #535, #934 and #800 in full and the security lines of #510 and #870, and #888, #914 and #982 by their titles (all read only), and searched open issues for security, secrets, scans, vulnerabilities, penetration and dependency scans.
- It ran no placement: the domain (software delivery planning) was decided. It did no web research, so no memory update is raised.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

Kept: "Test security". Folder: `test-security`.
- It is the agreed name, and it sits beside "Test performance" and "Test accessibility", which follow the same pattern.
- The list's longer line, "Test security, against the product profile's security level", is the first line of the page's intent, so the yardstick is still the first thing a reader sees. A longer title would add nothing the first line does not say, and unlike capability 1 there is no unique barrier in the name to keep.

## What is built, and what is only planned

Built and live:
- **The review of each change** (/check-change, with the quality auditor running check-pr-quality). A script, `scan_taxonomy.py`, matches the severity table's rows against the lines a change adds, "No LLM judgment." The security rows are SEC-01 to SEC-26, with BE-08, DATA-18 and DATA-19 on secrets and personal data in the code; their rank is P1, "Security, secrets, injection, auth, data-loss, breaking API contract, migration safety." The review rejects a change "if any P1 finding (or a runnable suite is red)". The scan is for changes only: "Use only from check-change play; never invoke standalone for full-repo audits." It belongs to capability 6 by the approved list.
  - It matches names and words; it runs no scanner. Its rule for libraries, ARCH-11, wants "file, cve-list" as evidence, but it is a `path:` rule that fires on the name of a dependency file, so nothing finds a library with a known weakness.
  - Open defects: #438 (planning pages and skill prose rejected as P1 security defects; the path table that classes files first now exists, the issue is still open), #890 (scripts in plays and skills are classed as prose, "so code rules never check them") and #535 (the review "has no model of what the project is", so a 0 can mean "never examined").
- **The commit's secret scanner** (/commit-change, `analyze_changeset.py`): "C6's guarantee is unchanged: actual secrets never commit." It guards landing, so it is Ship every change the same way's, in Developer tooling. The self-review in /propose-change checks "No secrets." too.
- **The product profile's security level.** Garura's own profile is set at medium, with the pass bar "no tracker or mapping write before the typed yes, on a test GitHub organization; no write to Phoenix memory or another project's memory". Its one capability with a security need, initialize, says how it is checked: "run initialize on a test GitHub organization with a missing type, answer no, and check the tracker's type list and the mapping are unchanged". The level was raised from none to medium by an approved decision. Nothing runs either check. The profile's compliance list is empty.

Built but stale or unused:
- **/validate-epic** (agreed new name /validate-slice), stale (#855): "Security is **code-level only**: static analysis, lint, dependency scans — never penetration-style probing." Its ICE: "C5 — Security verification is code-level only ... No penetration-style probing of running systems." It ran tool runners, among them `runner_lint.py` ("semgrep, dependency audits like npm audit / pip-audit"), and compared results with the profile's bars ("An unmeasured bar is not a passed bar."). Its scenario S3 names a persona, the "security auditor". Its fix report "names each failure by check and location".
- **quality-auditor** (agent, live): can "Run dependency vulnerability scan" and "Run SAST scan" when its checks ask; only the stale plays ask, and its lookup for project quality standards finds nothing.
- **check-quality** (skill, built, never used): a scored audit with a security area that reads `security/owasp-secure-coding.md`, `security/auth-data-protection.md` and `security/secrets-vulnerability-mgmt.md`. None of the three is in any memory tier.
- **/release-increment** (stale): its scenario S4, "security reviewer, no secret leak": "secrets are read from the manager and no secret literal appears in the logs, the deploy record, or the repo." The stale run design play has a "security reviewer" scenario too ("no secrets in repo").

Planned only:
- "Security testing (planned): The product is tested for security before it runs.", moved here from Validation → Run on 2026-11-09.
- /validate-security: a name only ("/validate-security (new)", `names.md` line 16, which ADR 066 names as the full list).
- The testing environment (Environment setup, not built), and the deployment design that says "which tests run in which environment" (not built).
- One severity scale for findings and defects, #934 (open).

What memory holds, and does not:
- No tier holds a rule for what a security test must cover, for any kind of product, and no security standards shelf.
- Phoenix memory's learnings name security only as conditions and baselines for building: the domain shelves add features when `nfr.security` is high (for example sign-in with a second factor), the GCP runtime note has a "Security baseline (non-negotiable)", the environments note keeps credentials "only in secrets management", the agentic note asks for "prompt-injection and untrusted-content defense", and the one-shot note names a dependency scanner among delivery checks. The note on profile floors carries the principle "an unmeasured bar is not a passed bar" and "The NUMBERS live in the product profile, per product". None of these says how to test; the pages quote only the principle and write no tool or baseline as a rule.

Not part of this capability, named so the line is clear:
- #888, #914, #982: the change plays push with no scan for client, company or personal references, and run records carry home-folder paths. These guard what Garura publishes, in Developer tooling.
- The project brief's "DxOps / security scanning" under the Control Tower: a view across projects, not a test of one product.
- #800 (open, "after the build, an independent step runs the hidden evals and the checks and gives the verdict"): worded for the evals; capability 1 holds it.

## The open points, each with options and a lean

None of these is decided here. Where a lean rests on what is built or on approved pages, the drafts follow it; the rest is named as not decided on the pages.

### 1. The line with capability 6, Check the code against its standards

What holds: the approved list gives "reviewing a change against its standards" to capability 6, and item 2 tests security "against the product profile's security level". Capability 1's approved page gives "testing security, performance, accessibility and the user experience on each surface, and checking the code against its standards, with the review of a change" to the other capabilities. The review's table already holds security rows (SEC), performance rows (PERF) and accessibility rows (FE), so the same line question comes back for capabilities 3 and 4.

1. **Split by yardstick and by scope.** Capability 6 holds the review of each change against the code's standards, with the table's security rows on the lines each change adds. Test security tests the whole built work against the profile's security level: the libraries for known weaknesses, the code's own weaknesses, any secret's value in the code, its settings or the records of the build, and the running build. It takes capability 6's record as evidence and never runs the same rows again. Gain: the approved lines hold; the same line works for performance and accessibility; the profile's level marks what belongs here. Cost: two capabilities look at the code's security, one change by change, one for the whole.
2. **All code-level security in capability 6; Test security tests the running build only.** Gain: one plain line, code at rest against running product, as the stale slice check and the BI-4 stock-take drew it. Cost: a pass bar often names code results (the schema's example allows "no P1/P2"), so this capability's verdict would rest on capability 6's record for that part, and capability 6 would need the profile as a yardstick too.
3. **All security here, the review's security rows included; capability 6 keeps the other rows.** Gain: one owner for every security check. Cost: one review and one table with two owners, against the approved line that the review of a change is capability 6's.

Lean: 1. The drafts follow it.

### 2. What is tested on the code, and what on the running build

What holds: the moved line says "The product is tested for security before it runs."; the list assumed the security tests run "in the testing environment Environment setup declares, never in production."; Garura's own pass bar is itself a test of the running product on a test organization; the stale slice check allowed "No penetration-style probing of running systems."

1. **Both, here.** The code at rest (its weaknesses, its libraries, any secret's value), and the running build in the testing environment, on its declared surfaces, for what the pass bar and each capability's security need say to try, never touching anything outside that environment. Gain: matches the move, the assumption and the pass bar that exists. Cost: nothing runs until a testing environment exists, and the old rule against trying running systems is narrowed to the copy set up for the test, and nothing else.
2. **The code only, as the stale slice check did.** Gain: needs no environment. Cost: Garura's own pass bar, and any bar like it, cannot be tested at all; the product owner moved running-product testing here.
3. **The running build only.** Cost: the library scan and the static scan, which the stale check and the quality auditor already know how to run, would have no home, unless option 2 of point 1 is taken.

Lean: 1. The drafts follow it, as two features.

### 3. The yardstick

What holds: the profile holds a level and "(the standard / how it's measured)" for security; Specify the product sets each capability's need with "a target someone can measure and how it is checked"; the profile's compliance list holds "regimes the box admits"; the approved architecture and deployment design hold rules each release must keep, among them where secrets are kept.

1. **The profile's security level and pass bar, with each capability's security need under it.** The compliance needs and the design's security rules count where the pass bar or a need names them. Gain: one yardstick that a person set; matches item 2's words. Cost: a loosely written pass bar leaves gaps that no test fills.
2. **Option 1 and the compliance needs, each regime adding its own security rules.** Gain: a product under a regime, such as card payments, is tested for it. Cost: memory holds no security rules for any regime; each needs research approved as a memory update.
3. **Option 2 and the security rules of the architecture and the deployment design, such as who can reach each environment.** Gain: what was designed is tested. Cost: overlaps Environment setup's own check that an environment answers, and neither design exists yet.

Lean: 1. The drafts follow it, with one exception: a secret's value anywhere outside where the deployment design keeps secrets is always tested for, because the approved Deployment design and Environment setup pages make it a Never for every product.

### 4. What a security test must cover

What holds: nothing. No memory tier says what a test must do for a level, a named standard or a kind of product; the scored quality check names three security standard files that are in no tier.

1. **Per product, from the pass bar.** What each part of the pass bar asks of a test comes from the project's own memory first, and for a named standard or a kind of product from research that a person approves as a memory update. Until then the part is named as not tested, and the verdict cannot pass. Gain: memory first, nothing from the agent's own knowledge. Cost: a product whose pass bar names a standard gets no pass until the memory exists.
2. **A set of security tests that Garura keeps in Phoenix memory for every product.** Gain: every project starts with the same floor. Cost: still needs research a person approves; one set fits a command-line tool and a payment site badly.
3. **A person writes the tests for each project.** Cost: a person for every project, and the tests are not shared.

Lean: 1. The drafts name it as not decided on both test features. No memory update is drafted: this run did no web research, and drafting one from the agent's own knowledge would break the rule.

### 5. The persona: who reads the verdict

What holds: the domain serves "the product owner, who names the work, the technical lead, who designs it, and the developer, who builds it"; Deployment design serves "the devops engineer"; Design the technology and architecture serves "the architect"; capability 1 (approved) has the product owner read the verdict and decide what a person must decide; the stale plays name a "security auditor" and a "security reviewer".

1. **The product owner reads the verdict and decides each finding a person must decide; the developer gets each finding the builder can fix alone.** Gain: the same as capability 1; the product owner set the security level and is the one who can move it. Cost: the product owner gets questions of design too.
2. **By what the way back changes: the developer for the code, the architect or technical lead for the architecture, the devops engineer for the deployment design or an environment, the product owner for the level itself.** Gain: each finding reaches the owner of what must change, as the approved pages name them. Cost: four routes, and the verdict still needs one reader.
3. **A new persona, a security reviewer, who reads the verdict for the product owner.** Gain: one owner for security. Cost: no approved page uses it, and the domain page would change.

Lean: 1. The drafts follow it; option 2 is named as not decided on the verdict feature, as capability 1 left the technical lead question open.

### 6. What a security failure sends back, and to whom

What holds: the recovery rule's test, "Can the builder fix this from information it already has, deterministically?", and its rule that "any irreversible / outward-facing decision" needs a person; a handoff plan "never names the failure condition, its id or the check"; the old slice check's fix report named "each failure by check and location". Security findings have no recovery written in a hidden file, so something must apply the test to each finding.

Does a security finding ever go to the builder alone?
1. **Yes, by the recovery rule's test for each finding.** The developer when the way back is a change of the code the builder controls, such as moving a library to a version without the weakness; a person when it needs judgment or authority the builder does not hold, such as a change of the architecture, the deployment design or an environment, a weakness with no known way back, or the level itself; a secret's value found anywhere always goes to a person, because the secret must be changed where it is kept; and a person whenever in doubt. Gain: the same rule as every other handoff; fixes that need no judgment do not wait. Cost: a part that is not the builder must make the call for each finding.
2. **No, every security finding goes to a person first, who sends it on.** Gain: no security call is left to an agent. Cost: a person for every finding, which slows each round.
3. **By rank: the most serious to a person, the rest to the developer.** Cost: rank says how bad, not who can fix; and the scale is open (#934).

Lean: 1. The drafts follow it.

What the handoff plan says:
1. **The weakness, where it is, and the way back; never the test, its rule, its id or its tool.** Gain: a weakness in code cannot be fixed without its place; the test stays hidden. Cost: naming the weakness says much of what the test looked for.
2. **The rule and where it fired, as the old fix report did.** Cost: the builder learns the test and can aim at it.
3. **A symptom only, as for the eval.** Cost: a library or a line of code cannot be found from a symptom.

Lean: 1. The drafts follow it.

### 7. What the builder may see

What holds: "Would knowing this change how the builder writes code? Yes → constraint. No → failure condition."; the philosophy names "security scan results" as checked after the work exists: "giving it to the builder only invites teaching-to-the-test."

1. **The builder knows the yardstick (the level, its pass bar, the security rules of the architecture and of the deployment design) but never gets the tests, their results or the verdict.** Gain: follows the rule that divides the two. Cost: the builder cannot run the same scans before handing over.
2. **Everything open: the builder may run the same scans itself.** Gain: fewer rounds. Cost: the builder grades itself, which BI-4 must not allow.
3. **The tests open, the verdict hidden.** Cost: the builder still aims at the test.

Lean: 1. The drafts follow it.

### 8. How secrets are handled in a test

What holds: Deployment design keeps "where secrets, such as passwords and keys, are kept", never their values; Environment setup's environments hold no secret's value and a builder's machine "holds only made-up data and no secret's value"; the review records a secret as a "redacted-snippet"; the stale release play read secrets "from the manager" so that "no secret literal appears in the logs, the deploy record, or the repo".

1. **A test that needs a secret, such as a test account's password, takes it at run time from where the deployment design keeps the testing environment's secrets, for that environment only, and writes its value nowhere; a finding names only where a value was found.** Gain: uses what is designed; no record holds a value. Cost: needs the deployment design and the testing environment, neither built.
2. **The test makes its own test accounts and keys for each run in the testing environment and removes them after.** Gain: no lasting secret. Cost: the test builds things in an environment, which is Environment setup's work, and needs the authority to do it.
3. **A person hands the secrets for each run.** Cost: a person for every run, and a secret passes through a conversation.

Lean: 1. The drafts follow it.

### Smaller points, named as not decided on the pages

- Where the tests run while no testing environment and no deployment design exist, as today.
- How the running test reaches each surface: through the slice's usage guide, as the eval does, or through what the deployment design records for each surface.
- The rank of each finding, while #934 is open.
- Where the verdict and the handoff plans are kept, and how a handoff plan reaches the developer.
- Which tests run again on each change: all of them, or only those the change could touch. The old slice check bounded its re-checks by what changed; it is not written as a rule.
- What counts as the same finding coming back, and how many rounds a project allows.
- A security line in a story's expectations is tested by the slice's eval (capability 1). When the eval names it under Untestable, whether this capability tests it is not decided.

## The features found

1. **Test the built code, its settings and its libraries for security weaknesses** (fn-test-code-security). Not built; the review of each change runs the table's rows on the lines it adds (capability 6's), and the stale slice check and the quality auditor ran library and static scans. Sources: item 2 of the approved list; /validate-epic ("static analysis, lint, dependency scans"); quality-auditor ("Run dependency vulnerability scan", "Run SAST scan"); the severity table's ARCH-11 ("file, cve-list") and SEC-19 ("redacted-snippet"); the note on profile floors; #438, #890, #535.
2. **Test the running build for security in the testing environment** (fn-test-running-security). Not built. Sources: the moved line ("The product is tested for security before it runs."); the assumption recorded with the list ("in the testing environment Environment setup declares, never in production."); Garura's own pass bar and initialize's security need, both tests on a test GitHub organization; Deployment design ("which tests run in which environment"); the stale release play's secrets rule.
3. **Give the security verdict, and send each finding to the developer or to a person** (fn-send-security-findings). Not built. Sources: BI-4's proof and must-not; the recovery rule; the ontology's handoff plan rule; /check-change's reject rule; /validate-epic's verdict and fix report; the approved Fix defects test first ("a finding in a review") and Build the work test first's update feature ("A handoff plan is the exact list of the work it calls for."); the decision that moved the level.
4. **Test security again as the product changes** (fn-retest-security). Not built. Sources: /validate-epic's rounds ("Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human.") with its security pass among its checks; the profile's rule that only an approved decision moves the level, and the decision that raised it, after which a need "is compared against medium, not none"; the Settings line; /loop-code-validation (a name).

Candidates not drafted, and why:
- **Run the review's security rules on each change**: capability 6's, by the approved list (point 1).
- **Keep secrets out of commits**: /commit-change's scanner, Ship every change the same way's.
- **Scan pushes for client, company and personal references** (#888, #914, #982): guards Garura's own publishing, Developer tooling.
- **Test against each compliance regime**: not decided (point 3); memory holds no regime's security rules.
- **Check that each environment matches its declared network and access**: Environment setup's check that an environment answers, or option 3 of point 3.
- **Rank findings by severity**: #934, which serves another business intent (#734).
- **A security reviewer persona**: point 5.
- **Match each test to a named standard**: part of the two test features, with point 4 open.

## Thin marks, and why

All five ICE pages open with the thin mark, with at most three Limits and three Fails if each: no part of this capability is built. The only live security check, the review of each change, belongs to capability 6.

## Lines elsewhere that are out of step (not changed here)

- Deployment design (approved) gives the tests to "The testing capabilities of Validation → Run (security, automated functional, performance, other testing and user acceptance testing)" and to the evals; security and performance testing moved to Code → Validation on 2026-11-09.
- Build the work test first and Fix defects test first (approved) name "Validate its own code", now "Check the code against its standards".
- The domain page says it "does not run the evals, release the work, or run the product"; this capability runs a copy of the product in the testing environment to test it. As approved, the domain line changes at BI-4's close.
- The stale slice check's rule "No penetration-style probing of running systems." is narrowed by the drafts to nothing outside the testing environment (point 2).
- The BI-4 stock-take leaned security testing to Validation → Run; the product owner's list of 2026-11-09 moved it here.
- The quality auditor's scans run only "if required by" checks that the stale quality design play writes.

## Assumptions

- Assumed: security tests run in the testing environment that Environment setup declares, never in production (recorded with his list).
- Assumed: the parts of this capability read the product profile, each capability's security need and the decisions that moved them from the product model, and never write them.
- Assumed: a secret's value found anywhere goes to a person, because the builder holds no secret and cannot change one where it is kept.
- The examples come from several kinds of product: a shop's checkout, a school's timetable app for phones, a team's command-line tool that writes to its tracker, a clinic's booking page, and a team's support assistant that answers customers' emails.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the four feature pages (`--kind feature`): ok, no errors, no warnings. The first run found one error on the code-test feature, a bullet under five words ("It tests three things:"); it was reworded and the check passed.
- **ICE shape check** (a small script in the session's scratch folder): each of the five ICE pages opens with the thin mark, holds Intent, Context and Expectation in that order, exactly one Goal, one to three Limits and one to three Fails if, the fixed Read line, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and a Done means checked by someone other than the doer. No part page holds an ICE section. No page says lens, seed, lock or gate, or names a real person, a home folder, a temp folder or a particular plan. Run once on a copy with five planted errors (no thin mark, a fourth Limit, a Done means by the doer, an ICE section on a part page, a forbidden word); it named all five.
- **Quotes** (a second small script): all 238 quotes on the ten pages are found word for word (spaces normalised; YAML's doubled apostrophes read as one) in their files: memory quotes against this run's copies in `memory/`, the product owner's words against `page-approvals.md` and `capabilities.md`, GitHub quotes against the issue texts read today. Every quote in a page body is also found in a file that page's Sources name. One quote of his was tidied for spelling only ("seecurity" to "security", "assessibility" to "accessibility"), and its Sources line says so. Run once with three planted errors; it named all three.
