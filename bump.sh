#!/usr/bin/env bash
# 最新の entertainment_lab_v{N}.html を index.html にコピーする
set -euo pipefail
cd "$(dirname "$0")"

LATEST=$(ls entertainment_lab_v*.html 2>/dev/null | sort -V | tail -1)
if [ -z "$LATEST" ]; then
  echo "No entertainment_lab_v*.html found" >&2
  exit 1
fi

cp "$LATEST" index.html
echo "Synced $LATEST -> index.html"
