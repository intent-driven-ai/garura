## Intent
- Goal: Machine checks read every part of the harness, every play, loop, sub-agent, skill, script and shared file, and fail each one that breaks a written rule of the standard, naming the part, the rule and the line, with each rule read from the rule files, so this intent's proof holds: "The checks hold every part to the standard."
- Limit: A check reads the rule files and counts; it judges nothing and holds no rule of its own.
- Limit: A new rule's check warns until the parts have moved, then fails.
- Limit: In an installed project, a check reads the installed parts and the rules fetched through the memory tool, never the source.
- Fails if: A part that breaks a written rule passes every check.
- Fails if: A check holds a rule that no written standard states.
- Fails if: Breaks on parts no change touched stay unseen, with no count and no owner.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the component linter and its eight rule families, the play linter, the loop linter, the old-name check, the rule files and Phoenix memory's copies, what each check reports on the source today, where the checks run, and the open issues on checks with no tests.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead, who keeps the checks; and the developer, a person or an AI agent who builds the code, whose part the checks pass or fail.
- Scope: In: the component linter, the play linter, the loop linter and the old-name check, their rules, where they run and their tests. Out: the review of each change and its verdict, the docs check, the tracker check, Phoenix memory's copies, and the way past a failed check.

## Expectation
- Scenario: In a bank's payments service, a developer's new skill has no `model` line; the component linter fails it and names the skill and the rule before the change is merged. In a harness repository, every check runs on the whole source: each break is named with its part, its rule and its line, and the breaks on parts no change touched are counted, each with an owner.
- Done means: Someone other than the one who built the parts runs every check on every part and reads the reports and the rule files, and finds each break of a written rule named with its part and rule, no rule held only in a check's code, and the breaks on parts no change touched counted with an owner.
