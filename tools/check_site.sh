#!/usr/bin/env bash
set -euo pipefail

if ! command -v hugo >/dev/null 2>&1; then
  echo "Error: hugo is not installed or not available on PATH." >&2
  exit 1
fi

hugo --minify

test -f public/index.html
test -f public/sitemap.xml
test -f public/robots.txt

echo "Success: NewGames.ai Hugo site built and required public files exist."
