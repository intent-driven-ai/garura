"""Make the copies of the four thin ICE drafts without their Thin line and the blank line after it.

Run from the repo root. Writes only under this write folder's approved/ folder. Each copy is
checked to be the draft's bytes after its first two lines, with no Thin line left.
"""
import os
import re
import sys

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
DRAFTS = ".garura/project/issues/1021/context/bi-8-capability-1/drafts/product-os/software-delivery-planning/ship-every-change"
THIN = re.compile(rb"^\s*(?:>\s*)?\**Thin(?: ICE)?\**\s*:", re.I)
FEATURES = ["fn-land-plan-with-evidence", "fn-land-several-issues", "fn-scan-every-push", "fn-keep-docs-in-step"]

for fn in FEATURES:
    src = os.path.join(DRAFTS, fn, "ice.md")
    data = open(src, "rb").read()
    first, blank, rest = data.split(b"\n", 2)
    if not THIN.match(first) or blank != b"":
        sys.exit(f"{src}: does not start with a Thin line and a blank line")
    if any(THIN.match(l) for l in rest.split(b"\n")):
        sys.exit(f"{src}: holds a second Thin line")
    dst = os.path.join(HERE, "approved", fn, "ice.md")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "wb") as f:
        f.write(rest)
    assert open(dst, "rb").read() == data[len(first) + 2:]
    print(dst, len(rest))
