# Feature: Read what a run made, as business intents with their ICE and as the product

## What it does
When a review opens, the person reads, in one calm page, the whole model's approval state first, then what the run changed: each business intent with the ICE under it, and the product as domain, capability and feature, then its limits and its decisions, each piece in plain words with what changed and why, so they judge what was made without reading a file.
- The overview comes first: a big plain headline, such as "Kickoff changed 3 intents and 14 parts of the product."; one row of numbers, Added, Changed, Removed, Answered and Waiting for you; the whole model's counts, approved, changed and in progress; and a "Needs you" list of the pieces still without an answer, intents first.
- The Intents section lists each business intent with its ICE under it, as pieces of their own. An ICE is answered here; the Product section shows the same lines to read only, with a link, "so nothing is answered twice".
- The Product section lists the product as domain, capability and feature, then the limits, then the decisions.
- Two switches change the view: Final or Changes (the clean text, or the words removed and added marked inside each sentence), and Only changed or Everything. "Only changed" means everything not approved, and the default is Only changed with Changes, "because that is the review".
- Each piece shows its title, its kind and what changed, one line on why, its sections in reading order, its approval state, and links that jump between Intents and Product.
- The page reads well on a laptop and on a phone.
- Examples, in different kinds of project:
  - A shop's checkout: the review shows two new intents with their ICE, and under Product a new capability for guest checkout with three features.
  - A school's timetable app: one intent's proof changed, and in Changes the person sees the old proof struck through and the new words marked.
  - A bank's payments service: the person picks Everything, to read the whole product as it stands, and sees which parts are approved and which changed since.
- How it meets the capability: this is the reading half of the capability's line for the business intents, their ICE and the product: what the person reads before answering each piece.

Status: not built. The design and its mockup show it, the mockup with "made-up shop data", and the Discovery loop's test runs read the mockup as a prototype. No page of Argus is built.

## Inputs / Outputs
- In: the review pack: each piece with its kind, words before and after, approval state, links, place and why it changed.
- In: the whole model's approval state, for the counts.
- In: the answers so far, for the ticks and the "Needs you" list.
- Out: the pieces shown, to read only. Reading writes nothing.

## Rules & behavior
- The outcome, not the plays, and not the plan. The reason: the person reviews what changed "in the business intents" and "in the product model", and "The plan is not reviewed here."
- The whole model's state, each time it opens. The reason, in the product owner's words: "Every time somebody opens up this tool, they should be able to see what is changed, what is approved, and what is in progress."
- The final words and the changes, and everything or only what changed, one switch away. The reason, in his words: "the full model, the full set of intents, the final version, the changes to the version. The user can swap between the two."
- Plain words, no files. The reason: "No file paths, no field names, no YAML."
- An ICE is answered in one place only. The reason: "so nothing is answered twice".
- Light on the person: what did not change is hidden unless asked, long sections fold, counts are always in view. The reason, in his words: "We don't want it to be a massive PR and add complex cognition load on the user."
- Section headings come from the page templates. The reason: "Section headings come from the page templates and cannot be edited."
- Not decided: whether a product decision that waits for a person is read under the Product section's decisions or in the ADRs section.

## Acceptance criteria
- Given a review opens, when the overview shows, then it gives the whole model's counts of approved, changed and in progress before what this run changed. This is not built.
- Given a run that changed an intent and its ICE, when the person opens Intents, then the ICE is listed under its intent, and Product shows the same lines to read only, with a link to answer them in Intents. This is not built.
- Given a piece whose words changed, when Changes is on, then the removed words are struck through and the added words marked inside the sentence; when Final is on, only the clean text shows. This is not built.
- Given a phone about 400 pixels wide, when the review opens, then every piece can be read without scrolling sideways. This is not built.

## Out of scope
- Answering a piece. Answer each piece, in the page or one card at a time (fn-answer-pieces) does it.
- The ADRs, Memory and Agent decisions sections. Accept or send back each ADR that waits for a person (fn-review-adrs), See what memory holds, and approve or reject each memory update that waits for a person (fn-review-memory), and Check each agent decision against the memory it rested on (fn-check-agent-decisions) cover them.
- Building the pack. Open a review on what a run changed, and keep every answer on the run's branch (fn-open-review) does it.
- A dark page. The design is light only.

## Sources
- The review tool's design, with the product owner's words: "the full model, the full set of intents, the final version, the changes to the version. The user can swap between the two.", "Every time somebody opens up this tool, they should be able to see what is changed, what is approved, and what is in progress.", "We don't want it to be a massive PR and add complex cognition load on the user.", "Kickoff changed 3 intents and 14 parts of the product.", "so nothing is answered twice", "because that is the review", "No file paths, no field names, no YAML."
- The review tool's mockup: "made-up shop data", "Needs you", "Waiting for you"
- docs/adr/032-drive-review-of-outcomes.md: "in the business intents", "in the product model", "The plan is not reviewed here."
- docs/adr/033-approval-in-the-product-model.md: "Only changed" means "everything not approved".
- docs/adr/041-a-drive-runs-in-rounds-and-owns-its-questions.md: "after Kickoff runs 1–5 on the Argus mockup"
