'use strict';
// #821, #813: every play's and skill's copy of a shared script (lint_grounding.py, model_names.py)
// must match the main copy in create-play/references.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { check } = require('../lib/rules/shared-scripts');
let passed = 0;
function t(label, got, want) { assert.deepStrictEqual(got, want, label); passed++; console.log(`  [PASS] ${label}`); }
function target(copyText, withMain = true, script = 'lint_grounding.py', home = 'plays/shape-thing') {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'shared-'));
  if (withMain) {
    fs.mkdirSync(path.join(dir, 'plays', 'create-play', 'references'), { recursive: true });
    fs.writeFileSync(path.join(dir, 'plays', 'create-play', 'references', script), 'print("main")\n');
  }
  fs.mkdirSync(path.join(dir, home, 'scripts'), { recursive: true });
  fs.writeFileSync(path.join(dir, home, 'scripts', script), copyText);
  return check(dir).map((v) => v.rule);
}
t('a copy that matches the main copy passes', target('print("main")\n'), []);
t('a copy that differs from the main copy fails', target('print("drifted")\n'), ['structural/lint_grounding-drift']);
t('with no main copy the check is skipped', target('print("drifted")\n', false), []);
t('a play copy of model_names.py that matches passes', target('print("main")\n', true, 'model_names.py'), []);
t('a play copy of model_names.py that differs fails', target('x\n', true, 'model_names.py'), ['structural/model_names-drift']);
t('a skill copy that matches passes', target('print("main")\n', true, 'model_names.py', 'skills/find-thing'), []);
t('a skill copy that differs fails', target('x\n', true, 'model_names.py', 'skills/find-thing'), ['structural/model_names-drift']);
console.log(`\n${passed} passed, 0 failed`);
