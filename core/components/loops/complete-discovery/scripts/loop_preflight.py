#!/usr/bin/env python3
"""loop_preflight.py — a loop's pre-flight facts, as JSON (Shared Loop Run, step R1).

The mechanical hand of a loop's pre-flight. It reads the config and the installed plays, and
returns facts; the loop keeps the policy (what halts). Canonical copy lives at
create-loop/references/loop_preflight.py and is stamped into each loop's scripts/.

    python3 loop_preflight.py --config .garura/core/config.yaml --loop discovery \
        --skills-root .. --plays intent,vision,understand --branch "<current branch>" \
        --out <working>/preflight.json

Facts: `stm_base`; `runner` (`loops.<loop>.runner`, default `subagent`); `checker`
(`loops.<loop>.checker`, kind default `subagent`; a sub-agent checker must name its model); `evidence_record`
(`evidence.plays.<loop>`, else `evidence.record`, else true); `on_default_branch`; and
`plays_ok` with `missing` (no SKILL.md under the skills root) and `no_contract` (a play that
does not check a loop contract, so it cannot run inside a loop) — the loop's plays and the
member plays every loop runs (`search-knowledge`, `research-knowledge`, `check-knowledge`).

Exit 0 — facts written and every play is present and accepts a contract. Exit 2 — the config
cannot be read, a play is missing or cannot run inside a loop, or the runner is unknown: the
loop halts and says why. Reads files only; no git, gh or network. Standard library only.
"""
import argparse
import json
import os
import sys

RUNNERS = ("subagent", "headless")
CHECKERS = ("subagent", "coding-agent")
DEFAULT_BRANCHES = {"main", "master"}
CONTRACT_MARK = "check_loop_contract"
MEMBERS = ("search-knowledge", "research-knowledge", "check-knowledge")  # member plays every loop runs (R5c, R5b)


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


def resolve(cfg, loop, skills_root, plays, branch):
    ev_loop = get(cfg, "evidence", "plays", loop)
    ev_global = get(cfg, "evidence", "record")
    evidence = ev_loop if ev_loop is not None else (ev_global if ev_global is not None else True)
    checker = get(cfg, "loops", loop, "checker", default={})
    checker = checker if isinstance(checker, dict) else {"kind": checker}
    missing, no_contract = check_plays(skills_root, list(plays) + [m for m in MEMBERS if m not in plays])
    return {
        "loop": loop,
        "stm_base": get(cfg, "stm", "base-path"),
        "runner": get(cfg, "loops", loop, "runner", default="subagent"),
        "checker": {"kind": checker.get("kind", "subagent"), "model": checker.get("model")},
        "evidence_record": bool(evidence),
        "old_settings": get(cfg, "drives") is not None and get(cfg, "loops", loop) is None,
        "branch": branch,
        "on_default_branch": branch in DEFAULT_BRANCHES,
        "plays": plays,
        "plays_ok": not missing and not no_contract,
        "missing": missing,
        "no_contract": no_contract,
    }


def problems(facts):
    out = []
    if facts.get("old_settings"):
        out.append(f"the config still has the old `drives:` block and no `loops.{facts['loop']}` block — "
                   f"rename it to `loops:` (ADR 045: Kickoff is now `discovery`; also rename "
                   f"`evidence.plays.kickoff` to `evidence.plays.{facts['loop']}`)")
    if facts["missing"]:
        out.append(f"these plays are not installed: {', '.join(facts['missing'])}")
    if facts["no_contract"]:
        out.append(f"these plays cannot run inside a loop (they check no loop contract): "
                   f"{', '.join(facts['no_contract'])}")
    if facts["runner"] not in RUNNERS:
        out.append(f"loops.{facts['loop']}.runner is `{facts['runner']}`; "
                   f"it must be one of {', '.join(RUNNERS)}")
    if facts["checker"]["kind"] not in CHECKERS:
        out.append(f"loops.{facts['loop']}.checker.kind is `{facts['checker']['kind']}`; "
                   f"it must be one of {', '.join(CHECKERS)}")
    if facts["checker"]["kind"] == "subagent" and not facts["checker"]["model"]:
        out.append(f"loops.{facts['loop']}.checker.model is not set — a sub-agent checker runs on "
                   f"a model that is not the session's, so name it (e.g. sonnet)")
    if not facts["stm_base"]:
        out.append("the config has no stm.base-path")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Resolve a loop's pre-flight facts.")
    ap.add_argument("--config", default=".garura/core/config.yaml")
    ap.add_argument("--loop", required=True)
    ap.add_argument("--skills-root", required=True, help="where the installed plays sit")
    ap.add_argument("--plays", required=True, help="the loop's plays, comma-separated, in the order they run")
    ap.add_argument("--branch", default="")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    plays = [p.strip() for p in args.plays.split(",") if p.strip()]
    try:
        with open(args.config, encoding="utf-8") as fh:
            cfg = parse_config(fh.read())
    except OSError as exc:
        sys.stderr.write(f"loop_preflight.py: cannot read {args.config}: {exc.__class__.__name__}\n")
        return 2
    facts = resolve(cfg, args.loop, args.skills_root, plays, args.branch)
    facts["problems"] = problems(facts)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(facts, fh, indent=2)
    print(json.dumps(facts, indent=2))
    for p in facts["problems"]:
        sys.stderr.write(f"loop_preflight.py: {p}\n")
    return 2 if facts["problems"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
