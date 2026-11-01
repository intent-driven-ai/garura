"""Tests for remove_part.py: an approved removal goes through whole, or nothing changes."""

import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "remove_part.py")
sys.path.insert(0, HERE)
import remove_part  # noqa: E402

SPINE = """\
# The spine — a comment that must stay.
domains:
- id: dom-1
  slug: dom-1
  intents:
  - bi-1
  status: proposed
  one_line: Mail
  doc: mail/domain.md

# A comment between two lists, that must stay.
capabilities:
# A comment inside a list, that must stay.
- id: cap-1
  slug: cap-1
  domain: dom-1
  intents:
  - bi-1
  status: proposed
  one_line: Send mail
  doc: capabilities/cap-1/capability.md
  depends_on: []
  identified_by: ''
  metadata:
    created_by: /test
# A comment above the second capability, that must stay.
- id: cap-2
  slug: cap-2
  domain: dom-1
  intents:
  - bi-1
  - bi-2
  status: proposed
  one_line: Read mail
  doc: capabilities/cap-2/capability.md
  depends_on:
  - cap-1
  identified_by: cap-1
  decisions:
  - dec-2
  issue: 22
  nfr_needs:
    performance:
      level: high
  compliance_needs:
  - gdpr
- id: cap-3
  slug: cap-3
  domain: dom-1
  intents:
  - bi-2
  status: proposed
  one_line: File mail
  doc: capabilities/cap-3/capability.md
  depends_on:
  - cap-2
  - cap-1
  identified_by: cap-2
- id: cap-4
  slug: cap-4
  domain: dom-1
  intents:
  - bi-2
  status: proposed
  one_line: Flag mail
  doc: capabilities/cap-4/capability.md
  depends_on:
  - cap-2
  identified_by: ''
features:
- id: fn-1
  slug: fn-1
  capability: cap-2
  intents:
  - bi-1
  status: proposed
  one_line: Read one message
  doc: features/fn-1/feature.md
  depends_on: []
  identified_by: cap-2
- id: fn-2
  slug: fn-2
  capability: cap-1
  intents:
  - bi-1
  status: proposed
  one_line: Send one message
  doc: features/fn-2/feature.md
  depends_on:
  - cap-2
  - cap-4
  identified_by: ''
slices:
- id: sl-1
  slug: sl-1
  feature_refs:
  - fn-1
  vertical: the mail screen
  intents:
  - bi-1
  record: slices/sl-1.yaml
- id: sl-2
  slug: sl-2
  feature_refs:
  - fn-2
  vertical: the mail screen
  intents:
  - bi-2
# A comment at the end, that must stay.
"""

COMMENTS = ["# The spine — a comment that must stay.", "# A comment between two lists, that must stay.",
            "# A comment inside a list, that must stay.", "# A comment above the second capability, that must stay.",
            "# A comment at the end, that must stay."]


def request(**kw):
    body = {"by": "/test", "approved_by": "the product owner"}
    body.update(kw)
    return body


class RemovePartCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = os.path.join(self.tmp.name, "base") + os.sep
        self.root = os.path.join(self.base, "product-os")
        self.out = os.path.join(self.tmp.name, "working", "report.json")
        self.req = os.path.join(self.tmp.name, "request.json")
        self.write("_spine.yaml", SPINE)
        self.write("mail/domain.md", "# Domain: Mail\n")
        self.write("capabilities/cap-1/capability.md", "# Capability: Send mail\n")
        self.write("capabilities/cap-2/capability.md", "# Capability: Read mail\n")
        self.write("capabilities/cap-3/capability.md", "# Capability: File mail\n")
        self.write("capabilities/cap-4/capability.md", "# Capability: Flag mail\n")
        self.write("features/fn-1/feature.md", "# Feature: Read one message\n")
        self.write("features/fn-2/feature.md", "# Feature: Send one message\n")
        self.write("intents/bi-1.md", "# People get their mail\n")
        self.write("intents/bi-2.md", "# People keep their mail\n")
        self.write("intents/bi-3.md", "# People find their mail\n")
        self.write("slices/sl-1.yaml", "slice:\n  name: Read mail\n")
        self.write("slices/sl-2.yaml", "slice:\n  name: Send mail\n")

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def read(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as fh:
            return fh.read()

    def exists(self, rel):
        return os.path.exists(os.path.join(self.root, rel))

    def tree(self):
        """Every file under the model with its bytes and permissions."""
        out = {}
        for here, dirs, files in os.walk(self.root):
            for name in dirs:
                path = os.path.join(here, name)
                out[os.path.relpath(path, self.root) + "/"] = stat.S_IMODE(os.stat(path).st_mode)
            for name in files:
                path = os.path.join(here, name)
                with open(path, "rb") as fh:
                    out[os.path.relpath(path, self.root)] = (fh.read(), stat.S_IMODE(os.stat(path).st_mode))
        return out

    def run_script(self, body):
        with open(self.req, "w", encoding="utf-8") as fh:
            json.dump(body, fh)
        return subprocess.run([sys.executable, SCRIPT, "--request", self.req, "--product-base", self.base,
                               "--out", self.out], capture_output=True, text=True)

    def done(self, body):
        r = self.run_script(body)
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(self.out, encoding="utf-8") as fh:
            return json.load(fh)

    def spine(self):
        return yaml.safe_load(self.read("_spine.yaml"))

    def part(self, key, pid):
        return next(e for e in self.spine()[key] if e["id"] == pid)

    def assert_refused(self, body, *words):
        before = self.tree()
        r = self.run_script(body)
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("refused, nothing written", r.stderr)
        self.assertNotIn("Traceback", r.stderr)
        for word in words:
            self.assertIn(word, r.stderr)
        self.assertEqual(self.tree(), before)
        self.assertFalse(os.path.exists(self.out))


class Repoint(RemovePartCase):
    def test_the_new_intent_takes_the_old_ones_place(self):
        rep = self.done(request(repoint=[{"id": "cap-2", "kind": "capability", "intents": {"bi-1": "bi-3"}}]))
        self.assertEqual(self.part("capabilities", "cap-2")["intents"], ["bi-3", "bi-2"])
        self.assertEqual(rep["repointed"], ["cap-2"])
        self.assertEqual(rep["changed"], ["product-os/_spine.yaml"])
        self.assertEqual(rep["deleted"], [])

    def test_null_drops_the_old_intent(self):
        self.done(request(repoint=[{"id": "cap-2", "kind": "capability", "intents": {"bi-1": None}}]))
        self.assertEqual(self.part("capabilities", "cap-2")["intents"], ["bi-2"])

    def test_a_new_intent_already_there_is_not_doubled(self):
        self.done(request(repoint=[{"id": "cap-2", "kind": "capability", "intents": {"bi-1": "bi-2"}}]))
        self.assertEqual(self.part("capabilities", "cap-2")["intents"], ["bi-2"])

    def test_two_parts_that_shared_an_intent_go_to_different_new_ones(self):
        self.done(request(repoint=[{"id": "dom-1", "kind": "domain", "intents": {"bi-1": "bi-3"}},
                                   {"id": "cap-1", "kind": "capability", "intents": {"bi-1": "bi-2"}},
                                   {"id": "fn-1", "kind": "feature", "intents": {"bi-1": "bi-3"}},
                                   {"id": "sl-1", "kind": "slice", "intents": {"bi-1": "bi-2"}}]))
        self.assertEqual(self.part("domains", "dom-1")["intents"], ["bi-3"])
        self.assertEqual(self.part("capabilities", "cap-1")["intents"], ["bi-2"])
        self.assertEqual(self.part("features", "fn-1")["intents"], ["bi-3"])
        self.assertEqual(self.part("slices", "sl-1")["intents"], ["bi-2"])

    def test_refusals(self):
        refusals = [
            ({"id": "cap-1", "kind": "capability", "intents": {"bi-2": "bi-3"}}, ["cap-1", "bi-2"]),
            ({"id": "cap-9", "kind": "capability", "intents": {"bi-1": "bi-3"}}, ["cap-9"]),
            ({"id": "cap-1", "kind": "feature", "intents": {"bi-1": "bi-3"}}, ["cap-1", "feature"]),
            ({"id": "cap-1", "kind": "intent", "intents": {"bi-1": "bi-3"}}, ["unknown"]),
            ({"id": "cap-1", "kind": "capability", "intents": {"bi-1": "bi-9"}}, ["bi-9", "no page"]),
            ({"id": "cap-1", "kind": "capability", "intents": {"bi-1": "../../bi-3"}}, ["leaves the model"]),
            ({"id": "cap-1", "kind": "capability", "intents": {}}, ["cap-1"]),
        ]
        for item, words in refusals:
            self.assert_refused(request(repoint=[item]), *words)

    def test_a_new_intent_this_request_removes_is_refused(self):
        self.assert_refused(request(repoint=[{"id": "cap-1", "kind": "capability", "intents": {"bi-1": "bi-3"}}],
                                    remove=[{"kind": "intent", "id": "bi-3"}]), "cap-1", "bi-3", "removes")


class RemoveIntent(RemovePartCase):
    def setUp(self):
        super().setUp()
        self.body = request(repoint=[{"id": "cap-3", "kind": "capability", "intents": {"bi-2": "bi-3"}},
                                     {"id": "cap-4", "kind": "capability", "intents": {"bi-2": "bi-3"}},
                                     {"id": "cap-2", "kind": "capability", "intents": {"bi-2": None}},
                                     {"id": "sl-2", "kind": "slice", "intents": {"bi-2": "bi-3"}}],
                            remove=[{"kind": "intent", "id": "bi-2"}])

    def test_its_page_goes_once_nothing_names_it(self):
        rep = self.done(self.body)
        self.assertFalse(self.exists("intents/bi-2.md"))
        self.assertEqual(rep["removed"], ["bi-2"])
        self.assertEqual(rep["deleted"], ["product-os/intents/bi-2.md"])
        self.assertEqual(rep["approved_by"], "the product owner")
        self.assertEqual(rep["by"], "/test")
        self.assertTrue(rep["layout_kept"])

    def test_it_is_refused_while_a_part_names_it(self):
        self.assert_refused(request(remove=[{"kind": "intent", "id": "bi-2"}]),
                            "bi-2", "still named by", "capability cap-2", "capability cap-3", "slice sl-2")

    def test_its_page_must_be_there(self):
        self.assert_refused(request(remove=[{"kind": "intent", "id": "bi-9"}]), "bi-9", "no page")

    def test_an_id_that_leaves_the_folder_is_refused(self):
        self.write("../outside.md", "not model\n")
        self.assert_refused(request(remove=[{"kind": "intent", "id": "../../outside"}]), "leaves the model")
        self.assert_refused(request(remove=[{"kind": "intent", "id": "Bi 1"}]), "Bi 1")
        self.assert_refused(request(remove=[{"kind": "intent", "id": "bi-1\n"}]), "leaves the model")

    def test_a_link_that_leaves_the_folder_is_refused(self):
        outside = os.path.join(self.tmp.name, "outside.md")
        with open(outside, "w", encoding="utf-8") as fh:
            fh.write("not model\n")
        os.symlink(outside, os.path.join(self.root, "intents", "bi-8.md"))
        self.assert_refused(request(remove=[{"kind": "intent", "id": "bi-8"}]), "leaves the model")
        with open(outside, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "not model\n")

    def test_a_longer_id_is_not_a_mention(self):
        self.write("features/fn-1/feature.md", "This names bi-22, bi-2-old and not-bi-2 only.\n")
        self.done(self.body)

    def test_a_mention_on_a_page_is_refused_with_its_path_and_line(self):
        self.write("features/fn-1/feature.md", "# Feature\n\nIt serves bi-2.\n")
        self.write("slices/sl-1.yaml", "slice:\n  intents: [bi-2]\n")
        self.assert_refused(self.body, "features/fn-1/feature.md:3", "slices/sl-1.yaml:2", "page skill")

    def test_only_md_and_yaml_files_count(self):
        self.write("notes/old.txt", "bi-2\n")
        self.done(self.body)
        self.assertTrue(self.exists("notes/old.txt"))

    def test_a_comment_in_the_spine_does_not_count(self):
        self.write("_spine.yaml", "# bi-2 was once here.\n" + SPINE)
        rep = self.done(self.body)
        self.assertIn("# bi-2 was once here.", self.read("_spine.yaml"))
        self.assertEqual(rep["removed"], ["bi-2"])

    def test_the_spine_naming_it_outside_the_intents_is_refused(self):
        self.write("_spine.yaml", SPINE.replace("one_line: Send mail", "one_line: Send mail for bi-2"))
        self.assert_refused(self.body, "bi-2", "capability cap-1", "one_line")


class MergeCapability(RemovePartCase):
    merge = {"kind": "capability", "id": "cap-2", "into": "cap-3"}

    def test_everything_that_named_it_now_names_the_survivor(self):
        rep = self.done(request(remove=[self.merge]))
        self.assertNotIn("cap-2", [c["id"] for c in self.spine()["capabilities"]])
        self.assertEqual(self.part("features", "fn-1")["capability"], "cap-3")
        self.assertEqual(self.part("features", "fn-2")["capability"], "cap-1")
        self.assertEqual(self.part("features", "fn-1")["identified_by"], "cap-3")
        self.assertEqual(self.part("features", "fn-2")["depends_on"], ["cap-3", "cap-4"])
        self.assertEqual(self.part("capabilities", "cap-4")["depends_on"], ["cap-3"])
        self.assertEqual(rep["merged"], [{"id": "cap-2", "into": "cap-3"}])
        self.assertEqual(rep["moved_features"], ["fn-1"])
        self.assertEqual(rep["removed"], ["cap-2"])

    def test_the_survivor_never_names_itself(self):
        self.done(request(remove=[self.merge]))
        survivor = self.part("capabilities", "cap-3")
        self.assertEqual(survivor["identified_by"], "")
        self.assertEqual(survivor["depends_on"], ["cap-1"])

    def test_no_list_holds_the_survivor_twice(self):
        self.write("_spine.yaml", SPINE.replace("  - cap-2\n  - cap-4\n", "  - cap-2\n  - cap-3\n  - cap-4\n"))
        self.done(request(remove=[self.merge]))
        self.assertEqual(self.part("features", "fn-2")["depends_on"], ["cap-3", "cap-4"])

    def test_the_survivor_gains_its_intents_and_decisions_in_order(self):
        self.done(request(remove=[self.merge]))
        survivor = self.part("capabilities", "cap-3")
        self.assertEqual(survivor["intents"], ["bi-2", "bi-1"])
        self.assertEqual(survivor["decisions"], ["dec-2"])

    def test_its_issue_stays_on_record(self):
        self.done(request(remove=[self.merge]))
        self.assertEqual(self.part("capabilities", "cap-3")["metadata"]["merged_from"],
                         [{"id": "cap-2", "issue": 22, "one_line": "Read mail"}])

    def test_its_needs_are_listed_and_never_copied(self):
        rep = self.done(request(remove=[self.merge]))
        self.assertEqual(rep["needs_to_review"], [{"id": "cap-2", "nfr_needs": {"performance": {"level": "high"}},
                                                   "compliance_needs": ["gdpr"]}])
        survivor = self.part("capabilities", "cap-3")
        self.assertNotIn("nfr_needs", survivor)
        self.assertNotIn("compliance_needs", survivor)

    def test_no_needs_means_nothing_to_review(self):
        rep = self.done(request(remove=[{"kind": "capability", "id": "cap-4", "into": "cap-3"}]))
        self.assertEqual(rep["needs_to_review"], [])

    def test_its_page_and_empty_folder_go(self):
        rep = self.done(request(remove=[self.merge]))
        self.assertFalse(self.exists("capabilities/cap-2"))
        self.assertEqual(rep["deleted"], ["product-os/capabilities/cap-2/capability.md",
                                          "product-os/capabilities/cap-2"])

    def test_the_merged_id_may_stay_only_in_merged_from(self):
        text = self.read("_spine.yaml")
        self.done(request(remove=[self.merge]))
        spine = self.spine()
        self.assertEqual(len(remove_part.left_in_spine(spine, "cap-2")), 0)
        self.assertIn("cap-2", text)
        self.assertIn("id: cap-2", self.read("_spine.yaml"))  # the one merged_from line

    def test_a_second_merge_of_the_same_survivor_adds_to_its_record(self):
        self.done(request(remove=[self.merge, {"kind": "capability", "id": "cap-4", "into": "cap-3"}]))
        self.assertEqual([m["id"] for m in self.part("capabilities", "cap-3")["metadata"]["merged_from"]],
                         ["cap-2", "cap-4"])

    def test_refusals(self):
        refusals = [
            ({"kind": "capability", "id": "cap-2"}, ["cap-2", "into"]),
            ({"kind": "capability", "id": "cap-2", "into": "cap-2"}, ["cap-2", "itself"]),
            ({"kind": "capability", "id": "cap-2", "into": "cap-9"}, ["cap-9", "not in the spine"]),
            ({"kind": "capability", "id": "cap-9", "into": "cap-3"}, ["cap-9", "not in the spine"]),
        ]
        for item, words in refusals:
            self.assert_refused(request(remove=[item]), *words)

    def test_the_survivor_cannot_be_removed_in_the_same_request(self):
        self.assert_refused(request(remove=[self.merge, {"kind": "capability", "id": "cap-3", "into": "cap-1"}]),
                            "cap-3", "removed in this request")

    def test_a_folder_with_any_other_file_is_refused_naming_it(self):
        self.write("capabilities/cap-2/ice.md", "# ICE\n")
        self.assert_refused(request(remove=[self.merge]), "capabilities/cap-2/ice.md")

    def test_an_entry_in_the_ices_list_is_refused(self):
        ices = "ices:\n- id: ice-2\n  for: cap-2\n  for_kind: capability\n  doc: capabilities/cap-2/ice.md\n"
        self.write("_spine.yaml", SPINE + ices)
        self.assert_refused(request(remove=[self.merge]), "cap-2", "its own entry", "ices")

    def test_a_page_path_that_leaves_the_folder_is_refused(self):
        self.write("_spine.yaml", SPINE.replace("doc: capabilities/cap-2/capability.md", "doc: ../../outside.md"))
        self.assert_refused(request(remove=[self.merge]), "leaves the model")

    def test_a_mention_of_it_on_a_page_is_refused(self):
        self.write("capabilities/cap-3/capability.md", "# File mail\n\nFound while building cap-2.\n")
        self.assert_refused(request(remove=[self.merge]), "capabilities/cap-3/capability.md:3", "cap-2")

    def test_a_list_of_identified_by_is_pointed_too(self):
        self.write("_spine.yaml", SPINE.replace("  identified_by: cap-1\n", "  identified_by: [cap-1]\n")
                   .replace("  identified_by: cap-2\n- id: cap-4", "  identified_by: [cap-2, cap-1]\n- id: cap-4"))
        self.done(request(remove=[{"kind": "capability", "id": "cap-1", "into": "cap-3"}]))
        self.assertEqual(self.part("capabilities", "cap-2")["identified_by"], ["cap-3"])
        self.assertEqual(self.part("capabilities", "cap-3")["identified_by"], ["cap-2"])

    def test_a_slice_with_a_depends_on_list_is_pointed_too(self):
        self.write("_spine.yaml", SPINE.replace("  record: slices/sl-1.yaml\n",
                                                "  record: slices/sl-1.yaml\n  depends_on:\n  - cap-2\n"))
        self.done(request(remove=[self.merge]))
        self.assertEqual(self.part("slices", "sl-1")["depends_on"], ["cap-3"])

    def test_a_capability_with_no_page_on_disk_still_merges(self):
        os.remove(os.path.join(self.root, "capabilities/cap-2/capability.md"))
        os.rmdir(os.path.join(self.root, "capabilities/cap-2"))
        rep = self.done(request(remove=[self.merge]))
        self.assertEqual(rep["deleted"], [])

    def test_a_capability_with_no_page_named_still_merges(self):
        self.write("_spine.yaml", SPINE.replace("  doc: capabilities/cap-2/capability.md\n", ""))
        rep = self.done(request(remove=[self.merge]))
        self.assertEqual(rep["deleted"], [])
        self.assertTrue(self.exists("capabilities/cap-2/capability.md"))

    def test_empty_folders_inside_its_folder_go_too(self):
        os.makedirs(os.path.join(self.root, "capabilities/cap-2/empty/deeper"))
        rep = self.done(request(remove=[self.merge]))
        self.assertFalse(self.exists("capabilities/cap-2"))
        self.assertIn("product-os/capabilities/cap-2/empty/deeper", rep["deleted"])

    def test_a_page_at_the_top_of_the_model_never_takes_the_model_with_it(self):
        self.write("capability.md", "# A page at the top\n")
        self.write("_spine.yaml", SPINE.replace("doc: capabilities/cap-2/capability.md", "doc: capability.md"))
        self.assert_refused(request(remove=[self.merge]), "other files", "_spine.yaml")

    def test_a_survivor_with_no_metadata_gets_some(self):
        self.done(request(remove=[{"kind": "capability", "id": "cap-1", "into": "cap-3"}]))
        self.assertEqual(self.part("capabilities", "cap-3")["metadata"]["merged_from"][0]["issue"], None)


class RemoveSlice(RemovePartCase):
    def test_its_entry_and_its_record_go(self):
        rep = self.done(request(remove=[{"kind": "slice", "id": "sl-1"}]))
        self.assertEqual([s["id"] for s in self.spine()["slices"]], ["sl-2"])
        self.assertFalse(self.exists("slices/sl-1.yaml"))
        self.assertEqual(rep["deleted"], ["product-os/slices/sl-1.yaml"])

    def test_with_no_record_field_the_usual_path_is_used(self):
        self.done(request(remove=[{"kind": "slice", "id": "sl-2"}]))
        self.assertFalse(self.exists("slices/sl-2.yaml"))

    def test_a_record_not_on_disk_is_no_problem(self):
        os.remove(os.path.join(self.root, "slices", "sl-1.yaml"))
        rep = self.done(request(remove=[{"kind": "slice", "id": "sl-1"}]))
        self.assertEqual(rep["deleted"], [])

    def test_the_last_slice_can_go(self):
        self.done(request(remove=[{"kind": "slice", "id": "sl-1"}, {"kind": "slice", "id": "sl-2"}]))
        self.assertEqual(self.spine()["slices"], [])
        self.assertIn("# A comment at the end, that must stay.", self.read("_spine.yaml"))

    def test_nothing_under_the_plans_folder_is_touched(self):
        plan = os.path.join(self.tmp.name, "base", "plans", "1", "evals", "sl-1.md")
        os.makedirs(os.path.dirname(plan))
        with open(plan, "w", encoding="utf-8") as fh:
            fh.write("sl-1\n")
        self.done(request(remove=[{"kind": "slice", "id": "sl-1"}]))
        self.assertTrue(os.path.exists(plan))

    def test_an_id_not_in_the_spine_is_refused(self):
        self.assert_refused(request(remove=[{"kind": "slice", "id": "sl-9"}]), "sl-9", "not in the spine")

    def test_a_record_that_leaves_the_folder_is_refused(self):
        self.write("_spine.yaml", SPINE.replace("record: slices/sl-1.yaml", "record: ../../plans/1.yaml"))
        self.assert_refused(request(remove=[{"kind": "slice", "id": "sl-1"}]), "leaves the model")

    def test_another_part_of_the_spine_naming_it_is_refused(self):
        epics = "epics:\n- id: ep-1\n  slice: sl-1\n"
        self.write("_spine.yaml", SPINE + epics)
        self.assert_refused(request(remove=[{"kind": "slice", "id": "sl-1"}]), "sl-1", "epic")


class TheWholeRequest(RemovePartCase):
    def test_all_three_kinds_together_in_their_order(self):
        rep = self.done(request(
            repoint=[{"id": "dom-1", "kind": "domain", "intents": {"bi-1": "bi-3"}},
                     {"id": "cap-1", "kind": "capability", "intents": {"bi-1": "bi-3"}},
                     {"id": "cap-2", "kind": "capability", "intents": {"bi-1": "bi-3"}},
                     {"id": "fn-1", "kind": "feature", "intents": {"bi-1": "bi-3"}},
                     {"id": "fn-2", "kind": "feature", "intents": {"bi-1": "bi-3"}}],
            remove=[{"kind": "intent", "id": "bi-1"},
                    {"kind": "capability", "id": "cap-2", "into": "cap-3"},
                    {"kind": "slice", "id": "sl-1"}]))
        self.assertEqual(rep["removed"], ["bi-1", "cap-2", "sl-1"])
        self.assertEqual(rep["repointed"], ["dom-1", "cap-1", "cap-2", "fn-1", "fn-2"])
        self.assertEqual(self.part("capabilities", "cap-3")["intents"], ["bi-2", "bi-3"])
        self.assertFalse(self.exists("intents/bi-1.md"))
        self.assertFalse(self.exists("capabilities/cap-2"))
        self.assertFalse(self.exists("slices/sl-1.yaml"))

    def test_the_spine_keeps_its_comments(self):
        rep = self.done(request(remove=[{"kind": "capability", "id": "cap-2", "into": "cap-3"},
                                        {"kind": "slice", "id": "sl-2"}]))
        text = self.read("_spine.yaml")
        for comment in COMMENTS:
            self.assertIn(comment, text)
        self.assertTrue(text.startswith(COMMENTS[0]))
        self.assertTrue(rep["layout_kept"])

    def test_parts_that_did_not_change_keep_their_lines(self):
        self.done(request(remove=[{"kind": "capability", "id": "cap-2", "into": "cap-3"}]))
        block = "- id: cap-1\n  slug: cap-1\n  domain: dom-1\n  intents:\n  - bi-1\n"
        self.assertIn(block, self.read("_spine.yaml"))

    def test_one_bad_item_refuses_the_whole_request(self):
        self.assert_refused(request(remove=[{"kind": "slice", "id": "sl-1"}, {"kind": "slice", "id": "sl-9"}]), "sl-9")

    def test_general_refusals(self):
        slice_item = {"kind": "slice", "id": "sl-1"}
        refusals = [
            ({"remove": [slice_item]}, ["approved_by"]),
            (request(approved_by=""), ["approved_by"]),
            (request(approved_by="   ", remove=[slice_item]), ["approved_by"]),
            (request(), ["nothing to repoint"]),
            (request(repoint=[], remove=[]), ["nothing to repoint"]),
            (request(remove=[{"kind": "feature", "id": "fn-1"}]), ["unknown"]),
            (request(remove=[{"kind": "domain", "id": "dom-1"}]), ["unknown"]),
            (request(remove=[slice_item, slice_item]), ["sl-1", "twice"]),
            (request(remove=[{"kind": "slice", "id": "sl-1", "into": "sl-2"}]), ["only a capability merges"]),
            (request(remove="sl-1"), ["must be a list"]),
            (request(remove=[{"kind": "slice"}]), ["needs an id"]),
            ([1, 2], ["not a JSON object"]),
        ]
        for body, words in refusals:
            self.assert_refused(body, *words)

    def test_a_bad_request_file_is_refused(self):
        with open(self.req, "w", encoding="utf-8") as fh:
            fh.write("not json")
        r = subprocess.run([sys.executable, SCRIPT, "--request", self.req, "--product-base", self.base,
                            "--out", self.out], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("Traceback", r.stderr)

    def test_an_old_model_stops_on_its_old_names(self):
        self.write("_spine.yaml", SPINE.replace("features:", "functionalities:"))
        before = self.tree()
        r = self.run_script(request(remove=[{"kind": "slice", "id": "sl-1"}]))
        self.assertEqual(r.returncode, 2)
        self.assertIn("old name", r.stderr)
        self.assertEqual(self.tree(), before)

    def test_a_removal_with_no_spine_change_leaves_the_spine_alone(self):
        self.write("intents/bi-9.md", "# Nothing names this\n")
        before = self.read("_spine.yaml")
        rep = self.done(request(remove=[{"kind": "intent", "id": "bi-9"}]))
        self.assertEqual(self.read("_spine.yaml"), before)
        self.assertEqual(rep["changed"], [])
        self.assertEqual(rep["deleted"], ["product-os/intents/bi-9.md"])


class PutBack(RemovePartCase):
    def body(self):
        return request(remove=[{"kind": "capability", "id": "cap-2", "into": "cap-3"},
                               {"kind": "slice", "id": "sl-1"}])

    def lock(self, rel):
        path = os.path.join(self.root, rel)
        os.chmod(path, 0o555)
        self.addCleanup(os.chmod, path, 0o755)

    def test_a_delete_that_fails_puts_every_file_back(self):
        self.lock("slices")
        before = self.tree()
        r = self.run_script(self.body())
        self.assertEqual(r.returncode, 2)
        self.assertIn("every file is back", r.stderr)
        self.assertEqual(self.tree(), before)

    def test_a_report_that_cannot_be_written_puts_every_file_back(self):
        blocker = os.path.join(self.tmp.name, "a-file")
        with open(blocker, "w", encoding="utf-8") as fh:
            fh.write("x")
        self.out = os.path.join(blocker, "report.json")
        before = self.tree()
        r = self.run_script(self.body())
        self.assertEqual(r.returncode, 2)
        self.assertEqual(self.tree(), before)

    def apply_with(self, failing_call, failing_on):
        """Run the real steps in this process, with one os call failing on its nth use."""
        spine_path = os.path.join(self.root, "_spine.yaml")
        files = [os.path.join(self.root, "capabilities/cap-2/capability.md"),
                 os.path.join(self.root, "slices/sl-1.yaml")]
        folders = [os.path.join(self.root, "capabilities/cap-2")]
        real, calls = getattr(os, failing_call), []

        def flaky(path):
            calls.append(path)
            if len(calls) == failing_on:
                raise OSError("disk full")
            real(path)

        with mock.patch.object(os, failing_call, flaky):
            with self.assertRaises(OSError):
                remove_part.apply(spine_path, SPINE, "changed: true\n", files, folders, self.out, "{}\n")

    def test_the_second_delete_failing_puts_the_first_file_and_the_spine_back(self):
        os.chmod(os.path.join(self.root, "capabilities/cap-2/capability.md"), 0o640)
        before = self.tree()
        self.apply_with("remove", 2)
        self.assertEqual(self.tree(), before)

    def test_the_folder_delete_failing_puts_the_files_back(self):
        before = self.tree()
        self.apply_with("rmdir", 1)
        self.assertEqual(self.tree(), before)

    def test_a_rewritten_spine_keeps_its_permissions(self):
        path = os.path.join(self.root, "_spine.yaml")
        os.chmod(path, 0o640)
        self.done(self.body())
        self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o640)


if __name__ == "__main__":
    unittest.main()
