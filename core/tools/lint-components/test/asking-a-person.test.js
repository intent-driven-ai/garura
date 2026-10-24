'use strict';
// #821, #854: the five parts that ask a person must point to _shared/asking-a-person.md.
// No other part is ever an error under this rule.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const { checkPart, check, RULE_ID } = require('../lib/rules/asking-a-person');
let passed = 0;
function t(label, got, want) { assert.deepStrictEqual(got, want, label); passed++; console.log(`  [PASS] ${label}`); }

const ASKS = '**Step 2 — Checkpoint 1** · Owner: play · Checkpoint (class: standard)\n' +
  'Show the draft, and ask the product owner to type **yes**, or **change: <what>**.\n';
const POINTER = 'Every draft shown follows `_shared/asking-a-person.md`.\n';
const OLD_POINTER = 'Every draft shown follows `standards/rules/asking-a-person.md`.\n';
const SILENT = '**Step 1 — Count the files** · Owner: play (script)\nRun the script; no one is asked.\n';

function part(kind, name, body, opts = {}) {
  const dir = opts.dir || fs.mkdtempSync(path.join(os.tmpdir(), 'asking-'));
  const folder = kind === 'play' ? 'plays' : 'skills';
  fs.mkdirSync(path.join(dir, folder, name), { recursive: true });
  const file = path.join(dir, folder, name, 'SKILL.md');
  const before = opts.before || '';
  const after = opts.after || '';
  fs.writeFileSync(file, `---\nname: ${name}\ndescription: ${opts.description || 'x'}\n---\n\n# ${name}\n\n` +
    `${before}## Workflow\n${body}${after}`);
  return { dir, file };
}
function rules(body, opts = {}) {
  const kind = opts.kind || 'play';
  const name = opts.name || 'shape-slice';
  const { file } = part(kind, name, body, opts);
  return check({ [kind === 'play' ? 'plays' : 'skills']: [{ file, name, type: kind }] }).map((v) => v.rule);
}

// The five named parts.
t('shape-slice with no pointer fails', rules(ASKS), [RULE_ID]);
t('shape-slice with the pointer passes', rules(ASKS + POINTER), []);
t('edit-ontology with no pointer fails', rules(ASKS, { name: 'edit-ontology' }), [RULE_ID]);
t('a named play fails even when no step signal is found', rules(SILENT), [RULE_ID]);
t('the old memory path does not count', rules(ASKS + OLD_POINTER), [RULE_ID]);
for (const name of ['author-product-ontology', 'find-slice-gaps', 'author-slice-brief']) {
  t(`skill ${name} with no pointer fails`, rules(SILENT, { kind: 'skill', name }), [RULE_ID]);
  t(`skill ${name} with the pointer passes`, rules(SILENT + POINTER, { kind: 'skill', name }), []);
}

// Any other part is never an error.
t('another play that asks and has no pointer passes', rules(ASKS, { name: 'shape-thing' }), []);
t('another skill with no pointer passes', rules(ASKS, { kind: 'skill', name: 'author-thing' }), []);
t('a skill named like a checked play passes', rules(ASKS, { kind: 'skill', name: 'shape-slice' }), []);

// Where the pointer counts in a play: inside the workflow, never before it or in notes.
t('pointer only under References fails',
  rules(SILENT + ASKS, { after: '\n## References\n- ' + POINTER }), [RULE_ID]);
t('pointer only in Pre-flight fails',
  rules(ASKS, { before: '## Pre-flight\n' + POINTER + '\n' }), [RULE_ID]);
t('pointer only in the frontmatter fails',
  rules(ASKS, { description: 'Follows _shared/asking-a-person.md.' }), [RULE_ID]);
t('pointer in a Phase inside the workflow passes',
  rules('\n### Phase: Draft\n' + POINTER + ASKS, { before: '## Pre-flight\nNothing here.\n' }), []);
t('a part with no Workflow section that names the rule in its body passes',
  (() => { const { file } = part('skill', 'find-slice-gaps', '');
    fs.writeFileSync(file, '---\nname: find-slice-gaps\ndescription: x\n---\n\n## Steps\n' + POINTER);
    return checkPart({ file, name: 'find-slice-gaps', type: 'skill' }).map((v) => v.rule); })(), []);

// Through the linter itself, with --target on any folder that holds the parts.
function lint(build) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'asking-'));
  build(dir);
  let out;
  try {
    out = execFileSync('node', [path.join(__dirname, '..', 'index.js'), '--target', dir], { encoding: 'utf8' });
  } catch (e) { out = e.stdout; }
  return JSON.parse(out).violations.filter((v) => v.rule === RULE_ID).length;
}
t('the linter names the named play with no pointer (--target)',
  lint((dir) => part('play', 'shape-slice', ASKS, { dir })), 1);
t('the linter passes the named play with the pointer (--target)',
  lint((dir) => part('play', 'shape-slice', ASKS + POINTER, { dir })), 0);
t('the linter passes another play with no pointer (--target)',
  lint((dir) => part('play', 'shape-thing', ASKS, { dir })), 0);
t('the linter names the named skill with no pointer (--target)',
  lint((dir) => part('skill', 'author-slice-brief', SILENT, { dir })), 1);

console.log(`\n${passed} passed, 0 failed`);
