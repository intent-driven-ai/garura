#!/usr/bin/env python3
"""
install.py — install Garura into a target project, for a chosen host tool.

The mechanical hand of the `install-garura` play. The play decides and
reports; this script does the deterministic file work.

Model
-----
This installs THIS garura checkout into a **target** project — a directory the
user names. It reads garura's `core/components/` (agents, skills, plays, memory)
and the source `core/config.yaml` + the project instructions, and lays them down so a
host coding tool can discover them in the target.

    python3 install.py --target <path> [--tool claude] [--scope full|harness]

  --target        the project directory to install into (a path, created if absent)
  --tool          which host tool to target: claude (default). codex is deprecated (#863):
                  it stops at once with a plain message and changes nothing
  --scope         which component set to install: full (default, every
                  component except the meta harness plays and the harness-only
                  skills) or harness (meta plays + harness-only skills + change
                  chain + discover-capabilities + their workers only)
  --source        the garura checkout to install FROM (auto-derived if omitted)
  --memory-dest   where shared memory goes (default ~/.garura/core/memory)
  --force-config  overwrite an existing target .garura/core/config.yaml
  --quiet         less output

Adapters
--------
The per-tool transform is NOT here. It lives in `adapters/<tool>.py`, and this
orchestrator selects one by `--tool` and delegates the host surface to it:

  - claude: resolves model tiers to Claude models, lays `.claude/skills` +
    `.claude/agents`, writes CLAUDE.md.
  - codex: lays `.agents/skills` (skills, plays, AND agents — Codex has no agent
    type), writes AGENTS.md, and writes model/sandbox/approval profiles into the
    Codex home so the tier the user wanted is actually selectable.

The orchestrator owns the tool-agnostic work: shared memory, garura's own
`.garura/core/config.yaml`, the STM scaffold, and the install manifest.

The orchestrator also lays the memory system (`memory_system.py`, shared with the public
installer): the memory tool in `.garura/core/tools/memory/` with its settings, short-term
memory's folder, and the memory guide where the host tool loads it for every agent. It then
checks the tool runs and reaches the project's tiers. The install brings no memory.

It also lays every other tool (`tools_system.py`, shared with the public installer) in
`.garura/core/tools/<name>/`, because plays and skills run them after the install.

The install never changes a product model the project already has (#813).

Exit: 0 = installed, 1 = installed but the memory check failed, 2 = bad input /
prerequisite missing.
Idempotent: re-running re-lays garura in place; it never duplicates.
"""

import argparse
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import memory_system  # noqa: E402
import tools_system  # noqa: E402
from adapters import common, get_adapter, known  # noqa: E402


def fail(msg):
    sys.stderr.write(f"install.py: {msg}\n")
    sys.exit(2)


# The Codex installer is deprecated (#863): it is to be redesigned completely. Until then an
# install for Codex stops at once and changes nothing in the target.
DEPRECATED_TOOLS = {
    "codex": ("the Codex installer is deprecated and installs nothing (#863: it is being "
              "redesigned). Install for Claude Code with --tool claude, or wait for #863."),
}


def stop_if_deprecated(tool):
    """Stop with a plain message, before anything is written, when the tool is deprecated."""
    if tool in DEPRECATED_TOOLS:
        fail(DEPRECATED_TOOLS[tool])


def info(quiet, msg):
    if not quiet:
        print(msg)


# --- locate the garura checkout (source root) ---------------------------------

def config_source(root):
    """The config's source: core/config.yaml (ADR 040); a checkout made before it keeps it at
    .garura/core/config.yaml."""
    path = os.path.join(root, "core", "config.yaml")
    return path if os.path.isfile(path) else os.path.join(root, ".garura", "core", "config.yaml")


def derive_source_root(explicit):
    """Find the garura checkout — holds core/components/ and core/config.yaml.

    With --source, trust it. Otherwise walk up from this script until a parent
    looks like a garura checkout.
    """
    def looks_like_garura(root):
        return (os.path.isdir(os.path.join(root, "core", "components"))
                and os.path.isfile(config_source(root)))

    if explicit:
        root = os.path.abspath(explicit)
        if not looks_like_garura(root):
            fail(f"{root} is not a garura checkout (need core/components/ and "
                 f"core/config.yaml)")
        return root
    here = os.path.dirname(os.path.abspath(__file__))
    cur = here
    while True:
        if looks_like_garura(cur):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            fail(f"could not find a garura checkout above {here} — "
                 f"pass --source <garura-checkout>")
        cur = parent


# --- config transform ---------------------------------------------------------

# where each host tool installs components, for garura's own config.yaml pointers
_COMPONENT_PATHS = {
    "claude": {"skills": "./.claude/skills/", "plays": "./.claude/skills/",
               "loops": "./.claude/skills/", "agents": "./.claude/agents/"},
    "codex": {"skills": "./.agents/skills/", "plays": "./.agents/skills/",
              "loops": "./.agents/skills/", "agents": "./.agents/skills/"},
}


def transform_config(content, project_name, tool):
    """Transform garura's own config for a target project + host tool.

    name->project name, type->Project, component paths->the tool's install
    location, and drop the platform/github lines (a fresh project sets its own).
    """
    cp = _COMPONENT_PATHS[tool]
    out_lines = []
    skip_github_block = False
    for line in content.splitlines():
        if re.match(r"^github:", line):
            skip_github_block = True
            continue
        if skip_github_block:
            if re.match(r"^\s+\S", line):  # still inside the block
                continue
            skip_github_block = False  # fall through to handle this line
        if re.match(r"^platform:", line):
            continue
        line = re.sub(r"^(\s*name:\s*).+$", r"\1" + project_name, line)
        line = re.sub(r"^(\s*type:\s*).+$", r"\1Project", line)
        line = re.sub(r"^(\s*skills:\s*).+$", r"\1" + cp["skills"], line)
        line = re.sub(r"^(\s*plays:\s*).+$", r"\1" + cp["plays"], line)
        line = re.sub(r"^(\s*loops:\s*).+$", r"\1" + cp["loops"], line)
        line = re.sub(r"^(\s*agents:\s*).+$", r"\1" + cp["agents"], line)
        out_lines.append(line)
    text = "\n".join(out_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


# Status / resume markers are machine-local and never committed (ADR 021). This
# ignore file ships inside the .garura tree so the rule travels with every install,
# covering every status location under it (issue, realize, shaping, product _status).
STATUS_GITIGNORE = (
    "# Status / resume markers — machine-local, never committed (ADR 021).\n"
    "# Plays write these to resume; they sit locally and are never shared via git.\n"
    "# The durable record is the evidence system (_evidence/), never these.\n"
    "**/status/\n"
    "**/_status/\n"
    "# Python's caches beside the installed tools' scripts — never part of a change (#613).\n"
    "**/__pycache__/\n"
)


def portable(path):
    """A path fit to commit: under the home folder it is written `~/…`, so a project's install
    record never carries a person's home folder (#613 finding K-0). Uninstall expands it."""
    home = os.path.expanduser("~")
    if path == home or path.startswith(home + os.sep):
        return "~" + path[len(home):]
    return path


# --- install scopes -----------------------------------------------------------

# A scope names WHICH components a target receives; everything else about the
# install (shared memory, config, STM scaffold, manifest) is unchanged. `full`
# is the default and installs every component EXCEPT the meta harness plays and the
# harness-only skills — a product project's ADLC has no use for garura's own build tooling. `harness`
# is for garura-style harness repos that must carry only the meta plays, the
# change chain, and the workers those plays dispatch — nothing product-facing.
# Membership is explicit and deterministic: when a kept play gains a new
# worker skill or agent, add it here in the same change.

# The meta harness plays are garura's own build tooling — they compile and deploy
# garura itself. A product project's ADLC has no use for them, so no target ever
# receives them under `full`. (`harness` is an explicit allow-list and names the
# two it does want.)
META_PLAYS = {"create-play", "edit-play", "create-loop", "edit-loop",
              "install-garura", "uninstall-garura", "edit-ontology"}
# Harness-only skills are the workers of the meta plays (edit-ontology runs
# author-product-ontology, #777). Plays run them; no person does (#778). Never installed under `full`.
META_SKILLS = {"author-product-ontology"}

SCOPES = {
    "full": None,  # marker only — resolved at run time by resolve_scope()
    "harness": {
        "plays": {
            "create-play", "edit-play",
            # loops are built and changed the same way as plays (#613)
            "create-loop", "edit-loop",
            "start-change", "commit-change", "propose-change",
            "check-change", "merge-change",
            # list-focus-issues is harness-class: it reads the HOST REPO's issue tracker, so it
            # works in a harness repo exactly as it does in a product one. Its only
            # workers are platform-adapter + project-orchestrator, both already kept.
            "list-focus-issues",
            # record-decision manages a repo's decision records — a harness repo's own ADRs too (#632).
            # Its workers: adr-keeper + author-decision, and the change chain already kept.
            "record-decision",
            # discover-capabilities writes the full ICE for Garura's own capabilities and
            # features, now that Garura plans its work with its product model (#753).
            # Its workers: product-os-keeper + find-work-placement, enrich-capability-ice,
            # judge-grounding; template-manager is already kept.
            "discover-capabilities",
            # edit-ontology changes the product ontology with the product owner (#777).
            # Its workers: product-os-keeper + author-product-ontology, both already kept.
            "edit-ontology",
            # shape-slice shapes the slice for each of Garura's own business intents (plan 788).
            # Its workers: product-os-keeper + the skills listed below; template-manager is kept.
            "shape-slice",
        },
        # a harness repo builds loops but runs none: no product loop installs there
        "loops": set(),
        "skills": {
            "assess-changes", "assess-pr", "commit-files", "track-issue",
            "merge-pr", "platform-adapter", "check-pr-quality",
            "find-matching-issues", "cut-branch", "open-pr",
            "author-product-ontology", "author-decision",
            "find-work-placement", "enrich-capability-ice", "judge-grounding",
            # the skills shape-slice calls (#842)
            "author-business-intent", "author-domains", "propose-answers", "author-slice",
            "find-slice-gaps", "author-slice-brief", "enrich-grounding", "author-failure-recovery",
        },
        "agents": {
            "change-reviewer", "project-orchestrator",
            "quality-auditor", "repo-orchestrator", "adr-keeper",
            # every play's close asks template-manager for its templates (ADR 039 §8–9)
            "template-manager",
            "product-os-keeper",
        },
    },
}


def resolve_scope(scope, components):
    """Per-kind allow sets for an install scope.

    A value of None for a kind means "install every component of that kind".
    `harness` is a fixed allow-list. `full` is everything on disk EXCEPT the
    meta harness plays and the harness-only skills, so it is resolved against the
    source tree at run time.
    """
    if scope != "full":
        return SCOPES[scope]
    plays_dir = os.path.join(components, "plays")
    plays = set(os.listdir(plays_dir)) if os.path.isdir(plays_dir) else set()
    skills_dir = os.path.join(components, "skills")
    skills = set(os.listdir(skills_dir)) if os.path.isdir(skills_dir) else set()
    return {"plays": plays - META_PLAYS, "loops": None,
            "skills": skills - META_SKILLS, "agents": None}


# --- the install --------------------------------------------------------------

def component_kinds(components, paths):
    """The kind of each component laid (play, loop, skill or agent), by where it sits in the
    source. Plays, loops and skills share one installed folder, so the folder alone cannot tell
    them apart; the linter's installed layout reads this record (#860)."""
    kinds = {}
    for rel in paths:
        head, name = os.path.split(rel.rstrip("/"))
        if name.startswith((".", "_")):
            continue
        if os.path.basename(head) == "agents" and name.endswith(".md"):
            kinds[rel] = "agent"
            continue
        for kind, folder in (("play", "plays"), ("loop", "loops"), ("skill", "skills"), ("agent", "agents")):
            if os.path.isdir(os.path.join(components, folder, name)) or \
                    os.path.isfile(os.path.join(components, folder, name + ".md")):
                kinds[rel] = kind
                break
    return kinds


def install(source, target, tool, force, quiet, memory_dest, scope="full",
            phoenix_place=memory_system.PHOENIX_PLACE, phoenix_source=memory_system.PHOENIX_SOURCE):
    stop_if_deprecated(tool)
    adapter = get_adapter(tool)
    components = os.path.join(source, "core", "components")
    if not os.path.isdir(components):
        fail(f"garura checkout at {source} has no core/components/")

    def _info(msg):
        info(quiet, msg)

    record = {
        "tool": tool,
        "scope": scope,
        "components": [],
        "counts": {},
        "instruction_surface": None,
        "config": None,
        "memory": None,
        "global_files": [],
        "tools": [],
    }

    # 1. components — the host surface, owned by the adapter; the scope filter
    #    decides which components the adapter may lay down
    allow = resolve_scope(scope, components)
    paths, counts, _ = adapter.lay_components(components, target, _info, allow=allow)
    record["components"] = paths
    record["counts"] = counts
    record["kinds"] = component_kinds(components, paths)

    # 2. machine-global host config (Codex profiles; Claude: none)
    record["global_files"] = adapter.write_global_config(_info)

    # 3. shared memory — machine-global, tool-agnostic
    src = os.path.join(components, "memory")
    if os.path.isdir(src):
        mem_dest = os.path.abspath(os.path.expanduser(memory_dest))
        common.copy_tree_merge(src, mem_dest)
        record["memory"] = portable(mem_dest)
        _info(f"  memory: {mem_dest}")

    # 4. target-local garura config.yaml (transformed from the source core/config.yaml, ADR 040);
    #    keep existing unless forced
    proj_core = os.path.join(target, ".garura", "core")
    os.makedirs(proj_core, exist_ok=True)
    cfg_dest = os.path.join(proj_core, "config.yaml")
    project_name = os.path.basename(os.path.abspath(target))
    src_cfg = config_source(source)
    if os.path.isfile(src_cfg):
        if os.path.isfile(cfg_dest) and not force:
            _info("  config: kept existing")
        else:
            transformed = transform_config(common.read_text(src_cfg), project_name, tool)
            common.write_text(cfg_dest, transformed)
            _info("  config: wrote .garura/core/config.yaml")
        record["config"] = ".garura/core/config.yaml"

    # 5. target STM scaffold: the memory system lays short-term memory, .garura/project/issues/
    #    (memory_system.py); .garura/project/specs/ is not part of the layout (ADR 039 §5)

    # 5b. status-marker ignore rule — keeps machine-local resume files out of git
    #     (ADR 021). Idempotent; overwritten on re-run to stay current with source.
    common.write_text(os.path.join(target, ".garura", ".gitignore"), STATUS_GITIGNORE)
    record["status_gitignore"] = ".garura/.gitignore"
    _info("  scaffold: wrote .garura/.gitignore (status markers)")

    # 6. instruction surface (CLAUDE.md / AGENTS.md) — owned by the adapter
    # The project's own instructions — not Garura's development guide (the repository's
    # CLAUDE.md), which would put how Garura is built into every agent of the project (#689).
    src_md = os.path.join(source, "core", "components", "plays", "install-garura", "project-instructions.md")
    if os.path.isfile(src_md):
        record["instruction_surface"] = adapter.write_instruction_surface(
            common.read_text(src_md), project_name, target, _info)

    # 7. the memory system (ADR 035 §8): the tool, its settings, short-term memory's folder
    #    and the guide every agent reads — then a check that the tool runs and reaches the
    #    project's tiers. The install brings no memory: the tool downloads Phoenix memory
    #    the first time it needs it.
    record["memory_system"] = memory_system.lay(source, target, tool, phoenix_place, phoenix_source, _info)
    record["memory_system"]["check"] = memory_system.check(target, _info)

    # 8. the tools (decision 6 of #860): every tool but the memory tool (laid above) and the
    #    play-reviewer prototype, in .garura/core/tools/<name>/
    record["tools"] = tools_system.lay(source, target, _info)

    return record


def retire_stale(target, new_paths, quiet):
    """Manifest-driven retirement: a component the PREVIOUS install placed that
    this install did not re-place was renamed or retired in source — remove it,
    so renames/retirements never leave stale copies in the target (the
    grill-me / sud-install-garura lesson, #434). Only paths the prior manifest
    recorded are ever candidates — user-owned files are invisible to this —
    and only paths inside the target are ever touched. Must run BEFORE the new
    manifest overwrites the prior one."""
    path = os.path.join(target, ".garura", "install-manifest.json")
    if not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8") as fh:
            prior_record = json.load(fh).get("record") or {}
        prior = (prior_record.get("components") or []) + (prior_record.get("tools") or [])
    except (OSError, ValueError):
        return []
    base = os.path.abspath(target)
    removed = []
    for rel in sorted(set(prior) - set(new_paths)):
        full = os.path.normpath(os.path.join(base, rel))
        if not full.startswith(base + os.sep):
            continue  # never step outside the target
        if os.path.isdir(full):
            shutil.rmtree(full)
            removed.append(rel)
        elif os.path.isfile(full):
            os.remove(full)
            removed.append(rel)
    for rel in removed:
        info(quiet, f"  retired: {rel} (placed by a previous install, no longer in source)")
    return removed


def retire_renamed(source, target, new_paths, quiet):
    """Rename-map retirement (#748): a component a Garura install placed under its OLD name
    (standards/rules/rename-map.yaml) is removed once its new name is laid. It covers projects
    installed before the install manifest existed, which retire_stale cannot see. A path is
    removed only when its file still says `name: <old name>` — proof Garura placed it; a
    folder the project wrote itself never carries Garura's old name line."""
    map_path = os.path.join(source, "core", "components", "memory", "standards", "rules", "rename-map.yaml")
    if not os.path.isfile(map_path):
        return []
    import yaml
    with open(map_path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    new_to_old = {}  # one new name can have several old ones (two old play names lead to shape-slice)
    for kind in ("plays", "loops", "skills", "agents"):
        for old, new in (data.get(kind) or {}).items():
            new_to_old.setdefault(new, []).append(old)
    base = os.path.abspath(target)
    removed = []
    for rel in new_paths:
        head, last = os.path.split(rel.rstrip("/"))
        stem, ext = os.path.splitext(last) if last.endswith(".md") else (last, "")
        for old in new_to_old.get(stem, []):
            old_rel = os.path.join(head, old + ext)
            full = os.path.normpath(os.path.join(base, old_rel))
            if not full.startswith(base + os.sep) or not os.path.exists(full):
                continue
            marker = full if ext else os.path.join(full, "SKILL.md")
            try:
                text = open(marker, encoding="utf-8").read()
            except OSError:
                continue
            if not re.search(rf"^name:\s*(?:garura:)?{re.escape(old)}\s*$", text, re.M):
                continue
            if os.path.isdir(full):
                shutil.rmtree(full)
            else:
                os.remove(full)
            removed.append(old_rel)
            info(quiet, f"  retired: {old_rel} (old name; now {rel})")
    return removed


def write_manifest(target, record, quiet):
    os.makedirs(os.path.join(target, ".garura"), exist_ok=True)
    path = os.path.join(target, ".garura", "install-manifest.json")
    manifest = {"installer": "install-garura", "version": 2, "record": record}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")
    info(quiet, f"manifest: {path}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Install Garura into a target project.")
    ap.add_argument("--target", required=True, help="project directory to install into (a path)")
    ap.add_argument("--tool", default="claude", choices=known(),
                    help="host tool to target (default: claude; codex is deprecated, #863)")
    ap.add_argument("--scope", default="full", choices=sorted(SCOPES),
                    help="component set to install: full (default, every component "
                         "except the meta harness plays and harness-only skills) or harness "
                         "(meta plays + harness-only skills + change chain + their workers)")
    ap.add_argument("--source", help="garura checkout to install from (auto-derived if omitted)")
    ap.add_argument("--memory-dest", default="~/.garura/core/memory",
                    help="where shared memory goes (default ~/.garura/core/memory)")
    ap.add_argument("--force-config", action="store_true",
                    help="overwrite an existing target .garura/core/config.yaml")
    ap.add_argument("--phoenix-place", default=memory_system.PHOENIX_PLACE,
                    help="where Phoenix memory lives on this machine (default ~/.phoenix/core/memory); "
                         "the memory tool downloads it there the first time it is needed")
    ap.add_argument("--phoenix-source", default=memory_system.PHOENIX_SOURCE,
                    help="where the memory tool downloads Phoenix memory from")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)
    stop_if_deprecated(args.tool)

    source = derive_source_root(args.source)
    target = os.path.abspath(args.target)
    os.makedirs(target, exist_ok=True)

    scoped = "" if args.scope == "full" else f" (scope: {args.scope})"
    info(args.quiet, f"installing garura ({source}) into {target} for {args.tool}{scoped}")
    record = install(source, target, args.tool, args.force_config, args.quiet,
                     args.memory_dest, scope=args.scope,
                     phoenix_place=args.phoenix_place, phoenix_source=args.phoenix_source)
    record["retired"] = retire_stale(target, record["components"] + record["tools"], args.quiet)
    record["retired"] += [r for r in retire_renamed(source, target, record["components"], args.quiet)
                          if r not in record["retired"]]
    write_manifest(target, record, args.quiet)

    c = record["counts"]
    n = c.get("skills", 0) + c.get("plays", 0) + c.get("loops", 0)
    retired = f", retired {len(record['retired'])} stale" if record["retired"] else ""
    if not record["memory_system"]["check"]["ok"]:
        sys.stderr.write("install.py: installed, but the memory check failed (see above) — "
                         "the project's agents cannot use memory until it is fixed\n")
        sys.exit(1)
    info(args.quiet, f"\ndone — installed {c.get('agents', 0)} agent(s) and "
                     f"{n} skill/play/loop(s){retired} into {target} for {args.tool}")


if __name__ == "__main__":
    main()
