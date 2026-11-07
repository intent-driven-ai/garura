# Feature: Read back what a person gave

## What it does
Proves that each Source a person gave can still be read exactly as it was when read.
- A Source is a saved copy of what a person gave: a file, a project folder, a deployed site, a document, or their own words. When Specify the product reads one, its capture saves the files with the run's evidence, the folder where a run keeps what it read and did, and writes a capture record. The record holds a fingerprint of each saved file: a short code worked out from the file's bytes, so any change to the file changes the code.
- This feature reads each kept Source back. Each saved file must still be there, and its fingerprint must still match the capture record.
- It also checks the link both ways: each Source's record names the intents it shows, and each of those intents still names the Source.
- The feature exists because a Source is the person's own words or work, and later steps go back to it instead of the original, which may be gone.

Status: not built. The fingerprints are written at capture, and no step checks them later.

## Inputs / Outputs
- In: each kept Source: its saved files, its capture record and its Source record.
- In: the intent pages that the Source records name.
- Out: for each Source, whether it reads as given, and for each file that does not, which file and whether it is missing or changed.
- Out: each link between a Source and an intent held on one side only.

## Rules & behavior
- It reads only and never repairs a Source. The reason: a Source is kept as it was when read and never changes afterwards, so a repaired copy would no longer be what the person gave.
- A missing or changed file is named to a person. The reason: only the person can give the original again.
- A rewritten intent that lost its list of Sources is named too. The reason: today a rewrite of an intent page drops that list, so the link back to what the person gave is held on the Source's side only.
- It does not judge whether the Source was used well. That belongs to Specify the product.

## Acceptance criteria
- Given a kept Source whose files are untouched, when the read-back runs, then it reads as given.
- Given a kept Source with one saved file changed by a single byte, when the read-back runs, then it names that file as changed.
- Given an intent whose page no longer lists a Source that names it, when the read-back runs, then it names the intent and the Source.

## Out of scope
- Capturing a Source at the moment it is read. The Specify-from features of Specify the product do it.
- Checking that what was given was fully used. Validate the attribution (fn-validate-attribution) will do it.
- Naming drift between an intent and the product. Name an intent's drift (fn-name-intent-drift) will do it.

## Sources
- The one line the product owner approved on 2026-11-03: "Everything a person gives is kept exactly as given"
- .garura/product/product-os/intents/bi-1.md: "Everything a person gave can still be read as given."
- core/components/plays/discover-intent/scripts/capture_source.py: "keep a Source exactly as it was when read", "def sha256(path):"
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "A fingerprint is a short code worked out from a file's bytes, so any change to the file changes the code.", "The reason: the Source must outlive the link or the file."
- core/components/plays/discover-intent/scripts/persist_intent.py: "one Source record per Source (kind, read on, snapshot, what it", 'lines.append("**Sources:**")'
- standards/schemas/product-os/ontology.md, in Phoenix memory: "It is kept as it was when read; the snapshot never changes afterwards."
- A rewrite through author-intent-page, tried on a throwaway copy of a page saved by discovery: the Sources block was gone afterwards.
