#!/usr/bin/env python3
"""
spine_text.py — write a changed spine back and keep its comments and layout (/shape-slice).

yaml.safe_dump writes the whole file again and drops every comment. This module changes only
the text of the top-level lists that changed, item by item, and keeps every other line:

  - a list that only grew gets its new items written at the end of its block;
  - a list where items were replaced (same length) gets each changed item's lines rewritten;
  - any other change to a list rewrites that list's block;
  - a top-level key that is new is written at the end of the file.

Comments outside a rewritten item or block stay as they are. The result is loaded again and
compared with the data; when it differs, the module falls back to a full safe_dump, and says
so (`kept` false), so the spine is always right even when a layout is too odd to keep.

    import spine_text
    text, kept = spine_text.dump(old_text, old_data, new_data)

Pure text in, text out: no files, no git, no network.
"""

import re

import yaml

KEY = re.compile(r"^(?P<key>[A-Za-z_][\w-]*):(?P<rest>.*)$")


def _dump(value, indent):
    """A YAML block for `value`, each line indented by `indent` spaces."""
    text = yaml.safe_dump(value, sort_keys=False, allow_unicode=True, default_flow_style=False)
    return [(" " * indent + ln) if ln else ln for ln in text.splitlines()]


def _blocks(lines):
    """{key: (start, end)} for each top-level key; end is past the block's last content line."""
    starts = [(i, KEY.match(ln).group("key")) for i, ln in enumerate(lines) if KEY.match(ln)]
    out = {}
    for n, (i, key) in enumerate(starts):
        nxt = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        end = nxt
        while end > i + 1 and (not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("#")):
            end -= 1
        out[key] = (i, end)
    return out


def _items(lines, start, end):
    """(indent, [(first, last_exclusive), ...]) of the block's sequence items, or None."""
    heads = [i for i in range(start + 1, end) if re.match(r"^\s*- ", lines[i]) or lines[i].strip() == "-"]
    if not heads:
        return None
    indent = len(lines[heads[0]]) - len(lines[heads[0]].lstrip())
    heads = [i for i in heads if len(lines[i]) - len(lines[i].lstrip()) == indent]
    spans = []
    for n, h in enumerate(heads):
        stop = heads[n + 1] if n + 1 < len(heads) else end
        while stop > h + 1 and (not lines[stop - 1].strip() or lines[stop - 1].lstrip().startswith("#")):
            stop -= 1
        spans.append((h, stop))
    return indent, spans


def _rewrite_list(lines, start, end, key, old, new):
    """New lines for the block of list `key`, or None when only a full rewrite fits."""
    rest = KEY.match(lines[start]).group("rest").strip()
    if not isinstance(old, list) or not old or rest not in ("",) and not rest.startswith("#"):
        return None
    found = _items(lines, start, end)
    if found is None or len(found[1]) != len(old):
        return None
    indent, spans = found
    block = lines[start:end]
    if len(new) >= len(old) and new[:len(old)] == old:
        return block + _dump(new[len(old):], indent)
    if len(new) == len(old):
        for (first, stop), was, now in reversed(list(zip(spans, old, new))):
            if was != now:
                block[first - start:stop - start] = _dump([now], indent)
        return block
    return None


def dump(old_text, old_data, new_data):
    """The new spine text, and whether its comments and layout were kept."""
    full = yaml.safe_dump(new_data, sort_keys=False, allow_unicode=True)
    if not isinstance(old_data, dict) or not isinstance(new_data, dict) \
            or any(k not in new_data for k in old_data):
        return full, False
    lines = old_text.splitlines()
    blocks = _blocks(lines)
    if set(blocks) != set(old_data):
        return full, False
    for key in sorted(old_data, key=lambda k: blocks[k][0], reverse=True):
        if old_data[key] == new_data[key]:
            continue
        start, end = blocks[key]
        part = None
        if isinstance(new_data[key], list):
            part = _rewrite_list(lines, start, end, key, old_data[key], new_data[key])
        if part is None:
            part = _dump({key: new_data[key]}, 0)
        lines[start:end] = part
    for key in new_data:
        if key not in old_data:
            lines += _dump({key: new_data[key]}, 0)
    text = "\n".join(lines) + "\n"
    try:
        same = yaml.safe_load(text) == new_data
    except yaml.YAMLError:
        same = False
    return (text, True) if same else (full, False)
