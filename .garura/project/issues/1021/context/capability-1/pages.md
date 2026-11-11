# Capability 1: approved by the product owner on 2026-11-03

Common Context, for the capability and every feature: "Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: <what it looks for>."

## Capability: Specify the product (cap-specify-product, folder specify-product, serves bi-1, domain dom-software-delivery-planning)
One line: The product is understood from what a person gives, whether a video, a prototype, a brief or all of those, and becomes confirmed intents, domains, capabilities and features.
What makes it unique: it starts from something that works, not from a written spec.
- Goal: What a person gives becomes a confirmed understanding of the product, at the depth the product owner chooses.
- Limit: What a person gives is the input, never the intent. An intent must allow more than one way to build it, so nothing copies how the source does it.
- Limit: Nothing without a basis. Every title, outcome and limit traces to the source, to memory or to the person's own answers.
- Limit: Only a person confirms an intent.
- Limit: Each kind can be written on its own, and no part waits for another to run first.
- Limit: The one who does the work reviews it first, and then a judge with no context checks it. The doer's own review never counts as the check.
- Fails if: A source couldn't be read and the work went on anyway.
- Fails if: An intent describes the source (its screens, fields or copied text) instead of the outcome the person wants.
- Fails if: A value appears that neither the source nor the person gave, with no basis named.
- Fails if: A part of what was given that matters isn't attributed, and the judge can't see that it was read.
- Fails if: Something already in the model is written as new, or a clash between intents isn't shown to a person.
- Context looks for: what the person gave, the intents, domains and capabilities already in the model, and what's known about the product's field.
- Checked by: `rebuild-eval` runs discovery on a prototype and tests the result: each intent has its outcome, why, asked by, proof and sources, and the domain is a real one. A judge with clean context gets only what was given and the attribution record, and says what was missed. A person sees each thing sorted, with what it touches.

## Features (each serves bi-1, capability cap-specify-product)

### fn-specify-intents: Specify intents. Status: built, except reading existing intents and writing attribution.
- Goal: What a person gives becomes the right business intents, at the depth the product owner chooses, each confirmed by them.
- Limit: One need is one intent, and it can hold several features. Transitional parts aren't intents.
- Limit: It writes business intents and their sources only.
- Fails if: An intent is confirmed without the person's typed word, or a part that matters wasn't considered.
- Context looks for: what was given, the existing intents, the depth preference.
- Checked by: A person sees every part considered, each as an intent or with the reason it isn't one.

### fn-specify-domains: Specify domains. Status: built.
- Goal: Each domain the product sits in has a detailed page.
- Limit: It writes domains only, and never invents one. Research must show the world recognises it.
- Fails if: A page fails its template or the content check, or it writes a capability.
- Context looks for: the intents, what was captured, the domain shelves.
- Checked by: A clean-context judge and the structure check.

### fn-specify-capabilities: Specify capabilities. Status: built.
- Goal: Each capability the product needs has a detailed page with its features and ICE.
- Limit: A new capability comes from the person's answers or from what the screens show, never invented.
- Limit: Each ICE meets the rubric.
- Fails if: A capability has no basis, or a page fails its template, the content check or the rubric.
- Context looks for: what was captured, the capability's shelf, the person's answers.
- Checked by: A clean-context judge and the structure check.

### fn-specify-from-journeys: Specify from a prototype's journeys. Status: built.
- Goal: Each journey through a prototype is walked and recorded, the way its people would use it.
- Limit: It never changes data on a deployed site unless the person said that's safe.
- Fails if: A view it could reach isn't kept, or one it couldn't reach isn't recorded with why.
- Context looks for: the prototype, the person's write-up.
- Checked by: Every captured view sits on a journey or is named as not walked.

### fn-specify-from-video: Specify from a video. Status: to build.
- Goal: What a video shows is captured, so intents can trace to moments in it.
- Limit: The video is kept as given.
- Fails if: Its contents are guessed, or a part that matters wasn't read.
- Context looks for: the video, any notes given with it.
- Checked by: Validate the attribution.

### fn-specify-from-file: Specify from a file. Status: built.
- Goal: A file is kept, and every view it offers is captured.
- Limit: The copy never changes.
- Fails if: A view it could reach isn't kept.
- Context looks for: the file.
- Checked by: Each view is saved with its picture and text.

### fn-specify-from-folder: Specify from a project folder. Status: built.
- Goal: A project is captured from its written docs and its running app.
- Limit: It starts the app as the README says, and stops it afterwards.
- Fails if: The app runs but isn't captured.
- Context looks for: the folder, its README.
- Checked by: Both the docs and the app are saved as sources.

### fn-specify-from-site: Specify from a deployed site. Status: built.
- Goal: Every view a deployed site offers is captured, up to two clicks deep.
- Limit: It never changes data or follows a link out of the prototype.
- Fails if: A view it couldn't reach isn't recorded with why.
- Context looks for: the site.
- Checked by: Each view is saved, or named as unreached.

### fn-specify-from-document: Specify from a document. Status: built.
- Goal: A document is kept exactly as given.
- Limit: It's never changed or summarised in place.
- Fails if: The copy differs from the original.
- Context looks for: the document.
- Checked by: The saved copy matches by its fingerprint.

### fn-specify-from-words: Specify from plain words. Status: built.
- Goal: A person's words are kept byte for byte.
- Limit: The words are never edited.
- Fails if: The kept text differs from what they typed.
- Context looks for: what they typed.
- Checked by: The saved text matches exactly.

### fn-validate-attribution: Validate the attribution. Status: to build.
- Goal: A judge with no context says whether what was given was fully and correctly used.
- Limit: The judge sees only the source and the attribution record, never the doer's reasoning.
- Fails if: A missed part passes the judge.
- Context looks for: the source, the attribution record.
- Checked by: Plant a known omission, and the judge names it.

### fn-specify-against-existing: Specify against what exists. Status: to build.
- Goal: What's given is sorted against what exists: a new intent, an enhancement, a new feature under one, or a clash.
- Limit: A person decides any clash, and nothing existing changes on its own.
- Fails if: Something that exists gets written as new.
- Context looks for: the model, the project, its code.
- Checked by: Give it something overlapping an existing intent, and it says so.
