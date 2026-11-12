#!/usr/bin/env python3
"""test_render_brief.py — the brief shows every tracker write, the clean-up, the features left out, the plan-file change and each skipped feature (C8, C9, C15, C16).

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
        root, p = make_model(tmp), paths(tmp)
        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind", "ft-pay", "ft-wait"])
        gather(root, p)
        empty_tracker(p, [
            issue(5, "Old epic", "Epic", "", subs=[6]),
            issue(6, "Pick a free slot", "Story", "Represents: ft-pick"),
            issue(7, "Send a reminder", "Story", "", state="closed", reason="completed")])
        code, text = brief(p)
        check("exit 0, and the brief has its sections", code == 0 and all(h in text for h in (
            "## What the run writes in the tracker", "### The plan's epic", "### The Feature issues",
            "## Held by another plan's epic", "## Left out: built", "## Not planned, left out", "## The plan file",
            "## Skipped features", "## Your answer")))
        check("one new epic is shown with its type and title, standing for the plan",
              "Make a new epic, type Epic, no label: \"A patient books a free slot online\"" in text
              and "stands for the plan" in text)
        check("a new Feature issue is shown with its type, its Represents line and its text",
              "File a new Feature issue for ft-pay, type Feature, no label, a sub-issue of the epic, with the "
              "line \"Represents: ft-pay\"" in text and "Never read: health records" in text)
        check("an old open story moves inside the new Feature issue, with the parent it leaves (S13)",
              "Story #6 \"Pick a free slot\": it leaves its parent #5 \"Old epic\"" in text)
        check("finished old work gives a Feature issue filed closed, and the feature is left out (S14)",
              "File a Feature issue for ft-remind" in text and "close it as completed" in text
              and "ft-remind: a Feature issue is filed closed as completed" in text.split("## Left out: built")[1])
        check("the plan file is shown as made, with the business intent, the epic mark and the slices",
              f"Make `{p['plan_file']}`" in text and "bi-340" in text and "epic: <the epic's issue>" in text
              and "Slices list, each at Not Started: sl-self-booking (Self-booking)" in text)
        check("the skipped feature is named with its reason",
              "ft-wait: its ICE is not ready" in text.split("## Skipped features")[1])
        check("no Story is filed", "Make a new story" not in text and "files no Stories" in text)
        check("the brief says yes, change or stop", "**yes**" in text and "**change: <what>**" in text and "**stop**" in text)
        check("the brief holds no failure words", "fails if" not in text.lower())

        empty_tracker(p, [
            issue(40, "Another plan's epic", "Epic", "", subs=[41]),
            issue(41, "Pick a free slot", "Feature", full_body("ft-pick")),
            issue(42, "Send a reminder", "Feature", full_body("ft-remind"), state="closed", reason="completed"),
            issue(43, "Pay the fee", "Feature", "Represents: ft-pay\n", labels=["work-item"]),
            issue(44, "Join the waiting list", "Feature", full_body("ft-wait"), state="closed",
                  reason="not_planned")])
        code, text = brief(p)
        check("a held Feature issue is shown as held_by, never moved",
              "ft-pick: Feature issue #41" in text and "held_by: 40" in text.split("## Held by another plan's epic")[1])
        check("a built feature is named as left out (C16)",
              "ft-remind: built: its Feature issue #42 is closed as completed" in text)
        part = text.split("## Not planned, left out")[1].split("## The plan file")[0]
        check("a not-planned feature is named under its own heading, with its issue number, and stays as it is",
              "ft-wait: its Feature issue #44" in part and "stays as it is" in part
              and "ft-wait: its ICE is not ready" not in text)
        check("a found Feature issue shows the sections it gains and its labels",
              "Use Feature issue #43" in text and "\"Scope of work\" and \"Context guidance\"" in text
              and "work-item" in text)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
