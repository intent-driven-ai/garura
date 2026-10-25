#!/usr/bin/env python3
"""Tests for copy_memory.py. Run: python3 test_copy_memory.py"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "copy_memory.py")


def answer(text="# Commits\nSubject under 72.", path="standards/rules/commits.md", **extra):
    a = {"ok": True, "contract_version": "5", "command": "read", "tier": "phoenix", "path": path,
         "start": 1, "end": 2, "text": text, "fingerprint": "sha256:abc", "version": "v1"}
    a.update(extra)
    return json.dumps(a)


class CopyMemoryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        self.manifest = os.path.join(self.root, "context", "memory", "manifest.json")

    def tearDown(self):
        self.tmp.cleanup()

    def copy_path(self, rel):
        return os.path.join(self.root, "context", "memory", rel)

    def run_script(self, stdin, copy, manifest=None):
        return subprocess.run([sys.executable, SCRIPT, copy, manifest or self.manifest],
                              input=stdin, capture_output=True, text=True)

    def read_manifest(self):
        with open(self.manifest, encoding="utf-8") as fh:
            return json.load(fh)

    def test_writes_the_copy_and_makes_folders(self):
        copy = self.copy_path("standards/rules/commits.md")
        result = self.run_script(answer(), copy)
        self.assertEqual(result.returncode, 0, result.stderr)
        with open(copy, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "# Commits\nSubject under 72.")
        self.assertTrue(json.loads(result.stdout)["ok"])

    def test_adds_the_manifest_entry(self):
        copy = self.copy_path("standards/rules/commits.md")
        self.run_script(answer(), copy)
        self.assertEqual(self.read_manifest(), {"files": [
            {"tier": "phoenix", "path": "standards/rules/commits.md", "version": "v1",
             "fingerprint": "sha256:abc", "copy": copy}]})

    def test_a_second_copy_of_the_same_file_replaces_its_entry(self):
        copy = self.copy_path("standards/rules/commits.md")
        self.run_script(answer(), copy)
        self.run_script(answer(text="new", fingerprint="sha256:def", version="v2"), copy)
        files = self.read_manifest()["files"]
        self.assertEqual(len(files), 1)
        self.assertEqual((files[0]["fingerprint"], files[0]["version"]), ("sha256:def", "v2"))
        with open(copy, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "new")

    def test_other_entries_and_keys_are_kept(self):
        os.makedirs(os.path.dirname(self.manifest))
        with open(self.manifest, "w", encoding="utf-8") as fh:
            json.dump({"note": "kept", "files": [{"copy": "other.md", "tier": "garura"}]}, fh)
        copy = self.copy_path("standards/rules/commits.md")
        self.run_script(answer(), copy)
        manifest = self.read_manifest()
        self.assertEqual(manifest["note"], "kept")
        self.assertEqual([f["copy"] for f in manifest["files"]], ["other.md", copy])

    def test_a_refused_read_writes_nothing_and_exits_1(self):
        refused = json.dumps({"ok": False, "command": "read",
                              "error": {"code": "not_found", "message": "phoenix memory has no file x.md."}})
        copy = self.copy_path("x.md")
        result = self.run_script(refused, copy)
        self.assertEqual(result.returncode, 1)
        self.assertIn("not_found", result.stderr)
        self.assertFalse(os.path.exists(copy))
        self.assertFalse(os.path.exists(self.manifest))

    def test_input_that_is_not_json_exits_1(self):
        result = self.run_script("not json", self.copy_path("x.md"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("not JSON", result.stderr)

    def test_an_answer_with_no_fingerprint_exits_1(self):
        bad = json.loads(answer())
        del bad["fingerprint"]
        result = self.run_script(json.dumps(bad), self.copy_path("x.md"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("fingerprint", result.stderr)

    def test_the_answer_of_another_command_exits_1(self):
        result = self.run_script(answer(command="find"), self.copy_path("x.md"))
        self.assertEqual(result.returncode, 1)

    def test_a_broken_manifest_exits_1_and_writes_no_copy(self):
        os.makedirs(os.path.dirname(self.manifest))
        with open(self.manifest, "w", encoding="utf-8") as fh:
            fh.write("{broken")
        copy = self.copy_path("x.md")
        result = self.run_script(answer(), copy)
        self.assertEqual(result.returncode, 1)
        self.assertIn("not valid JSON", result.stderr)
        self.assertFalse(os.path.exists(copy))

    def test_wrong_arguments_exit_1(self):
        result = subprocess.run([sys.executable, SCRIPT, "only-one"], input=answer(),
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Usage", result.stderr)

    def test_no_temp_file_is_left_beside_the_manifest(self):
        copy = self.copy_path("standards/rules/commits.md")
        self.run_script(answer(), copy)
        leftovers = [n for n in os.listdir(os.path.dirname(self.manifest)) if n.endswith(".tmp")]
        self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main()
