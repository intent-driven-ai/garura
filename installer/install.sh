#!/usr/bin/env bash
set -euo pipefail

# Garura Installer
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/intent-driven-ai/garura/main/installer/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/intent-driven-ai/garura/main/installer/install.sh | bash -s -- --project-name my-app
#   curl -fsSL https://raw.githubusercontent.com/intent-driven-ai/garura/main/installer/install.sh | bash -s -- --version v3.0.0
#   curl -fsSL https://raw.githubusercontent.com/intent-driven-ai/garura/main/installer/install.sh | bash -s -- --version main
#
# --version <tag>   install a published release, e.g. v3.0.0
# --version main    install the newest work on main (unreleased)
# (no --version)    install the latest published release

REPO="intent-driven-ai/garura"
# Skills that must not be deployed into target projects (space-separated).
# Deployment is handled by the sudarshan /sud:install meta-play.
EXCLUDED_SKILLS=""

# --- Helpers ---

info()  { printf '\033[1;34m[garura]\033[0m %s\n' "$1"; }
ok()    { printf '\033[1;32m[garura]\033[0m %s\n' "$1"; }
warn()  { printf '\033[1;33m[garura]\033[0m %s\n' "$1"; }
err()   { printf '\033[1;31m[garura]\033[0m %s\n' "$1" >&2; }

cleanup() {
  if [ -n "${TMPDIR_WORK:-}" ] && [ -d "$TMPDIR_WORK" ]; then
    rm -rf "$TMPDIR_WORK"
  fi
}
trap cleanup EXIT

# --- Parse arguments ---

PROJECT_NAME=""
VERSION=""
TARGET_DIR="$(pwd)"

while [ $# -gt 0 ]; do
  case "$1" in
    --project-name)
      shift
      PROJECT_NAME="${1:-}"
      if [ -z "$PROJECT_NAME" ]; then
        err "--project-name requires a value"
        exit 1
      fi
      ;;
    --version)
      shift
      VERSION="${1:-}"
      if [ -z "$VERSION" ]; then
        err "--version requires a value (a release tag such as v3.0.0, or main)"
        exit 1
      fi
      ;;
    *)
      err "Unknown option: $1"
      exit 1
      ;;
  esac
  shift
done

if [ -z "$PROJECT_NAME" ]; then
  PROJECT_NAME="$(basename "$TARGET_DIR")"
fi

# --- Detect mode ---

GARURA_CONFIG="$TARGET_DIR/.garura/core/config.yaml"
VERSION_FILE="$TARGET_DIR/.garura/core/garura-version"
MODE="init"
if [ -f "$GARURA_CONFIG" ]; then
  MODE="upgrade"
fi

# --- Resolve the version to install ---

if [ -z "$VERSION" ]; then
  info "Finding the latest Garura release..."
  VERSION="$(curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" 2>/dev/null \
    | python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"])' 2>/dev/null || true)"
  if [ -z "$VERSION" ]; then
    err "Could not find the latest Garura release on GitHub."
    err "Try again, or name a version: --version v3.0.0 (or --version main for unreleased work)."
    exit 1
  fi
fi

if [ "$VERSION" = "main" ]; then
  ARCHIVE_URL="https://github.com/$REPO/archive/refs/heads/main.tar.gz"
  MAIN_SHA="$(curl -fsSL "https://api.github.com/repos/$REPO/commits/main" 2>/dev/null \
    | python3 -c 'import json,sys; print(json.load(sys.stdin)["sha"][:8])' 2>/dev/null || true)"
  INSTALLED_VERSION="main${MAIN_SHA:+@$MAIN_SHA}"
else
  ARCHIVE_URL="https://github.com/$REPO/archive/refs/tags/$VERSION.tar.gz"
  INSTALLED_VERSION="$VERSION"
fi

# --- Download repo archive ---

info "Downloading Garura $INSTALLED_VERSION from GitHub..."
TMPDIR_WORK="$(mktemp -d)"

if ! curl -fsSL "$ARCHIVE_URL" -o "$TMPDIR_WORK/garura.tar.gz"; then
  err "Garura version '$VERSION' was not found."
  err "See the published releases: https://github.com/$REPO/releases"
  exit 1
fi
tar xzf "$TMPDIR_WORK/garura.tar.gz" -C "$TMPDIR_WORK"

# The archive holds one top-level folder (garura-main, garura-3.0.0, ...)
SRC_DIR="$(find "$TMPDIR_WORK" -mindepth 1 -maxdepth 1 -type d | head -1)"

if [ -z "$SRC_DIR" ] || [ ! -d "$SRC_DIR/core" ]; then
  err "Downloaded archive does not contain core/ directory. Something went wrong."
  exit 1
fi

COMPONENTS_DIR="$SRC_DIR/core/components"

# --- Utility functions ---

copy_dir() {
  local src="$1" dest="$2"
  mkdir -p "$dest"
  cp -R "$src"/* "$dest"/ 2>/dev/null || true
}

# --- Transform config.yaml ---

transform_config() {
  local content="$1" name="$2"
  echo "$content" \
    | sed -E "s/^([[:space:]]*name:[[:space:]]*).+$/\1$name/" \
    | sed -E "s/^([[:space:]]*type:[[:space:]]*).+$/\1Project/" \
    | sed -E "s|^([[:space:]]*skills:[[:space:]]*).+$|\1./.claude/skills/|" \
    | sed -E "s|^([[:space:]]*plays:[[:space:]]*).+$|\1./.claude/skills/|" \
    | sed -E "s|^([[:space:]]*agents:[[:space:]]*).+$|\1./.claude/agents/|" \
    | sed -E "s|^([[:space:]]*memory:[[:space:]]*).+$|\1~/.garura/core/memory/|" \
    | sed -E '/^platform:/d' \
    | sed -E '/^github:/,/^[^ ]/{ /^github:/d; /^  /d; }' \
    | sed -E '/^$/N;/^\n$/d'
}

# --- Transform CLAUDE.md ---

transform_claude_md() {
  local content="$1" name="$2"

  # Use a temp file for multi-step sed transforms
  local tmpfile
  tmpfile="$(mktemp)"
  echo "$content" > "$tmpfile"

  # Update title
  sed -i.bak -E "s/^# CLAUDE\.md$/# CLAUDE.md — $name/" "$tmpfile"

  # Replace architecture diagram block
  python3 -c "
import re, sys
with open('$tmpfile', 'r') as f:
    text = f.read()

new_diagram = '''\`\`\`
.claude/                   # AI components (managed by Garura)
\u251c\u2500\u2500 agents/               # Agent definitions
\u2514\u2500\u2500 skills/               # Skills + plays

.garura/
\u251c\u2500\u2500 core/
\u2502   \u251c\u2500\u2500 memory/           # LTM: practices, templates, standards
\u2502   \u2514\u2500\u2500 config.yaml       # Project configuration
\u2514\u2500\u2500 project/              # STM: checkpoints, specs
    \u2514\u2500\u2500 specs/
\`\`\`'''

text = re.sub(r'\`\`\`\ncore/components/.*?\`\`\`', new_diagram, text, flags=re.DOTALL)

# Remove Source of Truth section
text = re.sub(r'### 1\. Source of Truth[\s\S]*?(?=### 2\. Execution Model)', '', text)

# Remove deploy-command reference (deployment handled by /sud:install)
text = re.sub(r'After editing source, run \`/sud:install\`\.\n*', '', text)

# Update config path references
text = text.replace('\`.garura/core/config.yaml\`', '\`.garura/core/config.yaml\`')

# Remove doc references
text = re.sub(r'- \`docs/.*\n', '', text)

# Collapse multiple blank lines
text = re.sub(r'\n{3,}', '\n\n', text)

with open('$tmpfile', 'w') as f:
    f.write(text)
" 2>/dev/null

  cat "$tmpfile"
  rm -f "$tmpfile" "$tmpfile.bak"
}

# --- Deploy skills (honoring EXCLUDED_SKILLS) ---

deploy_skills() {
  local src="$1" dest="$2"
  mkdir -p "$dest"
  for skill_dir in "$src"/*/; do
    local skill_name
    skill_name="$(basename "$skill_dir")"
    # Skip excluded skills
    if echo "$EXCLUDED_SKILLS" | grep -qw "$skill_name"; then
      continue
    fi
    copy_dir "$skill_dir" "$dest/$skill_name"
  done
}

# ===================================================================
# INIT MODE — Fresh installation
# ===================================================================

if [ "$MODE" = "init" ]; then
  info "Initializing Garura $INSTALLED_VERSION in $TARGET_DIR..."
  info "  Project name: $PROJECT_NAME"

  # 1. Deploy agents
  if [ -d "$COMPONENTS_DIR/agents" ]; then
    info "  Deploying agents..."
    copy_dir "$COMPONENTS_DIR/agents" "$TARGET_DIR/.claude/agents"
  fi

  # 2. Deploy skills (honoring EXCLUDED_SKILLS)
  if [ -d "$COMPONENTS_DIR/skills" ]; then
    info "  Deploying skills..."
    deploy_skills "$COMPONENTS_DIR/skills" "$TARGET_DIR/.claude/skills"
  fi

  # 3. Deploy plays → .claude/skills/
  if [ -d "$COMPONENTS_DIR/plays" ]; then
    info "  Deploying plays..."
    for play_dir in "$COMPONENTS_DIR/plays"/*/; do
      local_name="$(basename "$play_dir")"
      copy_dir "$play_dir" "$TARGET_DIR/.claude/skills/$local_name"
    done
  fi

  # 4. Deploy memory
  if [ -d "$COMPONENTS_DIR/memory" ]; then
    info "  Deploying memory..."
    copy_dir "$COMPONENTS_DIR/memory" "$HOME/.garura/core/memory"
  fi

  # 5. Transform and write config.yaml
  if [ -f "$SRC_DIR/.garura/core/config.yaml" ]; then
    info "  Writing config..."
    mkdir -p "$TARGET_DIR/.garura/core"
    config_content="$(cat "$SRC_DIR/.garura/core/config.yaml")"
    transform_config "$config_content" "$PROJECT_NAME" > "$TARGET_DIR/.garura/core/config.yaml"
  fi

  # 6. Create project directories
  info "  Creating project structure..."
  mkdir -p "$TARGET_DIR/.garura/project/specs"
  mkdir -p "$TARGET_DIR/src"

  # 7. Transform and write CLAUDE.md
  if [ -f "$SRC_DIR/CLAUDE.md" ]; then
    info "  Writing CLAUDE.md..."
    claude_content="$(cat "$SRC_DIR/CLAUDE.md")"
    transform_claude_md "$claude_content" "$PROJECT_NAME" > "$TARGET_DIR/CLAUDE.md"
  fi

  # 8. Record the installed version
  mkdir -p "$(dirname "$VERSION_FILE")"
  echo "$INSTALLED_VERSION" > "$VERSION_FILE"

  ok ""
  ok "Garura $INSTALLED_VERSION initialized successfully!"
  ok ""
  ok "Project structure created:"
  ok "  .claude/agents/      — Agent definitions"
  ok "  .claude/skills/      — Skills and plays"
  ok "  .garura/core/    — Memory and config"
  ok "  .garura/project/ — Project artifacts"
  ok "  src/                 — Source code"
  ok "  CLAUDE.md            — AI instructions"
  ok "  .garura/core/garura-version — the installed Garura version"
  ok ""
  ok "Next steps:"
  ok "  1. Review and customize CLAUDE.md for your project"
  ok "  2. Update .garura/core/config.yaml with your repo details"
  ok "  3. Start developing with Claude Code!"

# ===================================================================
# UPGRADE MODE — Non-destructive update
# ===================================================================

else
  PREVIOUS_VERSION="unknown (installed before versions were recorded)"
  if [ -f "$VERSION_FILE" ]; then
    PREVIOUS_VERSION="$(cat "$VERSION_FILE")"
  fi
  info "Upgrading Garura in $TARGET_DIR..."
  info "  Existing installation detected."
  info "  From: $PREVIOUS_VERSION"
  info "  To:   $INSTALLED_VERSION"

  # 1. Upgrade agents (overwrite managed files)
  if [ -d "$COMPONENTS_DIR/agents" ]; then
    info "  Upgrading agents..."
    copy_dir "$COMPONENTS_DIR/agents" "$TARGET_DIR/.claude/agents"
  fi

  # 2. Upgrade skills (overwrite managed, honoring EXCLUDED_SKILLS)
  if [ -d "$COMPONENTS_DIR/skills" ]; then
    info "  Upgrading skills..."
    deploy_skills "$COMPONENTS_DIR/skills" "$TARGET_DIR/.claude/skills"
  fi

  # 3. Upgrade plays
  if [ -d "$COMPONENTS_DIR/plays" ]; then
    info "  Upgrading plays..."
    for play_dir in "$COMPONENTS_DIR/plays"/*/; do
      local_name="$(basename "$play_dir")"
      copy_dir "$play_dir" "$TARGET_DIR/.claude/skills/$local_name"
    done
  fi

  # 4. Upgrade memory
  if [ -d "$COMPONENTS_DIR/memory" ]; then
    info "  Upgrading memory..."
    copy_dir "$COMPONENTS_DIR/memory" "$HOME/.garura/core/memory"
  fi

  # 5. Write config.yaml.new for user to diff/merge
  if [ -f "$SRC_DIR/.garura/core/config.yaml" ]; then
    info "  Writing config.yaml.new (review and merge manually)..."
    config_content="$(cat "$SRC_DIR/.garura/core/config.yaml")"
    transform_config "$config_content" "$PROJECT_NAME" > "$TARGET_DIR/.garura/core/config.yaml.new"
  fi

  # 6. Write CLAUDE.md.new for user to diff/merge
  if [ -f "$SRC_DIR/CLAUDE.md" ]; then
    info "  Writing CLAUDE.md.new (review and merge manually)..."
    claude_content="$(cat "$SRC_DIR/CLAUDE.md")"
    transform_claude_md "$claude_content" "$PROJECT_NAME" > "$TARGET_DIR/CLAUDE.md.new"
  fi

  # 7. Record the installed version
  echo "$INSTALLED_VERSION" > "$VERSION_FILE"

  ok ""
  ok "Garura upgraded successfully: $PREVIOUS_VERSION -> $INSTALLED_VERSION"
  ok ""
  ok "Updated (overwritten):"
  ok "  .claude/agents/              — Agent definitions"
  ok "  .claude/skills/              — Skills and plays"
  ok "  ~/.garura/core/memory/   — Memory (practices, templates)"
  ok ""
  ok "Review these files for changes:"
  ok "  .garura/core/config.yaml.new  — diff with config.yaml"
  ok "  CLAUDE.md.new                     — diff with CLAUDE.md"
  ok ""
  ok "Preserved (not touched):"
  ok "  .garura/project/     — Your project artifacts"
  ok "  .garura/core/config.yaml — Your config"
  ok "  CLAUDE.md                — Your AI instructions"
  ok "  .claude/settings.json    — Your Claude settings"
fi
