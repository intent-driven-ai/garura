#!/usr/bin/env python3
"""Tests for guidance_block.py — the judge gets the per-section guidance and never the gold example."""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import guidance_block as gb  # noqa: E402

PASSED, FAILED = 0, 0


def check(name, ok):
    global PASSED, FAILED
    PASSED, FAILED = PASSED + bool(ok), FAILED + (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


TEMPLATE = """# Capability Grounding Doc — TEMPLATE & CONTRACT

## Heading contract (required, in order)

```
## Per-section guidance
## Intent
```

## Per-section guidance

### Intent
Say who it serves and why.

```
## not a heading inside a fence
```

## Gold example

# Capability: Guest checkout
The secret answer.
"""

with tempfile.TemporaryDirectory() as tmp:
    src, out = os.path.join(tmp, "capability.md"), os.path.join(tmp, "guidance.md")
    with open(src, "w") as fh:
        fh.write(TEMPLATE)
    rc = gb.main(["--template", src, "--out", out])
    text = open(out).read() if os.path.exists(out) else ""
    check("the guidance block is written", rc == 0 and text.startswith("## Per-section guidance"))
    check("the block keeps its own sub-sections and fenced lines",
          "Say who it serves and why." in text and "not a heading inside a fence" in text)
    check("the gold example is left out", "Gold example" not in text and "The secret answer." not in text)
    check("a heading named inside a fence earlier does not start the block",
          text.count("## Per-section guidance") == 1 and "\n## Intent\n" not in text)
    bare, out2 = os.path.join(tmp, "bare.md"), os.path.join(tmp, "g2.md")
    with open(bare, "w") as fh:
        fh.write("# No guidance here\n\n## Gold example\nx\n")
    check("a template with no guidance block writes nothing",
          gb.main(["--template", bare, "--out", out2]) == 2 and not os.path.exists(out2))
    check("a missing template writes nothing",
          gb.main(["--template", os.path.join(tmp, "nope.md"), "--out", out2]) == 2 and not os.path.exists(out2))
    staged, out4 = os.path.join(tmp, "staged.md"), os.path.join(tmp, "g4.md")
    with open(staged, "w") as fh:
        fh.write("## Per-section guidance (directional stage)\nA\n\n## Gold example\nG\n\n"
                 "## Per-section guidance (detailed stage)\nB\n")
    t4 = open(out4).read() if gb.main(["--template", staged, "--out", out4]) == 0 else ""
    check("every stage's guidance block is kept, and no gold example", "A" in t4 and "B" in t4 and "G" not in t4)
    real = os.path.normpath(os.path.join(HERE, "..", "..", "..", "memory", "standards", "schemas",
                                         "product-os", "grounding", "capability.md"))
    if os.path.isfile(real):
        out3 = os.path.join(tmp, "g3.md")
        rc = gb.main(["--template", real, "--out", out3])
        t3 = open(out3).read() if rc == 0 else ""
        check("the real capability template gives its guidance and no gold example",
              rc == 0 and t3.startswith("## Per-section guidance") and "## Gold example" not in t3)


def test_each_stage_gets_its_own_guidance():
    """/discover-domains judges a directional capability, /discover-capabilities a detailed one (#662)."""
    real = os.path.normpath(os.path.join(HERE, "..", "..", "..", "memory", "standards", "schemas",
                                         "product-os", "grounding", "capability.md"))
    if not os.path.isfile(real):
        return
    directional, detailed = gb.cut(open(real).read(), "directional"), gb.cut(open(real).read(), "detailed")
    check("the directional judge gets the directional guidance and the agent intent",
          "Directional intent** —" in directional and "at every stage" in directional)
    check("the directional judge never gets the detailed stage's guidance",
          "Benefit hypothesis** —" not in directional and "(detailed stage)" not in directional)
    check("the detailed judge gets the detailed guidance, not the directional",
          "Benefit hypothesis** —" in detailed and "Directional intent** —" not in detailed)
    check("no stage ever gets a gold example", "Gold example" not in directional + detailed)


def test_every_copy_is_this_one():
    plays = os.path.normpath(os.path.join(HERE, "..", ".."))
    canonical = open(os.path.join(HERE, "guidance_block.py")).read()
    copies = [os.path.join(plays, p, "scripts", "guidance_block.py") for p in sorted(os.listdir(plays))
              if os.path.isfile(os.path.join(plays, p, "scripts", "guidance_block.py"))]
    check(f"every play's guidance_block.py is identical to the canonical one ({len(copies)} copies)",
          len(copies) >= 2 and all(open(c).read() == canonical for c in copies))


test_each_stage_gets_its_own_guidance()
test_every_copy_is_this_one()
print(f"\n{PASSED} passed, {FAILED} failed")
sys.exit(1 if FAILED else 0)

