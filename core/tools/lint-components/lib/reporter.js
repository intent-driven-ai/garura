'use strict';

/**
 * Report violations in the requested format.
 *
 * @param {{ violations: Array, summary: Object }} result
 * @param {'json'|'text'} format
 */
function report(result, format) {
  const notes = result.notes || [];
  if (format === 'text') {
    for (const n of notes) {
      process.stdout.write(`note: ${n}\n`);
    }
    for (const v of result.violations) {
      process.stdout.write(
        `${v.severity}: ${v.file}:${v.line} [${v.rule}] ${v.message}\n`
      );
    }
    process.stdout.write(
      `${result.summary.errors} errors, ${result.summary.warnings} warnings, ${result.summary.infos} infos\n`
    );
  } else {
    // Default: json
    const out = { violations: result.violations, summary: result.summary };
    if (result.layout) out.layout = result.layout;
    if (notes.length) out.notes = notes;
    process.stdout.write(JSON.stringify(out, null, 2) + '\n');
  }
}

module.exports = { report };
