#!/usr/bin/env python3
"""drive_preflight.py — a drive's pre-flight facts, as JSON (Shared Drive Run, step R1).

The mechanical hand of a drive's pre-flight. It reads the config and the installed plays, and
returns facts; the drive keeps the policy (what halts). Canonical copy lives at
drive-creator/references/drive_preflight.py and is stamped into each drive's scripts/.

    python3 drive_preflight.py --config .garura/core/config.yaml --drive kickoff \
        --skills-root .. --plays intent,vision,understand --branch "<current branch>" \
        --out <working>/preflight.json

Facts: `stm_base`; `runner` (`drives.<drive>.runner`, default `subagent`); `checker`
(`drives.<drive>.checker`, kind default `subagent`; a sub-agent checker must name its model); `evidence_record`
(`evidence.plays.<drive>`, else `evidence.record`, else true); `on_default_branch`; and
`plays_ok` with `missing` (no SKILL.md under the skills root) and `no_contract` (a play that
does not check a drive contract, so it cannot run inside a drive) — the drive's plays and the
member plays every drive runs (`search-knowledge`, `build-knowledge`, `review-knowledge`).

Exit 0 — facts written and every play is present and accepts a contract. Exit 2 — the config
cannot be read, a play is missing or cannot run inside a drive, or the runner is unknown: the
drive halts and says why. Reads files only; no git, gh or network. Standard library only.
"""
import argparse
import json
import os
import sys

RUNNERS = ("subagent", "headless")
CHECKERS = ("subagent", "coding-agent")
DEFAULT_BRANCHES = {"main", "master"}
CONTRACT_MARK = "check_drive_contract"
MEMBERS = ("search-knowledge", "build-knowledge", "review-knowledge")  # member plays every drive runs (R5c, R5b)


def parse_config(text):
    """The nested `key: value` YAML the config uses, as a dict (no lists, no anchors)."""
    root = {}
    stack = [(-1, root)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        cut = line.find(" #")
        if cut != -1:
            line = line[:cut].rstrip()
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if val == "":
            parent[key] = {}
            stack.append((indent, parent[key]))
        else:
            val = val.strip("'\"")
            parent[key] = {"true": True, "false": False}.get(val.lower(), val)
    return root


def get(cfg, *path, default=None):
    cur = cfg
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


def check_plays(skills_root, plays):
    """(missing, no_contract): plays with no SKILL.md, and plays that check no contract."""
    missing, no_contract = [], []
    for play in plays:
        md = os.path.join(skills_root, play, "SKILL.md")
        if not os.path.isfile(md):
            missing.append(play)
            continue
        with open(md, encoding="utf-8") as fh:
            if CONTRACT_MARK not in fh.read():
                no_contract.append(play)
    return missing, no_contract


def resolve(cfg, drive, skills_root, plays, branch):
    ev_drive = get(cfg, "evidence", "plays", drive)
    ev_global = get(cfg, "evidence", "record")
    evidence = ev_drive if ev_drive is not None else (ev_global if ev_global is not None else True)
    checker = get(cfg, "drives", drive, "checker", default={})
    checker = checker if isinstance(checker, dict) else {"kind": checker}
    missing, no_contract = check_plays(skills_root, list(plays) + [m for m in MEMBERS if m not in plays])
    return {
        "drive": drive,
        "stm_base": get(cfg, "stm", "base-path"),
        "runner": get(cfg, "drives", drive, "runner", default="subagent"),
        "checker": {"kind": checker.get("kind", "subagent"), "model": checker.get("model")},
        "evidence_record": bool(evidence),
        "branch": branch,
        "on_default_branch": branch in DEFAULT_BRANCHES,
        "plays": plays,
        "plays_ok": not missing and not no_contract,
        "missing": missing,
        "no_contract": no_contract,
    }


def problems(facts):
    out = []
    if facts["missing"]:
        out.append(f"these plays are not installed: {', '.join(facts['missing'])}")
    if facts["no_contract"]:
        out.append(f"these plays cannot run inside a drive (they check no drive contract): "
                   f"{', '.join(facts['no_contract'])}")
    if facts["runner"] not in RUNNERS:
        out.append(f"drives.{facts['drive']}.runner is `{facts['runner']}`; "
                   f"it must be one of {', '.join(RUNNERS)}")
    if facts["checker"]["kind"] not in CHECKERS:
        out.append(f"drives.{facts['drive']}.checker.kind is `{facts['checker']['kind']}`; "
                   f"it must be one of {', '.join(CHECKERS)}")
    if facts["checker"]["kind"] == "subagent" and not facts["checker"]["model"]:
        out.append(f"drives.{facts['drive']}.checker.model is not set — a sub-agent checker runs on "
                   f"a model that is not the session's, so name it (e.g. sonnet)")
    if not facts["stm_base"]:
        out.append("the config has no stm.base-path")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Resolve a drive's pre-flight facts.")
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--drive", required=True)
    ap.add_argument("--skills-root", required=True, help="where the installed plays sit")
    ap.add_argument("--plays", required=True, help="the drive's plays, comma-separated, in the order they run")
    ap.add_argument("--branch", default="")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    plays = [p.strip() for p in args.plays.split(",") if p.strip()]
    try:
        with open(args.config, encoding="utf-8") as fh:
            cfg = parse_config(fh.read())
    except OSError as exc:
        sys.stderr.write(f"drive_preflight.py: cannot read {args.config}: {exc.__class__.__name__}\n")
        return 2
    facts = resolve(cfg, args.drive, args.skills_root, plays, args.branch)
    facts["problems"] = problems(facts)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(facts, fh, indent=2)
    print(json.dumps(facts, indent=2))
    for p in facts["problems"]:
        sys.stderr.write(f"drive_preflight.py: {p}\n")
    return 2 if facts["problems"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
