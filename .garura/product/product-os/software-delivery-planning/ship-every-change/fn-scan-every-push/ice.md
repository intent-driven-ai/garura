Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Every push a change play makes is scanned first, over every file in the commits it pushes, and stops with nothing pushed when it finds a client or company name from the project's protected list, a personal reference, or a home-folder path.
- Limit: The list of protected names never sits in a file in the repository.
- Limit: A found reference stops the push; it is never only a warning.
- Limit: No push of a change play skips the scan, its own records included.
- Fails if: A push reaches the code host with a client, company or personal reference, or a home-folder path, in it.
- Fails if: The list of protected names is found in the repository or its history.
- Fails if: A change play pushes without the scan having run.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the commits about to be pushed and every file in them, the place outside the repository where the project keeps its protected names, and the shapes of a personal reference and a home-folder path.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, whose rule is that no client and no personal reference is in a file or in the history.
- Scope: In: the scan before each push by a change play, the stop, and its message. Out: secrets in a commit, the review's check against the project's rules, and writing the rule into memory.

## Expectation
- Scenario: In a consultancy's product repository, the review's own record names the client the work is for. When the review pushes its records, the scan stops the push and names the file and the line; nothing reaches the code host. After the line is fixed, the push goes through.
- Done means: Someone other than the one who pushed plants a protected name and a home-folder path in two test commits, sees both pushes stopped with the file and line named and nothing on the code host, and sees a clean push go through.
