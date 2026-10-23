'use strict';

// Shared scripts that create-play stamps into plays and that must stay byte-identical to
// their main copy in plays/create-play/references/. Kept short on purpose: only scripts
// listed here are checked, so other stamped scripts are not flagged.
const fs = require('fs');
const path = require('path');

const SHARED_SCRIPTS = ['lint_grounding.py'];

/**
 * @param {string} targetDir - Absolute path to the components folder (e.g. core/components)
 * @returns {Array<object>} violations
 */
function check(targetDir) {
  const violations = [];
  const playsDir = path.join(targetDir, 'plays');
  if (!fs.existsSync(playsDir)) return violations;

  for (const script of SHARED_SCRIPTS) {
    const mainCopy = path.join(playsDir, 'create-play', 'references', script);
    if (!fs.existsSync(mainCopy)) continue;
    const mainBytes = fs.readFileSync(mainCopy);
    const ruleName = script.replace(/\.py$/, '');

    for (const entry of fs.readdirSync(playsDir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const copy = path.join(playsDir, entry.name, 'scripts', script);
      if (!fs.existsSync(copy)) continue;
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

  return violations;
}

module.exports = { check, SHARED_SCRIPTS };
