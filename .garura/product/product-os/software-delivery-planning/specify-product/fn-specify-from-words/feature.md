# Feature: Specify from plain words

## What it does
A person's words are kept byte for byte.

Status: built.

## Agent intent (ICE)
- Goal: A person's words are kept byte for byte.
- Limit: The words are never edited.
- Fails if: The kept text differs from what they typed.
- Context: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what they typed.
- Checked by: The saved text matches exactly.
