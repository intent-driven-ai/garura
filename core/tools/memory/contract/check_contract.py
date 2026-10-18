#!/usr/bin/env python3
"""
check_contract.py — keep the memory tool's contract, its samples and its folder in step.

    python3 contract/check_contract.py [--contract contract/v1.json]

Four checks, all from this folder alone (standard library only, Python 3.10 or newer):
  1. every sample in samples/ matches the contract: its request against the
     command's request shape, its response against the command's response shape;
  2. every sample also keeps the contract's answer rules (answer_rules): no tier
     is skipped silently, the first answer stops the lookup, results come from
     tiers looked in, and a fingerprint is the sha256 of the text it travels with;
  3. every sample in samples/broken/ fails at least one of those;
  4. the boundary: no file in the tool's folder names a path inside a project, the
     framework's source tree or a home folder, and no Python file imports from
     outside the standard library or the folder.

Prints a JSON report. Exit 0 when all hold, 1 when any fails, 2 on a usage error.

The contract is written in a subset of JSON Schema (2020-12): type, const, enum,
properties, required, additionalProperties, items, minItems, minLength, minimum,
pattern, oneOf and local $ref. This file validates exactly that subset. Its own
tests are in test_check_contract.py.
"""

import argparse
import ast
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.dirname(HERE)

# Strings that would tie the folder to one project's layout, the framework's source
# tree, or one machine. Built from parts so this file does not trip its own scan.
FORBIDDEN = tuple("".join(parts) for parts in (
    (".", "garura"), (".", "claude/"), ("core/", "components"), ("core/", "grounding"),
    ("docs/", "adr"), ("/", "Users/"), ("/", "home/"),
))

TYPES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def same(a, b):
    """JSON equality: true is not 1, and 1 is not true."""
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    return type(a) is type(b) and a == b if isinstance(a, (int, float, str)) else a == b


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
    if "const" in schema and not same(value, schema["const"]):
        problems.append(f"{where}: must be {schema['const']!r}")
    if "enum" in schema and not any(same(value, e) for e in schema["enum"]):
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


def fingerprint(text):
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def check_meaning(sample, contract):
    """The contract's answer_rules, which a shape alone cannot express."""
    request, response = sample.get("request", {}), sample.get("response", {})
    if not isinstance(response, dict) or response.get("ok") is not True:
        return []
    problems = []
    order = contract["lookup_order"]
    if response.get("command") in ("find", "search"):
        looked, answered = response.get("looked_in", []), response.get("answered_by")
        asked, every = request.get("tier"), request.get("every_tier") is True
        expected_all = [asked] if asked else order
        if [t for t in order if t in looked] != looked:
            problems.append("looked_in is not in lookup order")
        if answered is None and looked != expected_all:
            problems.append(f"nothing found after looking in {looked}, not {expected_all}: a tier was skipped")
        if answered is not None and not every and looked and looked[-1] != answered:
            problems.append(f"the lookup went on past {answered!r}, the first tier that answered")
        results = response.get("hits", response.get("matches", []))
        for r in results:
            if r.get("tier") not in looked:
                problems.append(f"a result comes from {r.get('tier')!r}, which is not in looked_in")
            elif not every and r.get("tier") != answered:
                problems.append(f"a result comes from {r.get('tier')!r}, not the tier that answered")
        for h in response.get("hits", []):
            if "text" in h and "fingerprint" in h and h["fingerprint"] != fingerprint(h["text"]):
                problems.append(f"hit {h.get('path')}:{h.get('line')} fingerprint is not the sha256 of its text")
    if response.get("command") == "read" and "text" in response and "fingerprint" in response:
        if response["fingerprint"] != fingerprint(response["text"]):
            problems.append("read fingerprint is not the sha256 of its text")
    if request.get("tier") and request.get("every_tier") and response.get("ok") is True:
        problems.append("tier with every_tier must be bad_request, not an answer")
    return problems


def check_sample(sample, contract):
    """Problems with one sample file's content."""
    command = sample.get("command")
    spec = contract["commands"].get(command)
    if spec is None:
        return [f"unknown command {command!r}"]
    if "request" not in sample or "response" not in sample:
        return ["a sample needs both request and response"]
    problems = []
    problems += validate(sample["request"], spec["request"], contract, "request")
    problems += validate(sample["response"], spec["response"], contract, "response")
    response = sample["response"]
    if isinstance(response, dict) and response.get("command") != command:
        problems.append(f"response.command is {response.get('command')!r}, sample is for {command!r}")
    if not problems:
        problems += check_meaning(sample, contract)
    return problems


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def samples_in(folder):
    if not os.path.isdir(folder):
        return []
    return sorted(os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".json"))


def check_imports(text, rel, stdlib, local):
    """Problems with one Python file's imports, read from its syntax tree."""
    problems = []
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [f"{rel}: cannot be parsed ({exc.msg})"]
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names = [node.module]
        for name in names:
            top = name.split(".")[0]
            if top not in stdlib and top not in local:
                problems.append(f"{rel}: imports {top!r}, not standard library or this folder")
        if isinstance(node, ast.Call):
            fn = node.func
            called = fn.id if isinstance(fn, ast.Name) else fn.attr if isinstance(fn, ast.Attribute) else ""
            if called in ("__import__", "import_module"):
                problems.append(f"{rel}: imports by name at run time ({called}), which this check cannot follow")
    return problems


def check_boundary(root=TOOL):
    """Problems that tie the folder to a project, a machine, or code outside it."""
    stdlib = getattr(sys, "stdlib_module_names", None)
    if stdlib is None:
        return ["the boundary check needs Python 3.10 or newer to know the standard library"]
    problems = []
    local = {os.path.splitext(f)[0] for _, _, files in os.walk(root) for f in files if f.endswith(".py")}
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in files:
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root)
            try:
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            for needle in FORBIDDEN:
                if needle in text:
                    problems.append(f"{rel}: names {needle!r}")
            if name.endswith(".py"):
                problems += check_imports(text, rel, set(stdlib), local)
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
