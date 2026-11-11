## Intent
- Goal: Every play, loop, skill and sub-agent is named by one written rule, plain lowercase words, the verb first, each verb with one meaning written in the rule file, never exactly a coding tool's own command, and each name used once, with the play verbs owned by five roles once ADR 066's rename lands, so a person learns the names once and a name that breaks the rule cannot land.
- Limit: The rule lives in the rule files; the linter reads them and holds no rule of its own.
- Limit: A new verb is added to the rule file with its one meaning before any name uses it.
- Limit: ADR 066's rule is applied in one change, after the reviews of BI-10 and BI-11; until then the rule files keep ADR 046's rule.
- Fails if: A verb means two things, or two parts of one kind follow different naming shapes.
- Fails if: A name that breaks the rule passes the linter.
- Fails if: The rule files a project reads differ from the source, and nothing names the difference as owed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the naming rule files and Phoenix memory's copies, ADR 046 and ADR 066, the agreed list of new names, the five roles of #1015 and their open points, the lists of built-in commands of the coding tools, and the name of every part.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who decides the names; the technical lead, who keeps the rule files; and the developer, a person or an AI agent who builds the code, who names a new part.
- Scope: In: the rule, its verbs and their meanings, the five roles, the built-in commands, and each kind's shape. Out: the rename map, each family's rename, running the check on every part, recording the ADR, and Phoenix memory's copies.

## Expectation
- Scenario: In a bank's payments service, a developer names a new skill `refund-letter-writer`; the linter fails it for having no verb first, and the skill becomes `author-refund-letter`. In a harness repository, after ADR 066's rename lands, the loop `/loop-product-spec` passes the linter, the old `complete-discovery` is gone, and every play verb belongs to one role.
- Done means: Someone other than the one who named the parts reads the rule files and the name of every part and runs the linter, and finds every verb with one meaning, every name passing, no name exactly a built-in command of a coding tool the rule covers, and, once the rename lands, each play verb with one role.
