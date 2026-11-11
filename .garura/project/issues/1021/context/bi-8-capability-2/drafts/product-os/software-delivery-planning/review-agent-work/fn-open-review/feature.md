# Feature: Open a review on what a run changed, and keep every answer on the run's branch

## What it does
At the end of a loop's run, Garura works out what the run changed against where its branch lands, by meaning and not by file, builds the review pack, checks that Argus is up, starts the review and opens its link for the person; a listener then keeps every action the person takes as a file on the run's branch as it happens, so the answers become part of the run's work and no agent reads the web page.
- What the pack holds, for each piece the run added, changed or removed: its kind, its words before and after, section by section; its approval state; its links, such as an intent's Touches or a capability's intents; where it sits, such as a capability under its domain; and one plain line on why it changed, taken from the plays' review records. The plays themselves are never shown.
- What the pack holds for the run: its title, its branch and where it lands, the note of the loop's checker (the agent that did not run the loop and checks its result), and, for a run that stopped, where it stopped and why.
- By meaning: "The pack is outcome-shaped, not file-shaped." The one place a file shows is an agent decision's source, as text for the person to check.
- The listener runs in the background from the moment the review opens. For each event it adds one line to the run's event log and brings the answers so far up to date, both on the run's branch, and it prints one line, so the agent sees each action as it happens.
- Garura never starts Argus. It checks that Argus is up and names it when it is not.
- Examples, in different kinds of project:
  - A loop's run on a shop's checkout drafts two intents and a capability; the review opens on those pieces, each with why it changed.
  - A loop's run on a clinic's booking app stops at a question no play could answer; the review opens with where it stopped and why, beside what it made.
  - A team's planning tool is reviewed from a laptop that sleeps halfway; when the listener connects again, it gets every action it missed.
- How it meets the capability: this is where a run's outcome reaches the person, and where each answer becomes part of the work, as Developer tooling's proof asks: "Their answers become part of the work."

Status: not built. No part builds a pack, opens a review or listens, and no setting names Argus's address (#648). What exists covers only the inputs and a stand-in:
- Inside a loop, each play writes what its checkpoint would have shown into the loop's review folder, "so the loop's end review can read every play's record in one place", and the record reads "decided: false" until the loop's review answers it.
- Until Argus exists, the Discovery loop "ends at the pull request": the person types confirm or drop for each intent, the words are kept in the issue's short-term memory, and the intents stay proposed.

## Inputs / Outputs
- In: the run's branch, and the branch it lands on.
- In: the model's pages and its index on both branches, with each piece's approval state once Product model keeps it (#964).
- In: the plays' review records in the loop's review folder, and the checker's note; for a run that stopped, where it stopped and why.
- In: Argus's address, from Garura's settings.
- Out: the review pack, checked against the contract before it is sent.
- Out: the review, started in Argus, and its link opened for the person.
- Out: on the run's branch, the event log, one line for each action, and the answers so far.

## Rules & behavior
- By meaning, never by file. The reason: "The tool never sees a file path as something to open.", and Developer tooling must not "Make people read raw files to know what was made."
- The pack is checked against the contract before it is sent. The reason: "Garura keeps a test that checks the packs it builds against that schema, so a break shows up on the Garura side first."
- Every action is kept on the run's branch as it happens. The reason, in the product owner's words: "Every time a change is made, it should have a direct connection back to Garura for listening."; and "Claude still never reads the web page: the answers are files on the branch".
- No action is lost. The listener connects again from the last event number it saw and gets everything after it. The reason: "Every event has a number and is kept in a log."
- Garura never starts Argus; a person starts it once. The reason: "Claude only checks `/v1/health` and never starts it."
- Why each piece changed comes from the plays' records, in one plain line, and the plays are never shown. The reason: the plays' records feed only that line, and "the plays are never shown."
- Not decided: how the events reach Garura, by Garura's listener reading Argus's event stream, or by Argus calling Garura on each event.
- Not decided: which runs open a review, a loop's run only or also a play run by hand.

## Acceptance criteria
- Given a loop's run that changed two intents and a capability, when the review opens, then the pack passes the contract's check, holds one piece for each change with its words before and after and why it changed, and names no file other than an agent decision's source. This is not built.
- Given Argus is not running, when a review is to open, then Garura says so and starts nothing.
- Given the person accepts a piece, when its event arrives, then the run's branch holds a line for it in the event log and the answers so far show it. This is not built.
- Given the listener drops in the middle of a review, when it connects again, then it gets every event after the last one it saw, and none is missing. This is not built.

## Out of scope
- Showing the pack and taking the answers. Read what a run made, as business intents with their ICE and as the product (fn-read-outcome), and Answer each piece, in the page or one card at a time (fn-answer-pieces), do them.
- Reworking a piece sent back, and applying the answers. Send a piece back and get it reworked (fn-send-back) and Finish the review and have every answer applied in one commit (fn-apply-answers) do them.
- Keeping each piece's approval state. Product model owns it (#964).
- Anything inside Argus, and its contract. Run Argus apart from Garura, and point Garura at it (fn-run-tool-apart) covers them.

## Sources
- .garura/product/product-os/intents/bi-8.md: "Their answers become part of the work.", "Make people read raw files to know what was made."
- .garura/project/issues/617/specs/review-tool.md, the design, with the product owner's words: "Every time a change is made, it should have a direct connection back to Garura for listening.", "The pack is outcome-shaped, not file-shaped.", "The tool never sees a file path as something to open.", "Garura keeps a test that checks the packs it builds against that schema, so a break shows up on the Garura side first.", "Claude still never reads the web page: the answers are files on the branch", "Every event has a number and is kept in a log.", "Claude only checks `/v1/health` and never starts it.", "the plays are never shown."
- GitHub #648 (open): "Garura opens a review on what a drive changed and records every answer on the drive's branch", "it never starts the server itself", "An action in the tool lands as a file on the branch."
- core/components/plays/create-play/references/write_loop_review.py: "so the loop's end review can read every play's record in one place", "decided: false"
- standards/rules/loop-contract.md, in Phoenix memory: "The loop's end review reads the record."
- core/components/loops/complete-discovery/scripts/record_confirmation.py: "ends at the pull request"
- docs/adr/041-a-drive-runs-in-rounds-and-owns-its-questions.md: "Until Argus exists, a drive ends at the pull request"
