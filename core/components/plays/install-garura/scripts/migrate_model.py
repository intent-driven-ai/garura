#!/usr/bin/env python3
"""
migrate_model.py — move a project's product model to the #807 names (ADR 048, #813).

A project that installed Garura before #807 keeps the old names in its product model; after
#807 the scripts read only the new names. A person runs this script by hand; nothing runs it
on its own, and the install never changes a model (#813; when an upgrade may: #835). It moves
the model once:

  spine and slice keys   functionalities -> features, functionality_refs -> feature_refs,
                         functionality_ref -> feature_ref, for_kind: functionality -> feature
  path values            functionalities/ -> features/, .../functionality.md -> .../feature.md
                         (doc:, record: and any other value that is a path)
  folders and files      every functionalities/ folder -> features/,
                         every functionality.md page -> feature.md
  page headings          "# Functionality: ..." -> "# Feature: ...",
                         "## Functionalities" -> "## Features"

Prose is left alone, and IDs (fn-...) never change. The YAML is rewritten line by line, so the
file's other content and its comments stay as they are.

    python3 migrate_model.py --target <project dir> [--summary]

It finds the model at <target>/<product.base-path>product-os/ (product.base-path from
<target>/.garura/core/config.yaml, default .garura/product/). It refuses a model folder that
lies outside the project, by its path or through a link, and any link in the model that
points outside it: it never changes anything outside the project. In a git repository it
makes ONE commit that holds only the paths it moved or changed. It does not commit when the
target is not a git repository, or when those paths already had changes of their own; it
still moves, and says why in "reason". When a step fails after it started moving (a git
step, a hook that blocks the commit), it puts every file and folder back as it was, stages
nothing, and says why in "reason".

Prints a JSON report (or, with --summary, one plain line):
  {"moved": {"keys": [...], "files": [...], "folders": [...], "headings": [...]},
   "committed": true|false, "commit": "<sha>"|null, "reason": "..."}

Exit 0 when moved or nothing to move (a second run, or no model); 1 when a step failed and
everything was put back ("failed": true); 2 when it refuses ("refused": true): the model lies
outside the project, the spine holds both `functionalities:` and `features:`, or a page would
land on a page that exists. Nothing is changed when it refuses or fails.

The name table lives here, in OLD_TO_NEW below, for now (it may move to the rename map later).
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

# --- the name table (ADR 048) -------------------------------------------------------------
# Old name -> new name. Keys are YAML keys; FOLDERS and PAGES are path parts.
KEYS = {
    "functionalities": "features",
    "functionality_refs": "feature_refs",
    "functionality_ref": "feature_ref",
}
KIND_KEY, OLD_KIND, NEW_KIND = "for_kind", "functionality", "feature"
FOLDERS = {"functionalities": "features"}
PAGES = {"functionality.md": "feature.md"}
HEADINGS = [
    (re.compile(r"^# Functionality:"), "# Feature:"),
    (re.compile(r"^## Functionalities(?=\s*$)"), "## Features"),
]
OLD_TO_NEW = {"keys": KEYS, KIND_KEY: {OLD_KIND: NEW_KIND}, "folders": FOLDERS, "pages": PAGES}

COMMIT_MESSAGE = "chore(model): move the product model to the #807 names (ADR 048)"
DEFAULT_BASE = ".garura/product/"
YAML_EXT = (".yaml", ".yml")

_KEY_RE = re.compile(r"^(?P<lead>\s*(?:-\s+)*)(?P<q>['\"]?)(?P<key>" + "|".join(KEYS) + r")(?P=q)(?P<colon>\s*:)")
_KIND_RE = re.compile(r"^(?P<lead>\s*(?:-\s+)*['\"]?" + KIND_KEY + r"['\"]?\s*:\s*)(?P<q>['\"]?)"
                      + OLD_KIND + r"(?P=q)(?P<tail>\s*(?:#.*)?)$")
# a value that is a path: key: <one token with a "/" in it>, or a list item of one
_PATH_LINE_RE = re.compile(r"^(?P<head>\s*(?:-\s+)*(?:['\"]?[\w.-]+['\"]?\s*:\s*)?)(?P<q>['\"]?)"
                           r"(?P<val>[^\s'\"#]*/[^\s'\"#]*)(?P=q)(?P<tail>\s*(?:#.*)?)$")


class Refused(Exception):
    pass


class Failed(Exception):
    pass


def new_path(rel):
    """The path a model path moves to: each old folder part and an old page name renamed."""
    parts = rel.split("/")
    parts = [FOLDERS.get(p, p) for p in parts[:-1]] + [PAGES.get(parts[-1], FOLDERS.get(parts[-1], parts[-1]))]
    return "/".join(parts)


def rewrite_path_value(val):
    parts = val.split("/")
    out = [FOLDERS.get(p, p) for p in parts[:-1]] + [PAGES.get(parts[-1], FOLDERS.get(parts[-1], parts[-1]))]
    return "/".join(out)


def rewrite_yaml_lines(lines):
    """Rewrite keys, the kind value and path values. Returns (lines, [(old, new), ...])."""
    out, changes = [], []
    for line in lines:
        body, nl = (line[:-1], "\n") if line.endswith("\n") else (line, "")
        m = _KEY_RE.match(body)
        if m:
            new = KEYS[m.group("key")]
            changes.append((m.group("key"), new))
            body = m.group("lead") + m.group("q") + new + m.group("q") + m.group("colon") + body[m.end():]
        m = _KIND_RE.match(body)
        if m:
            changes.append((f"{KIND_KEY}: {OLD_KIND}", f"{KIND_KEY}: {NEW_KIND}"))
            body = m.group("lead") + m.group("q") + NEW_KIND + m.group("q") + m.group("tail")
        m = _PATH_LINE_RE.match(body)
        if m:
            val = rewrite_path_value(m.group("val"))
            if val != m.group("val"):
                changes.append((m.group("val"), val))
                body = m.group("head") + m.group("q") + val + m.group("q") + m.group("tail")
        out.append(body + nl)
    return out, changes


def rewrite_markdown(text):
    """Front matter gets the YAML rewrite; headings outside code fences get renamed."""
    lines = text.splitlines(keepends=True)
    key_changes, heading_changes = [], []
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm, key_changes = rewrite_yaml_lines(lines[1:i])
                lines[1:i] = fm
                start = i + 1
                break
    fenced = False
    for i in range(start, len(lines)):
        if lines[i].lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        for rx, repl in HEADINGS:
            if rx.match(lines[i]):
                old = lines[i].rstrip("\n")
                lines[i] = rx.sub(repl, lines[i], count=1)
                heading_changes.append((old, lines[i].rstrip("\n")))
    return "".join(lines), key_changes, heading_changes


# --- finding the model ----------------------------------------------------------------------

def product_base(target):
    cfg = os.path.join(target, ".garura", "core", "config.yaml")
    if not os.path.isfile(cfg):
        return DEFAULT_BASE
    text = open(cfg, encoding="utf-8").read()
    try:
        import yaml
        data = yaml.safe_load(text) or {}
        base = (data.get("product") or {}).get("base-path")
        if isinstance(base, str) and base.strip():
            return base
    except Exception:  # an unreadable config: fall back to a plain read of the key
        m = re.search(r"^product:\s*\n(?:[ \t]+.*\n)*?[ \t]+base-path:\s*['\"]?([^'\"\s#]+)", text, re.M)
        if m:
            return m.group(1)
    return DEFAULT_BASE


def inside(path, root):
    """True when `path`, with every link followed, lies inside `root`."""
    real, base = os.path.realpath(path), os.path.realpath(root)
    return real == base or real.startswith(base.rstrip(os.sep) + os.sep)


def model_dir(target):
    """The model folder from the project's config; refused when it lies outside the project."""
    base = product_base(target)
    model = os.path.normpath(os.path.join(target, base, "product-os"))
    if not inside(model, target):
        raise Refused(f"the product model folder ({model}, from product.base-path: {base}) lies outside "
                      f"the project ({target}). This script changes only the project; nothing was moved.")
    return model


def refuse_links_outside(model, target):
    for d, dirs, names in os.walk(model):
        for n in dirs + names:
            full = os.path.join(d, n)
            if os.path.islink(full) and not inside(full, target):
                raise Refused(f"{full} is a link to {os.path.realpath(full)}, outside the project. "
                              "This script changes only the project; nothing was moved.")


# --- git --------------------------------------------------------------------------------------

def git(target, *args, check=True):
    run = subprocess.run(["git", "-C", target, *args], capture_output=True, text=True)
    if check and run.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:2])} failed: {run.stderr.strip()}")
    return run


def in_git(target):
    return git(target, "rev-parse", "--is-inside-work-tree", check=False).stdout.strip() == "true"


def tracked(target, rel_dir):
    out = git(target, "ls-files", "-z", "--", rel_dir).stdout
    return {p for p in out.split("\0") if p}


def changed(target, paths):
    """Paths among `paths` (tracked ones) that already differ from the last commit."""
    if not paths:
        return []
    out = git(target, "status", "--porcelain=v1", "-z", "--untracked-files=no", "--", *paths).stdout
    entries = [e for e in out.split("\0") if e]
    return sorted({e[3:] for e in entries if len(e) > 3})


# --- the migration ---------------------------------------------------------------------------

def model_new_path(rel, model_rel):
    """new_path for a target-relative path, renaming only the parts inside the model folder."""
    if rel == model_rel:
        return rel
    return model_rel + "/" + new_path(rel[len(model_rel) + 1:])


def snapshot(model):
    """Every folder, file and link under the model, held in memory, so a failed run can put it back."""
    entries = []
    for d, dirs, names in os.walk(model):
        for n in sorted(dirs + names):
            full = os.path.join(d, n)
            rel = os.path.relpath(full, model)
            if os.path.islink(full):
                entries.append(("link", rel, os.readlink(full), None))
            elif os.path.isdir(full):
                entries.append(("dir", rel, None, os.stat(full).st_mode))
            else:
                with open(full, "rb") as fh:
                    entries.append(("file", rel, fh.read(), os.stat(full).st_mode))
    return entries, os.stat(model).st_mode


def restore(model, snap):
    entries, mode = snap
    if os.path.lexists(model):
        shutil.rmtree(model)
    os.makedirs(model)
    os.chmod(model, mode & 0o7777)
    for kind, rel, data, m in entries:  # os.walk is top-down: a folder comes before what it holds
        full = os.path.join(model, rel)
        if kind == "dir":
            os.makedirs(full, exist_ok=True)
        elif kind == "link":
            os.symlink(data, full)
        else:
            with open(full, "wb") as fh:
                fh.write(data)
        if kind != "link":
            os.chmod(full, m & 0o7777)


def walk(model, target):
    files, folders = [], []
    for d, dirs, names in os.walk(model):
        dirs[:] = sorted(x for x in dirs if x != ".git")
        for x in dirs:
            if x in FOLDERS:
                folders.append(os.path.relpath(os.path.join(d, x), target).replace(os.sep, "/"))
        for n in sorted(names):
            files.append(os.path.relpath(os.path.join(d, n), target).replace(os.sep, "/"))
    return files, folders


def refuse_if_both(model):
    spine = os.path.join(model, "_spine.yaml")
    if not os.path.isfile(spine):
        return
    text = open(spine, encoding="utf-8").read()
    if re.search(r"^functionalities\s*:", text, re.M) and re.search(r"^features\s*:", text, re.M):
        raise Refused(f"the spine ({spine}) holds both `functionalities:` and `features:`. "
                      "A person must merge them into `features:` by hand; nothing was moved.")


def migrate(target):
    target = os.path.abspath(target)
    report = {"moved": {"keys": [], "files": [], "folders": [], "headings": []},
              "committed": False, "commit": None, "reason": ""}
    model = model_dir(target)
    if not os.path.isdir(model):
        report["reason"] = "no product model (no product-os folder); nothing to move"
        return report
    refuse_links_outside(model, target)
    refuse_if_both(model)

    files, folders = walk(model, target)
    model_rel = os.path.relpath(model, target).replace(os.sep, "/")
    moves = [(f, model_new_path(f, model_rel)) for f in files if model_new_path(f, model_rel) != f]
    for old, new in moves:
        if os.path.exists(os.path.join(target, new)):
            raise Refused(f"{old} would move onto {new}, which exists. A person must merge the two; "
                          "nothing was moved.")

    # what each text file becomes
    edits = {}
    for f in files:
        full = os.path.join(target, f)
        if not f.endswith(YAML_EXT + (".md",)):
            continue
        try:
            text = open(full, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        if f.endswith(".md"):
            new_text, keys, heads = rewrite_markdown(text)
        else:
            lines, keys = rewrite_yaml_lines(text.splitlines(keepends=True))
            new_text, heads = "".join(lines), []
        if new_text != text:
            edits[f] = (new_text, keys, heads)

    if not moves and not edits:
        report["reason"] = "the product model already uses the new names; nothing to move"
        return report

    use_git = in_git(target)
    known = tracked(target, model_rel) if use_git else set()
    touched_tracked = sorted({old for old, _ in moves if old in known} | {f for f in edits if f in known})
    dirty = changed(target, touched_tracked) if use_git else []

    snap = snapshot(model)
    stage = []
    try:
        return _apply(target, model, model_rel, moves, folders, edits, use_git, known,
                      touched_tracked, dirty, stage, report)
    except Exception as e:  # any failed step: put the model back as it was, and stage nothing
        why = str(e) or e.__class__.__name__
        try:
            restore(model, snap)
            if use_git and stage:
                git(target, "reset", "-q", "--", *stage, check=False)
        except Exception as undo:
            raise Failed(f"{why}; and putting the model back failed too: {undo}. "
                         "The model folder may be part-moved; restore it from git.") from None
        raise Failed(why + "; every move and edit was undone, nothing was committed") from None


def _apply(target, model, model_rel, moves, folders, edits, use_git, known, touched_tracked, dirty,
           stage, report):
    # 1. move files (git sees each move as a rename when the paths are staged in step 4)
    for old, new in moves:
        os.makedirs(os.path.dirname(os.path.join(target, new)), exist_ok=True)
        shutil.move(os.path.join(target, old), os.path.join(target, new))
    # 2. move what is left in old folders (empty folders, ignored files), deepest first
    for d in sorted(folders, key=lambda p: -p.count("/")):
        full = os.path.join(target, d)
        if not os.path.isdir(full):
            continue
        dest = os.path.join(target, model_new_path(d, model_rel))
        os.makedirs(dest, exist_ok=True)
        for name in os.listdir(full):
            shutil.move(os.path.join(full, name), os.path.join(dest, name))
        os.rmdir(full)
    # 3. rewrite keys and headings, in each file's new place
    moved_to = dict(moves)
    for f, (new_text, keys, heads) in sorted(edits.items()):
        dest = moved_to.get(f, f)
        with open(os.path.join(target, dest), "w", encoding="utf-8") as fh:
            fh.write(new_text)
        counts = {}
        for pair in keys:
            counts[pair] = counts.get(pair, 0) + 1
        for (o, n), c in counts.items():
            report["moved"]["keys"].append({"file": dest, "from": o, "to": n, "count": c})
        for o, n in heads:
            report["moved"]["headings"].append({"file": dest, "from": o, "to": n})
    report["moved"]["files"] = [{"from": o, "to": n} for o, n in moves
                                if os.path.basename(o) != os.path.basename(n)]
    report["moved"]["folders"] = [{"from": d, "to": model_new_path(d, model_rel)} for d in folders]

    # 4. one commit, holding only the paths this moved or changed
    if not use_git:
        report["reason"] = "moved, but not committed: the target is not a git repository"
        return report
    if dirty:
        report["reason"] = ("moved, but not committed: these paths had changes of their own before the "
                            "move, so a commit would mix them in: " + ", ".join(dirty))
        return report
    if not touched_tracked:
        report["reason"] = "moved, but not committed: none of the moved paths is tracked by git"
        return report
    stage.extend(sorted({moved_to.get(p, p) for p in touched_tracked} | {o for o, _ in moves if o in known}))
    git(target, "add", "-A", "--", *stage)
    run = git(target, "commit", "-q", "-m", COMMIT_MESSAGE, "--", *stage, check=False)
    if run.returncode != 0:
        raise RuntimeError("the commit failed: " + (run.stderr.strip() or run.stdout.strip()
                                                     or f"git commit exited {run.returncode}"))
    report["committed"] = True
    report["commit"] = git(target, "rev-parse", "HEAD").stdout.strip()
    report["reason"] = "moved and committed"
    return report


def summary(report):
    if report.get("refused") or report.get("failed"):
        return "model: not moved — " + report["reason"]
    m = report["moved"]
    if not any(m.values()):
        return "model: " + report["reason"]
    keys = sum(k["count"] for k in m["keys"])
    line = (f"model: moved to the #807 names — {keys} key(s), {len(m['files'])} page file(s), "
            f"{len(m['folders'])} folder(s), {len(m['headings'])} heading(s)")
    return line + (f"; committed {report['commit'][:8]}" if report["committed"] else f"; {report['reason']}")


def _empty(reason, **flag):
    return {"moved": {"keys": [], "files": [], "folders": [], "headings": []},
            "committed": False, "commit": None, "reason": reason, **flag}


def run(target):
    """The report, never an exception: a refusal or a failure is in the report."""
    try:
        return migrate(target)
    except Refused as e:
        return _empty(str(e), refused=True)
    except Failed as e:
        return _empty(str(e), failed=True)
    except Exception as e:  # a step before any move failed (an unreadable file, git missing)
        return _empty(f"{e.__class__.__name__}: {e}; nothing was moved", failed=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Move a project's product model to the #807 names.")
    ap.add_argument("--target", required=True, help="the project directory")
    ap.add_argument("--summary", action="store_true", help="print one plain line instead of the JSON report")
    args = ap.parse_args(argv)
    report = run(args.target)
    if report.get("refused") or report.get("failed"):
        sys.stderr.write("migrate_model.py: " + report["reason"] + "\n")
    print(summary(report) if args.summary else json.dumps(report, indent=2))
    sys.exit(2 if report.get("refused") else 1 if report.get("failed") else 0)


if __name__ == "__main__":
    main()
