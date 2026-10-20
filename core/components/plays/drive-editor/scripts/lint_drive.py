#!/usr/bin/env python3
"""
lint_drive.py — mechanical consistency check for a compiled drive.

A drive is a higher-order play: it runs other plays in a fixed order and carries no rules of
its own (ADR 029 §2). So it gets every check a compiled play gets — reused from
`lint_play.py` (coverage, one recovery per failure, no orphans, required sections, the
shared close, the stop condition, a real fingerprint, the Next line) — plus the drive's own:

  - frontmatter `kind: drive`, and `position: both` (a drive opens and lands its change);
  - the Shared Drive Run anchors, once each, in order, and the shared file exists;
  - the drive's values between the anchors: `drive=`, `plays=`, `questions=`, `runner_key=`,
    `checker_key=` — the keys name the drive's own config (`drives.<drive>.runner|checker`);
  - every play it names exists and checks a drive contract, and none is named twice;
  - every step's owner is the drive, its checker, a play it names, or a change play —
    a step owned by anything else is the drive doing a play's work;
  - a Done means in its ICE, baked into stop-condition.yaml (required for a drive);
  - the shared run's scripts are stamped into scripts/, unchanged from their source;
  - the fingerprint is the sha256 of reference/ice.md as it is now;
  - the config sets the drive's runner, checker kind, and evidence recording on;
  - each play has its own step and its own done clause (`<play>-done.json`);
  - every input the drive hands a play (`inputs.<play>.<key>`) appears in that play's SKILL.md.

It counts; it does not judge. Usage: python3 lint_drive.py <path-to-drive/SKILL.md>
Exit: 0 clean, 1 gaps found, 2 could not read the file or find lint_play.py.
"""

import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (HERE, os.path.join(HERE, "..", "..", "play-creator", "scripts")):
    if os.path.isfile(os.path.join(_p, "lint_play.py")):
        sys.path.insert(0, _p)
        break
try:
    import lint_play as lp  # the play checks a drive also passes
except ImportError:
    lp = None

OPENER = "# --- Shared Drive Run (shared; see ../_shared/drive-run.md) ---"
CLOSER = "# --- end Shared Drive Run ---"
VALUES = ("drive", "plays", "questions", "runner_key", "checker_key", "end")
CHANGE_PLAYS = {"start-change", "commit-change", "propose-change", "review-change", "merge-change"}
MEMBER_PLAYS = {"search-knowledge", "build-knowledge", "review-knowledge"}  # plays the Shared Drive Run runs inside every drive (R5c, R5b)
DRIVE_OWNERS = {"drive", "drive (script)", "checker"}
STAMPED = ("drive_preflight.py", "write_drive_contract.py", "check_drive_contract.py",
           "check_play_done.py", "commit_run_files.py", "run_play_headless.py",
           "round_state.py", "drive_status.py", "prepare_check.py", "run_checker_codex.py", "record_check.py",
           "session_stamp.py", "check_stop_condition.py")
CONTRACT_MARK = "check_drive_contract"


def frontmatter_value(ctx, key):
    if not ctx["fm"]:
        return None
    m = re.search(rf"(?m)^{key}:\s*(\S+)\s*$", ctx["fm"].group(1))
    return m.group(1).strip("\"'") if m else None


def drive_values(text):
    """The drive's own values, from `key=value` lines between the run anchors."""
    if OPENER not in text or CLOSER not in text:
        return {}
    block = text[text.index(OPENER): text.index(CLOSER)]
    return {k: v.strip().strip("\"'") for k, v in re.findall(r"(?m)^(\w+)=(.*)$", block)}


def plays_of(values):
    return [p.strip() for p in values.get("plays", "").split(",") if p.strip()]


def find_play(drive_dir, play):
    """A play's SKILL.md: beside the drive once installed, or in plays/ in the source."""
    for base in (os.path.join(drive_dir, ".."), os.path.join(drive_dir, "..", "..", "plays")):
        md = os.path.normpath(os.path.join(base, play, "SKILL.md"))
        if os.path.isfile(md):
            return md
    return None


# --- the drive's own checks ---------------------------------------------------------
def check_kind(ctx):
    kind = frontmatter_value(ctx, "kind")
    pos = frontmatter_value(ctx, "position")
    return [(kind == "drive", "kind", "kind: drive" if kind == "drive"
             else f"frontmatter must say `kind: drive` (found {kind!r})"),
            (pos == "both", "drive position", "position: both" if pos == "both"
             else f"a drive opens and lands its change — `position: both` (found {pos!r})")]


def check_run_anchors(ctx):
    text = ctx["text"]
    n_open, n_close = text.count(OPENER), text.count(CLOSER)
    ok = n_open == 1 and n_close == 1 and text.index(OPENER) < text.index(CLOSER)
    shared = os.path.join(ctx["play_dir"], "..", "_shared", "drive-run.md")
    results = [(ok, "shared drive run",
                "anchors present, once each, in order" if ok else
                f"Shared Drive Run anchors must appear once each, opener first "
                f"(found opener {n_open}, closer {n_close})")]
    if n_open:
        results.append((os.path.isfile(shared), "shared drive run file",
                        "../_shared/drive-run.md exists" if os.path.isfile(shared)
                        else "the drive points to ../_shared/drive-run.md, which does not exist"))
    return results


def check_values(ctx):
    values = drive_values(ctx["text"])
    missing = [k for k in VALUES if not values.get(k)]
    results = [(not missing, "drive values",
                "drive, plays, questions, runner_key, checker_key, end set" if not missing
                else "missing between the run anchors: " + ", ".join(f"{k}=" for k in missing))]
    drive = values.get("drive")
    if drive:
        wrong = [f"{k}={values.get(k)}" for k, want in
                 (("runner_key", f"drives.{drive}.runner"), ("checker_key", f"drives.{drive}.checker"))
                 if values.get(k) and values[k] != want]
        results.append((not wrong, "config keys",
                        "runner and checker keys name the drive's own config" if not wrong
                        else "keys must be drives.<drive>.runner|checker: " + ", ".join(wrong)))
    return results


def check_plays(ctx):
    plays = plays_of(drive_values(ctx["text"]))
    if not plays:
        return [(False, "plays", "the drive names no plays")]
    problems = []
    dupes = sorted({p for p in plays if plays.count(p) > 1})
    if dupes:
        problems.append("named twice: " + ", ".join(dupes))
    for play in dict.fromkeys(plays):
        md = find_play(ctx["play_dir"], play)
        if md is None:
            problems.append(f"{play}: no such play")
            continue
        with open(md, encoding="utf-8") as fh:
            if CONTRACT_MARK not in fh.read():
                problems.append(f"{play}: cannot run inside a drive (checks no drive contract)")
    return [(not problems, "plays", f"{len(plays)} plays, in order, each runs inside a drive"
             if not problems else "; ".join(problems))]


def check_owners(ctx):
    allowed = DRIVE_OWNERS | CHANGE_PLAYS | MEMBER_PLAYS | set(plays_of(drive_values(ctx["text"])))
    owners = [o.strip().strip("`").strip() for o in
              re.findall(r"Owner:\s*([^·\n]+?)\s*(?:·|$)", ctx["workflow"], re.M)]
    if not owners:
        return [(False, "step owners", "no `Owner:` on any workflow step")]
    stray = sorted({o for o in owners if o not in allowed})
    return [(not stray, "step owners (ADR 029 §2)",
             "every step is run by the drive, its checker, or a play" if not stray
             else "steps owned by something that is not a play of the drive — a drive does no "
                  "work of its own: " + ", ".join(stray))]


def check_done_means(ctx):
    ice = os.path.join(ctx["play_dir"], "reference", "ice.md")
    text = ""
    if os.path.isfile(ice):
        with open(ice, encoding="utf-8") as fh:
            text = fh.read()
    ok = bool(re.search(r"(?im)^###\s+Done means\b", text))
    return [(ok, "done means", "the ICE has a Done means" if ok
             else "reference/ice.md must have a '### Done means' section — a drive proves done")]


def check_stamped(ctx):
    missing = [s for s in STAMPED
               if not os.path.isfile(os.path.join(ctx["play_dir"], "scripts", s))]
    return [(not missing, "stamped scripts", "the shared run's scripts are in scripts/"
             if not missing else "missing from scripts/: " + ", ".join(missing))]


def check_fingerprint_matches(ctx):
    """The fingerprint must be the sha256 of reference/ice.md as it is now, not just present."""
    ice = os.path.join(ctx["play_dir"], "reference", "ice.md")
    m = re.search(r"sha256:([0-9a-f]{64})", ctx["meta"])
    if not (m and os.path.isfile(ice)):
        return []  # absence is reported by the play check `fingerprint` and `done means`
    with open(ice, "rb") as fh:
        now = hashlib.sha256(fh.read()).hexdigest()
    ok = now == m.group(1)
    return [(ok, "fingerprint matches", "the fingerprint is reference/ice.md's sha256" if ok
             else "reference/ice.md changed since the drive was built — rebuild it "
                  "(/drive-editor) and recompute the fingerprint")]


def canonical_dirs(drive_dir):
    """Where the stamped scripts' sources live: the source tree, or the installed builders."""
    for plays in (os.path.join(drive_dir, "..", "..", "plays"), os.path.join(drive_dir, "..")):
        mine = os.path.join(plays, "drive-creator", "references")
        if os.path.isdir(mine):
            return [mine, os.path.join(plays, "play-creator", "references")]
    return []


def check_stamped_unchanged(ctx):
    dirs = canonical_dirs(ctx["play_dir"])
    if not dirs:
        return []  # a project without the builders installed: nothing to compare against
    changed = []
    for name in STAMPED:
        stamped = os.path.join(ctx["play_dir"], "scripts", name)
        source = next((os.path.join(d, name) for d in dirs if os.path.isfile(os.path.join(d, name))), None)
        if not (os.path.isfile(stamped) and source):
            continue
        with open(stamped, "rb") as a, open(source, "rb") as b:
            if a.read() != b.read():
                changed.append(name)
    return [(not changed, "stamped scripts unchanged", "each stamped script matches its source"
             if not changed else "differs from its source — copy it again, never edit a stamped "
                                 "copy: " + ", ".join(changed))]


def find_config(drive_dir):
    for rel in (("..", "..", "..", "config.yaml"), ("..", "..", "..", ".garura", "core", "config.yaml")):
        path = os.path.normpath(os.path.join(drive_dir, *rel))
        if os.path.isfile(path):
            return path
    return None


def check_config(ctx):
    """The drive's own settings exist in the config: runner, checker kind, and evidence on."""
    values = drive_values(ctx["text"])
    drive, cfg = values.get("drive"), find_config(ctx["play_dir"])
    if not (drive and cfg):
        return []
    with open(cfg, encoding="utf-8") as fh:
        text = fh.read()
    block = None  # walk lines, not a backtracking pattern: the drive's block under `drives:`
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.rstrip() == "drives:":
            for j in range(i + 1, len(lines)):
                if lines[j] and not lines[j].startswith(" "):
                    break
                if lines[j].rstrip() == f"  {drive}:":
                    body = []
                    for k in range(j + 1, len(lines)):
                        if lines[k].startswith("    ") or not lines[k].strip():
                            body.append(lines[k])
                        else:
                            break
                    block = "\n".join(body)
                    break
    plays_on = False
    for i, line in enumerate(lines):
        if line.rstrip() == "evidence:":
            for j in range(i + 1, len(lines)):
                if lines[j] and not lines[j].startswith(" "):
                    break
                if re.match(rf"^    {re.escape(drive)}:\s*true\b", lines[j]):
                    plays_on = True
    missing = []
    if not block or not re.search(r"(?m)^    runner:\s*\S", block):
        missing.append(f"drives.{drive}.runner")
    if not block or not re.search(r"(?m)^      kind:\s*\S", block):
        missing.append(f"drives.{drive}.checker.kind")
    if not plays_on:
        missing.append(f"evidence.plays.{drive}: true")
    return [(not missing, "config entries", f"{os.path.basename(cfg)} sets the drive's runner, "
             "checker and evidence" if not missing else "missing from the config: " + ", ".join(missing))]


def check_per_play(ctx):
    """Each play has its own step and its own done clause — `plays=` alone is a half-done edit."""
    plays = plays_of(drive_values(ctx["text"]))
    owners = {o.strip().strip("`").strip() for o in
              re.findall(r"Owner:\s*([^·\n]+?)\s*(?:·|$)", ctx["workflow"], re.M)}
    sc = os.path.join(ctx["play_dir"], "stop-condition.yaml")
    done = open(sc, encoding="utf-8").read() if os.path.isfile(sc) else ""
    no_step = [p for p in plays if p not in owners]
    no_done = [p for p in plays if f"{p}-done.json" not in done]
    problems = ([f"no step owned by: {', '.join(no_step)}"] if no_step else []) + \
               ([f"no done clause reads: {', '.join(p + '-done.json' for p in no_done)}"] if no_done else [])
    return [(not problems, "one step and one done clause per play",
             "every play has its step and its done clause" if not problems else "; ".join(problems))]


def check_inputs_read(ctx):
    """Every input handed to a play (`inputs.<play>.<key>`) is one the play reads."""
    plays = set(plays_of(drive_values(ctx["text"])))
    ice = os.path.join(ctx["play_dir"], "reference", "ice.md")
    text = ctx["text"] + (open(ice, encoding="utf-8").read() if os.path.isfile(ice) else "")
    unread = []
    for play, key in sorted(set(re.findall(r"inputs\.([a-z0-9-]+)\.([A-Za-z_][\w-]*)", text))):
        if key == "argument":
            continue  # handed on the play's command line, as a person types it (shared run R5)
        md = find_play(ctx["play_dir"], play) if play in plays else None
        if md is None:
            continue  # an unknown play is reported by the plays check
        with open(md, encoding="utf-8") as fh:
            if key not in fh.read():
                unread.append(f"inputs.{play}.{key}")
    return [(not unread, "handed inputs are read", "every input handed to a play is one it reads"
             if not unread else "the play never reads: " + ", ".join(unread))]


DRIVE_CHECKS = [check_kind, check_run_anchors, check_values, check_plays, check_owners,
                check_done_means, check_stamped, check_stamped_unchanged, check_fingerprint_matches,
                check_config, check_per_play, check_inputs_read]


def play_checks():
    """The play checks a drive passes too (its own position check is stricter, above)."""
    return [lp.check_sections, lp.check_coverage, lp.check_recovery, lp.check_orphans,
            lp.check_close_anchors, lp.check_stop_condition, lp.check_fingerprint,
            lp.check_next_command]


def defang(text):
    """Indent `#` lines inside code fences, so a shell comment (the run's anchors) is not read
    as a markdown header that cuts the Workflow section short. Anchors still match as text."""
    out, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        elif fence and line.startswith("#"):
            line = " " + line
        out.append(line)
    return "\n".join(out)


def main(argv):
    if len(argv) != 2:
        print("usage: python3 lint_drive.py <drive/SKILL.md>", file=sys.stderr)
        return 2
    if lp is None:
        print("lint_drive.py: cannot find lint_play.py (beside this script, or in "
              "play-creator/scripts)", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(f"cannot read {argv[1]}: {exc}", file=sys.stderr)
        return 2
    ctx = lp.load_context(argv[1], defang(text))
    results = []
    for check in play_checks() + DRIVE_CHECKS:
        results.extend(check(ctx))
    gaps = [r for r in results if not r[0]]
    print(f"DRIVE LINT: {argv[1]}")
    for ok, label, detail in results:
        print(f"  [{'PASS' if ok else 'GAP '}] {label}: {detail}")
    print(f"VERDICT: {'PASS' if not gaps else 'FAIL'} ({len(gaps)} gap(s))")
    return 0 if not gaps else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
