#!/usr/bin/env python3
"""test_render_brief.py — the brief shows every tracker write, the plan-file change and each skipped feature (C8, C9).

    python3 test_render_brief.py
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, empty_tracker, finish, gather, make_drafts, make_model, paths,  # noqa: E402
                          read, run, set_slice, write)


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
        set_slice(root, "sl-self-booking", ["ft-pick", "ft-remind", "ft-wait"])
        gather(root, p)
        empty_tracker(p)
        code, text = brief(p)
        check("exit 0, and the brief has its sections", code == 0 and all(h in text for h in (
            "## What the run writes in the tracker", "## The plan file", "## Skipped features", "## Your answer")))
        check("a new epic is shown with its type and title",
              "Make a new epic, type Feature, no label: \"A patient books a free slot online\"" in text)
        check("each new story is shown with its text", text.count("Make a new story for") == 2
              and "Never read: health records" in text)
        check("the plan file is shown as made", f"Make `{p['plan_file']}`" in text)
        check("the skipped feature is named with its reason", "ft-wait (slice sl-self-booking)" in text
              and "not ready" in text.split("## Skipped features")[1])
        check("the brief says yes, change or stop", "**yes**" in text and "**change: <what>**" in text and "**stop**" in text)
        check("the brief holds no failure words", "fails if" not in text.lower())

        write(p["plan_file"], "id: 340\ntitle: x\nstatus: active\ntree:\n- issue: 10\n  kind: epic\n"
              "  title: Self-booking\n  represents: sl-self-booking\n  children:\n  - issue: 11\n"
              "    represents: ft-pick\n  - issue: 13\n    represents: ft-cancel\n")
        empty_tracker(p, [
            {"number": 10, "title": "Self-booking", "type": "Epic", "labels": ["work-item"], "body": ""},
            {"number": 11, "title": "Pick a free slot", "type": "Story", "body": "Text a person wrote."},
            {"number": 13, "title": "Cancel online", "type": "Story", "body": ""}])
        code, text = brief(p)
        check("a used epic shows its type change, its labels and its map",
              "Use epic #10" in text and "set its type to Feature" in text and "work-item" in text
              and "feature-to-story map" in text)
        check("a found story shows the sections it gains", "Use story #11" in text and "\"Scope of work\" and \"Context guidance\"" in text)
        check("a moved-out story is shown, and it stays open", "Move story #13 out of the plan" in text and "stays\nopen" not in text
              and "stays open in the tracker" in text)
        check("the plan file is shown as updated, with the node taken out",
              f"Update `{p['plan_file']}`" in text and "Take out the story node #13" in text)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
