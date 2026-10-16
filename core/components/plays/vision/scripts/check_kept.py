#!/usr/bin/env python3
"""check_kept.py — every existing grounding doc a run changed kept what it had (#637, C6).

Under ontology v4 a play may update a page another play wrote — raise a light domain page to
the full one, add light detail to a capability — but it must keep what was there. This diffs
the model tree against the base ref and, for every grounding doc that existed at the base and
was changed, checks that each `##` section it had is still there and not empty. A section may
grow or be reworded; it may not disappear. Lines of the `## Agent intent (ICE)` section are
checked one by one: an agent-intent line may be added to, never dropped.

Layer rule: git reads + file reads only; no gh/network.

    python3 check_kept.py --product-base <product_base> --base-ref HEAD --out <working>/kept-report.json

Prints and writes {ok, checked[], lost[]}. Exit 0 ok · 1 something was lost · 2 usage/git error.
"""
import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_grounding import ICE_SECTION, parse_sections  # noqa: E402

DOCS = ("domain.md", "capability.md", "functionality.md")


def git(root, *args):
    proc = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout


def sections(text):
    return {h: "\n".join(body).strip() for h, body in parse_sections(text)[1]}


def ice_lines(body):
    return {" ".join(l.split()) for l in body.splitlines() if l.strip().startswith(("-", "*"))}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check that changed grounding docs kept their sections.")
    ap.add_argument("--product-base", required=True)
    ap.add_argument("--base-ref", default="HEAD")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    start = args.product_base if os.path.isdir(args.product_base) else "."
    rc, top = git(start, "rev-parse", "--show-toplevel")
    if rc:
        sys.stderr.write("check_kept.py: not a git repo\n")
        return 2
    root = top.strip()
    tree = os.path.relpath(os.path.realpath(os.path.join(args.product_base, "product-os")),
                           os.path.realpath(root)).replace(os.sep, "/")
    rc, diff = git(root, "diff", "--name-status", "--no-renames", args.base_ref, "--", tree)
    if rc:
        sys.stderr.write(f"check_kept.py: git diff against {args.base_ref} failed\n")
        return 2

    checked, lost = [], []
    for line in diff.splitlines():
        parts = line.split("\t")
        if len(parts) < 2 or parts[0].strip() != "M" or os.path.basename(parts[-1]) not in DOCS:
            continue
        path = parts[-1].strip()
        rc, old = git(root, "show", f"{args.base_ref}:{path}")
        if rc:
            continue
        with open(os.path.join(root, path), encoding="utf-8") as fh:
            new = fh.read()
        was, now = sections(old), sections(new)
        checked.append(path)
        for head, body in was.items():
            if not body:
                continue
            if not now.get(head):
                lost.append({"path": path, "section": head, "what": "the section is gone or empty"})
            elif head == ICE_SECTION:
                for item in sorted(ice_lines(body) - ice_lines(now[head])):
                    lost.append({"path": path, "section": head, "what": f"dropped: {item[:80]}"})

    report = {"ok": not lost, "base_ref": args.base_ref, "checked": checked, "lost": lost}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0 if not lost else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
