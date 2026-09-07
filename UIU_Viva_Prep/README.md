# Bismillah.

## Separate seniors' workbook-only companion

[Workbook topics PDF](UIU_Seniors_Workbook_Topics_Explained.pdf) and
[its Markdown](UIU_Seniors_Workbook_Topics_Explained.md) select existing
explanations for Excel topics within UIU-listed courses, including **AI and ML**.
Standalone networking, security, hardware, graphics, TOC and personal research
chapters are excluded; SQL injection remains as a database topic. This companion
does not replace the full demo-and-interview reference below.

From the workspace root:

```powershell
python .\BRACU_Viva_Prep\build\assemble_workbook_topics.py
powershell -ExecutionPolicy Bypass -File .\BRACU_Viva_Prep\build\build_workbook_topics_pdf.ps1 -Pack UIU
```

# UIU CSE Lecturer Demo and Interview Preparation

This pack follows the selection email supplied by Ahmmad Nur Swapnil. The
session is **September 14, 2026, reporting at 1:30 PM, candidate waiting room
408**, at UIU's United City campus, Madani Avenue, Badda, Dhaka. The email labels
it **Demo Session D**; this is a session label, not your assigned teaching topic.

The session consists of a 30-second–1-minute introduction, a **randomly assigned
4–5 minute marker-and-whiteboard class**, and 4–5 minutes of questions related
to that class. This differs from preparing one fixed slide presentation.

## What was copied

The ten subject files below are complete, byte-for-byte copies of the existing
`BRACU_Viva_Prep` notes. Their detailed explanations, source mappings, equations,
code, examples, and diagrams were retained. This is a selection and PDF rebuild
of those notes, not a claim of another fresh reading of all academic slides.
They now include the September 2026 seniors' workbook corrections and worked
supplements. All 15 workbook tabs and 17 embedded images were inspected; the
full mapping is in `20_SENIORS_WORKBOOK_COVERAGE_AUDIT.md`.

Original filenames/numbers are retained for traceability; gaps are intentional.

| UIU email domain | Included detailed notes | Original academic routing |
|---|---|---|
| Structured Programming Language | `04_C_PROGRAMMING_SLIDE_COMPLETE.md` | `101-CP` |
| Object-Oriented Programming | `03_OOP_CPP_JAVA_SLIDE_COMPLETE.md` | `107-OOP` |
| Discrete Mathematics | `10_DISCRETE_MATHEMATICS_SLIDE_COMPLETE.md` | `103-DM`, selected counting/probability connections |
| Data Structures | `01_DSA_I_SLIDE_COMPLETE.md`, relevant parts of volume 02 | `203-DSA1`, `207-DSA2` |
| Algorithms | `02_DSA_II_SLIDE_COMPLETE.md`, foundations in volume 01 | `207-DSA2`, selected `461-AE` |
| Database Management Systems | `05_DBMS_SLIDE_COMPLETE.md` | `215-DBMS` |
| Software Engineering | `08_SOFTWARE_ENGINEERING_SLIDE_COMPLETE.md` | `307-SWE`, `325-ISD` |
| Operating Systems | `06_OPERATING_SYSTEMS_SLIDE_COMPLETE.md` | `313-OS` |
| Artificial Intelligence, including ML as requested | `09_ARTIFICIAL_INTELLIGENCE_SLIDE_COMPLETE.md` **and** `11_MACHINE_LEARNING_SLIDE_COMPLETE.md` | `317-AI`, `471-ML` and its notebook |

Start with `00_UIU_DEMO_AND_QA_GUIDE.md` for an introduction based on the current
`My_Resume/main.tex`, a reusable whiteboard structure, worked mini-lessons,
follow-up questions, and rehearsal priorities. `19_UIU_RELEVANT_COMMON_INTERVIEW_QA.md`
contains the relevant complete chapters selected from the existing question bank.
`17_THESIS_RESEARCH_INDUSTRY_COMPLETE.md` is also copied after checking personal
facts against the current résumé. It supplies research and industry follow-ups
for the **interview**, with detailed projects kept secondary and unknown private
manuscript details explicitly marked rather than invented.

Standalone networking, security, graphics, hardware/DLD/micro, TOC/compiler,
and numerical-methods volumes are not included because the supplied email does
not list them. Related material already inside the copied books is retained:
for example, P/NP in algorithms and memory hierarchy where needed by OS.

Your older UIU PDFs and archived notes are preserved. The active BRACU Markdown
books were updated where the workbook revealed gaps; the updated relevant files
were then recopied here. The older UIU PDFs
are not inputs to this new combined book. Personal facts in older BRACU notes
are not substituted for the current résumé in the new introduction.

## Combined PDF and rebuilding

Output: `UIU_CSE_Demo_and_Interview_Preparation_Ahmmad_Nur_Swapnil.pdf`.

It uses the same comfortable charcoal theme as the BRACU book: `#2b2e34`
background, off-white text, muted blue headings, rendered Mermaid diagrams,
MathML equations, searchable text, contents, and PDF bookmarks.

From the workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File .\UIU_Viva_Prep\build\build_viva_pdf.ps1
```

From this folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\build\build_viva_pdf.ps1
```

Requirements match the BRACU build: Pandoc, Python with PyMuPDF, Chrome/Edge,
and Mermaid CLI (`mmdc`). The selected notes stay intact during the build;
only generated temporary files are transformed.

## How to use a large reference book for a short demo

1. Rehearse one small, defensible lesson per domain without a screen.
2. Practise several alternative topics within every domain; the topic is random.
3. Use a definition, one visible worked example, and a check-for-understanding question.
4. Prepare the next level of detail for the Q&A: assumptions, equation, invariant,
   complexity, counterexample, trade-off, and implementation.
5. Consult the copied full chapter whenever a recall gap appears. Do not try to
   speak an entire chapter in five minutes.

AI preparation includes **both classical AI and machine learning**. In particular,
be able to derive bias–variance under squared loss and give an actual pigeonhole
example, rather than only naming underfitting/overfitting or resource allocation.

The PDF is a reference for **both the whiteboard demonstration and the interview**,
not a script to deliver from beginning to end. The copied coverage audit mentions
non-UIU subjects so nothing from the seniors' source is silently lost; those
standalone books remain in `BRACU_Viva_Prep`, outside this selected PDF.
