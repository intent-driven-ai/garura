# Feature: Update an intent from approved words

## What it does
Rewrites a business intent's page from words a person approved, or changes only the lines a person approved, and keeps the intent's record of what was done.
- A business intent is what a person or the organisation wants, in their own words. Its page in the product model holds its title, the outcome, why it matters, who asks for it (a persona, such as "the product owner"), the proof it is met, any limits and rules, its stage, its issue in the tracker, the parts it touches and what was done for it. The stage is proposed until a person confirms it.
- An intent is updated when the person's view of what they want changes, often because the product was built or changed. Whoever first specifies the intent writes its first page; this feature changes it after that.
- It also writes the page of a new intent that replaces or splits an old one, from approved words. Replace or retire an intent (fn-replace-or-retire-intent) then moves the parts.
- There are two ways to change an intent page:
  - The whole page. The skill author-intent-page puts an approved draft on the page in one fixed order, and drafts nothing of its own.
  - A few lines. The page skill (enrich-grounding) changes exactly the lines a request names, to the words it gives, and keeps every other line word for word. For example, a real person's name becomes a persona.
- The same page skill updates a domain, capability or feature page, and an ICE page, from approved words: a few named lines, or a whole page a person approved, copied word for word. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. The spec is more than its intents, so a part's page that no longer matches the work is updated the same way.
- The feature exists because the spec must follow the product as it changes, and each change to what a person wants must be that person's.

Status: built. A rewrite of an intent page drops the intent's list of Sources, which is not fixed yet.

## Inputs / Outputs
- In: the draft of the intent: its id, its issue number, title, outcome, why, asked by and proof lines, and when given, its limits, rules, the intent it serves, the intent it was identified by, and the parts it touches. Its words are settled before this feature runs.
- In: whether the page is new or a rewrite, and, for a confirmed stage, the person who confirmed it.
- In, for a few lines: a named-lines request. It gives each line to change, whole and as it is on the page, its new words, and the request's source, such as an approved design or the person's own words.
- In, for a whole domain, capability, feature or ICE page: an approved-text request. It names each page, the file that holds its approved text, the person who approved it, and where that approval is recorded.
- Out: the intent page, written or rewritten, and a report that names the page, whether it was a rewrite, its stage, and the old blocks it kept.
- Out, for a few lines: a report that names each page and each line, old and new.
- Out, for an approved page: a report that names each page, whether it was created or replaced, and who approved it.

## Rules & behavior
- It drafts nothing. A required part left empty (title, outcome, why, asked by, a proof line) refuses the page. The reason: the words are the person's, so a gap the tool filled would put the tool's words in their place.
- It never confirms by itself. The stage reads confirmed only when the caller names the person who confirmed it. A rewrite that names nobody goes back to proposed, whatever the old page said. A draft part holding a line break refuses the page, so a draft cannot slip in a stage line of its own. The reason: only a person confirms or drops a business intent.
- It never overwrites by accident. A page that is there changes only when the caller asks for a rewrite, and a rewrite needs the page to be there. The reason: other work relies on a confirmed intent, so a new draft must not replace it by mistake.
- A rewrite keeps the record. The What-was-done block stays byte for byte. The Touches block, the list of parts the intent touches, stays too, unless the draft gives a new list, which replaces it. Everything else on the old page is replaced. The reason: the words are new, but what happened to the intent is history.
- Not built: a rewrite keeps the list of Sources. An intent saved by discovery lists the Sources it came from, and a rewrite drops that list. A Source is a saved copy of what a person gave, such as a file, a document or their own words. The rewritten intent then loses its link to what the person gave, while the Source records still name the intent, so the link is held on one side only.
- The id is the issue's. The page is named after its issue, as bi-1 for issue 1, and an id that does not match the issue refuses the page. The reason: the page and the issue are the same intent.
- Every Touches line can be followed. A bad kind or mark, an empty title, or a link that leads to no file inside the model refuses the page. The reason: a line nobody can follow tells nobody what the intent touches.
- A named-lines change is all or nothing. Each named line must be on its page exactly once, every check runs before the first write, and when a write fails every page already written is put back. The reason: half a change would leave a page saying something nobody approved.
- An approved page is copied word for word, all or nothing. It refuses a text that holds the thin mark, a part's page that holds an ICE section, an ICE page without its three parts (Intent, Context and Expectation), and a request that names no one who approved it. The reason: the page must be exactly what the person approved, and a part's ICE has its own page.
- It writes pages and nothing else. The part's side of a link in the model's index, and the thin mark, are another skill's work. The reason: each shared file then has one writer.

## Acceptance criteria
- Given an intent page that is there and a draft with no rewrite asked, when the skill runs, then it refuses and the page stays as it was.
- Given a rewrite of a confirmed intent that names no confirming person, when it runs, then the page reads proposed.
- Given a rewrite whose draft gives no Touches list, when it runs, then the old What-was-done and Touches blocks are on the new page byte for byte.
- Given a draft whose id is not its issue's, when the skill runs, then it refuses and writes nothing.
- Given a named-lines request whose old line is not on the page, when it runs, then nothing is written and the error names the page and the line.
- Given an approved-text request that names no one who approved it, when it runs, then nothing is written.
- Given an intent page saved by discovery with a list of Sources, when it is rewritten, then the list is still on the page. This is not built.

## Out of scope
- Writing an intent's first page from what a person gave. Specify intents (fn-specify-intents) does it in discovery, and /shape-slice, in Design slices, writes one from its issue when the model has none.
- Choosing the new words. The person approves them. Find where the spec and what's built no longer match (fn-find-spec-drift) will often be the reason they change.
- Linking a part to the intent in the model's index. Keep an intent's links current (fn-keep-intent-links-current) keeps the intent's side.
- The intent's issue in the tracker. Keep the tracker's words matched to the model (fn-keep-tracker-matched) does it.

## Sources
- core/components/skills/author-intent-page/SKILL.md: "It drafts nothing.", "It never confirms by itself.", "a rewrite with no stage goes back to proposed, whatever the old page said"
- core/components/skills/author-intent-page/SKILL.md: "A page that is there changes only with `rewrite`.", "A rewrite keeps the old page's What-was-done", "An id that is not `bi-<digits>`, or not `bi-<issue>`, refuses the page.", "Every Touches line can be followed and read back."
- core/components/skills/author-intent-page/SKILL.md: "Used through product-os-keeper by any play or run that has a person's approved words for an intent page."
- core/components/skills/author-intent-page/scripts/write_page.py: "It keeps the old page's What-was-done block", "Everything else"
- core/components/skills/enrich-grounding/scripts/change_lines.py: "exactly those lines and keeps every other line word for word", "Every named line must be on its page exactly once"
- core/components/skills/enrich-grounding/SKILL.md: "or a real person's name to a", "change of meaning is the person's or an approved design's"
- core/components/skills/enrich-grounding/scripts/write_approved.py: "This script copies each approved text to its page exactly as it is.", "It decides nothing and composes nothing.", "No text holds a Thin line", "`approved_by` names the person."
- core/components/plays/discover-intent/scripts/persist_intent.py: 'lines.append("**Sources:**")'
- A rewrite tried on a throwaway copy of a page saved by discovery: the Sources block was gone afterwards and only What was done was kept.
- core/components/plays/shape-slice/SKILL.md: "writes the intent page from the issue when the model has none"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or drops it; an agent never does."
