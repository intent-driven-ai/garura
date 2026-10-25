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
// #860: every copy of lint_play.py matches the tool's copy (core/tools/lint-play/lint_play.py).
function toolTarget(copyText, { layout = 'source', withTool = true, home = 'plays/create-play' } = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'tool-'));
  const comps = path.join(root, layout === 'source' ? 'components' : '.claude');
  const toolDir = layout === 'source' ? path.join(root, 'tools', 'lint-play') : path.join(root, '.garura', 'core', 'tools', 'lint-play');
  if (withTool) {
    fs.mkdirSync(toolDir, { recursive: true });
    fs.writeFileSync(path.join(toolDir, 'lint_play.py'), 'print("tool")\n');
  }
  fs.mkdirSync(path.join(comps, home, 'scripts'), { recursive: true });
  fs.writeFileSync(path.join(comps, home, 'scripts', 'lint_play.py'), copyText);
  return check(comps).map((v) => v.rule);
}
t('a lint_play.py copy that matches the tool passes', toolTarget('print("tool")\n'), []);
t('a lint_play.py copy that differs from the tool fails', toolTarget('print("drifted")\n'), ['structural/lint_play-drift']);
t('an edit-play copy that differs fails too', toolTarget('x\n', { home: 'plays/edit-play' }), ['structural/lint_play-drift']);
t('installed layout: a copy that differs from the installed tool fails',
  toolTarget('x\n', { layout: 'installed', home: 'skills/create-play' }), ['structural/lint_play-drift']);
t('installed layout: a copy that matches the installed tool passes',
  toolTarget('print("tool")\n', { layout: 'installed', home: 'skills/edit-play' }), []);
t('with no tool the check is skipped', toolTarget('x\n', { withTool: false }), []);
console.log(`\n${passed} passed, 0 failed`);
