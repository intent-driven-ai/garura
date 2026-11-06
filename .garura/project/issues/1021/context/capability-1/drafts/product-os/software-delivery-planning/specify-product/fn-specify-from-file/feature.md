# Feature: Specify from a file

## What it does
A person gives one web-page file, which is a file whose name ends in .html or .htm. The run saves an exact copy of it. A browser with no window then opens the file and saves the first screen and each view, each as a full-page picture and its visible text. A view is what a prototype shows after a click, such as the content of a tab. A person can then see the prototype again without the original file.

Status: built.

## Inputs / Outputs
- In: the file's path, and who gave it.
- In: any more pages to capture, and any named controls to click on the first page. Both are optional.
- Out: the exact copy of the file.
- Out: a full-page picture and the visible text of the first screen and of each new view.
- Out: the capture record, with the kind "prototype — file" and how many views were found and kept, and each view not reached with why.

## Rules & behavior
- It finds views the same way as Specify from a deployed site (fn-specify-from-site), with the same limits and the same skipped controls.
- It skips those controls here too, although a local file holds no real data to change. So a view behind "Edit" is not captured here. A journey can still open it (fn-specify-from-journeys).
- Only a web-page file takes this path. Specify from a document (fn-specify-from-document) takes any other file.

## Acceptance criteria
- Given a web-page file with three controls that each open a different view, when it is captured, then the run keeps the exact copy, four pictures and four texts, and the record reads four kept.
- Given a web-page file, when it is captured, then the fingerprint of the copy equals one worked out from the original.
- Given a path with no file, when the capture runs, then it fails and the record names the path.
- Given a file whose name ends in .txt, when the capture runs, then the record reads "document" and the run saves no pictures.

## Out of scope
- A project with many files. Specify from a project folder (fn-specify-from-folder) does this.
- A site on the web. Specify from a deployed site (fn-specify-from-site) does this.
- Walking the prototype as its people would. Specify from a prototype's journeys (fn-specify-from-journeys) does this.

## Sources
- The product owner approved this page and its ICE on 2026-11-06.
- core/components/plays/discover-intent/scripts/capture_source.py: "a copy of the file + a rendered screenshot of every view"
- core/components/plays/discover-intent/SKILL.md: "An HTML file is copied and rendered"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "a copy of the file for a file or a document"
