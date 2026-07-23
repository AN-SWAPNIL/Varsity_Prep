# Bismillah.

# BRACU CSE Faculty Viva — Final Slide-Grounded Preparation Pack

This is the final active set. It was rebuilt subject by subject from the academic folders rather than generated from a generic question list. Algorithms include invariants, traces, complexity, edge cases, and code where the sources support them. Incorrect or obsolete slide statements are marked and corrected.

The `olds/` directory preserves the earlier drafts. UIU preparation was deliberately excluded.

## Evidence and source boundaries

| Volume | Audited local material |
|---|---|
| DSA I | all 16 decks/540 slides, seven PDFs/583 pages, including the image-heavy material |
| DSA II | all 21 PDFs/1,669 counted pages, including both large merged sequences and image-heavy TSP |
| OOP | all 14 C++ lectures, 11 Java PDFs, and 178/178 Java source files |
| C | 13 PDFs/294 inspected pages and 35/35 C programs |
| DBMS | every Ashik/Toufik deck/PDF plus supplied SQL/load/control/readme assets |
| OS | canonical RRR 241-page + KRV 445-page sequences, 686 pages total |
| Networking | both merged sequences, 268 + 453 = 721 pages |
| SWE | 447 lecture slides/pages plus one CT page, 448 total |
| AI | both large merged sequences and all 21 legacy decks |
| Discrete | all 16 decks/760 slides, with book consultation for definitions/context |
| ML | both merged course sets, 674 + 512 = 1,186 pages |
| Graphics | both merged sets, 473 + 263 = 736 pages |
| Research/industry | `main.tex`, two public papers, official Matter references, and explicitly marked private-manuscript boundaries |

No standalone local slide folder exists for Security, Architecture/DLD/Microprocessor, TOC, or Numerical Methods. Those files are clearly labeled **standard-core supplements** and do not pretend to quote absent slides.

## Final reading order

1. `00_INTERVIEW_TEACHING_INDUSTRY_COMPLETE.md`
2. `01_DSA_I_SLIDE_COMPLETE.md`
3. `02_DSA_II_SLIDE_COMPLETE.md`
4. `03_OOP_CPP_JAVA_SLIDE_COMPLETE.md`
5. `04_C_PROGRAMMING_SLIDE_COMPLETE.md`
6. `05_DBMS_SLIDE_COMPLETE.md`
7. `06_OPERATING_SYSTEMS_SLIDE_COMPLETE.md`
8. `07_NETWORKING_SLIDE_COMPLETE.md`
9. `08_SOFTWARE_ENGINEERING_SLIDE_COMPLETE.md`
10. `09_ARTIFICIAL_INTELLIGENCE_SLIDE_COMPLETE.md`
11. `10_DISCRETE_MATHEMATICS_SLIDE_COMPLETE.md`
12. `11_MACHINE_LEARNING_SLIDE_COMPLETE.md`
13. `12_COMPUTER_GRAPHICS_SLIDE_COMPLETE.md`
14. `13_SECURITY_CORE_COMPLETE.md`
15. `14_ARCHITECTURE_DLD_MICRO_CORE_COMPLETE.md`
16. `15_TOC_CORE_COMPLETE.md`
17. `16_NUMERICAL_METHODS_CORE_COMPLETE.md`
18. `17_THESIS_RESEARCH_INDUSTRY_COMPLETE.md`
19. `18_LAST_DAY_RECALL_AND_MOCKS.md`

The combined printable file is `BRACU_CSE_Viva_Slide_Based_Detailed_Ahmmad_Nur_Swapnil.pdf`.

## Highest-risk corrections

- Bias and variance are statistical error components; underfitting and overfitting are related learning behaviors, not synonyms. The exact squared-error decomposition is in ML and last-day recall.
- Pigeonhole is stated and proved formally, with hash collisions, compression, modulo classes, birthdays, and load distribution as concrete uses.
- Four actual ripple-counter flip-flop outputs driven by 32 kHz are 16, 8, 4, and **2 kHz**. A 4 kHz answer is the third output unless the question uses a different stage convention.
- `gets`, `void main`, `while(!feof)`, unbounded `%s`, nonterminated `%s`, and unsafe signed shifts in old C examples are not recommended modern C.
- A* optimality depends on the search variant and heuristic assumptions. With `h=0`, it becomes uniform-cost/Dijkstra behavior for nonnegative costs.
- TLS protects a channel in transit; it does not secure a compromised endpoint or authorize users by itself.

## How to study this much material

Use active recall rather than linear rereading:

1. **Map:** scan headings and source matrices; mark red/yellow/green.
2. **Reconstruct:** for red/yellow concepts, close the file and define/draw/derive/trace aloud.
3. **Verify:** reopen only to correct the missing invariant, formula term, assumption, or edge case.
4. **Teach:** give a 30-second answer, then a whiteboard explanation suitable for a fresher.
5. **Mock:** use volume 18 and repair only failed topics in the detailed volume.

Suggested priority:

- DSA, thesis/research, self-introduction, teaching demonstrations;
- OS, DBMS, Networking/Security, OOP;
- AI/ML, Architecture/DLD/Micro, SWE;
- Discrete, C, Graphics, TOC, Numerical breadth.

## Rebuilding the PDF

Requirements: Pandoc, Python with PyMuPDF, and Chrome or Edge. From this directory:

```powershell
powershell -ExecutionPolicy Bypass -File .\build\build_viva_pdf.ps1
```

The stylesheet uses a comfortable charcoal page (`#2b2e34`), soft off-white text, muted blue headings, and low-contrast panels—dark, but not pure black. The build combines the ordered Markdown files, embeds resources, creates the PDF, adds H1/H2 bookmarks, verifies page/bookmark/link counts, and only then replaces the final PDF.
