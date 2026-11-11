# Feature: Record a decision as an ADR, with what it overrides and what it changes

## What it does
When a person, or a play that made a decision, gives a decision brief, the decision is drafted as an ADR from the one ADR template, with every older ADR it supersedes or amends named with the part it changes, the files, rules, schemas, plays and agents it changes named by real paths, its effect on agent intent, and its business-intent check, so that whoever accepts it, and every later reader, sees what it replaces before it holds.
- The brief holds what is decided, why now, the options considered with why each lost, who decides, where it was decided, and the shape of the record. A heading left empty is asked of the person, one at a time, and never filled in for them.
- The ADR template is loaded at the start of the run. When it cannot be loaded, the run stops, because "no record is written off the template".
- The record has one of two shapes. A Markdown ADR, in the project's ADR folder (`docs/adr/NNN-<slug>.md`), records a decision on how the project is built. A `decision.yaml` record is the shape for a product decision in the product model; that shape is built in the tool, and product decisions belong to Product model.
- A Markdown ADR takes the next free number in the ADR folder.
- The older ADRs it may change are found in two steps:
  - a script lists the candidates: each older ADR the decision names, or that shares a file path or a play name with it, at most ten;
  - an agent reads each candidate and judges it superseded in full, superseded in part, amended with the part named, or not affected.
- What it changes is named by real paths, and every path under Affects must exist in the repository. Its effect on agent intent names the agent intents it changes, or says that it changes none, and why.
- The business-intent check is one of three: none; kind, when it changes the Business Intent kind or its rules and no person's intent; or instance, when it would change a person's business intent. A script also reads the draft, and a draft that names a business intent page or an intent is treated as instance. An instance stops the run before anything is written: the person is shown which business intent and why, and the run ends. Inside a loop it is a new question, and "a new question stops the loop".
- A skill drafts the record with status proposed: the title as a statement of what is decided, then Context, Decision, Consequences and Alternatives Considered. Every alternative says why it lost, and the consequences name what gets harder.
- The agent checks the draft against the template and runs the business-intent script. A problem goes back to the skill, at most twice; then the run fails and names what is still wrong.
- Run by hand, the run starts only when the ADR folder and the product model have no uncommitted change. It writes the record at its place, never over a file that exists, and only when its number matches its file name. A script then checks that nothing else changed, and the record is committed as `docs(adr): ADR <NNN or id> — <title> (#<issue>)`.
- Run by hand, the decision play opens its own change first and lands it through the commit, the raise, the review and the merge. Handed a loop's contract, it opens no issue and no branch and works on the loop's branch.
- Examples, in different kinds of project:
  - In a shop's checkout service, the technical lead records the decision to keep a guest's cart in the database for thirty days. The candidates include the older ADR that kept carts in memory; the agent reads it, and the new ADR names it as superseded in full.
  - In a hospital's appointment system, a decision to send reminders through a queue amends only the part of an older ADR that said reminders are sent at once, and the ADR names that part and the two services it changes.
  - In a harness repository, a decision that renames the loops amends five older ADRs, each with its part, and lists every play file it changes under Affects.
  - In a mobile banking app, a drafted decision would drop a feature a person asked for. The run stops before anything is written, and the product owner is shown the business intent it would change.
- How it meets the capability: this is the record in "Decisions on how the project is built are recorded", with what it overrides and what it changes in plain view, so agents know which decision holds when they "coordinate many pieces from them".

Status: built, in /record-decision, with the adr-keeper agent, the author-decision skill and its script adr.py, and apply_adr.py; first built in #632 (closed). Not built, or open:
- It cannot record an ADR on the branch of a change that is already open. Run by hand, it opens its own change from main, so the change the decision belongs to lands without it (#822, /record-decision cannot join an open change). Record the ADR in the change it belongs to (fn-adr-in-its-change) is to do it.
- No play hands it a decision today. Only a person runs it. Take in each design choice that Spec → Design hands over (fn-take-design-choices) is to do it for the design choices.
- Nothing catches a decision made in a session that no one records.
- The candidates leave out an older ADR that shares only words with the decision, not a path, a play name or its number.

## Inputs / Outputs
- In: the decision brief, from the person or from the play that made the decision.
- In: the ADR template, loaded at the start of the run.
- In: the ADR folder and its older ADRs.
- In: the business intent pages, for the business-intent check.
- In: inside a loop, the loop's contract, naming its run and its branch.
- Out: the gathered context: the number, each older ADR with its kind and part, what the decision affects, its effect on agent intent, its business-intent check, and the points for the person who accepts.
- Out: the draft, with status proposed, and the report of its checks.
- Out: once a person has answered, the record at its place in the ADR folder, the report of the scope check, and one commit.

## Rules & behavior
- It starts from a brief and never fills one in. The reason: "Ask the person for any heading that is empty — plainly, one at a time; never fill one in.", and the agent's rule: "No outside research: a decision's reasons come from the brief and the person, never from you."
- Every record is written from the one template and checked against it. The reason: "no record is written off the template"; the check "checks the shape, never the merit".
- A script finds the candidates, and reading them decides. The reason: "Candidates are found mechanically; which ones really apply is judged by reading them.", and the script says of its list: "candidates only — the agent judges which are really superseded or amended".
- What it changes is named by real paths. The reason: "What it changes is recorded with real names"; a path that does not exist fails the draft.
- A decision that would change a person's business intent is stopped and shown to the person, by hand and inside a loop. The reason: "An ADR never changes a person's business intent.", and "the ADR is never applied to the intent either way". A change to the Business Intent kind is allowed: "changing the Business Intent kind (framework doctrine) is allowed and recorded as such".
- The draft is always proposed. The reason: "You draft; you never accept."
- Every check runs before the first write. The reason: "Every check runs before the first write, so a stop writes nothing".
- A record never replaces a file. The reason: "a record is never overwritten".
- A run writes only the record, its pointers and the index. The reason: a script checks that "only the record, its pointers, the index and the run's own records changed".
- At most two retries of the draft. The reason: "Retry the skill at most twice"; a draft that still fails is named, never passed.

## Acceptance criteria
- Given a brief for a decision that changes part of two older ADRs, when the record is drafted, then it names both with the part each changes, every path under Affects exists, and it reads proposed.
- Given a brief with no options considered, when the run starts, then the person is asked for the options and nothing is drafted until they answer.
- Given a draft whose business-intent check reads instance, or that names a business intent page, when the run reaches the person, then no ADR is written, the person is shown which business intent and why, and the run ends halted.
- Given a run by hand with an uncommitted change in the ADR folder, when it starts, then it stops before anything is drafted.
- Given a target file that already exists, when the record is applied, then nothing is written.
- Given a run inside a loop, when it ends, then no issue and no branch were opened, and the record sits on the loop's branch.
- Given an accepted record, when the run ends, then only the record, its pointers, the index and the run's own records changed.

## Out of scope
- Accepting or rejecting the ADR. Accept an ADR only on a person's word, then or later (fn-accept-adr) does it.
- The forward pointers and the index. Keep older ADRs pointing forward and the index current (fn-keep-adrs-linked) does them.
- The points found on the way, for the person who accepts. Give the person who accepts every point found on the way, and check it is whole (fn-show-accepter-findings) does them.
- Recording the ADR in a change that is already open. Record the ADR in the change it belongs to (fn-adr-in-its-change) is to do it; it is not built.
- Product decisions in the product model. Product model owns them.
- What a design choice says. The four capabilities of Spec → Design decide it.
- Opening and landing the change. Ship every change the same way, in Developer tooling, owns it.
- Reviewing the change that holds the ADR. Check the code against its standards, in Code → Validation, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, the list set on 2026-11-10: "Manage ADRs: Decisions on how the project is built are recorded closely as they're made, so agents can coordinate many pieces from them."
- core/components/plays/record-decision/SKILL.md: "no record is written off the template", "Ask the person for any heading that is empty — plainly, one at a time; never fill one in.", "a new question stops the loop", "the ADR is never applied to the intent either way", "Every check runs before the first write, so a stop writes nothing", "only the record, its pointers, the index and the run's own records changed"
- core/components/plays/record-decision/reference/ice.md: "Candidates are found mechanically; which ones really apply is judged by reading them.", "What it changes is recorded with real names", "An ADR never changes a person's business intent.", "changing the Business Intent kind (framework doctrine) is allowed and recorded as such"
- core/components/plays/record-decision/scripts/apply_adr.py: "a record is never overwritten"
- core/components/plays/record-decision/scripts/check_adr_scope.py: the scope check over the paths changed before and after the run
- core/components/agents/adr-keeper.md: "No outside research: a decision's reasons come from the brief and the person, never from you.", "Retry the skill at most twice"
- core/components/skills/author-decision/SKILL.md: "You draft; you never accept."
- core/components/skills/author-decision/scripts/adr.py: "candidates only — the agent judges which are really superseded or amended"
- standards/templates/adr.md, in Phoenix memory: "It checks the shape, never the merit"
- GitHub #632 (closed), the product owner on 2026-10-09: "check if this adr invalidates any older ones"
- GitHub #822 (open): "/record-decision cannot join a change that is already open"
- The stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, sections 4.1 and 9: "Nothing catches a decision made in a session that no one records."
