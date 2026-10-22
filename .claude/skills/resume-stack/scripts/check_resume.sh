#!/usr/bin/env bash
# Build a tailored resume (or cover letter), convert it to PDF, and run the ATS checks.
# Usage: check_resume.sh <tailored-folder> [build-script, default build.py]
# Env:   PREVIEW_DIR  where to write the PNG preview (default /tmp; use the session scratchpad)
# Exit:  non-zero when the PDF is not exactly one page or contains an em dash.
set -euo pipefail
dir="$1"; script="${2:-build.py}"
cd "$dir"
docx=$(python3 "$script" | awk '/^wrote/{print $2}')
[ -n "$docx" ] || { echo "FAIL: $script did not print 'wrote <file>.docx'"; exit 1; }
soffice --headless --convert-to pdf "$docx" >/dev/null 2>&1
pdf="${docx%.docx}.pdf"
pages=$(pdfinfo "$pdf" | awk '/^Pages:/{print $2}')
text=$(pdftotext -layout "$pdf" -)
read -r em pua < <(printf '%s' "$text" | python3 -c 'import sys; t=sys.stdin.buffer.read().decode("utf-8","replace"); print(t.count("\u2014"), sum(0xE000 <= ord(c) <= 0xF8FF for c in t))')
words=$(printf '%s' "$text" | wc -w)
preview_dir="${PREVIEW_DIR:-/tmp}"
mkdir -p "$preview_dir"
pdftoppm -png -r 110 -f 1 -l 1 "$pdf" "$preview_dir/${docx%.docx}-preview"
echo "file:        $dir/$pdf"
echo "pages:       $pages"
echo "words:       $words"
echo "em dashes:   $em"
echo "junk glyphs: $pua (private-use bullets that parsers read as garbage)"
echo "preview:     $preview_dir/${docx%.docx}-preview-1.png"
status=0
[ "$pages" = "1" ] || { echo "FAIL: must be exactly one page"; status=1; }
[ "$em" = "0" ] || { echo "FAIL: remove em dashes"; status=1; }
[ "$pua" = "0" ] || { echo "FAIL: replace symbol-font bullets with a real bullet character"; status=1; }
[ $status = 0 ] && echo "PASS"
exit $status
