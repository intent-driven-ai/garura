# Feature: Specify from plain words

## What it does
A person types what they want, with no file or link. The agent running the work writes those exact words into a working file. A script then copies this file byte for byte into the run's evidence. The kept text is the Source, and the run drafts its intents from it. Nothing edits the kept text after that.

Status: built.

## Inputs / Outputs
- In: what the person typed, held in a working file, and who gave it.
- Out: the kept text, byte for byte.
- Out: the capture record, with the kind "statement".

## Rules & behavior
- The work has two steps. The agent writes the typed words into the working file, and then a script makes the copy. Only the second step is mechanical.
- The agent's closing check asks that the kept text match the person's words. No script compares the kept text with the message the person typed.
- A missing working file fails the capture.
- What the person says later goes in the answers record. The kept text stays as it was.

## Acceptance criteria
- Given typed words with line breaks and odd spacing, when they are captured, then the kept text matches the working file byte for byte and the record reads "statement".
- Given no working file at the path, when the capture runs, then it fails and the record names the path.
- Given a person who answers a later question, when the answer is recorded, then the kept text's fingerprint has not changed.

## Out of scope
- A file the person attaches. Specify from a document (fn-specify-from-document) does this.
- Turning the words into intents. Specify intents (fn-specify-intents) does this.

## Sources
- The product owner approved this page and its ICE on 2026-11-06.
- core/components/plays/discover-intent/scripts/capture_source.py: "the exact text, byte for byte"
- core/components/plays/discover-intent/SKILL.md: "first write the person's exact words to", "matches the person's words byte for byte"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "the exact text for a statement"
