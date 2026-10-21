#!/usr/bin/env python3
"""test_lint_grounding.py — fixture tests for lint_grounding.py's spine orphan check (#634).

A lens doc belongs to its slice (`<domain>/slices/<slice>/lens/<type>.md`), not to a spine
node, so the spine never points at it. It must not be reported as an orphan while its slice
is in the spine, and must be reported when its slice is not. The lens contracts themselves are
checked against each lens template's gold example. Every play's copy of lint_grounding.py must
be identical to this one.

    python3 test_lint_grounding.py
"""
import glob
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lint_grounding as lg  # noqa: E402

REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
LENS_TEMPLATES = os.path.join(REPO, "core", "components", "memory", "standards", "schemas", "product-os",
                              "grounding", "lens")

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


def gold(lens):
    """The gold example from a lens template — the first ```markdown block."""
    with open(os.path.join(LENS_TEMPLATES, f"{lens}.md"), encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"```markdown\n(.*?)\n```", text, re.DOTALL)
    return m.group(1) + "\n"


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


SPINE = """domains: []
capabilities: []
functionalities: []
slices:
  - id: slice-checkout
    slug: checkout
"""


def orphans(root):
    errors, warnings = [], []
    lg.check_spine(root, os.path.join(root, "_spine.yaml"), errors, warnings, {})
    return [e for e in errors if "orphan" in e]


def test_lens_docs_and_the_orphan_check():
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        write(os.path.join(root, "_spine.yaml"), SPINE)
        write(os.path.join(root, "shop", "slices", "checkout", "lens", "quality.md"), gold("quality"))
        check("a lens doc under a slice the spine knows is not an orphan", orphans(root) == [])
        write(os.path.join(root, "shop", "slices", "slice-checkout", "lens", "ux.md"), gold("ux"))
        check("the slice may be named by its id as well as its slug", orphans(root) == [])
        write(os.path.join(root, "shop", "slices", "gone", "lens", "run.md"), gold("run"))
        found = orphans(root)
        check("a lens doc under a slice the spine does not know is an orphan",
              len(found) == 1 and "slices/gone/lens/run.md" in found[0] and "slice is not in the spine" in found[0])
        write(os.path.join(root, "shop", "lens", "agentic.md"), gold("agentic"))
        check("a lens doc outside any slice folder is an orphan",
              any("shop/lens/agentic.md" in e for e in orphans(root)))


def test_lens_contracts_match_their_templates():
    for path in sorted(glob.glob(os.path.join(LENS_TEMPLATES, "*.md"))):
        lens = os.path.splitext(os.path.basename(path))[0]
        text = gold(lens)
        title = lg.parse_sections(text)[0]
        kind = lg.infer_kind(title)
        errors, warnings = [], []
        if kind:
            lg.check_doc(path, text, kind, errors, warnings)
        check(f"the {lens} lens template's gold example is a valid {lens} lens doc",
              kind == f"lens-{lens}" and not errors)


LIGHT_DOMAIN = """# Theme: Commerce

## Intent
Let shoppers find what they want and pay for it without friction, so the store turns
visits into orders it can trust and fulfil.
"""


def spine_errors(root, spine_text):
    write(os.path.join(root, "_spine.yaml"), spine_text)
    errors, warnings = [], []
    lg.check_spine(root, os.path.join(root, "_spine.yaml"), errors, warnings, {})
    return errors


def test_domain_stages():
    domain_template = os.path.join(LENS_TEMPLATES, "..", "domain.md")
    with open(domain_template, encoding="utf-8") as fh:
        full = re.search(r"```markdown\n(.*?)\n```", fh.read(), re.DOTALL).group(1) + "\n"
    errors = []
    lg.check_doc("light.md", LIGHT_DOMAIN, "domain", errors, [], expected_stage="directional")
    check("a light domain page passes as directional", errors == [])
    errors = []
    lg.check_doc("light.md", LIGHT_DOMAIN, "domain", errors, [])
    check("a light domain page with no stage given is read as directional", errors == [])
    errors = []
    lg.check_doc("light.md", LIGHT_DOMAIN, "domain", errors, [], expected_stage="detailed")
    check("a light domain page fails when the spine says detailed",
          any("missing required section '## Business goal'" in e for e in errors))
    errors = []
    lg.check_doc("full.md", full, "domain", errors, [], expected_stage="detailed")
    check("the domain template's gold example passes as detailed", errors == [])
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        write(os.path.join(root, "commerce", "domain.md"), LIGHT_DOMAIN)
        entry = ("domains:\n  - id: dom-commerce\n    slug: commerce\n    status: proposed\n"
                 "    detail: {}\n    one_line: Selling to shoppers\n    doc: commerce/domain.md\n"
                 "capabilities: []\nfunctionalities: []\n")
        check("the spine's `detail: directional` on a domain is honoured",
              spine_errors(root, entry.format("directional")) == [])
        check("the spine's `detail: detailed` on a light domain page is an error",
              any("Business goal" in e for e in spine_errors(root, entry.format("detailed"))))


CAP = """# Capability: Checkout

## Directional intent
Checkout turns a full cart into a paid order, so a shopper who has decided to buy is never
lost at the last step; it owns paying and confirming, and leaves the cart to its neighbour.
"""
ICE = """
## Agent intent (ICE)
- Goal: A shopper with no account completes a purchase from start to finish.
- Limit: Nothing about how returns work may change for any shopper.
- Fails if: a guest shopper is asked to sign up before paying.
"""


def lint(text, **kw):
    errors = []
    lg.check_doc("cap.md", text, "capability", errors, [], **kw)
    return errors


def lint_warnings(text, **kw):
    warnings = []
    lg.check_doc("cap.md", text, "capability", [], warnings, **kw)
    return warnings


def test_agent_intent_section():
    for kind in ("capability", "functionality"):
        with open(os.path.join(LENS_TEMPLATES, "..", f"{kind}.md"), encoding="utf-8") as fh:
            golds = re.findall(r"```markdown\n(.*?)\n```", fh.read(), re.DOTALL)
        errors = []
        for g in golds:
            lg.check_doc(f"{kind}.md", g + "\n", kind, errors, [])
        check(f"every gold example in the {kind} template passes", golds and errors == [])
    check("a capability page with no agent intent passes when nothing requires it", lint(CAP) == [])
    check("a capability page with no agent intent is a warning, not an error, when its spine entry names an intent",
          lint(CAP, require_ice=True) == []
          and any("no '## Agent intent (ICE)' yet" in w for w in lint_warnings(CAP, require_ice=True)))
    legacy = CAP + "\nGoals:\n- A shopper with no account can buy, start to finish.\n"
    check("a page /intent wrote before ontology v4 (a loose Goals list) still passes",
          lint(legacy, expected_stage="directional", require_ice=True) == [])
    check("a light agent intent section passes, at the directional stage",
          lint(CAP + ICE, expected_stage="directional", require_ice=True) == [])
    moved = CAP.replace("## Directional intent", ICE.strip() + "\n\n## Directional intent")
    check("the agent intent section must be the last section",
          any("as the last section" in e for e in lint(moved)))
    check("an unknown label is an error",
          any("not a labelled item" in e for e in lint(CAP + ICE + "- Wish: something nice for every shopper here\n")))
    check("an agent intent with no Goal is an error",
          any("has no Goal" in e for e in lint(CAP + "\n## Agent intent (ICE)\n- Limit: returns stay exactly as they are today\n")))
    check("a telegraphic item is an error",
          any("telegraphic" in e for e in lint(CAP + "\n## Agent intent (ICE)\n- Goal: guest checkout\n")))
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "product-os")
        write(os.path.join(root, "commerce", "domain.md"), LIGHT_DOMAIN)
        write(os.path.join(root, "commerce", "checkout", "capability.md"), CAP)
        spine = ("domains:\n  - {id: dom-commerce, slug: commerce, detail: directional, one_line: Selling, "
                 "doc: commerce/domain.md}\ncapabilities:\n  - {id: cap-checkout, slug: checkout, domain: "
                 "dom-commerce, detail: directional, one_line: Paying, doc: commerce/checkout/capability.md%s}\n"
                 "functionalities: []\n")
        write(os.path.join(root, "_spine.yaml"), spine % ", intents: [guest-checkout]")
        errors, warnings = [], []
        lg.check_spine(root, os.path.join(root, "_spine.yaml"), errors, warnings, {})
        check("in the spine, a capability linked to an intent with no agent intent gets a warning",
              errors == [] and any("Agent intent" in w for w in warnings))
        check("in the spine, a capability with no intent link need not",
              spine_errors(root, spine % "") == [])


def test_sources_section():
    src = "\n## Sources\n- Board screen, the column header: \"In review\"\n"
    check("a capability page may end with its sources (#689)", lint(CAP + src, expected_stage="directional") == [])
    check("sources sit just before the agent intent", lint(CAP + src + ICE, expected_stage="directional") == [])
    check("sources after the agent intent are an error",
          any("as the last section" in e for e in lint(CAP + ICE + src, expected_stage="directional")))
    moved = CAP.replace("## Directional intent", src.strip() + "\n\n## Directional intent")
    check("sources in the middle of the page are an error",
          any("'## Sources' must appear once" in e for e in lint(moved, expected_stage="directional")))
    check("an empty sources section is an error",
          any("lists no source" in e for e in lint(CAP + "\n## Sources\nnothing\n", expected_stage="directional")))
    errors = []
    lg.check_doc("light.md", LIGHT_DOMAIN + "\n## Sources\n- https://example.org/commerce\n", "domain", errors, [],
                 expected_stage="directional")
    check("a domain page may end with its research sources", errors == [])


def test_every_copy_is_identical():
    mine = open(os.path.join(HERE, "lint_grounding.py"), "rb").read()
    copies = glob.glob(os.path.join(REPO, "core", "components", "plays", "*", "scripts", "lint_grounding.py"))
    different = [c for c in copies if open(c, "rb").read() != mine]
    check(f"every play's lint_grounding.py is identical to this one ({len(copies)} copies)",
          len(copies) >= 12 and not different)


def main():
    for test in (test_lens_docs_and_the_orphan_check, test_lens_contracts_match_their_templates,
                 test_domain_stages, test_agent_intent_section, test_sources_section, test_every_copy_is_identical):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
