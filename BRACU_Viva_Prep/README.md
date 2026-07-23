# Bismillah.

# BRACU CSE Faculty Viva — Final Source-Grounded Preparation Pack

This is the active viva-preparation set. The current academic folders were re-audited on **24 July 2026** after the source collection was reduced to the main slides and notes.

The fresh source snapshot contains:

- **70 PDFs**
- **18,977 PDF pages**
- **1 annotated ML notebook**
- **2,114 pages with little or no extractable text**, flagged for visual rather than text-only review

The aim is not to transcribe every administrative or repeated slide. The aim is to preserve the concepts an examiner can ask you to define, derive, compare, trace, implement, debug, or teach. Important algorithms include contracts, invariants, proofs, complexity, edge cases, and code. Important quantitative courses include formulas, assumptions, worked calculations, and failure cases.

## Current source routing

| Academic folder | Current source size | Viva destination and decision |
|---|---:|---|
| `101-CP` | 192 pages | Volume 04: C fundamentals plus the embedded string/structure/file/bitwise code appendix |
| `103-DM` | 236 pages | Volume 10: logic, proofs, counting, pigeonhole, recurrence, generating functions, and graph basics |
| `107-OOP` | 436 pages | Volume 03: the two current C++/Java merged decks; stale removed-file inventories were deleted |
| `203-DSA1` | 523 pages | Volume 01: four current sources, including the 22-page handwritten/image deck |
| `205-DLD` | 191 pages | Volume 14: combinational and sequential logic, including visual review of the 60-page handwritten deck |
| `207-DSA2` | 1,078 pages | Volume 02: the three current merged sources |
| `211-TOC` | 1,265 pages | Volume 15: automata, grammars, PDA, Turing machines, undecidability, and complexity |
| `215-DBMS` | 896 pages | Volume 05: two current merged DBMS sequences |
| `218-NM` | 198 pages | Volume 16: slide-centered numerical methods |
| `301-CM` | 936 pages | Selected number-theory/probability recall is folded into Discrete; no low-yield standalone volume |
| `305-CA` | 459 pages | Volume 14: ALU, MIPS-style datapath, performance, pipelining, cache, and virtual memory |
| `307-SWE` | 1,013 pages | Volume 08: 603 course pages plus the design-pattern reference |
| `309-Compiler` | 1,402 pages | Volume 15: compiler pipeline, lexing, LL/LR parsing, SDD/SDT, IR, runtime, optimization, and code generation |
| `311-DC` | 1,156 pages | Volume 07: signals, channel limits, sampling, coding, modulation, multiplexing, and link reliability |
| `313-OS` | 752 pages | Volume 06: both canonical OS sequences plus shell-command recall |
| `315-MP` | 1,094 pages | Volume 14: 8086 assembly/architecture and ATmega32/AVR peripherals |
| `317-AI` | 735 pages | Volume 09: two current merged AI sequences |
| `321-Networking` | 921 pages | Volume 07: networking decks, notebook/cheatsheet cross-check, and compact ns-3 orientation |
| `325-ISD` | 520 pages | Volume 08: requirements/UML/BPMN, architecture, DevOps, estimation, metrics, testing, and CMMI |
| `405-Security` | 1,572 pages | Volume 13: full slide-grounded security expansion |
| `409-Graphics` | 814 pages | Volume 12: both main decks plus the image-note cross-check |
| `421-GT` | 137 image-only pages | Selected graph facts only; DSA/Discrete already carry the interview-relevant core |
| `461-AE` | 453 pages | Volume 02: stable matching, matching variants, arborescence, LP, FFT, flow, and complexity |
| `463-BioInfo` | 812 pages | Deliberately not made a standalone core-viva volume; consult only if an examiner follows an elective/CV thread |
| `471-ML` | 1,186 pages + notebook | Volume 11: both merged sets and the annotated diffusion implementation |

## Final volumes

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
16. `15_TOC_CORE_COMPLETE.md` — now includes Compiler
17. `16_NUMERICAL_METHODS_CORE_COMPLETE.md`
18. `17_THESIS_RESEARCH_INDUSTRY_COMPLETE.md`
19. `18_LAST_DAY_RECALL_AND_MOCKS.md`

The combined printable file is `BRACU_CSE_Viva_Slide_Based_Detailed_Ahmmad_Nur_Swapnil.pdf`.

## Study priority

### Tier 1 — must be defensible deeply

1. DSA I, DSA II, and the Algorithm Engineering additions
2. Thesis/research, self-introduction, and teaching demonstrations
3. DBMS and Operating Systems
4. Networking/Data Communication and Security
5. OOP in C++ and Java

### Tier 2 — strong core breadth

1. Computer Architecture, DLD, Microprocessor/Microcontroller
2. AI and ML
3. SWE/ISD
4. TOC and Compiler

### Tier 3 — recall breadth

1. Discrete Mathematics
2. C
3. Computer Graphics
4. Numerical Methods

Bioinformatics is intentionally not given equal study time unless the panel follows it from your transcript or asks about the elective directly.

## Corrections that must stay exact

- Bias and variance are statistical error components. Underfitting and overfitting are related learning behaviors, not synonyms.
- The pigeonhole principle is a counting theorem: placing more objects than boxes forces at least one box to contain multiple objects. Hash collisions are a concrete computing use.
- For a 32 kHz ripple-counter input, the successive flip-flop outputs are 16, 8, 4, and **2 kHz**. A 4 kHz answer is the third flip-flop output.
- Bottom-up heap construction is $\Theta(n)$ because most nodes have small height; it is not $n$ independent $O(\log n)$ insertions.
- A* is optimal only under the relevant graph/tree-search and heuristic assumptions. With $h=0$, it behaves like uniform-cost search/Dijkstra for nonnegative costs.
- TLS protects a channel in transit; it does not authorize users or repair a compromised endpoint.
- TCP flow control protects the receiver; congestion control protects the network.
- `SYN` requests synchronization of initial TCP sequence state; `ACK` confirms a valid acknowledgment number.
- `gets`, unbounded `%s`, `while (!feof(fp))`, unchecked signed shifts, and raw binary-struct persistence are not safe modern C practices.

## How to study the pack

For each topic, use this loop:

1. **Recall:** define it without looking.
2. **Draw:** reconstruct the state, architecture, graph, table, or pipeline.
3. **Derive:** write the formula and state every assumption.
4. **Trace:** execute a small example.
5. **Implement:** write the core algorithm or API pattern.
6. **Defend:** give the invariant, proof idea, complexity, and failure case.
7. **Teach:** explain the same idea to a first-year student.

Do not read all 19 volumes linearly on the last day. Use volume 18 to identify weak areas, then jump to the detailed volume.

## Rebuilding the PDF

Requirements:

- Pandoc
- Python with PyMuPDF
- Chrome or Edge
- Mermaid CLI (`mmdc`) for Mermaid diagrams

From `BRACU_Viva_Prep`:

```powershell
powershell -ExecutionPolicy Bypass -File .\build\build_viva_pdf.ps1
```

The stylesheet uses a comfortable charcoal background (`#2b2e34`), soft off-white text, muted blue headings, and low-contrast panels. The build renders Mermaid diagrams, embeds all resources, generates bookmarks and links, validates the PDF, and removes temporary browser/rendering files after success.
