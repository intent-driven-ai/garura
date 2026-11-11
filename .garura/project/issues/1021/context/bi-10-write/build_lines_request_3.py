"""Build the third named-lines request for BI-10: 21 short label bullets on the new pages that the structure check
counts as errors ("a telegraphic label"), each widened to a full phrase with the same meaning. Applies the same changes
to the drafts, so the drafts stay equal to the model. Run from the repo root; writes lines-request-3.json.
"""
import json, os
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
S = "software-delivery-planning"
RUN = {"standards": 1, "build-your-own-harness": 2, "structure": 3, "settings": 4, "memory": 5, "model-routing": 6}
CH = [
 ("features/fn-738/feature.md", "- Two changes are recorded so far:", "- Two changes to the standard are recorded so far, each as an accepted ADR:"),
 ("features/fn-741/feature.md", "- In: the rename map.", "- In: the rename map, which pairs every old name with its new name."),
 ("features/fn-744/feature.md", "- Under ADR 046, built:", "- Built under ADR 046, these plays took their new names:"),
 ("features/fn-745/feature.md", "- Under ADR 046, built:", "- Built under ADR 046, these plays took their new names:"),
 ("features/fn-745/feature.md", "- Not decided: the name for /release-increment.", "- Not decided: the name that /release-increment takes under the standard."),
 (f"{S}/build-your-own-harness/fn-build-loop/feature.md", "  - how it ends.", "  - how the loop ends: its end steps and its close."),
 (f"{S}/build-your-own-harness/fn-change-loop/feature.md", "  - the checker or the runner: the loop's settings;", "  - the checker or the runner, which are the loop's settings;"),
 (f"{S}/build-your-own-harness/fn-mark-play-running/feature.md", "- In: the play's close.", "- In: the play's close, when the run ends."),
 (f"{S}/build-your-own-harness/fn-build-agent-skill/feature.md", "- What exists to build to:", "- What a team can already build a new part to, today:"),
 (f"{S}/structure/fn-garura-folder-list/feature.md", "  - `product/`: the product model;", "  - `product/`: the product model, with its pages and its spine;"),
 (f"{S}/structure/fn-run-records-with-issue/feature.md", "- What exists today:", "- What exists today, for the records of a run:"),
 (f"{S}/structure/fn-run-records-with-issue/feature.md", "- What is open:", "- What is still open, for the records of a run:"),
 (f"{S}/settings/fn-settings-folder/feature.md", "- What stays where it is:", "- What stays where it is, outside the settings folder:"),
 (f"{S}/settings/fn-checkpoint-settings/feature.md", "- How the policy is learned:", "- How the policy is learned, from each crossing of a checkpoint:"),
 (f"{S}/settings/fn-evidence-setting/feature.md", "- In: `evidence.record`, the default.", "- In: `evidence.record`, the setting for every play, which is the default."),
 (f"{S}/settings/fn-settings-others-need/feature.md", "- Built, and read today:", "- Built, and read by a play or a tool today:"),
 (f"{S}/settings/fn-tools-read-settings/feature.md", "- What each tool does today:", "- What each tool does today, tool by tool:"),
 (f"{S}/memory/fn-read-through-tool/feature.md", "- The protocol's steps:", "- The protocol's steps, in the order an agent takes them:"),
 (f"{S}/memory/fn-promote-page/feature.md", "- What is planned around it:", "- What is planned around it, in open issues:"),
 (f"{S}/memory/fn-decide-inside-memory/feature.md", "- What is planned:", "- What is planned, in an ADR and an open issue:"),
 (f"{S}/model-routing/fn-step-on-set-model/feature.md", "- In: the session's own model.", "- In: the session's own model, to tell it apart from the named one."),
]
def draft(rel):
    if rel.startswith("features/"):
        return f".garura/project/issues/1021/context/bi-10-capability-1/drafts/product-os/{rel}"
    slug = rel.split("/")[1]
    return f".garura/project/issues/1021/context/bi-10-capability-{RUN[slug]}/drafts/product-os/{rel}"
by = {}
for rel, o, n in CH:
    by.setdefault(rel, []).append((o, n))
pages = []
for rel, subs in by.items():
    lines = open(f"{MODEL}/{rel}", encoding="utf-8").read().split("\n")
    new, changes = list(lines), []
    for o, n in subs:
        hit = [i for i, l in enumerate(lines) if l == o]
        assert len(hit) == 1, (rel, o, len(hit))
        new[hit[0]] = n
        changes.append({"old": o, "new": n})
    pages.append({"page": rel, "changes": changes})
    d = draft(rel)
    assert open(d, encoding="utf-8").read() == "\n".join(lines), d
    open(d, "w", encoding="utf-8").write("\n".join(new))
json.dump({"by": "product-os-keeper (reorganise business intents, #1021)",
           "source": f"{HERE}/approval.md: the approved pages, with 21 short label bullets widened to full phrases of the same meaning, so the structure check finds no new error",
           "pages": pages}, open(f"{HERE}/lines-request-3.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("pages", len(pages), "changes", len(CH))
