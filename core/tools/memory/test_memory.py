#!/usr/bin/env python3
"""Tests for memory.py. Run from the tool's folder: python3 test_memory.py

Every answer the tool gives is also put through the contract check (shape and answer
rules), so the tool cannot drift from contract/v4.json.
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
        spec = memory.CONTRACT["commands"][command]
        for a in answers:
            if cc.validate(request, spec["request"], memory.CONTRACT):
                # a request the contract refuses: the answer must be that refusal
                self.assertEqual(cc.validate(a, spec["response"], memory.CONTRACT), [], a)
                self.assertEqual(a["error"]["code"], "bad_request", a)
                continue
            problems = cc.check_sample({"command": command, "request": request, "response": a}, memory.CONTRACT)
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

    def test_the_read_says_where_it_saved(self):
        a = self.ask("read", {"issue": 7, "tier": "phoenix", "path": "standards/rules/commits.md"})
        self.assertEqual(a["saved_to"], {"tier": "garura", "path": "pulled-memory/standards/rules/commits.md"})

    def test_never_saved_over_a_different_garura_file(self):
        mine = os.path.join(self.garura, "pulled-memory", "standards/rules/commits.md")
        os.makedirs(os.path.dirname(mine))
        with open(mine, "w") as fh:
            fh.write("# Commits\nOur own rule: subject under 50.\n")
        a = self.ask("read", {"issue": 7, "tier": "phoenix", "path": "standards/rules/commits.md"})
        self.assertIn("not_saved", a)
        with open(mine) as fh:
            self.assertEqual(fh.read(), "# Commits\nOur own rule: subject under 50.\n")
        self.assertEqual(self.ask("pull", {"path": "standards/rules/commits.md"})["error"]["code"], "would_overwrite")

    def test_a_pulled_piece_is_refreshed_when_phoenix_moves_on(self):
        self.ask("read", {"issue": 7, "tier": "phoenix", "path": "standards/rules/commits.md"})
        write(self.phoenix, "standards/rules/commits.md", "# Commits\nSubject under 60.\n")
        self.commit("change")
        a = self.ask("read", {"issue": 7, "tier": "phoenix", "path": "standards/rules/commits.md"})
        self.assertIn("saved_to", a)

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


class Updates(Tiers):
    """A gap, a memory update, a person's word, the write — all in the issue's short-term memory."""

    def raise_update(self, **extra):
        request = {"issue": 7, "missing": "How long a reset link lasts in this product.",
                   "target_tier": "short-term", "target_path": "7/context/answers/reset-link.md",
                   "draft": "A reset link lasts 30 minutes in this product.", "draft_source": "web",
                   "sources": [], "requested_by": "test agent"} | extra
        return self.ask("propose", request)["update"]

    def decide(self, uid, verdict="approve"):
        return self.ask("decide", {"id": uid, "verdict": verdict, "by": "a person", "reply": verdict,
                                   "decided_in": "review-tool"})

    def test_the_whole_way_in_one_issue(self):
        gap = self.ask("search", {"issue": 7, "pattern": "30 minutes"})
        self.assertEqual(gap["answered_by"], None)
        update = self.raise_update()
        self.assertEqual((update["status"], update["blocking"]), ("waiting", False))
        self.assertEqual(self.ask("search", {"issue": 7, "pattern": "30 minutes"})["answered_by"], None)
        self.assertEqual(self.decide(update["id"])["update"]["status"], "approved")
        applied = self.ask("apply", {"id": update["id"]})
        self.assertEqual(applied["written"]["path"], "7/context/answers/reset-link.md")
        found = self.ask("search", {"issue": 7, "pattern": "30 minutes"})
        self.assertEqual((found["answered_by"], found["hits"][0]["path"]),
                         ("short-term", "7/context/answers/reset-link.md"))
        self.assertEqual(self.ask("search", {"issue": 8, "pattern": "30 minutes"})["answered_by"], None)

    def test_a_waiting_draft_is_never_found_or_read(self):
        update = self.raise_update()
        self.assertEqual(self.ask("search", {"issue": 7, "pattern": "30 minutes"})["answered_by"], None)
        self.assertEqual(self.ask("find", {"issue": 7, "glob": "**/mu-*.json"})["matches"], [])
        stored = f"7/review/memory-updates/{update['id']}.json"
        self.assertEqual(self.ask("read", {"issue": 7, "tier": "short-term", "path": stored})["error"]["code"],
                         "not_found")

    def test_a_rejected_update_writes_nothing(self):
        update = self.raise_update()
        self.decide(update["id"], "reject")
        self.assertEqual(self.ask("apply", {"id": update["id"]})["error"]["code"], "not_approved")
        self.assertFalse(os.path.exists(os.path.join(self.short, "7/context/answers/reset-link.md")))

    def test_nothing_is_written_before_a_person_decides(self):
        update = self.raise_update()
        self.assertEqual(self.ask("apply", {"id": update["id"]})["error"]["code"], "not_approved")

    def test_a_person_decides_once_and_it_is_applied_once(self):
        update = self.raise_update()
        self.decide(update["id"])
        self.assertEqual(self.decide(update["id"])["error"]["code"], "wrong_state")
        self.ask("apply", {"id": update["id"]})
        self.assertEqual(self.ask("apply", {"id": update["id"]})["error"]["code"], "wrong_state")

    def test_a_target_that_changed_is_not_written_over(self):
        update = self.raise_update()
        self.decide(update["id"])
        write(self.short, "7/context/answers/reset-link.md", "someone wrote here first\n")
        self.assertEqual(self.ask("apply", {"id": update["id"]})["error"]["code"], "changed")

    def test_an_update_stays_in_its_issue(self):
        a = self.ask("propose", {"issue": 7, "missing": "x", "target_tier": "short-term",
                                 "target_path": "8/context/x.md", "draft": "x", "draft_source": "person",
                                 "sources": [], "requested_by": "test agent"})
        self.assertEqual(a["error"]["code"], "bad_request")

    def test_an_update_never_writes_into_the_updates_folder(self):
        a = self.ask("propose", {"issue": 7, "missing": "x", "target_tier": "short-term",
                                 "target_path": "7/review/memory-updates/mu-20261018-001.json", "draft": "x",
                                 "draft_source": "person", "sources": [], "requested_by": "test agent"})
        self.assertEqual(a["error"]["code"], "bad_request")

    def test_an_update_never_targets_garura_or_phoenix(self):
        for tier in ("garura", "phoenix"):
            a = self.ask("propose", {"issue": 7, "missing": "x", "target_tier": tier, "target_path": "7/x.md",
                                     "draft": "x", "draft_source": "person", "sources": [],
                                     "requested_by": "test agent"})
            self.assertEqual(a["error"]["code"], "bad_request", tier)

    def test_listing_and_blocking(self):
        first = self.raise_update(blocking=True)
        second = self.raise_update(target_path="7/context/answers/other.md")
        self.decide(second["id"])
        waiting = self.ask("updates", {"status": "waiting"})["updates"]
        self.assertEqual([(u["id"], u["blocking"]) for u in waiting], [(first["id"], True)])
        self.assertEqual(len(self.ask("updates", {})["updates"]), 2)
        self.assertNotEqual(first["id"], second["id"])

    def test_an_unknown_update(self):
        self.assertEqual(self.ask("apply", {"id": "mu-20000101-001"})["error"]["code"], "not_found")


class Citations(Tiers):
    """Every decision names the memory it came from, as a trace of steps, and a check reads each
    step's source again."""

    def step(self, tier, path, start, end, asked="What does memory say?", found="It says so."):
        text = self.ask("read", {"issue": 7, "tier": tier, "path": path, "start": start, "end": end})["text"]
        return {"asked": asked, "found": found,
                "source": {"tier": tier, "path": path, "start": start, "end": end, "fingerprint": cc.fingerprint(text)}}

    def cite(self, trace, **extra):
        return self.ask("cite", {"issue": 7, "question": "How long does a reset link last?",
                                 "answer": "One hour.", "decided_by": "test agent", "play": "/vision",
                                 "trace": trace} | extra)

    def test_a_decision_is_recorded_and_checked(self):
        a = self.cite([self.step("phoenix", "knowledge/domains/user-management.md", 5, 5)])
        self.assertEqual(a["stored"], {"tier": "short-term", "path": "7/context/citations.jsonl"})
        listed = self.ask("citations", {"issue": 7, "check": True})
        self.assertEqual(([r["citation_id"] for r in listed["records"]], listed["problems"]), ([a["citation_id"]], []))

    def test_nothing_is_recorded_from_a_wrong_or_missing_source(self):
        bad = self.step("phoenix", "knowledge/domains/user-management.md", 5, 5)
        bad["source"]["fingerprint"] = cc.fingerprint("x")
        self.assertEqual(self.cite([bad])["error"]["code"], "changed")
        gone = {"asked": "q", "found": "f", "source": {"tier": "phoenix", "path": "knowledge/none.md", "start": 1,
                                                       "end": 1, "fingerprint": cc.fingerprint("x")}}
        self.assertEqual(self.cite([self.step("phoenix", "standards/rules/commits.md", 1, 1), gone])["error"]["code"],
                         "not_found")
        self.assertEqual(self.ask("citations", {"issue": 7})["records"], [])

    def test_the_check_names_the_step_whose_source_changed_or_went(self):
        self.cite([self.step("phoenix", "standards/rules/commits.md", 1, 1),
                   self.step("phoenix", "knowledge/domains/user-management.md", 5, 5)])
        self.cite([self.step("phoenix", "standards/rules/commits.md", 2, 2)])
        write(self.phoenix, "knowledge/domains/user-management.md", "# User management\n\n\n\n- Links last 30 minutes.\n")
        git(self.phoenix, "rm", "-q", "standards/rules/commits.md")
        self.commit("memory moved on")
        problems = self.ask("citations", {"issue": 7, "check": True})["problems"]
        self.assertEqual(sorted((p["problem"], p["step"]) for p in problems),
                         [("source_changed", 2), ("source_missing", 1), ("source_missing", 1)])
        changed = next(p for p in problems if p["problem"] == "source_changed")
        self.assertEqual((changed["source"]["text"], changed["now"]),
                         ("- A reset link expires after one hour.", "- Links last 30 minutes."))
        self.assertEqual(changed["now_around"], {"start": 2, "end": 5, "text": "\n\n\n- Links last 30 minutes."})
        missing = next(p for p in problems if p["problem"] == "source_missing")
        self.assertEqual((missing["now"], missing["now_around"]), (None, None))

    def test_the_record_keeps_each_step_with_what_the_agent_read_in_its_place(self):
        self.cite([self.step("phoenix", "standards/rules/commits.md", 2, 2, asked="What is the subject limit?",
                             found="72 characters."),
                   self.step("phoenix", "knowledge/domains/user-management.md", 5, 5)])
        trace = self.ask("citations", {"issue": 7})["records"][0]["trace"]
        self.assertEqual([(st["asked"], st["found"]) for st in trace],
                         [("What is the subject limit?", "72 characters."), ("What does memory say?", "It says so.")])
        src = trace[1]["source"]
        self.assertEqual(src["text"], "- A reset link expires after one hour.")
        self.assertEqual(src["around"], {"start": 2, "end": 5, "text": "## Sign-in\n- Lock the account after five "
                                         "failed sign-ins.\n## Passwords\n- A reset link expires after one hour."})
        self.assertEqual(trace[0]["source"]["around"], {"start": 1, "end": 2, "text": "# Commits\nSubject under 72."})
        self.assertEqual(src["version"], self.ask("health", {})["tiers"][2]["version"])

    def test_a_decision_with_no_trace_is_a_problem(self):
        os.makedirs(os.path.join(self.short, "7", "context"))
        with open(os.path.join(self.short, "7", "context", "citations.jsonl"), "w") as fh:
            fh.write(json.dumps({"citation_id": "cite-20261018-001", "issue": 7, "play": None, "question": "q",
                                 "answer": "a", "decided_by": "someone", "decided_at": "2026-10-18T00:00:00Z",
                                 "trace": [], "from_update": None}) + "\n")
        problems = self.ask("citations", {"issue": 7, "check": True})["problems"]
        self.assertEqual([(p["problem"], p["step"], p["source"]) for p in problems], [("no_source", None, None)])

    def test_a_decision_from_an_approved_update(self):
        u = self.ask("propose", {"issue": 7, "missing": "Reset link length here.", "target_tier": "short-term",
                                 "target_path": "7/context/answers/reset.md", "draft": "Thirty minutes here.",
                                 "draft_source": "person", "sources": [], "requested_by": "test agent"})["update"]
        self.assertEqual(self.cite([self.step("phoenix", "standards/rules/commits.md", 1, 1)],
                                   from_update=u["id"])["error"]["code"], "not_approved")
        self.ask("decide", {"id": u["id"], "verdict": "approve", "by": "a person", "reply": "yes",
                            "decided_in": "review-tool"})
        self.ask("apply", {"id": u["id"]})
        self.assertEqual(self.cite([self.step("phoenix", "standards/rules/commits.md", 1, 1)],
                                   from_update=u["id"])["error"]["code"], "bad_request")
        ok = self.cite([self.step("phoenix", "standards/rules/commits.md", 1, 1),
                        self.step("short-term", "7/context/answers/reset.md", 1, 1)], from_update=u["id"])
        self.assertTrue(ok["ok"])

    def test_an_unreadable_line_stops_only_its_own_issue(self):
        os.makedirs(os.path.join(self.short, "8", "context"))
        with open(os.path.join(self.short, "8", "context", "citations.jsonl"), "w") as fh:
            fh.write('{"citation_id": "cite-2026')
        self.assertTrue(self.cite([self.step("phoenix", "standards/rules/commits.md", 1, 1)])["ok"])
        broken = self.ask("citations", {"issue": 8, "check": True})["error"]
        self.assertEqual((broken["code"], broken["tier"]), ("unreadable", "short-term"))
        self.assertIn("8/context/citations.jsonl line 1", broken["message"])
        again = self.ask("cite", {"issue": 8, "question": "q", "answer": "a", "decided_by": "test agent",
                                  "trace": [self.step("phoenix", "standards/rules/commits.md", 1, 1)]})
        self.assertEqual(again["error"]["code"], "unreadable")

    def test_a_failed_write_names_short_term_memory(self):
        folder = os.path.join(self.short, "7")
        os.makedirs(folder)
        os.chmod(folder, 0o500)
        self.addCleanup(os.chmod, folder, 0o700)
        a = self.cite([self.step("phoenix", "standards/rules/commits.md", 1, 1)])
        self.assertEqual((a["error"]["code"], a["error"]["tier"]), ("tier_missing", "short-term"))
        self.assertTrue(a["error"]["message"].startswith("Short-term memory cannot be written"))

    def test_a_decision_is_not_memory(self):
        self.cite([self.step("phoenix", "knowledge/domains/user-management.md", 5, 5)],
                  answer="A remembered answer, only in the decision record.")
        self.assertEqual(self.ask("search", {"issue": 7, "pattern": "remembered answer"})["answered_by"], None)

    def test_listing_one_play(self):
        self.cite([self.step("phoenix", "standards/rules/commits.md", 1, 1)], play="/vision")
        self.cite([self.step("phoenix", "standards/rules/commits.md", 1, 1)], play="/understand")
        self.assertEqual([r["play"] for r in self.ask("citations", {"issue": 7, "play": "/understand"})["records"]],
                         ["/understand"])


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

    def test_pull_takes_the_contract_request(self):
        for argv in (["pull", "--path", "standards/rules/commits.md"],
                     ["pull", "--request", '{"path": "standards/rules/commits.md"}'],
                     ["pull", "standards/rules/commits.md"]):
            code, answers = self.main(argv)
            self.assertEqual((code, answers[0]["path"]), (0, "standards/rules/commits.md"), argv)

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
