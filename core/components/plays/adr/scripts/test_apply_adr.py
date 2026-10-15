#!/usr/bin/env python3
"""test_apply_adr.py — fixture tests for /adr's apply step (#632), one group per scenario:
accept by hand with pointers and index (S1, S6), the business-intent stop (S2), a product
decision (S3), proposed inside a drive and accepted later (S4), reject (S5), and the refusals.

    python3 test_apply_adr.py
"""
import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stdout

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_adr as ap  # noqa: E402
import check_adr_scope as cs  # noqa: E402

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


OLD_1 = "# ADR 001: Store the cache on disk\n\n**Status:** Accepted\n**Date:** 2026-01-01\n\n## Context\n\nText.\n"
OLD_2 = "# ADR 002: Retry three times\n\n## Context\n\nOld text.\n"

DRAFT = """# ADR 003 — Keep the cache in memory for now

**Status:** Proposed
**Date:** 2026-10-15
**Level:** framework
**Decided in:** #632 (a test)
**Supersedes:** ADR 002 (in full)
**Amends:** ADR 001 — the storage section
**Affects:** `core/cache.py`
**ICE impact:** none — no agent intent changes
**Business intent check:** none

## Context

The cache is small.

## Decision

Keep it in memory.

## Consequences

- Simple.

## Alternatives Considered

- **A database** — too heavy for now.
"""

CONTEXT = {"shape": "markdown", "number": "003",
           "supersedes": [{"adr": "002", "part": "full"}],
           "amends": [{"adr": "001", "part": "the storage section"}]}

PRODUCT = {"decision": {
    "id": "dec-2", "title": "Cache sessions for an hour", "status": "proposed", "level": "capability",
    "node_ref": "cap-sessions", "reason": "Sessions are read often.",
    "alternatives": [{"name": "No cache", "why_not": "Too slow."}],
    "amends": [{"id": "dec-1", "part": "the cache length"}],
    "affects": ["capabilities/cap-sessions/capability.md"], "ice_impact": "none — no goal changes",
    "business_intent_check": "none", "consequences": {"positive": ["Faster reads."], "negative": ["Stale for an hour."]},
    "metadata": {"decided_by": "/understand", "date": "2026-10-15", "decided_in": "#632"}}}


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def dump(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, sort_keys=False)
    return path


def setup(tmp, draft=DRAFT, context=CONTEXT):
    d = os.path.join(tmp, "docs", "adr")
    write(os.path.join(d, "001-cache-on-disk.md"), OLD_1)
    write(os.path.join(d, "002-retry.md"), OLD_2)
    w = os.path.join(tmp, "work")
    paths = {"dir": d, "work": w, "draft": write(os.path.join(w, "adr-draft.md"), draft),
             "context": dump(os.path.join(w, "adr-context.yaml"), context),
             "target": os.path.join(d, "003-cache-in-memory.md"), "index": os.path.join(d, "_index.md")}
    return paths


def accept_file(w, verdict="accept", by="person", reply="yes, accept it", name="Kapil"):
    return dump(os.path.join(w, "decision.yaml"),
                {"decision": {"verdict": verdict, "by": by, "accepted_by": name, "reply": reply}})


def run(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = ap.main(argv)
    return code


def manifest(w):
    with open(os.path.join(w, "adr-manifest.json")) as fh:
        return json.load(fh)


def base(p, extra):
    return ["--draft", p["draft"], "--context", p["context"], "--target", p["target"], "--adr-dir", p["dir"],
            "--index", p["index"], "--date", "2026-10-16", "--working", p["work"]] + extra


def test_accept_by_hand():
    with tempfile.TemporaryDirectory() as tmp:
        p = setup(tmp)
        code = run(base(p, ["--decision", accept_file(p["work"])]))
        m = manifest(p["work"])
        check("S1: accepted by hand — decided, linted, linked", code == 0 and m["decided"] and m["lint_ok"]
              and m["linked"] and m["status"] == "accepted")
        text = open(p["target"]).read()
        check("the new ADR reads Accepted with the person's name", "**Status:** Accepted" in text
              and "**Decided by:** Kapil" in text)
        one = open(os.path.join(p["dir"], "001-cache-on-disk.md")).read()
        check("an amended ADR points forward, and only its Status line changed",
              "amended in part by [ADR 003](003-cache-in-memory.md): the storage section" in one
              and one.split("\n", 3)[3] == OLD_1.split("\n", 3)[3])
        two = open(os.path.join(p["dir"], "002-retry.md")).read()
        check("a superseded ADR with no Status line gains one pointing forward",
              "**Status:** (not recorded) — superseded by [ADR 003](003-cache-in-memory.md)" in two)
        idx = open(p["index"]).read()
        check("S6: the index lists the new ADR as Accepted, and every ADR",
              "| [003](003-cache-in-memory.md) |" in idx and "| Accepted |" in idx.split("[003]")[1].split("\n")[0]
              and "[001]" in idx and "[002]" in idx and m.get("index_ok"))
        check("a record is never overwritten", run(base(p, ["--decision", accept_file(p["work"])])) == 2)


def test_business_intent_stop():
    with tempfile.TemporaryDirectory() as tmp:
        draft = DRAFT.replace("**Business intent check:** none", "**Business intent check:** instance — grow-sales")
        p = setup(tmp, draft=draft)
        code = run(base(p, ["--decision", accept_file(p["work"])]))
        m = manifest(p["work"])
        check("S2: a decision that changes a business intent stops before writing (exit 4)",
              code == 4 and m.get("business_intent") and not os.path.exists(p["target"]) and not m["decided"])
        check("no older ADR changed", open(os.path.join(p["dir"], "001-cache-on-disk.md")).read() == OLD_1)


def test_product_decision():
    with tempfile.TemporaryDirectory() as tmp:
        node = os.path.join(tmp, "product-os", "capabilities", "cap-sessions", "decisions")
        older = dump(os.path.join(node, "dec-1.yaml"), {"decision": dict(PRODUCT["decision"], id="dec-1",
                                                                            status="accepted", amends=[])})
        w = os.path.join(tmp, "work")
        draft = dump(os.path.join(w, "adr-draft.yaml"), PRODUCT)
        ctx = dump(os.path.join(w, "adr-context.yaml"), {"shape": "yaml", "amends": [{"id": "dec-1", "part": "the cache length"}]})
        target = os.path.join(node, "dec-2.yaml")
        code = run(["--draft", draft, "--context", ctx, "--target", target, "--adr-dir", node,
                    "--decision", accept_file(w), "--date", "2026-10-16", "--working", w])
        d = yaml.safe_load(open(target))["decision"]
        check("S3: a product decision is written for its node, accepted by the person",
              code == 0 and d["status"] == "accepted" and d["metadata"]["accepted_by"] == "Kapil"
              and d["node_ref"] == "cap-sessions")
        check("the older product decision gets its forward pointer",
              yaml.safe_load(open(older))["decision"].get("amended_by") == ["dec-2"])


def test_drive_then_accept_later():
    with tempfile.TemporaryDirectory() as tmp:
        p = setup(tmp)
        code = run(base(p, ["--proposed"]))
        m = manifest(p["work"])
        check("S4: inside a drive it is saved as proposed, with no stop and no pointers",
              code == 0 and m["status"] == "proposed" and m["pointers_deferred"] and m["decided"]
              and "**Status:** Proposed" in open(p["target"]).read()
              and open(os.path.join(p["dir"], "001-cache-on-disk.md")).read() == OLD_1)
        code = run(["--accept-existing", p["target"], "--by", "Kapil", "--adr-dir", p["dir"], "--index", p["index"],
                    "--date", "2026-10-17", "--working", os.path.join(tmp, "later")])
        m = manifest(os.path.join(tmp, "later"))
        check("a supersede 'in full' read back from the ADR is written as a full supersede",
              "**Status:** (not recorded) — superseded by [ADR 003](003-cache-in-memory.md)\n" in
              open(os.path.join(p["dir"], "002-retry.md")).read()
              or "Superseded by [ADR 003]" in open(os.path.join(p["dir"], "002-retry.md")).read())
        check("accepted later, its pointers come from its own Supersedes and Amends lines",
              code == 0 and m["linked"] and sorted(m["pointers_written"]) == ["001-cache-on-disk.md", "002-retry.md"]
              and "amended in part by [ADR 003]" in open(os.path.join(p["dir"], "001-cache-on-disk.md")).read())
        check("accepting later needs a person", run(["--accept-existing", p["target"], "--by", " ", "--date", "x",
                                                     "--working", os.path.join(tmp, "x")]) == 2)


def test_reject_and_refusals():
    with tempfile.TemporaryDirectory() as tmp:
        p = setup(tmp)
        code = run(base(p, ["--decision", accept_file(p["work"], verdict="reject")]))
        check("S5: a rejected ADR writes nothing (exit 5)", code == 5 and not os.path.exists(p["target"])
              and manifest(p["work"]).get("rejected") and open(os.path.join(p["dir"], "001-cache-on-disk.md")).read() == OLD_1)
        check("a decision not by a person is refused", run(base(p, ["--decision", accept_file(p["work"], by="agent")])) == 2
              and not os.path.exists(p["target"]))
        check("an empty reply is refused", run(base(p, ["--decision", accept_file(p["work"], reply="")])) == 2)
        check("both modes at once are refused", run(base(p, ["--decision", accept_file(p["work"]), "--proposed"])) == 2)
        bad = setup(os.path.join(tmp, "b"), draft=DRAFT.replace("## Alternatives Considered\n\n- **A database** — too heavy for now.\n", ""))
        check("a draft off the template is refused before anything is written",
              run(base(bad, ["--decision", accept_file(bad["work"])])) == 2 and not os.path.exists(bad["target"]))


def test_scope():
    with tempfile.TemporaryDirectory() as tmp:
        before = write(os.path.join(tmp, "b.txt"), " M docs/other.md\n")
        after = write(os.path.join(tmp, "a.txt"), " M docs/other.md\n?? docs/adr/003-x.md\n M docs/adr/001-y.md\n"
                                                    " M docs/adr/_index.md\n?? .garura/project/issues/632/context/a.json\n")
        args = ["--before", before, "--after", after, "--allow", "docs/adr/003-x.md", "--allow", "docs/adr/001-y.md",
                "--allow", "docs/adr/_index.md"]
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cs.main(args)
        check("only the ADR, its pointers, the index and the run's records changed: ok", code == 0)
        bad = write(os.path.join(tmp, "c.txt"), open(after).read() + " M core/components/agents/x.md\n")
        with redirect_stdout(io.StringIO()):
            code = cs.main(["--before", before, "--after", bad, "--allow", "docs/adr/*"])
        check("any other change is a violation", code == 1)
        dirty = write(os.path.join(tmp, "docs-other.md"), "first\n")
        before2 = write(os.path.join(tmp, "b2.txt"), f" M {dirty}\n")
        hashes = os.path.join(tmp, "h.json")
        with redirect_stdout(io.StringIO()):
            cs.main(["--snapshot", "--before", before2, "--out", hashes])
        after2 = write(os.path.join(tmp, "a2.txt"), f" M {dirty}\n")
        with redirect_stdout(io.StringIO()):
            code = cs.main(["--before", before2, "--after", after2, "--before-hashes", hashes])
        check("a file already changed before the run and untouched since is fine", code == 0)
        write(dirty, "changed again inside the run\n")
        with redirect_stdout(io.StringIO()):
            code = cs.main(["--before", before2, "--after", after2, "--before-hashes", hashes])
        check("a file already changed before the run and changed again is caught", code == 1)


def test_nothing_half_written():
    with tempfile.TemporaryDirectory() as tmp:
        ctx = dict(CONTEXT, amends=[{"adr": "009", "part": "a part"}])
        p = setup(tmp, context=ctx)
        code = run(base(p, ["--decision", accept_file(p["work"])]))
        check("an older ADR that does not exist stops the run before anything is written",
              code == 2 and not os.path.exists(p["target"]) and "not found" in str(manifest(p["work"])["problem"]))
        p2 = setup(os.path.join(tmp, "a"), draft=DRAFT.replace("**Status:** Proposed", "**Status:** Accepted\n**Decided by:** Someone"))
        for mode in (["--proposed"], ["--decision", accept_file(p2["work"])]):
            code = run(base(p2, mode))
            check(f"a draft already marked Accepted is refused ({mode[0]}), nothing written",
                  code == 2 and not os.path.exists(p2["target"]))
        p3 = setup(os.path.join(tmp, "n"))
        p3["target"] = os.path.join(p3["dir"], "004-cache-in-memory.md")
        check("a number that does not match the file name is refused",
              run(base(p3, ["--proposed"])) == 2 and not os.path.exists(p3["target"]))
        p4 = setup(os.path.join(tmp, "t"))
        write(os.path.join(p4["dir"], "003-someone-else.md"), "# ADR 003 — Taken\n")
        check("a number already taken by another file is refused", run(base(p4, ["--proposed"])) == 2
              and not os.path.exists(p4["target"]))


def test_accept_later_safely():
    with tempfile.TemporaryDirectory() as tmp:
        p = setup(tmp)
        run(base(p, ["--proposed"]))
        os.remove(os.path.join(p["dir"], "002-retry.md"))
        code = run(["--accept-existing", p["target"], "--by", "Kapil", "--adr-dir", p["dir"], "--index", p["index"],
                    "--date", "2026-10-17", "--working", os.path.join(tmp, "later")])
        check("accepting later with a missing older ADR stops before accepting",
              code == 2 and "**Status:** Proposed" in open(p["target"]).read()
              and open(os.path.join(p["dir"], "001-cache-on-disk.md")).read() == OLD_1)
        none = DRAFT.replace("**Supersedes:** ADR 002 (in full)", "**Supersedes:** none — unlike ADR 002, nothing")
        q = setup(os.path.join(tmp, "q"), draft=none, context=dict(CONTEXT, supersedes=[]))
        run(base(q, ["--proposed"]))
        run(["--accept-existing", q["target"], "--by", "Kapil", "--adr-dir", q["dir"], "--index", q["index"],
             "--date", "2026-10-17", "--working", os.path.join(tmp, "q2")])
        check("a Supersedes line that reads 'none — unlike ADR 002' supersedes nothing",
              open(os.path.join(q["dir"], "002-retry.md")).read() == OLD_2)


def test_round_two():
    with tempfile.TemporaryDirectory() as tmp:
        p = setup(tmp)
        write(os.path.join(p["dir"], "002-retry.md"),
              OLD_2.replace("# ADR 002: Retry three times\n", "# ADR 002: Retry three times\n\n"
                            "**Status:** Superseded by [ADR 005](005-x.md)\n"))
        code = run(base(p, ["--decision", accept_file(p["work"])]))
        check("an older ADR already superseded in full by another stops the run before writing",
              code == 2 and not os.path.exists(p["target"]) and "already superseded" in str(manifest(p["work"])["problem"]))
        q = setup(os.path.join(tmp, "q"))
        run(base(q, ["--proposed"]))
        write(os.path.join(q["dir"], "002-retry.md"),
              OLD_2.replace("# ADR 002: Retry three times\n", "# ADR 002: Retry three times\n\n"
                            "**Status:** Superseded by [ADR 005](005-x.md)\n"))
        code = run(["--accept-existing", q["target"], "--by", "Kapil", "--adr-dir", q["dir"], "--index", q["index"],
                    "--date", "2026-10-17", "--working", os.path.join(tmp, "q2")])
        check("accepting later with such an older ADR stops before accepting",
              code == 2 and "**Status:** Proposed" in open(q["target"]).read())
        r = os.path.join(tmp, "r")
        w = os.path.join(r, "work")
        draft = write(os.path.join(w, "adr-draft.md"), DRAFT.replace("**Supersedes:** ADR 002 (in full)\n", "")
                      .replace("**Amends:** ADR 001 — the storage section\n", ""))
        ctx = dump(os.path.join(w, "adr-context.yaml"), {"shape": "markdown", "number": "003"})
        new_dir = os.path.join(r, "newdocs", "adr")
        code = run(["--draft", draft, "--context", ctx, "--target", os.path.join(new_dir, "003-first.md"),
                    "--adr-dir", new_dir, "--index", os.path.join(new_dir, "_index.md"),
                    "--decision", accept_file(w), "--date", "2026-10-17", "--working", w])
        check("the first ADR in a project with no ADR folder creates it, and its index",
              code == 0 and os.path.isfile(os.path.join(new_dir, "003-first.md"))
              and "[003](003-first.md)" in open(os.path.join(new_dir, "_index.md")).read())
        s4 = setup(os.path.join(tmp, "s4"), draft=DRAFT.replace("**Business intent check:** none",
                                                                 "**Business intent check:** instance — grow"))
        run(base(s4, ["--decision", accept_file(s4["work"])]))
        m = manifest(s4["work"])
        check("a business-intent stop still records that the lint passed and what the guard said",
              m["lint_ok"] and m.get("guard", {}).get("declared") == "instance" and m.get("business_intent"))
        s5 = setup(os.path.join(tmp, "s5"))
        run(base(s5, ["--decision", accept_file(s5["work"], verdict="reject")]))
        m = manifest(s5["work"])
        check("a reject still records that the lint passed", m["lint_ok"] and m.get("rejected"))
        bad = setup(os.path.join(tmp, "bad"))
        with open(bad["context"], "w") as fh:
            fh.write("- not\n- a mapping\n")
        check("a context of the wrong shape exits 3 and writes nothing",
              run(base(bad, ["--proposed"])) == 3 and not os.path.exists(bad["target"]))


def test_copy_in_sync():
    skill = os.path.join(HERE, "..", "..", "..", "skills", "author-adr", "scripts", "adr.py")
    if os.path.isfile(skill):
        check("the play's adr.py is the author-adr skill's adr.py, unchanged",
              open(skill, "rb").read() == open(os.path.join(HERE, "adr.py"), "rb").read())


def main():
    for test in (test_accept_by_hand, test_business_intent_stop, test_product_decision,
                 test_drive_then_accept_later, test_reject_and_refusals, test_scope,
                 test_nothing_half_written, test_accept_later_safely, test_round_two, test_copy_in_sync):
        print(test.__name__)
        test()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
