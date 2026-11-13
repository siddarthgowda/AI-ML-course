#!/usr/bin/env python3
"""Build assigment/day1_python.ipynb from assigment/day1_python.docx."""
from __future__ import annotations

import json
import re
import uuid
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "assigment" / "day1_python.docx"
OUT = ROOT / "assigment" / "day1_python.ipynb"

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def read_docx_paragraphs(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    out: list[str] = []
    for para in root.iter(f"{W_NS}p"):
        text = "".join((node.text or "") for node in para.iter(f"{W_NS}t")).strip()
        if text:
            out.append(text)
    return out


def cell_id() -> str:
    return uuid.uuid4().hex[:12]


def md_cell(text: str) -> dict:
    if not text.endswith("\n"):
        text += "\n"
    return {
        "id": cell_id(),
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True),
    }


def code_cell(prefix: str = "") -> dict:
    body = f"# {prefix}\n# Write your code below\n\n"
    return {
        "id": cell_id(),
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": body.splitlines(keepends=True),
    }


PART_RE = re.compile(r"^Part\s+[A-G]\s*[–-]\s*.+", re.I)
STAR_CHALLENGE = re.compile(r"^⭐\s*Challenge", re.I)

QUESTION_START = re.compile(
    r"^(Write a|Write |Create a|Create |Accept |Explain |What |Why |Revise |Go through|Understand |Explore |Think of|You are|A company|A shopping|In your own|⭐)",
    re.I,
)

SUB_BULLET = re.compile(
    r"^(upper\(\)|lower\(\)|strip\(\)|replace\(\)|split\(\)|find\(\)|"
    r"Adding elements|Removing elements|Updating elements|Accessing elements|Sorting elements|"
    r"Union$|Intersection$|Difference$|"
    r"Set A:|Set B:|Find:$|Display |Add |Remove |"
    r"The first |The last |Employees who |Total unique|"
    r"Example:$|Output |"
    r"Ordered or|Allows duplicates|Mutable or|Example use case$|"
    r"Python Developers:|SQL Developers:|"
    r"\[.+\]$|"
    r"A list of|A tuple containing|A set containing|"
    r"Your program should|Try to make)",
    re.I,
)

METHOD_ONLY = re.compile(r"^[a-z_]+\(\)$", re.I)


def group_into_sections(paras: list[str]) -> list[tuple[str, list[str]]]:
    """Return [(part_title, question_texts), ...]."""
    sections: list[tuple[str, list[str]]] = []
    current_title = "Introduction"
    current_blocks: list[str] = []
    buffer: list[str] = []

    def flush_block():
        nonlocal buffer
        if buffer:
            current_blocks.append("\n".join(buffer))
            buffer = []

    def flush_section():
        nonlocal current_blocks, current_title
        flush_block()
        if current_blocks or current_title != "Introduction":
            sections.append((current_title, current_blocks))
        current_blocks = []

    for line in paras:
        if line.strip() == "Instructions":
            continue
        if PART_RE.match(line) or STAR_CHALLENGE.match(line):
            flush_section()
            current_title = line
            continue
        if current_title == "Introduction" and not sections and not current_blocks:
            # preamble before first Part
            if QUESTION_START.match(line) or line.startswith("Complete all"):
                buffer = [line]
                flush_block()
            else:
                if not buffer:
                    buffer = [line]
                else:
                    buffer.append(line)
            continue

        is_new = QUESTION_START.match(line)
        is_sub = SUB_BULLET.match(line) or METHOD_ONLY.match(line)

        if is_new and buffer:
            flush_block()
        if is_new or (not buffer):
            buffer.append(line)
        elif is_sub or (not QUESTION_START.match(line) and len(line) < 120):
            buffer.append(line)
        else:
            flush_block()
            buffer.append(line)

    flush_section()
    return sections


def build_notebook(paras: list[str]) -> dict:
    cells: list[dict] = []
    cells.append(
        md_cell(
            "# Day 1 Python — `day1_python`\n\n"
            "Questions from `assigment/day1_python.docx`.\n\n"
            "For each question: read the markdown cell, then code in the cell below. "
            "Run with **Shift + Enter**.\n"
        )
    )

    # Instructions block (first paragraphs before Part A)
    intro_lines = []
    for line in paras:
        if PART_RE.match(line):
            break
        if line == "Instructions":
            continue
        intro_lines.append(line)
    if intro_lines:
        cells.append(md_cell("## Instructions\n\n" + "\n\n".join(intro_lines)))

    qnum = 0
    sections = group_into_sections(paras)
    for part_title, questions in sections:
        if not questions or part_title == "Introduction":
            continue
        cells.append(md_cell(f"---\n\n## {part_title}\n"))
        for qtext in questions:
            if part_title == "Introduction":
                continue
            qnum += 1
            cells.append(md_cell(f"### Q{qnum}. {qtext.split(chr(10), 1)[0]}\n\n{qtext}\n"))
            cells.append(code_cell(f"Q{qnum}"))

    cells.append(
        md_cell(
            f"---\n\n**Total questions:** {qnum}\n\n"
            "Re-run `.bin/build_day1_python_notebook.py` after editing the `.docx`."
        )
    )

    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "cells": cells,
    }


def main() -> None:
    paras = read_docx_paragraphs(DOCX)
    nb = build_notebook(paras)
    OUT.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    qcount = sum(1 for c in nb["cells"] if c["cell_type"] == "code")
    print(f"paragraphs={len(paras)} questions={qcount} cells={len(nb['cells'])}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
