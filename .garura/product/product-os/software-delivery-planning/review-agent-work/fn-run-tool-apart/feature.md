# Feature: Run Argus apart from Garura, and point Garura at it

## What it does
The person starts Argus once, as a small server on their laptop or, later, on a hosted place, and Garura reaches it only at the one address Garura's settings name, through one written and versioned contract: what a review pack holds, the requests Garura makes, and the events that come back; Argus knows nothing of Garura, so it can move, into Griffin later, by moving its folder and changing that one address.
- The contract, the one written agreement between the two, has three parts:
  - the review pack: the pieces of a review, each with its words before and after, what changed, its approval state and its links, by meaning and never as files;
  - the requests: is Argus up, start a review, read it, the events after a given number, a new version of a piece, a reply on a comment, and close the review;
  - the events: one numbered event for each action of the person, kept so that any of them can be read again.
- Garura's words are data for Argus: an intent, a capability or a limit arrives in the pack as a kind, with its label and its icon, and Argus's code never names them, so "A product other than Garura could send its own kinds."
- Argus has its own folder, its own guide, its own tests and its own version. It imports no Garura code and reads no Garura path, and a check fails if any of its files names Garura's folders or reaches outside its own.
- Its settings come from outside it: the port it listens on, its data folder, its address and its access token. On a laptop it listens only on that machine, with a token; hosted, the host's own sign-in goes in front.
- It keeps its reviews behind one small store: files on disk today, a database later, with nothing else changed.
- Everything it needs is inside its folder, so it works with no internet connection.
- It is a Phoenix tool, built apart from Garura and tracked in the Phoenix project under Garura tools.
- Examples, in different kinds of project:
  - A person building a recipe app alone runs Argus on their laptop, and their project's settings point at it there.
  - A company's platform team later uses Argus hosted, behind its own sign-in, and its projects change only the address.
  - A content team's product, which is not Garura, sends its own kinds of piece, such as an article, and Argus shows them without a change to its code.
- How it meets the capability: this is the "one tool", kept apart so it can serve Garura and move without it.

Status: not built. No folder holds Argus, in Garura or in any other repository, and no setting in Garura names its address. The stories still say it lives in a folder inside Garura, while it was decided on 20 October 2026 that "the review tool needs to be built separately".

## Inputs / Outputs
- In: the review packs and the requests Garura sends, at Argus's address.
- In: Argus's settings: its port, data folder, address and access token.
- In: the person's actions in the page.
- Out: the events, numbered and kept, read by Garura from any number on.
- Out: a written, versioned contract that Garura checks its packs against.

## Rules & behavior
- Garura and Argus meet only through the contract. The reason: "The line between the tool and Garura is the contract".
- No Garura code, and no Garura path, in Argus. The reason, in the product owner's words: "The way I want you to build the tool is that it is easily extractable and movable out of Garura."; and Argus "imports no Garura code, so it can move into Griffin later".
- Garura's words are data, not code. The reason: "Garura words are data, not code."
- One address in Garura's settings is all that changes when Argus moves. The reason: "Moving the tool to Griffin means moving one folder and changing one address in Garura's config."
- Every action is a numbered event that can be read again. The reason: "Every event has a number and is kept in a log."
- A person starts Argus; Garura never does. The reason: "Claude only checks `/v1/health` and never starts it."
- On a laptop, only that machine reaches it, and only with its token. The reason: "On a laptop it listens only on 127.0.0.1 with a token."
- Not decided: whether Garura's install lays Argus, a setting only points at it, or a team uses it alongside, while Developer tooling's page says the tools "ship with Garura".
- Not decided: where Argus's code is kept, now that no repository holds it.

## Acceptance criteria
- Given Argus's folder, when the boundary check runs, then no file in it names Garura's folders or reaches outside the folder. This is not built.
- Given the two example packs of the contract, a run that ended and a run that stopped, when they are checked, then both pass the contract's schema. This is not built.
- Given a listener that read events up to number 40, when it asks for the events after 40, then it gets every later event and none before it. This is not built.
- Given Argus moves to another place, when Garura's settings name its new address, then a review opens there with nothing else in Garura changed. This is not built.

## Out of scope
- Building the pack, and keeping the answers on the run's branch. Open a review on what a run changed, and keep every answer on the run's branch (fn-open-review) does it.
- The pages a person reads and answers in. Read what a run made, as business intents with their ICE and as the product (fn-read-outcome) and Answer each piece, in the page or one card at a time (fn-answer-pieces) cover them.
- Moving Argus into Griffin, which comes later.

## Sources
- The review tool's design, with the product owner's words: "The way I want you to build the tool is that it is easily extractable and movable out of Garura.", "The line between the tool and Garura is the contract", "Garura words are data, not code.", "A product other than Garura could send its own kinds.", "Moving the tool to Griffin means moving one folder and changing one address in Garura's config.", "Every event has a number and is kept in a log.", "Claude only checks `/v1/health` and never starts it.", "On a laptop it listens only on 127.0.0.1 with a token.", "It works offline on a laptop", "the review tool needs to be built separately"
- .garura/user-provided/managing-work.md: "Tools built beside Garura", "are Phoenix tools"
- .garura/product/product-os/intents/bi-8.md: "ship with Garura"
- The product owner on 2026-11-10: "in one tool"
