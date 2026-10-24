#!/usr/bin/env python3
"""test_check_ice_workable.py — fixture tests for check_ice_workable.py (#612, v5 #724).

An ICE is workable only when its node serves a confirmed business intent and nothing it
needs is open; no intent, a proposed or dropped one, or a missing page leaves it kept but
not workable. A missing domain is a warning, never a block (ontology v5).

    python3 test_check_ice_workable.py
"""
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_ice_workable as cw  # noqa: E402

PASSED = 0
FAILED = 0


def check(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name}")
        if os.environ.get("PYTEST_CURRENT_TEST"):
            raise AssertionError(name)


def page(stage):
    return f"# An intent\n\n**Outcome:** something\n**Stage:** {stage} — by the product owner, 2026-10-09\n"


def setup(tmp):
    intents = os.path.join(tmp, "intents")
    os.makedirs(intents)
    for iid, stage in (("confirmed-one", "confirmed"), ("proposed-one", "proposed"),
                       ("dropped-one", "dropped"), ("met-one", "met")):
        with open(os.path.join(intents, f"{iid}.md"), "w") as fh:
            fh.write(page(stage))
    spine = {"domains": [{"id": "d1"}], "capabilities": [
        {"id": "cap-ok", "domain": "d1", "intents": ["proposed-one", "confirmed-one"]},
        {"id": "cap-loose", "domain": "", "intents": ["confirmed-one"]},
        {"id": "cap-none", "domain": "d1"},
        {"id": "cap-proposed", "domain": "d1", "intents": ["proposed-one"]},
        {"id": "cap-dropped", "domain": "d1", "intents": ["dropped-one"]},
        {"id": "cap-missing", "domain": "d1", "intents": ["no-such-intent"]},
        {"id": "cap-met", "domain": "d1", "intents": ["met-one"]}],
        "features": [{"id": "fn-ok", "capability": "cap-ok", "intents": ["confirmed-one"]},
                            {"id": "fn-loose", "capability": "", "intents": ["confirmed-one"]},
                            {"id": "fn-under-loose", "capability": "cap-loose", "intents": ["confirmed-one"]},
                            {"id": "fn-via-cap", "capability": "cap-ok"},
                            {"id": "fn-needs-cap", "capability": "cap-ok", "intents": ["confirmed-one"], "depends_on": ["cap-loose"]},
                            {"id": "fn-under-proposed", "capability": "cap-proposed", "intents": ["confirmed-one"]}]}
    path = os.path.join(tmp, "_spine.yaml")
    with open(path, "w") as fh:
        yaml.safe_dump(spine, fh)
    return path, intents


FULL_ICE = """## Intent

- **Goal:** A shopper can pay without making an account.
- **Limit:** No stored card details.
- **Fails if:** The shopper must sign up to pay.

## Context

- **Read:** the checkout page and the cart spine entry.
- **Never read:** other shoppers' orders.
- **Persona:** a first-time shopper.
- **Scope:** paying for one cart; not refunds.

## Expectation

- **Scenario:** a shopper with no account pays for one item and gets a receipt.
- **Done means:** the receipt is sent and the order is stored.
- **Quality need:** PCI for the payment step.
"""
LIGHT_ICE = "## Intent\n\n- **Goal:** pay.\n\n## Context\n\n- **Read:** cart.\n\n## Expectation\n\n- **Scenario:** pays.\n"
NO_CONTEXT = "## Intent\n\n- **Goal:** pay.\n\n## Expectation\n\n- **Scenario:** pays.\n"
EMPTY_EXP = "## Intent\n\n- **Goal:** pay.\n\n## Context\n\n- **Read:** cart.\n\n## Expectation\n\n"
THIN_LINE = "Thin: proposed by `/shape-slice` from the person's answers; deepen with `/discover-capabilities`.\n\n"
THIN_ICE = THIN_LINE + "## Intent\n\n- **Goal:** pay.\n- **Limit:** card only.\n- **Fails if:** a card is charged twice.\n\n## Context\n\n- **Persona:** shopper.\n\n## Expectation\n\n- **Done means:** the order is paid.\n"


def setup_v6(tmp):
    """Ontology v6 (#760): ICE nodes in an `ices` list, one ice.md each."""
    root = os.path.join(tmp, "v6")
    intents = os.path.join(root, "intents")
    os.makedirs(intents)
    for iid, stage in (("bi-ok", "confirmed"), ("bi-prop", "proposed")):
        with open(os.path.join(intents, f"{iid}.md"), "w") as fh:
            fh.write(page(stage))
    pages = {"cap-a": FULL_ICE, "cap-loose": LIGHT_ICE, "cap-noid": LIGHT_ICE, "cap-prop": FULL_ICE,
             "cap-needs": LIGHT_ICE, "cap-noctx": NO_CONTEXT, "cap-emptyexp": EMPTY_EXP,
             "cap-thin": THIN_ICE, "cap-thin-page": THIN_ICE, "cap-thin-spine": LIGHT_ICE, "cap-thin-text": LIGHT_ICE, "fn-a": LIGHT_ICE, "fn-orphan": LIGHT_ICE, "fn-under-prop": LIGHT_ICE, "fn-own-needs": LIGHT_ICE}
    ices = []
    for n, (part, text) in enumerate(pages.items(), 1):
        rel = f"{part}/ice.md"
        os.makedirs(os.path.join(root, part))
        with open(os.path.join(root, rel), "w") as fh:
            fh.write(text)
        ice = {"id": f"ice-{n}", "for": part,
               "for_kind": "capability" if part.startswith("cap-") else "feature", "doc": rel}
        if part in ("cap-thin", "cap-thin-spine"):
            ice["metadata"] = {"thin": True}
        if part == "cap-thin-text":
            ice["metadata"] = {"thin": "false"}
        ices.append(ice)
    spine = {"domains": [{"id": "d1"}],
             "capabilities": [
                 {"id": "cap-a", "domain": "d1", "intents": ["bi-ok"], "identified_by": "cap-x"},
                 {"id": "cap-loose", "domain": "", "intents": ["bi-ok"], "identified_by": "cap-a"},
                 {"id": "cap-noid", "domain": "d1", "intents": ["bi-ok"]},
                 {"id": "cap-prop", "domain": "d1", "intents": ["bi-prop"], "identified_by": "cap-a"},
                 {"id": "cap-needs", "domain": "d1", "intents": ["bi-ok"], "identified_by": "cap-a",
                  "depends_on": ["cap-a", "fn-a"]},
                 {"id": "cap-noctx", "domain": "d1", "intents": ["bi-ok"], "identified_by": "cap-a"},
                 {"id": "cap-emptyexp", "domain": "d1", "intents": ["bi-ok"], "identified_by": "cap-a"},
                 {"id": "cap-noice", "domain": "d1", "intents": ["bi-ok"], "identified_by": "cap-a"},
                 {"id": "cap-thin", "domain": "d1", "intents": ["bi-ok"], "identified_by": "cap-a"},
                 {"id": "cap-thin-page", "domain": "d1", "intents": ["bi-ok"], "identified_by": "cap-a"},
                 {"id": "cap-thin-spine", "domain": "d1", "intents": ["bi-ok"], "identified_by": "cap-a"},
                 {"id": "cap-thin-text", "domain": "d1", "intents": ["bi-ok"], "identified_by": "cap-a"}],
             "features": [
                 {"id": "fn-a", "capability": "cap-a", "intents": ["bi-prop"]},
                 {"id": "fn-orphan", "capability": "", "intents": ["bi-ok"]},
                 {"id": "fn-under-prop", "capability": "cap-prop", "intents": ["bi-ok"]},
                 {"id": "fn-own-needs", "capability": "cap-a", "depends_on": ["cap-prop"]}],
             "ices": ices}
    path = os.path.join(root, "_spine.yaml")
    with open(path, "w") as fh:
        yaml.safe_dump(spine, fh)
    return path, intents


def v6_tests(tmp):
    import json
    spine, intents = setup_v6(tmp)
    args = ["--spine", spine, "--intents-dir", intents]
    out = os.path.join(tmp, "v6.json")

    def node(n, extra=()):
        code = cw.main(args + ["--node", n, "--out", out] + list(extra))
        with open(out) as fh:
            return code, json.load(fh)

    print("ICE nodes (ontology v6, #760)")
    code, r = node("cap-a")
    check("ready: confirmed intent, all three parts, no gaps — exit 0", code == 0 and r["answer"] == "ready"
          and r["gaps"] == [] and r["stops"] == [])
    check("the answer keeps `workable` for old callers", r["workable"] is True)
    check("--node takes the ICE id as well as the part id", node("ice-1")[1]["for"] == "cap-a")
    check("the check does not count lines: no richness report (v11)", "richness" not in r)

    code, r = node("cap-loose")
    check("partly ready: no domain — exit 0, gap listed", code == 0 and r["answer"] == "partly_ready"
          and any("domain" in g for g in r["gaps"]))
    check("a short ICE with no thin mark is not thin: no thin gap (v11)",
          not any("thin" in g for g in r["gaps"]) and "richness" not in r)
    code, r = node("cap-thin")
    check("partly ready: the thin mark (page line and spine) gives the gap 'thin ICE' — exit 0 (v11)",
          code == 0 and r["answer"] == "partly_ready" and r["gaps"] == ["thin ICE"] and r["thin"] is True)
    code, r = node("cap-thin-page")
    check("the Thin line on the page with no `thin: true` in the spine is drift, and still thin (v11)",
          r["answer"] == "partly_ready" and "thin ICE" in r["gaps"]
          and any("thin mark" in g and "spine" in g for g in r["gaps"]))
    code, r = node("cap-thin-spine")
    check("`thin: true` in the spine with no Thin line on the page is drift, and still thin (v11)",
          r["answer"] == "partly_ready" and "thin ICE" in r["gaps"]
          and any("thin mark" in g and "page" in g for g in r["gaps"]))
    code, r = node("cap-a")
    check("an ICE with no thin mark reads thin false (v11)", r["thin"] is False)
    code, r = node("cap-thin-text")
    check("only the value true is the thin mark: the text 'false' is not thin (v11)",
          r["thin"] is False and r["answer"] == "ready")
    code, r = node("cap-noid")
    check("partly ready: no identified-by — gap listed", r["answer"] == "partly_ready"
          and any("identified by" in g for g in r["gaps"]))

    code, r = node("cap-prop")
    check("not ready: no confirmed business intent — exit 1", code == 1 and r["answer"] == "not_ready"
          and any("business intent" in s for s in r["stops"]))
    code, r = node("cap-noctx")
    check("not ready: a missing part (Context)", r["answer"] == "not_ready" and any("Context" in s for s in r["stops"]))
    code, r = node("cap-emptyexp")
    check("not ready: an empty part (Expectation)", r["answer"] == "not_ready"
          and any("Expectation" in s for s in r["stops"]))
    code, r = node("cap-noice")
    check("not ready: a capability with no ICE at all", code == 1 and r["answer"] == "not_ready"
          and any("no ICE" in s for s in r["stops"]))

    done_none = os.path.join(tmp, "v6-done-none.yaml")
    with open(done_none, "w") as fh:
        yaml.safe_dump([], fh)
    done_a = os.path.join(tmp, "v6-done-a.yaml")
    with open(done_a, "w") as fh:
        yaml.safe_dump(["cap-a"], fh)
    code, r = node("cap-needs", ["--done", done_none])
    check("not ready: a needed capability is not done", r["answer"] == "not_ready" and r["needs_open"] == ["cap-a"])
    check("needs are read between capabilities only (fn-a is not a need)", r["needs"] == ["cap-a"])
    code, r = node("cap-needs", ["--done", done_a])
    check("a needed capability that is done no longer stops", r["answer"] == "ready")

    code, r = node("fn-a")
    check("a feature finds its business intent through its parent (its own intents are not read)",
          r["answer"] == "ready")
    code, r = node("fn-orphan")
    check("not ready: a feature with no parent capability", r["answer"] == "not_ready"
          and any("capability" in s for s in r["stops"]))
    code, r = node("fn-under-prop")
    check("not ready: a feature whose parent serves no confirmed intent", r["answer"] == "not_ready")
    code, r = node("fn-own-needs", ["--done", done_none])
    check("a feature's own needs are not read (v6: it never needs anything)", r["answer"] == "ready")

    code = cw.main(args + ["--out", out])
    with open(out) as fh:
        r = json.load(fh)
    check("the full report counts each answer", code == 0 and r["counts"] == {"ready": 5, "partly_ready": 5,
                                                                              "not_ready": 6})
    check("an unknown node exits 2", cw.main(args + ["--node", "nope"]) == 2)

    here = os.path.join(HERE, "check_ice_workable.py")
    copy = os.path.join(HERE, "..", "..", "discover-intent", "scripts", "check_ice_workable.py")
    with open(here, "rb") as a, open(copy, "rb") as b:
        check("both copies of check_ice_workable.py are identical", a.read() == b.read())


def main():
    with tempfile.TemporaryDirectory() as tmp:
        v6_tests(tmp)
        spine, intents = setup(tmp)
        args = ["--spine", spine, "--intents-dir", intents]
        check("built from a confirmed intent is workable (one confirmed is enough)",
              cw.main(args + ["--node", "cap-ok"]) == 0)
        check("a feature is checked the same way", cw.main(args + ["--node", "fn-ok"]) == 0)
        check("built from a met intent stays workable", cw.main(args + ["--node", "cap-met"]) == 0)
        for node, label in (("cap-none", "no intent at all"), ("cap-proposed", "only a proposed intent"),
                            ("cap-dropped", "only a dropped intent"), ("cap-missing", "an intent with no page")):
            check(f"{label} is kept but not workable", cw.main(args + ["--node", node]) == 1)
        check("a capability with no domain is ready from a confirmed intent (v5)",
              cw.main(args + ["--node", "cap-loose"]) == 0)
        check("a feature whose capability has no domain is ready (v5)",
              cw.main(args + ["--node", "fn-under-loose"]) == 0)
        check("a feature with no capability is kept but not ready",
              cw.main(args + ["--node", "fn-loose"]) == 1)
        check("a feature is ready through its capability's confirmed intent",
              cw.main(args + ["--node", "fn-via-cap"]) == 0)
        check("a feature under a capability that is not ready is not ready",
              cw.main(args + ["--node", "fn-under-proposed"]) == 1)
        done_none = os.path.join(tmp, "done-none.yaml")
        with open(done_none, "w") as fh:
            yaml.safe_dump([], fh)
        done_cap = os.path.join(tmp, "done-cap.yaml")
        with open(done_cap, "w") as fh:
            yaml.safe_dump(["cap-loose"], fh)
        check("an open need blocks: not ready",
              cw.main(args + ["--node", "fn-needs-cap", "--done", done_none]) == 1)
        check("a need that is done no longer blocks",
              cw.main(args + ["--node", "fn-needs-cap", "--done", done_cap]) == 0)
        check("without a done list, needs are listed but not judged",
              cw.main(args + ["--node", "fn-needs-cap"]) == 0)
        r1 = cw.assess({"id": "cap-loose", "domain": "", "intents": ["confirmed-one"]}, "capability", intents,
                       {"domains": [{"id": "d1"}]})
        check("a missing domain shows as a warning", any("no domain" in w for w in r1["warnings"]))
        check("an unknown node is an error, not a pass", cw.main(args + ["--node", "nope"]) == 2)
        out = os.path.join(tmp, "r.json")
        check("the full report runs and exits 0", cw.main(args + ["--out", out]) == 0)
        import json
        with open(out) as fh:
            r = json.load(fh)
        check("the report counts workable and not workable", r["workable"] == 7 and r["not_workable"] == 6)
        bad = os.path.join(tmp, "bad.yaml")
        with open(bad, "w") as fh:
            fh.write("- not a mapping\n")
        check("an unreadable spine exits 2", cw.main(["--spine", bad, "--intents-dir", intents]) == 2)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
