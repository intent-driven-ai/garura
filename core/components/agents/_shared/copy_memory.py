#!/usr/bin/env python3
"""Write one short-term copy of a memory file, and its line in the manifest.

Usage:
  python3 .garura/core/tools/memory/memory.py read --issue <issue> --tier <tier> --path <path> \\
    | python3 .claude/skills/_shared/copy_memory.py <short-term copy> <manifest>

It reads one answer of the memory tool's `read` command on standard input. It writes the
answer's text, unchanged, to the copy path (it makes the folders). It adds the file's entry
to the manifest, or replaces the entry with the same copy path:

  {"files": [{"tier": ..., "path": ..., "version": ..., "fingerprint": ..., "copy": ...}]}

It prints one line of JSON. It exits 1 with a plain message when the answer says
"ok": false, when the input is not a `read` answer, or when the manifest is not valid.
"""

import json
import os
import sys
import tempfile

FIELDS = ("tier", "path", "version", "fingerprint")


class Stop(Exception):
    pass


def parse_answer(raw):
    try:
        answer = json.loads(raw)
    except ValueError:
        raise Stop("The input is not JSON. Pipe one answer of the memory tool's read command into this script.")
    if not isinstance(answer, dict):
        raise Stop("The input is not a memory tool answer (a JSON object).")
    if answer.get("ok") is False:
        error = answer.get("error") or {}
        message = error.get("message") if isinstance(error, dict) else str(error)
        code = error.get("code") if isinstance(error, dict) else None
        raise Stop(f"The memory tool did not read the file ({code or 'error'}): {message or 'no message'}. "
                   "No copy was written.")
    if answer.get("ok") is not True:
        raise Stop("The input has no \"ok\" field. It is not a memory tool answer.")
    if answer.get("command") not in (None, "read"):
        raise Stop(f"The input is the answer of '{answer.get('command')}', not of 'read'.")
    if not isinstance(answer.get("text"), str):
        raise Stop("The read answer has no text.")
    for field in FIELDS:
        if not isinstance(answer.get(field), str) or not answer.get(field):
            raise Stop(f"The read answer has no '{field}'.")
    return answer


def write_atomic(path, text):
    folder = os.path.dirname(path) or "."
    os.makedirs(folder, exist_ok=True)
    handle, temp = tempfile.mkstemp(dir=folder, prefix=".copy-", suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        os.replace(temp, path)
    except BaseException:
        if os.path.exists(temp):
            os.unlink(temp)
        raise


def load_manifest(path):
    if not os.path.exists(path):
        return {"files": []}
    try:
        with open(path, encoding="utf-8") as fh:
            manifest = json.load(fh)
    except ValueError:
        raise Stop(f"The manifest {path} is not valid JSON. Fix it or remove it, then copy again.")
    if not isinstance(manifest, dict):
        raise Stop(f"The manifest {path} is not a JSON object.")
    files = manifest.setdefault("files", [])
    if not isinstance(files, list):
        raise Stop(f"The manifest {path} has a 'files' value that is not a list.")
    return manifest


def run(raw, copy_path, manifest_path):
    answer = parse_answer(raw)
    manifest = load_manifest(manifest_path)
    entry = {field: answer[field] for field in FIELDS}
    entry["copy"] = copy_path
    write_atomic(copy_path, answer["text"])
    files = [f for f in manifest["files"] if not (isinstance(f, dict) and f.get("copy") == copy_path)]
    files.append(entry)
    manifest["files"] = files
    write_atomic(manifest_path, json.dumps(manifest, indent=2) + "\n")
    return {"ok": True, "copy": copy_path, "manifest": manifest_path,
            "tier": entry["tier"], "path": entry["path"], "fingerprint": entry["fingerprint"]}


def main(argv):
    if len(argv) != 3:
        print("Usage: copy_memory.py <short-term copy> <manifest>  (a memory tool read answer on stdin)",
              file=sys.stderr)
        return 1
    try:
        result = run(sys.stdin.read(), argv[1], argv[2])
    except Stop as stop:
        print(str(stop), file=sys.stderr)
        return 1
    except OSError as err:
        print(f"Could not write the copy or the manifest: {err}", file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
