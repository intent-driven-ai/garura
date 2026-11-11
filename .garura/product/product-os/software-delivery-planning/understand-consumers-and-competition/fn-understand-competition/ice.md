Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: The competitors the project follows are proposed from memory first and from the rivals people name in what is taken in, each with its source, and the product owner says yes to each; then, on their own each time new items come in, what people say each followed competitor does, offers or lacks is drawn from the items taken in, each finding with every item it rests on, quoted as taken in, its counts and how sure it is, so that the product owner sees what the competition is doing through what consumers say.
- Limit: No competitor is followed without the product owner's yes, and a rival named often and not followed is shown as a proposal, never followed in silence.
- Limit: Only the items taken in are read about a competitor, and a finding says what people say it does, never that it does it; nothing comes from what the AI agent knows by itself, and research is used only through a memory update a person approves.
- Limit: It writes only its own findings: no intent, page, memory, tracker or connected tool changes.
- Fails if: A competitor was followed without the product owner's yes, or a rival named often was neither proposed nor followed.
- Fails if: A finding about a competitor rests on anything but the items, or states as fact what only people said.
- Fails if: A finding names no item, quotes one other than as taken in, or a weak one is shown as strong.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the competitors the project's memory names, the rivals named in the items taken in, the competitors the product owner follows, the items that name them, and the earlier findings.
- Never read: a competitor's own pages, or any outside tool, forum or web page the first capability did not take in; production; anything that would bring back who a person is; and any ICE page.
- Persona: the product owner, who says yes to each competitor followed and wants what the competition is doing understood from what consumers say.
- Scope: In: proposing the competitors to follow, and drawing what people say each followed competitor does, offers or lacks, with its items. Out: taking in, reading a competitor's own pages, understanding what consumers want of this product, placing findings, and deciding what to build.

## Expectation
- Scenario: A team's planning tool takes in reviews and posts from a forum where teams compare planning tools. Two rivals are named often; one is already in the project's memory as a competitor, the other is proposed with the posts that name it. The product owner says yes to both. From the items, a finding says that teams say they moved to the second rival for its calendar view, with the eleven posts quoted; another, resting on one review, says the first rival is slow on phones and is marked weak. Nothing is read from either rival's own site.
- Done means: Someone other than the one who drew the findings checks that each followed competitor has the product owner's yes, that each finding lists the items it rests on and says only what people said, that weak findings are marked weak, and that nothing outside the items was read.
