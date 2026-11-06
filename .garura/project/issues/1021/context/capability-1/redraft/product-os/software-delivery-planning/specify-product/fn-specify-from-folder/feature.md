# Feature: Specify from a project folder

## What it does
A person gives a project folder. The run treats it as two Sources: the project's written docs and its running app. It keeps the docs first. It then starts the app the way the README (the project's main instruction file) says, captures the running app the way it captures a deployed site, and stops the app. The intent draft reads both Sources together. A Source is a saved copy of what a person gave, which later steps read instead of the original. A folder gives two because a runnable source is also run through, so what it does is seen, not only what its docs say. The intent draft is the first version of the business intents, which the person then confirms or drops.

Status: built.

## Inputs / Outputs
- In: the folder's path, and who gave it.
- In: the README's words on how to start the project.
- Out: the docs Source: a copy of each written doc at the top of the folder. Its capture record reads "prototype — project". A capture record is what each capture writes about its Source: its kind, the date it was read, who gave it and its saved files.
- Out: the app Source: what Specify from a deployed site (fn-specify-from-site) saves for the running app. Its capture record reads "prototype — deployed site".

## Rules & behavior
- The run keeps only files that end in .md or .txt at the top of the folder. It skips subfolders and links to other files. So a doc in a subfolder or in another format is not kept.
- A folder with no such file fails the capture.
- The agent running the work starts and stops the app by following the README. No fixed script does this, and no check confirms that the app stopped. So an app left running after the capture is not caught.
- Each capture is checked on its own. No check confirms that a project has both Sources.
- An app that does not start fails its capture, as any source does that cannot be run through.
- Both Sources link to every intent the run confirms. An intent is confirmed when the person types confirm for it.

## Acceptance criteria
- Given a folder with README.md, NOTES.txt and app.js at its top, when it is captured, then the docs Source holds README.md and NOTES.txt and does not hold app.js.
- Given a folder with no .md or .txt file at its top, when it is captured, then the capture fails and the record names the folder.
- Given a README that says how to start the project, when the run ends, then two Source records exist and each names every confirmed intent.

## Out of scope
- Reading the project's code. Specify against what exists (fn-specify-against-existing) will read it, and it is not built.
- Finding the running app's views. Specify from a deployed site (fn-specify-from-site) does this.
- A single web-page file. Specify from a file (fn-specify-from-file) does this.

## Sources
- The product owner approved this page and its ICE on 2026-11-06.
- core/components/plays/discover-intent/scripts/capture_source.py: "a copy of its top-level written docs (README, SPEC, *.md, *.txt)", "the project folder has no top-level written docs to keep"
- core/components/plays/discover-intent/SKILL.md: "start the project the way its README says", "Both Sources link to every intent the run confirms."
- core/components/plays/discover-intent/reference/ice.md: "A project folder is two Sources (its written docs and the running app)"
- core/components/plays/discover-intent/reference/ice.md: "a runnable source is also run through, so what it does is seen, not only what it says", "becomes `confirmed` only on the person's typed confirmation"
- core/components/plays/discover-intent/SKILL.md: "draft the person's Business Intents from these sources and their answers", "ask the person to type one of"
- core/components/plays/discover-intent/scripts/capture_source.py: "takes its snapshot into the run's evidence folder, so it outlives the link or the file, and writes the source manifest"
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "Later steps read this copy, so they do not need the original."
