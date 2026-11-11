"""Build item 4 of BI-10's close (not applied until the product owner's yes): Argus takes a person's yes to move a page
from short-term memory to the project's Garura memory, and nothing more; moving a page to Phoenix memory is not
designed and is to happen outside Garura. Named line changes on the Memory and Argus pages, and fn-promote-page's
one-line. Run from the repo root; writes lines-request-4.json, link-request-4.json and item-4-diff.md.
"""
import json, os
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
S = "software-delivery-planning"
APPR = ".garura/project/issues/1021/context/bi-10-close/approval.md"
QA = "Argus can only allow from short term to the project memory."
QP = "Going to the Phoenix is not designed yet. That would need an organizational change."
SRC = f'- {APPR}, line 3, the product owner\'s words of 2026-11-11: "{QA} {QP}"'
SUB = {  # page: [(old substring, new substring)]
 f"{S}/memory/fn-promote-page/feature.md": [
  ("from an issue's short-term memory to Garura memory, or up to Phoenix memory, only when a person says yes to it in the Memory section of Argus, and what Run → Product learned is proposed there for that person to choose, so an answer one issue found can reach the next issue without anyone copying it by hand.",
   "from an issue's short-term memory to the project's Garura memory, only when a person says yes to it in the Memory section of Argus, and what Run → Product learned is proposed there for that person to choose, so an answer one issue found can reach the next issue without anyone copying it by hand. Nothing moves from a project to Phoenix memory."),
  ("It is the only way Garura memory and Phoenix memory change.", "It is the only way a page an issue found reaches Garura memory."),
  ("Phoenix memory changes only by a promotion, and takes only what is generic, with no names of a client, an organisation or a person.",
   "Phoenix memory is not changed from a project: moving a page to it is not designed, needs an organisational change, and is to happen outside Garura."),
  ("the person gives the yes in the Memory section of Argus, in Developer tooling; and Run → Product proposes what was learned.",
   f"the person gives the yes in the Memory section of Argus, in Developer tooling, for a move to Garura memory only: \"{QA}\"; and Run → Product proposes what was learned."),
  ("  - In an open-source library's harness, a generic rule on how to name a release has proved itself in two projects. The product owner says yes to moving it up to Phoenix memory, and it lands there as one commit.",
   "  - In a bank's payments service, a rule on how refunds are named has proved itself in one issue. The technical lead says yes to it in Argus, and it moves to the bank's Garura memory; it does not go to Phoenix memory, which no project changes."),
  ("- In: a page in an issue's short-term memory, such as an approved memory update or a person's answer, or a page in Garura memory.",
   "- In: a page in an issue's short-term memory, such as an approved memory update or a person's answer."),
  ("- Out, on a yes: the page in Garura memory, or in Phoenix memory as one commit, with a record of who said yes and their words.",
   "- Out, on a yes: the page in the project's Garura memory, with a record of who said yes and their words."),
  ("- Every change to Phoenix memory is a commit. The reason: \"Every change here is a commit.\"",
   f"- Nothing moves from a project to Phoenix memory. The reason, in the product owner's words: \"{QP}\""),
  ("- Phoenix memory takes only what is generic. The reason: \"No client, organisation or personal references.\"",
   f"- Argus takes the person's yes for a move to Garura memory only. The reason, in the product owner's words: \"{QA}\""),
  ("or a memory update aimed at Garura or Phoenix memory.", "or a memory update aimed at Garura memory."),
  ("- Not decided: whether a page moves up one tier at a time, as Phoenix memory's own notes say, or from short-term memory straight to Phoenix memory, as the tool's notes allow.",
   "- Not decided: how a move to Phoenix memory is designed, and which product outside Garura makes it."),
  ("- Not decided: how the Memory section of Argus takes the person's yes on a promotion, while its approved page says \"Moving memory up is not done here\".",
   "- Not decided: how the Memory section of Argus shows a page that waits for a person's yes to move to Garura memory, beside the updates that wait."),
  ("- Given a page proposed for Phoenix memory, when the product owner says yes, then it lands in Phoenix memory as one commit with who said yes and their words. This is not built.",
   "- Given a page in a project's Garura memory, when anyone in the project tries to move it to Phoenix memory, then nothing moves. This is not built."),
 ],
 f"{S}/memory/fn-promote-page/ice.md": [
  ("from an issue's short-term memory to Garura memory, or up to Phoenix memory as one commit, only when", "from an issue's short-term memory to the project's Garura memory, only when"),
  ("and the person chooses what is kept and in which tier;", "and the person chooses what is kept; nothing moves from a project to Phoenix memory;"),
  ("- Limit: Phoenix memory takes only what is generic, with no names of a client, an organisation or a person.",
   "- Limit: Nothing moves from a project to Phoenix memory; that move is not designed and is to happen outside Garura."),
  ("- Fails if: Garura memory or Phoenix memory gains a page with no person's yes on record.", "- Fails if: Garura memory gains a page with no person's yes on record."),
  ("- Fails if: A page that holds the name of a client, an organisation or a person reaches Phoenix memory.", "- Fails if: A page moves from a project to Phoenix memory."),
  (", where each tier lives, and how a change lands in Phoenix memory's repository.", ", and where each tier lives."),
  ("In an open-source library's harness, the product owner says yes to moving a generic rule up to Phoenix memory, and it lands as one commit; a second page, which names a client, is not moved.",
   "In a bank's payments service, the technical lead says yes in Argus to a rule on how refunds are named, and it moves to the bank's Garura memory; nothing is sent to Phoenix memory."),
  ("one commit in Phoenix memory for the generic rule, and the page that names a client not in Phoenix memory.",
   "the refund rule in the bank's Garura memory with the technical lead's yes, and no change from either project in Phoenix memory."),
 ],
 f"{S}/memory/capability.md": [
  ("- A promotion moves a page up a tier: from short-term memory to Garura memory, or to Phoenix memory.",
   "- A promotion moves a page up a tier, from short-term memory to the project's Garura memory. Moving a page to Phoenix memory is not designed, needs an organisational change, and is to happen outside Garura."),
  ("a page moves from short-term memory to Garura memory, or up to Phoenix memory, only on a person's yes in the Memory section of Argus,",
   "a page moves from short-term memory to the project's Garura memory only on a person's yes in the Memory section of Argus,"),
  ("or a memory update aimed at Garura or Phoenix memory.", "or a memory update aimed at Garura memory."),
 ],
 f"{S}/review-agent-work/fn-review-memory/feature.md": [
  ("- Nothing moves up to Garura memory or Phoenix memory from here. The reason: \"Moving memory up is not done here\".",
   f"- A page moves up from here only from an issue's short-term memory to the project's Garura memory, on a person's yes, and never to Phoenix memory. The reason, in the product owner's words of 2026-11-11: \"{QA} {QP}\""),
  ("- What a memory update is, who may decide it, and moving memory up. Memory,", "- What a memory update is, who may decide it, and what moving a page up does. Memory,"),
 ],
 f"{S}/review-agent-work/fn-review-memory/ice.md": [
  ("; nothing moves up to Garura memory or Phoenix memory from here.", "; a page moves up from here only to the project's Garura memory, on a person's yes, and never to Phoenix memory."),
  ("Out: what an update is and who may decide it, moving memory up,", "Out: what an update is and who may decide it, what moving a page up does,"),
 ],
 f"{S}/review-agent-work/capability.md": [
  ("while the design says \"Moving memory up is not done here\".", "while a page moves up from Argus only to Garura memory, and Phoenix memory is not reached from Garura."),
  ("- Out: what a memory update is, who may decide it, and moving memory up. Memory, in Standards, structure, settings and memory, owns them.",
   "- Out: what a memory update is, who may decide it, and what moving a page up does. Memory, in Standards, structure, settings and memory, owns them; the person's yes to move a page to Garura memory is given here."),
  ("- Never: move memory up from a review. The reason: \"Moving memory up is not done here\".",
   f"- Never: move a page to Phoenix memory from a review. The reason, in the product owner's words: \"{QP}\""),
 ],
}
ADD = {  # page: [(after this whole line, add this line)]
 f"{S}/memory/capability.md": [("- The three capabilities of Run → Product leave \"choosing and promoting what is learned into Garura memory or Phoenix memory\" here. Fifteen pages of Spec → Design and Design → Code hand promotion on without naming who owns it; four of them say an approved update moves up only by \"a promotion a person makes on purpose, outside this work\".",
   f"- Some of these pages also hand here promoting a page to Phoenix memory. That move is not Garura's: in the product owner's words of 2026-11-11, \"{QP}\"")],
}
OOS = "- Moving a page to Phoenix memory. It is not designed, needs an organisational change, and another product, outside Garura, is to own it."
pages, diff = [], []
for rel in list(dict.fromkeys(list(SUB) + list(ADD))):
    lines = open(f"{MODEL}/{rel}", encoding="utf-8").read().split("\n")
    new, ch = list(lines), []
    for o, n in SUB.get(rel, []):
        hit = [i for i, l in enumerate(new) if o in l]
        assert len(hit) == 1, (rel, o[:70], len(hit))
        i = hit[0]
        new[i] = new[i].replace(o, n)
        same = [c for c in ch if c.get("old") == lines[i]]
        if same:  # a second change on the same line: one entry, with every change of that line in its new words
            same[0]["new"] = new[i]
        else:
            ch.append({"old": lines[i], "new": new[i]})
        diff += [f"  {rel}", f"- {lines[i]}", f"+ {new[i]}", ""]
    for after, add in ADD.get(rel, []):
        assert new.count(after) == 1, (rel, after[:60])
        ch.append({"after": after, "add": add})
        diff += [f"  {rel}", f"+ {add}", ""]
    if rel.endswith("/feature.md") and "fn-promote-page" in rel:
        oos_i = new.index("## Out of scope")
        nxt = next(j for j in range(oos_i + 1, len(new)) if new[j].startswith("## "))
        last_oos = [l for l in new[oos_i + 1:nxt] if l.startswith("- ")][-1]
        ch.append({"after": last_oos, "add": OOS})
        diff += [f"  {rel}", f"+ {OOS}", ""]
    if not rel.endswith("/ice.md"):
        last = [l for l in new if l.strip()][-1]
        assert last.startswith("- ")
        ch.append({"after": last, "add": SRC})
        diff += [f"  {rel} (Sources)", f"+ {SRC}", ""]
    pages.append({"page": rel, "changes": ch})
json.dump({"by": "product-os-keeper, for #1021 (reorganise the business intents): BI-10 close, item 4",
           "source": f"{APPR}: \"{QA} {QP} It will happen in Sphinx or Griffin that we are building, but not in Karo.\"",
           "pages": pages}, open(f"{HERE}/lines-request-4.json", "w"), ensure_ascii=False, indent=1)
one = "A page moves from an issue's short-term memory to the project's Garura memory only on a person's yes in Argus, and what Run → Product learned is chosen by that person."
json.dump({"by": "product-os-keeper, for #1021: BI-10 close, item 4", "parts": [{"id": "fn-promote-page", "kind": "feature", "mode": "update", "one_line": one}]},
          open(f"{HERE}/link-request-4.json", "w"), ensure_ascii=False, indent=1)
open(f"{HERE}/item-4-diff.md", "w").write("\n".join(diff))
print("pages", len(pages), "changes", sum(len(p["changes"]) for p in pages))
