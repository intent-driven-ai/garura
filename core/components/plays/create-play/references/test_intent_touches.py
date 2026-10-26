#!/usr/bin/env python3
"""test_intent_touches.py — tests for the Touches list on a business intent page.

Every play's and skill's stamped copy of intent_touches.py must be identical to this canonical one.

    python3 test_intent_touches.py
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import intent_touches as it  # noqa: E402

REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
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


PAGE = """# Shoppers can check out without making an account

**Outcome:** A shopper with no account can buy, start to finish.
**Stage:** proposed

**What was done:** (nothing yet)
"""

OLD_PAGE = """# Guest checkout

**Sources:**
- [prototype, read 2026-10-08](../_evidence/intent/x/source.md)
**ICE built from it (proposed capabilities, no domain yet):**
- [Checkout](../capabilities/checkout/capability.md)

**What was done:** (nothing yet)
"""

CHECKOUT = it.entry("Checkout", "../commerce/checkout/capability.md", "capability", "adds")
COMMERCE = it.entry("Commerce", "../commerce/domain.md", "domain", "changes")


def test_write_and_read():
    text = it.upsert(PAGE, [CHECKOUT])
    check("a page with no list gets one, just before What was done",
          "**Stage:** proposed\n\n**Touches:**\n- [Checkout](../commerce/checkout/capability.md) (capability) — adds\n\n**What was done:**" in text)
    check("the list reads back", it.read(text) == [CHECKOUT])
    again = it.upsert(text, [CHECKOUT, COMMERCE])
    check("upsert adds only what is not listed yet", it.read(again) == [CHECKOUT, COMMERCE])
    check("upsert with nothing new changes nothing", it.upsert(again, [COMMERCE]) == again)
    changed = it.upsert(again, [it.entry("Checkout", CHECKOUT["link"], "capability", "changes")])
    check("an entry already listed keeps its mark", it.read(changed)[0]["mark"] == "adds")
    check("the rest of the page is untouched",
          again.replace("\n".join(it.render([CHECKOUT, COMMERCE])) + "\n\n", "") == PAGE)


def test_a_line_a_person_wrote_stays():
    free = "- fn-727 and fn-728 (features of cap-718) — moved under cap-718's folder"
    page = PAGE.replace("**What was done:**", "**Touches:**\n- [Checkout](../commerce/checkout/capability.md) "
                        f"(capability) — adds\n{free}\n\n**What was done:**")
    check("upsert with nothing new returns the page unchanged, a free-form line and all",
          it.upsert(page, [CHECKOUT]) == page)
    text = it.upsert(page, [COMMERCE])
    check("a line in a form the module cannot read stays, in its place; a new entry goes after it",
          f"capability) — adds\n{free}\n- [Commerce](../commerce/domain.md) (domain) — changes\n" in text)
    check("only the new line is added", text.replace("- [Commerce](../commerce/domain.md) (domain) — changes\n", "") == page)


def test_none_yet():
    empty = it.upsert(PAGE, [])
    check("a page that touches nothing yet says so", "**Touches:** none yet" in empty and it.read(empty) == [])
    filled = it.upsert(empty, [CHECKOUT])
    check("'none yet' gives way to the first entry",
          "none yet" not in filled and it.read(filled) == [CHECKOUT] and filled.count("**Touches:**") == 1)


def test_the_old_list_is_converted():
    text = it.upsert(OLD_PAGE, [COMMERCE])
    check("the pre-v4 list becomes a Touches list, each capability `adds`",
          it.read(text) == [it.entry("Checkout", "../capabilities/checkout/capability.md", "capability", "adds"), COMMERCE]
          and "ICE built from it" not in text)
    check("the Sources list is left alone", "- [prototype, read 2026-10-08](../_evidence/intent/x/source.md)" in text)


def test_relink():
    text, n = it.relink(OLD_PAGE, "../capabilities/checkout/capability.md", "../commerce/checkout/capability.md")
    check("relink points the link at the new page", n == 1 and "](../commerce/checkout/capability.md)" in text)
    check("relink changes nothing else", text.replace("commerce/checkout", "capabilities/checkout") == OLD_PAGE)
    _, n = it.relink(OLD_PAGE, "../capabilities/check", "x")
    check("relink matches whole link targets only", n == 0)
    check("the link from an intent page is relative to it",
          it.rel("/m/product-os/intents/a.md", "/m/product-os/commerce/checkout/capability.md")
          == "../commerce/checkout/capability.md")


def test_bad_entries():
    for args, name in ((("X", "a.md", "epic", "adds"), "an unknown kind"),
                       (("X", "a.md", "domain", "keeps"), "an unknown mark"),
                       (("", "a.md", "domain", "adds"), "no title")):
        try:
            it.entry(*args)
            check(f"{name} is refused", False)
        except it.Bad:
            check(f"{name} is refused", True)


def test_every_copy_is_identical():
    mine = open(os.path.join(HERE, "intent_touches.py"), "rb").read()
    copies = [c for kind in ("plays", "skills")
              for c in glob.glob(os.path.join(REPO, "core", "components", kind, "*", "scripts", "intent_touches.py"))]
    different = [c for c in copies if open(c, "rb").read() != mine]
    check(f"every play's and skill's intent_touches.py is identical to the canonical one ({len(copies)} copies)",
          len(copies) >= 2 and not different)


def main():
    for test in (test_write_and_read, test_a_line_a_person_wrote_stays, test_none_yet, test_the_old_list_is_converted, test_relink, test_bad_entries,
                 test_every_copy_is_identical):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
