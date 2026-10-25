#!/usr/bin/env python3
"""test_gather_plan.py — gather_plan.py finds the slices of an intent and writes clean ICE copies (C2, C5, C9).

    python3 test_gather_plan.py
"""
import glob
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_support import (check, finish, gather, make_model, paths, read, read_json,  # noqa: E402
                          set_slice, write, FAILS)


def main():
    print("gather_plan.py")
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp), paths(tmp)
        code, out, _ = gather(root, p)
        g = read_json(p["gather"])
        check("exit 0 with one slice", code == 0 and out["ok"] and len(g["slices"]) == 1)
        check("the plan id is the intent's number and the plan file is <plans>/<id>.yaml",
              g["plan_id"] == "340" and g["plan_file"] == os.path.join(p["plans"], "340.yaml"))
        check("the intent's title is read from its page",
              g["intent_title"] == "Patients book their own appointments online")
        sl = g["slices"][0]
        check("the slice carries its name and outcome from its record",
              sl["name"] == "Self-booking" and sl["outcome"].startswith("A patient books"))
        check("the features keep the build order", [f["id"] for f in sl["features"]] == ["ft-pick", "ft-remind", "ft-pay"])
        check("each feature names its capability and its two ICE pages",
              sl["features"][2]["capability"] == "cap-payment" and len(sl["features"][2]["ice_pages"]) == 2)
        check("every feature is ready", all(f["ready"] for f in sl["features"]))
        copies = sorted(glob.glob(os.path.join(p["working"], "ice", "*.md")))
        check("one clean copy for each ready feature", [os.path.basename(c) for c in copies]
              == ["ft-pay.md", "ft-pick.md", "ft-remind.md"])
        text = read(os.path.join(p["working"], "ice", "ft-pick.md"))
        check("the clean copy holds both ICE", "Feature ICE — ft-pick" in text and "Capability ICE — cap-booking" in text
              and "- Goal: Pick a free slot works for the patient." in text and "- Limit:" in text)
        check("the clean copy holds no failure line, no wrapped part of it, and not the words",
              all("fails if" not in read(c).lower() and "The line goes on here." not in read(c) for c in copies)
              and not any(FAILS[k] in read(c) for c in copies for k in FAILS))

        si = read(os.path.join(p["working"], "skill-input.json"))
        sij = read_json(os.path.join(p["working"], "skill-input.json"))
        check("skill-input.json names each ready feature and its clean copy, and no ICE page",
              [f["id"] for f in sij["slices"][0]["features"]] == ["ft-pick", "ft-remind", "ft-pay"]
              and all(f["clean_ice"].endswith(f"ice/{f['id']}.md") for f in sij["slices"][0]["features"])
              and "feature.md" not in si and "capability.md" not in si and "ice_pages" not in si)
        check("the clean copy names no ICE page", not any("feature.md" in read(c) or "capability.md" in read(c)
                                                          for c in copies))
        page = os.path.join(root, "clinic", "payment", "ft-pay", "feature.md")
        write(page, read(page).replace("- Context:", "- Fails if:\n  - the fee is taken twice\n"
                                       "    and the patient is not told\n  - no receipt is sent\n- Context:"))
        gather(root, p)
        text = read(os.path.join(p["working"], "ice", "ft-pay.md"))
        check("a nested block: no child line of it reaches the clean copy",
              "taken twice" not in text and "not told" not in text and "receipt" not in text
              and "- Context:" in text and "- Limit:" in text)

        set_slice(root, "sl-self-booking", ["ft-pick", "ft-wait"])
        code, _, _ = gather(root, p)
        g = read_json(p["gather"])
        wait = g["slices"][0]["features"][1]
        check("a feature whose ICE is not ready is ready false, with a reason",
              code == 0 and wait["ready"] is False and "not ready" in wait["reason"] and wait["clean_ice"] is None)
        check("skill-input.json leaves out a feature that is not ready",
              [f["id"] for f in read_json(os.path.join(p["working"], "skill-input.json"))["slices"][0]["features"]]
              == ["ft-pick"])
        check("no clean copy for it, and old copies of features not ready now are gone",
              sorted(os.path.basename(c) for c in glob.glob(os.path.join(p["working"], "ice", "*.md"))) == ["ft-pick.md"])

        page = os.path.join(root, "clinic", "booking", "ft-pick", "feature.md")
        write(page, read(page).split("## Agent intent (ICE)")[0])
        gather(root, p)
        pick = read_json(p["gather"])["slices"][0]["features"][0]
        check("a feature page with no ICE is not ready", pick["ready"] is False and "has no lines" in pick["reason"])

        code, out, _ = gather(root, p, intent="bi-341")
        check("no slice serves the intent: exit 2", code == 2 and out["ok"] is False)
        code, _, _ = gather(root, p, intent="340")
        check("an intent not of the form bi-<n>: exit 2", code == 2)
    with tempfile.TemporaryDirectory() as tmp:
        extra = [{"id": "sl-cancel", "slug": "cancel-online", "feature_refs": ["ft-cancel"],
                  "intents": ["bi-340"], "vertical": "the booking page"}]
        root, p = make_model(tmp, extra_slices=extra), paths(tmp)
        gather(root, p)
        g = read_json(p["gather"])
        check("every slice that serves the intent, in spine order",
              [s["id"] for s in g["slices"]] == ["sl-self-booking", "sl-cancel"])
    with tempfile.TemporaryDirectory() as tmp:
        root, p = make_model(tmp, features=("ft-pick",)), paths(tmp)
        import yaml
        spine = yaml.safe_load(read(os.path.join(root, "_spine.yaml")))
        ice = ("# ICE\n\n## Intent\n- **Goal:** a patient picks a slot.\n- **Fails if:** two patients get one slot.\n\n"
               "## Context\n- **Persona:** the patient.\n\n## Expectation\n- **Scenario:** a slot is booked.\n")
        spine["ices"] = [{"id": "ice-pick", "for": "ft-pick", "doc": "ices/pick.md"},
                         {"id": "ice-booking", "for": "cap-booking", "doc": "ices/booking.md"}]
        write(os.path.join(root, "_spine.yaml"), spine)
        write(os.path.join(root, "ices", "pick.md"), ice)
        write(os.path.join(root, "ices", "booking.md"), ice)
        code, _, _ = gather(root, p)
        f = read_json(p["gather"])["slices"][0]["features"][0]
        text = read(os.path.join(p["working"], "ice", "ft-pick.md"))
        check("a spine with an ICE list: the ice.md pages are read, three parts each",
              code == 0 and f["ready"] and f["ice_pages"][0].endswith("ices/pick.md")
              and "### Intent" in text and "### Expectation" in text and "Goal" in text)
        check("and their failure lines are taken out", "fails if" not in text.lower() and "two patients" not in text)
    return finish()


if __name__ == "__main__":
    sys.exit(main())
