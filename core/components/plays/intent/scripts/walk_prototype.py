#!/usr/bin/env python3
"""walk_prototype.py — take one step of a journey through a prototype (/intent, #613).

`/intent` understands a prototype by using it (C15): the walk-prototype skill plans journeys
— who, what they set out to do — and walks each one a step at a time through this script. Each
call loads the prototype fresh, replays the journey's steps so far, takes the next one, and
keeps what the page shows after it: its picture, its visible text, and the controls and fields
the person could use next. The steps file is the journey's own record, so any step can be seen
again by replaying it.

    python3 walk_prototype.py --source <file path or link> --steps <journey>.steps.json \
        --out-dir <evidence>/journeys --name <journey-id>-NN [--allow-changes]

`<journey>.steps.json` holds the steps taken so far, the last one being the one to take now:

    [ {"do": "click", "target": "Catch up"},
      {"do": "type",  "target": "Search", "text": "refund"},
      {"do": "press", "target": "ArrowRight"},
      {"do": "back"} ]

`click` and `type` find their target by the words a person sees (a button's text, a field's
label or placeholder), or by `#<n>` — the n-th control in the last step's `controls` list.

Safety: a click on a control that answers or changes data (accept, delete, pay, submit …) is
refused on a deployed site unless `--allow-changes` is given — the person says the site is safe
for it. On a file or a local folder's page it is allowed: nothing real changes.

Writes `<name>.png`, `<name>.txt` and `<name>.json` (`{ok, step, url, controls, fields,
changed, why}`) and prints the JSON. Exit 0 the step was taken; 1 the step could not be taken
(the record says why — the journey ends there or tries another way); 2 bad input or the
prototype cannot be opened. No git, no LLM.
"""
import argparse
import json
import os
import pathlib
import sys

CONTROLS = ("button, [role=tab], [role=menuitem], [role=link], a[href], [aria-pressed], "
            "[data-go], [data-view], summary")
FIELDS = "input:not([type=hidden]), textarea, select, [contenteditable=true]"
CHANGES = ("accept", "approve", "reject", "drop", "send back", "delete", "remove", "finish",
           "submit", "save", "pay", "buy", "upload", "sign out", "log out", "reset")


def url_of(source):
    if source.startswith(("http://", "https://")):
        return source, True
    if not os.path.exists(source):
        raise FileNotFoundError(f"nothing is at {source}")
    return pathlib.Path(os.path.abspath(source)).as_uri(), False


def label_of(h):
    text = " ".join((h.inner_text() or "").split())[:60]
    return text or h.get_attribute("aria-label") or h.get_attribute("placeholder") \
        or h.get_attribute("title") or h.get_attribute("name") or h.get_attribute("id") or ""


def visible(page, selector):
    out, loc = [], page.locator(selector)
    for i in range(loc.count()):
        h = loc.nth(i)
        try:
            if h.is_visible():
                out.append((h, label_of(h)))
        except Exception:  # noqa: BLE001 — a node that vanished while reading
            continue
    return out


def find(page, target, selector):
    """The control or field a person would mean by `target`: its words, or `#n`."""
    items = visible(page, selector)
    if target.startswith("#") and target[1:].isdigit():
        n = int(target[1:])
        if n >= len(items):
            raise LookupError(f"there is no {target} on this screen")
        return items[n]
    wanted = " ".join(target.split()).lower()
    for exact in (True, False):
        for h, label in items:
            have = label.lower()
            if (have == wanted) if exact else (wanted in have):
                return h, label
    raise LookupError(f"nothing on this screen reads `{target}`")


def take(page, step, deployed, allow_changes):
    do = step.get("do")
    if do == "click":
        h, label = find(page, str(step.get("target", "")), CONTROLS)
        if deployed and not allow_changes and any(w in label.lower() for w in CHANGES):
            raise PermissionError(f"`{label}` changes data on a deployed site — take it only when "
                                  f"the person says the site is safe (--allow-changes)")
        h.click(timeout=5000)
    elif do == "type":
        h, _ = find(page, str(step.get("target", "")), FIELDS)
        h.fill(str(step.get("text", "")), timeout=5000)
    elif do == "press":
        page.keyboard.press(str(step.get("target", "")))
    elif do == "back":
        page.go_back(timeout=5000)
    else:
        raise ValueError(f"unknown step `{do}` — use click, type, press or back")
    page.wait_for_timeout(300)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Take one step of a journey through a prototype.")
    ap.add_argument("--source", required=True)
    ap.add_argument("--steps", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--allow-changes", action="store_true")
    args = ap.parse_args(argv)
    try:
        url, deployed = url_of(args.source)
        with open(args.steps, encoding="utf-8") as fh:
            steps = json.load(fh)
        if not isinstance(steps, list):
            raise ValueError("the steps file must hold a list of steps")
        from playwright.sync_api import sync_playwright
    except (OSError, ValueError, ImportError) as exc:
        sys.stderr.write(f"walk_prototype.py: {exc}\n")
        return 2
    os.makedirs(args.out_dir, exist_ok=True)
    record = {"ok": False, "step": steps[-1] if steps else None, "why": None}
    code = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception as exc:  # noqa: BLE001
            browser.close()
            sys.stderr.write(f"walk_prototype.py: cannot open the prototype: {exc}\n")
            return 2
        before = page.inner_text("body")
        for i, step in enumerate(steps):
            try:
                if i == len(steps) - 1:
                    before = page.inner_text("body")
                take(page, step, deployed, args.allow_changes)
            except Exception as exc:  # noqa: BLE001 — the journey learns this step failed
                record["why"] = (f"step {i + 1}: " if i < len(steps) - 1 else "") + str(exc).splitlines()[0]
                code = 1
                break
        else:
            record["ok"] = True
        text = page.inner_text("body")
        page.screenshot(path=os.path.join(args.out_dir, f"{args.name}.png"), full_page=True)
        with open(os.path.join(args.out_dir, f"{args.name}.txt"), "w", encoding="utf-8") as fh:
            fh.write(text)
        record.update({"url": page.url, "changed": text != before,
                       "controls": [lb for _, lb in visible(page, CONTROLS)],
                       "fields": [lb for _, lb in visible(page, FIELDS)],
                       "files": [f"{args.name}.png", f"{args.name}.txt"]})
        browser.close()
    with open(os.path.join(args.out_dir, f"{args.name}.json"), "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    print(json.dumps({k: record[k] for k in ("ok", "changed", "why")}))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
