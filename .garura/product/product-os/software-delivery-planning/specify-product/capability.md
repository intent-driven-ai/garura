# Capability: Specify the product

## Directional intent
The product is understood from what a person gives, whether a video, a prototype, a brief or all of those, and becomes confirmed intents, domains, capabilities and features.

What makes it unique: it starts from something that works, not from a written spec.

Features: Specify intents (fn-specify-intents), Specify domains (fn-specify-domains), Specify capabilities (fn-specify-capabilities), Specify from a prototype's journeys (fn-specify-from-journeys), Specify from a video (fn-specify-from-video), Specify from a file (fn-specify-from-file), Specify from a project folder (fn-specify-from-folder), Specify from a deployed site (fn-specify-from-site), Specify from a document (fn-specify-from-document), Specify from plain words (fn-specify-from-words), Validate the attribution (fn-validate-attribution), Specify against what exists (fn-specify-against-existing).

## Agent intent (ICE)
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
- Context: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what the person gave, the intents, domains and capabilities already in the model, and what's known about the product's field.
- Checked by: `rebuild-eval` runs discovery on a prototype and tests the result: each intent has its outcome, why, asked by, proof and sources, and the domain is a real one. A judge with clean context gets only what was given and the attribution record, and says what was missed. A person sees each thing sorted, with what it touches.
