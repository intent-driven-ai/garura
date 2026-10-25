'use strict';
// #860: an installed part names no path in Garura's source and no memory folder
// (installed-paths/source-path), in the source layout and in the installed layout; and the
// installed layout finds plays, loops, skills and agents in .claude.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const { check, docsPointer, RULE_ID } = require('../lib/rules/installed-paths');
const discover = require('../lib/discover');

let passed = 0;
function t(label, got, want) { assert.deepStrictEqual(got, want, label); passed++; console.log(`  [PASS] ${label}`); }

function write(root, rel, text) {
  const full = path.join(root, rel);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, text);
}
function tmp(prefix) { return fs.mkdtempSync(path.join(os.tmpdir(), prefix)); }
function lines(dir, layout) { return check(dir, layout).map((v) => `${path.relative(dir, v.file)}:${v.line}`).sort(); }

const PLAY_CLOSE = '# --- Standard Play Close (shared; see ../_shared/play-close.md) ---';

// --- source layout ---------------------------------------------------------
let dir = tmp('ip-src-');
write(dir, 'plays/do-thing/SKILL.md', '---\nname: do-thing\n---\nRun `core/tools/lint-components/index.js`.\n');
write(dir, 'plays/do-thing/reference/ice.md', 'The model: `core/components/memory/standards/x.md`.\n');
write(dir, 'plays/do-thing/scripts/run.py', 'ROOT = "~/.garura/core/memory/knowledge"\n');
write(dir, 'plays/do-thing/scripts/test_run.py', 'ROOT = "core/components/plays"\n');
write(dir, 'skills/find-thing/SKILL.md', '---\nname: find-thing\n---\nRead `./.garura/core/memory/standards/rules/pr.md`.\n');
write(dir, 'skills/find-thing/SKILL.md.bak', 'core/components/\n');
write(dir, 'agents/thing-keeper.md', '---\nname: thing-keeper\n---\nRun `python3 .garura/core/tools/memory/memory.py find`.\n');
write(dir, 'plays/_shared/play-close.md', 'This lives at `core/components/plays/_shared/play-close.md`.\n');
t('source layout: each source path, memory folder and note of origin is found; the memory tool and a dev test pass',
  lines(dir, 'source'),
  ['plays/_shared/play-close.md:1', 'plays/do-thing/SKILL.md:4', 'plays/do-thing/reference/ice.md:1',
    'plays/do-thing/scripts/run.py:1', 'skills/find-thing/SKILL.md:4']);
t('the rule id is installed-paths/source-path, an error',
  [...new Set(check(dir, 'source').map((v) => `${v.rule}/${v.severity}`))], [`${RULE_ID}/error`]);

dir = tmp('ip-exc-');
for (const part of ['create-play', 'edit-play', 'create-loop', 'edit-loop', 'install-garura', 'uninstall-garura', 'edit-ontology']) {
  write(dir, `plays/${part}/SKILL.md`, 'Edit `core/components/plays/` and run `core/tools/lint-components`.\n');
}
write(dir, 'skills/author-product-ontology/SKILL.md', 'Read `core/components/memory/`.\n');
write(dir, 'plays/commit-change/SKILL.md', 'clean\n');
write(dir, 'plays/commit-change/scripts/analyze_changeset.py', 'R = r"^core/components/"\n');
write(dir, 'skills/assess-pr/SKILL.md', 'clean\n');
write(dir, 'skills/assess-pr/reference/quality-rules.md', '**Triggers:** `core/components/**` changed\n');
write(dir, 'loops/complete-thing/SKILL.md', 'clean\n');
write(dir, 'loops/complete-thing/scripts/x.py', '"core/tools/naming"\n');
t('the named exceptions pass; a loop that names the source fails',
  lines(dir, 'source'), ['loops/complete-thing/scripts/x.py:1']);

// --- installed layout ------------------------------------------------------
dir = tmp('ip-inst-');
write(dir, 'skills/do-thing/SKILL.md', `---\nname: do-thing\n---\n${PLAY_CLOSE}\n# --- end Standard Play Close ---\nSee \`core/components/plays/_shared/play-close.md\`.\n`);
write(dir, 'skills/complete-thing/SKILL.md', '---\nname: complete-thing\nkind: loop\n---\nclean\n');
write(dir, 'skills/find-thing/SKILL.md', '---\nname: find-thing\n---\nUse `.garura/core/tools/lint-play/lint_play.py`.\n');
write(dir, 'skills/create-play/SKILL.md', 'Edit `core/components/`.\n');
write(dir, 'skills/_shared/play-close.md', 'Checked by `core/tools/lint-components`.\n');
write(dir, 'agents/thing-keeper.md', '---\nname: thing-keeper\n---\nLoad from `~/.garura/core/memory/`.\n');
t('installed layout: the play, the shared file and the agent fail; the installed tool and create-play pass',
  lines(dir, 'installed'), ['agents/thing-keeper.md:4', 'skills/_shared/play-close.md:1', 'skills/do-thing/SKILL.md:6']);

const found = discover(dir, 'installed');
t('installed layout: a SKILL.md with the close anchor is a play',
  found.plays.map((c) => c.name), ['do-thing']);
t('installed layout: a SKILL.md with kind: loop is a loop', found.loops.map((c) => c.name), ['complete-thing']);
t('installed layout: the rest are skills', found.skills.map((c) => c.name).sort(), ['create-play', 'find-thing']);
t('installed layout: agents are .claude/agents/*.md', found.agents.map((c) => c.name), ['thing-keeper']);
t('installed layout: a loop finds the shared close in skills/_shared',
  found.loops[0].playsShared, path.join(dir, 'skills', '_shared'));

// --- each installed part judged by its real kind (round 3) ------------------
const { kindFromText } = require('../lib/discover');
const structural = require('../lib/rules/structural');
t('front matter: a user-invocable SKILL.md with no close anchor is a play (create-play, edit-play)',
  kindFromText('---\nname: create-play\nuser-invocable: true\n---\n# create-play\n'), 'play');
t('front matter: a pipeline position or a Compiled From section makes a play',
  [kindFromText('---\nname: p\nposition: end\n---\n'), kindFromText('---\nname: p\n---\n## Compiled From\n')],
  ['play', 'play']);
t('front matter: user-invocable false and no play mark is a skill',
  kindFromText('---\nname: find-thing\nuser-invocable: false\n---\n## Input\n'), 'skill');
const proj = tmp('ip-kinds-');
const claudeDir = path.join(proj, '.claude');
write(claudeDir, 'skills/edit-loop/SKILL.md', '---\nname: edit-loop\ndescription: x\n---\n# edit-loop\n');
write(claudeDir, 'skills/find-thing/SKILL.md', '---\nname: find-thing\ndescription: x\nuser-invocable: false\nallowed-tools: Read\n---\n## Input\n## Process\n## Output\n');
write(proj, '.garura/install-manifest.json', JSON.stringify({ record: { kinds: {
  '.claude/skills/edit-loop': 'play', '.claude/skills/find-thing': 'skill' } } }));
const kinds = discover(claudeDir, 'installed');
t('the install manifest decides the kind: edit-loop is a play though its text has no play mark',
  [kinds.plays.map((c) => c.name), kinds.skills.map((c) => c.name)], [['edit-loop'], ['find-thing']]);
t('an installed skill with no model line is not an error (the install sets the host model)',
  structural.check(kinds).filter((v) => v.file.includes('find-thing')).map((v) => v.message), []);
t('a source skill with no model line is still an error',
  structural.checkSkill({ file: path.join(claudeDir, 'skills/find-thing/SKILL.md'), name: 'find-thing', type: 'skill' })
    .map((v) => v.message), ['Missing required frontmatter field: model']);

// --- pointers to Garura's own docs (decision 10) -----------------------------
t('a pointer to a Garura docs folder or file is found',
  ['Load from `docs/framework/` as needed', 'see ../../docs/standards/harness-standard.md',
    '(`docs/philosophy/idsd.md`)', 'What a loop is: `docs/components/loops.md`.'].map(docsPointer),
  ['docs/framework/', 'docs/standards/harness-standard.md', 'docs/philosophy/idsd.md', 'docs/components/loops.md']);
t('repo layout is not a pointer: a project ADR folder, a review grounding glob, a branch prefix, a bare docs/',
  ['ADRs in `docs/adr/NNN-<slug>.md`', 'grounds on `docs/philosophy/**`, `docs/adr/**`', '| `docs/*` | docs |',
    'Triggers: `docs/components/*.md`', 'creates new docs/decisions as untracked files', 'in README.md, docs/, .github/',
    'mydocs/framework/x'].map(docsPointer),
  [null, null, null, null, null, null, null]);
const docsDir = tmp('ip-docs-');
write(docsDir, 'agents/thing-keeper.md', '---\nname: thing-keeper\n---\nLoad framework protocols from `docs/framework/` as needed.\n');
write(docsDir, 'skills/find-thing/SKILL.md', '---\nname: find-thing\n---\nThe ADRs live in `docs/adr/`; ground on `docs/philosophy/**`.\n');
write(docsDir, 'skills/find-thing/reference/notes.md', 'Background: `docs/philosophy/idsd.md`.\n');
write(docsDir, 'skills/edit-play/SKILL.md', 'See `docs/standards/harness-standard.md`.\n');
t('installed layout: a docs pointer fails in an agent and a reference file; repo layout and a source-only part pass',
  lines(docsDir, 'installed'), ['agents/thing-keeper.md:4', 'skills/find-thing/reference/notes.md:1']);
t('a docs pointer is reported under installed-paths/source-path with its own message',
  check(docsDir, 'installed').every((v) => v.rule === RULE_ID && v.message.includes("Garura's documentation")), true);

// --- the tools laid beside the target (decision 23) -------------------------
const toolProj = tmp('ip-tools-');
const toolTarget = path.join(toolProj, '.claude');
write(toolTarget, 'skills/find-thing/SKILL.md', '---\nname: find-thing\n---\nclean\n');
write(toolProj, '.garura/core/tools/run-thing/run.py', 'SRC = "core/components/plays"\nOK = ".garura/core/tools/memory/memory.py"\n');
write(toolProj, '.garura/core/tools/run-thing/README.md', 'Read `~/.garura/core/memory/standards`.\n');
write(toolProj, '.garura/core/tools/run-thing/test_run.py', 'SRC = "core/components/"\n');
write(toolProj, '.garura/core/tools/run-thing/__pycache__/run.py', 'core/components/\n');
write(toolProj, '.garura/core/tools/node-thing/index.js', 'module.exports = 1;\n');
write(toolProj, '.garura/core/tools/node-thing/node_modules/dep/index.js', '// core/tools/x\n');
write(toolProj, '.garura/core/tools/lint-components/lib/rules/installed-paths.js', "const re = /core\\/components\\//; // core/components/\n");
function toolLines() {
  return check(toolTarget, 'installed').map((v) => `${path.relative(toolProj, v.file)}:${v.line}`).sort();
}
t('installed layout: a laid tool that names the source or a memory folder fails; tests, caches, node_modules and the linter rule pass',
  toolLines(), ['.garura/core/tools/run-thing/README.md:1', '.garura/core/tools/run-thing/run.py:1']);
t('a laid tool is named in the message',
  check(toolTarget, 'installed').every((v) => v.message.startsWith('The tool run-thing')), true);
t('the source layout does not scan the laid tools', check(toolTarget, 'source'), []);

// --- the command line ------------------------------------------------------
const index = path.join(__dirname, '..', 'index.js');
function run(args) {
  try {
    return JSON.parse(execFileSync('node', [index, ...args], { encoding: 'utf8' }));
  } catch (err) {
    return JSON.parse(err.stdout);
  }
}
let out = run(['--layout', 'installed', '--target', dir]);
t('the command line runs the installed layout and says so', out.layout, 'installed');
t('with no --naming the naming rules are skipped, and the output says so',
  (out.notes || []).some((n) => n.startsWith('naming rules skipped')), true);
t('the installed-paths errors are in the report',
  out.violations.filter((v) => v.rule === RULE_ID).length, 3);

const naming = path.join(tmp('ip-naming-'), 'naming.yaml');
fs.writeFileSync(naming, 'play:\n  verbs: { shape: x }\nskill:\n  verbs: { find: x }\nagent:\n  roles: [keeper]\nloop:\n  verb: complete\nreserved: []\n');
out = run(['--layout', 'installed', '--target', dir, '--naming', naming]);
t('with --naming the naming rules run (do-thing has no play verb)',
  out.violations.some((v) => v.rule === 'naming-play' && v.file.endsWith(path.join('do-thing', 'SKILL.md'))), true);
t('with --naming there is no skip note', (out.notes || []).length, 0);

console.log(`\n${passed} passed, 0 failed`);
