# Trial — /adr on ADR 031 as if new (2026-10-15)

Kapil's test: run it on ADR 031 as if it were new; it passes if it finds ADR 026, 027 and 029
on its own and sees that ADR 031 changes the Business Intent kind but no person's business intent.

Setup (scratch folder, outside the repo): the ADR folder as it was before PR #631 merged
(`git archive acc876fc^1 docs/adr`, 30 files, no ADR 031); a brief written from ADR 031's
decision with **no ADR numbers in it** (`brief.md`). The agent ran as a general agent given
`adr-keeper.md` as is — a newly added agent does not load mid-session.

Result — passed:
- **Amends:** 026 (/intent run by hand confirms before it writes), 027 (the IDSD row: a business
  intent sits above ICE), 029 (§6, Kickoff's /intent and /vision; §2's no-stop rule applied to
  /intent) — exactly the three, each with its part. Supersedes: none.
- **Not affected:** 028, 030, 002, 003, 022, 023, 019, 020, 025 — each with a reason.
- **Business intent check:** `kind` — the guard agreed (exit 0).
- **Draft:** lint clean; number 031.
- **Apply, drive mode:** saved as proposed; no older ADR changed; pointers deferred.
- **Accept later** (by "SIMULATED — trial, not Kapil", scratch copy only): pointers written on
  026, 027 and 029 — only their Status lines changed; the index lists 031 as Accepted.

Found and fixed: a Status line ending in a full stop was joined as ".; and amended" — the
pointer now drops the trailing full stop (test added).
