#!/usr/bin/env python3
"""test_adr.py — fixture tests for adr.py (#632): number, lint (both shapes), index, overlaps,
forward pointers (both shapes, with and without a Status line), and the business-intent guard.

    python3 test_adr.py
"""
import json
import os
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import adr  # noqa: E402

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
        if os.environ.get("PYTEST_CURRENT_TEST"):
            raise AssertionError(name)


GOOD_MD = """# ADR 003 — Keep the cache in memory for now

**Status:** Accepted
**Date:** 2026-10-15
**Level:** framework
**Decided by:** Kapil · **Decided in:** #632 (a test)
**Amends:** ADR 001 — the storage section
**Affects:** `core/cache.py`, `/vision`
**ICE impact:** none — no agent intent changes
**Business intent check:** none

## Context

The cache is small.

## Decision

Keep it in memory.

## Consequences

### Positive

- Simple.

## Alternatives Considered

- **A database** — too heavy for now.
"""

OLD_MD = """# ADR 001: Store the cache on disk

**Status:** Accepted
**Date:** 2026-01-01

## Context

Text about `core/cache.py`.

## Decision

On disk.
"""

LEGACY_MD = """# ADR 002: A record with no status line

## Context

Old text about `/vision`.
"""

GOOD_YAML = {"decision": {
    "id": "dec-2", "title": "Cache sessions for an hour", "status": "proposed", "level": "capability",
    "node_ref": "cap-sessions", "reason": "Sessions are read often.",
    "alternatives": [{"name": "No cache", "why_not": "Too slow."}],
    "affects": ["capabilities/cap-sessions/capability.md"], "ice_impact": "none — no goal changes",
    "business_intent_check": "none", "metadata": {"decided_by": "/understand", "date": "2026-10-15"}}}


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def folder(tmp):
    d = os.path.join(tmp, "adr")
    os.makedirs(d)
    write(os.path.join(d, "001-cache-on-disk.md"), OLD_MD)
    write(os.path.join(d, "002-legacy.md"), LEGACY_MD)
    write(os.path.join(d, "003-cache-in-memory.md"), GOOD_MD)
    write(os.path.join(d, "SUPERSEDED-004-gone.md"), "# ADR 004: Gone\n")
    return d


def run(argv):
    from io import StringIO
    old, sys.stdout = sys.stdout, StringIO()
    try:
        code = adr.main(argv)
        out = sys.stdout.getvalue()
    finally:
        sys.stdout = old
    try:
        return code, json.loads(out)
    except ValueError:
        return code, out


def test_number_and_index():
    with tempfile.TemporaryDirectory() as tmp:
        d = folder(tmp)
        code, out = run(["number", "--dir", d])
        check("the next number counts superseded files too", code == 0 and out["next"] == "005")
        idx = os.path.join(tmp, "_index.md")
        code, _ = run(["index", "--dir", d, "--out", idx])
        text = open(idx).read()
        check("the index lists every ADR with its status",
              code == 0 and "| [001](001-cache-on-disk.md) | Store the cache on disk | Accepted |" in text
              and "(not recorded)" in text and "| Superseded |" in text)


def test_lint():
    with tempfile.TemporaryDirectory() as tmp:
        good = write(os.path.join(tmp, "003-x.md"), GOOD_MD)
        code, out = run(["lint", "--adr", good])
        check("a Markdown ADR written from the template is valid", code == 0 and out["valid"])
        for label, broken in (
                ("a missing ICE impact line", GOOD_MD.replace("**ICE impact:** none — no agent intent changes\n", "")),
                ("a bad status", GOOD_MD.replace("**Status:** Accepted", "**Status:** Maybe")),
                ("a bad business intent check", GOOD_MD.replace("**Business intent check:** none",
                                                                  "**Business intent check:** perhaps")),
                ("a missing section", GOOD_MD.replace("## Alternatives Considered\n\n- **A database** — too heavy for now.\n", "")),
                ("an accepted ADR with no one who accepted it", GOOD_MD.replace("**Decided by:** Kapil · ", "")),
                ("a bad title line", GOOD_MD.replace("# ADR 003 — ", "# Decision: "))):
            path = write(os.path.join(tmp, "bad.md"), broken)
            code, out = run(["lint", "--adr", path])
            check(f"{label} is caught", code == 2 and out["problems"])
        y = os.path.join(tmp, "dec.yaml")
        with open(y, "w") as fh:
            yaml.safe_dump(GOOD_YAML, fh)
        check("a YAML decision written from the template is valid", run(["lint", "--adr", y])[0] == 0)
        bad = yaml.safe_load(yaml.safe_dump(GOOD_YAML))
        del bad["decision"]["node_ref"]
        bad["decision"]["status"] = "accepted"
        with open(y, "w") as fh:
            yaml.safe_dump(bad, fh)
        code, out = run(["lint", "--adr", y])
        check("a YAML decision with no node and no accepter is caught",
              code == 2 and any("node_ref" in p for p in out["problems"])
              and any("accepted_by" in p for p in out["problems"]))
        check("an unreadable file exits 3", run(["lint", "--adr", os.path.join(tmp, "nope.md")])[0] == 3)


def test_overlaps():
    with tempfile.TemporaryDirectory() as tmp:
        d = folder(tmp)
        code, out = run(["overlaps", "--adr", os.path.join(d, "003-cache-in-memory.md"), "--dir", d])
        got = {c["adr"]: c for c in out["candidates"]}
        check("an ADR it names is a candidate", "001" in got and got["001"]["named_in_new"])
        check("an ADR sharing a path or play is a candidate", "002" in got and got["002"]["shared_paths"] == ["/vision"])
        check("the new ADR is not its own candidate", "003" not in got)


def test_pointer():
    with tempfile.TemporaryDirectory() as tmp:
        d = folder(tmp)
        new = os.path.join(d, "003-cache-in-memory.md")
        old = os.path.join(d, "001-cache-on-disk.md")
        code, _ = run(["pointer", "--older", old, "--newer", new, "--kind", "amended", "--what", "the storage section"])
        text = open(old).read()
        check("an amended ADR gains a forward pointer on its Status line only",
              code == 0 and "**Status:** Accepted — amended in part by [ADR 003](003-cache-in-memory.md): "
              "the storage section" in text and text.replace(text.split("\n")[2], "") ==
              OLD_MD.replace(OLD_MD.split("\n")[2], ""))
        code, out = run(["pointer", "--older", old, "--newer", new, "--kind", "amended"])
        check("pointing twice changes nothing", code == 0 and out.get("unchanged"))
        dotted = write(os.path.join(d, "005-dotted.md"), OLD_MD.replace("**Status:** Accepted",
                                                                        "**Status:** Accepted — amended by ADR 004."))
        run(["pointer", "--older", dotted, "--newer", new, "--kind", "amended"])
        check("a Status line ending in a full stop is joined cleanly",
              "amended by ADR 004; and amended in part by [ADR 003]" in open(dotted).read())
        legacy = os.path.join(d, "002-legacy.md")
        run(["pointer", "--older", legacy, "--newer", new, "--kind", "superseded"])
        text = open(legacy).read()
        check("an ADR with no Status line gains one under its title, nothing else",
              text.startswith("# ADR 002: A record with no status line\n\n**Status:** (not recorded) — "
                              "superseded by [ADR 003](003-cache-in-memory.md)"))
        check("the rest of that ADR is unchanged", text.endswith(LEGACY_MD.split("\n", 1)[1]))
        y_old, y_new = os.path.join(tmp, "old.yaml"), os.path.join(tmp, "new.yaml")
        older = yaml.safe_load(yaml.safe_dump(GOOD_YAML))
        older["decision"]["id"] = "dec-1"
        older["decision"]["status"] = "accepted"
        for p, data in ((y_old, older), (y_new, GOOD_YAML)):
            with open(p, "w") as fh:
                yaml.safe_dump(data, fh)
        run(["pointer", "--older", y_old, "--newer", y_new, "--kind", "superseded"])
        d1 = yaml.safe_load(open(y_old))["decision"]
        check("a YAML decision superseded in full gets its pointer and status",
              d1["superseded_by"] == "dec-2" and d1["status"] == "superseded" and d1["title"] == GOOD_YAML["decision"]["title"])
        check("mixing shapes is refused", run(["pointer", "--older", y_old, "--newer", new, "--kind", "amended"])[0] == 2)


def test_guard():
    with tempfile.TemporaryDirectory() as tmp:
        intents = os.path.join(tmp, "intents")
        os.makedirs(intents)
        write(os.path.join(intents, "grow-online-sales.md"), "# Grow online sales without adding sales staff\n")
        good = write(os.path.join(tmp, "003-x.md"), GOOD_MD)
        check("an ADR that changes no business intent passes",
              run(["guard", "--adr", good, "--intents-dir", intents])[0] == 0)
        kind = write(os.path.join(tmp, "k.md"), GOOD_MD.replace("**Business intent check:** none",
                                                                 "**Business intent check:** kind — the Business Intent kind"))
        check("an ADR that changes only the Business Intent kind passes",
              run(["guard", "--adr", kind, "--intents-dir", intents])[0] == 0)
        inst = write(os.path.join(tmp, "i.md"), GOOD_MD.replace("**Business intent check:** none",
                                                                 "**Business intent check:** instance — grow-online-sales"))
        code, out = run(["guard", "--adr", inst, "--intents-dir", intents])
        check("an ADR declaring it changes a person's intent goes to the person (exit 4)", code == 4)
        hidden = write(os.path.join(tmp, "h.md"), GOOD_MD.replace("`core/cache.py`", "`product-os/intents/grow-online-sales.md`"))
        code, out = run(["guard", "--adr", hidden, "--intents-dir", intents])
        check("an ADR that touches an intent but declares none is caught and goes to the person",
              code == 4 and "problem" in out)
        named = write(os.path.join(tmp, "n.md"), GOOD_MD.replace("Keep it in memory.",
                                                                  "Keep it in memory, and drop Grow online sales without adding sales staff."))
        check("an ADR that names an intent's title goes to the person",
              run(["guard", "--adr", named, "--intents-dir", intents])[0] == 4)
        missing = write(os.path.join(tmp, "m.md"), GOOD_MD.replace("**Business intent check:** none\n", ""))
        check("an ADR with no business intent check is a problem (exit 2)",
              run(["guard", "--adr", missing])[0] == 2)
        y = os.path.join(tmp, "dec.yaml")
        bad = yaml.safe_load(yaml.safe_dump(GOOD_YAML))
        bad["decision"]["affects"].append("product-os/intents/grow-online-sales.md")
        with open(y, "w") as fh:
            yaml.safe_dump(bad, fh)
        check("a YAML decision touching an intent page goes to the person",
              run(["guard", "--adr", y, "--intents-dir", intents])[0] == 4)


def test_accept():
    with tempfile.TemporaryDirectory() as tmp:
        prop = GOOD_MD.replace("**Status:** Accepted", "**Status:** Proposed").replace("**Decided by:** Kapil · ", "")
        path = write(os.path.join(tmp, "003-x.md"), prop)
        code, _ = run(["accept", "--adr", path, "--by", "Kapil", "--date", "2026-10-16"])
        text = open(path).read()
        check("a proposed ADR is accepted, naming the person and the date",
              code == 0 and "**Status:** Accepted" in text and "**Decided by:** Kapil" in text
              and "**Date:** 2026-10-16" in text and run(["lint", "--adr", path])[0] == 0)
        check("an ADR already accepted is not accepted again",
              run(["accept", "--adr", path, "--by", "Kapil", "--date", "2026-10-16"])[0] == 2)
        path = write(os.path.join(tmp, "004-y.md"), prop)
        check("no person, no acceptance", run(["accept", "--adr", path, "--by", " ", "--date", "x"])[0] == 2)
        y = os.path.join(tmp, "dec.yaml")
        with open(y, "w") as fh:
            yaml.safe_dump(GOOD_YAML, fh)
        run(["accept", "--adr", y, "--by", "Kapil", "--date", "2026-10-16"])
        d = yaml.safe_load(open(y))["decision"]
        check("a proposed YAML decision is accepted with its accepter",
              d["status"] == "accepted" and d["metadata"]["accepted_by"] == "Kapil"
              and d["metadata"]["decided_by"] == "/understand")


def main():
    for test in (test_number_and_index, test_lint, test_overlaps, test_pointer, test_guard, test_accept):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
