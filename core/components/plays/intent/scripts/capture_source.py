#!/usr/bin/env python3
"""capture_source.py — keep a Source exactly as it was when read (/intent, #612).

A Source is anything that explains a business intent (ontology v2): a prototype (a file or
a deployed site), a document, or a plain statement. This script takes its snapshot into the
run's evidence folder, so it outlives the link or the file, and writes the source manifest:

  site       (http/https)    full-page screenshot(s) + the page HTML, via a headless browser,
                             and every view the page offers, found by exploring it (C1)
  file       (.html/.htm)    a copy of the file + a rendered screenshot of every view
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


# What can switch a view: buttons, tabs, menu items, links and pressed-state toggles.
CONTROLS = ("button, [role=tab], [role=menuitem], [role=link], a[href], [aria-pressed], "
            "[data-go], [data-view], summary")
# Controls that answer or change data rather than show a view: never clicked while exploring.
ANSWERS = ("accept", "approve", "reject", "drop", "send back", "delete", "remove", "edit",
           "comment", "finish", "submit", "undo", "save", "reset", "log out", "sign out",
           "point", "upload", "pay", "buy")
MAX_VIEWS = 40
MAX_CLICKS = 160


def _label(handle):
    """A control's words, for the record: its text, else its aria-label, title or id."""
    text = " ".join((handle.inner_text() or "").split())[:60]
    return text or handle.get_attribute("aria-label") or handle.get_attribute("title") \
        or handle.get_attribute("id") or "(no label)"


def _controls(page, origin):
    """The visible, enabled controls on the page now, as (index, label) — the index is the
    control's place in page.locator(CONTROLS), stable on a fresh load of the same state."""
    found = []
    loc = page.locator(CONTROLS)
    for i in range(loc.count()):
        h = loc.nth(i)
        try:
            if not (h.is_visible() and h.is_enabled()):
                continue
            label = _label(h)
            href = h.get_attribute("href") or ""
        except Exception:  # noqa: BLE001 — a control that vanished while reading is skipped
            continue
        if any(word in label.lower() for word in ANSWERS):
            continue
        if href.startswith(("mailto:", "tel:", "javascript:")) or (
                href.startswith(("http://", "https://")) and not href.startswith(origin)):
            continue  # leaves the prototype
        found.append((i, label))
    return found


def _text(page):
    return page.inner_text("body")


def explore(page, url, out_dir, start_no):
    """Find every view the page offers, two clicks deep, and keep each new one (#613).

    For each control on the first screen — then for each new control on each view that
    opened — load the page fresh, replay the clicks, and keep the view when its visible text
    differs from every view kept so far. Returns (files, views): `views` records what was
    found, kept and could not be reached, for the source manifest."""
    origin = url.split("#")[0].rsplit("/", 1)[0]
    files, seen, unreached, found = [], set(), [], []
    page.goto(url, wait_until="networkidle", timeout=30000)
    seen.add(hashlib.sha256(_text(page).encode()).hexdigest())
    root = _controls(page, origin)
    root_labels = {label for _, label in root}
    queue = [((i,), (label,)) for i, label in root]
    clicks = 0
    while queue and clicks < MAX_CLICKS and len(files) // 2 < MAX_VIEWS:
        path, labels = queue.pop(0)
        found.append(" > ".join(labels))
        clicks += 1
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
            for idx in path:
                page.locator(CONTROLS).nth(idx).click(timeout=5000)
                page.wait_for_timeout(250)
            text = _text(page)
        except Exception as exc:  # noqa: BLE001 — record it, keep exploring
            unreached.append({"view": " > ".join(labels), "why": str(exc).splitlines()[0][:160]})
            continue
        digest = hashlib.sha256(text.encode()).hexdigest()
        if digest in seen:
            continue  # same as a view already kept (or the first screen)
        seen.add(digest)
        n = start_no + len(files) // 2
        slug = "".join(c if c.isalnum() else "-" for c in labels[-1].lower())[:40].strip("-")
        files += keep_view(page, out_dir, f"view-{n:02d}-{slug or 'control'}")
        if len(path) == 1:  # one level deeper: the controls this view added
            for i, label in _controls(page, origin):
                if label not in root_labels:
                    queue.append((path + (i,), labels + (label,)))
    if queue:
        unreached += [{"view": " > ".join(lb), "why": "the exploration limit was reached"}
                      for _, lb in queue]
    views = {"explored": True, "found": len(found) + 1, "kept": len(files) // 2 + 1,
             "unreached": unreached, "limit_reached": bool(queue),
             "note": "a control whose view repeats one already kept is found but not kept again"}
    return files, views


def screenshot(urls, out_dir, html_out=None, clicks=(), views=None):
    """Full-page screenshots of each url; with `views` (a dict), every view of the first url,
    found by exploring it (`view-NN-….png/.txt`); then the first url after clicking each named
    control in turn. Each view keeps its visible text beside its picture, so every view can be
    read, not only seen. Returns file names. Raises on failure — a named control that cannot
    be found is a failure, not a skip."""
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
        if views is not None:  # find and keep every view of the first page (C1)
            more, record = explore(page, urls[0], out_dir, len(shots) // 2 + 1)
            shots += more
            views.update(record)
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
            manifest["views"] = {}
            manifest["files"] += screenshot([args.source] + args.also, args.out_dir, html_out="page.html",
                                            clicks=args.click, views=manifest["views"])
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
                manifest["views"] = {}
                manifest["files"] += screenshot([url] + args.also, args.out_dir, clicks=args.click,
                                                views=manifest["views"])
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
