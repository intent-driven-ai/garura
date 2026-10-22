#!/usr/bin/env python3
"""test_lint_ice.py — fixture tests for lint_grounding.py's ICE node checks (ontology v6, #759).

An ICE is its own node: one `ice.md` page in its part's folder with the three sections
Intent, Context and Expectation, and one entry in the spine's `ices` list (`id`, `for`,
`for_kind`, `doc`, `metadata`). The linter checks the shape and the links, never whether a
part is thin or wrong. A model with no `ices` list is linted as before.

    python3 test_lint_ice.py
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lint_grounding as lg  # noqa: E402

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


GOOD_ICE = """## Intent

- **Goal:** A shopper can pay without making an account.

## Context

- **Read:** the checkout capability page and the cart spine entry.

## Expectation

- **Scenario:** a shopper with no account pays for one item and gets a receipt.
"""


def write(root, rel, text):
    full = os.path.join(root, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text)


def spine(ices, extra_caps=""):
    out = ["capabilities:",
           "  - id: cap-checkout", "    slug: checkout", "    one_line: Shoppers pay for what is in their cart.",
           "    doc: capabilities/checkout/capability.md", "    status: proposed"]
    if extra_caps:
        out.append(extra_caps)
    out.append("functionalities:")
    out += ["  - id: fn-guest", "    slug: guest", "    capability: cap-checkout",
            "    one_line: A shopper pays without an account.",
            "    doc: capabilities/checkout/guest/functionality.md", "    status: proposed"]
    if ices is not None:
        out.append("ices:")
        for e in ices:
            out.append(f"  - id: {e['id']}")
            for k in ("for", "for_kind", "doc"):
                if k in e:
                    out.append(f"    {k}: {e[k]}")
            for k, v in e.get("extra", {}).items():
                out.append(f"    {k}: {v}")
    return "\n".join(out) + "\n"


def run(ices, pages, extra_caps=""):
    """Lint only the ICE part of a spine: returns (errors, warnings)."""
    with tempfile.TemporaryDirectory() as root:
        for rel, text in pages.items():
            write(root, rel, text)
        sp = os.path.join(root, "_spine.yaml")
        with open(sp, "w", encoding="utf-8") as fh:
            fh.write(spine(ices, extra_caps))
        errors, warnings = [], []
        lg.check_ices(root, lg.load_spine(sp), errors, warnings, {})
        return errors, warnings


CAP_ICE = {"id": "ice-1", "for": "cap-checkout", "for_kind": "capability", "doc": "capabilities/checkout/ice.md"}
FN_ICE = {"id": "ice-2", "for": "fn-guest", "for_kind": "functionality", "doc": "capabilities/checkout/guest/ice.md"}
PAGES = {"capabilities/checkout/ice.md": GOOD_ICE, "capabilities/checkout/guest/ice.md": GOOD_ICE}


def has(msgs, *words):
    return any(all(w in m for w in words) for m in msgs)


def main():
    print("ICE node checks")

    e, w = run([CAP_ICE, FN_ICE], PAGES)
    check("a good model with one ICE per part passes", e == [] and w == [])

    e, w = run(None, {})
    check("a model with no ices list is not checked (v5 inline ICE)", e == [] and w == [])

    e, _ = run([CAP_ICE, FN_ICE], {"capabilities/checkout/ice.md": GOOD_ICE})
    check("a missing ice.md page is an error", has(e, "ice-2", "not found"))

    no_context = GOOD_ICE.replace("## Context\n\n- **Read:** the checkout capability page and the cart spine entry.\n\n", "")
    e, _ = run([CAP_ICE, FN_ICE], {**PAGES, "capabilities/checkout/guest/ice.md": no_context})
    check("a missing Context section is an error", has(e, "ice-2", "Context"))

    empty_exp = GOOD_ICE.split("## Expectation")[0] + "## Expectation\n\n"
    e, _ = run([CAP_ICE, FN_ICE], {**PAGES, "capabilities/checkout/ice.md": empty_exp})
    check("an empty Expectation section is an error (a part with nothing in it is missing)",
          has(e, "ice-1", "Expectation"))

    thin = "## Intent\n\n- **Goal:** pay.\n\n## Context\n\n- **Read:** cart.\n\n## Expectation\n\n- **Scenario:** pays.\n"
    e, _ = run([CAP_ICE, FN_ICE], {**PAGES, "capabilities/checkout/ice.md": thin})
    check("a thin part is not the linter's business (no error)", e == [])

    bad_for = dict(FN_ICE, **{"for": "fn-nothing"})
    e, _ = run([CAP_ICE, bad_for], PAGES)
    check("an ICE for a part that does not exist is an error", has(e, "ice-2", "fn-nothing"))

    bad_kind = dict(FN_ICE, **{"for_kind": "capability"})
    e, _ = run([CAP_ICE, bad_kind], PAGES)
    check("for_kind that does not match its part is an error", has(e, "ice-2", "for_kind"))

    with_bi = dict(CAP_ICE, extra={"intents": "[bi-756]"})
    e, _ = run([with_bi, FN_ICE], PAGES)
    check("an ICE entry that names a business intent is an error", has(e, "ice-1", "business intent"))

    page_bi = GOOD_ICE.replace("## Intent\n\n", "## Intent\n\n- **Business intent:** bi-756\n")
    e, _ = run([CAP_ICE, FN_ICE], {**PAGES, "capabilities/checkout/ice.md": page_bi})
    check("an ice.md that names a business intent is an error", has(e, "ice-1", "business intent"))

    twin = {"id": "ice-3", "for": "cap-checkout", "for_kind": "capability", "doc": "capabilities/checkout/ice.md"}
    e, _ = run([CAP_ICE, FN_ICE, twin], PAGES)
    check("two ICE for one part is an error", has(e, "cap-checkout", "two ICE") or has(e, "cap-checkout", "ice-1", "ice-3"))

    e, w = run([CAP_ICE], {"capabilities/checkout/ice.md": GOOD_ICE})
    check("a part with no ICE is a warning, not an error", e == [] and has(w, "fn-guest", "no ICE"))

    e, _ = run([CAP_ICE, FN_ICE], {**PAGES, "capabilities/stray/ice.md": GOOD_ICE})
    check("an ice.md no ices entry points at is an orphan error", has(e, "orphan", "capabilities/stray/ice.md"))

    no_doc = {k: v for k, v in CAP_ICE.items() if k != "doc"}
    e, _ = run([no_doc, FN_ICE], PAGES)
    check("an ICE entry with no doc pointer is an error", has(e, "ice-1", "doc"))

    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
