#!/usr/bin/env python3
"""test_shape_eval_scripts.py — the /design-eval scripts: gather, input check, place, eval file check, summary.

One plan, one eval (ADR 069): plan 1 holds two slices, each with its hidden file; its one epic maps
each feature to its Feature issue; one Feature issue sits under another plan's epic (held_by).

    python3 test_shape_eval_scripts.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, "..", "..", "..", "memory", "standards", "schemas", "eval",
                                    "steps-command-line.yaml"))
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
    return cond


def run(script, *args):
    p = subprocess.run([sys.executable, os.path.join(HERE, script), *args], capture_output=True, text=True)
    try:
        out = json.loads(p.stdout) if p.stdout.strip() else None
    except json.JSONDecodeError:
        out = None
    return p.returncode, out, p.stderr


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text if isinstance(text, str) else json.dumps(text, indent=2))
    return path


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


ISSUE = """Represents: {fid}
Plan: 1

## Scope of work

Goals:
- {goal}

Limits:
- Write only the booking.

Expectations:
- {exp1}
- {exp2}

## Context guidance

- Read: the booking page.
- Never read: the code.
- Persona: the patient.
- In and out: booking is in; payment is out.
"""

HIDDEN_BOOK = """# Failure and recovery: slice sl-self-booking

Slice: Self booking (sl-self-booking). Plan: 1 (business intent bi-1). Surface: the booking command line; tested by the patient.

## fn-pick: Pick a free slot

### Failure conditions

- F1 (from the feature ICE): a slot is booked twice.

### Recovery

- For F1
  - When: two bookings are on one slot.
  - Way back: keep the first booking, free the second, tell the second patient.
  - Who fixes: the builder can fix this alone

## fn-remind: Send a reminder

### Failure conditions

- F2 (from the feature ICE): a reminder goes to the wrong patient.

### Recovery

- For F2
  - When: a patient gets a reminder for a visit that is not theirs.
  - Way back: send the reminder only to the patient of the booking.
  - Who fixes: a person must decide
"""

HIDDEN_CANCEL = """# Failure and recovery: slice sl-cancel

Slice: Cancel online (sl-cancel). Plan: 1 (business intent bi-1). Surface: the booking command line; tested by the patient.

## fn-built: A feature built before the plan

### Failure conditions

- none

## fn-cancel: Cancel a visit

### Failure conditions

- F1 (from the feature ICE): a cancelled slot stays taken.

### Recovery

- For F1
  - When: the slot of a cancelled visit is not in the list.
  - Way back: free the slot of each cancelled visit.
  - Who fixes: the builder can fix this alone
"""

PLAN = ("id: 1\ntitle: Patients book their own visits\nstatus: Not Started\nepic: 2\n"
        "slices:\n- id: sl-self-booking\n  status: Not Started\n- id: sl-cancel\n  status: Not Started\n"
        "tree:\n- issue: 2\n  kind: epic\n  title: Book and cancel visits\n  children:\n"
        "  - {issue: 3, kind: feature, represents: fn-pick}\n  - {issue: 4, kind: feature, represents: fn-remind}\n"
        "  - {issue: 5, kind: feature, represents: fn-cancel, held_by: 21}\n")

MAP = [("fn-pick", 3, ""), ("fn-remind", 4, ""), ("fn-cancel", 5, " (under Epic #21)")]


def project(tmp, surface=None, hidden_cancel=True):
    plans = os.path.join(tmp, "plans")
    write(os.path.join(plans, "1.yaml"), PLAN)
    book = HIDDEN_BOOK if surface is None else HIDDEN_BOOK.replace("the booking command line", surface)
    write(os.path.join(plans, "1", "evals", "self-booking", "failure-and-recovery.md"), book)
    if hidden_cancel:  # the cancel slice was first shaped for another intent: its hidden file is in plan 9's folder
        write(os.path.join(plans, "9", "evals", "cancel-online", "failure-and-recovery.md"), HIDDEN_CANCEL)
    epic = "Delivers: a patient books and cancels a visit.\n\n## Feature-to-story map\n\n" + "".join(
        f"- {f} → #{n}{held}\n" for f, n, held in MAP)
    issues = [{"number": 2, "title": "Book and cancel visits", "body": epic, "type": "Epic"},
              {"number": 3, "title": "Pick a free slot", "type": "Feature",
               "body": ISSUE.format(fid="fn-pick", goal="A patient books a free slot.",
                                    exp1="The booking shows as booked.", exp2="The slot is gone from the list.")},
              {"number": 4, "title": "Send a reminder", "type": "Feature",
               "body": ISSUE.format(fid="fn-remind", goal="A patient gets a reminder.",
                                    exp1="The reminder names the visit.", exp2="It is sent one day before.")},
              {"number": 5, "title": "Cancel a visit", "type": "Feature",
               "body": ISSUE.format(fid="fn-cancel", goal="A patient cancels.", exp1="The slot is free.",
                                    exp2="The patient gets a note.")}]
    tracker = write(os.path.join(tmp, "tracker.json"), {"issues": issues})
    working = os.path.join(tmp, "work")
    os.makedirs(working, exist_ok=True)
    return plans, tracker, working


LINES = {3: {"goal-1": "A patient books a free slot.", "expectation-1": "The booking shows as booked.",
             "expectation-2": "The slot is gone from the list."},
         4: {"goal-1": "A patient gets a reminder.", "expectation-1": "The reminder names the visit.",
             "expectation-2": "It is sent one day before."},
         5: {"goal-1": "A patient cancels.", "expectation-1": "The slot is free.", "expectation-2": "The patient gets a note."}}


def feature_draft(feature, issue, scenarios, untestable="", covered=None):
    tags = sorted({t for t in re.findall(r"`@((?:goal|expectation)-\d+)`", scenarios)})
    covered = covered if covered is not None else {t: LINES.get(issue, {}).get(t, "?") for t in tags}
    cov = "".join(f"- `@{t}`: {x}\n" for t, x in covered.items())
    return (f"`@feature-{issue}`\n# Feature: Feature issue #{issue} — {feature}\n\nFeature {feature} of plan 1.\n\n"
            "## Background:\n* Given [the clinic] is set up\n\n" + scenarios
            + (f"\n## Untestable\n\n{untestable}" if untestable else "")
            + (f"\n## Lines covered\n\n{cov}" if cov else ""))


PICK = """`@goal-1` `@expectation-1`
## Scenario: a patient books a free slot
* When I run [the book command] and answer "10:00"
* Then the exit code is 0
* And the output contains "booked"

`@expectation-2`
## Scenario: the slot leaves the list
* When I run [the list command]
* Then the output does not contain "10:00"

`@F1`
## Scenario: a slot is not booked twice
* Given the file "bookings.json" holds "[]"
* When I run [the book command] and answer "10:00"
* And I run [the book command] and answer "10:00"
* Then the file "bookings.json" field "slots.10:00" has 1 items
"""

REMIND = """`@goal-1` `@expectation-1`
## Scenario: the reminder names the visit
* When I run [the remind command]
* Then the output contains "10:00"

`@F2`
## Scenario: the reminder goes only to the patient of the booking
* When I run [the remind command]
* Then the output does not contain "another patient"
"""

CANCEL = """`@goal-1` `@expectation-1` `@expectation-2`
## Scenario: a patient cancels
* When I run [the cancel command]
* Then the output contains "cancelled"

`@F1`
## Scenario: a cancelled slot is free
* When I run [the cancel command]
* And I run [the list command]
* Then the output contains "10:00"
"""

PLAN_FILE = """# Eval: plan 1 — epic #2

Business intent "Patients book their own visits" (#1).
Written by /design-eval from epic #2, its Feature issues and the hidden file of each slice the plan holds.

## Pass rule

The eval passes only when every scenario of every feature file below passes.

## Slice sl-self-booking

Surface: the booking command line
Surface kind: command-line
Time limit for each scenario: 120 seconds

Features, in build order:

{book}

## Slice sl-cancel

Surface: the booking command line
Surface kind: command-line
Time limit for each scenario: 120 seconds

Features, in build order:

1. Feature issue #5 (fn-cancel) — eval.fn-cancel.feature.md (held by epic #21)
{out}
## Names

- [the clinic]: a test clinic with one doctor and free slots.
- [the book command]: the command that books a slot.
- [the list command]: the command that lists free slots.
- [the remind command]: the command that sends reminders.
- [the cancel command]: the command that cancels a visit.

## Context

- Read: the booking page.
"""


def drafts(working, pick=PICK, remind=REMIND, cancel=CANCEL,
           untestable="- `@expectation-2`: it is sent one day before, and the eval cannot wait a day.\n",
           order=(("fn-pick", 3), ("fn-remind", 4)), out="", plan=None):
    d = os.path.join(working, "drafts")
    if os.path.isdir(d):
        shutil.rmtree(d)
    write(os.path.join(d, "eval.fn-pick.feature.md"), feature_draft("fn-pick", 3, pick))
    write(os.path.join(d, "eval.fn-remind.feature.md"), feature_draft("fn-remind", 4, remind, untestable))
    write(os.path.join(d, "eval.fn-cancel.feature.md"), feature_draft("fn-cancel", 5, cancel))
    book = "\n".join(f"{i}. Feature issue #{n} ({f}) — eval.{f}.feature.md" for i, (f, n) in enumerate(order, 1))
    write(os.path.join(d, "eval.1.md"), plan if plan is not None else PLAN_FILE.format(book=book, out=out))
    return d


def gather(plans, tracker, working):
    return run("gather_eval.py", "--plan-file", os.path.join(plans, "1.yaml"), "--plans", plans,
               "--library", LIB, "--tracker-file", tracker, "--working", working,
               "--out", os.path.join(working, "inputs.json"))


def place(working, d):
    return run("place_eval.py", "--inputs", os.path.join(working, "inputs.json"), "--drafts", d,
               "--out", os.path.join(working, "place.json"),
               "--yardstick-out", os.path.join(working, "yardstick-check.json"))


def evalcheck(working):
    run("check_eval.py", "--inputs", os.path.join(working, "inputs.json"),
        "--place", os.path.join(working, "place.json"), "--out", os.path.join(working, "eval-check.json"))
    res = json.loads(read(os.path.join(working, "eval-check.json")))
    return (0 if res["ok"] else 1), res


def summary(working, check_file="eval-check.json", out="summary.md"):
    code, _, _ = run("render_summary.py", "--check", os.path.join(working, check_file),
                     "--place", os.path.join(working, "place.json"),
                     "--inputs", os.path.join(working, "inputs.json"), "--out", os.path.join(working, out))
    return code, read(os.path.join(working, out))


def inputs_of(working):
    return json.loads(read(os.path.join(working, "inputs.json")))


def test_first_eval_two_slices():
    print("first eval: one plan, two slices, a held_by Feature issue")
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        code, out, err = gather(plans, tracker, working)
        inputs = inputs_of(working)
        check("gather: the plan is ready, with its two slices in the Slices list's order",
              code == 0 and inputs["ready"] and [s["slice_id"] for s in inputs["slices"]] == ["sl-self-booking", "sl-cancel"]) \
            or print("   ", inputs.get("reasons"), err)
        check("gather: each slice's features are its hidden file's entries that the map names, in build order",
              [s["features"] for s in inputs["slices"]] == [["fn-pick", "fn-remind"], ["fn-cancel"]])
        check("gather: one Feature issue for each line of the map, the held_by one included",
              [(f["feature"], f["issue"], f["held_by"]) for f in inputs["features"]]
              == [("fn-pick", 3, None), ("fn-remind", 4, None), ("fn-cancel", 5, 21)])
        check("gather: each slice's surface kind comes from its own hidden file",
              [s["surface_kind"] for s in inputs["slices"]] == ["command-line", "command-line"]
              and inputs["features"][2]["surface_kind"] == "command-line")
        check("gather: a hidden file in the folder of another plan (the slice's first intent) is found",
              inputs["slices"][1]["hidden_folder"].endswith(os.path.join("9", "evals", "cancel-online")))
        check("gather: each Feature issue's goals, expectations and failure conditions are read, in order",
              inputs["features"][0]["goals"] == ["A patient books a free slot."]
              and len(inputs["features"][0]["expectations"]) == 2
              and [f["id"] for f in inputs["features"][2]["failures"]] == ["F1"])
        check("gather: copies of the epic, each Feature issue and each hidden file are in inputs/",
              sorted(os.listdir(os.path.join(working, "inputs"))) ==
              ["epic-2.md", "feature-3.md", "feature-4.md", "feature-5.md", "hidden-cancel-online.md",
               "hidden-self-booking.md"])
        code, _, _ = place(working, drafts(working))
        folder = os.path.join(plans, "1", "evals")
        check("place: one feature file for each Feature issue and one plan file, in the plan's evals folder",
              code == 0 and sorted(f for f in os.listdir(folder) if f.startswith("eval.")) ==
              ["eval.1.md", "eval.fn-cancel.feature.md", "eval.fn-pick.feature.md", "eval.fn-remind.feature.md"])
        check("place: nothing is written in a slice's hidden-file folder",
              os.listdir(os.path.join(folder, "self-booking")) == ["failure-and-recovery.md"]
              and os.listdir(os.path.join(plans, "9", "evals", "cancel-online")) == ["failure-and-recovery.md"])
        code, res = evalcheck(working)
        check("eval file check: a full eval of two slices reads ok", code == 0 and res["ok"]) or print(res["problems"])
        st = res["features"]
        check("eval file check: the counts for the summary",
              st[0]["scenarios"] == 3 and st[0]["goals"] == [1, 1] and st[0]["expectations"] == [2, 2]
              and st[0]["failure_conditions"] == [1, 1] and len(st[1]["untestable"]) == 1
              and st[2]["held_by"] == 21)
        code, text = summary(working)
        check("summary: one table per slice, one line per Feature issue with its counts, the untestable item, the files",
              code == 0 and "the 3 Feature issues of the plan's 2 slice(s)" in text and "7 scenarios" in text
              and "### Slice sl-self-booking" in text and "### Slice sl-cancel" in text
              and "| #3 Pick a free slot | 3 | 1/1 | 2/2 | 1/1 | 0 |" in text
              and "#5 Cancel a visit (held by epic #21)" in text
              and "expectation-2: it is sent one day before" in text and folder in text) or print(text)
        check("summary: it is short, never the eval itself", "Scenario:" not in text and len(text.splitlines()) < 40)
        partial = json.loads(read(os.path.join(working, "eval-check.json")))
        partial["features"][0]["untestable"] = [
            {"tags": ["@goal-1"], "reason": "the step library cannot count lines", "partly": True}]
        write(os.path.join(working, "eval-check-partly.json"), partial)
        code, text = summary(working, "eval-check-partly.json", "summary-partly.md")
        check("summary: a note on a part of a tested line is shown, marked partly tested",
              code == 0 and "#3 @goal-1 (partly tested): the step library cannot count lines" in text)

        before = {n: read(os.path.join(folder, n)) for n in os.listdir(folder) if n.startswith("eval.")}
        os.unlink(os.path.join(working, "place.json"))
        gather(plans, tracker, working)
        code, out, _ = place(working, drafts(working))
        check("run again, nothing changed: no file is written, byte for byte",
              code == 0 and out["files"] == 0
              and {n: read(os.path.join(folder, n)) for n in before} == before)


def test_feature_in_two_slices():
    print("a feature that sits in two slices")
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        cancel = os.path.join(plans, "9", "evals", "cancel-online", "failure-and-recovery.md")
        write(cancel, read(cancel) + "\n## fn-pick: Pick a free slot\n\n### Failure conditions\n\n"
              "- F2 (from the feature ICE): a slot is booked twice.\n")
        gather(plans, tracker, working)
        inputs = inputs_of(working)
        pick = inputs["features"][0]
        check("gather: the feature is written once, with the hidden-file entry of the first slice that holds it",
              pick["slices"] == ["sl-self-booking", "sl-cancel"] and pick["slice"] == "sl-self-booking"
              and [f["id"] for f in pick["failures"]] == ["F1"]
              and inputs["slices"][1]["features"] == ["fn-cancel", "fn-pick"])
        plan = PLAN_FILE.replace("1. Feature issue #5 (fn-cancel) — eval.fn-cancel.feature.md (held by epic #21)\n",
                                 "1. Feature issue #5 (fn-cancel) — eval.fn-cancel.feature.md (held by epic #21)\n"
                                 "2. Feature issue #3 (fn-pick) — eval.fn-pick.feature.md\n").format(
            book="1. Feature issue #3 (fn-pick) — eval.fn-pick.feature.md\n2. Feature issue #4 (fn-remind) — eval.fn-remind.feature.md",
            out="")
        place(working, drafts(working, plan=plan))
        code, res = evalcheck(working)
        check("eval file check: each slice section lists the shared feature in its own build order; reads ok",
              code == 0 and res["ok"]) or print(res["problems"])
        _, text = summary(working)
        check("summary: the shared feature is counted once, under its first slice, and named in the other",
              "| #3 Pick a free slot | counted under slice sl-self-booking |" in text and "7 scenarios" in text)


def test_dropped_slice():
    print("a dropped slice is left out")
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp, hidden_cancel=False)  # the dropped slice has no hidden file
        write(os.path.join(plans, "1.yaml"), PLAN.replace("- id: sl-cancel\n  status: Not Started", "- id: sl-cancel\n  status: Dropped"))
        code, out, _ = gather(plans, tracker, working)
        inputs = inputs_of(working)
        check("gather: a dropped slice's missing hidden file does not block the eval; the plan is ready with one slice",
              code == 0 and inputs["ready"] and [s["slice_id"] for s in inputs["slices"]] == ["sl-self-booking"]
              and inputs["dropped"] == [{"slice_id": "sl-cancel", "hidden": False}]) or print(inputs["reasons"])
        check("gather: the feature only the dropped slice holds is left out, with why, and is not copied",
              [f["feature"] for f in inputs["features"]] == ["fn-pick", "fn-remind"]
              and [f["feature"] for f in inputs["left_out"]] == ["fn-cancel"]
              and "feature-5.md" not in os.listdir(os.path.join(working, "inputs")))
        plan = PLAN_FILE.split("## Slice sl-cancel")[0].format(
            book="1. Feature issue #3 (fn-pick) — eval.fn-pick.feature.md\n2. Feature issue #4 (fn-remind) — eval.fn-remind.feature.md") \
            + "## Names\n\n- [the clinic]: x\n- [the book command]: x\n- [the list command]: x\n- [the remind command]: x\n"
        code, _, _ = place(working, drafts(working, plan=plan))
        folder = os.path.join(plans, "1", "evals")
        check("place: one section for the live slice, and no feature file for the dropped slice's own feature",
              code == 0 and sorted(f for f in os.listdir(folder) if f.startswith("eval.")) ==
              ["eval.1.md", "eval.fn-pick.feature.md", "eval.fn-remind.feature.md"])
        code, res = evalcheck(working)
        check("eval file check: the eval without the dropped slice reads ok", code == 0 and res["ok"]) or print(res["problems"])
        _, text = summary(working)
        check("summary: it names the dropped slice and the feature left out",
              "Dropped slices, left out of the eval: sl-cancel" in text and "#5 fn-cancel: no live slice holds it" in text)
        place(working, drafts(working))  # a plan file with a section for the dropped slice fails
        code, res = evalcheck(working)
        check("eval file check: a section for the dropped slice fails",
              code == 1 and any("slice sections are not the plan's slices" in p for p in res["problems"]))
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)  # the dropped slice's hidden file is there and also holds fn-pick
        cancel = os.path.join(plans, "9", "evals", "cancel-online", "failure-and-recovery.md")
        write(cancel, read(cancel) + "\n## fn-pick: Pick a free slot\n\n### Failure conditions\n\n- F2 (from the feature ICE): x.\n")
        write(os.path.join(plans, "1.yaml"), PLAN.replace("- id: sl-cancel\n  status: Not Started", "- id: sl-cancel\n  status: Dropped"))
        gather(plans, tracker, working)
        inputs = inputs_of(working)
        check("gather: a feature a dropped and a live slice both hold is tested through the live slice",
              [f["feature"] for f in inputs["features"]] == ["fn-pick", "fn-remind"]
              and inputs["features"][0]["slices"] == ["sl-self-booking"]
              and inputs["left_out"] == [{"feature": "fn-cancel", "issue": 5, "why": "only a dropped slice holds it"}]
              and "hidden-cancel-online.md" not in os.listdir(os.path.join(working, "inputs")))


def test_bad_drafts():
    print("bad drafts")
    cases = [
        ("a step that is not a sentence of the library",
         dict(pick=PICK.replace('* Then the exit code is 0', '* Then the booking looks right')), "step library"),
        ("a goal with no scenario and no Untestable line",
         dict(remind=REMIND.replace("`@goal-1` `@expectation-1`", "`@expectation-1`")), "'goal-1' has no scenario"),
        ("a scenario that covers something the Feature issue does not say",
         dict(remind=REMIND + "\n`@goal-7`\n## Scenario: extra\n* When I run [the remind command]\n* Then the exit code is 0\n"),
         "covers 'goal-7'"),
        ("a recovery text in a feature file",
         dict(pick=PICK + "\nWay back: keep the first booking.\n"), "recovery or handoff"),
        ("a recovery line of the second slice's hidden file",
         dict(cancel=CANCEL + "\nfree the slot of each cancelled visit.\n"), "recovery line of a hidden file"),
        ("a name used but not listed",
         dict(remind=REMIND.replace("[the remind command]", "[the reminder job]")), "not listed under Names"),
        ("a slice section's features not in build order",
         dict(order=(("fn-remind", 4), ("fn-pick", 3))), "not the slice's features in build order"),
        ("a scenario with no Then",
         dict(remind=REMIND.replace('* Then the output does not contain "another patient"', "")), "has no Then"),
        ("a plan file with one section where the plan holds two slices",
         dict(plan=PLAN_FILE.split("## Slice sl-cancel")[0].format(
             book="1. Feature issue #3 (fn-pick) — eval.fn-pick.feature.md\n2. Feature issue #4 (fn-remind) — eval.fn-remind.feature.md")
             + "## Names\n\n- [the clinic]: x\n- [the book command]: x\n- [the list command]: x\n- [the remind command]: x\n"
             "- [the cancel command]: x\n"), "slice sections are not the plan's slices"),
        ("a slice section with no time limit",
         dict(plan=PLAN_FILE.replace("Time limit for each scenario: 120 seconds\n\nFeatures, in build order:\n\n1. Feature issue #5",
                                     "Features, in build order:\n\n1. Feature issue #5").format(
             book="1. Feature issue #3 (fn-pick) — eval.fn-pick.feature.md\n2. Feature issue #4 (fn-remind) — eval.fn-remind.feature.md",
             out="")), "no time limit"),
        ("a held_by Feature issue whose line does not say so",
         dict(plan=PLAN_FILE.replace(" (held by epic #21)", "").format(
             book="1. Feature issue #3 (fn-pick) — eval.fn-pick.feature.md\n2. Feature issue #4 (fn-remind) — eval.fn-remind.feature.md",
             out="")), "held by epic #21"),
    ]
    for label, kw, words in cases:
        with tempfile.TemporaryDirectory() as tmp:
            plans, tracker, working = project(tmp)
            gather(plans, tracker, working)
            place(working, drafts(working, **kw))
            code, res = evalcheck(working)
            check(f"eval file check: {label} fails",
                  code == 1 and any(words in p for p in res["problems"])) or print("   ", res["problems"])
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        gather(plans, tracker, working)
        d = drafts(working)
        p = os.path.join(d, "eval.fn-pick.feature.md")
        write(p, read(p).replace("# Feature: Feature issue #3", "# Feature: Slice sl-self-booking"))
        place(working, d)
        code, res = evalcheck(working)
        check("eval file check: a Feature: that is not its Feature issue fails",
              code == 1 and any("is not 'Feature issue #3" in x for x in res["problems"]))
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        gather(plans, tracker, working)
        d = drafts(working)
        place(working, d)
        write(os.path.join(plans, "1", "evals", "eval.fn-other.feature.md"), "x\n")
        code, res = evalcheck(working)
        check("eval file check: a feature file for a feature that is not in the plan's map fails",
              code == 1 and any("eval.fn-other.feature.md is not a feature of the plan's map" in x for x in res["problems"]))


def test_absent_phrase_is_allowed():
    print("a check that recovery text is absent")
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        gather(plans, tracker, working)
        place(working, drafts(working, pick=PICK.replace('* And the output contains "booked"',
                                                         '* And the output does not contain "Way back:"')))
        code, res = evalcheck(working)
        check("eval file check: 'does not contain \"Way back:\"' checks absence and is allowed",
              code == 0 and res["ok"]) or print("   ", res["problems"])


def test_lines_covered_and_moved():
    print("lines covered, moved lines, clear")
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        gather(plans, tracker, working)
        d = drafts(working)
        p = os.path.join(d, "eval.fn-pick.feature.md")
        write(p, read(p).replace("- `@goal-1`: A patient books a free slot.\n", ""))
        place(working, d)
        code, res = evalcheck(working)
        check("eval file check: a covered line missing from 'Lines covered' fails",
              code == 1 and any("has no line under 'Lines covered'" in x for x in res["problems"]))
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        gather(plans, tracker, working)
        place(working, drafts(working))
        folder = os.path.join(plans, "1", "evals")
        before = read(os.path.join(folder, "eval.fn-pick.feature.md"))
        t = json.loads(read(tracker))
        t["issues"][1]["body"] = t["issues"][1]["body"].replace("The booking shows as booked.", "The booking shows on the calendar.")
        write(tracker, t)
        os.unlink(os.path.join(working, "place.json"))
        gather(plans, tracker, working)
        place(working, drafts(working))
        code, res = evalcheck(working)
        check("later run: a Feature issue line that changed is named under moved, for a person, and is not a problem",
              code == 0 and res["ok"] and [m["tag"] for m in res["moved"]] == ["expectation-1"]
              and res["moved"][0]["was"] == "The booking shows as booked.") or print(res["problems"], res["moved"])
        check("later run: the scenario of the changed line is word for word as it was",
              read(os.path.join(folder, "eval.fn-pick.feature.md")) == before)
        _, text = summary(working)
        check("summary: it opens with a plain sentence, names the plan by its epic, and names the moved line",
              "This eval checks, from the outside" in text and '"Book and cancel visits"' in text
              and "moved or changed" in text and "The booking shows on the calendar." in text)
        code, out, _ = run("place_eval.py", "--clear", os.path.join(working, "clear.json"),
                           "--inputs", os.path.join(working, "inputs.json"))
        left = [p for p in ("drafts", os.path.join("inputs", "existing"), os.path.join("inputs", "hidden-self-booking.md"),
                            os.path.join("inputs", "hidden-cancel-online.md"))
                if os.path.exists(os.path.join(working, p))]
        check("clear: no draft, no copy of an eval file and no hidden-file copy of either slice is left; the eval stays",
              code == 0 and out["ok"] and left == [] and os.path.isfile(os.path.join(folder, "eval.fn-pick.feature.md")))


def test_yardstick():
    print("fixed yardstick")
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        gather(plans, tracker, working)
        place(working, drafts(working))
        folder = os.path.join(plans, "1", "evals")
        old_pick = read(os.path.join(folder, "eval.fn-pick.feature.md"))
        # the plan changes: fn-remind leaves the self-booking slice and the epic's map
        t = json.loads(read(tracker))
        t["issues"][0]["body"] = "## Feature-to-story map\n\n- fn-pick → #3\n- fn-cancel → #5 (under Epic #21)\n"
        write(tracker, t)
        os.unlink(os.path.join(working, "place.json"))
        gather(plans, tracker, working)
        inputs = inputs_of(working)
        check("gather, later run: the feature file of the feature that left is out of the plan",
              inputs["out_of_plan"] == ["eval.fn-remind.feature.md"] and inputs["ready"]) or print(inputs["reasons"])
        d = os.path.join(working, "drafts")
        shutil.rmtree(d)
        reworded = PICK.replace("a patient books a free slot", "a patient books any slot")
        write(os.path.join(d, "eval.fn-pick.feature.md"), feature_draft("fn-pick", 3, reworded))
        write(os.path.join(d, "eval.fn-cancel.feature.md"), feature_draft("fn-cancel", 5, CANCEL))
        write(os.path.join(d, "eval.1.md"), PLAN_FILE.format(
            book="1. Feature issue #3 (fn-pick) — eval.fn-pick.feature.md",
            out="\n## Out of the plan\n\n- Feature issue #4 (fn-remind) — eval.fn-remind.feature.md: its feature left the plan; kept, not run.\n")
            .replace("- [the remind command]: the command that sends reminders.\n", ""))
        code, out, _ = place(working, d)
        yard = json.loads(read(os.path.join(working, "yardstick-check.json")))
        check("place, later run: a reworded draft does not change a scenario that was there",
              code == 0 and yard["ok"] and read(os.path.join(folder, "eval.fn-pick.feature.md")) == old_pick)
        check("place, later run: the feature file of the feature that left keeps its file, tagged out of the plan",
              "`@out-of-plan`" in read(os.path.join(folder, "eval.fn-remind.feature.md")).splitlines()[0])
        code, res = evalcheck(working)
        check("eval file check, later run: reads ok", code == 0 and res["ok"]) or print(res["problems"])
        sys.path.insert(0, HERE)
        import place_eval as pe
        old = feature_draft("fn-pick", 3, PICK + "\n`@goal-1`\n## Scenario: kept from before\n* When I run [the list command]\n* Then the exit code is 0\n")
        text, n_sc, n_un = pe.merge_feature(old, feature_draft("fn-pick", 3, reworded))
        check("merge: a scenario the draft lacks stays, and a draft that adds nothing changes nothing",
              text == old and n_sc == 0 and n_un == 0)
        extra = reworded + "\n`@F9`\n## Scenario: new cover\n* When I run [the list command]\n* Then the exit code is 0\n"
        text, n_sc, _ = pe.merge_feature(old, feature_draft("fn-pick", 3, extra))
        old_sc = [sc["raw"] for sc in pe.ec.parse_feature_file(old)["scenarios"]]
        check("merge: only the scenario for something not covered yet is added, after the old ones",
              n_sc == 1 and all(r in text for r in old_sc) and "new cover" in text and "any slot" not in text
              and text.index("new cover") > text.index(old_sc[-1]) and text.index("new cover") < text.index("## Lines covered"))


def test_not_ready_and_undo():
    print("not ready, undo, input check")
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp, hidden_cancel=False)
        code, out, _ = gather(plans, tracker, working)
        check("gather: a missing hidden file of the second slice: the plan gets no eval, and the slice is named",
              code == 0 and out["ready"] is False
              and any("slice sl-cancel has no hidden file" in r for r in out["reasons"]))
        code, out, _ = place(working, drafts(working))
        check("place: a plan that is not ready gets no file",
              code == 0 and out["files"] == 0
              and not [f for f in os.listdir(os.path.join(plans, "1", "evals")) if f.startswith("eval.")])
        evalcheck(working)
        code, text = summary(working)
        check("summary: a plan that is not ready is named with its reason, and has no table",
              code == 0 and "Plan 1: no eval" in text and "sl-cancel has no hidden file" in text and "|" not in text)
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp, surface="the booking app on a phone")
        code, out, _ = gather(plans, tracker, working)
        check("gather: a slice whose surface has no step library: the plan gets no eval, with the slice named",
              code == 0 and out["ready"] is False
              and any("sl-self-booking: no step library" in r for r in out["reasons"]))
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        t = json.loads(read(tracker))
        t["issues"][1]["body"] = "Represents: fn-pick\n"
        t["issues"][2]["body"] = t["issues"][2]["body"].replace("Represents: fn-remind", "Represents: fn-remind-old")
        t["issues"][3]["type"] = "Story"
        write(tracker, t)
        code, out, _ = gather(plans, tracker, working)
        r = " | ".join(out["reasons"])
        check("gather: a Feature issue with no Scope of work, no exact Represents line, or of another type makes the plan not ready",
              out["ready"] is False and "#3 has no Scope of work" in r and "'Represents: fn-remind'" in r
              and "#5 is of type Story" in r) or print(r)
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        t = json.loads(read(tracker))
        t["issues"] = [i for i in t["issues"] if i["number"] != 4]
        t["issues"][0]["body"] += "- fn-lost → #8\n"
        write(tracker, t)
        code, out, _ = gather(plans, tracker, working)
        r = " | ".join(out["reasons"])
        check("gather: a missing Feature issue, and a map feature in no slice's hidden file, are each named",
              out["ready"] is False and "no Feature issue #4" in r and "fn-lost (Feature issue #8) is in no hidden file" in r) \
            or print(r)
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        write(os.path.join(plans, "1.yaml"), PLAN.replace("epic: 2\n", ""))
        code, out, _ = gather(plans, tracker, working)
        check("gather: a plan file with no epic mark makes the plan not ready",
              out["ready"] is False and any("no `epic:` mark" in r for r in out["reasons"]))
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        code, out, _ = run("gather_eval.py", "--plan-file", os.path.join(plans, "5.yaml"), "--plans", plans,
                           "--library", LIB, "--tracker-file", tracker, "--working", working,
                           "--out", os.path.join(working, "inputs.json"))
        check("gather: no plan file is refused", code == 2)
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        gather(plans, tracker, working)
        place(working, drafts(working))
        folder = os.path.join(plans, "1", "evals")
        code, out, _ = run("place_eval.py", "--undo", os.path.join(working, "place.json"),
                           "--inputs", os.path.join(working, "inputs.json"))
        check("undo: a stop takes back every file the run wrote",
              code == 0 and not [f for f in os.listdir(folder) if f.startswith("eval.")])
        contract = write(os.path.join(working, "contract.json"),
                         {"inputs": {"inputs": os.path.join(working, "inputs.json"),
                                     "copies": os.path.join(working, "inputs")},
                          "outputs": {"drafts": os.path.join(working, "drafts")}})
        code, out, _ = run("check_inputs.py", "--contract", contract, "--working", working,
                           "--out", os.path.join(working, "inputs-check.json"))
        check("input check: a contract with only the copies reads ok", code == 0 and out["ok"])
        named = write(os.path.join(working, "contract-templates.json"),
                      {"inputs": {"templates": [os.path.join(working, "templates", "eval-feature.feature.md"),
                                                os.path.join(working, "templates", "eval-plan.md")]},
                       "outputs": {"drafts": os.path.join(working, "drafts")}})
        code, out, _ = run("check_inputs.py", "--contract", named, "--working", working,
                           "--out", os.path.join(working, "inputs-check.json"))
        check("input check: a template whose name ends in feature.md is not an ICE page", code == 0 and out["ok"])
        bad = write(os.path.join(working, "contract-bad.json"),
                    {"inputs": {"ice": "product-os/booking/fn-pick/feature.md",
                                "hidden": os.path.join(plans, "1", "evals", "self-booking", "failure-and-recovery.md")},
                     "outputs": {"drafts": os.path.join(working, "drafts")}})
        code, out, _ = run("check_inputs.py", "--contract", bad, "--working", working,
                           "--out", os.path.join(working, "inputs-check.json"))
        check("input check: an ICE page or the plans folder in a contract fails",
              code == 1 and len(out["problems"]) == 2) or print(out)


def main():
    test_first_eval_two_slices()
    test_feature_in_two_slices()
    test_dropped_slice()
    test_bad_drafts()
    test_absent_phrase_is_allowed()
    test_lines_covered_and_moved()
    test_yardstick()
    test_not_ready_and_undo()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
