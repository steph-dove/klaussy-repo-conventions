#!/usr/bin/env bash
#
# Regenerate the committed example scans under examples/<name>/.
#
# Each example is a full scan of a real upstream repository. This script clones
# the latest upstream source, runs the scanner with every output format, and
# copies the generated artifacts into examples/<name>/. Because it tracks the
# latest upstream, regenerated diffs include upstream drift (new files,
# changelog entries, counts) in addition to changes from this codebase.
#
# Usage:  scripts/regen-examples.sh
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PYTHON="$REPO_ROOT/.venv/bin/python"
[ -x "$PYTHON" ] || PYTHON="python3"

# example name -> upstream git URL
EXAMPLES=(
  "httpx|https://github.com/encode/httpx"
  "fastapi|https://github.com/fastapi/fastapi"
)

# Files copied from a scanned repo into examples/<name>/.
ARTIFACTS=(
  "CLAUDE.md"
  ".conventions/conventions.raw.json"
  ".conventions/conventions.md"
  ".conventions/conventions-review.md"
  ".conventions/conventions.html"
  ".conventions/conventions.sarif"
)

for entry in "${EXAMPLES[@]}"; do
  name="${entry%%|*}"
  url="${entry##*|}"
  # Clone into the project root as <name>_repo so the scanned repo path is
  # stable across runs (matches how the original examples were produced).
  clone_dir="$REPO_ROOT/${name}_repo"
  dest="$REPO_ROOT/examples/$name"

  echo ">> Regenerating example: $name (from $url)"
  rm -rf "$clone_dir"
  git clone --depth 1 --quiet "$url" "$clone_dir"

  PYTHONPATH="$REPO_ROOT/src" "$PYTHON" -m conventions discover \
    -r "$clone_dir" \
    --format json,markdown,review,html,sarif \
    --claude \
    --quiet

  mkdir -p "$dest"
  for artifact in "${ARTIFACTS[@]}"; do
    src="$clone_dir/$artifact"
    if [ -f "$src" ]; then
      cp "$src" "$dest/$(basename "$artifact")"
    else
      echo "   WARNING: expected artifact missing: $artifact" >&2
    fi
  done

  # Refresh the full .claude agent bundle (repo map + path-scoped rule files).
  # Rebuilt from scratch so rules that are no longer generated are dropped,
  # keeping the bundle in sync with CLAUDE.md and the reports above.
  rm -rf "$dest/.claude"
  mkdir -p "$dest/.claude"
  if [ -f "$clone_dir/.claude/directory-map.md" ]; then
    cp "$clone_dir/.claude/directory-map.md" "$dest/.claude/directory-map.md"
  else
    echo "   WARNING: expected directory map missing" >&2
  fi
  if [ -d "$clone_dir/.claude/rules" ]; then
    cp -R "$clone_dir/.claude/rules" "$dest/.claude/rules"
  fi

  rm -rf "$clone_dir"
  echo "   wrote -> examples/$name/ (incl. .claude/ bundle)"
done

echo "Done. Review 'git diff examples/' to see the effect of code changes (plus upstream drift)."
