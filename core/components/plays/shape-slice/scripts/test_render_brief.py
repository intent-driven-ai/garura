#!/usr/bin/env python3
"""test_render_brief.py — the one slice-confirmation brief of /shape-slice (C3, C16, C17, C18).

    python3 core/components/plays/shape-slice/scripts/test_render_brief.py
"""
import json
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
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


def run(script, *args):
    p = subprocess.run([sys.executable, os.path.join(HERE, script), *args],
                       capture_output=True, text=True)
    try:
        out = json.loads(p.stdout) if p.stdout.strip() else None
    except json.JSONDecodeError:
        out = None
    return p.returncode, out, p.stderr


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        if isinstance(data, str):
            fh.write(data)
        elif path.endswith(".json"):
            json.dump(data, fh)
        else:
            yaml.safe_dump(data, fh, sort_keys=False)
    return path


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


Q = {"why": "The slice is built for it.", "examples": ["a clinic: a booking screen", "a shop: a cart"]}


def setup(tmp, reused=False, rule_missing=False, thin=True):
    root = os.path.join(tmp, "po")
    work = os.path.join(tmp, "work")
    for doc, title in (("care/domain.md", "Theme: Patient care"),
                       ("care/booking/capability.md", "Capability: Booking"),
                       ("care/booking/pick/feature.md", "Feature: Pick a free slot"),
                       ("notify/domain.md", "Theme: Messages"),
                       ("notify/remind/capability.md", "Capability: Reminders"),
                       ("notify/remind/send/feature.md", "Feature: Send a reminder")):
        write(os.path.join(root, doc), f"# {title}\n")
    spine = {"domains": [{"id": "dm-care", "doc": "care/domain.md"},
                         {"id": "dm-notify", "doc": "notify/domain.md"}],
             "capabilities": [{"id": "cap-booking", "domain": "dm-care", "doc": "care/booking/capability.md"},
                              {"id": "cap-remind", "domain": "dm-notify", "doc": "notify/remind/capability.md",
                               "metadata": {"thin": True} if thin else {}}],
             "features": [{"id": "ft-pick", "capability": "cap-booking", "doc": "care/booking/pick/feature.md"},
                          {"id": "ft-send", "capability": "cap-remind", "doc": "notify/remind/send/feature.md"}]}
    spine_p = write(os.path.join(root, "_spine.yaml"), spine)
    write(os.path.join(work, "slice.json"),
          {"id": "sl-self", "feature_refs": ["ft-pick", "ft-send"], "vertical": "the booking screen",
           "surface": {"id": "sf-b", "name": "the booking screen", "persona_ref": "patient",
                       "user_action": "books a free slot"},
           "left_out": [{"what": "Pay a deposit", "why": "the intent does not need it"}]})
    write(os.path.join(work, "fills.json"), {"thin": ["cap-remind"] if thin else []})
    write(os.path.join(work, "persist-fills.json"),
          {"ok": True, "written": {"domains": ["dm-notify"], "capabilities": ["cap-remind"],
                                   "features": ["ft-send"], "ices": []},
           "updated": ["cap-booking"]})
    ps = {"ok": True, "reused": reused, "record": "slices/sl-self.yaml", "differences": [],
          "upgraded_to_v2": [], "dropped_fields": [], "pulled_in": [], "pushed_out": []}
    if reused:
        ps.update(differences=["tester differs: the slice keeps 'clerk'; the new shape names 'patient'"],
                  upgraded_to_v2=["slice.name", "surface (moved from slice.surface)"],
                  dropped_fields=["status"], pulled_in=["ft-send"])
        write(os.path.join(root, "slices/sl-self.yaml"),
              {"slice": {"id": "sl-self", "name": "Self booking"}, "surface": {"name": "x"}})
    write(os.path.join(work, "persist-slice.json"), ps)
    write(os.path.join(work, "slice-check.json"),
          {"valid": True, "problems": [], "older_problems": ["old/x/feature.md: missing required section '## Out of scope'"],
           "warnings": ["slice 'sl-other' record surface has no persona_ref (no tester)"]})
    write(os.path.join(work, "hidden-file.json"),
          {"ok": True, "path": "340/evals/self/failure-and-recovery.md",
           "entries": [{"feature": "ft-pick", "capability": "cap-booking", "thin": [], "lines": 3},
                       {"feature": "ft-send", "capability": "cap-remind",
                        "thin": ["capability"] if thin else [], "lines": 3}],
           "counts": {"lines": 6, "builder_alone": 4, "person": 2}, "problems": []})
    write(os.path.join(work, "split.json"),
          {"asked": [dict(Q, id="Q-scope-1", blocking=False, question="Is a reminder in scope for the patient?",
                          proposed_answer="yes", basis={"kind": "model", "ref": "x"}),
                     dict(Q, id="Q-pay-1", blocking=True, question="Who pays for a missed visit today?",
                          proposed_answer=None)],
           "assumptions": [dict(Q, id="Q-scale-1", blocking=False, question="How many a day?",
                                assume="about 200 bookings a day")]})
    write(os.path.join(work, "early-split.json"),
          {"asked": [dict(Q, id="Q-pay-1", blocking=True, question="Who pays?")], "assumptions": []})
    write(os.path.join(work, "brief-split.json"),
          {"asked": [dict(Q, id="Q-scope-1", blocking=False, question="Is a reminder in scope?")],
           "assumptions": []})
    write(os.path.join(work, "questions-checked.json"), {"no_proposed_answer": 1})
    write(os.path.join(work, "gather.json"),
          {"rule_missing": {"path": "_shared/asking-a-person.md"}}
          if rule_missing else {})
    opening = write(os.path.join(work, "opening.md"),
                    "You decide if this slice shows that patients can book online. Read Q-scope-1 "
                    "first. Then type yes, change or stop.\n")
    return root, work, spine_p, opening


def render(root, work, spine_p, opening):
    out = os.path.join(work, "brief.md")
    code, _, err = run("render_brief.py", "--working", work, "--root", root, "--spine", spine_p,
                       "--opening", opening, "--out", out)
    return code, (read(out) if os.path.isfile(out) else ""), err


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root, work, spine_p, opening = setup(tmp)
        code, text, err = render(root, work, spine_p, opening)
        check("render: written (exit 0)", code == 0)
        check("render: what the person runs and who tests it",
              "## What you run" in text and "the booking screen" in text and "books a free slot" in text
              and "## Who tests it" in text and "- patient" in text)
        check("render: both capabilities, each with a link to its domain's page",
              "### Booking (cap-booking) — filled" in text and "### Reminders (cap-remind) — new" in text
              and "Domain: [Patient care](" in text and "care/domain.md)" in text
              and "notify/domain.md)" in text)
        check("render: features in build order, each marked new, filled or reused",
              "1. Pick a free slot (ft-pick) — reused" in text and "2. Send a reminder (ft-send) — new" in text)
        check("render: the hidden file's place and counts (6, 4, 2)",
              "Place: 340/evals/self/failure-and-recovery.md" in text and "Fails if lines: 6" in text
              and "The builder can fix alone: 4" in text and "A person must decide: 2" in text)
        check("render: what is left out, and each assumption",
              "## Left out" in text and "Pay a deposit" in text and "about 200 bookings a day" in text)
        check("render: the thin-ICE warning names the part and /discover-capabilities",
              "## Thin ICE" in text and "- cap-remind" in text and "/discover-capabilities" in text)
        check("render: the model check shows the older problems and the warnings word for word",
              "Older problems: 1" in text and "missing required section '## Out of scope'" in text
              and "slice 'sl-other' record surface has no persona_ref (no tester)" in text)
        check("render: the count of questions with no proposed answer, and each open question",
              "Questions with no proposed answer: 1" in text and "### Q-scope-1" in text
              and "**Answer** proposed: yes" in text)
        check("render: a question asked before the slice was shaped is not asked again",
              "### Q-pay-1" not in text)
        check("render: no Kept slice section for a new slice", "## Kept slice" not in text)
        code, out, _ = run("record_questions.py", "brief", "--brief", os.path.join(work, "brief.md"),
                           "--split", os.path.join(work, "brief-split.json"))
        check("brief check: the rendered brief passes, and its opening may name a question id",
              code == 0 and out["ok"] is True)

    with tempfile.TemporaryDirectory() as tmp:
        root, work, spine_p, opening = setup(tmp, reused=True, rule_missing=True, thin=False)
        code, text, _ = render(root, work, spine_p, opening)
        check("render: a reuse shows each difference word for word",
              "## Kept slice" in text and "tester differs: the slice keeps 'clerk'" in text)
        check("render: each field a record upgrade set or dropped is in plain words with its own word",
              "had no name; it now has the name 'Self booking'" in text and "surface" in text
              and "old field status" in text)
        check("render: a pulled-in feature is shown", "pulls feature ft-send" in text)
        check("render: a missing rule for asking a person is said, with its shared path",
              "rule for asking a person" in text and "_shared/asking-a-person.md" in text)
        check("render: no Thin ICE section when no part is thin", "## Thin ICE" not in text)
        os.remove(os.path.join(work, "hidden-file.json"))
        code, _, err = render(root, work, spine_p, opening)
        check("render: a missing record stops it (exit 2)", code == 2 and "hidden-file.json" in err)

    with tempfile.TemporaryDirectory() as tmp:
        root, work, spine_p, opening = setup(tmp)
        write(os.path.join(work, "hidden-write.json"),
              {"ok": True, "vague": [{"feature": "ft-send", "count": 2}]})
        code, text, _ = render(root, work, spine_p, opening)
        check("render: a line too vague to judge is shown in the Hidden file section",
              code == 0 and "Too vague to judge, so a person must decide: 2 line(s) of ft-send" in text)

    with tempfile.TemporaryDirectory() as tmp:
        work = os.path.join(tmp, "work")
        early = write(os.path.join(work, "early-split.json"), {
            "asked": [dict(Q, id="Q-pay-1", blocking=True, topic="payment",
                           question="Which way does a patient pay for a booking?",
                           proposed_answer=None)],
            "assumptions": []})
        opening = write(os.path.join(tmp, "early-opening.md"),
                        "You decide how a patient pays before the run shapes the slice. The run "
                        "shapes the slice after your answer.\n")
        out_p = os.path.join(work, "early-brief.md")
        code, _, err = run("render_brief.py", "--early", "--working", work, "--opening", opening,
                           "--split", early, "--out", out_p)
        text = read(out_p) if os.path.isfile(out_p) else ""
        check("early: written with no --root and no --spine", code == 0 and text != "")
        check("early: the opening comes first, then ## Questions",
              text.startswith("You decide") and "## Questions" in text)
        check("early: each question has its four parts and 'no proposed answer yet'",
              "### Q-pay-1" in text and "**Question** Which way" in text
              and "**Answer** no proposed answer yet" in text and "**Why it matters**" in text
              and "**Example** (a)" in text)
        check("early: no section of the confirmation brief", "## Features" not in text)
        code, out, _ = run("record_questions.py", "brief", "--brief", out_p, "--split", early,
                           "--early")
        check("early: the result passes record_questions.py brief --early",
              code == 0 and out["ok"] is True)
        write(os.path.join(work, "gather.json"),
              {"rule_missing": {"path": "_shared/asking-a-person.md"}})
        code, _, _ = run("render_brief.py", "--early", "--working", work, "--opening", opening,
                         "--split", early, "--out", out_p)
        check("early: a missing rule for asking a person is said, with its shared path",
              code == 0 and "rule for asking a person" in read(out_p)
              and "_shared/asking-a-person.md" in read(out_p))
        code, _, _ = run("render_brief.py", "--early", "--working", work, "--opening", opening,
                         "--out", out_p)
        check("early: --early with no --split is refused (exit 2)", code == 2)
        code, _, _ = run("render_brief.py", "--working", work, "--opening", opening, "--out", out_p)
        check("render: the confirmation brief with no --root or --spine is refused (exit 2)",
              code == 2)
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
