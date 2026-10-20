# #613 item 8 — Kickoff on a real prototype: findings (as they come)

Test project `argus-shop`: Garura installed from `feature/613-the-kickoff-drive` (full scope),
pushed to the private sandbox repo `intent-driven-ai/test-sandbox` (Kapil, 2026-10-20: one
sandbox repo for all tests). Prototype: the Argus mockup, copied in as `prototype/argus.html`.
Phoenix memory on the machine at `7d4d49d`. Kickoff run headless (`claude -p "/kickoff …"`),
its plays as sub-agents (the default runner).

## Before the run

- K-0 — the install writes the absolute shared-memory path into the project's committed
  `.garura/install-manifest.json` (`"memory": "/…/argus-shared-memory"`). Any project that
  commits its install record commits that path — with the default, the user's home folder. It
  reached the sandbox repo's first push; the sandbox history was rewritten and force-pushed
  clean (3 commits, minutes old). For its own issue.
- K-1 — this branch changes two Phoenix memory files (`standards/rules/drive-contract.md`,
  `standards/rules/pipeline-next.md`); Phoenix memory on the machine has the older copies until
  #613 lands, so the run reads the old drive contract and has no Next line for `kickoff`.

## Run 1 (2026-10-20) — stopped at /intent's questions, then stopped by Kapil

- K-2 — Python leaves `__pycache__/` beside the stamped scripts in the installed
  `.claude/skills/kickoff/scripts/`; it is outside the issue folder, so `commit_run_files.py`
  would call the tree unclean and halt the drive after the first play. To watch on the rerun.
- K-3 — **`/intent` read one screen of the Argus mockup.** The capture kept only the first,
  Overview screen (4.7 KB of text) of a prototype with five sections, Catch up and its cards;
  the play clicks a view only when one is named, and nothing named them. `/intent` drafted two
  business intents that were rules about agents ("agents build only from what a person
  approved") — Kapil: "completely wrong … none of it reflects what Argus does". **Fixed on this
  branch** (Kapil, "1"): C1, F1, REC1 and S1 of `/intent`'s ICE now require a prototype to be
  captured view by view; `capture_source.py` finds every view itself (two clicks deep, never an
  answer button or an outside link) and records what it found, kept and could not reach. On the
  mockup: 36 views kept (about 99 KB of text), 4 unreached with why.
- K-4 — the business intents were drawn from rules written in the page, not the person's
  purpose, and the mockup's sample shop data confused it (its Q1). Held: the rerun shows whether
  this remains once `/intent` sees every view.
