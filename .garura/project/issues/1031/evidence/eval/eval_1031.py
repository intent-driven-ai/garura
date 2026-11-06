#!/usr/bin/env python3
"""Acceptance check: the model's skills write an approved ICE page and its index entry.

Written before the build, so it fails until the two jobs exist. Run from the repo root:

    python3 <this file>

E1  The page skill writes a feature page and its ICE page from approved text, word for word.
E2  The page skill refuses, and the model stays byte for byte as it was, when:
    the text holds a Thin line; a part page holds an ICE section; an ICE page lacks a part;
    no one approved it; the page leaves the model; the page is an intent page.
E3  The index skill adds the ICE's entry (id, for, for_kind, doc) and, for a thin one, the thin
    mark on the ICE page (a Thin line before Intent) and on its entry; the spine keeps its comment.
E4  The index skill refuses, and the model stays as it was, when: the part is not in the spine;
    the part already has an ICE; the ICE page is not beside the part's page; the ICE page lacks
    a part; the thin mark is asked for on a part that has an ICE.
E5  A spine that gets no ICE entry gets no `ices` list.
"""

import json
import os
import subprocess
import sys
import tempfile

import yaml

ROOT = os.getcwd()
PAGE_SCRIPT = os.path.join(ROOT, "core/components/skills/enrich-grounding/scripts/write_approved.py")
INDEX_SCRIPT = os.path.join(ROOT, "core/components/skills/link-model-part/scripts/link_part.py")

SPINE = """\
# The spine: a comment that must stay.
domains: []
capabilities:
- id: cap-mail
  slug: mail
  domain: ''
  intents:
  - bi-1
  status: proposed
  one_line: Send mail
  doc: capabilities/cap-mail/capability.md
features:
- id: fn-send
  slug: fn-send
  capability: cap-mail
  intents:
  - bi-1
  status: proposed
  one_line: Send one message
  doc: capabilities/cap-mail/fn-send/feature.md
  depends_on: []
  identified_by: ''
slices: []
"""

FEATURE = """\
# Feature: Send one message

## What it does
A person writes one message and sends it to one address.

## Inputs / Outputs
- In: the address and the words.
- Out: the sent message.

## Rules & behavior
- A message with no address is not sent.

## Acceptance criteria
- Given an address and words, when the person sends, then the message arrives.

## Out of scope
- Sending to a group. Another feature does this.
"""

ICE = """\
## Intent
- Goal: A person sends one message to one address.
- Limit: It never sends without an address.
- Fails if: A message goes to the wrong address.

## Context
- Read: the mail rules.
- Persona: a person with one message to send.

## Expectation
- Scenario: A message with an address arrives.
- Done means: A tester who did not build it sees the message arrive.
"""

THIN = "Thin: proposed from the person's words; deepen with `/discover-capabilities`."
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


class Model:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = self.tmp.name + "/"
        self.root = os.path.join(self.base, "product-os")
        self.work = os.path.join(self.tmp.name, "work")
        os.makedirs(self.work)
        self.put("_spine.yaml", SPINE)
        self.put("intents/bi-1.md", "# People get their mail\n")
        self.put("capabilities/cap-mail/capability.md", "# Capability: Send mail\n\n## Directional intent\nPeople send mail.\n")
        self.put("capabilities/cap-mail/fn-send/feature.md", "# Feature: Send one message\n\n## What it does\nOld words.\n")

    def put(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def read(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as fh:
            return fh.read()

    def snapshot(self):
        out = {}
        for d, _, files in os.walk(self.root):
            for f in files:
                p = os.path.join(d, f)
                with open(p, "rb") as fh:
                    out[os.path.relpath(p, self.root)] = fh.read()
        return out

    def approved(self, name, text):
        path = os.path.join(self.work, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def run(self, script, request):
        req = os.path.join(self.work, "request.json")
        out = os.path.join(self.work, "report.json")
        with open(req, "w", encoding="utf-8") as fh:
            json.dump(request, fh)
        if os.path.exists(out):
            os.remove(out)
        if not os.path.isfile(script):
            return 127, f"{os.path.relpath(script, ROOT)} does not exist"
        p = subprocess.run([sys.executable, script, "--request", req, "--product-base", self.base,
                            "--out", out], capture_output=True, text=True)
        return p.returncode, p.stderr


def page_request(m, pages, approved_by="the product owner"):
    req = {"by": "the acceptance check", "source": "an approved draft", "pages": pages}
    if approved_by:
        req["approved_by"] = approved_by
    return req


# E1
m = Model()
fp = m.approved("feature.md", FEATURE)
ip = m.approved("ice.md", ICE)
code, err = m.run(PAGE_SCRIPT, page_request(m, [
    {"page": "capabilities/cap-mail/fn-send/feature.md", "from": fp},
    {"page": "capabilities/cap-mail/fn-send/ice.md", "from": ip}]))
check("E1 page skill writes both pages", code == 0, err.strip()[:200])
if code == 0:
    check("E1 feature page word for word", m.read("capabilities/cap-mail/fn-send/feature.md") == FEATURE)
    check("E1 ICE page word for word", m.read("capabilities/cap-mail/fn-send/ice.md") == ICE)

# E2
refusals = {
    "a Thin line in the text": [{"page": "capabilities/cap-mail/fn-send/ice.md",
                                 "from": ("thin.md", THIN + "\n\n" + ICE)}],
    "an ICE section on a part page": [{"page": "capabilities/cap-mail/fn-send/feature.md",
                                       "from": ("inline.md", FEATURE + "\n## Agent intent (ICE)\n- Goal: Send one message to one address.\n")}],
    "an ICE page with no Expectation": [{"page": "capabilities/cap-mail/fn-send/ice.md",
                                         "from": ("short.md", ICE.split("## Expectation")[0])}],
    "a page that leaves the model": [{"page": "../outside.md", "from": ("out.md", FEATURE)}],
    "an intent page": [{"page": "intents/bi-1.md", "from": ("intent.md", "# People get their mail\n")}],
}
for why, pages in refusals.items():
    m = Model()
    before = m.snapshot()
    pages = [{"page": p["page"], "from": m.approved(*p["from"])} for p in pages]
    code, err = m.run(PAGE_SCRIPT, page_request(m, pages))
    check(f"E2 page skill refuses {why}", code == 2 and m.snapshot() == before, f"exit {code}: {err.strip()[:160]}")
m = Model()
before = m.snapshot()
code, err = m.run(PAGE_SCRIPT, page_request(m, [{"page": "capabilities/cap-mail/fn-send/feature.md",
                                                 "from": m.approved("f.md", FEATURE)}], approved_by=None))
check("E2 page skill refuses with no one who approved", code == 2 and m.snapshot() == before, f"exit {code}")


def index_request(parts):
    return {"by": "the acceptance check", "parts": parts}


def with_ice(m, thin_text=False):
    m.put("capabilities/cap-mail/fn-send/ice.md", ICE)
    m.put("capabilities/cap-mail/ice.md", ICE)


# E3
m = Model()
with_ice(m)
code, err = m.run(INDEX_SCRIPT, index_request([
    {"id": "ice-send", "kind": "ice", "mode": "new", "for": "fn-send",
     "doc": "capabilities/cap-mail/fn-send/ice.md", "thin": True},
    {"id": "ice-mail", "kind": "ice", "mode": "new", "for": "cap-mail",
     "doc": "capabilities/cap-mail/ice.md"}]))
check("E3 index skill adds the ICE entries", code == 0, err.strip()[:200])
if code == 0:
    spine = yaml.safe_load(m.read("_spine.yaml"))
    ices = {e.get("id"): e for e in spine.get("ices") or []}
    send, mail = ices.get("ice-send") or {}, ices.get("ice-mail") or {}
    check("E3 feature ICE entry", send.get("for") == "fn-send" and send.get("for_kind") == "feature"
          and send.get("doc") == "capabilities/cap-mail/fn-send/ice.md")
    check("E3 capability ICE entry", mail.get("for") == "cap-mail" and mail.get("for_kind") == "capability")
    check("E3 thin on the ICE entry only", (send.get("metadata") or {}).get("thin") is True
          and not (mail.get("metadata") or {}).get("thin"))
    page = m.read("capabilities/cap-mail/fn-send/ice.md")
    check("E3 Thin line at the top, before Intent", page.splitlines()[0] == THIN and page.index(THIN) < page.index("## Intent"))
    check("E3 unthin ICE page untouched", m.read("capabilities/cap-mail/ice.md") == ICE)
    check("E3 no business intent on an ICE entry", not any(k in send for k in ("intents", "business_intent")))
    check("E3 spine keeps its comment", m.read("_spine.yaml").startswith("# The spine: a comment that must stay."))
    check("E3 part entry not marked thin", not ((next(f for f in spine["features"] if f["id"] == "fn-send").get("metadata") or {}).get("thin")))

# E4
cases = {
    "a part not in the spine": {"id": "ice-x", "kind": "ice", "mode": "new", "for": "fn-none",
                                "doc": "capabilities/cap-mail/fn-send/ice.md"},
    "an ICE page not beside its part": {"id": "ice-send", "kind": "ice", "mode": "new", "for": "fn-send",
                                        "doc": "capabilities/cap-mail/ice.md"},
}
for why, part in cases.items():
    m = Model()
    with_ice(m)
    before = m.snapshot()
    code, err = m.run(INDEX_SCRIPT, index_request([part]))
    check(f"E4 index skill refuses {why}", code == 2 and m.snapshot() == before, f"exit {code}: {err.strip()[:160]}")
m = Model()
with_ice(m)
first = {"id": "ice-send", "kind": "ice", "mode": "new", "for": "fn-send", "doc": "capabilities/cap-mail/fn-send/ice.md"}
code, _ = m.run(INDEX_SCRIPT, index_request([first]))
before = m.snapshot()
code2, err = m.run(INDEX_SCRIPT, index_request([dict(first, id="ice-send-2")]))
check("E4 index skill refuses a second ICE for one part", code == 0 and code2 == 2 and m.snapshot() == before, f"exit {code}/{code2}: {err.strip()[:160]}")
code3, err = m.run(INDEX_SCRIPT, index_request([{"id": "fn-send", "kind": "feature", "mode": "update", "thin": True}]))
check("E4 index skill refuses the thin mark on a part that has an ICE", code == 0 and code3 == 2 and m.snapshot() == before, f"exit {code3}: {err.strip()[:160]}")
m = Model()
m.put("capabilities/cap-mail/fn-send/ice.md", ICE.split("## Expectation")[0])
before = m.snapshot()
code, err = m.run(INDEX_SCRIPT, index_request([first]))
check("E4 index skill refuses an ICE page with a part missing", code == 2 and m.snapshot() == before, f"exit {code}: {err.strip()[:160]}")

# E5
m = Model()
m.put("capabilities/cap-mail/fn-other/feature.md", FEATURE.replace("Send one message", "Send a copy"))
code, err = m.run(INDEX_SCRIPT, index_request([{"id": "fn-other", "kind": "feature", "mode": "new", "slug": "fn-other",
                                                "capability": "cap-mail", "intents": ["bi-1"], "one_line": "Send a copy",
                                                "doc": "capabilities/cap-mail/fn-other/feature.md"}]))
check("E5 no ICE entry, no ices list", code == 0 and "ices" not in (yaml.safe_load(m.read("_spine.yaml")) or {}), err.strip()[:160])

failed = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + ("" if ok or not detail else f"  ({detail})"))
print(f"\n{len(results) - len(failed)} of {len(results)} pass")
sys.exit(1 if failed else 0)
