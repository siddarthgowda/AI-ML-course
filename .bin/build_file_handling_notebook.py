#!/usr/bin/env python3
"""Build file-handling-pratice.ipynb from the interview notes source."""
import ast
import json
import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / ".bin" / "python-file-handling-source.txt"
OUT = ROOT / "file-handling-pratice.ipynb"

CONCEPT = {
    1: "A variable disappears when the program stops. A file keeps the data on disk, so you can open it again later. File handling is how Python creates, opens, reads, writes, and deletes that file.",
    2: "The mode is the second argument of open(). It decides whether you may only read, overwrite, add at the end, or create the file only when it is missing.",
    3: "Once a file is open, read() takes the whole text, readline() takes one line, and readlines() gives a list of lines. write() sends one string out. writelines() sends many strings.",
    4: "Python remembers a position inside the open file, called the file pointer. tell() reports that position. seek() moves it, so you can read the same text again.",
    5: "with open() is the normal way to open a file. When the block ends, or if the code crashes inside it, Python still closes the file.",
    6: "Opening a missing file, a locked file, or a file that already exists in x mode raises an exception. try and except let the program handle that instead of stopping.",
    7: "open() returns a file object. That object knows its name, its mode, whether it is closed, and whether you can read, write, or move the pointer.",
    8: "The os module talks to the operating system: current folder, make a folder, list names, rename, and delete.",
    9: "shutil is for bigger file jobs than os: copy a file, copy a whole folder, move, or delete a folder and everything inside it.",
    10: "pathlib treats a path as an object. Path('notes.txt') can check, read, write, and delete without passing strings to os functions.",
    11: "tempfile creates a file or folder that you do not need to keep. StringIO and BytesIO act like files, but the data stays in memory.",
    12: "A CSV file is a table written as text, with commas between columns. The csv module reads each row as a list or as a dictionary.",
    13: "JSON is text for dictionaries and lists. json.dumps() makes the text. json.loads() turns that text back into Python.",
    14: "pickle saves a Python object as bytes and can rebuild that same object later. Only load pickle data that you created yourself.",
    15: "Encoding is the rule that turns letters into bytes, usually UTF-8. Buffering keeps data in memory for a moment so the program does not hit the disk on every small write.",
    16: "Compression stores the same data in fewer bytes. zipfile can pack many files. gzip, bz2, and lzma each compress one stream.",
    17: "Read the small program and decide the output before you run the solution. Running the cell shows whether the prediction was right.",
    18: "These are complete small tasks: create, read, append, count, copy, rename, and delete. Run each solution and read the print output.",
    19: "These questions cover paths, editing one line, large files, and the difference between text mode and binary mode.",
    20: "Each scenario asks which tool fits the job: append, x mode, with, binary mode, csv, json, or zip.",
    21: "Short pairs to revise out loud. The left side is the question. The right side is the answer.",
    22: "Use this list as a checklist before an interview. Each line points back to a part you already practiced.",
    23: "JSON text uses true, false, and null. Python uses True, False, and None. The json module converts between them.",
    24: "pickle.dump() writes an object into a binary file. pickle.load() reads it back. Do not unpickle a file from someone you do not trust.",
    25: "A Path knows its file name, suffix, and parent folder. read_text() and write_text() open and close the file for you.",
}


def nice(title: str) -> str:
    small = {"and", "of", "in", "to", "on"}
    words = []
    for i, word in enumerate(title.strip().title().split()):
        low = word.lower()
        if low in {"json", "csv", "os", "io"}:
            words.append(low.upper())
        elif low == "oops":
            words.append("OOPs")
        elif i and low in small:
            words.append(low)
        else:
            words.append(word)
    return " ".join(words)


def cell_id() -> str:
    return uuid.uuid4().hex[:12]


def md(source: str) -> dict:
    if not source.endswith("\n"):
        source += "\n"
    return {
        "id": cell_id(),
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def code(source: str) -> dict:
    source = source.strip("\n") + "\n"
    return {
        "id": cell_id(),
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def looks_like_code(text: str) -> bool:
    hits = 0
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for line in lines:
        if line.startswith(("import ", "from ", "with ", "def ", "for ", "try:", "print(", "file", "open(")) or re.match(r"^[A-Za-z_][\w.]*\s*=", line):
            hits += 1
    return bool(lines) and hits >= max(1, len(lines) // 2)


def revision_table(body: str) -> str:
    rows = []
    other = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or set(stripped) <= {"="}:
            continue
        if stripped.startswith("END OF"):
            continue
        if "=" in stripped and not stripped.startswith(("Q", "PART", "HIGH")):
            left, right = stripped.split("=", 1)
            rows.append(f"| {left.strip()} | {right.strip()} |")
        else:
            other.append(stripped)
    chunks = []
    if other:
        chunks.append("\n".join(other))
    if rows:
        chunks.append("| Question | Answer |\n| --- | --- |\n" + "\n".join(rows))
    return "\n\n".join(chunks)


def parse_question(chunk: str):
    lines = chunk.strip("\n").splitlines()
    header = lines[0].strip()
    match = re.match(r"Q(\d+)\.\s*(.*)", header)
    if not match:
        return None
    number = int(match.group(1))
    title = match.group(2).strip() or f"Question {number}"
    rest = "\n".join(lines[1:]).strip()
    if re.search(r"(?m)^Ans:\s*", rest):
        question, answer = re.split(r"(?m)^Ans:\s*", rest, maxsplit=1)
    else:
        question, answer = "", rest
    code_text = None
    if "```python" in answer:
        answer, fenced = answer.split("```python", 1)
        code_text = fenced.split("```", 1)[0].strip("\n")
    answer = re.sub(r"\n*Example program:\s*$", "", answer).strip()
    return {
        "n": number,
        "title": title,
        "question": question.strip(),
        "answer": answer.strip(),
        "code": code_text,
    }


def split_prompt(text: str):
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("import ", "from ", "with ", "def ", "for ", "try:", "print(", "file", "open(", "@")) or re.match(r"^[A-Za-z_][\w.]*\s*=", stripped):
            start = i
            break
    if start is None:
        return text.strip(), ""
    return "\n".join(lines[:start]).strip(), "\n".join(lines[start:]).strip()


def question_markdown(item: dict) -> str:
    parts = [f"## Q{item['n']}. {item['title']}", ""]
    extra = item["question"].strip()
    if extra:
        prose, snippet = split_prompt(extra)
        if prose:
            parts.append(prose)
            parts.append("")
        if snippet:
            parts.append("Read this first and decide what it does.")
            parts.append("")
            parts.append("```python")
            parts.append(snippet)
            parts.append("```")
        elif not prose:
            parts.append(extra)
        parts.append("")
    parts.append("**Concept**")
    parts.append("")
    parts.append(item["answer"] or "_See the program below._")
    if item["code"]:
        parts.append("")
        parts.append("Run the next cell. That program is the solution.")
    return "\n".join(parts)


def parse_parts(text: str):
    chunks = re.split(r"(?=^PART\s+\d+:)", text, flags=re.M)
    parts = []
    for chunk in chunks:
        chunk = chunk.strip()
        match = re.match(r"PART\s+(\d+):\s*(.+)", chunk)
        if not match:
            continue
        number = int(match.group(1))
        title = nice(match.group(2).splitlines()[0].strip(" -="))
        body = re.sub(r"^PART\s+\d+:.*\n(?:=+\n|-+)?", "", chunk, count=1)
        body = re.sub(r"\n=+\n\s*END OF PYTHON FILE HANDLING INTERVIEW NOTES\s*\n=+\s*$", "", body).strip()
        questions = []
        leftover = []
        for piece in re.split(r"(?=^Q\d+\.)", body, flags=re.M):
            piece = piece.strip()
            if not piece:
                continue
            if piece.startswith("Q") and re.match(r"Q\d+\.", piece):
                item = parse_question(piece)
                if item:
                    questions.append(item)
            else:
                leftover.append(piece)
        parts.append({"num": number, "title": title, "questions": questions, "notes": "\n\n".join(leftover).strip()})
    return parts


def build():
    parts = parse_parts(SRC.read_text(encoding="utf-8"))
    cells = []
    toc = ["# File handling practice", "", "25 parts. Each question has the concept, then a program you can run.", "", "Press **Shift + Enter** to run a cell. The programs save practice files in a folder named `file_demo` next to this notebook.", "", "## Parts", ""]
    for part in parts:
        count = len(part["questions"])
        label = f"{count} questions" if count else "revision"
        toc.append(f"{part['num']}. **{part['title']}** — {label}")
    cells.append(md("\n".join(toc)))

    code_cells = 0
    question_count = 0
    for part in parts:
        concept = CONCEPT.get(part["num"], "")
        heading = [f"# Part {part['num']}: {part['title']}", "", concept]
        cells.append(md("\n".join(heading)))
        if part["notes"] and not part["questions"]:
            body = revision_table(part["notes"]) if part["num"] == 21 else part["notes"]
            cells.append(md(body))
        for item in part["questions"]:
            question_count += 1
            cells.append(md(question_markdown(item)))
            if item["code"]:
                code_cells += 1
                cells.append(code(f"# Q{item['n']} solution\n" + item["code"]))

    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }
    OUT.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    errors = []
    for cell in cells:
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell["source"])
        try:
            ast.parse(source)
        except SyntaxError as error:
            errors.append(f"{error}: {source.splitlines()[0]}")
    print(f"parts={len(parts)} questions={question_count} code_cells={code_cells} cells={len(cells)}")
    print(f"syntax_errors={len(errors)}")
    for line in errors[:10]:
        print(line)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
