Bismillah.

# NP-Completeness demo: current files

Use **sonia_np_completeness_demo_stepwise** for the current audited presentation.
The files without `_stepwise` are older versions and were left untouched.

For editable slide text, use the new **`sonia_np_completeness_demo_editable`**
version described below. The original LaTeX and its layout-faithful exports
remain unchanged.

## Editable PowerPoint version

- [Editable PowerPoint](sonia_np_completeness_demo_editable.pptx): 16 teaching frames, 44 successive reveal slides.
- [PDF exported by Microsoft PowerPoint](sonia_np_completeness_demo_editable.pdf): matches the editable deck.
- [Editable Quarto source](sonia_np_completeness_demo_editable.qmd): prose, equations, tables, reveal timing, and speaker notes.
- [Original LaTeX source](sonia_np_completeness_demo_stepwise.tex): retains the original TikZ drawings.
- [Build script](build_editable.py): Quarto/Pandoc conversion plus native-shape layout and reveal assembly.

Body text, titles, equations, and tables are native editable PowerPoint objects.
The original **17 TikZ drawings remain images**: you can move, resize, or replace
them, but their internal labels, vertices, and edges are not individually
editable. Their source is still the LaTeX file. This preserves the original
drawings while making the surrounding teaching content editable. Native picture
cropping removes export whitespace, not diagram content. Spacing is adapted to
PowerPoint; this version is not a pixel-identical LaTeX rendering.

The deck was opened and rendered with installed Microsoft PowerPoint. All
44 slides exported successfully, the text-height/slide-boundary check reported
zero issues, and screenshots of all 16 final teaching frames were visually
reviewed. Original drawings and the P/NP/NP-hard/NP-complete illustration remain.

From `E:\Documents\Varsity_Prep\Demo`, rebuild the editable deck with:

```powershell
python .\build_editable.py
```

If you only changed Quarto text or native layout, reuse the existing diagrams:

```powershell
python .\build_editable.py --skip-figures
```

Then export the matching PDF and check it in Microsoft PowerPoint:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\build\check_editable_powerpoint.ps1
```

The Python build uses Quarto installed at `D:\Applications\Quarto\bin\quarto.exe`
(change `QUARTO` in the script if needed), XeLaTeX on PATH, PyMuPDF, and Pillow.
The final check/PDF export requires Microsoft PowerPoint on Windows and runs
without opening a visible presentation window. Do not run `quarto render` on
the editable QMD alone to obtain the final deck: the filter produces native
element fragments that the Python composer must arrange into the 44 slides.

## Layout-faithful, image-backed version

- [LaTeX source](sonia_np_completeness_demo_stepwise.tex): edit the visible content here.
- [PDF](sonia_np_completeness_demo_stepwise.pdf): 16 teaching frames, 44 pages including incremental reveals.
- [PowerPoint](sonia_np_completeness_demo_stepwise.pptx): the same 44 reveals, produced by Quarto.
- [Quarto source](sonia_np_completeness_demo_stepwise.qmd): generated slide backgrounds and editable speaker notes.
- [Build script](build_stepwise.py): regenerates the PDF, images, Quarto source, and PowerPoint.

The PowerPoint preserves the LaTeX layout as high-resolution slide background images. Text, equations, and TikZ vertices are **not individually editable PowerPoint objects**. Speaker notes are editable. Each click advances one reveal, matching the PDF; these are successive slides rather than native PowerPoint animations. The original 4:3 aspect ratio is preserved.

## Rebuild after editing LaTeX

From `E:\Documents\Varsity_Prep\Demo`:

```powershell
python .\build_stepwise.py --quarto 'D:\Applications\Quarto\bin\quarto.exe'
```

Requires XeLaTeX, Quarto, and PyMuPDF (`fitz`). The source uses Tinos and STIX Math when installed, with Times New Roman and Cambria Math as Windows fallbacks. Use XeLaTeX, not pdfLaTeX, for these system fonts.

To rebuild only the PowerPoint from the existing Quarto source and images:

```powershell
& 'D:\Applications\Quarto\bin\quarto.exe' render .\sonia_np_completeness_demo_stepwise.qmd --to pptx
```

If Quarto is on your terminal's PATH, `quarto render .\sonia_np_completeness_demo_stepwise.qmd --to pptx` also works. Keep the `_assets` directory beside the QMD to render it again; the finished PPTX itself is self-contained.

## Audit and teaching guidance

The review checked P/NP definitions, the NP-hardness hypothesis and reduction direction, the EVEN translation, the exact clause-gadget edges, all eight truth patterns, both reduction directions, construction counts, the formula assignment, and the CLIQUE graph. The clause gadget has no output vertex: its result is whether fixed T/F input colors extend to a valid internal coloring. Gray/white vertices denote unassigned colors; edge colors are explanatory styling.

Exhaustive enumeration of the six internal vertices gives these numbers of valid completions:

| Inputs | FFF | FFT | FTF | FTT | TFF | TFT | TTF | TTT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Completions | 0 | 1 | 1 | 4 | 1 | 5 | 2 | 9 |

For `n` variables and `m` clauses, the constructed graph has `3 + 2n + 6m` vertices and `3 + 3n + 13m` edges. The exact clause construction and proof agree with the [Princeton COS 423 reduction notes](https://www.cs.princeton.edu/~wayne/cs423/lectures/reductions-poly-4up.pdf).

Seven minutes is feasible as a **rehearsed overview for students already familiar with basic graph theory, Boolean logic, and polynomial time**. It is too dense for a complete first lesson covering every proof detail. The notes provide explanation and answers to likely follow-up questions; do not read all of them aloud. Spend most of the explanation on the reduction direction and the clause gadget. Introduce CLIQUE as a brief second pattern. All material remains in the main deck.

The per-frame timing in the LaTeX comments and PowerPoint notes totals seven minutes, including every reveal within each frame. It leaves no question time, so rehearse with a timer. For actual classroom teaching with discussion, allow substantially longer.

Quarto export uses its documented [PowerPoint background images and speaker notes](https://quarto.org/docs/presentations/powerpoint.html). The build checks the PPTX archive, slide count, 4:3 canvas, exact image content/order, and presence of notes. PDF pages are visually reviewed; no Microsoft PowerPoint rendering engine is required by the build.
