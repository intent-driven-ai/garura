#!/usr/bin/env python3
"""test_vision_scripts.py — fixture tests for /vision's scripts that keep the one product model
(#637): read_intents.py, persist_seed.py, check_kept.py, grounding_check.py, and the scoped
guard over a real /intent → /vision hand-over.

    python3 test_vision_scripts.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_kept as ck  # noqa: E402
import grounding_check as gc  # noqa: E402
import intent_touches as it  # noqa: E402
import lint_grounding as lg  # noqa: E402
import persist_seed as ps  # noqa: E402
import read_intents as ri  # noqa: E402

PASSED = 0
FAILED = 0

CAP_DOC = """# Capability: Buy without an account

## Directional intent
Guest checkout is about letting a shopper finish a purchase with no account. It broadly owns
the path from cart to paid order for a shopper who never signs up, and it matters because four
in ten shoppers leave at the sign-up step.

## Agent intent (ICE)
- Goal: A shopper with no account can buy, start to finish.
"""
LIGHT_DOMAIN = """# Theme: Shop

## Intent
The shop is where returning customers keep their carts and come back to finish what they
started buying, so no visit is wasted.
"""
FULL_DOMAIN = LIGHT_DOMAIN.replace("# Theme: Shop", "# Theme: Shop") + """
## Business goal
A store owner can answer how many shoppers come back and buy, from one place, and trust it.

## Guiding rules
- A cart is never lost without the shopper choosing to empty it, because a lost cart is a lost sale.

## Capabilities
- Saved carts — keeps a shopper's cart between visits so they can finish buying later.

## Scope (In / Out)
- In: carts, returning shoppers, and finishing a purchase that was started on an earlier visit.
- Out: payments and refunds, which the payments area owns instead of the shop.
"""
INTENT_PAGE = """# Grow online sales without adding sales staff

**Outcome:** More shoppers finish buying online.
**Stage:** proposed — saved inside a drive, 2026-10-09; the person confirms or drops it at the drive's final review
**Sources:**
- [prototype, read 2026-10-08](../../_evidence/intent/x/source.md)

**Touches:**
- [Buy without an account](../capabilities/guest-checkout/capability.md) (capability) — adds

**What was done:** (nothing yet)
"""


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


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def sh(cwd, *args):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def model_after_intent(tmp):
    """The model as /intent leaves it: a light domain with no capability yet linked, one
    capability in the holding folder, one proposed intent. Committed, like a fresh branch."""
    sh(tmp, "git", "init", "-q")
    sh(tmp, "git", "config", "user.email", "t@example.com")
    sh(tmp, "git", "config", "user.name", "t")
    base = os.path.join(tmp, "product")
    m = os.path.join(base, "product-os")
    write(os.path.join(m, "shop", "domain.md"), LIGHT_DOMAIN)
    write(os.path.join(m, "capabilities", "guest-checkout", "capability.md"), CAP_DOC)
    write(os.path.join(m, "intents", "grow-online-sales.md"), INTENT_PAGE)
    write(os.path.join(m, "_spine.yaml"), yaml.safe_dump({
        "domains": [{"id": "shop", "slug": "shop", "status": "proposed", "detail": "directional",
                     "one_line": "Where returning shoppers buy.", "doc": "shop/domain.md", "intents": []}],
        "capabilities": [{"id": "guest-checkout", "slug": "guest-checkout", "domain": "",
                          "intents": ["grow-online-sales"], "status": "proposed", "detail": "directional",
                          "one_line": "Lets a shopper buy without an account.",
                          "doc": "capabilities/guest-checkout/capability.md"}],
        "functionalities": []}, sort_keys=False))
    sh(tmp, "git", "add", "-A")
    sh(tmp, "git", "commit", "-q", "-m", "after /intent")
    return base, m


def spine(m):
    with open(os.path.join(m, "_spine.yaml")) as fh:
        return yaml.safe_load(fh)


def seed(work, delta, caps=None, same_as=None):
    path = os.path.join(work, "seed-manifest.yaml")
    write(path, yaml.safe_dump({"seed": {"spine_delta": delta, "capabilities": caps or [],
                                         "same_as": same_as or []}}))
    return path


def persist(base, work, delta, intents=None):
    argv = ["--seed-manifest", seed(work, delta), "--product-base", base + "/",
            "--out-manifest", os.path.join(work, "persist.json")]
    if intents:
        argv += ["--intents", intents]
    rc = ps.main(argv)
    out = json.load(open(os.path.join(work, "persist.json"))) if rc == 0 else None
    return rc, out


VISION_DELTA = {
    "capabilities": [{"id": "saved-carts", "slug": "saved-carts", "domain": "shop",
                      "intents": ["grow-online-sales"], "status": "proposed", "detail": "directional",
                      "one_line": "Keeps a cart between visits.", "doc": "shop/saved-carts/capability.md"}],
    "updates": [{"kind": "domain", "id": "shop", "detail": "detailed"},
                {"kind": "capability", "id": "guest-checkout", "domain": "shop"}],
}


def run_vision(tmp, base, m, work):
    """What /vision's skill + persist do: raise the light domain, add a capability, place one."""
    write(os.path.join(m, "shop", "domain.md"), FULL_DOMAIN)
    write(os.path.join(m, "shop", "saved-carts", "capability.md"), CAP_DOC.replace(
        "Buy without an account", "Come back to a left cart").replace(
        "- Goal: A shopper with no account can buy, start to finish.",
        "- Goal: A shopper who leaves finds the same cart waiting when they return."))
    ri.main(["--product-base", base + "/", "--intent", "grow-online-sales", "--out", os.path.join(work, "intents.json")])
    return persist(base, work, VISION_DELTA, os.path.join(work, "intents.json"))


def test_read_intents():
    with tempfile.TemporaryDirectory() as tmp:
        base, m = model_after_intent(tmp)
        out = os.path.join(tmp, "intents.json")
        rc = ri.main(["--product-base", base + "/", "--intent", "grow-online-sales", "--intent", "gone", "--out", out])
        rec = json.load(open(out))
        first = rec["intents"][0]
        check("a proposed intent is read and accepted", rc == 0 and first["stage"] == "proposed" and first["accepted"])
        check("its capability in the holding folder is found",
              rec["capabilities"] and rec["capabilities"][0]["in_holding_folder"])
        check("a missing intent page is a warning, not a stop",
              not rec["intents"][1]["accepted"] and any("gone" in w for w in rec["warnings"]))
        man = os.path.join(tmp, "intent-manifest.json")
        write(man, json.dumps({"intents": [{"id": "grow-online-sales"}]}))
        ri.main(["--product-base", base + "/", "--intent-manifest", man, "--out", out])
        check("intents can come from /intent's save record", json.load(open(out))["intents"][0]["id"] == "grow-online-sales")


def test_the_hand_over():
    with tempfile.TemporaryDirectory() as tmp:
        base, m = model_after_intent(tmp)
        work = os.path.join(tmp, "work")
        os.makedirs(work)
        rc, out = run_vision(tmp, base, m, work)
        check("the persist runs", rc == 0)
        sp = spine(m)
        caps = {c["id"]: c for c in sp["capabilities"]}
        dom = sp["domains"][0]
        check("the holding-folder capability is placed under its domain",
              caps["guest-checkout"]["domain"] == "shop"
              and caps["guest-checkout"]["doc"] == "shop/guest-checkout/capability.md")
        check("its page moved unchanged, and the holding folder is gone",
              out["placed"] == [{"id": "guest-checkout", "from": "capabilities/guest-checkout/capability.md",
                                 "to": "shop/guest-checkout/capability.md", "unchanged": True}]
              and not os.path.exists(os.path.join(m, "capabilities")))
        check("the light domain is raised to detailed and gains the intent",
              dom["detail"] == "detailed" and dom["intents"] == ["grow-online-sales"])
        page = open(os.path.join(m, "intents", "grow-online-sales.md")).read()
        listed = {(e["link"], e["kind"], e["mark"]) for e in it.read(page)}
        check("the intent page's Touches list is relinked and complete",
              listed == {("../shop/guest-checkout/capability.md", "capability", "adds"),
                         ("../shop/saved-carts/capability.md", "capability", "adds"),
                         ("../shop/domain.md", "domain", "changes")})
        check("the rest of the intent page is untouched",
              page.split("**Touches:**")[0] == INTENT_PAGE.split("**Touches:**")[0]
              and page.endswith("**What was done:** (nothing yet)\n"))
        check("nothing needed a warning", out["warnings"] == [])
        errors, warnings = [], []
        lg.check_spine(m, os.path.join(m, "_spine.yaml"), errors, warnings, {})
        check("the grounding linter passes with no warning", errors == [] and warnings == [])
        g = subprocess.run([sys.executable, os.path.join(HERE, "scoped_write_guard.py"), "--product-base",
                            base + "/", "--base-ref", "HEAD",
                            "--add-only", "product-os/*/domain.md", "--modify-only", "product-os/*/domain.md",
                            "--add-only", "product-os/*/*/capability.md", "--modify-only", "product-os/*/*/capability.md",
                            "--remove-only", "product-os/capabilities/*/capability.md",
                            "--modify-only", "product-os/intents/*.md", "--allow", "product-os/_spine.yaml"],
                           cwd=tmp, capture_output=True, text=True)
        check("the scoped guard holds over the whole hand-over", g.returncode == 0 and json.loads(g.stdout)["ok"])
        kept = os.path.join(work, "kept.json")
        check("the keep check holds: the raised domain kept its intent",
              ck.main(["--product-base", base + "/", "--out", kept]) == 0
              and json.load(open(kept))["checked"] == [
                  "product/product-os/shop/domain.md",
                  "product/product-os/capabilities/guest-checkout/capability.md -> "
                  "product/product-os/shop/guest-checkout/capability.md"])
        sh(tmp, "git", "add", "-A")
        sh(tmp, "git", "commit", "-q", "-m", "after /vision")
        rc, again = run_vision(tmp, base, m, work)
        sh(tmp, "git", "add", "-A")
        diff = subprocess.run(["git", "diff", "--cached", "--stat", "--", "product"], cwd=tmp, capture_output=True, text=True).stdout
        check("a re-run with nothing new changes nothing", rc == 0 and diff == "" and again["placed"] == [])


def test_named_updates_only():
    for label, update, why in (
            ("an update to a field outside the named ones", {"kind": "capability", "id": "guest-checkout", "status": "active"}, "not a named update"),
            ("lowering a detail", {"kind": "domain", "id": "shop", "detail": "directional"}, None),
            ("detailing a capability", {"kind": "capability", "id": "guest-checkout", "detail": "detailed"}, None),
            ("an update to an entry not in the spine", {"kind": "capability", "id": "nope", "one_line": "x y z"}, None)):
        with tempfile.TemporaryDirectory() as tmp:
            base, m = model_after_intent(tmp)
            work = os.path.join(tmp, "work")
            os.makedirs(work)
            if label == "lowering a detail":
                sp = spine(m)
                sp["domains"][0]["detail"] = "detailed"
                write(os.path.join(m, "_spine.yaml"), yaml.safe_dump(sp))
            before = open(os.path.join(m, "_spine.yaml")).read()
            rc, _ = persist(base, work, {"updates": [update]})
            check(f"{label} refuses the run and writes nothing",
                  rc == 2 and open(os.path.join(m, "_spine.yaml")).read() == before)
    with tempfile.TemporaryDirectory() as tmp:
        base, m = model_after_intent(tmp)
        work = os.path.join(tmp, "work")
        os.makedirs(work)
        persist(base, work, {"updates": [{"kind": "capability", "id": "guest-checkout", "domain": "shop"}]})
        rc, out = persist(base, work, {"updates": [{"kind": "capability", "id": "guest-checkout", "domain": "payments"}]})
        check("moving a capability between domains is not applied, only warned",
              rc == 0 and spine(m)["capabilities"][0]["domain"] == "shop"
              and any("alignment work" in w for w in out["warnings"]))


def test_bad_inputs():
    with tempfile.TemporaryDirectory() as tmp:
        base, m = model_after_intent(tmp)
        work = os.path.join(tmp, "work")
        os.makedirs(work)
        sp = spine(m)
        sp["capabilities"].append(dict(sp["capabilities"][0], id="guest-checkout-2",
                                       doc="capabilities/guest-checkout-2/capability.md"))
        sp["capabilities"][1]["slug"] = "guest-checkout"
        write(os.path.join(m, "_spine.yaml"), yaml.safe_dump(sp))
        write(os.path.join(m, "capabilities", "guest-checkout-2", "capability.md"), CAP_DOC)
        before = open(os.path.join(m, "_spine.yaml")).read()
        rc, _ = persist(base, work, {"updates": [{"kind": "capability", "id": "guest-checkout", "domain": "shop"},
                                                 {"kind": "capability", "id": "guest-checkout-2", "domain": "shop"}]})
        check("two placements onto one page refuse the run and write nothing",
              rc == 2 and open(os.path.join(m, "_spine.yaml")).read() == before
              and os.path.isfile(os.path.join(m, "capabilities", "guest-checkout", "capability.md")))
        write(os.path.join(m, "_spine.yaml"), "domains: [\n")
        rc = subprocess.run([sys.executable, os.path.join(HERE, "persist_seed.py"), "--seed-manifest",
                             seed(work, {"updates": [{"kind": "capability", "id": "guest-checkout", "one_line": "a b c d"}]}),
                             "--product-base", base + "/", "--out-manifest", os.path.join(work, "p.json")],
                            capture_output=True, text=True)
        check("a broken spine exits 2 with nothing written, not a crash",
              rc.returncode == 2 and "cannot read" in rc.stderr and "Traceback" not in rc.stderr)
        write(os.path.join(m, "_spine.yaml"), "- a list\n")
        rc = ri.main(["--product-base", base + "/", "--intent", "grow-online-sales", "--out", os.path.join(work, "i.json")])
        check("read_intents reads a spine that is not a mapping as empty, with a warning",
              rc == 0 and any("not a mapping" in w for w in json.load(open(os.path.join(work, "i.json")))["warnings"]))


def test_never_blocks():
    with tempfile.TemporaryDirectory() as tmp:
        base, m = model_after_intent(tmp)
        os.remove(os.path.join(m, "intents", "grow-online-sales.md"))
        work = os.path.join(tmp, "work")
        os.makedirs(work)
        rc, out = persist(base, work, {"updates": [{"kind": "capability", "id": "guest-checkout", "domain": "shop"}]})
        check("a missing intent page is a warning; the capability is still placed",
              rc == 0 and out["placed"] and any("has no page" in w for w in out["warnings"]))
    with tempfile.TemporaryDirectory() as tmp:
        base, m = model_after_intent(tmp)
        work = os.path.join(tmp, "work")
        os.makedirs(work)
        ri.main(["--product-base", base + "/", "--intent", "grow-online-sales", "--out", os.path.join(work, "i.json")])
        rc, out = persist(base, work, {"domains": [{"id": "pay", "slug": "pay", "one_line": "x", "doc": "pay/domain.md"}]},
                          os.path.join(work, "i.json"))
        check("a capability left unplaced is named in a warning, and the run still completes",
              rc == 0 and any("still has no domain" in w for w in out["warnings"]))


def test_keep_check():
    with tempfile.TemporaryDirectory() as tmp:
        base, m = model_after_intent(tmp)
        out = os.path.join(tmp, "kept.json")
        write(os.path.join(m, "shop", "domain.md"), "# Theme: Shop\n\n## Business goal\nSomething else.\n")
        check("a page that lost a section fails the keep check",
              ck.main(["--product-base", base + "/", "--out", out]) == 1
              and json.load(open(out))["lost"][0]["section"] == "Intent")
        shutil.copy(os.path.join(m, "capabilities", "guest-checkout", "capability.md"), os.path.join(tmp, "c"))
        write(os.path.join(m, "shop", "domain.md"), LIGHT_DOMAIN)
        write(os.path.join(m, "capabilities", "guest-checkout", "capability.md"),
              CAP_DOC.replace("- Goal: A shopper with no account can buy, start to finish.",
                              "- Goal: Something different that replaces the old goal entirely."))
        check("an agent-intent line that was dropped fails the keep check",
              ck.main(["--product-base", base + "/", "--out", out]) == 1
              and "dropped" in json.load(open(out))["lost"][0]["what"])
        write(os.path.join(m, "capabilities", "guest-checkout", "capability.md"),
              CAP_DOC + "- Limit: Nothing about how returns work changes for anyone.\n")
        check("adding to the agent intent passes", ck.main(["--product-base", base + "/", "--out", out]) == 0)
    with tempfile.TemporaryDirectory() as tmp:
        base, m = model_after_intent(tmp)
        out = os.path.join(tmp, "kept.json")
        os.makedirs(os.path.join(m, "shop", "guest-checkout"))
        os.rename(os.path.join(m, "capabilities", "guest-checkout", "capability.md"),
                  os.path.join(m, "shop", "guest-checkout", "capability.md"))
        write(os.path.join(m, "shop", "guest-checkout", "capability.md"), "# Capability: Replaced.\n")
        check("a page cut down while it was moved out of the holding folder fails the keep check",
              ck.main(["--product-base", base + "/", "--out", out]) == 1
              and any(x["section"] == "Directional intent" for x in json.load(open(out))["lost"]))
        os.remove(os.path.join(m, "shop", "guest-checkout", "capability.md"))
        check("a holding page removed and placed nowhere fails the keep check",
              ck.main(["--product-base", base + "/", "--out", out]) == 1
              and "placed nowhere" in json.load(open(out))["lost"][0]["what"])


def test_grounding_covers_every_capability():
    with tempfile.TemporaryDirectory() as tmp:
        path = seed(tmp, VISION_DELTA, caps=[{"id": "saved-carts", "grounding": {"kb_shelf": "ecommerce → Carts"}}])
        rc = gc.main(["--manifest", path])
        check("a capability the run places but does not record is ungrounded", rc == 1)
        path = seed(tmp, VISION_DELTA, caps=[{"id": "saved-carts", "grounding": {"kb_shelf": "ecommerce → Carts"}},
                                             {"id": "guest-checkout", "grounding": {"kb_shelf": "ecommerce → Checkout"}}])
        check("recording it with its shelf passes", gc.main(["--manifest", path]) == 0)


def main():
    for test in (test_read_intents, test_the_hand_over, test_named_updates_only, test_bad_inputs, test_never_blocks,
                 test_keep_check, test_grounding_covers_every_capability):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
