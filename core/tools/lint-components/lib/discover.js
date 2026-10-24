'use strict';

const fs = require('fs');
const path = require('path');

/**
 * Walk a directory and return matching files.
 * @param {string} dir - Base directory
 * @param {function} predicate - Returns true if file path should be included
 * @returns {string[]} - Array of absolute file paths
 */
function walk(dir, predicate) {
  const results = [];

  if (!fs.existsSync(dir)) {
    return results;
  }

  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...walk(fullPath, predicate));
    } else if (entry.isFile() && predicate(fullPath)) {
      results.push(fullPath);
    }
  }

  return results;
}

/**
 * Discover all Garura components under the target directory.
 *
 * Source layout (the default): plays/, loops/, skills/ and agents/ beside each other.
 * Installed layout: plays, loops and skills all in <target>/skills/<name>/SKILL.md and agents
 * in <target>/agents/*.md. There a SKILL.md that says `kind: loop` or carries the Shared Loop
 * Run anchor is a loop, one that carries the Standard Play Close anchor is a play, and the rest
 * are skills. The shared files sit in <target>/skills/_shared/.
 *
 * @param {string} targetDir - Absolute path to the components folder, or to .claude / .agents
 * @param {'source'|'installed'} [layout]
 * @returns {{
 *   skills: Array<{file: string, name: string, type: string}>,
 *   plays: Array<{file: string, name: string, type: string}>,
 *   agents: Array<{file: string, name: string, type: string}>,
 *   intents: Array<{file: string, name: string, type: string}>,
 *   loops: Array<{file: string, name: string, type: string}>
 * }}
 */
const PLAY_CLOSE = '# --- Standard Play Close (shared; see ../_shared/play-close.md) ---';
const LOOP_RUN = '# --- Shared Loop Run (shared; see ../_shared/loop-run.md) ---';

function discoverInstalled(targetDir) {
  const skills = [];
  const plays = [];
  const loops = [];
  const intents = [];
  const sharedDir = path.join(targetDir, 'skills', '_shared');
  const skillsDir = path.join(targetDir, 'skills');
  if (fs.existsSync(skillsDir)) {
    for (const entry of fs.readdirSync(skillsDir, { withFileTypes: true })) {
      if (!entry.isDirectory() || entry.name.startsWith('_')) continue;
      const file = path.join(skillsDir, entry.name, 'SKILL.md');
      if (!fs.existsSync(file)) continue;
      const text = fs.readFileSync(file, 'utf8');
      if (/^kind:\s*loop\s*$/m.test(text) || text.includes(LOOP_RUN)) {
        loops.push({ file, name: entry.name, type: 'loop', playsShared: sharedDir });
      } else if (text.includes(PLAY_CLOSE)) {
        plays.push({ file, name: entry.name, type: 'play' });
        const intentFile = path.join(skillsDir, entry.name, 'reference', 'intent.yaml');
        if (fs.existsSync(intentFile)) {
          const expectationFile = path.join(skillsDir, entry.name, 'reference', 'expectation.yaml');
          intents.push({
            file: intentFile,
            name: entry.name,
            type: 'intent',
            expectationFile: fs.existsSync(expectationFile) ? expectationFile : null,
          });
        }
      } else {
        skills.push({ file, name: entry.name, type: 'skill' });
      }
    }
  }
  const agents = [];
  const agentsDir = path.join(targetDir, 'agents');
  if (fs.existsSync(agentsDir)) {
    for (const entry of fs.readdirSync(agentsDir, { withFileTypes: true })) {
      if (entry.isFile() && entry.name.endsWith('.md')) {
        agents.push({ file: path.join(agentsDir, entry.name), name: entry.name.slice(0, -3), type: 'agent' });
      }
    }
  }
  return { skills, plays, agents, intents, loops };
}

function discover(targetDir, layout = 'source') {
  if (layout === 'installed') return discoverInstalled(targetDir);
  const skillsDir = path.join(targetDir, 'skills');
  const playsDir = path.join(targetDir, 'plays');
  const agentsDir = path.join(targetDir, 'agents');

  // skills: {target}/skills/*/SKILL.md (exactly one level deep)
  const skills = [];
  if (fs.existsSync(skillsDir)) {
    const skillDirs = fs.readdirSync(skillsDir, { withFileTypes: true });
    for (const entry of skillDirs) {
      if (entry.isDirectory()) {
        const skillFile = path.join(skillsDir, entry.name, 'SKILL.md');
        if (fs.existsSync(skillFile)) {
          skills.push({ file: skillFile, name: entry.name, type: 'skill' });
        }
      }
    }
  }

  // plays: {target}/plays/*/SKILL.md (exactly one level deep)
  const plays = [];
  const intents = [];
  if (fs.existsSync(playsDir)) {
    const playDirs = fs.readdirSync(playsDir, { withFileTypes: true });
    for (const entry of playDirs) {
      if (entry.isDirectory()) {
        const playFile = path.join(playsDir, entry.name, 'SKILL.md');
        if (fs.existsSync(playFile)) {
          plays.push({ file: playFile, name: entry.name, type: 'play' });
        }

        // intent.yaml: {target}/plays/*/reference/intent.yaml
        const intentFile = path.join(playsDir, entry.name, 'reference', 'intent.yaml');
        if (fs.existsSync(intentFile)) {
          // expectation.yaml (ICE): {target}/plays/*/reference/expectation.yaml
          // Present = play is ICE-migrated (scenarios + recovery live here, not in intent).
          const expectationFile = path.join(playsDir, entry.name, 'reference', 'expectation.yaml');
          intents.push({
            file: intentFile,
            name: entry.name,
            type: 'intent',
            expectationFile: fs.existsSync(expectationFile) ? expectationFile : null,
          });
        }
      }
    }
  }

  // agents: {target}/agents/*.md (one level, no subdirs)
  const agents = [];
  if (fs.existsSync(agentsDir)) {
    const agentEntries = fs.readdirSync(agentsDir, { withFileTypes: true });
    for (const entry of agentEntries) {
      if (entry.isFile() && entry.name.endsWith('.md')) {
        const agentName = entry.name.slice(0, -3); // strip .md
        agents.push({
          file: path.join(agentsDir, entry.name),
          name: agentName,
          type: 'agent',
        });
      }
    }
  }

  // loops: {target}/loops/*/SKILL.md — higher-order plays (ADR 029), own folder (#613)
  const loops = [];
  const drivesDir = path.join(targetDir, 'loops');
  if (fs.existsSync(drivesDir)) {
    for (const entry of fs.readdirSync(drivesDir, { withFileTypes: true })) {
      if (entry.isDirectory() && !entry.name.startsWith('_')) {
        const driveFile = path.join(drivesDir, entry.name, 'SKILL.md');
        if (fs.existsSync(driveFile)) {
          loops.push({ file: driveFile, name: entry.name, type: 'loop' });
        }
      }
    }
  }

  return { skills, plays, agents, intents, loops };
}

module.exports = discover;
