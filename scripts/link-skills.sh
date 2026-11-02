#!/usr/bin/env bash
set -euo pipefail

# Dev-only: symlinks every skill outside deprecated/ into the local harness
# skill folders, so edits in this repo take effect without reinstalling.
# Re-run after adding, removing or renaming a skill.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")

for DEST in "${DESTS[@]}"; do
  # A destination that is itself a symlink into this repo would receive links
  # back into skills/, polluting the working copy.
  if [ -L "$DEST" ]; then
    case "$(readlink -f "$DEST")" in
      "$REPO"|"$REPO"/*)
        echo "error: $DEST is a symlink into this repo; remove it and re-run." >&2
        exit 1
        ;;
    esac
  fi
  mkdir -p "$DEST"
  while IFS= read -r -d '' skill_md; do
    src="$(dirname "$skill_md")"
    target="$DEST/$(basename "$src")"
    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "skip $target: a real folder exists there" >&2
      continue
    fi
    ln -sfn "$src" "$target"
    echo "linked $(basename "$src") -> $DEST"
  done < <(find "$REPO/skills" -name SKILL.md -not -path '*/deprecated/*' -print0)
done
