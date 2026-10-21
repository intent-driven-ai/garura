#!/usr/bin/env python3
"""
test_intent_scripts.py — fixture tests for /intent's three scripts (#612).

capture_source.py  — a statement is kept byte for byte; a document is copied; an HTML file is
                     copied and rendered to a screenshot; a missing source fails (F1).
                     A clicked tab keeps its picture and its text. Every view of a prototype
                     is found and kept without naming it, two clicks deep (#613, C1).
walk_prototype.py / check_journeys.py — a journey step is taken, replayed and kept; the
                     record is complete and covers every view (#613, C15).
check_intent.py    — per intent: required properties, provenance, copying the source,
                     code-like text, bare labels; for the draft: ids, sources summarised, the
                     coverage map to intents, one kind only (no ICE, domains or capabilities —
                     ADR 043), one line per intent for what the person must answer, examples.
persist_intent.py  — saves only the intents the person confirmed, refuses unless every intent
                     was decided by the person and when the draft carries another kind, never
                     overwrites, links intents and sources both ways, writes nothing else.

    python3 test_intent_scripts.py
"""

import json
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import capture_source as cs  # noqa: E402
import check_intent as ci  # noqa: E402
import persist_intent as pi  # noqa: E402
import check_journeys as cj  # noqa: E402
import walk_prototype as wp  # noqa: E402

PASSED = 0
FAILED = 0
SKIPPED = []


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


def skip(names, reason):
    """Record checks that could not run, so the summary says so instead of hiding them."""
    for name in names:
        SKIPPED.append(name)
        print(f"  [SKIP] {name} — {reason}")


def read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


INTENT_A = {
    "id": "grow-online-sales", "title": "Grow online sales without adding sales staff",
    "outcome": "More shoppers finish buying online, so sales grow while the team stays the same size.",
    "why": "Four in ten shoppers leave before they pay.",
    "asked_by": "Priya, Head of Growth",
    "proof": "Online sales rise by a fifth within two quarters, with no new hires.",
    "must_not": "Change how returns work for anyone.",
    "provenance": {"title": "person", "outcome": "person", "why": "person", "asked_by": "person",
                   "proof": "person", "must_not": "person"}}
INTENT_B = {
    "id": "know-the-customer", "title": "Know who our returning customers are",
    "outcome": "The team knows which customers come back and what brings them back.",
    "why": "Returning customers spend twice as much as new ones.",
    "asked_by": "Priya, Head of Growth",
    "proof": "Every campaign names the returning customers it is aimed at.",
    "provenance": {"title": "person", "outcome": "person", "why": "person", "asked_by": "person",
                   "proof": "person"}}
SNAP = "/evidence/source"
EXAMPLES = ["Sales are flat.", "Shoppers leave at sign-up.", "Costs are rising."]
GOOD = {"intents": [INTENT_A, INTENT_B],
        "sources": [{"snapshot_dir": SNAP, "shows": "A checkout with a guest button, and a saved cart page."}],
        "coverage": [{"part": "the guest checkout page", "intent": "grow-online-sales"},
                     {"part": "the saved cart page", "intent": "grow-online-sales"}],
        "questions": [{"intent": "grow-online-sales", "ask": "Why does this matter?",
                       "examples": EXAMPLES, "answer": "Four in ten shoppers leave before they pay."}]}


def fresh():
    return yaml.safe_load(yaml.safe_dump(GOOD))


def test_capture():
    with tempfile.TemporaryDirectory() as tmp:
        st = os.path.join(tmp, "s.txt")
        with open(st, "wb") as fh:
            fh.write("Let shoppers buy without an account.\n  ✓ exact".encode())
        out, man = os.path.join(tmp, "src1"), os.path.join(tmp, "m1.json")
        check("a statement is captured", cs.main(["--statement", st, "--out-dir", out,
                                                   "--given-by", "Kapil", "--manifest", man]) == 0)
        with open(os.path.join(out, "statement.txt"), "rb") as fh, open(st, "rb") as orig:
            check("the statement is kept byte for byte", fh.read() == orig.read())
        check("its kind is statement", read_json(man)["kind"] == "statement")

        doc = os.path.join(tmp, "brief.md")
        with open(doc, "w") as fh:
            fh.write("# Brief\nGuest checkout.\n")
        out, man = os.path.join(tmp, "src2"), os.path.join(tmp, "m2.json")
        check("a document is captured", cs.main(["--source", doc, "--out-dir", out,
                                                  "--given-by", "Kapil", "--manifest", man]) == 0)
        check("its kind is document and it was copied",
              read_json(man)["kind"] == "document" and os.path.isfile(os.path.join(out, "brief.md")))

        page = os.path.join(tmp, "proto.html")
        with open(page, "w") as fh:
            fh.write("<html><body><h1>Checkout</h1><button>Continue as guest</button></body></html>")
        out, man = os.path.join(tmp, "src3"), os.path.join(tmp, "m3.json")
        rc = cs.main(["--source", page, "--out-dir", out, "--given-by", "Kapil", "--manifest", man])
        m = read_json(man)
        if "Playwright" in (m.get("problem") or "") and "installed" in m["problem"]:
            check("an HTML prototype without Playwright fails plainly (F1)", rc == 2)
            skip(["an HTML prototype is copied and rendered", "the screenshot is a real image",
                  "a named tab is clicked and captured", "the clicked view's text is kept beside its picture",
                  "every view is found and kept without naming it", "a view two clicks deep is kept",
                  "an answer button is never clicked while exploring", "a link out of the prototype is not followed",
                  "the manifest records the views found and kept",
                  "a tab that does not exist fails, not skipped", "a file path with # or ? is captured"],
                 "Playwright is not installed")
        else:
            check("an HTML prototype is copied and rendered", rc == 0 and "screen-01.png" in m["files"])
            check("the screenshot is a real image",
                  os.path.getsize(os.path.join(out, "screen-01.png")) > 1000)
            tabs = os.path.join(tmp, "tabs.html")
            with open(tabs, "w") as fh:
                fh.write("<html><body><button onclick=\"document.getElementById('v').textContent='second view'\">"
                         "Details</button><p id='v'>first view</p></body></html>")
            out, man = os.path.join(tmp, "src7"), os.path.join(tmp, "m7.json")
            rc = cs.main(["--source", tabs, "--out-dir", out, "--given-by", "Kapil", "--manifest", man,
                          "--click", "Details"])
            named = [f for f in read_json(man)["files"] if f.startswith("screen-") and f.endswith("-details.png")]
            check("a named tab is clicked and captured", rc == 0 and len(named) == 1)
            with open(os.path.join(out, named[0].replace(".png", ".txt") if named else "none")) as fh:
                check("the clicked view's text is kept beside its picture", "second view" in fh.read())

            # every view is found without naming it, two clicks deep (#613, C1)
            app = os.path.join(tmp, "app.html")
            with open(app, "w") as fh:
                fh.write("""<html><body>
<nav><button onclick="show('home')">Home</button><button onclick="show('cart')">Cart</button>
<a href="https://elsewhere.example.com/">Help</a><button onclick="show('gone')">Accept</button></nav>
<main id="m">home view</main>
<script>
function show(v){
  const m=document.getElementById('m');
  if(v==='cart'){m.innerHTML='cart view <button onclick="show(\\'pay\\')">Checkout</button>';}
  else if(v==='pay'){m.textContent='checkout view';}
  else if(v==='gone'){m.textContent='an answer was given';}
  else {m.textContent='home view';}
}
</script></body></html>""")
            out, man = os.path.join(tmp, "src10"), os.path.join(tmp, "m10.json")
            rc = cs.main(["--source", app, "--out-dir", out, "--given-by", "Kapil", "--manifest", man])
            m = read_json(man)
            texts = ""
            for f in m["files"]:
                if f.endswith(".txt"):
                    with open(os.path.join(out, f)) as fh:
                        texts += fh.read()
            check("every view is found and kept without naming it",
                  rc == 0 and "cart view" in texts and "checkout view" in texts)
            check("a view two clicks deep is kept", any(f.startswith("view-") and "checkout" in f
                                                        for f in m["files"]))
            check("an answer button is never clicked while exploring", "an answer was given" not in texts)
            check("a link out of the prototype is not followed", "elsewhere" not in json.dumps(m["views"]))
            check("the manifest records the views found and kept",
                  m["views"]["explored"] is True and m["views"]["kept"] >= 3
                  and m["views"]["kept"] <= m["views"]["found"] and m["views"]["unreached"] == [])
            out, man = os.path.join(tmp, "src8"), os.path.join(tmp, "m8.json")
            check("a tab that does not exist fails, not skipped",
                  cs.main(["--source", tabs, "--out-dir", out, "--given-by", "Kapil", "--manifest", man,
                           "--click", "Nowhere"]) == 2)
            odd = os.path.join(tmp, "draft #2?.html")
            with open(odd, "w") as fh:
                fh.write("<html><body><p>odd name</p></body></html>")
            out, man = os.path.join(tmp, "src9"), os.path.join(tmp, "m9.json")
            check("a file path with # or ? is captured",
                  cs.main(["--source", odd, "--out-dir", out, "--given-by", "Kapil", "--manifest", man]) == 0
                  and "screen-01.png" in read_json(man)["files"])

        proj = os.path.join(tmp, "proj")
        os.makedirs(os.path.join(proj, "app"))
        for name, body in (("README.md", "# Demo"), ("SPEC.md", "## Purpose"), ("package.json", "{}")):
            with open(os.path.join(proj, name), "w") as fh:
                fh.write(body)
        os.symlink(os.path.join(proj, "README.md"), os.path.join(proj, "AGENTS.md"))
        out, man = os.path.join(tmp, "src6"), os.path.join(tmp, "m6.json")
        check("a project folder is captured", cs.main(["--source", proj, "--out-dir", out,
                                                        "--given-by", "Kapil", "--manifest", man]) == 0)
        m = read_json(man)
        check("its written docs are kept, not code or links",
              m["kind"] == "prototype — project" and m["files"] == ["README.md", "SPEC.md"])

        out, man = os.path.join(tmp, "src4"), os.path.join(tmp, "m4.json")
        check("a missing file fails (F1)", cs.main(["--source", os.path.join(tmp, "nope.pdf"), "--out-dir",
                                                    out, "--given-by", "Kapil", "--manifest", man]) == 2)
        check("the failure is recorded", "not found" in read_json(man)["problem"])
        out, man = os.path.join(tmp, "src5"), os.path.join(tmp, "m5.json")
        check("an empty given-by is refused", cs.main(["--statement", st, "--out-dir", out,
                                                        "--given-by", " ", "--manifest", man]) == 2)


def test_journeys():
    """walk_prototype.py takes one journey step at a time; check_journeys.py checks the record (C15)."""
    with tempfile.TemporaryDirectory() as tmp:
        app = os.path.join(tmp, "shop.html")
        with open(app, "w") as fh:
            fh.write("""<html><body><input placeholder="Search" id="q">
<button onclick="document.getElementById('o').textContent='cart has '+document.getElementById('q').value">Add to cart</button>
<button onclick="document.getElementById('o').textContent='order placed'">Pay now</button>
<p id="o">empty</p></body></html>""")
        out = os.path.join(tmp, "journeys")

        def walk(name, steps, *extra):
            path = os.path.join(tmp, name + ".steps.json")
            with open(path, "w") as fh:
                json.dump(steps, fh)
            return wp.main(["--source", app, "--steps", path, "--out-dir", out, "--name", name, *extra])

        try:
            import playwright  # noqa: F401
        except ImportError:
            skip(["a journey step is taken and kept", "a later step replays the earlier ones",
                  "a step that cannot be taken is recorded, not hidden",
                  "a data-changing step is allowed on a file prototype",
                  "a session keeps the journey's browser and takes the next step",
                  "a step tells only what changed", "a changed journey loads fresh in the same session"],
                 "Playwright is not installed")
        else:
            rc = walk("buy-01", [{"do": "type", "target": "Search", "text": "lamp"}])
            check("a journey step is taken and kept", rc == 0 and os.path.isfile(os.path.join(out, "buy-01.png")))
            rc = walk("buy-02", [{"do": "type", "target": "Search", "text": "lamp"},
                                 {"do": "click", "target": "Add to cart"}])
            with open(os.path.join(out, "buy-02.txt")) as fh:
                check("a later step replays the earlier ones", rc == 0 and "cart has lamp" in fh.read())
            rc = walk("buy-03", [{"do": "click", "target": "Checkout"}])
            check("a step that cannot be taken is recorded, not hidden",
                  rc == 1 and "nothing on this screen" in read_json(os.path.join(out, "buy-03.json"))["why"])
            rc = walk("buy-04", [{"do": "click", "target": "Pay now"}])
            check("a data-changing step is allowed on a file prototype", rc == 0)
            # one browser kept open for the journey (--session): same result, only the change told
            sess = f"test-{os.getpid()}"
            try:
                rc1 = walk("fast-01", [{"do": "type", "target": "Search", "text": "lamp"}], "--session", sess)
                rc2 = walk("fast-02", [{"do": "type", "target": "Search", "text": "lamp"},
                                       {"do": "click", "target": "Add to cart"}], "--session", sess)
                rec = read_json(os.path.join(out, "fast-02.json"))
                check("a session keeps the journey's browser and takes the next step",
                      rc1 == 0 and rc2 == 0 and rec["changed"] and "cart has lamp" in rec["added"])
                check("a step tells only what changed", "Search" not in " ".join(rec["added"]))
                rc3 = walk("fast-03", [{"do": "click", "target": "Pay now"}], "--session", sess)
                with open(os.path.join(out, "fast-03.txt")) as fh:
                    check("a changed journey loads fresh in the same session",
                          rc3 == 0 and "order placed" in fh.read())
            finally:
                wp.main(["--session", sess, "--stop"])

        evidence = os.path.join(tmp, "ev")
        os.makedirs(evidence)
        for f in ("buy-01.png", "buy-02.png"):
            open(os.path.join(evidence, f), "w").close()
        manifest = {"files": ["screen-01.png", "view-02-cart.png", "view-02-cart.txt", "view-03-help.png"]}
        good = {"main_sections": ["Shop"],
                "journeys": [{"id": "buy", "section": "Shop", "who": "a shopper", "sets_out_to": "buy a lamp",
                              "ends_with": "the lamp is in the cart",
                              "steps": [{"do": "type lamp in Search", "shows": "the field holds lamp",
                                         "view": ["buy-01.png"]},
                                        {"do": "click Add to cart", "shows": "cart has lamp",
                                         "view": ["buy-02.png"], "covers": ["view-02-cart"]}]}],
                "not_walked": [{"view": "view-03-help", "why": "help text only; no task starts there"}]}
        gaps, counts = cj.check(good, manifest, evidence)
        check("complete journeys that cover every view are clean", gaps == [] and counts["covered"] == 1)
        bad = fresh_journeys(good)
        bad["journeys"][0]["steps"] = bad["journeys"][0]["steps"][:1]
        bad["not_walked"] = []
        gaps, _ = cj.check(bad, manifest, evidence)
        check("a one-step journey is a gap", any("fewer than two steps" in g for g in gaps))
        check("a view on no journey and not named is a gap",
              any("view-03-help" in g for g in gaps) and any("view-02-cart" in g for g in gaps))
        gaps, _ = cj.check(good, manifest, evidence, {"intents": [{"id": "lamps", "from_journey": "buy"}]})
        check("a business intent from a journey is clean", gaps == [])
        gaps, _ = cj.check(good, manifest, evidence, {"intents": [{"id": "rule"}]})
        check("a business intent that names no journey is a gap", any("names no journey" in g for g in gaps))
        gaps, _ = cj.check({"journeys": []}, manifest, evidence)
        check("no journeys at all is a gap", any("no journeys" in g for g in gaps))
        two = fresh_journeys(good)
        two["main_sections"] = ["Shop", "Orders"]
        gaps, _ = cj.check(two, manifest, evidence)
        check("a main section with no journey of its own is a gap",
              any("'Orders' is no journey's `section`" in g for g in gaps))
        two["journeys"].append(dict(fresh_journeys(good)["journeys"][0], id="orders", section="Orders"))
        gaps, _ = cj.check(two, manifest, evidence, {"intents": [{"id": "lamps", "from_journey": "buy"}]})
        check("a main section folded into another section's intent is a gap",
              any("'Orders' has no business intent of its own" in g for g in gaps))
        gaps, _ = cj.check(two, manifest, evidence, {"intents": [{"id": "lamps", "from_journey": "buy"},
                                                                {"id": "orders", "from_journey": "orders"}]})
        check("every main section with its own intent is clean", gaps == [])
        nosec = fresh_journeys(good)
        del nosec["main_sections"]
        gaps, _ = cj.check(nosec, manifest, evidence)
        check("journeys without their main sections named are a gap", any("no `main_sections`" in g for g in gaps))


def fresh_journeys(doc):
    return json.loads(json.dumps(doc))


def test_check():
    check("a good two-level draft is clean", ci.check(GOOD)["clean"])
    r = ci.check(GOOD)
    check("it counts the intents", r["intents"] == 2)
    check("an empty draft is caught", not ci.check({})["clean"])
    bad = fresh()
    del bad["intents"][0]["outcome"]
    bad["questions"].append({"intent": "grow-online-sales", "ask": "What should be true when it works?",
                             "examples": EXAMPLES, "answer": ""})
    r = ci.check(bad)
    lines = [p for p in r["problems"] if p.startswith("[grow-online-sales]")]
    check("a gap and its question are reported once, not twice",
          len(lines) == 1 and "`outcome` missing" in lines[0] and "1 open question" in lines[0])
    check("a gap alone is a question for the person", r["person_only"])
    bad = fresh()
    del bad["intents"][0]["proof"]
    r = ci.check(bad)
    check("a missing proof is the play's to draft, not the person's (C17)",
          any("`proof` is empty" in p for p in r["problems"]) and not r["person_only"])
    bad = fresh()
    bad["intents"][0]["proof"] = "open — the loop asks this; nothing is filled in until it is answered"
    check("a proof left open is caught (C17)", any("`proof` is left open" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["questions"].append({"intent": "all", "ask": "How will you know each intent is met?",
                             "examples": EXAMPLES, "answer": ""})
    check("a question that asks for the proof is refused — the play drafts it (C17)",
          any("draft it with its basis instead of asking" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["intents"][0]["provenance"]["proof"] = "proposed"
    check("a proposed proof with no basis is caught (C17)",
          any("proposed with no basis" in p for p in ci.check(bad)["problems"]))
    bad["intents"][0]["basis"] = {"proof": "the prototype's sales report counts online orders"}
    check("a proposed proof with its basis is clean", ci.check(bad)["clean"])
    bad["intents"][0]["provenance"]["title"] = "proposed"
    check("only why, asked by and proof may be the play's own proposal",
          any("`title` is marked proposed" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["intents"][0]["provenance"]["why"] = "agent"
    r = ci.check(bad)
    check("a property invented by an agent is caught", any("provenance `agent`" in p for p in r["problems"]))
    check("an invented property is not a question for the person", not r["person_only"])
    src = "Welcome. A shopper with no account can buy start to finish using our new guest checkout page today."
    bad = fresh()
    bad["intents"][0]["outcome"] = "A shopper with no account can buy start to finish using our new guest checkout."
    check("an outcome copied from the source is caught (F3)", any("copies the source" in p for p in ci.check(bad, src)["problems"]))
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for i, body in enumerate(("Nothing to see here.", src)):
            paths.append(os.path.join(tmp, f"t{i}.txt"))
            with open(paths[-1], "w") as fh:
                fh.write(body)
        draft = os.path.join(tmp, "d.yaml")
        bad = fresh()
        bad["intents"][0]["outcome"] = "A shopper with no account can buy start to finish using our new guest checkout."
        with open(draft, "w") as fh:
            yaml.safe_dump(bad, fh)
        check("a copy from the second of two sources is caught",
              ci.main(["--draft", draft, "--source-text", paths[0], "--source-text", paths[1]]) == 2)
        man = os.path.join(tmp, "m.json")
        with open(man, "w") as fh:
            json.dump({"snapshot_dir": "/evidence/other"}, fh)
        good = os.path.join(tmp, "g.yaml")
        with open(good, "w") as fh:
            yaml.safe_dump(GOOD, fh)
        check("a Source the draft does not summarise is caught",
              ci.main(["--draft", good, "--source-manifest", man]) == 2)
        ans = os.path.join(tmp, "a.yaml")
        for label, record, want in (
                ("a picked example marked picked passes",
                 {"about": "x", "reply": "Sales are flat.", "offered": EXAMPLES, "picked": True}, 0),
                ("a picked example not marked picked is caught (F13)",
                 {"about": "x", "reply": "sales are flat", "offered": EXAMPLES}, 2),
                ("an answer with no examples offered is caught (F13)",
                 {"about": "x", "reply": "my own words"}, 2),
                ("the person's own words pass", {"about": "x", "reply": "my own words", "offered": EXAMPLES}, 0),
                ("an answer given unprompted needs no examples",
                 {"about": "x", "reply": "these are my intents", "volunteered": True}, 0)):
            with open(ans, "w") as fh:
                yaml.safe_dump({"answers": [record]}, fh)
            check(label, ci.main(["--draft", good, "--answers", ans]) == want)
    check("a plain outcome is not flagged against a prototype's own text",
          ci.check(GOOD, "Welcome to the demo shop. Your cart. Continue as guest. Pay with card or wallet.")["clean"])
    bad = fresh()
    bad["intents"][0]["outcome"] = "The <button id='guest'> calls submitOrder() in src/checkout.js."
    check("code-like text is caught", any("code-like" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["intents"][0]["why"] = "Conversion"
    check("a bare label is caught", any("bare label" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["coverage"].append({"part": "the order history page", "intent": "order-history"})
    check("a part of the source mapped to no business intent is caught (F12)",
          any("maps to no business intent" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["intents"][1]["provenance"]["outcome"] = "source"
    check("an intent the source shows but no part maps to is caught (F12)",
          any("[know-the-customer] is mapped from no part" in p for p in ci.check(bad)["problems"]))
    check("an intent the person stated may have no part yet", ci.check(GOOD)["clean"])
    for key in ("ice", "domains", "capabilities", "functionalities"):
        bad = fresh()
        bad[key] = [{"id": "x"}]
        check(f"a draft that carries `{key}` is caught — /intent writes intents only (ADR 043)",
              any(f"carries `{key}`" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["questions"][0]["examples"] = []
    check("a question with no examples is caught (F13)", any("example answers" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    del bad["coverage"]
    check("a draft with no coverage map is caught", any("no `coverage`" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["intents"][1]["id"] = "grow-online-sales"
    check("two intents with one id are caught", any("not unique" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["intents"][0]["id"] = "../../escape"
    check("an id that is not file-name safe is caught",
          any("lower-case letters, digits and dashes" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["intents"][0]["provenance"] = "person"
    check("a provenance of the wrong shape is reported, not a crash",
          any("provenance `none`" in p for p in ci.check(bad)["problems"]))
    with tempfile.TemporaryDirectory() as tmp:
        lst = os.path.join(tmp, "list.yaml")
        with open(lst, "w") as fh:
            fh.write("- not\n- a mapping\n")
        good = os.path.join(tmp, "g.yaml")
        with open(good, "w") as fh:
            yaml.safe_dump(GOOD, fh)
        check("a draft of the wrong shape exits 3, not a traceback", ci.main(["--draft", lst]) == 3)
        check("an answers record of the wrong shape exits 3", ci.main(["--draft", good, "--answers", lst]) == 3)
    bad = fresh()
    bad["sources"][0]["shows"] = ""
    check("a source with no 'what it shows' is caught", any("what it shows" in p for p in ci.check(bad)["problems"]))


def persist_setup(tmp, decisions, shows=True, two_sources=False, by="person"):
    working = os.path.join(tmp, "work")
    os.makedirs(working)
    base = os.path.join(tmp, "product", "_evidence", "intent", "20261008")
    dirs = [os.path.join(base, "source-app")] + ([os.path.join(base, "source-docs")] if two_sources else [])
    draft = fresh()
    draft["sources"] = [{"snapshot_dir": d, "shows": "A checkout and a saved cart page." if shows else ""}
                        for d in dirs]
    paths = {"draft": os.path.join(working, "draft.yaml"), "conf": os.path.join(working, "conf.yaml")}
    with open(paths["draft"], "w") as fh:
        yaml.safe_dump(draft, fh)
    with open(paths["conf"], "w") as fh:
        yaml.safe_dump({"confirmation": {"by": by, "confirmed_by": "Kapil Viren Ahuja", "at": "2026-10-08",
                                         "decisions": decisions}}, fh)
    argv = ["--draft", paths["draft"], "--confirmation", paths["conf"],
            "--product-base", os.path.join(tmp, "product") + os.sep, "--working", working]
    for n, d in enumerate(dirs):
        os.makedirs(d)
        man = os.path.join(working, f"source-manifest-{n}.json")
        with open(man, "w") as fh:
            json.dump({"snapshot_saved": True, "kind": "prototype — deployed site", "read_on": "2026-10-08",
                       "given_by": "Kapil", "snapshot_dir": d, "files": ["screen-01.png"]}, fh)
        argv += ["--source-manifest", man]
    return argv, working, dirs


def both(a="confirmed", b="confirmed", reply="yes, that's it"):
    return [{"intent": "grow-online-sales", "decision": a, "reply": reply},
            {"intent": "know-the-customer", "decision": b, "reply": reply}]


def intent_file(tmp, iid):
    return os.path.join(tmp, "product", "product-os", "intents", f"{iid}.md")


def model_files(tmp):
    """Every file written under product-os other than the intent pages."""
    model = os.path.join(tmp, "product", "product-os")
    return [os.path.relpath(os.path.join(r, f), model) for r, _, fs in os.walk(model) for f in fs
            if not os.path.relpath(r, model).startswith("intents")]


def test_persist():
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, dirs = persist_setup(tmp, both(), two_sources=True)
        check("two confirmed intents from two sources are saved", pi.main(argv) == 0)
        m = read_json(os.path.join(working, "intent-manifest.json"))
        check("the manifest holds both, decided and linked",
              len(m["intents"]) == 2 and m["decided"] and m["stage"] == "confirmed" and m["linked"] and m["sources_saved"])
        check("nothing but the intent pages is written in the model — no spine, no capability, no domain (ADR 043)",
              model_files(tmp) == [])
        with open(intent_file(tmp, "grow-online-sales")) as fh:
            body = fh.read()
        check("the intent page names every source", body.count("source.md") == 2 and "**Sources:**" in body)
        check("the intent page has no Touches list yet — the plays that link a part write it",
              "**Touches:**" not in body and "capability.md" not in body)
        for d in dirs:
            with open(os.path.join(d, "source.md")) as fh:
                text = fh.read()
            check(f"the source {os.path.basename(d)} names every intent",
                  "grow-online-sales.md" in text and "know-the-customer.md" in text)
        check("no separate hand-off file is written — the model is the hand-off",
              not [f for f in os.listdir(working) if f.startswith("vision-goal")])
        check("an existing intent is never overwritten", pi.main(argv) == 2)
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, dirs = persist_setup(tmp, both())
        i = argv.index("--confirmation")
        loop = argv[:i] + argv[i + 2:] + ["--proposed", "--at", "2026-10-09"]
        check("inside a loop every intent is saved as proposed, with no confirmation file",
              pi.main(loop) == 0)
        m = read_json(os.path.join(working, "intent-manifest.json"))
        with open(intent_file(tmp, "grow-online-sales")) as fh:
            body = fh.read()
        check("the loop run is decided, its stage proposed, and the page says so",
              m["decided"] and m["stage"] == "proposed" and "**Stage:** proposed" in body
              and "final review" in body)
    # inside a loop (C16): a gap is saved open when the draft names its question; the questions
    # go to the loop; a later round updates only the intents this loop saved
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, dirs = persist_setup(tmp, both())
        draft_path = argv[argv.index("--draft") + 1]
        with open(draft_path) as fh:
            draft = yaml.safe_load(fh)
        draft["intents"][0]["outcome"] = ""
        draft["questions"] = [{"intent": "grow-online-sales", "ask": "What should be true when online sales grow?",
                               "examples": ["Online orders pass shop orders", "Half of sales are online"]}]
        with open(draft_path, "w") as fh:
            yaml.safe_dump(draft, fh)
        i = argv.index("--confirmation")
        open_out = os.path.join(tmp, "review", "open-intent.json")
        loop = argv[:i] + argv[i + 2:] + ["--proposed", "--at", "2026-10-20", "--loop-run-id", "discovery-1",
                                           "--open-out", open_out]
        check("inside a loop a gap with its question is saved as open", pi.main(loop) == 0)
        with open(intent_file(tmp, "grow-online-sales")) as fh:
            body = fh.read()
        check("the page names the gap as open and the loop that saved it",
              "**Outcome:** open" in body and "(loop discovery-1)" in body)
        q = read_json(open_out)["questions"]
        check("the open question goes to the loop with what it is about and its examples",
              len(q) == 1 and q[0]["about"] and q[0]["blocks"] == ["grow-online-sales:outcome"]
              and q[0]["examples"] and q[0]["for_person"])
        draft["intents"][0]["outcome"] = "Online orders pass shop orders"
        draft["intents"][0].setdefault("provenance", {})["outcome"] = "model"
        draft["questions"] = []
        with open(draft_path, "w") as fh:
            yaml.safe_dump(draft, fh)
        check("a second save without --update-proposed is refused", pi.main(loop) == 2)
        page = intent_file(tmp, "grow-online-sales")
        with open(page) as fh:
            linked = fh.read().replace("**What was done:**",
                                       "**Touches:**\n- [Checkout](../shop/checkout/capability.md) (capability) — adds\n\n**What was done:**")
        with open(page, "w") as fh:
            fh.write(linked)
        check("a later round updates the intent this loop saved", pi.main(loop + ["--update-proposed"]) == 0)
        with open(page) as fh:
            check("a Touches list another play wrote is kept on a later round",
                  "- [Checkout](../shop/checkout/capability.md) (capability) — adds" in fh.read())
        with open(intent_file(tmp, "grow-online-sales")) as fh:
            check("the gap is filled on the later round", "**Outcome:** Online orders pass shop orders" in fh.read())
        other = [a if a != "discovery-1" else "discovery-2" for a in loop] + ["--update-proposed"]
        check("another loop cannot update this loop's intents", pi.main(other) == 2)
        draft["intents"][0]["outcome"] = ""
        with open(draft_path, "w") as fh:
            yaml.safe_dump(draft, fh)
        check("a gap with no question named is refused, even in a loop",
              pi.main(loop + ["--update-proposed"]) == 2)
        draft["intents"][0]["outcome"] = "Online orders pass shop orders"
        draft["intents"][0]["proof"] = ""
        draft["questions"] = [{"intent": "grow-online-sales", "ask": "How will we know?", "examples": ["x"]}]
        with open(draft_path, "w") as fh:
            yaml.safe_dump(draft, fh)
        check("an empty proof is refused even in a loop with a question — the play drafts it (C17)",
              pi.main(loop + ["--update-proposed"]) == 2)
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, _ = persist_setup(tmp, both())
        i = argv.index("--confirmation")
        check("run by hand with no confirmation and no --proposed is refused",
              pi.main(argv[:i] + argv[i + 2:]) == 2)
        check("both --confirmation and --proposed at once is refused",
              pi.main(argv + ["--proposed"]) == 2 and not os.path.exists(intent_file(tmp, "grow-online-sales")))
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, dirs = persist_setup(tmp, both(a="dropped"))
        check("a dropped intent is not saved",
              pi.main(argv) == 0 and not os.path.exists(intent_file(tmp, "grow-online-sales"))
              and os.path.isfile(intent_file(tmp, "know-the-customer")))
        m = read_json(os.path.join(working, "intent-manifest.json"))
        check("the dropped intent is recorded", m["dropped"] == ["grow-online-sales"])
    for label, decisions, by in (("all dropped", both("dropped", "dropped"), "person"),
                                 ("decided by an agent", both(), "agent"),
                                 ("with no typed reply", both(reply=""), "person"),
                                 ("with one left undecided", both()[:1], "person")):
        with tempfile.TemporaryDirectory() as tmp:
            argv, working, _ = persist_setup(tmp, decisions, by=by)
            check(f"a run {label} is refused (F4)", pi.main(argv) == 2)
            check(f"nothing saved when {label}",
                  not os.path.exists(intent_file(tmp, "grow-online-sales"))
                  and not os.path.exists(os.path.join(working, "intent-manifest.json")))
    for key in ("ice", "domains"):
        with tempfile.TemporaryDirectory() as tmp:
            argv, working, _ = persist_setup(tmp, both())
            draft_path = argv[argv.index("--draft") + 1]
            with open(draft_path) as fh:
                d = yaml.safe_load(fh)
            d[key] = [{"id": "guest-checkout"}]
            with open(draft_path, "w") as fh:
                yaml.safe_dump(d, fh)
            check(f"a draft carrying `{key}` is refused and nothing is written (ADR 043)",
                  pi.main(argv) == 2 and not os.path.exists(intent_file(tmp, "grow-online-sales")))
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, _ = persist_setup(tmp, both(), shows=False)
        check("a source with no 'what it shows' is refused before anything is written",
              pi.main(argv) == 2 and not os.path.exists(intent_file(tmp, "grow-online-sales")))
    for label, change in (("a business intent id that climbs out of the folder", ("intents", 0, "../../../escape")),
                          ("a business intent id with a slash", ("intents", 1, "a/b"))):
        with tempfile.TemporaryDirectory() as tmp:
            argv, working, _ = persist_setup(tmp, both())
            draft_path = argv[argv.index("--draft") + 1]
            with open(draft_path) as fh:
                d = yaml.safe_load(fh)
            key, n, value = change
            d[key][n]["id"] = value
            if key == "intents":
                with open(argv[argv.index("--confirmation") + 1]) as fh:
                    c = yaml.safe_load(fh)
                c["confirmation"]["decisions"][n]["intent"] = value
                with open(argv[argv.index("--confirmation") + 1], "w") as fh:
                    yaml.safe_dump(c, fh)
            with open(draft_path, "w") as fh:
                yaml.safe_dump(d, fh)
            rc = pi.main(argv)
            written = [os.path.join(r, f) for r, _, fs in os.walk(tmp) for f in fs
                       if f.endswith((".md", ".yaml")) and "product-os" in r]
            check(f"{label} is refused and nothing is written", rc == 2 and not written)
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, _ = persist_setup(tmp, both())
        with open(argv[argv.index("--draft") + 1], "w") as fh:
            fh.write("- not a mapping\n")
        check("a draft of the wrong shape is refused, not a traceback", pi.main(argv) == 2)


def main():
    for test in (test_capture, test_journeys, test_check, test_persist):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed, {len(SKIPPED)} skipped")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
