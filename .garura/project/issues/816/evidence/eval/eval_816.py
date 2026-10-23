#!/usr/bin/env python3
"""
eval_816.py — the eval for the grouped change #816 + #817 + #815 + #820 (plan 788).

Written before the build. It must fail before the build and pass after it.
A builder never reads this file.

    python3 .garura/project/issues/816/evidence/eval/eval_816.py [--root .]

Exit 0 when every check passes, 1 when one fails.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

ONTOLOGY = "core/components/memory/standards/schemas/product-os/ontology.md"
CONFIG = "core/config.yaml"
GRILL = "core/components/plays/shape-slice/scripts/grill_budget.py"
GRILL_TEST = "core/components/plays/shape-slice/scripts/test_grill_budget.py"
OLD_NAMES = "core/tools/naming/check_old_names.py"
NAMING_TEST = "core/tools/naming/test_naming_tools.py"
ASK_RULE = "core/components/memory/standards/rules/asking-a-person.md"
EDIT_ONTOLOGY = "core/components/plays/edit-ontology/SKILL.md"
AUTHOR_SKILL = "core/components/skills/author-product-ontology/SKILL.md"
CHECK_ONTOLOGY = "core/components/plays/edit-ontology/scripts/check_ontology.py"

results = []


def check(name, ok, detail=""):
    results.append({"check": name, "ok": bool(ok), "detail": detail})


def read(root, rel):
    p = os.path.join(root, rel)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def run(root, args, stdin=None):
    return subprocess.run(args, cwd=root, capture_output=True, text=True, input=stdin)


def section(text, heading):
    """The body of one '### heading' kind section, up to the next '### ' or '## '."""
    m = re.search(r"^### " + re.escape(heading) + r"\s*$(.*?)(?=^### |^## )", text, re.M | re.S)
    return m.group(1) if m else ""


def before_log(text):
    return text.split("\n## Log", 1)[0]


def eval_816(root):
    text = read(root, ONTOLOGY) or ""
    head = before_log(text)
    check("816: ontology is version 9", re.search(r"^version:\s*9\s*$", text, re.M))
    check("816: one v9 log line", len(re.findall(r"^- \d{4}-\d{2}-\d{2} — v9 ", text, re.M)) == 1)
    slice_ = section(text, "Slice")
    plan = section(text, "Plan")
    check("816: Slice serves Business Intent", re.search(r"serves", slice_) and "Business Intent" in slice_)
    check("816: Slice has the testable-surface rule", re.search(r"test(ed|able)? end to end", slice_))
    check("816: Slice names its eval and the evals folder", "eval" in slice_ and "evals/" in text)
    check("816: Slice names its usage guide", re.search(r"usage guide", slice_, re.I))
    check("816: a builder never reads the eval", re.search(r"builder never reads", head, re.I))
    check("816: the eval never reads the ICE", re.search(r"never (reads )?(the )?ICE", slice_ + plan, re.I)
          or re.search(r"never the ICE", slice_, re.I))
    check("816: no 'two tests' outside the log", not re.search(r"two tests", head, re.I))
    check("816: no 'picks a slice' outside the log", not re.search(r"picks? (a |the )?slice", head, re.I))
    check("816: one plan for each business intent", re.search(r"one plan (for each|per) business intent", head, re.I)
          or re.search(r"never (has )?a second plan", head, re.I))
    check("816: questions Q27 to Q31 exist", all(re.search(r"\bQ%d\b" % n, text) for n in range(27, 32)))
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "check.json")
        r = run(root, [sys.executable, CHECK_ONTOLOGY, "--ontology", ONTOLOGY, "--out", out])
        valid = False
        if os.path.exists(out):
            with open(out, encoding="utf-8") as fh:
                valid = json.load(fh).get("valid") is True
        check("816: check_ontology reads valid", r.returncode == 0 and valid, r.stdout[-300:] + r.stderr[-300:])
    claude = read(root, "CLAUDE.md") or ""
    check("816: CLAUDE.md says a builder never reads a plan's evals folder",
          "evals/" in claude and re.search(r"never read", claude, re.I))


def eval_817(root):
    import yaml
    cfg = yaml.safe_load(read(root, CONFIG) or "") or {}
    check("817: config has shape-slice.grill-tier: m", (cfg.get("shape-slice") or {}).get("grill-tier") == "m")
    if not os.path.exists(os.path.join(root, GRILL)):
        check("817: grill_budget.py exists", False)
        return
    with tempfile.TemporaryDirectory() as tmp:
        for tier, budget in (("xs", 5), ("s", 12), ("m", 25), ("l", 45), ("xl", 70)):
            p = os.path.join(tmp, "c-%s.yaml" % tier)
            with open(p, "w") as fh:
                fh.write("shape-slice:\n  grill-tier: %s\n" % tier)
            r = run(root, [sys.executable, GRILL, "tier", "--config", p])
            ok = r.returncode == 0 and json.loads(r.stdout or "{}") == {"tier": tier, "budget": budget}
            check("817: tier %s gives %d" % (tier, budget), ok, r.stdout + r.stderr)
        p = os.path.join(tmp, "none.yaml")
        with open(p, "w") as fh:
            fh.write("project:\n  name: x\n")
        r = run(root, [sys.executable, GRILL, "tier", "--config", p])
        check("817: absent setting gives m, 25", r.returncode == 0
              and json.loads(r.stdout or "{}") == {"tier": "m", "budget": 25}, r.stdout + r.stderr)
        p = os.path.join(tmp, "bad.yaml")
        with open(p, "w") as fh:
            fh.write("shape-slice:\n  grill-tier: huge\n")
        r = run(root, [sys.executable, GRILL, "tier", "--config", p])
        check("817: unknown tier exits 2", r.returncode == 2, r.stdout + r.stderr)

        def split(qs, budget):
            q = os.path.join(tmp, "q.json")
            with open(q, "w") as fh:
                json.dump(qs, fh)
            r = run(root, [sys.executable, GRILL, "split", "--questions", q, "--budget", str(budget)])
            return r, (json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else {})

        def ids(items):
            return [i["id"] if isinstance(i, dict) else i for i in items]

        qs = [{"id": "a", "blocking": False}, {"id": "b", "blocking": True},
              {"id": "c", "blocking": False}, {"id": "d", "blocking": False}]
        r, out = split(qs, 2)
        asked, assumed = ids(out.get("asked", [])), ids(out.get("assumptions", []))
        check("817: split asks every blocking question", "b" in asked, r.stdout + r.stderr)
        check("817: split asks no more than the budget", len(asked) == 2, str(asked))
        check("817: split fills the budget in the given order", asked and set(asked) == {"a", "b"}, str(asked))
        check("817: each question not asked is an assumption", sorted(assumed) == ["c", "d"], str(assumed))
        check("817: over_budget false when blocking fits", out.get("over_budget") is False)
        qs = [{"id": x, "blocking": True} for x in "xyz"]
        r, out = split(qs, 2)
        check("817: blocking over budget are all asked", sorted(ids(out.get("asked", []))) == ["x", "y", "z"],
              r.stdout + r.stderr)
        check("817: blocking over budget sets over_budget", out.get("over_budget") is True)
    r = run(root, [sys.executable, GRILL_TEST])
    check("817: grill_budget tests pass", os.path.exists(os.path.join(root, GRILL_TEST)) and r.returncode == 0,
          r.stdout[-300:])


def eval_815(root):
    src = read(root, OLD_NAMES) or ""
    check("815: FIRST_NEW_ADR is gone", "FIRST_NEW_ADR" not in src)
    check("815: FIRST_RENAME_ADR is used", "FIRST_RENAME_ADR" in src)
    tests = read(root, NAMING_TEST) or ""
    check("815: test for ADR 049 searched", "049" in tests)
    check("815: test for SUPERSEDED-046 skipped", "SUPERSEDED-046" in tests)
    check("815: test for SUPERSEDED-047 searched", "SUPERSEDED-047" in tests)
    r = run(root, [sys.executable, NAMING_TEST])
    check("815: naming tests pass", r.returncode == 0, r.stdout[-300:])
    r = run(root, [sys.executable, OLD_NAMES, "--root", "."])
    check("815: old-name check reads 0", r.returncode == 0, r.stdout[-300:])


def eval_820(root):
    rule = read(root, ASK_RULE) or ""
    check("820: asking-a-person rule exists", bool(rule))
    for part in ("Question", "Answer", "Why it matters", "Example"):
        check("820: rule names the part '%s'" % part, part in rule)
    check("820: rule says each question asks one thing", re.search(r"one thing", rule, re.I))
    check("820: rule asks for several examples", re.search(r"several examples|more than one example", rule, re.I))
    check("820: rule says the opening names the decision", re.search(r"decide", rule, re.I))
    for rel in (EDIT_ONTOLOGY, AUTHOR_SKILL):
        check("820: %s points to the rule" % rel, "asking-a-person.md" in (read(root, rel) or ""))


def eval_old_suites(root):
    # The test files are plain scripts (no pytest here): run each one.
    for rel in ("core/components/plays/edit-ontology/scripts", "core/components/plays/shape-slice/scripts",
                "core/tools/naming"):
        d = os.path.join(root, rel)
        for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if name.startswith("test_") and name.endswith(".py"):
                r = run(root, [sys.executable, os.path.join(rel, name)])
                check("all: %s/%s passes" % (rel, name), r.returncode == 0, r.stdout[-300:] + r.stderr[-300:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    for fn in (eval_816, eval_817, eval_815, eval_820, eval_old_suites):
        try:
            fn(root)
        except Exception as e:  # a crash is a failed check, never a pass
            check("%s ran" % fn.__name__, False, repr(e))
    failed = [r for r in results if not r["ok"]]
    report = {"passed": len(results) - len(failed), "failed": len(failed), "results": results}
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(report, fh, indent=2)
    for r in results:
        print(("PASS " if r["ok"] else "FAIL ") + r["check"])
    print("%d passed, %d failed" % (report["passed"], report["failed"]))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
