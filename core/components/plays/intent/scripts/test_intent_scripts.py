#!/usr/bin/env python3
"""
test_intent_scripts.py — fixture tests for /intent's three scripts (#612).

capture_source.py  — a statement is kept byte for byte; a document is copied; an HTML file is
                     copied and rendered to a screenshot; a missing source fails (F1).
                     A clicked tab keeps its picture and its text.
check_intent.py    — per intent: required properties, provenance, copying the source,
                     code-like text, bare labels, ICE under it; per ICE: goals, built from an
                     intent; for the draft: ids, sources summarised, the coverage map, one
                     line per intent for what the person must answer, example answers.
persist_intent.py  — saves only the intents the person confirmed and the ICE built from them
                     (ICE shape, not yet placed), refuses unless every intent was decided by the
                     person, never overwrites, links intents, ICE and sources, writes no
                     separate hand-off file.

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
import lint_grounding as lg  # noqa: E402

import check_ice_workable as cw  # noqa: E402

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
ICE_1 = {"id": "guest-checkout", "title": "Buy without an account", "built_from": "grow-online-sales",
         "one_line": "Lets a shopper buy without making an account.",
         "directional_intent": "Guest checkout is about letting a shopper finish a purchase with no "
                               "account. It broadly owns the path from cart to paid order for a "
                               "shopper who never signs up, and it matters because four in ten "
                               "shoppers leave at the sign-up step.",
         "goals": ["A shopper with no account can buy, start to finish."]}
ICE_2 = {"id": "saved-carts", "title": "Come back to a left cart", "built_from": "grow-online-sales",
         "one_line": "Keeps a shopper's cart until they come back.",
         "directional_intent": "Saved carts is about not losing a shopper who leaves halfway. It "
                               "broadly owns keeping a cart and bringing it back on the next visit, "
                               "and it matters because many carts are left half full and never "
                               "bought.",
         "goals": ["A shopper who leaves finds the same cart waiting when they return."]}
SNAP = "/evidence/source"
EXAMPLES = ["Sales are flat.", "Shoppers leave at sign-up.", "Costs are rising."]
GOOD = {"intents": [INTENT_A, INTENT_B],
        "ice": [ICE_1, ICE_2],
        "sources": [{"snapshot_dir": SNAP, "shows": "A checkout with a guest button, and a saved cart page."}],
        "coverage": [{"part": "the guest checkout page", "ice": "guest-checkout"},
                     {"part": "the saved cart page", "ice": "saved-carts"}],
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
            check("a named tab is clicked and captured",
                  cs.main(["--source", tabs, "--out-dir", out, "--given-by", "Kapil", "--manifest", man,
                           "--click", "Details"]) == 0 and "screen-02-details.png" in read_json(man)["files"])
            with open(os.path.join(out, "screen-02-details.txt")) as fh:
                check("the clicked view's text is kept beside its picture", "second view" in fh.read())
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


def test_check():
    check("a good two-level draft is clean", ci.check(GOOD)["clean"])
    r = ci.check(GOOD)
    check("it counts intents and ICE", r["intents"] == 2 and r["ice"] == 2)
    check("an empty draft is caught", not ci.check({})["clean"])
    bad = fresh()
    del bad["intents"][0]["proof"]
    bad["questions"].append({"intent": "grow-online-sales", "ask": "How will we know?",
                             "examples": EXAMPLES, "answer": ""})
    r = ci.check(bad)
    lines = [p for p in r["problems"] if p.startswith("[grow-online-sales]")]
    check("a gap and its question are reported once, not twice",
          len(lines) == 1 and "`proof` missing" in lines[0] and "1 open question" in lines[0])
    check("a gap alone is a question for the person", r["person_only"])
    bad = fresh()
    bad["intents"][0]["provenance"]["why"] = "agent"
    r = ci.check(bad)
    check("a property invented by an agent is caught", any("provenance `agent`" in p for p in r["problems"]))
    check("an invented property is not a question for the person", not r["person_only"])
    src = "Welcome. A shopper with no account can buy start to finish using our new guest checkout page today."
    bad = fresh()
    bad["intents"][0]["outcome"] = "A shopper with no account can buy start to finish using our new guest checkout."
    check("an outcome copied from the source is caught (F3)", any("copies the source" in p for p in ci.check(bad, src)["problems"]))
    bad = fresh()
    bad["ice"][0]["goals"] = ["A shopper with no account can buy start to finish using our new guest checkout."]
    check("an ICE goal copied from the source is caught (F3)",
          any(p.startswith("ICE [guest-checkout] goal copies") for p in ci.check(bad, src)["problems"]))
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
    bad["coverage"].append({"part": "the order history page", "ice": "order-history"})
    check("a part of the source mapped to no ICE is caught (F12)",
          any("maps to no ICE" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["coverage"] = bad["coverage"][:1]
    check("an ICE mapped from nothing is caught (F12)",
          any("ICE [saved-carts] is mapped from no part" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["ice"][1]["built_from"] = "nobody"
    check("an ICE built from no business intent is caught (F12)",
          any("ICE [saved-carts] is built from no business intent" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["ice"][0]["goals"] = []
    check("an ICE with no goals is caught", any("has no goals" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    del bad["ice"][1]["directional_intent"]
    check("an ICE with no directional paragraph is caught",
          any("no `directional_intent`" in p for p in ci.check(bad)["problems"]))
    bad = fresh()
    bad["intents"][1]["provenance"]["outcome"] = "source"
    check("an intent the source shows with no ICE under it is caught",
          any("[know-the-customer] has no ICE" in p for p in ci.check(bad)["problems"]))
    check("an intent the person stated may have no ICE yet", ci.check(GOOD)["clean"])
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
    bad["ice"][0]["id"] = "../../escape"
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


def ice_file(tmp, cid):
    return os.path.join(tmp, "product", "product-os", "capabilities", cid, "capability.md")


def spine_of(tmp):
    with open(os.path.join(tmp, "product", "product-os", "_spine.yaml")) as fh:
        return yaml.safe_load(fh)


def test_persist():
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, dirs = persist_setup(tmp, both(), two_sources=True)
        check("two confirmed intents and their ICE from two sources are saved", pi.main(argv) == 0)
        m = read_json(os.path.join(working, "intent-manifest.json"))
        check("the manifest holds both, decided and linked",
              len(m["intents"]) == 2 and m["decided"] and m["stage"] == "confirmed" and m["linked"] and m["sources_saved"])
        caps = {c["id"]: c for c in spine_of(tmp)["capabilities"]}
        cap = caps.get("guest-checkout", {})
        check("each ICE is a proposed capability in the spine, no domain yet, built from its intent",
              cap.get("status") == "proposed" and cap.get("detail") == "directional"
              and cap.get("domain") == "" and cap.get("intents") == ["grow-online-sales"]
              and cap.get("doc") == "capabilities/guest-checkout/capability.md")
        with open(ice_file(tmp, "guest-checkout")) as fh:
            doc = fh.read()
        check("its grounding doc carries the ICE goals inline",
              doc.startswith("# Capability: Buy without an account") and ICE_1["goals"][0] in doc)
        model = os.path.join(tmp, "product", "product-os")
        errors, warnings = [], []
        lg.check_spine(model, os.path.join(model, "_spine.yaml"), errors, warnings, {})
        check("the grounding linter passes; 'no domain yet' is only a warning",
              not errors and warnings and all("no domain yet" in w for w in warnings))
        check("every capability it wrote is workable (its intent is confirmed)",
              all(n["workable"] for n in cw.check(spine_of(tmp), os.path.join(model, "intents"))))
        with open(intent_file(tmp, "grow-online-sales")) as fh:
            body = fh.read()
        check("the intent page names every source and its capabilities",
              body.count("source.md") == 2 and "**Sources:**" in body
              and "guest-checkout/capability.md" in body and "saved-carts/capability.md" in body)
        with open(intent_file(tmp, "know-the-customer")) as fh:
            check("an intent with no ICE says so", "none yet" in fh.read().split("**ICE built from it")[1])
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
        drive = argv[:i] + argv[i + 2:] + ["--proposed", "--at", "2026-10-09"]
        check("inside a drive every intent is saved as proposed, with no confirmation file",
              pi.main(drive) == 0)
        m = read_json(os.path.join(working, "intent-manifest.json"))
        with open(intent_file(tmp, "grow-online-sales")) as fh:
            body = fh.read()
        check("the drive run is decided, its stage proposed, and the page says so",
              m["decided"] and m["stage"] == "proposed" and "**Stage:** proposed" in body
              and "final review" in body)
        model = os.path.join(tmp, "product", "product-os")
        check("its ICE is not workable until the person confirms the intent",
              not any(n["workable"] for n in cw.check(spine_of(tmp), os.path.join(model, "intents"))))
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, _ = persist_setup(tmp, both())
        i = argv.index("--confirmation")
        check("run by hand with no confirmation and no --proposed is refused",
              pi.main(argv[:i] + argv[i + 2:]) == 2)
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, dirs = persist_setup(tmp, both(a="dropped"))
        check("dropping an intent drops its ICE too",
              pi.main(argv) == 0 and not os.path.exists(intent_file(tmp, "grow-online-sales"))
              and not os.path.exists(ice_file(tmp, "guest-checkout"))
              and os.path.isfile(intent_file(tmp, "know-the-customer")))
        m = read_json(os.path.join(working, "intent-manifest.json"))
        check("the dropped intent and its ICE are recorded",
              m["dropped"] == ["grow-online-sales"] and sorted(m["ice_dropped"]) == ["guest-checkout", "saved-carts"])
    for label, decisions, by in (("all dropped", both("dropped", "dropped"), "person"),
                                 ("decided by an agent", both(), "agent"),
                                 ("with no typed reply", both(reply=""), "person"),
                                 ("with one left undecided", both()[:1], "person")):
        with tempfile.TemporaryDirectory() as tmp:
            argv, working, _ = persist_setup(tmp, decisions, by=by)
            check(f"a run {label} is refused (F4)", pi.main(argv) == 2)
            check(f"nothing saved when {label}",
                  not os.path.exists(intent_file(tmp, "grow-online-sales"))
                  and not os.path.exists(ice_file(tmp, "guest-checkout"))
                  and not os.path.exists(os.path.join(working, "intent-manifest.json")))
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, _ = persist_setup(tmp, both())
        model = os.path.join(tmp, "product", "product-os")
        os.makedirs(model)
        keep = {"domains": [{"id": "d1", "one_line": "x"}], "capabilities": [
            {"id": "existing-cap", "domain": "d1", "one_line": "Already here."}], "functionalities": []}
        with open(os.path.join(model, "_spine.yaml"), "w") as fh:
            yaml.safe_dump(keep, fh)
        check("an existing spine gains the new capabilities", pi.main(argv) == 0)
        ids = [c["id"] for c in spine_of(tmp)["capabilities"]]
        check("its existing entries are kept unchanged",
              ids[0] == "existing-cap" and spine_of(tmp)["capabilities"][0] == keep["capabilities"][0]
              and spine_of(tmp)["domains"] == keep["domains"] and set(ids[1:]) == {"guest-checkout", "saved-carts"})
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, _ = persist_setup(tmp, both())
        model = os.path.join(tmp, "product", "product-os")
        os.makedirs(model)
        with open(os.path.join(model, "_spine.yaml"), "w") as fh:
            yaml.safe_dump({"capabilities": [{"id": "saved-carts", "domain": "d1"}]}, fh)
        check("a capability id already in the spine is refused, and nothing is written",
              pi.main(argv) == 2 and not os.path.exists(intent_file(tmp, "grow-online-sales"))
              and not os.path.exists(ice_file(tmp, "guest-checkout")))
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, _ = persist_setup(tmp, both())
        os.makedirs(os.path.dirname(ice_file(tmp, "saved-carts")))
        with open(ice_file(tmp, "saved-carts"), "w") as fh:
            fh.write("# Capability: Old\n")
        check("an existing capability doc is never overwritten, and nothing is written",
              pi.main(argv) == 2 and not os.path.exists(intent_file(tmp, "grow-online-sales")))
    with tempfile.TemporaryDirectory() as tmp:
        argv, working, _ = persist_setup(tmp, both(), shows=False)
        check("a source with no 'what it shows' is refused before anything is written",
              pi.main(argv) == 2 and not os.path.exists(intent_file(tmp, "grow-online-sales"))
              and not os.path.exists(ice_file(tmp, "guest-checkout")))
    for label, change in (("an ICE id that climbs out of the folder", ("ice", 0, "../../../escape")),
                          ("a business intent id with a slash", ("intents", 1, "a/b")),
                          ("two ICE with one id", ("ice", 1, "guest-checkout"))):
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
    for test in (test_capture, test_check, test_persist):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed, {len(SKIPPED)} skipped")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
