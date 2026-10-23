'use strict';

// A play or loop that asks a person a question must point to the shared rule for asking a
// person, memory/standards/rules/asking-a-person.md (#821, follows #820).

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

function asksAPerson(content) {
  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    for (const signal of ASKS_A_PERSON) {
      if (signal.test(lines[i])) return { line: i + 1, text: lines[i].trim() };
    }
  }
  return null;
}

function checkPlay(component) {
  const content = fs.readFileSync(component.file, 'utf8');
  const asks = asksAPerson(content);
  if (!asks || content.includes(RULE_FILE)) return [];
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

module.exports = { check, checkPlay, asksAPerson, RULE_ID };
