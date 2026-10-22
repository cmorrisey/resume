"""Build the Stryker Ortho Sales Intern (Summer 2027) resume as DOCX.

ATS / Workday notes:
- Single column, no tables, no text boxes, no header/footer. Contact info lives in the body.
- Right-aligned dates use a right tab stop, so text extracts as "Company<TAB>Date".
- Bullets are a literal U+2022 character in Times New Roman (not a Symbol-font glyph),
  so parsers read a real bullet instead of a private-use character.
- Dates are "Mon YYYY - Mon YYYY" so Workday can fill From/To fields.
"""
import sys
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

FONT = "Times New Roman"
BODY = Pt(10.4)
MARGIN = Inches(0.55)
RIGHT = Inches(8.5) - 2 * MARGIN
SKILL_TAB = Inches(1.3)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.left_margin = sec.right_margin = MARGIN
sec.top_margin = Inches(0.45)
sec.bottom_margin = Inches(0.4)

normal = doc.styles["Normal"]
normal.font.name = FONT
normal.font.size = BODY
normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.space_after = Pt(0)
normal.paragraph_format.line_spacing = 1.0

props = doc.core_properties
props.title = "Charles Morrisey Resume"
props.author = "Charles Morrisey"
props.subject = "Resume"
props.keywords = ""
props.comments = ""


def para(space_before=0, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    if align is not None:
        p.alignment = align
    return p


def run(p, text, bold=False, italic=False, size=None):
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    if size:
        r.font.size = size
    return r


def bottom_border(p):
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    b = OxmlElement("w:bottom")
    for k, v in {"w:val": "single", "w:sz": "6", "w:space": "1", "w:color": "000000"}.items():
        b.set(qn(k), v)
    bdr.append(b)
    pPr.append(bdr)


def heading(text):
    p = para(space_before=3)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    run(p, text, bold=True)
    bottom_border(p)


def left_right(left, right, bold=False, italic=False, space_before=0):
    p = para(space_before=space_before)
    p.paragraph_format.tab_stops.add_tab_stop(RIGHT, WD_TAB_ALIGNMENT.RIGHT)
    p.paragraph_format.keep_with_next = True
    run(p, left, bold=bold, italic=italic)
    run(p, "\t")
    run(p, right, bold=bold, italic=italic)


def entry(org, dates, role, location, space_before=1):
    left_right(org, dates, bold=True, space_before=space_before)
    left_right(role, location, italic=True)


def bullet(parts):
    """parts: str, or list of (text, bold) tuples."""
    p = para()
    pf = p.paragraph_format
    pf.left_indent = Inches(0.3)
    pf.first_line_indent = Inches(-0.15)
    pf.tab_stops.add_tab_stop(Inches(0.3))
    run(p, "•\t")
    if isinstance(parts, str):
        parts = [(parts, False)]
    for text, b in parts:
        run(p, text, bold=b)


def skill(label, value):
    p = para()
    pf = p.paragraph_format
    pf.left_indent = SKILL_TAB
    pf.first_line_indent = -SKILL_TAB
    pf.tab_stops.add_tab_stop(SKILL_TAB)
    run(p, label + ":", bold=True)
    run(p, "\t")
    run(p, value)


# ---------- Header ----------
p = para(align=WD_ALIGN_PARAGRAPH.CENTER)
run(p, "CHARLES MORRISEY", size=Pt(20))
p = para(align=WD_ALIGN_PARAGRAPH.CENTER)
run(p, "San Luis Obispo, CA | (626) 705-1471 | cmorrise@calpoly.edu | linkedin.com/in/charlesmorrisey | U.S. Citizen",
    size=Pt(10))

# ---------- Summary ----------
heading("SUMMARY")
p = para()
run(p, "Biomedical Engineering sophomore and Account Executive who built a 3,050-record target account list "
       "and founded a business that booked $14,280 across 40 jobs. Former West Point cadet with proven "
       "leadership, sales presentation, and interpersonal skills.")

# ---------- Education ----------
heading("EDUCATION")
left_right("California Polytechnic State University, San Luis Obispo", "Expected June 2029", bold=True)
left_right("Bachelor of Science in Biomedical Engineering (Sophomore)", "GPA: 3.56/4.00", italic=True)
p = para()
run(p, "Relevant Coursework: ", bold=True)
run(p, "Introduction to Mechanical Design in Biomedical Engineering, Engineering Design Communication "
       "(SolidWorks), Public Speaking, Writing Arguments")
entry("United States Military Academy at West Point", "Jun 2025 - Jan 2026", "Cadet", "West Point, NY")
bullet("Ranked 285 of 1,187 cadets (top 25%); earned Tactical Combat Casualty Care "
       "certification with a perfect written exam score.")

# ---------- Skills ----------
heading("SKILLS")
skill("Sales", "Prospecting; target account lists; lead scoring; client onboarding; sales presentations; "
      "cost estimates")
skill("Marketing", "Market segmentation; outbound email campaigns; website launch; fundraising pitches")
skill("Software", "Microsoft Excel, Word, and PowerPoint; Google Places API; data cleaning and validation")
skill("Hands-On", "Equipment operation and safety training; quality inspection; SolidWorks through ME 228")

# ---------- Experience ----------
heading("EXPERIENCE")
entry("MeldMD", "Aug 2026 - Present", "Account Executive", "Remote / On-Site", space_before=0)
bullet("Onboard medical spas and clinics to 503A and 503B compounding pharmacy partners, guiding accounts "
       "through the sales cycle on product quality and pricing.")
bullet("Built a 3,050-record target account list covering 19 states and 348 cities using the Google "
       "Places API.")
bullet("Cleaned and de-duplicated two source datasets, verified phone contacts for 98% of records, and "
       "scored each lead by segment and product fit to prioritize outreach.")
bullet("Built an outbound email campaign system on the validated list to run structured prospecting at scale.")

entry("Coastal Shine", "Mar 2026 - Present", "Founder and Operator", "San Luis Obispo, CA")
bullet("Founded and run an exterior cleaning business while enrolled full time; booked $14,280 across 40 "
       "jobs for 40 clients ($357 average job value) through direct sales.")
bullet("Grew from 3 jobs in the first month to 30 jobs over a two-month peak while managing sales, "
       "scheduling, and service delivery; expanded into solar panel cleaning and roof soft washing.")
bullet("Built and launched gocoastalshine.com with service pages, before-and-after photos, a service-area "
       "map, and a quote form to generate leads.")

entry("Quality Windows", "Jun 2023 - Aug 2025", "Quality Control Supervisor (Summers)", "San Luis Obispo, CA")
bullet("Inspected 30+ residential and commercial properties per season; documented nonconformities and "
       "directed corrective rework before client sign-off.")
bullet("Trained 3 employees on safety procedures, equipment operation, and client communication.")

# ---------- Projects ----------
heading("MEDICAL DEVICE PROJECTS")
entry("EMPOWER Student Association, Cal Poly", "Fall 2026 - Present",
      "Marketing and Fundraising Lead | NICU Temperature Probe Adhesive", "San Luis Obispo, CA", space_before=0)
bullet("Lead marketing and fundraising for a student team developing a layered adhesive that keeps "
       "temperature probes on premature infants while reducing skin injury.")

# ---------- Leadership ----------
heading("LEADERSHIP AND SERVICE")
bullet([("Associated Student Body President", True), (", Mission College Prep (2024 - 2025). Elected "
        "to represent 350+ students before faculty and administrators.", False)])
bullet([("Varsity Football Captain", True), (", Mission College Prep. Named 1st Team All-League.", False)])
bullet([("STEM Tutor", True), (", Skill Haven (Apr. 2026 - Present). Teach math to seventh- "
        "and eighth-grade students through 20+ sessions.", False)])
bullet([("Youth Basketball Coach", True), (", 3Ball SLO (2025). Coached athletes ages 7-13 through "
        "25+ hours of free community programming.", False)])

# ---------- Honors ----------
heading("HONORS")
bullet([("CIF Central Section Scholar-Athlete of the Year", True), (", 2025. Selected from 120+ member "
        "schools.", False)])
bullet([("Sttark Essay and Label Design Scholarship", True), (", 2026. National winner; awarded $3,000 "
        "for an original essay and label design.", False)])
bullet([("Dean's List", True), (", California Polytechnic State University, Spring 2026.", False)])

out = sys.argv[1] if len(sys.argv) > 1 else "Charles_Morrisey_Stryker_Ortho_Sales_Intern.docx"
doc.save(out)
print("wrote", out)
