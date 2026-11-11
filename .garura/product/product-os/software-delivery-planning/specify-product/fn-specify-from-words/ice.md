## Intent
- Goal: A person's words are kept byte for byte.
- Limit: The words are never edited.
- Fails if: The kept text differs from what they typed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what they typed.
- Persona: the product owner typing what they want.
- Scope: In: the typed words, kept byte for byte. Out: a file the person attaches, and turning the words into intents.

## Expectation
- Scenario: Typed words with line breaks and odd spacing are kept byte for byte.
- Done means: The saved text matches exactly.
