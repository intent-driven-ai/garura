'use strict';
// #821: a play that asks a person a question must point to asking-a-person.md.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const { checkPlay, RULE_ID } = require('../lib/rules/asking-a-person');
let passed = 0;
function t(label, got, want) { assert.deepStrictEqual(got, want, label); passed++; console.log(`  [PASS] ${label}`); }

const ASKS = '**Step 2 — Checkpoint 1** · Owner: play · Checkpoint (class: standard)\n' +
  'Show the draft, and ask the product owner to type **yes**, or **change: <what>**.\n';
const POINTER = 'Every draft shown follows `standards/rules/asking-a-person.md`.\n';
const SILENT = '**Step 1 — Count the files** · Owner: play (script)\nRun the script; no one is asked.\n';

function play(body) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'asking-'));
  fs.mkdirSync(path.join(dir, 'plays', 'shape-thing'), { recursive: true });
  const file = path.join(dir, 'plays', 'shape-thing', 'SKILL.md');
  fs.writeFileSync(file, `---\nname: shape-thing\ndescription: x\n---\n\n# shape-thing\n\n## Workflow\n${body}`);
  return { dir, file };
}
function rules(body) {
  const { file } = play(body);
  return checkPlay({ file, name: 'shape-thing', type: 'play' }).map((v) => v.rule);
}

t('a play that asks a person and has no pointer fails', rules(ASKS), [RULE_ID]);
t('a play that asks a person and points to the rule passes', rules(ASKS + POINTER), []);
t('a play that asks no one passes', rules(SILENT), []);
t('a play that waits for a typed reply and has no pointer fails',
  rules('Show the summary and wait for the typed approval.\n'), [RULE_ID]);

// Through the linter itself, with --target on any folder that holds plays/<name>/SKILL.md.
function lint(body) {
  const { dir } = play(body);
  let out;
  try {
    out = execFileSync('node', [path.join(__dirname, '..', 'index.js'), '--target', dir], { encoding: 'utf8' });
  } catch (e) { out = e.stdout; }
  return JSON.parse(out).violations.filter((v) => v.rule === RULE_ID).length;
}
t('the linter names the play with no pointer (--target)', lint(ASKS), 1);
t('the linter passes the play with the pointer (--target)', lint(ASKS + POINTER), 0);

console.log(`\n${passed} passed, 0 failed`);
