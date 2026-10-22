---
name: resume-stack
description: Champ (Charles) Morrisey's full job-application stack. Tailors his resume to a specific internship or job posting, runs the resume-ats-optimizer and resume-bullet-writer skills, builds an ATS-safe one-page DOCX and PDF named Charles_Morrisey_Company_Role, verifies it, commits it to the resume repo, and returns Workday-ready skills tags, keyword coverage, and a check-before-submit list. Also writes matching cover letters (with orwells-rules), Workday Work Experience copy-paste blocks, and coursework field text. Use this whenever Champ pastes a job or internship posting, a Workday/Handshake/careers link, or says anything like "tailor my resume," "apply to this," "same stack," "run the stack," "cover letter for this role," or "what skills do I enter," even if he does not name the skill.
---

# Resume Stack

One command, the whole application: tailored resume, checks, files, and the fields Champ has to paste into the portal. This skill captures the workflow refined across his MiniMed, Insmed, GDMS, L3Harris, Goldwater, and Stryker applications.

The goal is a resume that gets past the ATS **and** survives an interviewer asking "tell me more about that." Never trade the second for the first. A missing keyword costs a few points of match; an inflated claim can cost the offer.

## Where things live

- **Repo root** (e.g. `/home/user/resume`): `README.md` is the source of truth for every fact, number, and date. `tailored/<company>-<role>-<year>/` holds one folder per application with `build.py`, the DOCX, the PDF, and `NOTES.md`.
- **This skill:** `references/claim-rules.md` (how each fact may be worded, verified corrections, coursework and grades), `references/report-template.md` (final reply format), `scripts/check_resume.sh` (build, convert, verify), `assets/build_template.py` and `assets/cover_letter_template.py` (used only if no repo folder exists to copy).

If the repo is not available, ask Champ to upload his latest resume PDF and work from it plus `references/claim-rules.md`.

## Workflow

### 1. Load the companion skills

Invoke these with the Skill tool before writing anything, because they carry the ATS and bullet-writing method this stack is built on:
- `anthropic-skills:resume-ats-optimizer`
- `anthropic-skills:resume-bullet-writer`
- `writing-skills:orwells-rules`, only when writing prose (cover letter, essays, short-answer fields)

If one is not installed, continue; the steps below cover the essentials.

### 2. Read the facts and the posting

Read `README.md` and `references/claim-rules.md`. If the posting is a URL, fetch it; if fetching fails, search for the posting text and say what you could not verify.

Pull from the posting:
- **Gates:** GPA floor, class standing, graduation window, citizenship or clearance, enrollment after the internship, location and on-site/hybrid/field, travel, dates, deadline, how long it has been posted.
- **Keywords:** duties and qualifications, tools, soft skills, industry terms. Note which ones Champ truthfully has.
- **Role family**, which decides the starting point:

| Role family | Copy this build.py | What leads |
|---|---|---|
| R&D, design, mechanical, systems | `tailored/minimed-engineering-intern-2027` | Skills, then EMPOWER project, then experience |
| Quality engineering (manufacturing, defense) | `tailored/l3harris-quality-engineer-intern-2027` | Quality Windows first under Relevant Experience |
| Quality systems, process, documentation | `tailored/insmed-quality-systems-intern-2027` | Summary, data and SOP work |
| Manufacturing, defense, cleared roles | `tailored/gdms-manufacturing-engineering-intern-2027` | Summary with clearance and West Point |
| Research programs, REUs, fellowships | `tailored/goldwater-summer-research-internship-2027` | Research interests, coursework, projects |
| Regulatory affairs, compliance | `tailored/stryker-regulatory-affairs-intern-2027` | 503A/503B work, writing and speaking coursework |
| Sales, marketing, field roles | `tailored/stryker-ortho-sales-intern-2027` | Target account list, revenue, athletics |

### 3. Ask only if blocked

If something would materially change the resume and is not in the README or claim rules, ask up to 3 short questions with AskUserQuestion. Otherwise state the assumption in one line and keep going. Champ is often on a deadline.

### 4. Tailor the content

Work section by section, applying the bullet-writer method (strong verb, a number, a result, one or two lines):

- **Header:** always ends with "U.S. Citizen". Contact info in the body, never a Word header.
- **Summary:** two lines when the role is not obviously engineering or when a gate (clearance, citizenship, class standing) should be seen first. Put 5-8 of the posting's top keywords in it naturally.
- **Education:** "(Sophomore)" on the degree line when standing matters; GPA as 3.56/4.00; Relevant Coursework chosen for the role from claim-rules section 3.
- **Skills:** 4-5 labeled lines, each fitting on one line, using the posting's exact phrases where true. Keep labels short (about 18 characters max) or they overrun the tab stop.
- **Bullets:** rewrite in the posting's language, but only with facts that pass `references/claim-rules.md`. Reorder sections and bullets so the best match comes first. Section names stay standard (Summary, Education, Skills, Experience, Relevant Experience, Engineering Projects, Leadership and Service, Honors).
- **Fit to one page:** cut the least relevant content first (Chateau Noland, website bullet, solar expansion clause, tutoring) rather than shrinking the font. Body font stays 10.2-10.5 pt.
- **Dates:** "Mon YYYY - Mon YYYY" so portals fill From/To fields.

### 5. Build and verify

1. Create `tailored/<company>-<role>-<year>/` (lowercase, hyphens) and copy the chosen `build.py` into it.
2. Replace the content below the `# ---------- Header ----------` marker. Set the docstring and default output name to `Charles_Morrisey_<Company>_<Role>.docx` (underscores, company and role as a recruiter would say them).
3. Run `PREVIEW_DIR=<scratchpad> bash <skill>/scripts/check_resume.sh tailored/<folder>`. It builds the DOCX, converts it with LibreOffice, and fails on more than one page, any em dash, or a junk bullet glyph.
4. Open the preview PNG with Read and look at it. The script cannot see a skills label colliding with its text, an orphaned word on its own line, or a section header stranded at the bottom. Fix and rerun until it passes and looks clean.

### 6. Record it

- Write `NOTES.md` in the folder: posting name and ID, location and work mode, what to upload, the rebuild command, what changed versus the other versions, honest keyword gaps, and anything to confirm.
- Add a row to the README Version History. If Champ corrected a fact during this run, update the README (and `references/claim-rules.md` if it is a wording rule) so the next run gets it right.
- Commit with a clear message and push to the session's working branch, following the session's git instructions.

### 7. Deliver

Send the PDF and DOCX with SendUserFile (PDF is what he uploads). Then reply using `references/report-template.md`: lead line, numbered tailoring changes, ATS match with covered and not claimed, skills tags code block, check-before-submit list, where it was pushed.

### 8. Add-ons (when asked, or when the portal clearly needs them)

- **Cover letter:** load orwells-rules. Research current cover letter practice once per session if Champ asks for it. One page, 250-400 words, "Dear Hiring Manager" unless a name is known, four paragraphs: who he is plus the two or three strongest selling points for this role, the best-matching experience mapped to listed duties, supporting experience, then what he wants to learn there, availability, and the ask. No clichés ("passionate," "hit the ground running"). Copy the closest `cover_letter.py` (or `assets/cover_letter_template.py`), name it `..._Cover_Letter`, and run the check script with `cover_letter.py` as the second argument. Flag any sentence that states his feelings or a lesson so he can make it his own.
- **Workday experience fields, coursework fields, skills fields:** use the formats in `references/report-template.md`.
- **Essays and short answers:** if Champ uploads his essay playbook, follow it (story bank, voice, kill list, rubric). Remind him to retype drafts in his own words.

## Why these rules exist

- **One page, single column, real bullets, tab-stop dates, no tables or text boxes:** Workday and SuccessFactors autofill from parsed text. Tables scramble the reading order, and the old Microsoft Print to PDF bullets came through as junk glyphs.
- **Filename with company and role:** Champ asked for this so every upload is easy to tell apart.
- **No em dashes:** Champ's standing preference for anything written for him.
- **Honest "not claimed" list:** it turns keyword gaps into interview prep instead of liabilities, and it is how he keeps trust with recruiters who check.
