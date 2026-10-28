'use strict';
// #778: skills are run by plays, never by a person — a skill with user-invocable: true fails.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { checkSkill } = require('../lib/rules/structural');
let passed = 0;
function t(label, got, want) { assert.deepStrictEqual(got, want, label); passed++; console.log(`  [PASS] ${label}`); }
function skill(invocable) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-'));
  const file = path.join(dir, 'SKILL.md');
  fs.writeFileSync(file, `---\nname: author-thing\ndescription: x\nuser-invocable: ${invocable}\nmodel: opus\nallowed-tools: Read\n---\n\n# author-thing\n\n## Input\nx\n## Process\nx\n## Output\nx\n`);
  return checkSkill({ file, name: 'author-thing', type: 'skill' }).map((v) => v.rule).filter((r) => r === 'structural/skill-user-invocable');
}
t('a skill a person can start fails', skill('true'), ['structural/skill-user-invocable']);
t('a skill only plays run passes', skill('false'), []);
console.log(`\n${passed} passed, 0 failed`);
