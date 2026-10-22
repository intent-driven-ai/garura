#!/usr/bin/env python3
"""intent_touches.py — the Touches list on a business intent page (ontology v4, #637).

A business intent page names every part of the product it touches — each domain,
capability and functionality — and how: it adds it, changes it, or removes it. The list
sits on the intent page, in the person's words, and each line links to the part's page:

    **Touches:**
    - [Checkout](../commerce/checkout/capability.md) (capability) — adds
    - [Commerce](../commerce/domain.md) (domain) — changes

The agent side of the same link is the spine: a node's `intents` names the intents it
serves. Any play that links a node to an intent writes both sides; this module writes the
intent-page side, so every play writes it the same way. It is never written by an LLM.

Canonical copy lives at create-play/references/intent_touches.py and is stamped into the
scripts/ of each play that writes intent links (/discover-intent, /discover-domains). Pure text in, text out:
no files, no git, no network.

    import intent_touches as it
    text = it.upsert(text, [it.entry("Checkout", link, "capability", "adds")])
    text, n = it.relink(text, old_link, new_link)
"""
import os
import re

HEADER = "**Touches:**"
KINDS = ("domain", "capability", "functionality")
MARKS = ("adds", "changes", "removes")
LINE = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<link>[^)\s]+)\) "
                  r"\((?P<kind>domain|capability|functionality)\) — (?P<mark>adds|changes|removes)$")
# The list /discover-intent wrote before ontology v4: capabilities only, all of them new.
OLD_HEADER = re.compile(r"^\*\*ICE built from it[^*]*:\*\*")
OLD_LINE = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<link>[^)\s]+)\)$")
NEXT_ANCHOR = "**What was done:**"


class Bad(ValueError):
    """A Touches entry that cannot be written."""


def entry(title, link, kind, mark):
    if kind not in KINDS:
        raise Bad(f"kind must be one of {KINDS}, not {kind!r}")
    if mark not in MARKS:
        raise Bad(f"mark must be one of {MARKS}, not {mark!r}")
    title = " ".join(str(title).split()).replace("[", "(").replace("]", ")")
    if not title or not link or any(c.isspace() for c in link):
        raise Bad(f"a Touches entry needs a title and a link with no spaces ({title!r}, {link!r})")
    return {"title": title, "link": link, "kind": kind, "mark": mark}


def rel(intent_page, target):
    """The link from an intent page to a part's page, both paths on disk."""
    return os.path.relpath(target, os.path.dirname(intent_page)).replace(os.sep, "/")


def render(entries):
    if not entries:
        return [f"{HEADER} none yet"]
    return [HEADER] + [f"- [{e['title']}]({e['link']}) ({e['kind']}) — {e['mark']}" for e in entries]


def _block(lines):
    """(start, end, entries, old) for the Touches list — or the pre-v4 list — else None."""
    for i, line in enumerate(lines):
        new = line.strip().startswith(HEADER)
        if not (new or OLD_HEADER.match(line.strip())):
            continue
        entries, j = [], i + 1
        while j < len(lines) and lines[j].startswith("- "):
            m = (LINE if new else OLD_LINE).match(lines[j].strip())
            if m:
                d = m.groupdict()
                entries.append(d if new else entry(d["title"], d["link"], "capability", "adds"))
            j += 1
        return i, j, entries, not new
    return None


def read(text):
    """The Touches entries on a page, in order ([] when it has none)."""
    found = _block(text.splitlines())
    return found[2] if found else []


def upsert(text, entries):
    """Add each entry whose link is not listed yet; an entry already listed keeps its mark.

    A page with the pre-v4 list has it turned into a Touches list (each capability `adds`).
    A page with no list gets one, just before "What was done", or at the end."""
    lines = text.splitlines()
    found = _block(lines)
    merged = list(found[2]) if found else []
    listed = {e["link"] for e in merged}
    for e in entries:
        if e["link"] not in listed:
            merged.append(e)
            listed.add(e["link"])
    if found:
        lines[found[0]:found[1]] = render(merged)
    else:
        at = next((i for i, line in enumerate(lines) if line.startswith(NEXT_ANCHOR)), len(lines))
        while at > 0 and not lines[at - 1].strip():
            at -= 1
        after = lines[at:]
        while after and not after[0].strip():
            after.pop(0)
        lines = lines[:at] + ([""] if at else []) + render(merged) + ([""] + after if after else [])
    return "\n".join(lines) + "\n"


def relink(text, old, new):
    """Point every link to `old` on the page at `new` (a part's page moved). Returns (text, n).

    Only markdown link targets equal to `old` change; nothing else on the page does."""
    pattern = re.compile(r"\]\(" + re.escape(old) + r"\)")
    out, n = pattern.subn("](" + new.replace("\\", "/") + ")", text)
    return out, n
