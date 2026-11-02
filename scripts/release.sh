#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/release.sh VERSION [--yes]
# Tags vVERSION on main and publishes the GitHub release with the changelog
# section as notes and the README showcase images attached. The README embeds
# them from releases/latest/download/, so every release must carry them.

VERSION="${1:?usage: scripts/release.sh VERSION [--yes]}"
TAG="v$VERSION"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

fail() { echo "error: $*" >&2; exit 1; }

[ "$(git branch --show-current)" = main ] || fail "release from main"
[ -z "$(git status --porcelain)" ] || fail "working tree is not clean"
git fetch -q origin main
[ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] || fail "main is not in sync with origin/main"
git rev-parse -q --verify "refs/tags/$TAG" >/dev/null && fail "tag $TAG already exists"

PLUGIN_VERSION="$(node -p "require('./.claude-plugin/plugin.json').version")"
[ "$PLUGIN_VERSION" = "$VERSION" ] || fail ".claude-plugin/plugin.json says $PLUGIN_VERSION, not $VERSION"

NOTES="$(awk -v v="## $VERSION" '$0 == v {on=1; next} /^## / && on {exit} on' CHANGELOG.md)"
[ -n "${NOTES//[[:space:]]/}" ] || fail "CHANGELOG.md has no '## $VERSION' section"

node scripts/check.mjs

OUT="$REPO/dist/showcase-$TAG"
rm -rf "$OUT"
uv run -q --with python-docx --with pymupdf --with pillow scripts/render-showcase.py "$OUT"
ls "$OUT"/*.png

if [ "${2:-}" != "--yes" ]; then
  read -r -p "Publish $TAG with these images? [y/N] " answer
  [ "$answer" = y ] || fail "aborted"
fi

git tag -a "$TAG" -m "qstack $VERSION"
git push -q origin "$TAG"
printf '%s\n' "$NOTES" | gh release create "$TAG" --verify-tag --title "qstack $VERSION" --notes-file - "$OUT"/*.png
echo "released $TAG"
