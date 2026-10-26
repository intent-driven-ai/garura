#!/usr/bin/env python3
"""test_shape_eval_scripts.py — the /shape-eval scripts: gather, input check, place, eval file check, summary (#798).

    python3 test_shape_eval_scripts.py
"""
import json
import os
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


STORY = """Feature: {name}

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

HIDDEN = """# Failure and recovery: slice sl-self-booking

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


def project(tmp, features=(("fn-pick", 3), ("fn-remind", 4)), surface=None):
    plans = os.path.join(tmp, "plans")
    write(os.path.join(plans, "1.yaml"),
          "id: 1\ntitle: Patients book their own visits\nstatus: active\ntree:\n"
          "- issue: 2\n  kind: epic\n  represents: sl-self-booking\n  title: Self booking\n")
    hidden = HIDDEN if surface is None else HIDDEN.replace("the booking command line", surface)
    write(os.path.join(plans, "1", "evals", "self-booking", "failure-and-recovery.md"), hidden)
    epic = "Delivers: a patient books a slot.\n\n## Feature-to-story map\n\n" + "".join(
        f"- {f} → #{n}\n" for f, n in features)
    issues = [{"number": 2, "title": "Self booking", "body": epic},
              {"number": 3, "title": "Pick a free slot",
               "body": STORY.format(name="pick", goal="A patient books a free slot.",
                                    exp1="The booking shows as booked.", exp2="The slot is gone from the list.")},
              {"number": 4, "title": "Send a reminder",
               "body": STORY.format(name="remind", goal="A patient gets a reminder.",
                                    exp1="The reminder names the visit.", exp2="It is sent one day before.")},
              {"number": 5, "title": "Cancel online",
               "body": STORY.format(name="cancel", goal="A patient cancels.", exp1="The slot is free.",
                                    exp2="The patient gets a note.")}]
    tracker = write(os.path.join(tmp, "tracker.json"), {"issues": issues})
    working = os.path.join(tmp, "work")
    os.makedirs(working, exist_ok=True)
    return plans, tracker, working


def story_draft(feature, issue, scenarios, untestable=""):
    return (f"`@story-{issue}`\n# Feature: Story #{issue} — {feature}\n\nFeature {feature} of slice sl-self-booking.\n\n"
            "## Background:\n* Given [the clinic] is set up\n\n" + scenarios
            + (f"\n## Untestable\n\n{untestable}" if untestable else ""))


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

SLICE = """# Eval: slice sl-self-booking — epic #2

Plan 1, business intent "Patients book their own visits" (#1).
Surface: the booking command line
Surface kind: command-line
Time limit for each scenario: 120 seconds

## Pass rule

The eval passes only when every scenario of every story below passes.

## Stories, in build order

{stories}
{out}
## Names

- [the clinic]: a test clinic with one doctor and free slots.
- [the book command]: the command that books a slot.
- [the list command]: the command that lists free slots.
- [the remind command]: the command that sends reminders.

## Context

- Read: the booking page.
"""


def drafts(working, pick=PICK, remind=REMIND, untestable="- `@expectation-2`: it is sent one day before, and the eval cannot wait a day.\n",
           order=(("fn-pick", 3), ("fn-remind", 4)), out=""):
    d = os.path.join(working, "drafts", "self-booking")
    if os.path.isdir(d):
        shutil.rmtree(d)
    write(os.path.join(d, "eval.fn-pick.feature.md"), story_draft("fn-pick", 3, pick))
    write(os.path.join(d, "eval.fn-remind.feature.md"), story_draft("fn-remind", 4, remind, untestable))
    stories = "\n".join(f"{i}. Story #{n} ({f}) — eval.{f}.feature.md" for i, (f, n) in enumerate(order, 1))
    write(os.path.join(d, "eval.sl-self-booking.md"), SLICE.format(stories=stories, out=out))
    return os.path.join(working, "drafts")


def gather(plans, tracker, working):
    return run("gather_eval.py", "--plan-file", os.path.join(plans, "1.yaml"), "--plans", plans,
               "--library", LIB, "--tracker-file", tracker, "--working", working,
               "--out", os.path.join(working, "inputs.json"))


def place(working, d):
    return run("place_eval.py", "--inputs", os.path.join(working, "inputs.json"), "--drafts", d,
               "--out", os.path.join(working, "place.json"),
               "--yardstick-out", os.path.join(working, "yardstick-check.json"))


def evalcheck(working):
    code, out, _ = run("check_eval.py", "--inputs", os.path.join(working, "inputs.json"),
                       "--place", os.path.join(working, "place.json"),
                       "--out", os.path.join(working, "eval-check.json"))
    return code, json.loads(read(os.path.join(working, "eval-check.json")))


def test_first_eval():
    print("first eval")
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        code, out, err = gather(plans, tracker, working)
        inputs = json.loads(read(os.path.join(working, "inputs.json")))
        sl = inputs["slices"][0]
        check("gather: the slice is ready, with its stories in the map's order",
              code == 0 and sl["ready"] and [s["feature"] for s in sl["stories"]] == ["fn-pick", "fn-remind"])
        check("gather: the surface kind comes from the hidden file's Surface line",
              sl["surface_kind"] == "command-line" and sl["slug"] == "self-booking")
        check("gather: each story's goals and expectations are read, in order",
              sl["stories"][0]["goals"] == ["A patient books a free slot."] and len(sl["stories"][0]["expectations"]) == 2)
        check("gather: the failure conditions of each feature are read from the hidden file",
              [f["id"] for f in sl["failures"]["fn-pick"]] == ["F1"])
        check("gather: copies of the epic, each story and the hidden file are in inputs/",
              sorted(os.listdir(os.path.join(working, "inputs"))) ==
              ["epic-2.md", "hidden-self-booking.md", "story-3.md", "story-4.md"])
        code, _, _ = place(working, drafts(working))
        folder = os.path.join(plans, "1", "evals", "self-booking")
        check("place: two story files and the slice file are in the evals folder",
              code == 0 and sorted(os.listdir(folder)) == ["eval.fn-pick.feature.md", "eval.fn-remind.feature.md",
                                                           "eval.sl-self-booking.md", "failure-and-recovery.md"])
        code, res = evalcheck(working)
        check("eval file check: a full eval reads ok", code == 0 and res["ok"], ) or print(res["problems"])
        st = res["slices"][0]["stories"]
        check("eval file check: the counts for the summary",
              st[0]["scenarios"] == 3 and st[0]["goals"] == [1, 1] and st[0]["expectations"] == [2, 2]
              and st[0]["failure_conditions"] == [1, 1] and len(st[1]["untestable"]) == 1)
        code, _, _ = run("render_summary.py", "--check", os.path.join(working, "eval-check.json"),
                         "--place", os.path.join(working, "place.json"),
                         "--inputs", os.path.join(working, "inputs.json"), "--out", os.path.join(working, "summary.md"))
        summary = read(os.path.join(working, "summary.md"))
        check("summary: one line per story with its counts, the untestable item, and where the files are",
              code == 0 and "2 stories, 5 scenarios" in summary and "| #3 Pick a free slot | 3 | 1/1 | 2/2 | 1/1 | 0 |" in summary
              and "expectation-2: it is sent one day before" in summary and folder in summary)
        check("summary: it is short, never the eval itself", "Scenario:" not in summary and len(summary.splitlines()) < 30)

        before = {n: read(os.path.join(folder, n)) for n in os.listdir(folder)}
        os.unlink(os.path.join(working, "place.json"))
        gather(plans, tracker, working)
        code, out, _ = place(working, drafts(working))
        check("run again, nothing changed: no file is written, byte for byte",
              code == 0 and out["files"] == 0 and {n: read(os.path.join(folder, n)) for n in os.listdir(folder)} == before)


def test_bad_drafts():
    print("bad drafts")
    cases = [
        ("a step that is not a sentence of the library",
         dict(pick=PICK.replace('* Then the exit code is 0', '* Then the booking looks right')), "step library"),
        ("a goal with no scenario and no Untestable line",
         dict(remind=REMIND.replace("`@goal-1` `@expectation-1`", "`@expectation-1`")), "'goal-1' has no scenario"),
        ("a scenario that covers something the story does not say",
         dict(remind=REMIND + "\n`@goal-7`\n## Scenario: extra\n* When I run [the remind command]\n* Then the exit code is 0\n"),
         "covers 'goal-7'"),
        ("a recovery text in a story file",
         dict(pick=PICK + "\nWay back: keep the first booking.\n"), "recovery or handoff"),
        ("a recovery phrase outside a 'does not contain' check",
         dict(pick=PICK.replace('* And the output contains "booked"', '* And the output contains "Way back: free the slot"')), "recovery or handoff"),
        ("a name used but not listed",
         dict(remind=REMIND.replace("[the remind command]", "[the reminder job]")), "not listed under Names"),
        ("the slice file's stories not in the map's order",
         dict(order=(("fn-remind", 4), ("fn-pick", 3))), "build order"),
        ("a scenario with no Then",
         dict(remind=REMIND.replace('* Then the output does not contain "another patient"', "")), "has no Then"),
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
        p = os.path.join(d, "self-booking", "eval.fn-pick.feature.md")
        write(p, read(p).replace("# Feature: Story #3", "# Feature: Slice sl-self-booking"))
        place(working, d)
        code, res = evalcheck(working)
        check("eval file check: a Feature: that is not its story fails",
              code == 1 and any("is not 'Story #3" in x for x in res["problems"]))


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


def test_yardstick():
    print("fixed yardstick")
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        gather(plans, tracker, working)
        place(working, drafts(working))
        folder = os.path.join(plans, "1", "evals", "self-booking")
        old_pick = read(os.path.join(folder, "eval.fn-pick.feature.md"))
        # the slice changes: fn-remind leaves, fn-cancel comes in
        plans2 = os.path.join(plans, "1.yaml")
        t = json.loads(read(tracker))
        t["issues"][0]["body"] = "## Feature-to-story map\n\n- fn-pick → #3\n- fn-cancel → #5\n"
        write(tracker, t)
        write(os.path.join(plans, "1", "evals", "self-booking", "failure-and-recovery.md"),
              HIDDEN + "\n## fn-cancel: Cancel online\n\n### Failure conditions\n\n- F3 (from the feature ICE): a cancelled slot stays taken.\n")
        os.unlink(os.path.join(working, "place.json"))
        code, out, _ = gather(plans, tracker, working)
        inputs = json.loads(read(os.path.join(working, "inputs.json")))
        check("gather, later run: the story file of the feature that left is out of the slice",
              inputs["slices"][0]["out_of_slice"] == ["eval.fn-remind.feature.md"])
        d = os.path.join(working, "drafts", "self-booking")
        shutil.rmtree(os.path.join(working, "drafts"))
        reworded = PICK.replace("a patient books a free slot", "a patient books any slot")
        write(os.path.join(d, "eval.fn-pick.feature.md"), story_draft("fn-pick", 3, reworded))
        write(os.path.join(d, "eval.fn-cancel.feature.md"), story_draft("fn-cancel", 5,
              "`@goal-1` `@expectation-1` `@expectation-2`\n## Scenario: a patient cancels\n* When I run [the cancel command]\n"
              "* Then the output contains \"cancelled\"\n\n`@F3`\n## Scenario: a cancelled slot is free\n"
              "* When I run [the cancel command]\n* And I run [the list command]\n* Then the output contains \"10:00\"\n"))
        write(os.path.join(d, "eval.sl-self-booking.md"), SLICE.format(
            stories="1. Story #3 (fn-pick) — eval.fn-pick.feature.md\n2. Story #5 (fn-cancel) — eval.fn-cancel.feature.md",
            out="\n## Out of the slice\n\n- Story #4 (fn-remind) — eval.fn-remind.feature.md: its feature left the slice; kept, not run.\n")
            .replace("- [the remind command]: the command that sends reminders.", "- [the cancel command]: the command that cancels."))
        code, out, _ = place(working, os.path.join(working, "drafts"))
        yard = json.loads(read(os.path.join(working, "yardstick-check.json")))
        check("place, later run: a reworded draft does not change a scenario that was there",
              code == 0 and yard["ok"] and read(os.path.join(folder, "eval.fn-pick.feature.md")) == old_pick)
        check("place, later run: the new story gets its file; the one that left keeps its file, tagged out of the slice",
              os.path.isfile(os.path.join(folder, "eval.fn-cancel.feature.md"))
              and "`@out-of-slice`" in read(os.path.join(folder, "eval.fn-remind.feature.md")).splitlines()[0])
        code, res = evalcheck(working)
        check("eval file check, later run: reads ok", code == 0 and res["ok"]) or print(res["problems"])
        # the merge keeps a scenario the draft lacks, and adds only what is not covered yet
        sys.path.insert(0, HERE)
        import place_eval as pe
        old = old_pick + "\n`@goal-1`\n## Scenario: kept from before\n* When I run [the list command]\n* Then the exit code is 0\n"
        text, n_sc, n_un = pe.merge_story(old, story_draft("fn-pick", 3, reworded))
        check("merge: a scenario the draft lacks stays, and a draft that adds nothing changes nothing",
              text == old and n_sc == 0 and n_un == 0)
        extra = reworded + "\n`@F9`\n## Scenario: new cover\n* When I run [the list command]\n* Then the exit code is 0\n"
        text, n_sc, _ = pe.merge_story(old, story_draft("fn-pick", 3, extra))
        check("merge: only the scenario for something not covered yet is added, after the old ones",
              n_sc == 1 and text.startswith(old.rstrip("\n")) and "new cover" in text and "any slot" not in text)


def test_not_ready_and_undo():
    print("not ready, undo, input check")
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp, surface="the booking app on a phone")
        code, out, _ = gather(plans, tracker, working)
        check("gather: a surface with no step library gets no eval, with its reason",
              code == 0 and out["ready"] == [] and "no step library" in out["skipped"][0]["reason"])
        code, out, _ = place(working, drafts(working))
        check("place: a slice that is not ready gets no file",
              code == 0 and out["files"] == 0
              and os.listdir(os.path.join(plans, "1", "evals", "self-booking")) == ["failure-and-recovery.md"])
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        t = json.loads(read(tracker))
        t["issues"][1]["body"] = "Feature: pick\n"
        write(tracker, t)
        code, out, _ = gather(plans, tracker, working)
        check("gather: a story with no Scope of work makes its slice not ready",
              out["ready"] == [] and "no Scope of work" in out["skipped"][0]["reason"])
    with tempfile.TemporaryDirectory() as tmp:
        plans, tracker, working = project(tmp)
        gather(plans, tracker, working)
        place(working, drafts(working))
        folder = os.path.join(plans, "1", "evals", "self-booking")
        code, out, _ = run("place_eval.py", "--undo", os.path.join(working, "place.json"),
                           "--inputs", os.path.join(working, "inputs.json"))
        check("undo: a stop takes back every file the run wrote", code == 0 and os.listdir(folder) == ["failure-and-recovery.md"])
        contract = write(os.path.join(working, "contract.json"),
                         {"inputs": {"inputs": os.path.join(working, "inputs.json"),
                                     "copies": os.path.join(working, "inputs")},
                          "outputs": {"drafts": os.path.join(working, "drafts")}})
        code, out, _ = run("check_inputs.py", "--contract", contract, "--working", working,
                           "--out", os.path.join(working, "inputs-check.json"))
        check("input check: a contract with only the copies reads ok", code == 0 and out["ok"])
        named = write(os.path.join(working, "contract-templates.json"),
                      {"inputs": {"templates": [os.path.join(working, "templates", "eval-story.feature.md"),
                                                os.path.join(working, "templates", "eval-slice.md")]},
                       "outputs": {"drafts": os.path.join(working, "drafts")}})
        code, out, _ = run("check_inputs.py", "--contract", named, "--working", working,
                           "--out", os.path.join(working, "inputs-check.json"))
        check("input check: a template whose name ends in feature.md or ice.md is not an ICE page",
              code == 0 and out["ok"])
        bad = write(os.path.join(working, "contract-bad.json"),
                    {"inputs": {"ice": "product-os/booking/fn-pick/feature.md",
                                "hidden": os.path.join(plans, "1", "evals", "self-booking", "failure-and-recovery.md")},
                     "outputs": {"drafts": os.path.join(working, "drafts")}})
        code, out, _ = run("check_inputs.py", "--contract", bad, "--working", working,
                           "--out", os.path.join(working, "inputs-check.json"))
        check("input check: an ICE page or the plans folder in a contract fails",
              code == 1 and len(out["problems"]) == 2)


def main():
    test_first_eval()
    test_bad_drafts()
    test_absent_phrase_is_allowed()
    test_yardstick()
    test_not_ready_and_undo()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
