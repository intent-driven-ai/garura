## Intent
- Goal: Argus runs as a small server that a person starts once, on a laptop or a hosted place, with its own folder, guide, tests and version and no Garura code, and Garura reaches it only at the one address its settings name, through a written, versioned contract of the review pack, the requests and the numbered events, so Argus can serve Garura and move, into Griffin later, by moving its folder and changing that address.
- Limit: Argus imports no Garura code, reads no Garura path and names none of Garura's kinds in its code; they arrive as data.
- Limit: Garura never starts Argus, and on a laptop Argus listens only on that machine, with a token.
- Limit: Every action is a numbered event that can be read again from any number.
- Fails if: A file in Argus's folder names Garura's folders, imports from outside the folder, or names a Garura kind in its code.
- Fails if: Moving Argus needs a change in Garura beyond the one address.
- Fails if: A listener that asks for the events after a number misses one, or a pack that breaks the contract is accepted.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the contract and its version, Argus's settings, the address in Garura's settings, and the example packs.
- Never read: any memory file by its path, any ICE page, Garura's code from inside Argus, and production.
- Persona: the product owner, who starts Argus once and points Garura at it.
- Scope: In: the contract, the server and its requests, the numbered events, the store, the settings from outside, the boundary check, and the one address in Garura's settings. Out: building the pack, the pages a person reads and answers in, and moving Argus into Griffin.

## Expectation
- Scenario: A person building a recipe app alone starts Argus on their laptop, and the project's settings name its address. A review opens; the laptop sleeps and the listener asks for the events after number 40, and gets every later one. Months later Argus moves to a hosted place behind its own sign-in; only the address in the project's settings changes, and the next review opens there.
- Done means: Someone other than the one who built Argus runs its boundary check, checks the two example packs against the contract, reads events again from a given number, and moves Argus to a new address, and finds no Garura code or path in Argus, both packs passing, no event missed, and nothing in Garura changed but the address.
