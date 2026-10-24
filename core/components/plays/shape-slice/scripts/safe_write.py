#!/usr/bin/env python3
"""safe_write.py — the one way /shape-slice's scripts write a file.

`atomic_write(path, text)` writes the text through a temp file in the same folder, then moves it
into place with os.replace. A run that stops half way never leaves half a file: the old file is
there whole, or the new one is. The folder is made when it is missing. A temp file that was not
moved into place is removed.

persist_fills.py, persist_slice.py, write_hidden_file.py, render_brief.py and
write_intent_page.py write their output files and pages through it. No other script of the play
calls os.replace or tempfile.mkstemp.
"""

import os
import tempfile


def atomic_write(path, text):
    """Write `text` to `path` through a temp file in the same folder, then os.replace it."""
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".shape-slice-", suffix=".tmp", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
