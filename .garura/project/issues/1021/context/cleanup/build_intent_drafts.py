"""Build BI-1's and BI-3's intent drafts: each page as it is, with its Touches list plus the features it takes in from
the two old capabilities, marked changes. Run from the repo root before the write; writes intent-draft-bi-1.json and
intent-draft-bi-3.json here. Titles are read from the feature pages as they are now.
"""
import json, os, re
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
MODEL = ".garura/product/product-os"
S = "software-delivery-planning"
TOUCH = re.compile(r"^- \[(.+)\]\((.+)\) \((capability|feature|domain)\) — (adds|changes|removes)$")
ADD = {"bi-1": [("fn-727", f"{S}/cap-718/fn-727/feature.md", f"{S}/turn-intents-into-work/fn-727/feature.md"),
                ("fn-728", f"{S}/cap-718/fn-728/feature.md", f"{S}/turn-intents-into-work/fn-728/feature.md"),
                ("fn-818", f"{S}/cap-718/fn-818/feature.md", f"{S}/turn-intents-into-work/fn-818/feature.md")],
       "bi-3": [("fn-798", f"{S}/shape-eval/fn-798/feature.md", f"{S}/write-work-evals/fn-798/feature.md"),
                ("fn-898", f"{S}/shape-eval/fn-898/feature.md", f"{S}/write-work-evals/fn-898/feature.md")]}
for bi, adds in ADD.items():
    lines = open(f"{MODEL}/intents/{bi}.md", encoding="utf-8").read().split("\n")
    one = lambda label: [l for l in lines if l.startswith(f"**{label}:** ")][0][len(f"**{label}:** "):]
    i = lines.index("**Proof it is met:**")
    proof = []
    for l in lines[i + 1:]:
        if not l.startswith("- "):
            break
        proof.append(l[2:])
    assert not any(l.startswith(("**Rules:**", "**Serves:**", "**Identified by:**")) for l in lines), bi
    t = lines.index("**Touches:**")
    touches = []
    for l in lines[t + 1:]:
        if not l.startswith("- "):
            break
        m = TOUCH.match(l)
        assert m, (bi, l)
        touches.append({"title": m.group(1), "link": m.group(2), "kind": m.group(3), "mark": m.group(4)})
    n0 = len(touches)
    for fid, now, later in adds:
        head = open(f"{MODEL}/{now}", encoding="utf-8").readline().rstrip("\n")
        assert head.startswith("# Feature: ")
        assert not any(x["link"].endswith(later) for x in touches)
        touches.append({"title": head[len("# Feature: "):], "link": f"../{later}", "kind": "feature", "mark": "changes"})
    draft = {"id": bi, "issue": int(bi[3:]), "title": lines[0][2:], "outcome": one("Outcome"), "why": one("Why"),
             "asked_by": one("Asked by"), "proof": proof, "must_not": one("Must not"), "touches": touches}
    json.dump(draft, open(f"{HERE}/intent-draft-{bi}.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    stage = [l for l in lines if l.startswith("**Stage:**")][0]
    print(bi, n0, "->", len(touches), "|", stage)
