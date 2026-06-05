import path from 'node:path';
import { DEFAULT_CONFIG } from '@/lib/config';

export function resolveFlightDeckRepoPath(repoRoot: string, configuredRepoPath: string): string {
  // When repo.path is omitted, config falls back to process.cwd(), which is the
  // engine worktree in dev. Flight Deck should stay anchored to the configured
  // target repo root unless the user explicitly overrides repo.path.
  if (configuredRepoPath === DEFAULT_CONFIG.repo.path) {
    return repoRoot;
  }
  return path.isAbsolute(configuredRepoPath)
    ? configuredRepoPath
    : path.resolve(repoRoot, configuredRepoPath);
}
