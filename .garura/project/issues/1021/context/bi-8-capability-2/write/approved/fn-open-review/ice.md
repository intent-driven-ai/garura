## Intent
- Goal: At the end of a loop's run, Garura builds a review pack of every piece the run added, changed or removed, by meaning, each with its words before and after, its approval state, its links and one plain line on why it changed, checks it against the contract, starts the review in Argus once Argus is up and opens its link for the person, and keeps every action the person takes as a line on the run's branch as it happens, so that each answer becomes part of the run's work.
- Limit: The pack names no file other than an agent decision's source, and never shows the plays.
- Limit: Garura never starts Argus, and no agent reads the review's web page; the answers reach the work only as files on the run's branch.
- Limit: No event is lost: after a drop, the listener picks up from the last event number it saw.
- Fails if: A piece the run changed is missing from the pack, or the pack fails the contract's check and is sent anyway.
- Fails if: An action the person took has no line on the run's branch.
- Fails if: Garura started Argus, or an agent read the web page to learn an answer.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the run's branch and where it lands, the model's pages and index on both, each piece's approval state once it is kept, the plays' review records and the checker's note, where a stopped run stopped and why, Argus's address and the contract's version.
- Never read: any memory file by its path, any ICE page, the review's web page, and production.
- Persona: the product owner, who opens the review at the end of a run and whose every answer must reach the work.
- Scope: In: working out what the run changed, building and checking the pack, starting the review and opening its link, and keeping every action on the run's branch. Out: showing the pieces and taking the answers, reworking a piece, applying the answers, keeping the approval state, and Argus's own contract and server.

## Expectation
- Scenario: A loop's run on a clinic's booking app changed one intent, its ICE and two features. At the end, Garura builds the pack with four pieces, each with its words before and after and why it changed, finds Argus up and opens the review. The product owner accepts the intent, and a line for it lands in the event log on the run's branch at once. His laptop sleeps; when the listener connects again, it gets the three actions he took in the meantime.
- Done means: Someone other than the one who built it compares what the run changed with the pack, and every action the person took in Argus with the lines on the run's branch, and finds every changed piece in the pack, no file named but an agent decision's source, and every action there once.
