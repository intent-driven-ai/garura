'use strict';

// The parts that ask a person a question must point to the shared rule for asking a person,
// skills/_shared/asking-a-person.md, by the path it has when installed: _shared/asking-a-person.md
// (beside the installed skills). #821 began the check; #854 moved the rule out of memory and
// set the list of parts it checks.
//
// The check reads only the parts named in PARTS. Any other part is never an error under this
// rule. A play names the rule in its own steps: the body after the frontmatter, in the
// `## Workflow` section (with any `## Phase` / `## Step` headings inside it), never in the Role,
// Constraints, Pre-flight, Task DAG or Arguments text before the workflow. A play or skill with
// no `## Workflow` section is read whole, minus its reference and note sections. The frontmatter
// is never read.

const fs = require('fs');

const RULE_ID = 'asking-a-person/missing-pointer';
const RULE_FILE = '_shared/asking-a-person.md';

// The parts that ask a person and must name the rule, by kind.
const PARTS = {
  play: ['edit-ontology', 'shape-slice'],
  skill: ['author-product-ontology', 'find-slice-gaps', 'author-slice-brief'],
};

// Sections that are references or notes about the play, not its steps.
const NOT_STEPS = /^(?:references?|related|compilation metadata|compiled from|compiled note|recompile note|direct-edit deviation note|per-environment migration note)\b/i;
const WORKFLOW = /^workflow\b/i;
const INSIDE_WORKFLOW = /^(?:phase|step)\b/i;

// Split the file into level-2 sections, skipping the frontmatter and ignoring headings inside
// code fences. Each section: { title, lines: [{ n, text }] }. Text before the first `## ` is
// the section with title ''.
function sections(content) {
  const lines = content.split('\n');
  let start = 0;
  if (lines[0] === '---') {
    const end = lines.indexOf('---', 1);
    if (end > 0) start = end + 1;
  }
  const out = [{ title: '', lines: [] }];
  let inFence = false;
  for (let i = start; i < lines.length; i++) {
    const text = lines[i];
    if (/^\s*(```|~~~)/.test(text)) inFence = !inFence;
    const h = !inFence && /^##\s+(.*)$/.exec(text);
    if (h) out.push({ title: h[1].trim(), lines: [] });
    out[out.length - 1].lines.push({ n: i + 1, text });
  }
  return out;
}

// The play's steps: where a person may be asked, and the only place the pointer counts.
function stepRegions(content) {
  const all = sections(content);
  const w = all.findIndex((s) => WORKFLOW.test(s.title));
  if (w < 0) return all.filter((s) => !NOT_STEPS.test(s.title));
  let end = w + 1;
  while (end < all.length && INSIDE_WORKFLOW.test(all[end].title)) end++;
  return all.slice(w, end);
}

function namesTheRule(content) {
  return stepRegions(content).some((s) => s.lines.some((l) => l.text.includes(RULE_FILE)));
}

function checkPart(component) {
  const content = fs.readFileSync(component.file, 'utf8');
  if (namesTheRule(content)) return [];
  return [{
    file: component.file,
    rule: RULE_ID,
    severity: 'error',
    message: `${component.type} "${component.name}" asks a person a question but does not point to the ` +
      `shared rule ${RULE_FILE} (source: skills/${RULE_FILE}); name that file where it asks`,
    line: 1,
  }];
}

function isChecked(component) {
  return (PARTS[component.type] || []).includes(component.name);
}

function check(components) {
  const all = [].concat(components.plays || [], components.skills || []);
  let out = [];
  for (const c of all) if (isChecked(c)) out = out.concat(checkPart(c));
  return out;
}

module.exports = { check, checkPart, isChecked, namesTheRule, PARTS, RULE_ID, RULE_FILE };
