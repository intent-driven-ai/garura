#!/usr/bin/env python3
"""
model_names.py — stop on a product model written before the feature rename (#807).

Issue #807 renamed the model's "functionality" to "feature". A script that reads an old
model with the new names finds no features and goes on as if the model were empty. This
guard makes that loud: on any old key it prints a plain message naming the key, the file
and the upgrade step, and exits with code 2.

Old names it stops on:
  functionalities:          (spine list, or a slice record's slice.functionalities)
  functionality_refs        (an epic's list of feature references)
  functionality_ref         (a slice record's feature reference)
  for_kind: functionality   (an ICE entry)

Use, right after the YAML is parsed:
    check_spine(spine, path)     # a _spine.yaml
    check_slice(record, path)    # a slice record
    check_model(data, path)      # any other model YAML

SHARED script: the main copy is plays/create-play/references/model_names.py, and every copy
must match it byte for byte (the component linter checks this). Standard library only.
"""

import sys

OLD_KEYS = {
    "functionalities": "features",
    "functionality_refs": "feature_refs",
    "functionality_ref": "feature_ref",
}

UPGRADE_STEP = (
    "Upgrade the model: re-install Garura (install-garura migrates the model), or run\n"
    "  python3 <install-garura>/scripts/migrate_model.py --target <project>"
)


def _stop(path, where, old, new):
    sys.stderr.write(
        f"{path}: this product model uses the old name '{old}' (at {where}); "
        f"since #807 it is '{new}'.\n"
        f"Reading it with the new names would see no features, so this script stops here.\n"
        f"{UPGRADE_STEP}\n"
    )
    sys.exit(2)


def _find_old(data, where):
    """Return (where, old, new) for the first old name in data, or None."""
    if isinstance(data, dict):
        for key, value in data.items():
            here = f"{where}.{key}" if where else str(key)
            if key in OLD_KEYS:
                return here, key, OLD_KEYS[key]
            if key == "for_kind" and value == "functionality":
                return here, "for_kind: functionality", "for_kind: feature"
            found = _find_old(value, here)
            if found:
                return found
    elif isinstance(data, list):
        for i, item in enumerate(data):
            found = _find_old(item, f"{where}[{i}]")
            if found:
                return found
    return None


def check_model(data, path):
    """Stop (exit 2) if any old name appears anywhere in this parsed YAML."""
    found = _find_old(data, "")
    if found:
        _stop(path, *found)
    return data


def check_spine(spine, path):
    """Stop (exit 2) if a parsed _spine.yaml still uses an old name."""
    return check_model(spine, path)


def check_slice(record, path):
    """Stop (exit 2) if a parsed slice record still uses an old name."""
    return check_model(record, path)
