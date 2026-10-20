# Audit: the drive's 82 open questions against the Argus prototype

Checked against `argus.html` (all 1,362 lines read, including the script's sample data and comments), the captured views in `prototype-capture/*.txt` and the journey captures in `prototype-capture/journeys/`. The journey and view files are captures of the same page, so the HTML is the root source; line numbers below are `argus.html` lines unless a view is named.

How each question is marked:
- ANSWERED: the prototype shows the answer, quoted.
- PARTLY: the prototype shows part of it, or strongly implies it. What is missing is named.
- NOT SHOWN (SHOULD-SHOW): a working prototype of this tool should show it, so leaving it out is a gap.
- NOT SHOWN (NOT-A-PROTOTYPE-THING): no screen would show it (speed targets, rules like GDPR, business success measures, where a capability sits in the knowledge base). It belongs to the person or to memory.

## Summary

| Result | Count |
|---|---|
| ANSWERED | 14 |
| PARTLY | 25 |
| NOT SHOWN (SHOULD-SHOW) | 5 |
| NOT SHOWN (NOT-A-PROTOTYPE-THING) | 38 |
| Total | 82 |

So 39 of 82 (14 + 25) are fully or partly in the prototype. 38 are things no prototype would show. Only 5 are real gaps in the prototype.

## Repeated questions (same underlying question)

1. How will you know it works (the business proof), sometimes with the why. Asked 15 times: intent-q2 to q7, understand-q2, q20, q24, q29, q44, q55, q57, q65, q74. NOT-A-PROTOTYPE-THING. The six intents' proofs are each asked twice, once by the intent play and again by the understand play. Note: the drive's own example answers mirror things the prototype does show (Finish stays locked until every piece has an answer, line 789; "Works on your phone too", line 702; "Nothing is lost", line 1005). The prototype shows the behaviour a proof could test, but the success measure itself is the person's to name.
2. Speed targets. Asked 11 times: understand-q3, q12, q16, q23, q25, q35, q36, q56, q58, q66, q70. NOT-A-PROTOTYPE-THING. (The "under 1 second" figures in the prototype belong to the sample shop, not to Argus.)
3. Who may give an answer, and how that person is known. Asked 8 times: understand-q1, q7, q19, q30, q37, q42, q50, q67. PARTLY each time. The prototype has one reviewer, "you", and records approvers by name ("Approved · 2 Oct 2026 by Kapil", line 650; "Approved by sample reviewer in the review tool", view-27). It has no sign-in, no role (lead or product owner) and no permission rule.
4. Who may see something. Asked 2 times: understand-q21, q71. NOT-A-PROTOTYPE-THING (an access rule). The related privacy questions q63 (PARTLY) and q68 (NOT-A-PROTOTYPE-THING) sit next to these.
5. Rules and regimes (SOC 2, GDPR) for Argus itself. Asked 5 times: understand-q4, q28, q34, q40, q48. NOT-A-PROTOTYPE-THING. (The PCI-DSS and GDPR in the prototype belong to the sample shop.)
6. Where a capability sits in the knowledge base. Asked 3 times: vision-q1, understand-q41, q49. NOT-A-PROTOTYPE-THING.
7. Does an answer take effect at once, or only when the review is finished? Asked 2 times: understand-q43, q69. ANSWERED. For drive pieces it is at the finish ("It becomes real when you finish", line 759). The ADRs, Memory and Agent decisions tabs have no Finish button at all (lines 1169–1173), and their answers act on the click. The drive wrote a "domain rule" that contradicts this.
8. Is a decision that moves a limit also listed with the recorded decisions (ADRs)? Asked 2 times: understand-q39, q46. ANSWERED: no. The ADRs tab holds "The decisions a person records with /adr" (line 1227). The limit decision lives in Product › Decisions, "Recorded by /understand" (line 565).
9. Questions that describe what the prototype already does and ask whether it was meant. 5 questions: understand-q17, q22, q45, q64, q72. The first four are ANSWERED by what is on screen; q72 is PARTLY because the rule exists only in the code, with no reason given.

Also worth knowing:
- understand-q26 says the prototype "does not show this case". It does: "Saved cards" is a whole piece the drive took out (lines 479–488).
- understand-q64 points at a real inconsistency in the prototype: a decision with no source is labelled "not allowed", yet "Looks right" is still offered.
- understand-q33 points at a smaller one: the Drop button reads "with a comment", but its prompt says "you can leave this empty".

## Every question

### open-intent.json

- **intent-q1**: Why does a person reviewing agent work matter to the business, and what goes wrong today without it?
  PARTLY. The prototype shows what each part protects: "Agents work only on approved pieces." (line 685, screen-01.txt); memory updates: "This work is stopped until you answer." (line 1280); agent decisions: "Each step's source is read again now: it still says the same, it changed, or it is gone." (line 1237). Missing: the business pain today (cost, delay, risk). That part is the person's to give.
- **intent-q2**: How will you know signing off a drive in one sitting works?
  NOT SHOWN (NOT-A-PROTOTYPE-THING). It is a business measure. The prototype does show the behaviour a measure could test: Finish stays locked while any piece has no answer ("Finish review (n left)", line 789); "Works on your phone too" (line 702).
- **intent-q3**: How will you know askers can see what was made of their request?
  NOT SHOWN (NOT-A-PROTOTYPE-THING). A business measure. The prototype shows each business intent linked to its agent intents ("Agent intent" links, line 597) and "Asked by Priya, Head of Growth" (line 392).
- **intent-q4**: How will you know the lead knows the whole picture before agents build?
  NOT SHOWN (NOT-A-PROTOTYPE-THING). A business measure. Related screen: "Agents work only on approved pieces." with Approved / Changed / In progress counts (lines 684–688).
- **intent-q5**: How will you know the owner settles decisions that bind later work?
  NOT SHOWN (NOT-A-PROTOTYPE-THING). A business measure.
- **intent-q6**: How will you know blocked work moves once the owner settles a fact?
  NOT SHOWN (NOT-A-PROTOTYPE-THING). A business measure. Related behaviour: "the work that waits on it goes on" (line 1280).
- **intent-q7**: How will you know a reviewer can trust decisions agents made alone?
  NOT SHOWN (NOT-A-PROTOTYPE-THING). A business measure. Related screen: Unchanged / Changed / Gone / No source counts (lines 1238–1244).

### open-vision.json

- **vision-q1**: Should Argus sit under Collaboration, or in its own area for overseeing agent work?
  NOT SHOWN (NOT-A-PROTOTYPE-THING). This is about how the knowledge base is organised. Nothing on screen bears on it.

### open-understand.json

- **understand-q1**: Who may give a verdict on a drive's pieces, and how is that person known?
  PARTLY. One reviewer, "you": "Waiting for you" (line 698); approvals are recorded by name: "Approved · 2 Oct 2026 by Kapil" (line 650). Missing: sign-in or identity, and who is allowed.
- **understand-q2**: Proof that signing off a drive in one sitting works.
  NOT SHOWN (NOT-A-PROTOTYPE-THING). A repeat of intent-q2.
- **understand-q3**: Speed target for answering a card and finishing.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q4**: Does SOC 2 or GDPR apply to the review record?
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q5**: Can a person reopen or change a review after finishing?
  PARTLY. The finish dialog says what happens next: "Garura now applies your answers on the drive's branch and reworks what you sent back. Anything it reworks comes back here for you." (line 859; journeys/catch-up-30.txt). There is no reopen control, which implies there is no reopen. Missing: an explicit statement on changing an answer that was already applied.
- **understand-q6**: What if a second person opens the same review while the first is answering?
  NOT SHOWN (SHOULD-SHOW). No "someone else is reviewing" state exists. If only one person may review at a time, the screen should show how a second person is kept out.
- **understand-q7**: Who may comment and settle, and how are they identified?
  PARTLY. Comments are by "you"; only your own comments get "Mark resolved" (line 766). Missing: identity and permissions.
- **understand-q8**: Does Garura's reply come in the same sitting or after rework?
  PARTLY. The sample thread: a comment marked "answered", then Garura: "Yes. The email field sits on the payment step, so a guest still has three steps. Changed in revision 2." (lines 602–603; view-18). Comment states run open → answered → resolved (line 235). "Revision 2" implies the reply comes with the rework. Missing: an explicit statement of timing.
- **understand-q9**: Can a person reply in a thread, edit or delete their comment, or reopen a settled thread?
  NOT SHOWN (SHOULD-SHOW). Only "Add a comment" and "Mark resolved" exist (lines 766–768). If these actions are wanted, they are screen actions.
- **understand-q10**: When Garura reworks a page, does a comment's anchor follow its words?
  PARTLY. A comment is stored with its section and its quoted words, and the mark is found again by searching for those words on each render (lines 735–745, 806). The thread also keeps the quote itself. Missing: what happens when the words change between revisions.
- **understand-q11**: Must commenting on an area work without a mouse?
  PARTLY. There is a keyboard path for commenting on a piece: "c comment · p point" (line 354), and c opens the composer (line 927). Drawing an area is mouse-drag only: "Drag a box over the part you want to talk about" (line 214; mouse handlers at lines 891–907). Missing: whether it must. That is the person's accessibility level.
- **understand-q12**: Speed target for a saved comment to show.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q13**: Are comments on unchanged pieces handed back too?
  PARTLY. Unchanged pieces still show "Add a comment" (lines 757, 768). Every comment is sent as an event: event('comment') (line 806); "Comment sent to Garura" (line 1031). Missing: what Garura does with a comment on an unchanged piece.
- **understand-q14**: What counts as "received"?
  ANSWERED. Garura's acknowledgement of each action: "Every action goes to Garura as it happens" (line 365); "Garura got event #" + number (line 639; view-36); "Each action you take shows here as it reaches Garura." (line 772). It is simulated, as everything in a mockup is.
- **understand-q15**: How long can an action stay unconfirmed before a warning, and is it re-sent?
  NOT SHOWN (SHOULD-SHOW). There is no "did not reach Garura" state. The failure state belongs on screen; the timeout number belongs to the person.
- **understand-q16**: Speed target for a receipt.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q17**: Must "left for later" reach Garura as an action?
  ANSWERED. No. Later is a reading state: "Later · keep unread" (line 997); "You kept these unread. Go through them now, or come back any time. Nothing is lost." (line 1005; journeys/catch-up-26.txt). In the code, Later sends no event (line 1035), while accept, send back and drop do (line 1039).
- **understand-q18**: Where is the full receipt trail beyond six lines?
  NOT SHOWN (SHOULD-SHOW). The feed shows `S.events.slice(0, 6)` only (line 772). There is no link to a full trail.
- **understand-q19**: Can more than one person answer a review, and whose actions does each trail show?
  PARTLY. The prototype shows one reviewer ("Waiting for you", line 698), and the trail "Sent to Garura, live" carries no names (line 772). Missing: whether more people may answer.
- **understand-q20**: Proof for the "askers see what was made" intent.
  NOT SHOWN (NOT-A-PROTOTYPE-THING). A repeat of intent-q3.
- **understand-q21**: Who may read a request and its agent work?
  NOT SHOWN (NOT-A-PROTOTYPE-THING). An access rule. The prototype shows only who asked ("Asked by Priya, Head of Growth", line 392).
- **understand-q22**: Should an agent intent that lacks a line (for example "Checked by") say so?
  ANSWERED. It shows only the lines it holds: `ICE_ORDER.filter(k => groups[k])` (line 593). The Saved cards agent intent shows only "Goal" (line 486). The drive saw this and asked whether it was meant.
- **understand-q23**: Performance, reliability and accessibility targets for this view.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q24**: Proof for "askers see what was made" (open on its page).
  NOT SHOWN (NOT-A-PROTOTYPE-THING). A repeat.
- **understand-q25**: Speed target for showing changes on a large piece or drive.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q26**: When a whole piece is taken out, does it stay listed with its removed mark?
  ANSWERED. Yes. "Saved cards" is removed by the drive and stays listed: status "Removed in this drive" (line 482; journeys/check-the-product-05.txt); approval chip "Changed — removal not approved" (line 651); a red dot in the rail; the overview shows "Removed … taken out" (line 696); it stays listed in the Final view too (line 608). The drive's claim that "the prototype does not show this case" is wrong.
- **understand-q27**: Accessibility need for change marks.
  NOT SHOWN (NOT-A-PROTOTYPE-THING). The level is the person's call. Note: the prototype already marks changes with symbols and strike-through, not colour alone ("+" and "–" markers, line-through; lines 193–196).
- **understand-q28**: Does SOC 2 or GDPR apply?
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q29**: How to measure that the lead knows the whole picture.
  NOT SHOWN (NOT-A-PROTOTYPE-THING). A repeat of intent-q4.
- **understand-q30**: Who may answer which part of the model?
  PARTLY. Same evidence as q1: one "you", approvers named (line 650). Missing: roles and permissions.
- **understand-q31**: Do the lead's answers go in the same review and finish as the owner's?
  PARTLY. Product parts sit in the same review with one Finish: "Kickoff changed N intents, N agent intents and N parts of the product." (line 690); Finish counts every changed piece (lines 609, 789). Missing: the lead and the owner as separate people. The prototype has no roles.
- **understand-q32**: May an already-approved part be sent back or taken out?
  ANSWERED. No. An unchanged piece shows "Not changed in this drive." with no Accept / Send back / Drop (line 757), and answering is blocked in code (`if (!changed(p)) return`, line 815). Only comments are possible.
- **understand-q33**: Must a take-out answer carry a reason?
  ANSWERED. No: "Why drop it? (you can leave this empty)" (line 973; journeys/catch-up-18.txt). Send back does need one: "Garura needs a comment to know what to change." (line 1033). Small inconsistency: the Drop button reads "with a comment · d" (line 995).
- **understand-q34**: Compliance for the kept record of answers.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q35**: Speed targets for the tree and part pages.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q36**: Speed targets for the limits pages.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q37**: Who is accountable for a moved limit: the owner, the lead, or either?
  PARTLY. The same single reviewer answers the limit and its decision in the one review (the limit and the decision both sit in the "Needs you" list, lines 678–680). Missing: which role.
- **understand-q38**: If the answers on a moved limit and its decision disagree, block the finish or warn?
  PARTLY. The prototype shows that the two are coupled: "If you drop it, the limit goes back to high and Refunds is reworked to fit." (line 564); Drop on a decision says "The limit goes back down." (line 761). Missing: any check when the two answers conflict. That would be a screen state (SHOULD-SHOW).
- **understand-q39**: Does a limit-moving decision also appear with the recorded decisions?
  ANSWERED. No. The ADRs tab holds "The decisions a person records with /adr." (line 1227) and lists two ADRs (lines 1130–1133). The limit decision is in Product › Decisions, "Recorded by /understand" (line 565).
- **understand-q40**: Does privacy law apply to reviewer names in the record?
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q41**: Should a knowledge-base node be proposed for product-wide limits?
  NOT SHOWN (NOT-A-PROTOTYPE-THING). Knowledge-base housekeeping.
- **understand-q42**: Who is accountable for a recorded decision, and how is that known?
  PARTLY. The ADR asks one person: "Accept this decision?" (line 1285). Missing: a named owner per ADR, and identity.
- **understand-q43**: Does an accept take effect at once or only with the finished review?
  ANSWERED. At once for ADRs: "Accept — The ADR is accepted, and older ones get a pointer." (line 1286); the status flips to accepted on click (line 1341); the ADRs tab has no Finish button (Finish is hidden in these tabs, lines 1169–1173). The drive's "domain rule" contradicts the prototype.
- **understand-q44**: Proof and why for the "owner settles decisions" intent.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q45**: Can a person undo an accept or send-back on a decision before finishing?
  ANSWERED. No, for ADRs: once accepted, the side shows only "Accepted." (line 1285). Undo exists only for drive pieces (z / Undo in Catch up, lines 1044 and 1092; a second click clears an answer, line 817). The drive saw this and asked whether it was meant.
- **understand-q46**: Is a limit-moving decision listed here or only under limits?
  ANSWERED. A repeat of q39.
- **understand-q47**: How are decisions ordered inside the waiting and accepted groups?
  PARTLY. Groups come "Waiting first" (line 1228); the rail shows "Waiting for you" then "Accepted" (lines 1186–1187). Missing: the order within a group. The sample has one item in each.
- **understand-q48**: Does an audit regime such as SOC 2 apply?
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q49**: Should a knowledge-base node be proposed for sign-off?
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q50**: Who may approve a drafted answer, and can they hand it on?
  PARTLY. One person answers with their words: "Your words — needed to approve or reject" (line 1293); the record names them: "Approved by sample reviewer in the review tool" (view-27; line 1272). Missing: owner per area, and hand-off.
- **understand-q51**: May the owner edit the draft and approve their own version?
  ANSWERED. No: the draft is approved or rejected as written, and the person's words are kept as a reply. "If you approve it: Garura writes it to issue #613's short-term memory" (line 1280). The applied sample keeps the draft text with the reply "Yes, 7 days." (line 1139). The Memory tab offers no edit (unlike drive pieces, which have Edit).
- **understand-q52**: After a rejection, what happens to the waiting work?
  PARTLY. "Reject — Nothing is written. Work that waits on it stays stopped." (line 1295; view-23). Missing: what restarts it (a new draft, a person giving the fact, or dropping the work).
- **understand-q53**: When a blocking answer is approved, how does the stopped work start again?
  ANSWERED. "…and the work that waits on it goes on." (line 1280; view-23). No step for anyone else is shown. The trigger mechanism behind it is not shown.
- **understand-q54**: Should the owner be alerted when a new draft waits?
  PARTLY. Inside the tool: "3 memory updates wait for your answer" (line 1215), "blocking first" (line 1216), the "Blocks the work" chip (line 1167), "Catch up (3)" (line 1303). Missing: any alert outside the tool, and how soon.
- **understand-q55**: Why does the owner settling facts matter, and how will they know it works?
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q56**: Speed for the list, answer page and verdict.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q57**: Proof for "ask what is already known".
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q58**: Speed for Ask and the overview.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q59**: Which pieces of work may the owner switch between?
  PARTLY. An issue picker with #613 and #614 "picks the short-term memory shown" (line 1212; view-04). #614 is not the drive's issue, so the picker is wider than the drive. Missing: which issues exactly, and who may see them.
- **understand-q60**: When the only match is a draft still waiting, should the answer say so?
  PARTLY. Drafts are not used until approved: "nothing in it is used before you approve it" (line 1215). Missing: what Ask says in that case. Ask's "no answer" state is not shown at all.
- **understand-q61**: When nothing answers, may the owner start a new memory update from Ask?
  NOT SHOWN (SHOULD-SHOW). Every update is raised by an agent ("Raised by product-os-keeper (/vision)", lines 1126–1128, 1278). There is no "nothing found" state and no start control.
- **understand-q62**: For a pulled piece that has fallen behind, see which one and bring it up to date?
  PARTLY. Only the count: "Pulled from Phoenix · 4 pieces · 1 behind" (line 1121; view-04). Missing: which piece, and an update action. The drive said the same.
- **understand-q63**: May the owner see Phoenix memory content from other projects?
  PARTLY. The owner sees Phoenix content in full, not just counts: the Ask answer cites "Phoenix memory · knowledge · ecommerce domain · lines 41–42" (line 1124), and the decision trail prints the Phoenix lines with their surroundings (lines 1259–1260; journeys/check-agent-decisions-03.txt). Missing: whether content from other projects (beyond shared knowledge) is shown. The privacy rule is the person's.
- **understand-q64**: May a decision with no source stand, or must it always be sent back?
  ANSWERED. It must be sent back: "No source … not allowed" (line 1243; view-05); "Every decision must name its memory (ADR 035 §6). Send it back, and the agent decides again from memory." (line 1274; view-33). Prototype inconsistency: "Looks right" is still offered on that page (lines 1288–1290). That is a fix for the prototype, not an open question.
- **understand-q65**: Proof and why for "trust agent decisions".
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q66**: Speed of re-reading, and how many decisions one issue can hold.
  NOT SHOWN (NOT-A-PROTOTYPE-THING). The sample has 12; volume limits are not a screen matter.
- **understand-q67**: Who counts as the reviewer allowed to stand or send back a decision?
  PARTLY. One reviewer: "Does this decision still hold?" with "Looks right" or "Send back" (lines 1288–1290). Missing: identity and permissions.
- **understand-q68**: Do memory lines in a trail need masking for private content?
  NOT SHOWN (NOT-A-PROTOTYPE-THING). A privacy level. The prototype shows the lines unmasked, but the sample holds no private content.
- **understand-q69**: Does a send-back on an agent decision reach Garura at once or only with the finished review?
  ANSWERED. At once: the click sends `decision_redo` immediately (line 1342); "Send back — The agent decides again, from memory as it is now." (line 1290); this tab has no Finish button (lines 1169–1173). The drive's "effect at the finish" contradicts the prototype.
- **understand-q70**: Speed of the overview counts.
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
- **understand-q71**: Who may see a review's standing?
  NOT SHOWN (NOT-A-PROTOTYPE-THING). An access rule.
- **understand-q72**: The model-wide count leaves out agent intents not tied to a business intent. Is that meant?
  PARTLY. The behaviour is in the code: `PIECES.filter(p => !(p.ice && !p.from.length))` (line 684). Such agent intents also never appear in the Intents rail. The page has wording for the case ("no intent yet", lines 592, 711, 982). Missing: any reason given.
- **understand-q73**: If the drive's own final check failed, should the overview still offer the review?
  PARTLY. The check result shows in the header: "Drive finished 17 Oct, 14:20 · second check found no gaps" (line 361; screen-01). Missing: the failed case, which is a screen state the prototype should show (SHOULD-SHOW).
- **understand-q74**: Why and proof for "see the review standing".
  NOT SHOWN (NOT-A-PROTOTYPE-THING).
