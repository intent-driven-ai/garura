#!/usr/bin/env python3
"""Tests for moving a product model made before #807 to the new names (#813, ADR 048).

Run: python3 test_migrate_model.py. The main fixture is Garura's own model as it stood before
#807 (commit f4137dc6), taken out of this repository with `git archive`, plus a small
hand-made part with what that model lacks: a slice record, an epic, an ICE entry and its page,
a nested feature page and a nested old folder. Everything runs in throwaway folders.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, HERE)
import migrate_model  # noqa: E402
import test_install  # noqa: E402  (its helpers only; its tests are not collected here)

SCRIPT = os.path.join(HERE, "migrate_model.py")
PRE_807 = "f4137dc6"
MODEL = os.path.join(".garura", "product", "product-os")
OLD = "function" + "alit"  # spelled in two parts so a search for old names in this file finds none

FEATURE_901 = """- id: fn-901
  slug: pay-by-card
  capability: cap-checkout
  status: proposed
  one_line: Pay by card — the first {old}y of checkout
  doc: shop/cap-checkout/fn-901/{old}y.md
""".format(old=OLD)

HAND_SPINE = """# hand-made part (#813 test): a slice, an epic and an ICE — this comment stays
slices:
- id: sl-901
  slug: checkout
  record: shop/slices/sl-901.yaml
  {old}y_refs: [fn-901]  # the slice's parts
epics:
- id: ep-901
  slice: sl-901
  "{old}y_refs":
  - fn-901
  - fn-902
ices:
- id: ice-901
  for: fn-901
  for_kind: '{old}y'
  doc: shop/cap-checkout/fn-901/ice.md
""".format(old=OLD)

HAND_FILES = {
    "shop/slices/sl-901.yaml": """# Checkout slice — kept comment
slice:
  id: sl-901
  name: Checkout
  {old}ies:
  - {old}y_ref: fn-901   # first
    ice_ref: ice-901
  - {old}y_ref: fn-902
  note: every {old}y here is paid by card
""",
    "shop/cap-checkout/capability.md": """# Capability: Checkout

Checkout holds two {old}ies.

## {Old}ies
- Pay by card (fn-901): this {old}y takes a card.
""",
    "shop/cap-checkout/fn-901/{old}y.md": """# {Old}y: Pay by card

This {old}y takes a card payment.
""",
    "shop/cap-checkout/fn-901/ice.md": """---
for: fn-901
for_kind: {old}y
---
# ICE: Pay by card
""",
    "shop/{old}ies/fn-902/{old}y.md": """# {Old}y: Pay by bank

The {old}y a bank transfer needs.
""",
}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True).stdout


def fill(text):
    return text.format(old=OLD, Old=OLD.capitalize())


def build_pre_807(target):
    """Garura's own pre-#807 model plus the hand-made part, under <target>/.garura/product/."""
    os.makedirs(target, exist_ok=True)
    arch = subprocess.run(["git", "-C", ROOT, "archive", PRE_807, ".garura/product/product-os"],
                          capture_output=True)
    if arch.returncode != 0:
        raise unittest.SkipTest(f"commit {PRE_807} is not in this checkout")
    subprocess.run(["tar", "-x", "-C", target], input=arch.stdout, check=True)
    model = os.path.join(target, MODEL)
    spine = os.path.join(model, "_spine.yaml")
    text = open(spine, encoding="utf-8").read()
    assert f"\n{OLD}ies:\n" in text
    text = text.replace(f"\n{OLD}ies:\n", f"\n{OLD}ies:\n" + FEATURE_901, 1) + HAND_SPINE
    with open(spine, "w", encoding="utf-8") as fh:
        fh.write(text)
    for rel, body in HAND_FILES.items():
        full = os.path.join(model, fill(rel))
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(fill(body))
    os.makedirs(os.path.join(model, "shop", OLD + "ies", "empty-one"))  # a folder git cannot see
    return model


def make_repo(target):
    git(target, "init", "-q", "-b", "main")
    # Demo address: sample data for this throwaway repository, not personal data.
    git(target, "config", "user.email", "t@example.com")
    git(target, "config", "user.name", "test")
    git(target, "add", "-A")
    git(target, "commit", "-q", "-m", "seed")


def run_cli(target):
    run = subprocess.run([sys.executable, SCRIPT, "--target", target], capture_output=True, text=True)
    return run.returncode, (json.loads(run.stdout) if run.stdout.strip().startswith("{") else None), run


def old_names_left(model):
    """Every old name still used as a key, a path part or a heading — prose is not counted."""
    left = []
    for d, dirs, names in os.walk(model):
        for n in dirs + names:
            if n in (OLD + "ies", OLD + "y.md"):
                left.append(os.path.join(d, n))
        for n in names:
            full = os.path.join(d, n)
            with open(full, encoding="utf-8") as fh:
                lines = fh.readlines()
            for i, line in enumerate(lines, 1):
                if (re.match(rf"^\s*(?:-\s+)*['\"]?{OLD}(?:ies|y_refs?)['\"]?\s*:", line)
                        or re.match(rf"^\s*for_kind\s*:\s*['\"]?{OLD}y", line)
                        or re.search(rf"(?:^|/){OLD}(?:ies/|y\.md)", line.split(":", 1)[-1].strip())
                        or re.match(rf"^#+ {OLD.capitalize()}(?:y:|ies\s*$)", line)):
                    left.append(f"{full}:{i}: {line.strip()}")
    return left


class Work(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.work, ignore_errors=True)
        self.target = os.path.join(self.work, "shop")

    def read(self, *parts):
        with open(os.path.join(self.target, MODEL, *parts), encoding="utf-8") as fh:
            return fh.read()


class MovesAPre807Model(Work):
    def test_the_whole_model_moves_in_one_commit_and_a_second_run_does_nothing(self):
        model = build_pre_807(self.target)
        make_repo(self.target)
        # unrelated work of the project's own: one staged file, one changed file — kept out
        with open(os.path.join(self.target, "notes.txt"), "w") as fh:
            fh.write("staged, not the model's\n")
        git(self.target, "add", "notes.txt")
        with open(os.path.join(self.target, "README.md"), "w") as fh:
            fh.write("changed, not the model's\n")
        before = int(git(self.target, "rev-list", "--count", "HEAD"))

        code, report, run = run_cli(self.target)
        self.assertEqual(code, 0, run.stderr)
        self.assertEqual(old_names_left(model), [])

        # exactly one commit, holding only model paths
        self.assertTrue(report["committed"], report["reason"])
        self.assertEqual(int(git(self.target, "rev-list", "--count", "HEAD")), before + 1)
        self.assertEqual(git(self.target, "rev-parse", "HEAD").strip(), report["commit"])
        self.assertEqual(git(self.target, "log", "-1", "--format=%s").strip(), migrate_model.COMMIT_MESSAGE)
        in_commit = git(self.target, "show", "--name-only", "--format=", "HEAD").split()
        self.assertTrue(in_commit)
        self.assertTrue(all(p.startswith(".garura/product/product-os/") for p in in_commit), in_commit)
        status = git(self.target, "status", "--porcelain")
        self.assertIn("A  notes.txt", status)
        self.assertNotIn(".garura/product", status)

        # the spine reads with the new names, and every page it points at exists
        spine = yaml.safe_load(self.read("_spine.yaml"))
        self.assertNotIn(OLD + "ies", spine)
        self.assertEqual(len(spine["features"]), 22)
        for f in spine["features"]:
            self.assertTrue(f["doc"].endswith("/feature.md"), f["doc"])
            self.assertTrue(os.path.isfile(os.path.join(model, f["doc"])), f["doc"])
        self.assertEqual(spine["slices"][0]["feature_refs"], ["fn-901"])
        self.assertEqual(spine["epics"][0]["feature_refs"], ["fn-901", "fn-902"])
        self.assertEqual(spine["ices"][0]["for_kind"], "feature")
        record = yaml.safe_load(self.read("shop", "slices", "sl-901.yaml"))["slice"]
        self.assertEqual([f["feature_ref"] for f in record["features"]], ["fn-901", "fn-902"])
        self.assertIn("for_kind: feature", self.read("shop", "cap-checkout", "fn-901", "ice.md"))

        # prose, comments and IDs stay as they were
        text = self.read("_spine.yaml")
        self.assertIn(f"one_line: A capability or {OLD}y is ready without a domain", text)
        self.assertIn("# hand-made part (#813 test): a slice, an epic and an ICE — this comment stays", text)
        self.assertIn("# the slice's parts", text)
        slice_text = self.read("shop", "slices", "sl-901.yaml")
        self.assertIn("# Checkout slice — kept comment", slice_text)
        self.assertIn(f"note: every {OLD}y here is paid by card", slice_text)
        self.assertIn("feature_ref: fn-901   # first", slice_text)
        page = self.read("shop", "cap-checkout", "fn-901", "feature.md")
        self.assertTrue(page.startswith("# Feature: Pay by card\n"))
        self.assertIn(f"This {OLD}y takes a card payment.", page)
        cap = self.read("shop", "cap-checkout", "capability.md")
        self.assertIn("\n## Features\n", cap)
        self.assertIn(f"Checkout holds two {OLD}ies.", cap)
        self.assertTrue(os.path.isfile(os.path.join(model, "features", "fn-724", "feature.md")))
        self.assertTrue(os.path.isfile(os.path.join(model, "shop", "features", "fn-902", "feature.md")))
        self.assertTrue(os.path.isdir(os.path.join(model, "shop", "features", "empty-one")))

        # the report names what moved
        moved = report["moved"]
        self.assertIn({"from": f"{MODEL}/{OLD}ies", "to": f"{MODEL}/features"}, moved["folders"])
        self.assertIn({"from": f"{MODEL}/shop/{OLD}ies", "to": f"{MODEL}/shop/features"}, moved["folders"])
        self.assertIn({"from": f"{MODEL}/shop/cap-checkout/fn-901/{OLD}y.md",
                       "to": f"{MODEL}/shop/cap-checkout/fn-901/feature.md"}, moved["files"])
        self.assertEqual(len(moved["files"]), 23)
        keys = {(k["file"].split("/")[-1], k["from"], k["to"]) for k in moved["keys"]}
        for want in [("_spine.yaml", OLD + "ies", "features"), ("_spine.yaml", OLD + "y_refs", "feature_refs"),
                     ("_spine.yaml", f"for_kind: {OLD}y", "for_kind: feature"),
                     ("sl-901.yaml", OLD + "ies", "features"), ("sl-901.yaml", OLD + "y_ref", "feature_ref"),
                     ("ice.md", f"for_kind: {OLD}y", "for_kind: feature")]:
            self.assertIn(want, keys)
        self.assertIn({"file": f"{MODEL}/shop/cap-checkout/capability.md",
                       "from": f"## {OLD.capitalize()}ies", "to": "## Features"}, moved["headings"])
        self.assertEqual(len([h for h in moved["headings"] if h["to"].startswith("# Feature:")]), 23)

        # a second run: nothing to move, no commit
        head = report["commit"]
        code, again, run = run_cli(self.target)
        self.assertEqual(code, 0, run.stderr)
        self.assertEqual(again["moved"], {"keys": [], "files": [], "folders": [], "headings": []})
        self.assertFalse(again["committed"])
        self.assertIsNone(again["commit"])
        self.assertEqual(git(self.target, "rev-parse", "HEAD").strip(), head)

    def test_a_spine_with_both_old_and_new_keys_is_refused_and_nothing_moves(self):
        model = build_pre_807(self.target)
        with open(os.path.join(model, "_spine.yaml"), "a", encoding="utf-8") as fh:
            fh.write("features: []\n")
        make_repo(self.target)
        code, report, run = run_cli(self.target)
        self.assertEqual(code, 2)
        self.assertTrue(report["refused"])
        self.assertEqual(report["moved"], {"keys": [], "files": [], "folders": [], "headings": []})
        self.assertIn("both", run.stderr)
        self.assertEqual(git(self.target, "status", "--porcelain"), "")
        self.assertEqual(int(git(self.target, "rev-list", "--count", "HEAD")), 1)

    def test_outside_git_it_moves_but_does_not_commit(self):
        model = build_pre_807(self.target)
        code, report, run = run_cli(self.target)
        self.assertEqual(code, 0, run.stderr)
        self.assertEqual(old_names_left(model), [])
        self.assertFalse(report["committed"])
        self.assertIn("not a git repository", report["reason"])

    def test_paths_with_their_own_changes_are_moved_but_not_committed(self):
        model = build_pre_807(self.target)
        make_repo(self.target)
        with open(os.path.join(model, "shop", "slices", "sl-901.yaml"), "a", encoding="utf-8") as fh:
            fh.write("  owner: someone's edit in progress\n")
        code, report, run = run_cli(self.target)
        self.assertEqual(code, 0, run.stderr)
        self.assertEqual(old_names_left(model), [])
        self.assertFalse(report["committed"])
        self.assertIn("sl-901.yaml", report["reason"])
        self.assertEqual(int(git(self.target, "rev-list", "--count", "HEAD")), 1)

    def test_no_model_is_a_quiet_no_op(self):
        os.makedirs(self.target)
        code, report, run = run_cli(self.target)
        self.assertEqual(code, 0, run.stderr)
        self.assertEqual(report["moved"], {"keys": [], "files": [], "folders": [], "headings": []})
        self.assertFalse(report["committed"])

    def test_the_model_is_found_through_the_projects_config(self):
        os.makedirs(os.path.join(self.target, ".garura", "core"))
        with open(os.path.join(self.target, ".garura", "core", "config.yaml"), "w") as fh:
            fh.write("product:\n  base-path: docs/product/\n")
        page = os.path.join(self.target, "docs", "product", "product-os", OLD + "ies", "fn-1", OLD + "y.md")
        os.makedirs(os.path.dirname(page))
        with open(page, "w") as fh:
            fh.write(f"# {OLD.capitalize()}y: One\n")
        code, report, _ = run_cli(self.target)
        self.assertEqual(code, 0)
        self.assertTrue(os.path.isfile(os.path.join(self.target, "docs", "product", "product-os",
                                                    "features", "fn-1", "feature.md")))


class TheInstallersMoveTheModel(test_install.Installed):
    """install.py (the install-garura play) moves the model and records it in the manifest record."""

    def test_install_py_moves_a_pre_807_model_and_records_it(self):
        build_pre_807(self.target)
        make_repo(self.target)
        record = self.install()
        self.assertTrue(record["model_migration"]["committed"], record["model_migration"]["reason"])
        self.assertEqual(old_names_left(os.path.join(self.target, MODEL)), [])
        self.assertEqual(int(git(self.target, "rev-list", "--count", "HEAD")), 2)
        again = self.install()["model_migration"]
        self.assertFalse(any(again["moved"].values()))


class ThePublicInstallerMovesTheModel(unittest.TestCase):
    """installer/install.sh, run whole (helpers borrowed from test_install.PublicInstaller)."""

    setUp = test_install.PublicInstaller.setUp
    archive = test_install.PublicInstaller.archive
    run_installer = test_install.PublicInstaller.run_installer

    def test_the_shell_installer_moves_a_pre_807_model(self):
        build_pre_807(self.target)
        make_repo(self.target)
        run = self.run_installer(self.archive())
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("model: moved to the #807 names", run.stdout)
        self.assertEqual(old_names_left(os.path.join(self.target, MODEL)), [])
        self.assertEqual(git(self.target, "log", "-1", "--format=%s").strip(), migrate_model.COMMIT_MESSAGE)

    def test_the_shell_installer_works_with_no_model(self):
        run = self.run_installer(self.archive())
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("model: no product model", run.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=1)
