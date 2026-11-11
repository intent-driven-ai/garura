**Reviewer verdict (human): approve**

The product owner approved this change after the review below. The computed recommendation was reject on one finding, and the reviewer approved over it.

**Overridden blocker**
- TEST-RED-1 (P1, tests): `reshape-plan/scripts/test_feature_ice.py` is red ("feature fn-818 has no ICE"). It is red the same way on main before this change. The change only renamed its folder from update-plan.

**Not blocking**
- P3, harness: plain loop names are left over ("the Discovery loop", "Execute / Learn loop") in the loop's page, four plays' scenario lines and pipeline-next.md. ADR 066 §3 says these names go.
- P3, harness: line 4 of `loop-product-spec/SKILL.md` says "product to intent". Its ICE says "product → spec" (ADR 066 §8).
- P3, harness: Phoenix memory's Next-line map still names the plays by their old names. After a reinstall, each renamed play's Next line finds no entry until that map is promoted (#966).
- P3, memory: pipeline-next.md and spine.yaml keep the plain loop names.
- P4: eight further notes, covering the installed linters that predate the rename, internal identifiers, the old fingerprint drift on list-issues, the ADR index behaviour, the one-pass ICE wording, the rename map's dropped lens plays, the naming.md examples and the edit to ADR 066 line 149.

**Checks run**
- Old-name check: 0 left.
- Branch linter: no naming error.
- Test suites: 92 of 93 pass.
- Acceptance check: 82 of 82 pass.
- Every play key in core/config.yaml names a real play.

The full findings are in `.garura/project/issues/1044/review/findings.yaml`.
