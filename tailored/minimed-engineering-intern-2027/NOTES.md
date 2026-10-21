# MiniMed Engineering Intern, Summer 2027 (R-801818)

Deadline: Oct 22, 2026. Upload `Charles_Morrisey_Resume.pdf` to Workday.
Rebuild after edits: `python3 build.py Charles_Morrisey_Resume.docx && soffice --headless --convert-to pdf Charles_Morrisey_Resume.docx`

## What changed vs. the master resume
- Header: added "U.S. Citizen" so the work-authorization requirement is explicit (posting says the resume must clearly show each requirement).
- Dates normalized to "Mon YYYY - Mon YYYY" so Workday fills From/To fields. "Summers 2023 - 2025" became "Jun 2023 - Aug 2025" with "(Summers)" in the title; "Summer 2023" became "Jun 2023 - Aug 2023"; "Fall 2026" became "Sep 2026 - Present". Months are assumed; correct if wrong.
- Bullets are a real "•" character. The old Microsoft Print-to-PDF file exported bullets as a private-use glyph (U+F0B7) that parsers read as junk.
- No tables, text boxes, or header/footer; dates use right tab stops. Text extracts in reading order.
- Skills retuned to posting keywords (design requirements, design for manufacturability, prototype testing, nonconformance documentation, technical writing, data analysis). One line per category.
- EMPOWER bullets framed as user needs -> design requirements -> prototype testing (design-controls language MiniMed R&D uses).
- GPA shown as 3.56/4.00.

## Keyword gaps (add only if true)
MATLAB, Python, C/C++, Minitab, Arduino/Raspberry Pi, LabVIEW, statistics. Any of these would go on the "Data and Software" line.
