#!/usr/bin/env bash
set -euo pipefail

if ! command -v hugo >/dev/null 2>&1; then
  echo "Error: hugo is not installed or not available on PATH." >&2
  exit 1
fi

rm -rf public

hugo --minify

test -f public/index.html
test -f public/sitemap.xml
test -f public/robots.txt

if [ -e public/blog/_draft-template/index.html ]; then
  echo "Error: draft template output found at public/blog/_draft-template/index.html." >&2
  exit 1
fi

if find public -name '*_draft-template*' -print -quit | grep -q .; then
  echo "Error: draft template output found in public. Move templates outside Hugo content before building." >&2
  find public -name '*_draft-template*' >&2
  exit 1
fi

echo "Success: NewGames.ai Hugo site built and required public files exist."
