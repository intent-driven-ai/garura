#!/usr/bin/env python3
"""test_vision_scripts.py — fixture tests for /discover-domains's scripts that keep the one product model
(#637, ADR 043 — /discover-domains writes domains only): read_intents.py, persist_seed.py, check_kept.py,
grounding_check.py, and the scoped guard over a real hand-over.

    python3 test_vision_scripts.py
"""
import contextlib
import io
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
import guidance_block as jg  # noqa: E402
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
**Stage:** proposed — saved inside a loop, 2026-10-09; the person confirms or drops it at the loop's final review
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
    """The model as /discover-intent leaves it: a light domain with no capability yet linked, one
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
    sh(tmp, "git", "commit", "-q", "-m", "after /discover-intent")
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
    "domains": [{"id": "support", "slug": "support", "status": "proposed", "detail": "detailed",
                 "one_line": "Helps shoppers who are stuck.", "doc": "support/domain.md",
                 "intents": ["grow-online-sales"]}],
    "updates": [{"kind": "domain", "id": "shop", "detail": "detailed", "intents": ["grow-online-sales"]}],
}
SUPPORT_DOMAIN = FULL_DOMAIN.replace("# Theme: Shop", "# Theme: Support")


def run_vision(tmp, base, m, work):
    """What /discover-domains's skill + persist do: raise the light domain, add a second one — domains only."""
    write(os.path.join(m, "shop", "domain.md"), FULL_DOMAIN)
    write(os.path.join(m, "support", "domain.md"), SUPPORT_DOMAIN)
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
        check("intents can come from /discover-intent's save record", json.load(open(out))["intents"][0]["id"] == "grow-online-sales")


def test_the_hand_over():
    with tempfile.TemporaryDirectory() as tmp:
        base, m = model_after_intent(tmp)
        work = os.path.join(tmp, "work")
        os.makedirs(work)
        rc, out = run_vision(tmp, base, m, work)
        check("the persist runs", rc == 0)
        sp = spine(m)
        doms = {d["id"]: d for d in sp["domains"]}
        cap = sp["capabilities"][0]
        check("the light domain is raised to detailed and gains the intent",
              doms["shop"]["detail"] == "detailed" and doms["shop"]["intents"] == ["grow-online-sales"])
        check("a second domain is added (a product may sit in several)", "support" in doms)
        check("/discover-domains leaves the capability alone — still waiting in the holding folder, no domain (ADR 043)",
              cap["domain"] == "" and cap["doc"] == "capabilities/guest-checkout/capability.md"
              and os.path.isfile(os.path.join(m, "capabilities", "guest-checkout", "capability.md")))
        page = open(os.path.join(m, "intents", "grow-online-sales.md")).read()
        listed = {(e["link"], e["kind"], e["mark"]) for e in it.read(page)}
        check("the intent page's Touches list names both domains and keeps the capability",
              listed == {("../capabilities/guest-checkout/capability.md", "capability", "adds"),
                         ("../support/domain.md", "domain", "adds"),
                         ("../shop/domain.md", "domain", "changes")})
        check("the rest of the intent page is untouched",
              page.split("**Touches:**")[0] == INTENT_PAGE.split("**Touches:**")[0]
              and page.endswith("**What was done:** (nothing yet)\n"))
        check("nothing needed a warning", out["warnings"] == [])
        errors, warnings = [], []
        lg.check_spine(m, os.path.join(m, "_spine.yaml"), errors, warnings, {})
        check("the grounding linter passes; the unplaced capability is only a warning",
              errors == [] and all("not ready until" in w for w in warnings))
        g = subprocess.run([sys.executable, os.path.join(HERE, "scoped_write_guard.py"), "--product-base",
                            base + "/", "--base-ref", "HEAD",
                            "--add-only", "product-os/*/domain.md", "--modify-only", "product-os/*/domain.md",
                            "--modify-only", "product-os/intents/*.md", "--allow", "product-os/_spine.yaml"],
                           cwd=tmp, capture_output=True, text=True)
        check("the scoped guard holds with domain pages, intent pages and the spine only",
              g.returncode == 0 and json.loads(g.stdout)["ok"])
        kept = os.path.join(work, "kept.json")
        check("the keep check holds: the raised domain kept its intent",
              ck.main(["--product-base", base + "/", "--out", kept]) == 0
              and json.load(open(kept))["checked"] == ["product/product-os/shop/domain.md"])
        sh(tmp, "git", "add", "-A")
        sh(tmp, "git", "commit", "-q", "-m", "after /discover-domains")
        rc, again = run_vision(tmp, base, m, work)
        sh(tmp, "git", "add", "-A")
        diff = subprocess.run(["git", "diff", "--cached", "--stat", "--", "product"], cwd=tmp, capture_output=True, text=True).stdout
        check("a re-run with nothing new changes nothing", rc == 0 and diff == "")


def test_named_updates_only():
    for label, update in (
            ("an update to a field outside the named ones", {"kind": "domain", "id": "shop", "status": "active"}),
            ("lowering a detail", {"kind": "domain", "id": "shop", "detail": "directional"}),
            ("placing a capability under a domain", {"kind": "capability", "id": "guest-checkout", "domain": "shop"}),
            ("any capability update", {"kind": "capability", "id": "guest-checkout", "one_line": "x y z"}),
            ("an update to a domain not in the spine", {"kind": "domain", "id": "nope", "one_line": "x y z"})):
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


def test_bad_inputs():
    for key, entry in (("capabilities", {"id": "x", "slug": "x", "one_line": "a b c", "doc": "shop/x/capability.md"}),
                       ("functionalities", {"id": "y", "slug": "y", "one_line": "a b c", "doc": "f/y/functionality.md"})):
        with tempfile.TemporaryDirectory() as tmp:
            base, m = model_after_intent(tmp)
            work = os.path.join(tmp, "work")
            os.makedirs(work)
            before = open(os.path.join(m, "_spine.yaml")).read()
            rc, _ = persist(base, work, {"domains": VISION_DELTA["domains"], key: [entry]})
            check(f"a delta that adds {key} refuses the run and writes nothing — /discover-domains writes domains only",
                  rc == 2 and open(os.path.join(m, "_spine.yaml")).read() == before)
    with tempfile.TemporaryDirectory() as tmp:
        base, m = model_after_intent(tmp)
        work = os.path.join(tmp, "work")
        os.makedirs(work)
        write(os.path.join(m, "_spine.yaml"), "domains: [\n")
        rc = subprocess.run([sys.executable, os.path.join(HERE, "persist_seed.py"), "--seed-manifest",
                             seed(work, {"updates": [{"kind": "domain", "id": "shop", "one_line": "a b c d"}]}),
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
        rc, out = persist(base, work, {"updates": [{"kind": "domain", "id": "shop", "intents": ["grow-online-sales"]}]})
        check("a missing intent page is a warning; the domain is still linked",
              rc == 0 and spine(m)["domains"][0]["intents"] == ["grow-online-sales"]
              and any("has no page" in w for w in out["warnings"]))
    with tempfile.TemporaryDirectory() as tmp:
        base, m = model_after_intent(tmp)
        work = os.path.join(tmp, "work")
        os.makedirs(work)
        ri.main(["--product-base", base + "/", "--intent", "grow-online-sales", "--out", os.path.join(work, "i.json")])
        rc, out = persist(base, work, {"domains": [{"id": "pay", "slug": "pay", "one_line": "x", "doc": "pay/domain.md"}]},
                          os.path.join(work, "i.json"))
        check("an input intent no domain names is a warning, and the run still completes",
              rc == 0 and any("named by no domain" in w for w in out["warnings"]))


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


def test_grounding_covers_every_domain():
    def run(tmp, man, extra=()):
        path = os.path.join(tmp, "seed-manifest.yaml")
        write(path, yaml.safe_dump({"seed": man}))
        with contextlib.redirect_stdout(io.StringIO()) as out:
            rc = gc.main(["--manifest", path, *extra])
        return rc, json.loads(out.getvalue())["errors"]
    with tempfile.TemporaryDirectory() as tmp:
        rc, errs = run(tmp, {"spine_delta": VISION_DELTA, "domains": [{"id": "support", "grounding": {"kb_shelf": "support"}}]})
        check("a domain the run raises but does not record is ungrounded", rc == 1 and any("'shop'" in e for e in errs))
        doms = [{"id": "support", "grounding": {"kb_shelf": "support"}},
                {"id": "shop", "grounding": {"kb_shelf": "ecommerce"}}]
        rc, _ = run(tmp, {"spine_delta": VISION_DELTA, "domains": doms})
        check("recording each domain with its shelf passes", rc == 0)
        rc, errs = run(tmp, {"spine_delta": dict(VISION_DELTA, capabilities=[{"id": "c"}]), "domains": doms})
        check("a delta that adds a capability fails — /discover-domains writes domains only (ADR 043)",
              rc == 1 and any("domains only" in e for e in errs))
        rc, errs = run(tmp, {"spine_delta": {}, "domains": []})
        check("a run that names no domain fails", rc == 1 and any("no domain" in e for e in errs))
    # #689: each domain page says where it comes from
    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, "product")
        m = os.path.join(base, "product-os")
        doms = [{"id": "shop", "doc": "product-os/shop/domain.md", "grounding": {"kb_shelf": "ecommerce"}},
                {"id": "support", "doc": "product-os/support/domain.md", "grounding": {"kb_shelf": "support"}}]
        man = {"spine_delta": VISION_DELTA, "domains": doms}
        write(os.path.join(m, "shop", "domain.md"), "# Theme: Shop\n\n## Intent\nSell.\n")
        write(os.path.join(m, "support", "domain.md"),
              "# Theme: Support\n\n## Intent\nHelp.\n\n## Sources\n- https://example.org/customer-support\n")
        rc, errs = run(tmp, man, ["--product-base", base])
        check("a domain page with no sources fails (#689)", rc == 1 and any("shop/domain.md" in e for e in errs))
        check("each domain page is checked on its own", not any("support/domain.md" in e for e in errs))
        write(os.path.join(m, "shop", "domain.md"), "# Theme: Shop\n\n## Intent\nSell.\n\n## Sources\n- the Shop screens\n")
        rc, errs = run(tmp, man, ["--product-base", base])
        check("a domain whose sources name no shelf and no research link fails — it was made up",
              any("name no shelf and no research link" in e for e in errs))
        write(os.path.join(m, "shop", "domain.md"),
              "# Theme: Shop\n\n## Intent\nSell.\n\n## Sources\n- https://example.org/e-commerce\n")
        rc, _ = run(tmp, man, ["--product-base", base])
        check("researched domain pages pass", rc == 0)
    # C12: every main section of the prototype sits in a domain, by that domain's own research
    with tempfile.TemporaryDirectory() as tmp:
        journeys = os.path.join(tmp, "journeys.yaml")
        write(journeys, yaml.safe_dump({"main_sections": ["Catalogue", "Orders", "Tickets"]}))
        doms = [{"id": "shop", "grounding": {"kb_shelf": "ecommerce"}},
                {"id": "support", "grounding": {"kb_shelf": "support"}},
                {"id": "chat", "grounding": {"kb_shelf": "messaging"}}]
        delta = {"domains": [{"id": d["id"]} for d in doms]}
        area = lambda s, d: {"section": s, "domain": d, "evidence": f"{d} covers {s.lower()}",
                             "source": f"https://example.org/{d}"}
        areas = [area("Catalogue", "shop"), area("Orders", "shop")]
        rc, errs = run(tmp, {"spine_delta": delta, "domains": doms, "areas": areas}, ["--journeys", journeys])
        check("a main section in no domain fails — find the field that does its work",
              rc == 1 and any("'Tickets' sits in no domain" in e for e in errs))
        check("a domain that holds no main section fails — one shared feature is not a field",
              any("'chat' holds no main section" in e for e in errs))
        rc, errs = run(tmp, {"spine_delta": delta, "domains": doms[:2],
                             "areas": areas + [dict(area("Tickets", "support"), evidence="", source="the screens")]},
                       ["--journeys", journeys])
        check("an area with no evidence or no researched source fails",
              any("no `evidence`" in e for e in errs) and any("no research link" in e for e in errs))
        rc, errs = run(tmp, {"spine_delta": {"domains": delta["domains"][:2]}, "domains": doms[:2],
                             "areas": areas + [area("Tickets", "support")]}, ["--journeys", journeys])
        check("every main section in a researched domain, and every domain holding one, passes",
              rc == 0)


TEMPLATE = """# Capability template

## Heading contract
```
## Directional intent
```

## Per-section guidance (detailed stage)

- **Boundary** — what it owns and why.
```
## Not a heading: inside a fence
```

## Gold example — DIRECTIONAL stage (/discover-domains)

## Directional intent
The answer the judge must never see.
"""


def test_judge_gets_only_the_guidance():
    with tempfile.TemporaryDirectory() as tmp:
        tpl, out = os.path.join(tmp, "capability.md"), os.path.join(tmp, "judge", "guidance.md")
        write(tpl, TEMPLATE)
        rc = jg.main(["--template", tpl, "--out", out])
        text = open(out).read() if os.path.exists(out) else ""
        check("the judge's guidance is the per-section guidance block",
              rc == 0 and text.startswith("## Per-section guidance") and "what it owns and why" in text)
        check("a heading inside a fence stays in the block", "## Not a heading: inside a fence" in text)
        check("the judge is never handed the gold example",
              "Gold example" not in text and "must never see" not in text)
        write(tpl, "# Template\n\n## Gold example\nthe answer\n")
        out2 = os.path.join(tmp, "none.md")
        check("a template with no guidance block writes nothing",
              jg.main(["--template", tpl, "--out", out2]) == 2 and not os.path.exists(out2))


def main():
    for test in (test_read_intents, test_the_hand_over, test_named_updates_only, test_bad_inputs, test_never_blocks,
                 test_keep_check, test_grounding_covers_every_domain, test_judge_gets_only_the_guidance):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
