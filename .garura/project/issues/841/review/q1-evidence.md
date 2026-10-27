# Q-1 evidence: proof rules on the four tool files (#841, review round 1 of PR #858)

The scanner hits on these four files come from `path:` rules that ask for proof. This file
gives, for each rule id in `quality-findings.yaml` (BE-19 and SEC-18 are fixed in `pr.md`
and tested in `test_scan_taxonomy.py`), what was run or read and the result. The rule text
is from `core/components/skills/check-quality/reference/all-requirements.md`.

How the numbers were taken:
- Syntax: `node --check <file>` and `python3 -m py_compile <file>`.
- Lint and format: `ruff check --no-cache` and `black --check` (Python). The repository
  has no ESLint, Prettier, Black or Ruff configuration.
- Imports: every `require(` and `import` line, followed one level into the modules they load.
- Size: `wc -l`. Function length (non-blank, non-comment lines), nesting depth and branch
  count (if, for, while, case, catch, `&&`, `||`, `?`, comprehensions): a Python `ast`
  walk, and a brace-matching count for JavaScript, run from the repository root.
- Speed: `/usr/bin/time -p` on each test file.

## core/tools/lint-components/lib/rules/asking-a-person.js

- ARCH-02 (no circular dependencies): read its `require(` lines. It loads only `fs`. Holds.
- ARCH-03 (no file over 500 lines with mixed concerns): 91 lines, one concern. Holds.
- ARCH-08 (module boundary matches function): one lint rule in `lib/rules/`, beside the other rules. Holds.
- CODE-03 (linter without warnings): `node --check` passes. No ESLint config is in the repository, so no JavaScript linter can run. Not applicable: no linter is configured.
- CODE-04 (formatter zero diff): no Prettier config in the repository. Not applicable: no formatter is configured.
- CODE-09 (cyclomatic complexity ≤ 10): largest is `sections` at 7. Holds.
- CODE-10 (function length ≤ 50): largest is `sections` at 18 lines. Holds.
- CODE-11 (nesting ≤ 4): deepest brace depth is 3. Holds.
- CODE-12 (module ≤ 300 lines): 91 lines. Holds.
- CODE-13 (single responsibility): it checks one rule, `asking-a-person/missing-pointer`. Holds.
- CODE-14 (no circular dependencies): same as ARCH-02; only `fs`. Holds.
- CODE-15 (cognitive complexity ≤ 15): branch count is at most 7 and nesting at most 3, so it is below 15. Holds.
- CODE-17 (idiomatic case): functions and variables are camelCase. Holds.
- CODE-18 (PascalCase classes, file matches class): it has no class; the file is named after its rule, like the other rule files. Not applicable: no class.
- CODE-19 (SCREAMING_SNAKE_CASE constants): `RULE_ID`, `RULE_FILE`, `PARTS`, `NOT_STEPS`, `WORKFLOW`, `INSIDE_WORKFLOW`. Holds.
- CODE-22 (boolean names use is/has/can/should): searched for boolean variables. Fixed: the flag `fence` is now `inFence`.
- FE-08 (JS bundle per route < 200KB): a Node command-line lint rule, not shipped to a browser. Not applicable: no bundle.

## core/tools/lint-components/test/asking-a-person.test.js

- ARCH-02 (no circular dependencies): loads `assert`, `fs`, `os`, `path`, `child_process` and the rule. The rule loads only `fs`. Holds.
- ARCH-03 (≤ 500 lines): 93 lines. Holds.
- ARCH-08 (boundaries): in `test/`, beside the other lint tests. Holds.
- CODE-03 (linter): `node --check` passes; no ESLint config in the repository. Not applicable: no linter is configured.
- CODE-04 (formatter): no Prettier config in the repository. Not applicable: no formatter is configured.
- CODE-09 (complexity ≤ 10): largest is `part` at 6. Holds.
- CODE-10 (function length ≤ 50): largest is `part` at 11 lines. Holds.
- CODE-11 (nesting ≤ 4): deepest brace depth is 3. Holds.
- CODE-12 (module ≤ 300 lines): 93 lines. Holds.
- CODE-13 (single responsibility): it tests one rule. Holds.
- CODE-14 (no cycles): same as ARCH-02. Holds.
- CODE-15 (cognitive complexity ≤ 15): branch count at most 6. Holds.
- CODE-17 (idiomatic case): camelCase functions and variables. Holds.
- CODE-18 (PascalCase classes): no class. Not applicable: no class.
- CODE-19 (constants): `ASKS`, `POINTER`, `OLD_POINTER`, `SILENT`, `RULE_ID`. Holds.
- CODE-22 (boolean names): searched; no boolean variable. Holds.
- FE-08 (bundle size): a Node test, not shipped to a browser. Not applicable: no bundle.
- TEST-02 (Arrange-Act-Assert): each case builds a part (arrange), runs the rule (act), and asserts with `t` (assert). Holds.
- TEST-03 (one behavior per test): each `t` call makes one `assert.deepStrictEqual`. Holds.
- TEST-05 (names describe behavior): each label says what passes or fails, for example "the old memory path does not count". Holds.
- TEST-06 (no shared mutable state): each case writes into its own new temporary folder. Fixed: the test now removes every temporary folder it made when it ends; before, they were left behind.
- TEST-07 (suite < 30 s): `node` run, 23 checks, 0.21 s. Holds.
- TEST-08 (assertion library): uses Node's `assert.deepStrictEqual`. Holds.
- TEST-22 (unit > integration > E2E): 19 unit cases call the rule directly, and 4 integration cases run the linter with `--target`. Holds.

## core/tools/lint-components/test/naming.test.js

- ARCH-02 (no circular dependencies): loads `assert` and `lib/rules/naming`. That rule loads `fs`, `path` and `js-yaml`, and none of them loads the test. Holds.
- ARCH-03 (≤ 500 lines): 31 lines. Holds.
- ARCH-08 (boundaries): in `test/`, beside the other lint tests. Holds.
- CODE-03 (linter): `node --check` passes; no ESLint config in the repository. Not applicable: no linter is configured.
- CODE-04 (formatter): no Prettier config in the repository. Not applicable: no formatter is configured.
- CODE-09 (complexity ≤ 10): two one-line helpers, `t` and `rules`, at 1. Holds.
- CODE-10 (function length ≤ 50): `t` and `rules` are 1 line each. Holds.
- CODE-11 (nesting ≤ 4): depth 2. Holds.
- CODE-12 (module ≤ 300 lines): 31 lines. Holds.
- CODE-13 (single responsibility): it tests the naming rule only. Holds.
- CODE-14 (no cycles): same as ARCH-02. Holds.
- CODE-15 (cognitive complexity ≤ 15): branch count 1. Holds.
- CODE-17 (idiomatic case): camelCase. Holds.
- CODE-18 (PascalCase classes): no class. Not applicable: no class.
- CODE-19 (constants): the fixture standard object was named `std`. Fixed: it is now `STANDARD`.
- FE-08 (bundle size): a Node test. Not applicable: no bundle.
- TEST-02 (Arrange-Act-Assert): each line gives a name (arrange), runs `checkName` (act), and asserts the rule ids (assert). Holds.
- TEST-03 (one behavior per test): one `assert.deepStrictEqual` for each `t`. Holds.
- TEST-05 (names describe behavior): for example "a skill with no skill verb fails". Holds.
- TEST-06 (no shared state): pure calls on fixed inputs; no files and no shared state. Holds.
- TEST-07 (suite < 30 s): 16 checks, 0.03 s. Holds.
- TEST-08 (assertion library): Node's `assert`. Holds.
- TEST-22 (pyramid): all 16 cases are unit tests of one function. Holds.

## core/tools/naming/test_naming_tools.py

- ARCH-02 (no circular dependencies): imports `apply_renames` and `check_old_names`. `apply_renames` imports `check_old_names`; `check_old_names` imports only the standard library and `yaml`. No cycle. Holds.
- ARCH-03 (≤ 500 lines): 141 lines. Holds.
- ARCH-08 (boundaries): beside the two tools it tests, in `core/tools/naming/`. Holds.
- CODE-03 (linter without warnings): `ruff check --no-cache` prints "All checks passed!". Holds.
- CODE-04 (formatter zero diff): `black --check` reports a diff. The repository sets no formatter: black's defaults (88 columns, its docstring rules) also fail the two tools this test sits beside (`check_old_names.py`, `apply_renames.py`). Reformatting one file to black alone would make it differ from its neighbours. Not applicable: no formatter is configured; lines are kept at 120 columns or less, like the rest of `core/tools`.
- CODE-09 (cyclomatic complexity ≤ 10): `main` was 16 (one 64-line function). Fixed: split into `seed_repo`, `check_before`, `check_after` and `main`. Now at most 6.
- CODE-10 (function length ≤ 50): `main` was 64 lines. Fixed by the same split. Now at most 19 lines (`check_after`).
- CODE-11 (nesting ≤ 4): depth at most 1. Holds.
- CODE-12 (module ≤ 300 lines): 141 lines. Holds.
- CODE-13 (single responsibility): it tests the old-name check and the rename tool on one scratch repository. Holds.
- CODE-14 (no cycles): same as ARCH-02. Holds.
- CODE-15 (cognitive complexity ≤ 15): after the split, at most 6 branches with nesting 1. Holds.
- CODE-17 (idiomatic case): snake_case functions and variables. Holds. Also changed: files are now opened with `with`, through the new `read` and `write` helpers.
- CODE-19 (constants): `RENAME_MAP`, `SEED`, `KINDS`, `ADR_TEXT`, `HERE`, and the counters `PASSED`/`FAILED`. Holds.
- BE-19 (raw SQL): the hits were the word "from" in `from ... import` and in text; no SQL is in the file. The rule is now narrowed in `pr.md` and gives no finding here. Holds.

## Run after the fixes

- `node core/tools/lint-components/test/asking-a-person.test.js`: 23 passed, 0 failed.
- `node core/tools/lint-components/test/naming.test.js`: 16 passed, 0 failed.
- `python3 core/tools/naming/test_naming_tools.py`: 23 passed, 0 failed.
