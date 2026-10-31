#!/usr/bin/env python3
"""safe_write.py — the one way a script that writes the product model writes a file.

`atomic_write(path, text)` writes the text through a temp file in the same folder, then moves it
into place with os.replace. A run that stops half way never leaves half a file: the old file is
there whole, or the new one is. The folder is made when it is missing. A temp file that was not
moved into place is removed. The file keeps the permissions it had; a new file gets the
permissions the process would give any new file (0666 less its umask).

/shape-slice's persist_fills.py, persist_slice.py, write_hidden_file.py, render_brief.py and
write_intent_page.py, link-model-part's link_part.py and enrich-grounding's change_lines.py write
their output files and pages through it. No other script of theirs calls os.replace or
tempfile.mkstemp.
"""

import os
import stat
import tempfile


def _mode_for(path):
    """The permissions the file at `path` has, or those a new file would get."""
    if os.path.exists(path):
        return stat.S_IMODE(os.stat(path).st_mode)
    umask = os.umask(0)
    os.umask(umask)
    return 0o666 & ~umask


def atomic_write(path, text):
    """Write `text` to `path` through a temp file in the same folder, then os.replace it."""
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    mode = _mode_for(path)
    fd, tmp = tempfile.mkstemp(prefix=".garura-write-", suffix=".tmp", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
