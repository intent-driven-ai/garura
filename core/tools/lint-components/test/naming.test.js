'use strict';
// Fixtures for lib/rules/naming.js (#740): one passing and one failing name per rule.
const assert = require('assert');
const { checkName } = require('../lib/rules/naming');
const STANDARD = {
  industry_terms: ['pr', 'ux'], reserved: ['plan', 'review', 'design', 'run', 'focus'],
  loop: { verb: 'complete' },
  play: { verbs: { discover: '', shape: '', check: '', create: '' }, one_word: ['next'] },
  skill: { verbs: { author: '', check: '' }, exceptions: ['platform-adapter'] },
  agent: { roles: ['keeper'] },
};
const rules = (type, name) => checkName({ type, name, file: 'x' }, STANDARD).map((v) => v.rule);
let passed = 0;
function t(label, got, want) { assert.deepStrictEqual(got, want, label); passed++; console.log(`  [PASS] ${label}`); }
t('a play with a play verb passes', rules('play', 'discover-domains'), []);
t('a play with no verb fails', rules('play', 'vision'), ['naming-play']);
t('the named one-word play passes', rules('play', 'next'), []);
t('a play that starts with a built-in fails', rules('play', 'review-change'), ['naming-reserved', 'naming-play']);
t('a built-in name fails', rules('play', 'focus'), ['naming-reserved', 'naming-play']);
t('a shortened word fails', rules('play', 'shape-arch-lens'), ['naming-shortened']);
t('an industry term passes', rules('play', 'shape-ux-lens'), []);
t('a loop named complete-<phase> passes', rules('loop', 'complete-discovery'), []);
t('a loop with another shape fails', rules('loop', 'discovery'), ['naming-loop']);
t('a play may not use the loop verb', rules('play', 'complete-thing'), ['naming-loop-verb', 'naming-play']);
t('a skill with a skill verb passes', rules('skill', 'author-slice'), []);
t('a skill with no skill verb fails', rules('skill', 'draft-rca'), ['naming-skill']);
t('the named skill exception passes', rules('skill', 'platform-adapter'), []);
t('an agent with a role passes', rules('agent', 'adr-keeper'), []);
t('an agent with no role fails', rules('agent', 'adr-thing'), ['naming-agent']);
t('upper case fails', rules('skill', 'Author-x'), ['naming-shape', 'naming-skill']);
console.log(`\n${passed} passed, 0 failed`);
