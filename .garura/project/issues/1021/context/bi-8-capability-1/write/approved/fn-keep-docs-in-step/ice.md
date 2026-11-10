## Intent
- Goal: Each change that adds, renames, retires or changes a command brings, in the same change, the docs and command pages that describe it, and a check run with the normal lint fails the change while a page names a command that does not exist, misses one that does, or gives a count that is not the count there is.
- Limit: The pages change in the same change as the command, never later.
- Limit: The check runs as part of the normal lint, not as a separate step.
- Limit: The check holds names, the set and counts; the words on what a command does are read in the review.
- Fails if: After a merge, a page names a command that does not exist, or a command exists that no page names.
- Fails if: A page's count of commands is not the count there is.
- Fails if: A change alters what a command does and lands with its page still saying the old thing.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the commands the change adds, renames, retires or changes, the list of commands the project has, and every docs and command page that names them.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, whose change brings the pages it alters; and the product owner, who reads the docs and command pages to know what each command does today.
- Scope: In: the pages changed with the change, and the lint check of names, set and counts. Out: the review of the docs' words, the lint's other rules, and the guides an install lays.

## Expectation
- Scenario: In a harness repository, a developer renames a play and retires another. The lint fails while the docs table still names the old name and the cheat sheet still lists the retired play with the old count. The same change fixes both pages, the lint passes, and the change lands.
- Done means: Someone other than the developer compares the list of plays with every docs and command page after the merge, and finds each play named, no retired play listed, and every count right.
