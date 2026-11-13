# Feature: Keep the docs and command pages in step with each change

## What it does
A change that adds, renames, retires or changes a command brings the docs and command pages that describe it, in the same change, and a check run with the normal lint fails the change while the pages and the commands disagree, so the pages always say what ships today.
- The docs are the pages a person reads to learn what the project does and how to use it. The command pages are the lists of commands a person reads to learn which ones exist and what each does, such as a cheat sheet of commands.
- As asked: "The docs and the command pages say what Garura does today, and something keeps them in step when a play changes." For Garura's own repository, the commands are its plays; for a product project, they are the commands its own docs list.
- What the check catches, by machine:
  - a page that names a command that does not exist, such as a short name no play has;
  - a command that no page names;
  - a count of commands on a page that is not the count there is.
- What the change brings, and the review reads: the pages' words on what each changed command does, so a page never says a command does what it no longer does.
- The check runs as part of the normal lint of the project's parts, "not as a separate thing to remember".
- Examples, in different kinds of project:
  - In a harness repository, a play is renamed; the same change renames it on the docs table and on the cheat sheet, and the lint fails until it does.
  - In a team's planning tool, a command is retired; the lint fails while its help page still lists it.
  - In a shop's checkout project, a command's options change; the change brings its README section, and the review reads it with the code.
- How it meets the capability: the docs move with the change that alters them, on the same path, so no change lands and leaves its pages behind.

Status: not built. Today only the self-review asks it, as one judgment line, "Docs in step", and it goes with the self-review. The review's docs check fires only when the change itself changes the docs: "the PR changes human-facing prose that is not a decision record". The component lint has no rule for the docs. The drift is real: Garura's table of plays lists six commands that are not plays today, and says the merge returns "to main", though an issue in a plan lands on its plan's branch. The published cheat sheet is updated by hand: "Nothing owns keeping it current." Planned: keeping Garura's docs and command pages in step with what ships, with a guard that fails when the cheat sheet and the plays disagree.

## Inputs / Outputs
- In: the change's diff, and the commands it adds, renames, retires or changes.
- In: the docs and command pages that name those commands.
- In: the list of commands the project has, such as the plays a person can type.
- Out: the docs and command pages, changed in the same change.
- Out: the lint's result: a failure that names each page and each command that disagree, or a pass.

## Rules & behavior
- The pages change in the same change as the command. The reason: a page changed later is a page wrong until then, and "something keeps them in step when a play changes".
- A machine check holds the names, the set and the count. The reason: "There is a mechanical guard that fails when the cheat sheet and the plays disagree", and a judgment line alone did not stop the drift.
- The check runs with the normal lint. The reason: "The guard runs as part of the normal component lint, not as a separate thing to remember".
- What each command does is read in the review with the change. The reason: a machine can check a name, but not that the words still describe the command.
- Not decided: where the command pages live and how the check reads them, because Garura's published cheat sheet sits outside the repository.

## Acceptance criteria
- Given a change that renames a command, when the lint runs while a docs page still names the old name, then the lint fails and names the page. This is not built.
- Given a change that adds a command no page names, when the lint runs, then it fails and names the command. This is not built.
- Given a command page with a count of commands, when a command is retired and the count is not changed, then the lint fails. This is not built.

## Out of scope
- Reviewing the docs' words with the change. Check the code against its standards, in Code → Validation, does it.
- The lint itself and its other rules. Standards, structure, settings and memory owns it.
- The guides an install lays into a project. Install into a project owns them.

## Sources
- The product owner on 2026-11-10: "Ship every change the same way: Every change goes from opening to merge through the same steps, with a self-review, an outside review and a person's yes.", "yes, record it with self-review dropped"
- standards/rules/self-review.md, in Phoenix memory: "Docs in step."
- knowledge/review/docs.md, in Phoenix memory: "the PR changes human-facing prose that is not a decision record"
- docs/components/plays.md: "Merge the approved PR, return to main, delete the branch", "| `implement` |", "| `launch` |"
- The capability list: "Not on this list: [the docs feature] (Garura's docs and command pages stay in step with what ships), brought to the review of Developer tooling."
