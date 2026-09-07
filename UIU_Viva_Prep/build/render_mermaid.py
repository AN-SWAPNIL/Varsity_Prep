#!/usr/bin/env python3
"""Render fenced Mermaid blocks in a generated Markdown file to local SVGs."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path


MERMAID_BLOCK = re.compile(
    r"(?ms)^(?P<fence>`{3,}|~{3,})mermaid[ \t]*\r?\n"
    r"(?P<body>.*?)"
    r"^(?P=fence)[ \t]*$"
)


def find_mmdc() -> str:
    for candidate in ("mmdc.cmd", "mmdc", "mmdc.ps1"):
        found = shutil.which(candidate)
        if found:
            return found
    raise RuntimeError(
        "Mermaid CLI was not found. Install @mermaid-js/mermaid-cli so mmdc is on PATH."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    parser.add_argument("diagram_dir", type=Path)
    args = parser.parse_args()

    markdown = args.markdown.resolve()
    diagram_dir = args.diagram_dir.resolve()
    text = markdown.read_text(encoding="utf-8")
    matches = list(MERMAID_BLOCK.finditer(text))
    if not matches:
        print("Mermaid: no fenced diagrams found.")
        return 0

    diagram_dir.mkdir(parents=True, exist_ok=True)
    mmdc = find_mmdc()
    replacements: list[tuple[int, int, str]] = []

    for index, match in enumerate(matches, start=1):
        stem = f"mermaid-{index:03d}"
        source = diagram_dir / f"{stem}.mmd"
        output = diagram_dir / f"{stem}.svg"
        source.write_text(match.group("body").strip() + "\n", encoding="utf-8")

        command = [
            mmdc,
            "-i",
            str(source),
            "-o",
            str(output),
            "-t",
            "dark",
            "-b",
            "transparent",
            "-s",
            "1.5",
        ]
        completed = subprocess.run(
            command,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        if completed.returncode != 0 or not output.exists():
            details = (completed.stdout + "\n" + completed.stderr).strip()
            raise RuntimeError(f"Mermaid rendering failed for diagram {index}:\n{details}")

        relative = output.relative_to(markdown.parent).as_posix()
        replacement = (
            f'<figure class="mermaid-figure">'
            f'<img class="mermaid-image" src="{relative}" '
            f'alt="Mermaid diagram {index}">'
            f"</figure>"
        )
        replacements.append((match.start(), match.end(), replacement))

    for start, end, replacement in reversed(replacements):
        text = text[:start] + replacement + text[end:]

    markdown.write_text(text, encoding="utf-8", newline="\n")
    print(f"Mermaid: rendered {len(matches)} diagram(s) with {mmdc}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
