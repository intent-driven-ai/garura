"""Find each quoted span on the drafts in the files the run read; print the ones found nowhere."""
import glob, re, sys, os
run = sys.argv[1]
pages = sorted(glob.glob(f"{run}/drafts/**/*.md", recursive=True))
corpus_files = [
 ".garura/project/issues/1021/context/capabilities.md",
 ".garura/project/issues/1021/context/bi-10-inventory/inventory.md",
 ".garura/product/product-os/intents/bi-10.md", ".garura/product/product-os/intents/bi-9.md",
 "docs/standards/harness-standard.md", "docs/adr/055-installed-parts-read-only-installed-files.md",
 "CLAUDE.md", "docs/components/loops.md", "docs/components/agents.md",
 "core/components/plays/create-play/SKILL.md", "core/components/plays/edit-play/SKILL.md",
 "core/components/plays/create-loop/SKILL.md", "core/components/plays/edit-loop/SKILL.md",
 "core/components/plays/create-loop/scripts/lint_loop.py", "core/components/plays/install-garura/scripts/install.py",
 "core/components/plays/create-play/references/workflow-structures.md",
 "core/components/plays/create-play/references/agent-audit.md",
 "core/components/plays/create-play/references/session_stamp.py",
 "core/components/plays/shape-eval/SKILL.md",
] + glob.glob(f"{run}/checks/gh/*.md") + glob.glob(".garura/product/product-os/software-delivery-planning/**/*.md", recursive=True)
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"(?m)^\s*#\s*", " ", s)).strip()
corpus = " ".join(norm(open(f, encoding="utf-8").read()) for f in corpus_files if os.path.isfile(f))
# also allow text with markdown bold stripped
corpus2 = corpus.replace("**", "")
missing = []
for p in pages:
    for n, line in enumerate(open(p, encoding="utf-8"), 1):
        for q in re.findall(r'"([^"]{12,})"', line):
            qn = norm(q)
            if qn not in corpus and qn not in corpus2:
                missing.append((os.path.relpath(p, run), n, q[:120]))
for m in missing:
    print(*m, sep=" | ")
print("not found:", len(missing))
