'use strict';

// Naming rules (harness standard, ADR 046, #740). Every rule's data lives in
// memory/standards/rules/naming.yaml; this file holds no rule of its own.

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const SHORTENED = ['arch', 'impl', 'cfg', 'env', 'util', 'utils', 'mgr', 'misc', 'tmp'];

function loadStandard(targetDir) {
  const file = path.join(targetDir, 'memory', 'standards', 'rules', 'naming.yaml');
  if (!fs.existsSync(file)) return null;
  return { file, rules: yaml.load(fs.readFileSync(file, 'utf8')) };
}

function violation(component, rule, message) {
  return { file: component.file, rule, severity: 'error', message, line: 1 };
}

function checkName(component, std) {
  const out = [];
  const name = component.name;
  const words = name.split('-');
  const first = words[0];
  const terms = new Set(std.industry_terms || []);
  const reserved = new Set(std.reserved || []);
  const loopVerb = (std.loop || {}).verb;

  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(name) || name.length > 64) {
    out.push(violation(component, 'naming-shape', `"${name}" must be lowercase words joined by "-", at most 64 characters`));
  }
  if (reserved.has(name) || reserved.has(first)) {
    out.push(violation(component, 'naming-reserved',
      `"${name}" is, or starts with, a Claude Code or Codex built-in command ("${reserved.has(name) ? name : first}")`));
  }
  for (const w of words) {
    if (SHORTENED.includes(w) && !terms.has(w)) {
      out.push(violation(component, 'naming-shortened', `"${name}" uses the shortened word "${w}"; spell it out`));
    }
  }

  if (component.type === 'loop') {
    if (first !== loopVerb || words.length < 2) {
      out.push(violation(component, 'naming-loop', `loop "${name}" must be "${loopVerb}-<phase>"`));
    }
    return out;
  }
  if (first === loopVerb) {
    out.push(violation(component, 'naming-loop-verb', `"${name}" starts with "${loopVerb}-", which only loops may use`));
  }

  if (component.type === 'play') {
    const play = std.play || {};
    const verbs = Object.keys(play.verbs || {});
    const oneWord = play.one_word || [];
    if (oneWord.includes(name)) return out;
    if (!verbs.includes(first) || words.length < 2) {
      out.push(violation(component, 'naming-play', `play "${name}" must be <verb>-<object> with a play verb (${verbs.join(', ')})`));
    }
  } else if (component.type === 'skill') {
    const skill = std.skill || {};
    const verbs = Object.keys(skill.verbs || {});
    if ((skill.exceptions || []).includes(name)) return out;
    if (!verbs.includes(first) || words.length < 2) {
      out.push(violation(component, 'naming-skill', `skill "${name}" must be <verb>-<object> with a skill verb (${verbs.join(', ')})`));
    }
  } else if (component.type === 'agent') {
    const roles = (std.agent || {}).roles || [];
    if (!roles.includes(words[words.length - 1])) {
      out.push(violation(component, 'naming-agent', `agent "${name}" must end in a role noun (${roles.join(', ')})`));
    }
  }
  return out;
}

function check(components, targetDir) {
  const loaded = loadStandard(targetDir);
  if (!loaded) return [];
  const std = loaded.rules || {};
  const all = [].concat(components.plays, components.skills, components.agents, components.loops || []);
  let out = [];
  const seen = new Map();
  for (const c of all) {
    out = out.concat(checkName(c, std));
    if (seen.has(c.name)) {
      out.push(violation(c, 'naming-duplicate', `"${c.name}" is also the name of a ${seen.get(c.name)}; every name is used once`));
    } else {
      seen.set(c.name, c.type);
    }
  }
  return out;
}

module.exports = { check, checkName };
