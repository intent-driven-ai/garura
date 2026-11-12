#!/usr/bin/env python3
"""test_render_brief.py — the brief shows every tracker write, the closed issues opened again, the features left out, the state changes, the plan-file change and each skipped feature (C8, C9, C16, C17, C18).

    python3 test_render_brief.py
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, empty_tracker, finish, full_body, gather, issue, make_drafts,  # noqa: E402
                          make_model, paths, read, run, set_slice)


def brief(p):
    out = os.path.join(p["working"], "brief.md")
    run("find_work_items.py", "--gather", p["gather"], "--plan-file", p["plan_file"],
        "--tracker-file", p["tracker"], "--out", p["items"])
    make_drafts(p)
    code, _, _ = run("render_brief.py", "--gather", p["gather"], "--work-items", p["items"],
                     "--drafts", p["drafts"], "--out", out)
    return code, read(out) if os.path.isfile(out) else ""


def main():
    print("render_brief.py")
    with tempfile.TemporaryDirectory() as tmp:
        root = make_model(tmp, states={"ft-remind": "Completed", "ft-cancel": "Dropped", "ft-pay": None})
        p = paths(tmp)
        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind", "ft-pay", "ft-cancel", "ft-wait"])
        gather(root, p)
        empty_tracker(p, [issue(7, "Send a reminder", "Feature", full_body("ft-remind"))])
        code, text = brief(p)
        check("exit 0, and the brief has its sections", code == 0 and all(h in text for h in (
            "## What the run writes in the tracker", "### The plan's epic", "### The Feature issues",
            "## Held by another plan's epic", "## Opened again", "## Built, left out", "## Dropped, left out",
            "## Had no state", "## State changes in the product model", "## The plan file",
            "## Skipped features", "## Your answer")))
        check("one new epic is shown with its type and title, standing for the plan",
              "Make a new epic, type Epic, no label: \"A patient books a free slot online\"" in text
              and "stands for the plan" in text)
        check("a new Feature issue is shown with its type, its Represents line and its text",
              "File a new Feature issue for ft-pay, type Feature, no label, a sub-issue of the epic, with the "
              "line \"Represents: ft-pay\"" in text and "Never read: health records" in text)
        check("a Completed feature is named under Built, left out, with no tracker write (C16, S17)",
              "ft-remind: it is Completed in the model" in text.split("## Built, left out")[1].split("##")[0]
              and "#7" not in text)
        check("a Dropped feature is named under Dropped, left out (C16, S17)",
              "ft-cancel: it is Dropped in the model" in text.split("## Dropped, left out")[1].split("##")[0])
        check("a feature with no status is named under Had no state (C16, S19)",
              "ft-pay: its spine entry has no status. It is treated as Unplanned."
              in text.split("## Had no state")[1].split("##")[0])
        part = text.split("## State changes in the product model")[1].split("## The plan file")[0]
        check("each state change is listed; a skipped feature changes nothing (C18, S18)",
              "ft-pick: Unplanned → Planned." in part and "ft-pay: Unplanned → Planned (it had no state)." in part
              and "ft-wait" not in part and "ft-remind" not in part)
        check("the plan file is shown as made, with the business intent, the epic mark and the slices",
              f"Make `{p['plan_file']}`" in text and "bi-340" in text and "epic: <the epic's issue>" in text
              and "Slices list, each at Not Started: sl-self-booking (Self-booking)" in text)
        check("the skipped feature is named with its reason",
              "ft-wait: its ICE is not ready" in text.split("## Skipped features")[1])
        check("no Story is filed", "Make a new story" not in text and "files no Stories" in text)
        check("the brief says yes, change or stop", "**yes**" in text and "**change: <what>**" in text and "**stop**" in text)
        check("the brief holds no failure words", "fails if" not in text.lower())
        check("no clean-up of old work is shown", "Clean-up" not in text and "old work" not in text)
    with tempfile.TemporaryDirectory() as tmp:
        root = make_model(tmp, states={"ft-pay": "In progress"})
        p = paths(tmp)
        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind", "ft-pay", "ft-wait"])
        gather(root, p)
        empty_tracker(p, [
            issue(40, "Another plan's epic", "Epic", "", subs=[41]),
            issue(41, "Pick a free slot", "Feature", full_body("ft-pick")),
            issue(42, "Send a reminder", "Feature", full_body("ft-remind"), state="closed", reason="not_planned"),
            issue(43, "Pay the fee", "Feature", "Represents: ft-pay\n", labels=["work-item"])])
        code, text = brief(p)
        check("a held Feature issue is shown as held_by, never moved",
              "ft-pick: Feature issue #41" in text and "held_by: 40" in text.split("## Held by another plan's epic")[1])
        part = text.split("## Opened again")[1].split("##")[0]
        check("a closed Feature issue is shown under Opened again, with its number and its close (C17, S16)",
              "ft-remind: Feature issue #42 \"Send a reminder\", closed as not planned, opens again." in part
              and "Open Feature issue #42 \"Send a reminder\" again for ft-remind: it is closed as not planned. "
                  "No second Feature issue is filed" in text)
        check("an In progress feature keeps its state (C18)",
              "ft-pay: stays In progress." in text.split("## State changes in the product model")[1])
        check("a found Feature issue shows the sections it gains and its labels",
              "Use Feature issue #43" in text and "\"Scope of work\" and \"Context guidance\"" in text
              and "work-item" in text)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
