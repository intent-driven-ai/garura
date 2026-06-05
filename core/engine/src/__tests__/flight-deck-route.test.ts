import { describe, expect, it } from 'vitest';
import { DEFAULT_CONFIG } from '@/lib/config';
import { resolveFlightDeckRepoPath } from '@/lib/flight-deck-paths';

describe('resolveFlightDeckRepoPath', () => {
  it('prefers the resolved target repo root when repo.path is only the default cwd placeholder', () => {
    const repoRoot = '/repos/production-garura';
    const result = resolveFlightDeckRepoPath(repoRoot, DEFAULT_CONFIG.repo.path);
    expect(result).toBe(repoRoot);
  });

  it('resolves explicit relative repo.path values against the target repo root', () => {
    const result = resolveFlightDeckRepoPath('/repos/production-garura', './subrepo');
    expect(result).toBe('/repos/production-garura/subrepo');
  });

  it('preserves explicit absolute repo.path overrides', () => {
    const result = resolveFlightDeckRepoPath('/repos/production-garura', '/tmp/alternate-repo');
    expect(result).toBe('/tmp/alternate-repo');
  });
});
