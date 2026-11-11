"""Find each quoted span on the drafts in the files the run read; print the ones found nowhere."""
import glob, re, sys, os
run = sys.argv[1]
pages = sorted(glob.glob(f"{run}/drafts/**/*.md", recursive=True))
corpus_files = [
 ".garura/project/issues/1021/context/capabilities.md",
 ".garura/project/issues/1021/context/bi-11-inventory/inventory.md",
 ".garura/project/issues/1021/context/bi-11-write/old-pages/link-the-product-model.md",
 ".garura/product/product-os/features/fn-597/feature.md",
 ".garura/product/product-os/features/fn-628/feature.md",
 ".garura/product/product-os/intents/bi-11.md", ".garura/product/product-os/intents/bi-9.md",
 ".garura/product/product-os/intents/bi-7.md",
 ".garura/product/product-os/decisions/dec-cap-initialize-security-none-medium.yaml",
 "docs/standards/harness-standard.md", "docs/adr/028-agentic-lifecycle-five-loops.md",
 "docs/adr/033-approval-in-the-product-model.md",
 "core/config.yaml", "core/grounding/glossary.md",
 "core/components/plays/edit-ontology/SKILL.md", "core/components/plays/edit-ontology/reference/ice.md",
 "core/components/skills/author-product-ontology/SKILL.md",
 "core/components/skills/author-product-ontology/scripts/check_ontology.py",
 "core/components/plays/install-garura/scripts/install.py",
 "core/components/plays/discover-intent/SKILL.md", "core/components/plays/shape-slice/SKILL.md",
 "core/components/plays/shape-slice/scripts/lint_grounding.py",
 "core/components/skills/link-model-part/scripts/model_names.py",
 "core/components/agents/product-os-keeper.md",
] + glob.glob(f"{run}/checks/gh/*.md") + glob.glob(f"{run}/checks/memory/*") \
  + glob.glob(".garura/product/product-os/software-delivery-planning/**/*.md", recursive=True)
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"(?m)^\s*#\s*", " ", s)).strip()
corpus = " ".join(norm(open(f, encoding="utf-8").read()) for f in corpus_files if os.path.isfile(f))
corpus2 = corpus.replace("**", "")
missing = []
for p in pages:
    for n, line in enumerate(open(p, encoding="utf-8"), 1):
        for q in re.findall(r'"([^"]{12,})"', line):
            qn = norm(q)
            if qn not in corpus and qn not in corpus2:
                missing.append((os.path.relpath(p, run), n, q[:140]))
for m in missing:
    print(*m, sep=" | ")
print("not found:", len(missing))
