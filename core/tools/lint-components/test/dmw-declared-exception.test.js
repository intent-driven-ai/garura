'use strict';
// ADR 062: /update-plan is a declared exception to L-DMW-4 (no product-os-only clean check, no
// separate feat(model) commit); every other model-writing play still needs both.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { checkDmwAnchors } = require('../lib/rules/structural');
let passed = 0;
function t(label, got, want) { assert.deepStrictEqual(got, want, label); passed++; console.log(`  [PASS] ${label}`); }
function rules(playName, body) {
  const dir = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'dmw-')), playName);
  fs.mkdirSync(path.join(dir, 'scripts'), { recursive: true });
  fs.writeFileSync(path.join(dir, 'scripts', 'scoped_write_guard.py'), '# guard\n');
  const file = path.join(dir, 'SKILL.md');
  fs.writeFileSync(file, body);
  return checkDmwAnchors({ file, name: playName, type: 'play' }, body).map((v) => v.rule).sort();
}
const plain = '# a play\n\nRuns the guard: scripts/scoped_write_guard.py --restore.\n';
t('another model-writing play with neither still fails L-DMW-4 twice',
  rules('shape-thing', plain).filter((r) => r.startsWith('structural/dmw-no-')),
  ['structural/dmw-no-clean-tree-assert', 'structural/dmw-no-model-commit']);
t('/update-plan, a declared exception, is not an L-DMW-4 finding',
  rules('update-plan', plain).filter((r) => r.startsWith('structural/dmw-no-')), []);
t('the exception covers L-DMW-4 only: a residual draft path still fails on /update-plan',
  rules('update-plan', plain + 'writes draft/product-os first\n').includes('structural/dmw-residual-draft'), true);
console.log(`\n${passed} passed, 0 failed`);
