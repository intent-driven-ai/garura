'use strict';
// Decision 21 of #860: an agent that uses the memory tool points to _shared/memory-reading.md
// and carries no pasted protocol. Checked in the source and the installed layout.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const { check, checkText, MISSING, PASTED } = require('../lib/rules/memory-reading');
const discover = require('../lib/discover');

let passed = 0;
function t(label, got, want) { assert.deepStrictEqual(got, want, label); passed++; console.log(`  [PASS] ${label}`); }
function rules(text) { return checkText('a.md', text, 'a').map((v) => `${v.rule}:${v.line}`); }

const FM = '---\nname: thing-keeper\ndescription: x\n---\n';
const POINTS = 'Read memory only as the shared protocol says: `.claude/skills/_shared/memory-reading.md`.\n';
const PASTED_STEPS = '## Memory Reading Protocol\n\nYou read memory only through the memory tool.\n\n' +
  '1. **Find** what the task needs:\n\n   ```\n   python3 .garura/core/tools/memory/memory.py find --glob "x"\n   ```\n' +
  '2. **Copy** each file.\n\n## Input Contract\n';
const ONE_LINER = "   | python3 -c 'import json,os,sys; a=json.load(sys.stdin); open(sys.argv[1], \"w\").write(a[\"text\"])' x\n";

t('an agent that names the memory tool and points to the shared file passes',
  rules(`${FM}## Memory Reading Protocol\n\n${POINTS}\n| Skill | What |\n`), []);
t('an agent that never names the memory tool passes', rules(`${FM}Writes code.\n`), []);
t('an agent that calls memory.py with no pointer fails',
  rules(`${FM}Run \`python3 .garura/core/tools/memory/memory.py find\`.\n`), [`${MISSING}:1`]);
t('an agent that says "the memory tool" with no pointer fails',
  rules(`${FM}Reach memory only through the Memory tool.\n`), [`${MISSING}:1`]);
t('the pasted steps under the heading fail, even with the pointer',
  rules(`${FM}${POINTS}${PASTED_STEPS}`), [`${PASTED}:10`]);
t('numbered Find steps under another heading are not the protocol',
  rules(`${FM}${POINTS}## Steps\n1. **Find** the file.\n`), []);
t('a heading inside a code fence does not open the protocol',
  rules(`${FM}${POINTS}\`\`\`\n## Memory Reading Protocol\n\`\`\`\n1. **Find** the file.\n`), []);
t('the inline copy command fails, wherever it is',
  rules(`${FM}${POINTS}## Notes\n${ONE_LINER}`), [`${PASTED}:7`]);
t('both rules are errors',
  [...new Set(checkText('a.md', `${FM}memory tool\n${PASTED_STEPS}${ONE_LINER}`, 'a').map((v) => v.severity))], ['error']);

// --- both layouts, through discover and the command line --------------------
function write(root, rel, text) {
  const full = path.join(root, rel);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, text);
}
const src = fs.mkdtempSync(path.join(os.tmpdir(), 'mr-src-'));
write(src, 'agents/good-keeper.md', `${FM}${POINTS}Use the memory tool.\n`);
write(src, 'agents/old-keeper.md', `${FM}${PASTED_STEPS}`);
write(src, 'agents/_shared/memory-reading.md', `# Memory Reading Protocol\n${PASTED_STEPS}`);
const names = (dir, layout) => check(discover(dir, layout)).map((v) => `${path.basename(v.file)}:${v.rule}`).sort();
t('source layout: the agent with the pasted protocol fails twice; the shared file is not an agent',
  names(src, 'source'), [`old-keeper.md:${MISSING}`, `old-keeper.md:${PASTED}`]);

const proj = fs.mkdtempSync(path.join(os.tmpdir(), 'mr-inst-'));
const claude = path.join(proj, '.claude');
write(claude, 'agents/good-keeper.md', `${FM}${POINTS}Use the memory tool.\n`);
write(claude, 'agents/old-keeper.md', `${FM}Use memory.py.\n${ONE_LINER}`);
write(claude, 'skills/_shared/memory-reading.md', '# Memory Reading Protocol\n');
t('installed layout: the agent with no pointer and the copy command fails',
  names(claude, 'installed'), [`old-keeper.md:${MISSING}`, `old-keeper.md:${PASTED}`]);

const index = path.join(__dirname, '..', 'index.js');
let out;
try {
  out = JSON.parse(execFileSync('node', [index, '--layout', 'installed', '--target', claude], { encoding: 'utf8' }));
} catch (err) {
  out = JSON.parse(err.stdout);
}
t('the command line reports the rule',
  out.violations.filter((v) => v.rule.startsWith('memory-reading/')).map((v) => v.rule).sort(), [MISSING, PASTED]);

console.log(`\n${passed} passed, 0 failed`);
