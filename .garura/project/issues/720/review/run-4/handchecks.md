# Round 4 — the checks the playbooks do by hand

Each check names what was read and what it showed. The commands' outputs are in
`adr-lint.txt`, `lint-play.txt`, `lint-components.json` and `runnable-checks.txt`.

## Decision records (review/adrs)

- ADR 061 and ADR 062 pass the ADR lint (`adr.py lint --adr`, valid, no problems); so do ADR 058
  and ADR 060, which gained pointers. ADR 026 fails the lint on seven header and section lines,
  exactly as it does at the base (`git show plan/717/base:docs/adr/026-…` gives the same seven):
  it predates the template; this change adds only its forward pointer. There before.
- Numbering: 061 and 062 follow 060 with no gap; `docs/adr/_index.md` has one row for each.
- The index has 62 rows for 62 files (60 numbered files and the two `SUPERSEDED-` files); no
  row without a file, no file without a row.
- Pointers: ADR 026 and ADR 058 name ADR 062 on their Status lines; ADR 060 names ADR 061.

## Memory (review/memory)

- `standards/templates/_index.md` line 21 lists `plan-update.md`.
- `standards/rules/pipeline-next.md` line 77 has the `update-plan` row (command null, with why),
  and the play linter's next-command check passes for update-plan, shape-slice and shape-plan.
- `plan-update.md` opens with its title and consumer line and holds one `yaml plan-update`
  settings block; the play's 37 tests read every screen from it (`render_screen.py`).
- `direct-model-write.md` holds the third declared exception and the L-DMW-4 note;
  `spine.yaml` parses (yaml.safe_load) after its comment change.

## Docs (review/docs)

- `core/tools/plan/README.md` lines 50–52: the commands `go`, `back` and `abort` and their flags
  (`--plan`, `--plans-dir`, `--ignore`, `--out`, `--record`) all exist in
  `plan_branch.py --help`; the optional `--repo`, `--remote` and `--main` are not listed, which
  the README's bracketed form allows.
- `core/grounding/glossary.md`: the Feature row and the new Feature item row agree with
  ontology v14 (Plan, item kinds).

## Config maps (review/config-maps)

- `install.py` lines 263 and 285: the harness allow-list holds `update-plan`,
  `author-plan-changes` and `track-plan-changes`; each resolves to a folder under
  `core/components` (plays/update-plan, skills/author-plan-changes, skills/track-plan-changes).
  The install suite (75 tests) is in `runnable-checks.txt`.
