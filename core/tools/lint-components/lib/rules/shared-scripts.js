'use strict';

// Shared scripts that create-play stamps into plays and that must stay byte-identical to
// their main copy in plays/create-play/references/. Copies are checked wherever they sit under
// plays/*/scripts/ or skills/*/scripts/. Kept short on purpose: only scripts listed here are
// checked, so other stamped scripts are not flagged.
const fs = require('fs');
const path = require('path');

const SHARED_SCRIPTS = ['lint_grounding.py', 'model_names.py',
  // the plan-aware change scripts and the branch-name issue reader (#731, #673)
  'preflight.py', 'resolve_plan.py', 'resolve_target.py', 'setup_branch.py', 'submit_pr.py', 'merge_pr.py'];

// Every <targetDir>/{plays,skills}/<name>/scripts/<script> that exists.
function copiesOf(targetDir, script) {
  const out = [];
  for (const kind of ['plays', 'skills']) {
    const dir = path.join(targetDir, kind);
    if (!fs.existsSync(dir)) continue;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const copy = path.join(dir, entry.name, 'scripts', script);
      if (fs.existsSync(copy)) out.push(copy);
    }
  }
  return out;
}

/**
 * @param {string} targetDir - Absolute path to the components folder (e.g. core/components)
 * @returns {Array<object>} violations
 */
function check(targetDir) {
  const violations = [];
  const playsDir = path.join(targetDir, 'plays');
  const hasPlays = fs.existsSync(playsDir);

  for (const script of hasPlays ? SHARED_SCRIPTS : []) {
    const mainCopy = path.join(playsDir, 'create-play', 'references', script);
    if (!fs.existsSync(mainCopy)) continue;
    const mainBytes = fs.readFileSync(mainCopy);
    const ruleName = script.replace(/\.py$/, '');

    for (const copy of copiesOf(targetDir, script)) {
      if (!fs.readFileSync(copy).equals(mainBytes)) {
        violations.push({
          file: copy,
          rule: `structural/${ruleName}-drift`,
          severity: 'error',
          message: `This copy of ${script} differs from the main copy at plays/create-play/references/${script}. Copy the main copy over it unchanged (change the main copy first if the change is wanted).`,
          line: 1,
        });
      }
    }
  }

  violations.push(...checkToolCopies(targetDir));
  return violations;
}

// Scripts whose main copy is a tool (#860): lint_play.py lives in core/tools/lint-play/, and
// create-play and edit-play keep stamped copies. Every copy must match the tool byte for byte.
// The tool is found beside the components folder (source layout: core/tools/) or in the
// project's install folder (installed layout: .garura/core/tools/ beside .claude).
const TOOL_SCRIPTS = [{ script: 'lint_play.py', tool: 'lint-play' }];

function toolMainCopy(targetDir, tool, script) {
  const candidates = [
    path.join(targetDir, '..', 'tools', tool, script),
    path.join(targetDir, '..', '.garura', 'core', 'tools', tool, script),
  ];
  return candidates.find((c) => fs.existsSync(c)) || null;
}

function checkToolCopies(targetDir) {
  const violations = [];
  for (const { script, tool } of TOOL_SCRIPTS) {
    const mainCopy = toolMainCopy(targetDir, tool, script);
    if (!mainCopy) continue;
    const mainBytes = fs.readFileSync(mainCopy);
    const ruleName = script.replace(/\.py$/, '');
    for (const copy of copiesOf(targetDir, script)) {
      if (!fs.readFileSync(copy).equals(mainBytes)) {
        violations.push({
          file: copy,
          rule: `structural/${ruleName}-drift`,
          severity: 'error',
          message: `This copy of ${script} differs from the tool's copy (the ${tool} tool). Copy the tool's ${script} over it unchanged (change the tool first if the change is wanted).`,
          line: 1,
        });
      }
    }
  }
  return violations;
}

module.exports = { check, SHARED_SCRIPTS, TOOL_SCRIPTS };
