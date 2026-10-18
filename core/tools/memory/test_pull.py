#!/usr/bin/env python3
"""Tests for pull.py. Run from the tool's folder: python3 test_pull.py"""

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "contract"))
import check_contract as cc  # noqa: E402
import pull  # noqa: E402

CONTRACT = cc.load(os.path.join(HERE, "contract", "v1.json"))


def git(repo, *args):
    subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True)


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def answers_of(command, request, answers):
    """Each answer must match the contract's response shape for its command."""
    spec = CONTRACT["commands"][command]["response"]
    return [cc.validate(a, spec, CONTRACT) for a in answers]


class Tiers(unittest.TestCase):
    def setUp(self):
        self.phoenix = tempfile.mkdtemp()
        self.garura = tempfile.mkdtemp()
        git(self.phoenix, "init", "-q", "-b", "main")
        git(self.phoenix, "config", "user.email", "t@example.com")
        git(self.phoenix, "config", "user.name", "test")
        write(self.phoenix, "standards/rules/commits.md", "# Commits\nSubject under 72.\n")
        write(self.phoenix, "standards/templates/adr.md", "# ADR template\n")
        write(self.phoenix, "knowledge/domains/payments.md", "# Payments\n")
        self.commit("seed")

    def commit(self, message):
        git(self.phoenix, "add", "-A")
        git(self.phoenix, "commit", "-q", "-m", message)
        return pull.version(self.phoenix)


class Pull(Tiers):
    def test_one_piece(self):
        answers = pull.pull(self.phoenix, self.garura, ["standards/rules/commits.md"])
        self.assertEqual(answers_of("pull", {}, answers), [[]])
        a = answers[0]
        self.assertEqual((a["tier"], a["path"], a["version"]), ("garura", "standards/rules/commits.md",
                                                                 pull.version(self.phoenix)))
        with open(os.path.join(self.garura, "standards/rules/commits.md"), encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "# Commits\nSubject under 72.\n")
        self.assertEqual(a["fingerprint"], cc.fingerprint("# Commits\nSubject under 72.\n"))

    def test_nothing_leaves_phoenix(self):
        pull.pull(self.phoenix, self.garura, ["standards/**"])
        self.assertTrue(os.path.isfile(os.path.join(self.phoenix, "standards/rules/commits.md")))

    def test_glob_pulls_only_what_it_names(self):
        answers = pull.pull(self.phoenix, self.garura, ["standards/**"])
        self.assertEqual(sorted(a["path"] for a in answers),
                         ["standards/rules/commits.md", "standards/templates/adr.md"])
        self.assertFalse(os.path.exists(os.path.join(self.garura, "knowledge")))

    def test_the_list_records_each_piece_once(self):
        pull.pull(self.phoenix, self.garura, ["standards/**"])
        write(self.phoenix, "standards/rules/commits.md", "# Commits\nSubject under 60.\n")
        later = self.commit("change")
        pull.pull(self.phoenix, self.garura, ["standards/rules/commits.md"])
        entries = pull.read_list(self.garura)
        self.assertEqual(sorted(entries), ["standards/rules/commits.md", "standards/templates/adr.md"])
        self.assertEqual(entries["standards/rules/commits.md"]["version"], later)

    def test_refusals(self):
        for pattern, code in (("../outside.md", "bad_request"), ("/abs.md", "bad_request"),
                              ("standards/missing.md", "not_found"), ("nothing/**", "not_found")):
            a = pull.pull(self.phoenix, self.garura, [pattern])[0]
            self.assertEqual(a["error"]["code"], code, pattern)
            self.assertEqual(answers_of("pull", {}, [a]), [[]])

    def test_never_pulls_git_internals(self):
        answers = pull.pull(self.phoenix, self.garura, ["**"])
        self.assertTrue(all(".git/" not in a["path"] and not a["path"].startswith(".git") for a in answers))
        self.assertEqual(len(answers), 3)


class Pulled(Tiers):
    def test_nothing_behind_after_a_pull(self):
        pull.pull(self.phoenix, self.garura, ["standards/**"])
        answer = pull.pulled(self.phoenix, self.garura)
        self.assertEqual(answers_of("pulled", {}, [answer]), [[]])
        self.assertEqual([p["behind"] for p in answer["pieces"]], [False, False])

    def test_a_change_in_phoenix_is_behind(self):
        pull.pull(self.phoenix, self.garura, ["standards/**"])
        write(self.phoenix, "standards/templates/adr.md", "# ADR template, version 2\n")
        later = self.commit("change")
        answer = pull.pulled(self.phoenix, self.garura, behind_only=True)
        self.assertEqual([(p["path"], p["behind"], p["current_version"]) for p in answer["pieces"]],
                         [("standards/templates/adr.md", True, later)])

    def test_a_piece_removed_from_phoenix_is_behind(self):
        pull.pull(self.phoenix, self.garura, ["knowledge/domains/payments.md"])
        git(self.phoenix, "rm", "-q", "knowledge/domains/payments.md")
        self.commit("remove")
        self.assertTrue(pull.pulled(self.phoenix, self.garura)["pieces"][0]["behind"])


class Settings(unittest.TestCase):
    def run_main(self, argv, env):
        old = dict(os.environ)
        os.environ.pop("MEMORY_PHOENIX_ROOT", None)
        os.environ.pop("MEMORY_GARURA_ROOT", None)
        os.environ.update(env)
        try:
            with contextlib.redirect_stdout(io.StringIO()) as out:
                code = pull.main(argv)
        finally:
            os.environ.clear()
            os.environ.update(old)
        return code, [json.loads(line) for line in out.getvalue().splitlines()]

    def test_no_settings(self):
        code, answers = self.run_main(["pulled"], {})
        self.assertEqual((code, answers[0]["error"]["code"]), (1, "settings_missing"))

    def test_a_tier_that_cannot_be_reached(self):
        code, answers = self.run_main(["pulled", "--phoenix", tempfile.mkdtemp(), "--garura", "/no/such/folder"], {})
        self.assertEqual((answers[0]["error"]["code"], answers[0]["error"]["tier"]), ("tier_missing", "garura"))

    def test_phoenix_must_be_a_repository(self):
        code, answers = self.run_main(["pulled"], {"MEMORY_PHOENIX_ROOT": tempfile.mkdtemp(),
                                                   "MEMORY_GARURA_ROOT": tempfile.mkdtemp()})
        self.assertEqual((answers[0]["error"]["code"], answers[0]["error"]["tier"]), ("tier_missing", "phoenix"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
