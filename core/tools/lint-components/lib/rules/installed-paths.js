'use strict';

// installed-paths/source-path (#860). An installed part reads only installed files. A play,
// loop, agent or skill, every file in its folder (its reference files and scripts), and the
// shared files must not name Garura's source (core/components/, core/tools/), a memory
// folder (~/.garura/core/memory, .garura/core/memory/) or Garura's own documentation (docs/). The memory tool's place,
// .garura/core/tools/memory/, is an installed place and passes. It runs in both layouts. In the
// installed layout it also scans the tools the install lays beside the target
// (<project>/.garura/core/tools/<tool>/, not node_modules or caches).
//
// Named exceptions, which work on the source only by design: the meta plays and the skill
// they run, dev tests, and the repo-layout text that sorts the paths of the repo under review.
const fs = require('fs');
const path = require('path');

const RULE_ID = 'installed-paths/source-path';

const SOURCE_ONLY_PARTS = new Set([
  'create-play', 'edit-play', 'create-loop', 'edit-loop',
  'install-garura', 'uninstall-garura', 'edit-ontology', 'author-product-ontology',
]);

// Files, by their path inside a part's folder, that sort the paths of the repo under review.
const REPO_LAYOUT_FILES = new Set([
  'commit-change/scripts/analyze_changeset.py',
  'assess-pr/reference/quality-rules.md',
  // the component linter's own rules: this rule's patterns, and where the source layout keeps
  // the lint_play.py tool (the linter checks Garura's source layout too)
  'lint-components/lib/rules/installed-paths.js',
  'lint-components/lib/rules/shared-scripts.js',
]);

const PATTERNS = [
  { re: /core\/components\//, what: 'core/components/' },
  { re: /(?<!\.garura\/)core\/tools\//, what: 'core/tools/' },
  { re: /~\/\.garura\/core\/memory/, what: '~/.garura/core/memory' },
  { re: /\.garura\/core\/memory\//, what: '.garura/core/memory/' },
];

// Garura's own documentation (docs/ in Garura's repository). The install never copies it, so an
// installed part that points there points at nothing (decision 10 of #860). Repo layout is not a
// pointer: a project's own docs/adr/, a glob over the reviewed repo (docs/philosophy/**), a
// docs/* branch prefix or a bare docs/ folder name pass.
const GARURA_DOCS = /(?<![A-Za-z0-9_-])docs\/(agentic-methodology|components|design|framework|philosophy|standards|usage)(?![A-Za-z0-9_-])[^\s`'"(),;]*/g;

function docsPointer(line) {
  for (const m of line.matchAll(GARURA_DOCS)) {
    if (!m[0].includes('*')) return m[0];
  }
  return null;
}

const TEXT_EXT = new Set(['.md', '.py', '.js', '.yaml', '.yml', '.json', '.sh', '.txt', '.html', '.css', '']);

function isDevTest(name) {
  return /^test_.*\.py$/.test(name) || /\.test\.js$/.test(name);
}

function filesUnder(dir) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === '__pycache__' || entry.name === 'node_modules' || entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...filesUnder(full));
    else if (entry.isFile() && TEXT_EXT.has(path.extname(entry.name)) && !isDevTest(entry.name)) out.push(full);
  }
  return out;
}

function scanFile(file, partLabel) {
  const out = [];
  const lines = fs.readFileSync(file, 'utf8').split('\n');
  lines.forEach((line, i) => {
    const doc = docsPointer(line);
    if (doc) {
      out.push({
        file,
        rule: RULE_ID,
        severity: 'error',
        message: `${partLabel} points to Garura's documentation (${doc}), which the install never copies. ` +
          'Put the text the part needs in the part itself (or its reference/ folder), or delete the pointer ' +
          'when it is only background.',
        line: i + 1,
      });
      return;
    }
    for (const p of PATTERNS) {
      if (p.re.test(line)) {
        out.push({
          file,
          rule: RULE_ID,
          severity: 'error',
          message: `${partLabel} names ${p.what}. An installed part reads only installed files: name the ` +
            'installed place (.claude/skills/, .claude/agents/, .garura/core/tools/), or read memory ' +
            'through the memory tool. A note of origin is deleted.',
          line: i + 1,
        });
        break;
      }
    }
  });
  return out;
}

/**
 * The folders and files to scan, as { root, name, files } — one entry for each part and one for
 * the shared files.
 */
function partsOf(targetDir, layout) {
  const parts = [];
  const folderKinds = layout === 'installed' ? ['skills'] : ['plays', 'loops', 'skills'];
  for (const kind of folderKinds) {
    const dir = path.join(targetDir, kind);
    if (!fs.existsSync(dir)) continue;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const root = path.join(dir, entry.name);
      if (entry.name.startsWith('_')) {
        parts.push({ name: entry.name, label: 'This shared file', root, files: filesUnder(root) });
      } else if (fs.existsSync(path.join(root, 'SKILL.md'))) {
        parts.push({ name: entry.name, label: `The part ${entry.name}`, root, files: filesUnder(root) });
      }
    }
  }
  const agentsDir = path.join(targetDir, 'agents');
  if (fs.existsSync(agentsDir)) {
    for (const entry of fs.readdirSync(agentsDir, { withFileTypes: true })) {
      if (entry.isFile() && entry.name.endsWith('.md')) {
        const name = entry.name.slice(0, -3);
        parts.push({ name, label: `The agent ${name}`, root: agentsDir, files: [path.join(agentsDir, entry.name)] });
      }
    }
  }
  if (layout === 'installed') parts.push(...laidTools(targetDir));
  return parts;
}

/**
 * The tools the install lays beside the target: <project>/.garura/core/tools/<tool>/, where the
 * target is <project>/.claude (or .agents). Each tool is one entry; filesUnder skips
 * node_modules, caches and dev tests.
 */
function laidTools(targetDir) {
  const toolsDir = path.join(path.dirname(path.resolve(targetDir)), '.garura', 'core', 'tools');
  if (!fs.existsSync(toolsDir)) return [];
  return fs.readdirSync(toolsDir, { withFileTypes: true })
    .filter((e) => e.isDirectory() && !e.name.startsWith('.') && e.name !== 'node_modules' && e.name !== '__pycache__')
    .map((e) => {
      const root = path.join(toolsDir, e.name);
      return { name: `tool:${e.name}`, label: `The tool ${e.name}`, root, files: filesUnder(root) };
    });
}

/**
 * @param {string} targetDir - the components folder (source layout) or .claude / .agents (installed)
 * @param {'source'|'installed'} layout
 */
function check(targetDir, layout = 'source') {
  let out = [];
  for (const part of partsOf(targetDir, layout)) {
    if (SOURCE_ONLY_PARTS.has(part.name)) continue;
    for (const file of part.files) {
      const inPart = path.relative(path.dirname(part.root), file).split(path.sep).join('/');
      if (REPO_LAYOUT_FILES.has(inPart)) continue;
      out = out.concat(scanFile(file, part.label));
    }
  }
  return out;
}

module.exports = { check, docsPointer, RULE_ID, SOURCE_ONLY_PARTS, REPO_LAYOUT_FILES };
