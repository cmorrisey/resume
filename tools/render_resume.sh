#!/usr/bin/env bash
# Render a resume HTML file to PDF and a PNG preview, then check page count and stray characters.
# Usage: tools/render_resume.sh resumes/Charles_Morrisey_Resume_<Company>.html
set -euo pipefail
html="$(realpath "$1")"
pdf="${html%.html}.pdf"
png="${html%.html}.preview.png"
chrome="$(ls /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1)"
timeout 60 "$chrome" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$pdf" "file://$html" >/dev/null 2>&1
pip show pymupdf >/dev/null 2>&1 || pip install -q pymupdf >/dev/null 2>&1
python3 - "$pdf" "$png" <<'EOF'
import sys, pymupdf
d = pymupdf.open(sys.argv[1])
d[0].get_pixmap(dpi=110).save(sys.argv[2])
odd = [c for c in d[0].get_text() if ord(c) > 0x2000 and c != "•"]
print(f"pages={len(d)} odd_chars={odd} preview={sys.argv[2]}")
if len(d) > 1:
    print("OVERFLOW onto page 2:\n" + d[1].get_text())
EOF
