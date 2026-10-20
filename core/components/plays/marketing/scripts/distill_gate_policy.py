#!/usr/bin/env python3
"""
distill_gate_policy.py — the deterministic learner over the gate ledger (#467).

Reads the live-eval ledger (gate-evals.jsonl) and writes the per-project gate policy
(gate-policy.yaml). Each issue keeps its own ledger under its folder
(`<stm_base><issue>/review/gate-evals.jsonl` — the issue ID governs, ADR 039); given one of
those, the learner reads every issue's ledger beside it, in time order, because the policy is
learned from all of them. A ledger anywhere else is read alone, as before. Pure rule, no inference, replay-deterministic (every output value
derives from ledger content — no wall clock):

  - a shape earns AUTO when its last `streak` consecutive entries are approved_clean
    (auto_pass lines EXTEND an earned streak but never start one) and no unrefuted
    correction stands against it;
  - any rejected / approved_edited / correction line RESETS that shape to gated;
  - a deferred_to_drive_review line (a crossing inside a drive, #614) is SKIPPED: it is
    not an approval and does not break a run of them, until the drive's review appends
    the person's real answer as its own line;
  - shapes in `never_auto` (human-pinned, preserved verbatim from the existing policy)
    are never emitted as auto regardless of the ledger.

  python3 distill_gate_policy.py --ledger <gate-evals.jsonl> \
      --policy <gate-policy.yaml> [--streak 3] [--project garura]

Writes the policy file and prints a JSON summary. Exit 0 on success, 2 on bad input.
"""

import argparse
import glob
import json
import os
import re
import sys


def fail(msg):
    sys.stderr.write(f"distill_gate_policy.py: {msg}\n")
    sys.exit(2)


def read_ledger(path):
    if not os.path.isfile(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for i, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                rec = json.loads(raw)
                rec["_line"] = i
                out.append(rec)
            except ValueError:
                continue
    return out


PER_ISSUE = re.compile(r"^(?P<base>.*)/(?P<issue>[^/]+)/review/gate-evals\.jsonl$")


def _ts_key(rec):
    """Order across ledgers by the run's own timestamp; both spellings in use
    (2026-10-20T04:42:16Z and 20261020T045014Z) reduce to the same digits."""
    return re.sub(r"\D", "", str(rec.get("ts", "")))


def read_ledgers(path):
    """One issue's ledger path -> every issue's records, in time order; any other path -> its
    own records. Each record carries `_src` (its issue, or None) so a correction's `refutes`
    (a line number in its own ledger) stays inside that ledger."""
    m = PER_ISSUE.match(path.replace(os.sep, "/"))
    if not m:
        return [dict(r, _src=None) for r in read_ledger(path)]
    out = []
    pattern = os.path.join(m.group("base"), "*", "review", "gate-evals.jsonl")
    for ledger in sorted(glob.glob(pattern)):
        issue = os.path.basename(os.path.dirname(os.path.dirname(ledger)))
        out += [dict(r, _src=issue) for r in read_ledger(ledger)]
    return sorted(out, key=lambda r: (_ts_key(r), str(r["_src"]), r["_line"]))


def _where(rec):
    """How a policy names the line that earned it: its line number, or issue#line."""
    return rec["_line"] if rec.get("_src") is None else f"{rec['_src']}#{rec['_line']}"


def _parse_inline_never(value):
    """never_auto given inline as `[a, b]` -> the list of shape keys."""
    inner = value.strip("[]")
    return [s.strip().strip("'\"") for s in inner.split(",") if s.strip()]


def _parse_never_item(line):
    """A `- shape` item line under never_auto:, or None."""
    m = re.match(r"^\s*-\s*(\S+)", line)
    return m.group(1).strip("'\"") if m else None


def read_existing_policy(path):
    """Minimal reader: version + never_auto list. No third-party YAML dep."""
    version, never = 0, []
    if not os.path.isfile(path):
        return version, never
    in_never = False
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^version:\s*(\d+)", line)
            if m:
                version = int(m.group(1))
            if re.match(r"^never_auto:", line):
                value = line.split(":", 1)[1].strip()
                if value and value != "[]":
                    never = _parse_inline_never(value)
                in_never = not value  # block form follows only on a bare key
                continue
            if in_never:
                item = _parse_never_item(line)
                if item:
                    never.append(item)
                elif line.strip() and not line.startswith(" "):
                    in_never = False
    return version, never


def _trailing_streak(recs, refuted):
    """The shape's live trailing streak of clean lines (auto_pass may extend it)."""
    run = []
    for rec in recs:
        human = rec.get("human")
        if human == "deferred_to_drive_review":
            continue  # no answer yet — skipped, even when a later line answers it
        if (rec.get("_src"), rec["_line"]) in refuted:
            run = []  # a refuted line breaks the streak it sat in
        elif human == "approved_clean":
            run.append(rec)
        elif human == "auto_pass" and run:
            run.append(rec)  # extends an earned streak, never starts one
        else:
            # rejected / approved_edited / a correction line / anything unknown
            run = []
    return run


def _group_by_shape(records):
    by_shape = {}
    for rec in records:
        if rec.get("shape"):
            by_shape.setdefault(rec["shape"], []).append(rec)
    return by_shape


def distill(records, streak, never_auto):
    """Return {shape: {earned_by: [...], since: ts}} for shapes that earn auto."""
    refuted = {(r.get("_src"), r["refutes"]) for r in records if r.get("refutes")}
    auto = {}
    for shape, recs in sorted(_group_by_shape(records).items()):
        if shape in never_auto:
            continue
        run = _trailing_streak(recs, refuted)
        clean = [r for r in run if r.get("human") == "approved_clean"]
        if len(clean) >= streak:
            earners = clean[-streak:]
            auto[shape] = {
                "earned_by": [_where(r) for r in earners],
                "since": earners[-1].get("ts", ""),
            }
    return auto


def write_policy(path, project, version, auto, never_auto, streak):
    lines = [
        "# gate-policy.yaml — learned per-project gate policy (#467).",
        "# Written by distill_gate_policy.py from gate-evals.jsonl — do not hand-edit",
        "# the auto: block (it is re-derived). never_auto: IS yours to edit — a shape",
        "# listed there stays gated forever regardless of the ledger.",
        f"version: {version}",
        f"project: {project}",
        f"streak: {streak}",
        "auto:",
    ]
    if auto:
        for shape in sorted(auto):
            e = auto[shape]
            lines.append(
                f"  {shape}: {{earned_by: {e['earned_by']}, since: {e['since']}}}"
            )
    else:
        lines[-1] = "auto: {}"
    if never_auto:
        lines.append("never_auto:")
        lines.extend(f"  - {s}" for s in never_auto)
    else:
        lines.append("never_auto: []")
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--streak", type=int, default=3)
    ap.add_argument("--project", default="project")
    args = ap.parse_args(argv)

    if args.streak < 1:
        fail("--streak must be >= 1")
    records = read_ledgers(args.ledger)
    version, never_auto = read_existing_policy(args.policy)
    auto = distill(records, args.streak, never_auto)
    write_policy(args.policy, args.project, version + 1, auto, never_auto, args.streak)
    print(
        json.dumps(
            {
                "policy": args.policy,
                "version": version + 1,
                "auto_shapes": sorted(auto),
                "never_auto": never_auto,
                "ledger_lines": len(records),
            }
        )
    )


if __name__ == "__main__":
    main()
