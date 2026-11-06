# Feature: Specify from a document

## What it does
A person gives a document, such as a brief or a PDF. The run saves an exact copy under the document's own name, with the run's evidence, so the document outlives the original file. The run's evidence is the folder where a run keeps what it read and did, committed with its change. At this step the run does not open or read the document. A later step reads the copy and writes what it shows in a separate record beside the copy.

Status: built.

## Inputs / Outputs
- In: the file's path, and who gave it.
- Out: the exact copy, under the document's own name.
- Out: the capture record, with the kind "document".

## Rules & behavior
- Any file whose name does not end in .html or .htm counts as a document. The reason: a web-page file is a prototype, and Specify from a file (fn-specify-from-file) captures it view by view in a browser. A video counts too, so today a video is only copied. Reading one belongs to Specify from a video (fn-specify-from-video), and it is not built.
- The capture does not open the file. The reason: this step only keeps and records, and saying what a document shows is judgment that a later step does. So a damaged file, or a format no later step can read, passes this step.
- The capture record holds the fingerprint of the saved copy. A fingerprint is a short code worked out from a file's bytes, so any change to the file changes the code. No step works out the original's fingerprint or compares the two. So the run cannot tell when the copy differs from the original.
- What the document shows goes in the Source record, beside the copy. The copy itself stays as it was.

## Acceptance criteria
- Given a brief in a file, when it is captured, then the record reads "document" and holds the copy's fingerprint, which equals one the test works out from the original.
- Given a path with no file, when the capture runs, then it fails and the record names the path.
- Given a file whose name ends in .html, when the capture runs, then the record does not read "document".
- Given a captured document, when the intents are saved, then the Source record sits beside the copy and the copy's fingerprint has not changed.

## Out of scope
- A web-page file. Specify from a file (fn-specify-from-file) does this.
- Saying what the document shows, and drafting intents from it. Specify intents (fn-specify-intents) does this.
- Reading the moments in a video. Specify from a video (fn-specify-from-video) will do this, and it is not built.

## Sources
- The product owner approved this page and its ICE on 2026-11-06.
- core/components/plays/discover-intent/scripts/capture_source.py: "document (any other file) a copy of the file"
- core/components/plays/discover-intent/scripts/persist_intent.py: "one Source record per Source (kind, read on, snapshot, what it"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "It is kept as it was when read; the snapshot never changes afterwards."
- core/components/plays/discover-intent/SKILL.md: "Each Source's snapshot goes to the issue's evidence folder", "committed with the run, so it outlives the link or the file", "An HTML file is copied and rendered"
- core/components/plays/discover-intent/scripts/capture_source.py: "a copy of the file + a rendered screenshot of every view", "is judgment and is filled in later by the play; this script only keeps and records"
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "A fingerprint is a short code worked out from a file's bytes, so any change to the file changes the code."
