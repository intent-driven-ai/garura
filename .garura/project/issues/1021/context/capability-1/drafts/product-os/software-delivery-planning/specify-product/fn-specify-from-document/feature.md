# Feature: Specify from a document

## What it does
A person gives a document, such as a brief or a PDF. The run saves an exact copy under the document's own name, with the run's evidence, so the document outlives the original file. At this step the run does not open or read the document. A later step reads the copy and writes what it shows in a separate record beside the copy.

Status: built.

## Inputs / Outputs
- In: the file's path, and who gave it.
- Out: the exact copy, under the document's own name.
- Out: the capture record, with the kind "document".

## Rules & behavior
- Any file whose name does not end in .html or .htm counts as a document. A video counts too, so today a video is only copied. Reading one belongs to Specify from a video (fn-specify-from-video), and it is not built.
- The capture does not open the file. So a damaged file, or a format no later step can read, passes this step.
- The capture record holds the fingerprint of the saved copy. No step works out the original's fingerprint or compares the two.
- What the document shows goes in the Source record, beside the copy. The copy itself stays as it was.

## Acceptance criteria
- Given a brief in a file, when it is captured, then the fingerprint of the copy equals one worked out from the original and the record reads "document".
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
