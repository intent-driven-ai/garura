'use strict';

// A play or loop that asks a person a question must point to the shared rule for asking a
// person, memory/standards/rules/asking-a-person.md (#821, follows #820).
//
// Only the play's own steps count, both for the "asks a person" signal and for the pointer:
// the body after the frontmatter, in the `## Workflow` section (with any `## Phase` / `## Step`
// headings inside it). The pointer counts only there, where the play asks: never in the Role,
// Constraints, Pre-flight, Task DAG or Arguments text before the workflow. A play with no
// `## Workflow` section is read whole, minus its reference and note sections, for both. The
// frontmatter is never read: a description that mentions approval is not a step.

const fs = require('fs');

const RULE_ID = 'asking-a-person/missing-pointer';
const RULE_FILE = 'asking-a-person.md';

// Signals that a play stops for a person's typed answer. Each one is a phrase compiled plays
// use for a checkpoint or a question shown for a typed reply. AskUserQuestion is never used.
const ASKS_A_PERSON = [
  /\bcheckpoint\s*\(class:/i, // a compiled checkpoint step
  /\bwait(?:s|ing)?\s+for\s+(?:a|the)?\s*(?:\w+'s\s+)?typed\b/i, // "wait for the typed reply"
  /\btyped\s+(?:yes|approval|approve|answers?|repl(?:y|ies)|responses?|confirmation|decision)\b/i,
  /\btypes?\s+[*`"]*yes\b/i, // "type **yes**"
  /\basks?\s+for\s+approval\b/i,
  /\binterviews?\s+the\s+(?:user|person)\b/i,
];

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
  let fence = false;
  for (let i = start; i < lines.length; i++) {
    const text = lines[i];
    if (/^\s*(```|~~~)/.test(text)) fence = !fence;
    const h = !fence && /^##\s+(.*)$/.exec(text);
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

// A signal may wrap onto the next line ("Checkpoint" then "(class: standard)"), so each line is
// also read joined with the one after it.
function findSignal(regions) {
  const hit = (text) => ASKS_A_PERSON.some((signal) => signal.test(text));
  for (const s of regions) {
    for (let i = 0; i < s.lines.length; i++) {
      const l = s.lines[i];
      const next = s.lines[i + 1];
      if (hit(l.text)) return { line: l.n, text: l.text.trim() };
      if (next && !hit(next.text) && hit(`${l.text.trim()} ${next.text.trim()}`)) {
        return { line: l.n, text: l.text.trim() };
      }
    }
  }
  return null;
}

function asksAPerson(content) {
  return findSignal(stepRegions(content));
}

function namesTheRule(content) {
  return stepRegions(content).some((s) => s.lines.some((l) => l.text.includes(RULE_FILE)));
}

function checkPlay(component) {
  const content = fs.readFileSync(component.file, 'utf8');
  const asks = asksAPerson(content);
  if (!asks || namesTheRule(content)) return [];
  return [{
    file: component.file,
    rule: RULE_ID,
    severity: 'error',
    message: `${component.type} "${component.name}" asks a person a question (line ${asks.line}) but does not ` +
      `point to the shared rule memory/standards/rules/${RULE_FILE}; name that file where the play asks`,
    line: asks.line,
  }];
}

function check(components) {
  const all = [].concat(components.plays || [], components.loops || []);
  let out = [];
  for (const c of all) out = out.concat(checkPlay(c));
  return out;
}

module.exports = { check, checkPlay, asksAPerson, namesTheRule, RULE_ID };
