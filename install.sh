#!/usr/bin/env bash
# Install skills into an agent skills directory.
set -euo pipefail
usage() { echo "Usage: $0 [--claude|--codex|--agents] [--dest DIR]"; exit 1; }
DEST=""
case "${1:-}" in
  --claude) DEST="$HOME/.claude/skills" ;;
  --codex)  DEST="$HOME/.codex/skills" ;;
  --agents) DEST="$HOME/.agents/skills" ;;
  --dest)   DEST="${2:-}"; [ -n "$DEST" ] || usage ;;
  *) usage ;;
esac
SRC="$(cd "$(dirname "$0")" && pwd)/skills"
mkdir -p "$DEST"
for d in "$SRC"/*/; do
  n="$(basename "$d")"
  rm -rf "${DEST:?}/$n"; cp -R "$d" "$DEST/$n"; echo "installed $n -> $DEST/$n"
done
