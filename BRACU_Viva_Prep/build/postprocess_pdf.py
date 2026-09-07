#!/usr/bin/env python3
"""Add metadata/bookmarks and validate a Chrome-generated viva PDF."""

from __future__ import annotations

import argparse
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import fitz


H1 = re.compile(r"^# (.+?)\s*$", re.MULTILINE)
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
ATTR = re.compile(r"\s*\{[^{}]*\}\s*$")


@dataclass
class Heading:
    level: int
    title: str


def display_title(raw: str) -> str:
    text = LINK.sub(r"\1", raw)
    text = ATTR.sub("", text)
    text = text.replace("`", "").replace("**", "").replace("__", "")
    text = text.replace("*", "").replace("_", " ")
    return " ".join(text.split()).strip()


def normalized(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def headings_from_markdown(paths: list[Path]) -> list[Heading]:
    result: list[Heading] = []
    for path in paths:
        source = path.read_text(encoding="utf-8")
        visible = []
        fence = None
        for line in source.splitlines():
            marker = re.match(r"^\s*(`{3,}|~{3,})", line)
            if marker:
                run = marker.group(1)
                if fence is None:
                    fence = run
                elif run[0] == fence[0] and len(run) >= len(fence):
                    fence = None
                continue
            if fence is None:
                visible.append(line)
        titles = [
            display_title(item)
            for item in H1.findall("\n".join(visible))
            if normalized(display_title(item)) not in {"bismillah", ""}
        ]
        if not titles:
            continue
        result.append(Heading(1, titles[0]))
        result.extend(Heading(2, title) for title in titles[1:])
    return result


def find_heading_pages(doc: fitz.Document, headings: list[Heading]) -> list[list[object]]:
    # Exclude small-font table-of-contents entries, which duplicate titles.
    page_text = []
    for page in doc:
        blocks = []
        for block in page.get_text("dict")["blocks"]:
            spans = [s for line in block.get("lines", []) for s in line["spans"]]
            if any(s["size"] >= 16.5 for s in spans):
                blocks.append(" ".join(s["text"] for s in spans))
        page_text.append(normalized(" ".join(blocks)))
    toc: list[list[object]] = []
    cursor = 0

    for heading in headings:
        target = normalized(heading.title)
        if not target:
            continue

        # Long headings occasionally wrap or include a subtitle not preserved verbatim.
        words = target.split()
        probes = [target]
        if len(words) > 10:
            probes.append(" ".join(words[:10]))
        if len(words) > 6:
            probes.append(" ".join(words[:6]))

        found = None
        for page_index in range(cursor, len(page_text)):
            if any(probe and probe in page_text[page_index] for probe in probes):
                found = page_index
                break

        if found is None:
            raise RuntimeError(f"Cannot locate body heading for bookmark: {heading.title}")
        else:
            cursor = found

        toc.append([heading.level, heading.title, found + 1])
    return toc


def verify(doc: fitz.Document, toc: list[list[object]]) -> None:
    if doc.page_count < 100:
        raise RuntimeError(f"Unexpectedly short PDF: {doc.page_count} pages")
    if len(toc) < 80:
        raise RuntimeError(f"Too few bookmarks were generated: {len(toc)}")

    sample_pages = sorted({0, doc.page_count // 4, doc.page_count // 2, doc.page_count - 1})
    for page_number in sample_pages:
        page = doc[page_number]
        if len(page.get_text("text").strip()) < 20:
            raise RuntimeError(f"Sample page {page_number + 1} has almost no text")
        pix = page.get_pixmap(matrix=fitz.Matrix(0.35, 0.35), alpha=False)
        if pix.width < 100 or pix.height < 100:
            raise RuntimeError(f"Sample page {page_number + 1} did not render normally")

    full_probe = "\n".join(
        doc[index].get_text("text")
        for index in sorted({0, min(20, doc.page_count - 1), doc.page_count // 2, doc.page_count - 1})
    ).casefold()
    if "bismillah" not in full_probe:
        raise RuntimeError("The rendered PDF probe did not contain the required opening.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--markdown", required=True, nargs="+", type=Path)
    args = parser.parse_args()

    headings = headings_from_markdown([path.resolve() for path in args.markdown])
    input_pdf = args.input.resolve()
    output_pdf = args.output.resolve()

    doc = fitz.open(input_pdf)
    toc = find_heading_pages(doc, headings)
    doc.set_toc(toc)
    metadata = doc.metadata or {}
    metadata.update(
        {
            "title": "Bismillah. BRACU CSE Faculty Viva - Source-Grounded Preparation Pack",
            "author": "Ahmmad Nur Swapnil",
            "subject": "Core CSE viva preparation from the selected academic slides",
            "keywords": "BRACU, CSE, viva, DSA, DBMS, OS, networking, security, compiler",
            "creator": "Pandoc + Chromium + PyMuPDF",
        }
    )
    doc.set_metadata(metadata)
    # Chromium has already compressed fonts, images and content streams. A full
    # garbage=4/clean/deflate rewrite can take several minutes for this 1,000+
    # page book without improving study quality. Preserve those streams and
    # write only the metadata/bookmark update.
    doc.save(output_pdf, garbage=1, deflate=False, clean=False)
    doc.close()

    verified = fitz.open(output_pdf)
    verify(verified, toc)
    print(
        f"PDF: {verified.page_count} pages, {len(toc)} bookmarks, "
        f"{output_pdf.stat().st_size / (1024 * 1024):.1f} MiB."
    )
    verified.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
