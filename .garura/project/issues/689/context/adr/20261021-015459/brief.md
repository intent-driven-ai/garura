## Decision

The Kickoff drive stops chaining its plays, and the product model stops being a tree that must be built top-down.

1. **Every kind is written on its own.** A business intent, an ICE, a domain, a capability and a functionality are independent nodes. Any play writes any of them as soon as it finds it, with no parent required: a capability may have no domain yet, and a functionality may have no capability yet (it waits in a holding folder, `functionalities/<id>/`, like capabilities do today). The spine's "functionality names a capability — REQUIRED" rule and the nested folder layout as the only home change accordingly.
2. **A node is ready only once it is attributed.** It is not approved and not workable until it is linked: functionality → capability → domain, and its ICE → a confirmed business intent. Unlinked nodes are kept, shown as not ready, and never worked on.
3. **The drive closes the loop.** A play run on its own writes only what it finds and links what it can see (/vision links the capabilities it writes to its domain); the rest stays visible as not ready, and a person has to run the next play by hand (/vision finds the domain, but no functionality exists until someone runs /understand). The drive does that work itself. After each round its connect step — a member play inside the drive — reads every node and does two things. It **connects**: attributes each functionality to its capability and each capability to its domain, links them to the intents they serve, and merges two nodes that are the same thing written by two plays. And it **finds the work that is still missing and gives it to the play that does it**: a capability with no functionalities goes to /understand, a screen no node covers goes to the play that writes that kind, an intent no capability serves goes back to /intent or /vision. The next round runs those plays on exactly that work. The drive keeps going until every node is connected and nothing on the screens is left uncovered — or it reaches its round limit and briefs the person (ADR 042). Connecting the three meaningfully, so the work gets done, is the value a drive adds over running the plays by hand.
4. **The plays read the prototype independently.** The prototype is read once by the `prototype-reader` agent; its capture (views, words, journeys) is shared. `/intent` drafts the business intents from it, `/vision` the domains and capabilities (by research), `/understand` the functionalities — each from the screens, none from another play's output, so their readings are independent and their agreement is the check. No play waits for another. They may run side by side; writes to the one shared spine file are made in turn, and inside a drive the drive commits the round once.
5. **The prototype comes with a short write-up.** Kickoff takes, beside the prototype, a few lines from the person in five parts: what the product is; who uses it; the field it serves and the job it does there; what on the screens is only sample data; a walkthrough of the steps a person takes. Without it the drive asks for it first (its questions-first step). Every play reads it as a Source; the prototype-reader plans its walk from the walkthrough. The intents and the model still come from the screens; the write-up guides the reading.

## Why now

Kapil (21 October): "drive is one part of the puzzle, but intent, understand, and vision can be run independently as well … I run vision, which identifies the domain, but it won't have functionality and capabilities available. Somebody will have to go back and run it manually. The whole point of a drive is that these loops are closed … It's not just connecting the three. It's really connecting the three meaningfully so that the work gets done."

Kickoff run 7 (20 October, Argus mockup) chained the plays: /intent's drive-framed intents flowed into /vision, which invented a domain ("Drive review"), and into /understand, which detailed the wrong capabilities and made a screen panel a functionality. One error at the top spread to everything below. The fixes under #689 made each play read the screens itself; the chain is what is left. Kapil (21 October): "all of them build the prototype and start working independently so that there's no dependency … It's not a tree structure. They are independent functions, and the drive's job is to find and connect everything later on … everybody can write anything, but it is not approved, not ready, until there is an attribution that a functionality goes under a capability and a capability goes under a domain. That's the whole point of breaking it up." And on the write-up: "prototype isn't enough … a small write up … that explains the prototype … this will guide the drive and internally plays very well." The doctrine "anyone writes; align later" (Kapil, 8 October, during #612) already said no play owns a kind; the spine schema and the drive's fixed order still contradict it.

## Options considered

- **Keep the chain (/intent → /vision → /understand), each reading the screens** — lost: an error early still flows down, and /understand still cannot write a functionality before /vision writes its capability.
- **Run the three plays fully at once with no connect step** — lost: two plays write the same thing twice, nothing links the nodes, and the model never comes together.
- **Read side by side into drafts only, then save from an agreed draft** — lost for now: it needs a draft-only mode in every play; independent nodes plus a connect step give the same check with less change. Running the plays side by side stays allowed (part 4).
- **No write-up; infer the field from the screens** — lost: /vision had to guess the field (it found Human Oversight, missed SDLC / Developer Experience and Requirements management); the person states it in a few lines.

## Decided by

Kapil Viren Ahuja

## Decided in

#689 — the session of 20–21 October 2026, after Kickoff run 7 on the Argus mockup and the single-play tests of /intent and /vision.

## Shape

markdown — a framework decision (docs/adr/).
