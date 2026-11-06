# Feature: Specify from a document

## What it does
A document is kept exactly as given.

Status: built.

## Agent intent (ICE)
- Goal: A document is kept exactly as given.
- Limit: It's never changed or summarised in place.
- Fails if: The copy differs from the original.
- Context: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the document.
- Checked by: The saved copy matches by its fingerprint.
