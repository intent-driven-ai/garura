#!/usr/bin/env python3
"""walk_prototype.py — take one step of a journey through a prototype (/intent, #613).

`/intent` understands a prototype by using it (C15): the walk-prototype skill plans journeys
— who, what they set out to do — and walks each one a step at a time through this script. After
each step it keeps what the page shows: its picture, its visible text, and the controls and
fields the person could use next — and tells the walker **only what changed** (`added` lines,
`gone` count), so the walker reads a short answer, not the whole page again.

    python3 walk_prototype.py --source <file path or link> --steps <journey>.steps.json \
        --out-dir <evidence>/journeys --name <journey-id>-NN [--session <journey-id>] \
        [--allow-changes]
    python3 walk_prototype.py --session <journey-id> --stop

`<journey>.steps.json` holds the steps taken so far, the last one being the one to take now:

    [ {"do": "click", "target": "Catch up"},
      {"do": "type",  "target": "Search", "text": "refund"},
      {"do": "press", "target": "ArrowRight"},
      {"do": "back"} ]

`click` and `type` find their target by the words a person sees (a button's text, a field's
label or placeholder), or by `#<n>` — the n-th control in the last step's `controls` list.

**One browser per journey (`--session`).** With `--session`, the first call starts a small
local helper that keeps the journey's browser open; each later call sends only the new step to
it, so a step costs a click, not a fresh load and a replay of every step before it (#613: a
28-step journey took 11 s a step that way). If the steps file no longer starts with the steps
the helper took, it loads the page fresh and replays. `--stop` ends the helper; an idle helper
ends itself after 10 minutes. Without `--session`, every call loads fresh and replays — the
same result, slower.

Safety: a click on a control that answers or changes data (accept, delete, pay, submit …) is
refused on a deployed site unless `--allow-changes` is given — the person says the site is safe
for it. On a file or a local folder's page it is allowed: nothing real changes.

Writes `<name>.png`, `<name>.txt` and `<name>.json` (`{ok, step, url, added, gone, controls,
fields, changed, why}`) and prints the short form. Exit 0 the step was taken; 1 the step could
not be taken (the record says why); 2 bad input or the prototype cannot be opened. No git, no
LLM.
"""
import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import threading
import time

CONTROLS = ("button, [role=tab], [role=menuitem], [role=link], a[href], [aria-pressed], "
            "[data-go], [data-view], summary")
FIELDS = "input:not([type=hidden]), textarea, select, [contenteditable=true]"
CHANGES = ("accept", "approve", "reject", "drop", "send back", "delete", "remove", "finish",
           "submit", "save", "pay", "buy", "upload", "sign out", "log out", "reset")
IDLE_SECONDS = 600
MAX_ADDED = 80


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


def changes(before, after):
    """What the step changed: the lines now shown that were not there before, and how many went."""
    old, new = before.splitlines(), after.splitlines()
    old_set, new_set = set(old), set(new)
    added = [ln for ln in new if ln.strip() and ln not in old_set]
    gone = len([ln for ln in old if ln.strip() and ln not in new_set])
    return added[:MAX_ADDED], gone, len(added) > MAX_ADDED


class Walker:
    """One browser on one prototype; applies steps and keeps what each one shows."""

    def __init__(self, source, allow_changes):
        from playwright.sync_api import sync_playwright
        self.url, self.deployed = url_of(source)
        self.allow = allow_changes
        self._pw = sync_playwright().start()
        self.browser = self._pw.chromium.launch()
        self.page = self.browser.new_page(viewport={"width": 1280, "height": 900})
        self.applied = None

    def fresh(self):
        self.page.goto(self.url, wait_until="networkidle", timeout=30000)
        self.applied = []

    def run(self, steps, out_dir, name):
        record = {"ok": False, "step": steps[-1] if steps else None, "why": None}
        if self.applied is None or steps[:len(self.applied)] != self.applied:
            self.fresh()
        before = self.page.inner_text("body")
        for i in range(len(self.applied), len(steps)):
            if i == len(steps) - 1:
                before = self.page.inner_text("body")
            try:
                take(self.page, steps[i], self.deployed, self.allow)
                self.applied.append(steps[i])
            except Exception as exc:  # noqa: BLE001 — the journey learns this step failed
                record["why"] = (f"step {i + 1}: " if i < len(steps) - 1 else "") + str(exc).splitlines()[0]
                self.applied = None  # the page is in an unknown state: load fresh next time
                break
        else:
            record["ok"] = True
        text = self.page.inner_text("body")
        os.makedirs(out_dir, exist_ok=True)
        self.page.screenshot(path=os.path.join(out_dir, f"{name}.png"), full_page=True)
        with open(os.path.join(out_dir, f"{name}.txt"), "w", encoding="utf-8") as fh:
            fh.write(text)
        added, gone, more = changes(before, text)
        record.update({"url": self.page.url, "changed": text != before, "added": added,
                       "added_cut": more, "gone": gone,
                       "controls": [lb for _, lb in visible(self.page, CONTROLS)],
                       "fields": [lb for _, lb in visible(self.page, FIELDS)],
                       "files": [f"{name}.png", f"{name}.txt"]})
        with open(os.path.join(out_dir, f"{name}.json"), "w", encoding="utf-8") as fh:
            json.dump(record, fh, indent=2)
        return record

    def close(self):
        self.browser.close()
        self._pw.stop()


def sock_path(session):
    key = hashlib.sha256(f"{os.getcwd()}|{session}".encode()).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), f"walk-{key}.sock")


def serve(source, session, allow_changes):
    """The journey's helper: one browser, kept open, taking steps sent to it."""
    from multiprocessing.connection import Listener
    path = sock_path(session)
    if os.path.exists(path):
        os.remove(path)
    walker = Walker(source, allow_changes)
    last = [time.time()]

    def idle_watch():
        while True:
            time.sleep(15)
            if time.time() - last[0] > IDLE_SECONDS:
                os._exit(0)
    threading.Thread(target=idle_watch, daemon=True).start()
    with Listener(path, family="AF_UNIX") as listener:
        while True:
            with listener.accept() as conn:
                msg = conn.recv()
                last[0] = time.time()
                if msg.get("stop"):
                    conn.send({"stopped": True})
                    break
                try:
                    conn.send(walker.run(msg["steps"], msg["out_dir"], msg["name"]))
                except Exception as exc:  # noqa: BLE001
                    conn.send({"ok": False, "why": f"the helper failed: {exc}", "fatal": True})
    walker.close()
    if os.path.exists(path):
        os.remove(path)


def ask_helper(args, steps):
    """Send the step to the journey's helper, starting it if it is not running."""
    from multiprocessing.connection import Client
    path = sock_path(args.session)
    if not os.path.exists(path):
        cmd = [sys.executable, os.path.abspath(__file__), "--serve", "--source", args.source,
               "--session", args.session] + (["--allow-changes"] if args.allow_changes else [])
        subprocess.Popen(cmd, start_new_session=True, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
        for _ in range(200):
            if os.path.exists(path):
                break
            time.sleep(0.1)
    with Client(path, family="AF_UNIX") as conn:
        conn.send({"steps": steps, "out_dir": args.out_dir, "name": args.name})
        return conn.recv()


def stop_helper(session):
    from multiprocessing.connection import Client
    path = sock_path(session)
    if not os.path.exists(path):
        return 0
    try:
        with Client(path, family="AF_UNIX") as conn:
            conn.send({"stop": True})
            conn.recv()
    except OSError:
        os.remove(path)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Take one step of a journey through a prototype.")
    ap.add_argument("--source")
    ap.add_argument("--steps")
    ap.add_argument("--out-dir")
    ap.add_argument("--name")
    ap.add_argument("--session", help="keep one browser open for this journey")
    ap.add_argument("--stop", action="store_true", help="end the journey's helper")
    ap.add_argument("--serve", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--allow-changes", action="store_true")
    args = ap.parse_args(argv)
    if args.stop:
        return stop_helper(args.session or "")
    if args.serve:
        serve(args.source, args.session, args.allow_changes)
        return 0
    try:
        if not (args.source and args.steps and args.out_dir and args.name):
            raise ValueError("give --source, --steps, --out-dir and --name")
        url_of(args.source)
        with open(args.steps, encoding="utf-8") as fh:
            steps = json.load(fh)
        if not isinstance(steps, list):
            raise ValueError("the steps file must hold a list of steps")
        import playwright  # noqa: F401
    except (OSError, ValueError, ImportError) as exc:
        sys.stderr.write(f"walk_prototype.py: {exc}\n")
        return 2
    try:
        if args.session:
            record = ask_helper(args, steps)
        else:
            walker = Walker(args.source, args.allow_changes)
            try:
                record = walker.run(steps, args.out_dir, args.name)
            finally:
                walker.close()
    except Exception as exc:  # noqa: BLE001 — the prototype could not be opened
        sys.stderr.write(f"walk_prototype.py: cannot open the prototype: {exc}\n")
        return 2
    if record.get("fatal"):
        sys.stderr.write(f"walk_prototype.py: {record['why']}\n")
        return 2
    print(json.dumps({k: record.get(k) for k in ("ok", "changed", "why", "added", "gone")}))
    return 0 if record.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
