#!/usr/bin/env python3
"""
grill_budget.py — the grilling tier: how many questions /shape-slice may ask, and which ones.

The tier is a project setting (`shape-slice.grill-tier` in the config). Each tier gives a
budget of questions: xs 5, s 12, m 25, l 45, xl 70. A question only the person can answer is
BLOCKING: it is always asked, and it counts first. The other questions are asked in their given
order until the budget is used. Each question not asked becomes an assumption.

Layer rule: reads files on disk only; no git/gh/network.

    python3 grill_budget.py tier  --config <path to config.yaml>
    python3 grill_budget.py split --questions <questions.json> --budget <n>

`tier` prints {tier, budget} JSON. A missing `shape-slice` section or `grill-tier` key gives
the default tier m (25). An unknown tier is a usage error that names the allowed values.

`split` reads a JSON list of question objects, each with "id" and "blocking" (true|false);
any other fields are kept. It prints {asked[], assumptions[], over_budget} JSON. Both lists
keep the questions' original order. over_budget is true only when the blocking questions
alone are more than the budget (they are still all asked).

Exit 0 done, 2 usage error.
"""

import argparse
import json
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("grill_budget.py: PyYAML is required (pip install pyyaml).\n")
    sys.exit(2)

BUDGETS = {"xs": 5, "s": 12, "m": 25, "l": 45, "xl": 70}
DEFAULT_TIER = "m"
SECTION = "shape-slice"
KEY = "grill-tier"


def usage_error(msg):
    sys.stderr.write(f"grill_budget.py: {msg}\n")
    return 2


def resolve_tier(config):
    """Return (tier, budget) from a loaded config, or raise ValueError for an unknown tier."""
    section = config.get(SECTION) if isinstance(config, dict) else None
    value = section.get(KEY) if isinstance(section, dict) else None
    if value is None:
        return DEFAULT_TIER, BUDGETS[DEFAULT_TIER]
    if not isinstance(value, str) or value not in BUDGETS:
        raise ValueError(f"unknown {SECTION}.{KEY} {value!r}; allowed values: {', '.join(BUDGETS)}")
    return value, BUDGETS[value]


def split(questions, budget):
    """Split questions into asked and assumptions under the budget. Order is kept."""
    blocking = sum(1 for q in questions if q["blocking"])
    room = budget - blocking
    asked, assumptions = [], []
    for q in questions:
        if q["blocking"]:
            asked.append(q)
        elif room > 0:
            asked.append(q)
            room -= 1
        else:
            assumptions.append(q)
    return {"asked": asked, "assumptions": assumptions, "over_budget": blocking > budget}


def cmd_tier(args):
    try:
        with open(args.config, encoding="utf-8") as fh:
            config = yaml.safe_load(fh) or {}
    except (OSError, yaml.YAMLError) as exc:
        return usage_error(f"cannot read config {args.config}: {exc}")
    try:
        tier, budget = resolve_tier(config)
    except ValueError as exc:
        return usage_error(str(exc))
    print(json.dumps({"tier": tier, "budget": budget}, indent=2))
    return 0


def cmd_split(args):
    if args.budget < 0:
        return usage_error("--budget must be 0 or more")
    try:
        with open(args.questions, encoding="utf-8") as fh:
            questions = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return usage_error(f"cannot read questions {args.questions}: {exc}")
    if not isinstance(questions, list):
        return usage_error("the questions file must hold a JSON list")
    for i, q in enumerate(questions):
        if not isinstance(q, dict) or "id" not in q or not isinstance(q.get("blocking"), bool):
            return usage_error(f"question {i} needs an \"id\" and a true/false \"blocking\"")
    print(json.dumps(split(questions, args.budget), indent=2))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="The /shape-slice grilling tier and question split.")
    sub = ap.add_subparsers(dest="command", required=True)
    t = sub.add_parser("tier", help="print the tier and its budget")
    t.add_argument("--config", required=True)
    s = sub.add_parser("split", help="split questions into asked and assumptions")
    s.add_argument("--questions", required=True)
    s.add_argument("--budget", required=True, type=int)
    args = ap.parse_args(argv)
    return cmd_tier(args) if args.command == "tier" else cmd_split(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
