'use strict';

// One shared memory reading protocol for agents (decision 21 of #860). The protocol lives once,
// in agents/_shared/memory-reading.md, which the install lays in the installed _shared/ folder
// (.claude/skills/_shared/memory-reading.md). An agent that uses the memory tool points to that
// file, and keeps only its own table of what it puts in short-term memory.
//
// Two errors, in the source and the installed layout:
//   memory-reading/missing-pointer  an agent names the memory tool (memory.py, or "memory tool")
//                                   and does not point to _shared/memory-reading.md
//   memory-reading/pasted-protocol  an agent still carries the pasted protocol: the numbered
//                                   "1. **Find**" steps under "## Memory Reading Protocol", or
//                                   the inline `python3 -c 'import json,os,sys; a=json.load(sys.stdin)`
//                                   copy command (the shared copy_memory.py does that job)
const fs = require('fs');

const MISSING = 'memory-reading/missing-pointer';
const PASTED = 'memory-reading/pasted-protocol';
const SHARED_FILE = '_shared/memory-reading.md';

const USES_TOOL = /memory\.py\b|memory tool/i;
const HEADING = /^##\s+Memory Reading Protocol\s*$/;
const FIND_STEP = /^\s*1\.\s+\*\*Find\*\*/;
const ONE_LINER = /python3\s+-c\s+['"]\s*import\s+json\s*,\s*os\s*,\s*sys\s*;\s*a\s*=\s*json\.load\(\s*sys\.stdin\s*\)/;

/**
 * The violations of one agent file's text.
 * @param {string} file
 * @param {string} content
 * @param {string} name
 */
function checkText(file, content, name) {
  const out = [];
  if (USES_TOOL.test(content) && !content.includes(SHARED_FILE)) {
    out.push({
      file,
      rule: MISSING,
      severity: 'error',
      message: `The agent ${name} uses the memory tool and does not point to the shared protocol. ` +
        `Point to .claude/skills/${SHARED_FILE} (its installed place), and keep only the table of ` +
        'what the agent puts in short-term memory.',
      line: 1,
    });
  }
  const lines = content.split('\n');
  let inFence = false;
  let inProtocol = false;
  lines.forEach((text, i) => {
    if (ONE_LINER.test(text)) {
      out.push({
        file,
        rule: PASTED,
        severity: 'error',
        message: `The agent ${name} carries the pasted copy command. Use the shared script ` +
          `_shared/copy_memory.py, as ${SHARED_FILE} says.`,
        line: i + 1,
      });
    }
    if (/^\s*(```|~~~)/.test(text)) { inFence = !inFence; return; }
    if (inFence) return;
    if (/^##\s/.test(text)) { inProtocol = HEADING.test(text); return; }
    if (inProtocol && FIND_STEP.test(text)) {
      out.push({
        file,
        rule: PASTED,
        severity: 'error',
        message: `The agent ${name} carries the pasted Memory Reading Protocol steps. Delete them and ` +
          `point to ${SHARED_FILE}, which holds them once.`,
        line: i + 1,
      });
    }
  });
  return out;
}

/**
 * @param {{agents: Array<{file: string, name: string}>}} components - from discover (either layout)
 * @returns {Array<object>} violations
 */
function check(components) {
  let out = [];
  for (const agent of components.agents || []) {
    let content;
    try {
      content = fs.readFileSync(agent.file, 'utf8');
    } catch (_) {
      continue;
    }
    out = out.concat(checkText(agent.file, content, agent.name));
  }
  return out;
}

module.exports = { check, checkText, MISSING, PASTED, SHARED_FILE };
