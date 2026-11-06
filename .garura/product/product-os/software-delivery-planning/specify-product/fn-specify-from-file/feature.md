# Feature: Specify from a file

## What it does
A person gives one web-page file, which is a file whose name ends in .html or .htm. The run saves an exact copy of it. A browser with no window then opens the file and saves the first screen and each view, each as a full-page picture and its visible text. A view is what a prototype shows after a click, such as the content of a tab. A person can then see the prototype again without the original file.

Status: built.

## Inputs / Outputs
- In: the file's path, and who gave it.
- In: any more pages to capture, and any named controls to click on the first page. Both are optional.
- Out: the exact copy of the file.
- Out: a full-page picture and the visible text of the first screen and of each new view.
- Out: the capture record, with the kind "prototype — file" and how many views were found and kept, and each view not reached with why. The record also holds a fingerprint of each saved file. A fingerprint is a short code worked out from a file's bytes, so any change to the file changes the code. The run does not compare it with the original. A test can, to show the copy is exact.

## Rules & behavior
- It finds views the same way as Specify from a deployed site (fn-specify-from-site), with the same limits and the same skipped controls.
- The browser goes two clicks deep. It clicks each control on the first screen, then each new control those views add.
- A view is found when a click reaches it. It is kept when its visible text differs from each view already kept. So a control that shows a repeat counts as found, and is not kept again.
- The size limit is 40 views beyond the first screen, or 160 clicks. Each control not tried then goes on the record as not reached, with the limit as the reason.
- A click that fails goes on the record as not reached, with the error, and the browser goes on to the next control.
- The browser does not follow mail, phone or script links, or any link that starts with http or https. It follows relative links.
- A named control is clicked with no word test. A named control that cannot be found fails the capture.
- The browser does not click a control with any of these words: accept, approve, reject, drop, send back, delete, remove, edit, comment, finish, submit, undo, save, reset, log out, sign out, point, upload, pay, buy. The test also finds these words inside longer words, and the record does not list the controls it skipped.
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
- core/components/plays/discover-intent/scripts/capture_source.py: "Find every view the page offers, two clicks deep", "a control whose view repeats one already kept is found but not kept again", "MAX_VIEWS = 40", "MAX_CLICKS = 160", "the exploration limit was reached", "record it, keep exploring", "leaves the prototype", "Controls that answer or change data rather than show a view: never clicked while exploring.", "a named control that cannot be found is a failure, not a skip", "def sha256(path):"
- core/components/plays/discover-intent/reference/ice.md: "The Source is kept as it was when read"
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "A fingerprint is a short code worked out from a file's bytes, so any change to the file changes the code."
