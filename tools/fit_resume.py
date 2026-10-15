#!/usr/bin/env python3
"""Scale a resume's font and spacing so it fills exactly one page.

Usage: python3 tools/fit_resume.py resumes/Charles_Morrisey_Resume_<Company>.html

Inserts (or replaces) a <style id="fit"> block. The body font grows (10pt up to
11pt) only while no line wraps onto a new line; then line and section spacing
grow until the last line of text sits just above the bottom margin.
"""
import re, subprocess, sys
import pymupdf

PAGE_H, BOTTOM_MARGIN = 792.0, 0.4 * 72      # Letter, matches @page margin
TARGET = PAGE_H - BOTTOM_MARGIN               # last text line should end here
SLACK = 6.0                                   # pt of breathing room we accept

html_path = sys.argv[1]
pdf_path = html_path[:-5] + ".pdf"
src = re.sub(r'\n?<style id="fit">.*?</style>\n?', "", open(html_path).read(), flags=re.S)
assert src.count("</head>") == 1


def css(fs, t):
    """fs = body font size in pt; t in [0, 1] = how much extra spacing."""
    k = fs / 10.0
    return (f'<style id="fit">\n'
            f'body {{ font-size: {fs:.2f}pt; line-height: {1.12 + 0.18 * t:.3f}; }}\n'
            f'h1 {{ font-size: {19 * k:.2f}pt; }}\n'
            f'.contact {{ font-size: {9 * k:.2f}pt; margin: {1 + 2 * t:.2f}pt 0 {3 + 3 * t:.2f}pt; }}\n'
            f'h2 {{ font-size: {fs:.2f}pt; margin: {4 + 6 * t:.2f}pt 0 {2 + 2 * t:.2f}pt; }}\n'
            f'li {{ margin-bottom: {1.2 * t:.2f}pt; }}\n'
            f'.skills {{ grid-template-columns: {82 * k:.1f}pt 1fr; }}\n'
            f'</style>\n')


def render(fs, t):
    open(html_path, "w").write(src.replace("</head>", "\n" + css(fs, t) + "</head>", 1))
    subprocess.run(["bash", "tools/render_resume.sh", html_path], check=True, capture_output=True)
    d = pymupdf.open(pdf_path)
    bottom = max(b[3] for b in d[0].get_text("blocks"))
    lines = sum(len(b["lines"]) for b in d[0].get_text("dict")["blocks"] if "lines" in b)
    return len(d), bottom, lines


def fits(fs, t):
    pages, bottom, _ = render(fs, t)
    return pages == 1 and bottom <= TARGET


# 1) Largest font size (0.1pt steps, 10.0 to 11.0) that adds no wrapped lines and still fits.
fs = 10.0
base_lines = render(fs, 0.0)[2]
for step in [x / 10 for x in range(101, 111)]:
    pages, bottom, lines = render(step, 0.0)
    if pages == 1 and bottom <= TARGET and lines == base_lines:
        fs = step
    else:
        break

# 2) Binary-search extra spacing at that font size.
lo, hi = 0.0, 2.0
if fits(fs, hi):
    lo = hi
else:
    for _ in range(8):
        mid = (lo + hi) / 2
        if fits(fs, mid):
            lo = mid
        else:
            hi = mid

pages, bottom, _ = render(fs, lo)
print(f"font={fs:.1f}pt spacing={lo:.2f} pages={pages} "
      f"bottom={bottom:.0f}pt of {TARGET:.0f}pt (gap {TARGET - bottom:.0f}pt)")
if pages != 1 or bottom > TARGET:
    sys.exit("could not fit on one page")
if TARGET - bottom > SLACK:
    print("note: page still not full; content is short, consider adding a line")
