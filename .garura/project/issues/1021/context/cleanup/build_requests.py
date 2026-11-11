"""Build the requests for #1021's last model work (not applied until the product owner's yes):
the two old capabilities Build a plan and Write the hidden eval taken in by BI-1's Turn intents into agent work and
BI-3's Write the evals, the one slice removed, the five old intent pages removed, every line naming a particular plan
dropped, and BI-1's and BI-3's Touches lists. Run from the repo root; writes the requests and changes-diff.md here.
"""
import json, os
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
S = "software-delivery-planning"
BY = "product-os-keeper, for #1021 (reorganise the business intents): the last model work"
SRC = f"{HERE}/approval.md"
DEEP_OLD = "written by /shape-slice for bi-788 at the directional depth."
DEEP_NEW = "written by /shape-slice at the directional depth."
OLDP = {  # old page path -> new page path, for the five features that move
 f"{S}/cap-718/fn-727/feature.md": f"{S}/turn-intents-into-work/fn-727/feature.md",
 f"{S}/cap-718/fn-728/feature.md": f"{S}/turn-intents-into-work/fn-728/feature.md",
 f"{S}/cap-718/fn-818/feature.md": f"{S}/turn-intents-into-work/fn-818/feature.md",
 f"{S}/shape-eval/fn-798/feature.md": f"{S}/write-work-evals/fn-798/feature.md",
 f"{S}/shape-eval/fn-898/feature.md": f"{S}/write-work-evals/fn-898/feature.md",
}
SUB = {
 f"{S}/domain.md": [(DEEP_OLD, DEEP_NEW)],
 f"{S}/cap-718/capability.md": [("Added by /shape-slice for bi-788 (", "Added by /shape-slice ("), (DEEP_OLD, DEEP_NEW)],
 f"{S}/shape-eval/capability.md": [(DEEP_OLD, DEEP_NEW)],
 f"{S}/cap-718/fn-818/feature.md": [(DEEP_OLD, DEEP_NEW),
   ("the product owner runs /shape-plan 788 in Claude Code", "the product owner runs /shape-plan on a business intent in Claude Code")],
 f"{S}/shape-eval/fn-798/feature.md": [(DEEP_OLD, DEEP_NEW),
   ("the product owner runs /shape-eval 788 in Claude Code after /shape-plan and finds the eval in plans/788/evals/<slug>/.",
    "the product owner runs /shape-eval on a business intent in Claude Code after /shape-plan and finds the eval in its plan's evals folder.")],
 f"{S}/shape-eval/fn-898/feature.md": [(DEEP_OLD, DEEP_NEW)],
 "features/fn-931/feature.md": [("The approved /update-plan session on plan 717, entry 3:", "An approved /update-plan session, entry 3:")],
 f"{S}/manage-model/capability.md": [("filed under the closed intent bi-722 (A product model can be managed, and grows as plans are built)",
   "filed under an older business intent, now closed (A product model can be managed, and grows as plans are built)")],
 f"{S}/define-product/capability.md": [("filed under the closed intent bi-722 (A product model can be managed, and grows as plans are built)",
   "filed under an older business intent, now closed (A product model can be managed, and grows as plans are built)")],
 f"{S}/standards/capability.md": [("filed under the closed intent bi-734 (Garura publishes a standard for building agentic harnesses)",
   "filed under an older business intent, now closed (Garura publishes a standard for building agentic harnesses)")],
 f"{S}/manage-model/fn-close-model-gaps/feature.md": [("four intents nothing serves (bi-11, bi-5, bi-734 and bi-756)",
   "four intents nothing served then (bi-11, bi-5, and two older intents since removed)")],
 f"{S}/turn-intents-into-work/capability.md": [
   (f"{MODEL}/{S}/cap-718/fn-818/feature.md", f"{MODEL}/{S}/turn-intents-into-work/fn-818/feature.md"),
   ("Build a plan (cap-718) with fn-727, fn-728 and fn-818", "Build a plan with fn-727, fn-728 and fn-818")],
 f"{S}/turn-intents-into-work/fn-cut-intent-into-work/feature.md": [
   (f"- {MODEL}/{S}/cap-718/capability.md:", f"- {HERE}/old-pages/build-a-plan.md, which keeps the page of Build a plan as it was before the merge:"),
   (f"{MODEL}/{S}/cap-718/fn-818/feature.md", f"{MODEL}/{S}/turn-intents-into-work/fn-818/feature.md")],
 f"{S}/turn-intents-into-work/fn-write-story-from-ice/feature.md": [
   (f"{MODEL}/{S}/cap-718/fn-818/feature.md", f"{MODEL}/{S}/turn-intents-into-work/fn-818/feature.md")],
 f"{S}/gather-work-under-item/fn-collect-story-context/feature.md": [
   (f"{MODEL}/{S}/shape-eval/fn-898/feature.md", f"{MODEL}/{S}/write-work-evals/fn-898/feature.md")],
 f"{S}/write-work-evals/capability.md": [
   (f"- {MODEL}/{S}/shape-eval/capability.md:", f"- {HERE}/old-pages/write-the-hidden-eval.md, which keeps the page of Write the hidden eval as it was before the merge:"),
   ("Write the hidden eval (cap-shape-eval) with its features", "Write the hidden eval with its features")],
 f"{S}/write-work-evals/fn-keep-evals-from-builder/feature.md": [
   (f"{MODEL}/{S}/shape-eval/fn-898/feature.md", f"{MODEL}/{S}/write-work-evals/fn-898/feature.md")],
}
pages, diff = [], []
for rel, subs in SUB.items():
    lines = open(f"{MODEL}/{rel}", encoding="utf-8").read().split("\n")
    new, ch = list(lines), []
    for o, n in subs:
        hit = [i for i, l in enumerate(new) if o in l]
        assert hit, (rel, o[:60])
        for i in hit:
            new[i] = new[i].replace(o, n)
    for i, (a, b) in enumerate(zip(lines, new)):
        if a != b:
            ch.append({"old": a, "new": b})
            diff += [f"  {rel}:{i+1}", f"- {a}", f"+ {b}", ""]
    assert len(set(c["old"] for c in ch)) == len(ch)
    pages.append({"page": rel, "changes": ch})
w = lambda name, obj: json.dump(obj, open(f"{HERE}/{name}", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
w("lines-request.json", {"by": BY, "source": SRC, "pages": pages})
# step 2: repoint and remove the slice
w("remove-request-1.json", {"by": BY, "approved_by": "the product owner", "source": SRC,
  "repoint": [{"id": "cap-718", "kind": "capability", "intents": {"bi-717": "bi-1", "bi-788": "bi-1"}},
              {"id": "fn-727", "kind": "feature", "intents": {"bi-717": "bi-1"}},
              {"id": "fn-728", "kind": "feature", "intents": {"bi-717": "bi-1"}},
              {"id": "fn-818", "kind": "feature", "intents": {"bi-788": "bi-1"}},
              {"id": "cap-shape-eval", "kind": "capability", "intents": {"bi-788": "bi-3"}},
              {"id": "fn-798", "kind": "feature", "intents": {"bi-788": "bi-3"}},
              {"id": "fn-898", "kind": "feature", "intents": {"bi-788": "bi-3"}},
              {"id": "dom-software-delivery-planning", "kind": "domain", "intents": {"bi-717": None, "bi-788": None}}],
  "remove": [{"kind": "slice", "id": "sl-intent-to-design"}]})
# step 3: the five old intent pages
w("remove-request-2.json", {"by": BY, "approved_by": "the product owner", "source": SRC,
  "remove": [{"kind": "intent", "id": b} for b in ("bi-717", "bi-722", "bi-734", "bi-756", "bi-788")]})
# step 4: file each moved feature under its new capability, with its page moved
moves = {"fn-727": "cap-turn-intents-into-work", "fn-728": "cap-turn-intents-into-work", "fn-818": "cap-turn-intents-into-work",
         "fn-798": "cap-write-work-evals", "fn-898": "cap-write-work-evals"}
newdoc = {old.split("/")[-2]: new for old, new in OLDP.items()}
w("link-request.json", {"by": BY + "; take-in approved by the product owner",
  "parts": [{"id": f, "kind": "feature", "mode": "update", "capability": c, "doc": newdoc[f]} for f, c in moves.items()]})
# step 5: merge the two emptied capabilities
w("remove-request-3.json", {"by": BY, "approved_by": "the product owner", "source": SRC,
  "remove": [{"kind": "capability", "id": "cap-718", "into": "cap-turn-intents-into-work"},
             {"kind": "capability", "id": "cap-shape-eval", "into": "cap-write-work-evals"}]})
open(f"{HERE}/changes-diff.md", "w", encoding="utf-8").write("\n".join(diff))
print("named lines: pages", len(pages), "changes", sum(len(p["changes"]) for p in pages))
