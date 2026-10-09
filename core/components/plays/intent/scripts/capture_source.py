#!/usr/bin/env python3
"""capture_source.py — keep a Source exactly as it was when read (/intent, #612).

A Source is anything that explains a business intent (ontology v2): a prototype (a file or
a deployed site), a document, or a plain statement. This script takes its snapshot into the
run's evidence folder, so it outlives the link or the file, and writes the source manifest:

  site       (http/https)    full-page screenshot(s) + the page HTML, via a headless browser
  file       (.html/.htm)    a copy of the file + a rendered screenshot
  document   (any other file) a copy of the file
  project    (a folder)      a copy of its top-level written docs (README, SPEC, *.md, *.txt);
                             the play runs the project and captures the running app as a
                             second, `site` source
  statement  (--statement)   the exact text, byte for byte

The plain-words "what it shows" is judgment and is filled in later by the play; this script
only keeps and records. No git, no LLM. Exit 0 on success, 2 when the source cannot be read
or captured (F1/F6) — the reason is printed and written to the manifest.

    python3 capture_source.py --source <path|url> | --statement <file> \
        --out-dir <evidence folder>/source --given-by "<git user>" \
        --manifest <working>/source-manifest.json [--also <url> ...] [--click <label> ...]
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import shutil
import sys

HTML_EXT = {".html", ".htm"}
DOC_EXT = {".md", ".txt"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def keep_view(page, out_dir, name):
    """Save the page as it is now: a full-page picture and its visible text."""
    page.screenshot(path=os.path.join(out_dir, f"{name}.png"), full_page=True)
    with open(os.path.join(out_dir, f"{name}.txt"), "w", encoding="utf-8") as fh:
        fh.write(page.inner_text("body"))
    return [f"{name}.png", f"{name}.txt"]


def screenshot(urls, out_dir, html_out=None, clicks=()):
    """Full-page screenshots of each url, then of the first url after clicking each named
    control in turn (tabs or buttons the app switches views with). Each view also keeps its
    visible text beside its picture (`screen-NN….txt`), so every view can be read, not only
    seen. Returns file names. Raises on failure — a named control that cannot be found is a
    failure, not a skip."""
    from playwright.sync_api import sync_playwright  # imported here: only sites need it
    shots = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        for i, url in enumerate(urls, start=1):
            page.goto(url, wait_until="networkidle", timeout=30000)
            name = f"screen-{i:02d}"
            shots += keep_view(page, out_dir, name)
            if i == 1 and html_out:
                with open(os.path.join(out_dir, html_out), "w", encoding="utf-8") as fh:
                    fh.write(page.content())
        if clicks:
            page.goto(urls[0], wait_until="networkidle", timeout=30000)
            for label in clicks:
                page.get_by_text(label, exact=True).first.click(timeout=10000)
                page.wait_for_load_state("networkidle")
                n = len(shots) // 2 + 1
                name = f"screen-{n:02d}-{''.join(c if c.isalnum() else '-' for c in label.lower())}"
                shots += keep_view(page, out_dir, name)
        browser.close()
    return shots


def main(argv=None):
    ap = argparse.ArgumentParser(description="Snapshot a Source for /intent.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--source", help="a file path or an http(s) link")
    src.add_argument("--statement", help="a file holding the person's statement, kept byte for byte")
    ap.add_argument("--also", action="append", default=[], help="more pages of the same site to capture")
    ap.add_argument("--click", action="append", default=[],
                    help="a tab or button label to click on the first page, then capture (repeatable)")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--given-by", required=True, help="the git user running the play")
    ap.add_argument("--manifest", required=True)
    args = ap.parse_args(argv)

    os.makedirs(args.out_dir, exist_ok=True)
    manifest = {"snapshot_saved": False, "kind": None, "read_on": datetime.date.today().isoformat(),
                "given_by": args.given_by, "snapshot_dir": args.out_dir, "files": [], "problem": None}

    def fail(reason):
        manifest["problem"] = reason
        with open(args.manifest, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2)
        print(json.dumps(manifest, indent=2))
        return 2

    if not args.given_by.strip():
        return fail("given-by is empty — it must be the git user running the play")

    try:
        if args.statement:
            if not os.path.isfile(args.statement):
                return fail(f"statement file not found: {args.statement}")
            manifest["kind"] = "statement"
            shutil.copyfile(args.statement, os.path.join(args.out_dir, "statement.txt"))
            manifest["files"].append("statement.txt")
        elif args.source.startswith(("http://", "https://")):
            manifest["kind"] = "prototype — deployed site"
            manifest["files"] += screenshot([args.source] + args.also, args.out_dir, html_out="page.html",
                                            clicks=args.click)
            manifest["files"].append("page.html")
        elif os.path.isdir(args.source):
            manifest["kind"] = "prototype — project"
            for name in sorted(os.listdir(args.source)):
                path = os.path.join(args.source, name)
                if os.path.isfile(path) and not os.path.islink(path) \
                        and os.path.splitext(name)[1].lower() in DOC_EXT:
                    shutil.copyfile(path, os.path.join(args.out_dir, name))
                    manifest["files"].append(name)
            if not manifest["files"]:
                return fail(f"the project folder has no top-level written docs to keep: {args.source}")
        else:
            if not os.path.isfile(args.source):
                return fail(f"source file not found: {args.source}")
            name = os.path.basename(args.source)
            shutil.copyfile(args.source, os.path.join(args.out_dir, name))
            manifest["files"].append(name)
            if os.path.splitext(name)[1].lower() in HTML_EXT:
                manifest["kind"] = "prototype — file"
                url = pathlib.Path(os.path.abspath(args.source)).as_uri()   # escapes # and ?
                manifest["files"] += screenshot([url] + args.also, args.out_dir, clicks=args.click)
            else:
                manifest["kind"] = "document"
    except ImportError:
        return fail("cannot run through a site or an HTML file: Playwright is not installed "
                    "(pip install playwright && playwright install chromium)")
    except Exception as exc:  # noqa: BLE001 — any failure to read the source is F1
        if "Executable doesn't exist" in str(exc):
            return fail("cannot run through a site or an HTML file: Playwright's browser is not "
                        "installed (python3 -m playwright install chromium)")
        return fail(f"could not read the source: {exc.__class__.__name__}: {str(exc).splitlines()[0]}")

    manifest["sha256"] = {f: sha256(os.path.join(args.out_dir, f)) for f in manifest["files"]}
    manifest["snapshot_saved"] = bool(manifest["files"])
    if not manifest["snapshot_saved"]:
        return fail("nothing was captured")
    with open(args.manifest, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
