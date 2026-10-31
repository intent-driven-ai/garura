# Code evidence for the path-only rows (PR #998, round 2 → 3)

The severity taxonomy's path-only rows fire on every changed code file and ask for evidence. This
is that evidence, for `core/tools/plan/plan_branch.py`, `core/tools/plan/test_plan_branch.py` and
`core/tools/lint-components/index.js`.

| Row | Asks for | Evidence |
|-----|----------|----------|
| CODE-03 (lint) | a lint message | `ruff check` on every changed non-test Python file: "All checks passed!" (`runnable-checks.txt`). No eslint is installed; `node --check core/tools/lint-components/index.js` passes. |
| CODE-04 (format) | a format diff | The repository commits no formatter configuration. The files beside these follow the same hand style and are not in ruff's default format either (`ruff format --check` reports `core/tools/plan/plan.py`, `core/components/skills/link-model-part/scripts/link_part.py`, `core/components/plays/shape-plan/scripts/write_plan_file.py`). The new code matches its neighbours; reformatting only the new files would split the style of one folder. |
| ARCH-02, CODE-14 (cycles) | a cycle trace | `plan_branch.py` imports only the standard library and `yaml`; `test_plan_branch.py` imports the standard library and `plan_branch`; `index.js` requires its own `lib/` modules and Node's `fs` and `path`, as before this change. No import cycle. |

False positives, kept as findings and named here with their reason:

| Row | Where | Why it does not apply |
|-----|-------|-----------------------|
| BE-12 (HTTP timeout) | `plan_branch.py`, `git fetch` | `fetch` is the git command, not an HTTP call. |
| DATA-17 (P2), DATA-18 (P1) | `test_plan_branch.py`, `user.email` | the throwaway git identity of a test repository made in a temporary folder; no personal data is stored. The rule matches the bare word "email" in any code file. |
