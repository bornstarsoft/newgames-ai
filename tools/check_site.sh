#!/usr/bin/env bash
set -euo pipefail

if ! command -v hugo >/dev/null 2>&1; then
  echo "Error: hugo is not installed or not available on PATH." >&2
  exit 1
fi

rm -rf public

hugo --minify

test -f public/index.html
test -f public/404.html
test -f public/sitemap.xml
test -f public/robots.txt
test -f public/_redirects

if ! grep -q '^/blog/_draft-template/' public/_redirects; then
  echo "Error: public/_redirects is missing the draft template 404 guard." >&2
  exit 1
fi

if [ -e public/blog/_draft-template/index.html ]; then
  echo "Error: draft template output found at public/blog/_draft-template/index.html." >&2
  exit 1
fi

draft_template_outputs="$(find public -path public/_redirects -prune -o -name '*_draft-template*' -print)"
if [ -n "$draft_template_outputs" ]; then
  echo "Error: draft template output found in public outside _redirects." >&2
  printf '%s\n' "$draft_template_outputs" >&2
  exit 1
fi

echo "Success: NewGames.ai Hugo site built and required public files exist."
