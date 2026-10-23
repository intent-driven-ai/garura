'use strict';
// #821: every play's copy of lint_grounding.py must match the main copy in create-play/references.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { check } = require('../lib/rules/shared-scripts');
let passed = 0;
function t(label, got, want) { assert.deepStrictEqual(got, want, label); passed++; console.log(`  [PASS] ${label}`); }
function target(copyText, withMain = true) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'shared-'));
  if (withMain) {
    fs.mkdirSync(path.join(dir, 'plays', 'create-play', 'references'), { recursive: true });
    fs.writeFileSync(path.join(dir, 'plays', 'create-play', 'references', 'lint_grounding.py'), 'print("main")\n');
  }
  fs.mkdirSync(path.join(dir, 'plays', 'shape-thing', 'scripts'), { recursive: true });
  fs.writeFileSync(path.join(dir, 'plays', 'shape-thing', 'scripts', 'lint_grounding.py'), copyText);
  return check(dir).map((v) => v.rule);
}
t('a copy that matches the main copy passes', target('print("main")\n'), []);
t('a copy that differs from the main copy fails', target('print("drifted")\n'), ['structural/lint_grounding-drift']);
t('with no main copy the check is skipped', target('print("drifted")\n', false), []);
console.log(`\n${passed} passed, 0 failed`);
