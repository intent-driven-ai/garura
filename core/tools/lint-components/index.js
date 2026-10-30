#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const discover = require('./lib/discover');
const structural = require('./lib/rules/structural');
const semantic = require('./lib/rules/semantic');
const crossReference = require('./lib/rules/cross-reference');
const naming = require('./lib/rules/naming');
const askingAPerson = require('./lib/rules/asking-a-person');
const sharedScripts = require('./lib/rules/shared-scripts');
const installedPaths = require('./lib/rules/installed-paths');
const memoryReading = require('./lib/rules/memory-reading');
const reporter = require('./lib/reporter');

function parseArgs(argv) {
  const args = {
    target: 'core/components',
    layout: 'source',
    naming: null,
    output: 'json',
    validateTemplates: false,
  };

  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--target' && argv[i + 1]) {
      args.target = argv[++i];
    } else if (arg.startsWith('--target=')) {
      args.target = arg.slice('--target='.length);
    } else if (arg === '--output' && argv[i + 1]) {
      args.output = argv[++i];
    } else if (arg.startsWith('--output=')) {
      args.output = arg.slice('--output='.length);
    } else if (arg === '--layout' && argv[i + 1]) {
      args.layout = argv[++i];
    } else if (arg.startsWith('--layout=')) {
      args.layout = arg.slice('--layout='.length);
    } else if (arg === '--naming' && argv[i + 1]) {
      args.naming = argv[++i];
    } else if (arg.startsWith('--naming=')) {
      args.naming = arg.slice('--naming='.length);
    } else if (arg === '--validate-templates') {
      args.validateTemplates = true;
    }
  }

  return args;
}

async function main() {
  const args = parseArgs(process.argv);

  // Resolve target relative to cwd
  const targetDir = path.resolve(process.cwd(), args.target);
  if (args.layout !== 'source' && args.layout !== 'installed') {
    process.stderr.write(`Unknown layout '${args.layout}': use source or installed\n`);
    process.exit(2);
  }

  // Step 1: Discover all components. The source layout is a components folder
  // (plays/, loops/, skills/, agents/); the installed layout is .claude or .agents
  // (skills/<name>/SKILL.md for plays, loops and skills, and agents/*.md).
  const components = discover(targetDir, args.layout);
  const notes = [];
  const namingFile = naming.standardFile(targetDir, { layout: args.layout, naming: args.naming });
  if (!namingFile) {
    notes.push('naming rules skipped: no naming standard given (--naming <naming.yaml>)');
  } else if (!fs.existsSync(namingFile)) {
    notes.push(`naming rules skipped: no naming standard at ${namingFile}`);
  }

  // Steps 2-4: Run rule sets, collect violations
  let violations = [];

  violations = violations.concat(structural.check(components));
  violations = violations.concat(semantic.check(components));
  violations = violations.concat(crossReference.check(components));
  violations = violations.concat(naming.check(components, targetDir, { layout: args.layout, naming: args.naming }));
  violations = violations.concat(askingAPerson.check(components));
  violations = violations.concat(sharedScripts.check(targetDir));
  violations = violations.concat(installedPaths.check(targetDir, args.layout));
  violations = violations.concat(memoryReading.check(components));

  // Step 5: Build summary
  const summary = {
    errors: violations.filter((v) => v.severity === 'error').length,
    warnings: violations.filter((v) => v.severity === 'warning').length,
    infos: violations.filter((v) => v.severity === 'info').length,
  };

  // Step 6: Report, with every path relative to where the linter ran: a report is often
  // committed as a review record, and an absolute path names the machine and its user.
  const here = process.cwd() + path.sep;
  const relative = (text) => (typeof text === 'string' ? text.split(here).join('') : text);
  violations = violations.map((v) => ({ ...v, file: relative(v.file), message: relative(v.message) }));
  reporter.report({ violations, summary, layout: args.layout, notes: notes.map(relative) }, args.output);

  // Step 7: Exit code
  process.exit(summary.errors > 0 ? 1 : 0);
}

main().catch((err) => {
  process.stderr.write('Fatal error: ' + err.message + '\n');
  process.exit(2);
});
