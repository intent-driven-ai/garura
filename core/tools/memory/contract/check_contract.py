#!/usr/bin/env python3
"""
check_contract.py — keep the memory tool's contract, its samples and its folder in step.

    python3 contract/check_contract.py [--contract contract/v1.json]

Three checks, all from this folder alone (standard library only):
  1. every sample in samples/ matches the contract: its request against the
     command's request shape, its response against the command's response shape;
  2. every sample in samples/broken/ fails at least one of those;
  3. the boundary: no file in the tool's folder names a path inside a project or
     the framework's own source tree, and no Python file imports from outside the
     standard library or the folder.

Prints a JSON report. Exit 0 when all three hold, 1 when any fails, 2 on a usage error.

The contract is written in a subset of JSON Schema (2020-12): type, const, enum,
properties, required, additionalProperties, items, minItems, minLength, minimum,
pattern, oneOf and local $ref. This file validates exactly that subset.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.dirname(HERE)

# Strings that would tie the folder to one project's layout or to the framework's source.
FORBIDDEN = (".garura/", "core/components", "~/.garura")

TYPES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def resolve(ref, root):
    if not ref.startswith("#/"):
        raise ValueError(f"only local $ref is supported: {ref}")
    node = root
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def validate(value, schema, root, where="$"):
    """Return a list of problems; empty means the value matches."""
    if "$ref" in schema:
        return validate(value, resolve(schema["$ref"], root), root, where)
    problems = []
    if "oneOf" in schema:
        passing = [s for s in schema["oneOf"] if not validate(value, s, root, where)]
        if len(passing) != 1:
            problems.append(f"{where}: matches {len(passing)} of the oneOf shapes, needs exactly 1")
        return problems
    if "const" in schema and value != schema["const"]:
        problems.append(f"{where}: must be {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        problems.append(f"{where}: {value!r} is not one of {schema['enum']}")
    if "type" in schema:
        kinds = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(TYPES[k](value) for k in kinds):
            problems.append(f"{where}: must be {' or '.join(kinds)}")
            return problems
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                problems.append(f"{where}: missing {key!r}")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    problems.append(f"{where}: unexpected {key!r}")
        for key, sub in props.items():
            if key in value:
                problems += validate(value[key], sub, root, f"{where}.{key}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            problems.append(f"{where}: needs at least {schema['minItems']} items")
        if "items" in schema:
            for i, item in enumerate(value):
                problems += validate(item, schema["items"], root, f"{where}[{i}]")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            problems.append(f"{where}: too short")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            problems.append(f"{where}: {value!r} does not match {schema['pattern']}")
    if TYPES["integer"](value) and "minimum" in schema and value < schema["minimum"]:
        problems.append(f"{where}: below {schema['minimum']}")
    return problems


def check_sample(sample, contract):
    """Problems with one sample file's content."""
    command = sample.get("command")
    spec = contract["commands"].get(command)
    if spec is None:
        return [f"unknown command {command!r}"]
    problems = []
    if "request" not in sample or "response" not in sample:
        return ["a sample needs both request and response"]
    problems += validate(sample["request"], spec["request"], contract, "request")
    problems += validate(sample["response"], spec["response"], contract, "response")
    response = sample["response"]
    if isinstance(response, dict) and response.get("command") != command:
        problems.append(f"response.command is {response.get('command')!r}, sample is for {command!r}")
    return problems


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def samples_in(folder):
    if not os.path.isdir(folder):
        return []
    return sorted(os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".json"))


def check_boundary():
    """Problems that tie the folder to a project or to code outside it."""
    problems = []
    stdlib = set(getattr(sys, "stdlib_module_names", ()))
    local = {os.path.splitext(f)[0] for _, _, files in os.walk(TOOL) for f in files if f.endswith(".py")}
    for dirpath, dirnames, files in os.walk(TOOL):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in files:
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, TOOL)
            try:
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            for needle in FORBIDDEN:
                # This file must spell the forbidden strings out to look for them.
                if needle in text and os.path.abspath(path) != os.path.abspath(__file__):
                    problems.append(f"{rel}: names {needle!r}")
            if name.endswith(".py") and stdlib:
                for m in re.finditer(r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", text, re.M):
                    top = (m.group(1) or m.group(2)).split(".")[0]
                    if top not in stdlib and top not in local:
                        problems.append(f"{rel}: imports {top!r}, not standard library or this folder")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--contract", default=os.path.join(HERE, "v1.json"))
    ns = ap.parse_args(argv)
    try:
        contract = load(ns.contract)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": f"cannot read the contract: {exc}"}))
        return 2

    good, broken = {}, {}
    for path in samples_in(os.path.join(HERE, "samples")):
        good[os.path.basename(path)] = check_sample(load(path), contract)
    for path in samples_in(os.path.join(HERE, "samples", "broken")):
        broken[os.path.basename(path)] = check_sample(load(path), contract)

    covered = {load(p).get("command") for p in samples_in(os.path.join(HERE, "samples"))}
    uncovered = sorted(set(contract["commands"]) - covered)
    good_failed = {k: v for k, v in good.items() if v}
    broken_passed = sorted(k for k, v in broken.items() if not v)
    boundary = check_boundary()

    ok = not good_failed and not broken_passed and not uncovered and bool(broken) and not boundary
    report = {
        "ok": ok,
        "contract": os.path.relpath(ns.contract, TOOL),
        "contract_version": contract.get("contract_version"),
        "samples_checked": len(good),
        "samples_failed": good_failed,
        "commands_without_a_sample": uncovered,
        "broken_checked": len(broken),
        "broken_that_passed": broken_passed,
        "broken_reasons": {k: v[:2] for k, v in broken.items() if v},
        "boundary_problems": boundary,
    }
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
