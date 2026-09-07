"""Rebuild the Beamer PDF and a visually faithful Quarto PowerPoint.

Usage: python build_stepwise.py [--quarto PATH] [--skip-latex]
Requires XeLaTeX, Quarto and PyMuPDF (import fitz).
The PowerPoint uses slide background images; speaker notes remain editable.
"""

from pathlib import Path
import argparse
import hashlib
import posixpath
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile

import fitz

ROOT = Path(__file__).resolve().parent
STEM = "sonia_np_completeness_demo_stepwise"
BUILD = ROOT / "build"
ASSETS = ROOT / f"{STEM}_assets"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

# These are total times per teaching frame, including all its reveals.
TIMES = [10, 20, 35, 35, 40, 25, 25, 30, 40, 35, 20, 25, 40, 20, 15, 5]
NOTES = [
    "Introduce yourself briefly and state the learning objective: explain NP-completeness and how a reduction transfers hardness. This is a seven-minute overview for students who already know basic graphs, Boolean logic, and polynomial running time; it is not a complete first lesson in complexity theory.",
    "Ask: if we cannot find a fast algorithm, how can we compare the difficulty of problems? We will distinguish solving, verifying, and comparing. The dotted arrows are the teaching order, not mathematical implications between the classes. Preview the known-hard-to-target direction.",
    "P contains decision problems we can solve in polynomial time. NP contains decision problems whose YES instances have short certificates checkable in polynomial time. A proposed coloring is the certificate: check the color domain and every edge. A NO instance has no accepting certificate. NP does not mean non-polynomial. P is contained in NP, but equality is unknown. Explain the formula verbally rather than reading every symbol.",
    "An NP-hard problem can receive an efficient answer-preserving reduction from every problem in NP. It need not have a short, efficiently verifiable certificate. NP-complete means both NP-hard and in NP. Point at the intersection. The P box indicates containment in NP; its exact boundary is deliberately unspecified. No polynomial-time algorithm is known for an NP-complete problem; NP-completeness does not prove that none exists.",
    "Read the direction aloud: A reduces to B. The translator transforms an instance, then a hypothetical B solver gives the answer to A. Both YES and NO must be preserved. Demonstrate 6 becoming 12 and 7 becoming 14: n is even exactly when 2n is a multiple of 4. Doubling a binary integer takes time linear in its bit length. This is a mechanics example, not a hardness proof. Never solve the hard source instance in the translator.",
    "Two obligations: membership in NP and NP-hardness. Choose a known NP-complete source A, construct the translator, prove the equivalence, and show polynomial construction time. The implication needs the assumption that A is NP-hard. A reduction from an easy source alone cannot establish NP-hardness of B.",
    "A literal is a variable or its negation. A three-literal OR is a clause; AND all clauses together. 3-SAT asks whether every clause can be made true. 3-COLOR asks whether every graph vertex can receive one of three colors with different colors on adjacent endpoints. We will turn truth choices and clause constraints into graph edges. The transformer builds the graph without knowing a satisfying assignment.",
    "A triangle forces three distinct colors; name them T, F, and B. These are relative names, so the actual red, green, and blue paints can be permuted. Each variable and its negation connect to B and to each other. Neither can use B, and they cannot match, so their only possibilities are T/F and F/T. Ask students which color remains for the negation once the positive literal is T.",
    "Reveal literal arms, T-links, then the forcing path. There are six new internal vertices and thirteen new edges. Literal inputs already have T/F colors because they connect to B. White and gray fills mean unassigned vertices, not fourth or fifth colors; colored lines are ordinary edges. A crossing without a vertex circle is not a junction. The gadget has no output vertex: its result is whether the fixed input coloring can extend to the internal vertices. The dotted edges already exist; omitted palette edges remain part of the complete graph.",
    "Trace the impossible case first. Three false inputs force all a vertices to B. The b vertices can then use only T/F. Starting at T forces b1=F, b2=T, b3=F, conflicting with the final fixed F. For any chosen true position i, color ai=F, bi=B and all other a vertices B. Valid b triples are (B,F,T), (F,B,T), or (F,T,B) for i=1,2,3 respectively, even if additional inputs are true. Show the i=3 picture; the displayed triples justify all seven satisfying patterns. The left image is an attempted coloring with a forced conflict, not a claim that invalid colorings are accepted.",
    "Use x1=true, x2=true, x3=false. The two clauses receive (T,F,F) and (F,T,T), so both gadgets extend. This is a demonstration of a witness after construction; the reduction never needs to discover this assignment. Each clause gets its own six fresh internal vertices.",
    "This is an assembly schematic, not an expanded adjacency drawing: the boxes represent the exact gadget just proved. Share one palette and the literal vertices, and add independent internal vertices per clause. Reusing a variable across clauses enforces a consistent global assignment. Clause gadgets also connect to the palette T and F as already shown.",
    "State both directions. A satisfying assignment colors all literal vertices, and every clause extends independently. Conversely, a legal coloring makes each variable pair opposite and supplies a true literal to every clause. With n variables and m clauses, the construction has 3+2n+6m vertices and 3+3n+13m edges. These can be enumerated in polynomial time (linear many graph records; bit encoding adds index lengths). A coloring is verified in O(V+E), so 3-COLOR belongs to NP. Together with NP-hardness, this proves NP-completeness.",
    "Treat this as a brief second pattern, not another full lecture. Create three occurrence vertices per clause and only cross-clause edges between noncomplementary literals. An m-clique must choose exactly one occurrence from each clause, since no two vertices in a clause are adjacent. Its choices are consistent and can be set true. Conversely, choose one true occurrence from each satisfied clause to form a clique. Highlight x1 from C1, x2 from C2, and x1 from C3. Repeated x1 occurrences are distinct vertices and compatible. There are 3m vertices and at most 9 times binomial(m,2) edges. CLIQUE is also in NP: check the chosen vertices and their pairwise edges.",
    "End with the reusable recipe: show the target is in NP, then reduce a known NP-complete problem to it in polynomial time, preserving YES and NO. Ask a quick direction check if time permits: to prove B hard, do we reduce A to B or B to A? Answer: known-hard A to target B.",
    "Acknowledge the sources. The exact six-vertex, thirteen-edge clause gadget is from the Princeton COS 423 reduction notes. The references stay in the main deck. Do not spend presentation time reading the bibliography.",
]


def run(command):
    result = subprocess.run([str(x) for x in command], cwd=ROOT,
                            capture_output=True, text=True, errors="replace")
    if result.returncode:
        raise RuntimeError(result.stdout[-6000:] + result.stderr[-6000:])
    return result.stdout


def find_quarto(explicit):
    candidates = [explicit, shutil.which("quarto"),
                  r"D:\Applications\Quarto\bin\quarto.exe",
                  r"C:\Program Files\Quarto\bin\quarto.exe"]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    raise SystemExit("Quarto not found. Pass --quarto with the full executable path.")


def reference_template(quarto):
    target = ASSETS / "reference-4x3.pptx"
    with tempfile.TemporaryDirectory(prefix="quarto-reference-", dir=BUILD) as tmp:
        original = Path(tmp) / "reference.pptx"
        run([quarto, "pandoc", "-o", original,
             "--print-default-data-file", "reference.pptx"])
        with zipfile.ZipFile(original) as src, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as dst:
            for item in src.infolist():
                data = src.read(item.filename)
                if item.filename == "ppt/presentation.xml":
                    # Change only the canvas size; empty slides use backgrounds.
                    data, count = re.subn(
                        rb'<p:sldSz\b[^>]*/>',
                        b'<p:sldSz cx="9144000" cy="6858000" type="screen4x3"/>',
                        data,
                    )
                    if count != 1:
                        raise RuntimeError("Could not set reference slide size")
                dst.writestr(item, data)
    return target


def verify_pptx(path, page_images):
    with zipfile.ZipFile(path) as ppt:
        assert ppt.testzip() is None, "Corrupt PowerPoint archive"
        root = ET.fromstring(ppt.read("ppt/presentation.xml"))
        size = root.find(f"{{{P}}}sldSz")
        assert (int(size.get("cx")), int(size.get("cy"))) == (9144000, 6858000)
        slides = root.find(f"{{{P}}}sldIdLst")
        assert len(slides) == len(page_images), "Missing or extra reveal steps"
        for number, expected in enumerate(page_images, 1):
            slide_path = f"ppt/slides/slide{number}.xml"
            slide = ET.fromstring(ppt.read(slide_path))
            bg = slide.find(f"{{{P}}}cSld/{{{P}}}bg")
            assert bg is not None, f"Slide {number}: missing background"
            blip = bg.find(f".//{{{A}}}blip")
            assert blip is not None, f"Slide {number}: missing image"
            rid = blip.get(f"{{{R}}}embed")
            rels = ET.fromstring(ppt.read(f"ppt/slides/_rels/slide{number}.xml.rels"))
            image_rel = next(r for r in rels if r.get("Id") == rid)
            image_path = posixpath.normpath(posixpath.join("ppt/slides", image_rel.get("Target")))
            assert hashlib.sha256(ppt.read(image_path)).digest() == hashlib.sha256(expected.read_bytes()).digest(), f"Slide {number}: changed image"
            assert any(r.get("Type", "").endswith("/notesSlide") for r in rels), f"Slide {number}: missing notes"
    print(f"Verified {len(page_images)} slides: 4:3 canvas, exact image order/content, speaker notes.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quarto")
    parser.add_argument("--skip-latex", action="store_true",
                        help="Use the already rebuilt PDF in build/.")
    args = parser.parse_args()
    quarto = find_quarto(args.quarto)
    BUILD.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)
    tex = ROOT / f"{STEM}.tex"
    built_pdf = BUILD / f"{STEM}.pdf"
    if not args.skip_latex:
        for pass_number in (1, 2):
            print(f"XeLaTeX pass {pass_number}/2", flush=True)
            run(["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                 "-output-directory=build", tex.name])
    if not built_pdf.is_file() or built_pdf.stat().st_mtime < tex.stat().st_mtime:
        raise RuntimeError("The build PDF is missing or older than the LaTeX source. Rebuild without --skip-latex.")
    log = (BUILD / f"{STEM}.log").read_text(errors="replace")
    issues = [line for line in log.splitlines() if re.search(r"Overfull|Missing character|^!", line)]
    if issues:
        raise RuntimeError("Inspect LaTeX layout/font errors before exporting:\n" + "\n".join(issues))

    reference = reference_template(quarto)
    doc = fitz.open(built_pdf)
    nav = (BUILD / f"{STEM}.nav").read_text()
    frame_ranges = [(int(a), int(b)) for a, b in re.findall(r"\\beamer@framepages\s*\{(\d+)\}\{(\d+)\}", nav)]
    assert len(frame_ranges) == len(NOTES) == len(TIMES) == 16
    assert frame_ranges[-1][1] == len(doc)
    pages = {}
    for frame, (first, last) in enumerate(frame_ranges, 1):
        for page in range(first, last + 1):
            pages[page] = (frame, page - first + 1, last - first + 1)

    qmd = ["---", "format:", "  pptx:",
           f"    reference-doc: {reference.relative_to(ROOT).as_posix()}",
           "slide-level: 2", "---", "",
           "<!-- Generated by build_stepwise.py from the corrected Beamer PDF.",
           "Each PDF reveal becomes a slide background; notes are editable.",
           "Edit the .tex for visible content and rebuild. -->", ""]
    page_images = []
    for number, page in enumerate(doc, 1):
        image = ASSETS / f"page-{number:03d}.png"
        page.get_pixmap(matrix=fitz.Matrix(5.5, 5.5), alpha=False).save(image)
        page_images.append(image)
        frame, reveal, reveals = pages[number]
        end = sum(TIMES[:frame])
        start = end - TIMES[frame - 1]
        timing = f"{start // 60}:{start % 60:02d} to {end // 60}:{end % 60:02d}"
        qmd += [f'## {{background-image="{image.relative_to(ROOT).as_posix()}"}}', "",
                "::: {.notes}",
                f"Teaching slide {frame}/16; reveal {reveal}/{reveals}. Total frame budget: {TIMES[frame - 1]} seconds ({timing}).",
                "", NOTES[frame - 1], "",
                "The timing applies to all reveals together; do not repeat the explanation on each click.",
                "::: ", ""]
    qmd_path = ROOT / f"{STEM}.qmd"
    qmd_path.write_text("\n".join(qmd), encoding="utf-8")
    print(f"Rendering {len(doc)} PDF pages through Quarto", flush=True)
    print(run([quarto, "render", qmd_path.name, "--to", "pptx"]))
    pptx = ROOT / f"{STEM}.pptx"
    verify_pptx(pptx, page_images)
    shutil.copy2(built_pdf, ROOT / f"{STEM}.pdf")
    print(f"Updated {STEM}.pdf, .pptx and .qmd")


if __name__ == "__main__":
    main()
