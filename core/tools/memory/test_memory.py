#!/usr/bin/env python3
"""Tests for memory.py. Run from the tool's folder: python3 test_memory.py

Every answer the tool gives is also put through the contract check (shape and answer
rules), so the tool cannot drift from contract/v2.json.
"""

import contextlib
import io
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "contract"))
import check_contract as cc  # noqa: E402
import memory  # noqa: E402
import test_pull  # noqa: E402
from test_pull import git, scratch, write  # noqa: E402


class Tiers(test_pull.Tiers):
    """The pull tests' throwaway Phoenix repository, plus a project whose short-term folder
    sits inside Garura memory."""

    def setUp(self):
        super().setUp()
        write(self.phoenix, "knowledge/domains/user-management.md",
              "# User management\n## Sign-in\n- Lock the account after five failed sign-ins.\n"
              "## Passwords\n- A reset link expires after one hour.\n")
        self.commit("user management")
        self.project = scratch(self)
        self.garura = os.path.join(self.project, "g")
        self.short = os.path.join(self.garura, "issues")
        os.makedirs(self.short)
        self.env = {"MEMORY_SHORT_TERM_ROOT": self.short, "MEMORY_GARURA_ROOT": self.garura,
                    "MEMORY_PHOENIX_ROOT": self.phoenix, "MEMORY_PHOENIX_REF": "main",
                    "MEMORY_GARURA_PULL_DIR": "pulled-memory"}

    def ask(self, command, request, env=None):
        """One answer, checked against the contract before the test sees it."""
        answers = memory.run(command, request, self.env if env is None else env)
        if command not in ("pull", "pulled"):
            spec = memory.CONTRACT["commands"][command]
            for a in answers:
                if cc.validate(request, spec["request"], memory.CONTRACT):
                    # a request the contract refuses: the answer must be that refusal
                    self.assertEqual(cc.validate(a, spec["response"], memory.CONTRACT), [], a)
                    self.assertEqual(a["error"]["code"], "bad_request", a)
                    continue
                problems = cc.check_sample({"command": command, "request": request, "response": a},
                                           memory.CONTRACT)
                self.assertEqual(problems, [], (command, request, a))
        return answers[0]


class LookupOrder(Tiers):
    def test_nothing_anywhere_looks_in_every_tier(self):
        a = self.ask("search", {"issue": 7, "pattern": "checkout"})
        self.assertEqual((a["looked_in"], a["answered_by"], a["hits"]),
                         (["short-term", "garura", "phoenix"], None, []))

    def test_goes_up_to_phoenix(self):
        a = self.ask("search", {"issue": 7, "pattern": "reset link"})
        self.assertEqual(a["answered_by"], "phoenix")
        self.assertEqual(a["hits"][0]["path"], "knowledge/domains/user-management.md")
        self.assertEqual(a["hits"][0]["line"], 5)

    def test_the_lowest_tier_answers_first(self):
        write(self.garura, "decisions/auth.md", "Reset link expires after 30 minutes here.\n")
        write(self.short, "7/notes.md", "reset link: ask the person\n")
        a = self.ask("search", {"issue": 7, "pattern": "reset link", "ignore_case": True})
        self.assertEqual((a["looked_in"], a["answered_by"]), (["short-term"], "short-term"))
        self.assertEqual(a["hits"][0]["path"], "7/notes.md")

    def test_every_tier_does_not_stop(self):
        write(self.garura, "decisions/auth.md", "Reset link expires after 30 minutes here.\n")
        a = self.ask("search", {"issue": 7, "pattern": "reset link", "ignore_case": True, "every_tier": True})
        self.assertEqual(a["answered_by"], "garura")
        self.assertEqual([h["tier"] for h in a["hits"]], ["garura", "phoenix"])

    def test_one_tier_only(self):
        a = self.ask("search", {"issue": 7, "pattern": "reset link", "tier": "garura"})
        self.assertEqual((a["looked_in"], a["answered_by"]), (["garura"], None))

    def test_tier_and_every_tier_is_refused(self):
        a = self.ask("search", {"issue": 7, "pattern": "x", "tier": "garura", "every_tier": True})
        self.assertEqual(a["error"]["code"], "bad_request")

    def test_find_by_glob(self):
        a = self.ask("find", {"issue": 7, "glob": "**/user-management.md"})
        self.assertEqual(a["answered_by"], "phoenix")
        self.assertEqual(a["matches"][0]["version"], self.ask("health", {})["tiers"][2]["version"])

    def test_max_truncates(self):
        a = self.ask("search", {"issue": 7, "pattern": "e", "tier": "phoenix", "max": 2})
        self.assertEqual((len(a["hits"]), a["truncated"]), (2, True))

    def test_fixed_text_and_a_bad_pattern(self):
        self.assertEqual(self.ask("search", {"issue": 7, "pattern": "(one", "fixed": True})["answered_by"], None)
        self.assertEqual(self.ask("search", {"issue": 7, "pattern": "(one"})["error"]["code"], "bad_request")


class ShortTerm(Tiers):
    def setUp(self):
        super().setUp()
        write(self.short, "613/specs/plan.md", "old notes about the reset link\n")

    def test_another_issue_never_answers(self):
        a = self.ask("search", {"issue": 7, "pattern": "reset link"})
        self.assertEqual(a["answered_by"], "phoenix")

    def test_short_term_is_not_garura_memory(self):
        a = self.ask("find", {"issue": 7, "glob": "**/plan.md", "tier": "garura"})
        self.assertEqual(a["matches"], [])

    def test_reading_another_issue_is_refused(self):
        a = self.ask("read", {"issue": 7, "tier": "short-term", "path": "613/specs/plan.md"})
        self.assertEqual(a["error"]["code"], "bad_request")

    def test_paths_that_step_outside_are_refused(self):
        for command, request in (("find", {"issue": 7, "glob": "../613/**"}),
                                 ("search", {"issue": 7, "pattern": "x", "glob": "../613/**"}),
                                 ("read", {"issue": 7, "tier": "garura", "path": "../x.md"})):
            self.assertEqual(self.ask(command, request)["error"]["code"], "bad_request", command)

    def test_own_issue_paths_carry_the_issue(self):
        write(self.short, "7/specs/plan.md", "the plan\n")
        a = self.ask("find", {"issue": 7, "glob": "specs/*.md"})
        self.assertEqual([m["path"] for m in a["matches"]], ["7/specs/plan.md"])


class WithoutAnIssue(Tiers):
    """Version 2: work can look things up before its issue exists."""

    def test_the_lookup_starts_at_garura_memory(self):
        write(self.short, "7/notes.md", "reset link: ask the person\n")
        a = self.ask("search", {"pattern": "reset link"})
        self.assertEqual((a["looked_in"], a["answered_by"]), (["garura", "phoenix"], "phoenix"))

    def test_nothing_found_looks_in_garura_and_phoenix(self):
        a = self.ask("find", {"glob": "**/nothing.md"})
        self.assertEqual((a["looked_in"], a["answered_by"]), (["garura", "phoenix"], None))

    def test_short_term_needs_an_issue(self):
        self.assertEqual(self.ask("search", {"pattern": "x", "tier": "short-term"})["error"]["code"], "bad_request")
        a = self.ask("read", {"tier": "short-term", "path": "7/notes.md"})
        self.assertEqual(a["error"]["code"], "bad_request")

    def test_a_phoenix_read_needs_no_issue(self):
        a = self.ask("read", {"tier": "phoenix", "path": "standards/rules/commits.md"})
        self.assertEqual(a["text"], "# Commits\nSubject under 72.")


class Read(Tiers):
    def test_exact_lines_and_fingerprint(self):
        a = self.ask("read", {"issue": 7, "tier": "phoenix", "path": "knowledge/domains/user-management.md",
                              "start": 2, "end": 3})
        self.assertEqual(a["text"], "## Sign-in\n- Lock the account after five failed sign-ins.")
        self.assertEqual(a["fingerprint"], cc.fingerprint(a["text"]))

    def test_whole_file_by_default(self):
        a = self.ask("read", {"issue": 7, "tier": "phoenix", "path": "standards/rules/commits.md"})
        self.assertEqual((a["start"], a["end"], a["text"]), (1, 2, "# Commits\nSubject under 72."))

    def test_refusals(self):
        path = "standards/rules/commits.md"
        for request, code in (({"start": 2, "end": 1}, "bad_request"), ({"start": 1, "end": 9}, "out_of_range"),
                              ({"path": "standards/missing.md"}, "not_found")):
            req = {"issue": 7, "tier": "phoenix", "path": path} | request
            self.assertEqual(self.ask("read", req)["error"]["code"], code, request)


class UsedMemoryIsSaved(Tiers):
    def test_a_phoenix_read_is_pulled_and_then_answered_by_garura(self):
        first = self.ask("search", {"issue": 7, "pattern": "reset link"})
        self.assertEqual(first["answered_by"], "phoenix")
        self.ask("read", {"issue": 7, "tier": "phoenix", "path": first["hits"][0]["path"]})
        again = self.ask("search", {"issue": 7, "pattern": "reset link"})
        self.assertEqual(again["answered_by"], "garura")
        self.assertEqual(again["hits"][0]["path"], "pulled-memory/knowledge/domains/user-management.md")
        listed = memory.run("pulled", {}, self.env)[0]["pieces"]
        self.assertEqual([p["path"] for p in listed], ["knowledge/domains/user-management.md"])

    def test_a_search_hit_alone_pulls_nothing(self):
        self.ask("search", {"issue": 7, "pattern": "reset link"})
        self.assertFalse(os.path.exists(os.path.join(self.garura, "pulled-memory")))


class ApprovedPhoenixOnly(Tiers):
    def test_an_unmerged_change_is_not_read(self):
        git(self.phoenix, "checkout", "-q", "-b", "promote-proposal")
        write(self.phoenix, "knowledge/domains/user-management.md", "- Reset links never expire.\n")
        self.commit("proposal, not approved")
        a = self.ask("search", {"issue": 7, "pattern": "never expire"})
        self.assertEqual(a["answered_by"], None)

    def test_a_working_tree_edit_is_not_read(self):
        write(self.phoenix, "knowledge/domains/new.md", "- Unapproved note.\n")
        self.assertEqual(self.ask("search", {"issue": 7, "pattern": "Unapproved"})["answered_by"], None)
        self.assertEqual(self.ask("find", {"issue": 7, "glob": "**/new.md"})["matches"], [])


class Settings(Tiers):
    def test_no_settings(self):
        self.assertEqual(self.ask("health", {}, env={})["error"]["code"], "settings_missing")

    def test_a_missing_tier_is_an_error_not_nothing(self):
        env = dict(self.env)
        del env["MEMORY_PHOENIX_ROOT"]
        a = self.ask("search", {"issue": 7, "pattern": "nothing here"}, env)
        self.assertEqual((a["error"]["code"], a["error"]["tier"]), ("tier_missing", "phoenix"))

    def test_health_reports_an_unreachable_tier(self):
        env = dict(self.env, MEMORY_GARURA_ROOT=os.path.join(self.project, "missing"))
        tiers = {t["tier"]: t["reachable"] for t in self.ask("health", {}, env)["tiers"]}
        self.assertEqual(tiers, {"short-term": True, "garura": False, "phoenix": True})

    def test_no_approved_version(self):
        env = dict(self.env, MEMORY_PHOENIX_REF="origin/main")
        a = self.ask("search", {"issue": 7, "pattern": "reset link"}, env)
        self.assertEqual((a["error"]["code"], a["error"]["tier"]), ("tier_missing", "phoenix"))

    def test_a_settings_file(self):
        write(self.project, "memory-settings.json",
              '{"short-term": "g/issues", "garura": "g", "phoenix": "%s", "phoenix_ref": "main"}' % self.phoenix)
        env = {"MEMORY_SETTINGS": os.path.join(self.project, "memory-settings.json")}
        self.assertEqual(self.ask("search", {"issue": 7, "pattern": "reset link"}, env)["answered_by"], "phoenix")

    def test_another_engine_is_one_setting_away(self):
        env = dict(self.env, MEMORY_ENGINE="server")
        self.assertEqual(self.ask("health", {}, env)["error"]["code"], "settings_missing")

    def test_a_request_the_contract_refuses(self):
        self.assertEqual(self.ask("search", {"issue": 7})["error"]["code"], "bad_request")
        self.assertEqual(memory.run("find", {"issue": 7, "glob": "*", "extra": 1}, self.env)[0]["error"]["code"],
                         "bad_request")


class CommandLine(Tiers):
    """Every command line gets a JSON answer, even one the tool cannot read."""

    def main(self, argv):
        old = dict(os.environ)
        os.environ.update(self.env)
        try:
            with contextlib.redirect_stdout(io.StringIO()) as out:
                code = memory.main(argv)
        finally:
            os.environ.clear()
            os.environ.update(old)
        return code, [json.loads(line) for line in out.getvalue().splitlines()]

    def test_flags_and_a_whole_request_give_the_same_answer(self):
        _, by_flags = self.main(["search", "--issue", "7", "--pattern", "reset link"])
        _, by_request = self.main(["search", "--request", '{"issue": 7, "pattern": "reset link"}'])
        self.assertEqual(by_flags, by_request)
        self.assertEqual(by_flags[0]["answered_by"], "phoenix")

    def test_what_the_tool_cannot_read_is_bad_request(self):
        for argv in (["pull"], ["search", "--issue", "7", "--pattern", "x", "--tier", "project"],
                     ["find", "--request", "{bad"], ["find", "--request", "[1]"], ["read", "--issue", "abc"]):
            code, answers = self.main(argv)
            self.assertEqual((code, answers[0]["error"]["code"]), (1, "bad_request"), argv)

    def test_garura_memory_that_cannot_be_written(self):
        blocked = os.path.join(self.garura, "pulled-memory")
        os.makedirs(self.garura, exist_ok=True)
        with open(blocked, "w") as fh:
            fh.write("a file where the pull folder should be")
        code, answers = self.main(["read", "--tier", "phoenix", "--path", "standards/rules/commits.md"])
        self.assertEqual((code, answers[0]["error"]["code"], answers[0]["error"]["tier"]),
                         (1, "tier_missing", "garura"))


class Boundary(unittest.TestCase):
    def test_nothing_in_the_folder_names_a_project(self):
        self.assertEqual(cc.check_boundary(), [])


if __name__ == "__main__":
    unittest.main(verbosity=1)
