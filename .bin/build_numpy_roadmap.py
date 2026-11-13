#!/usr/bin/env python3
"""Generate NumPy learning roadmap source, HTML, and DOCX."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / ".bin" / "numpy_roadmap_outline.txt"
SRC = ROOT / ".bin" / "python-numpy-roadmap-source.txt"
HTML_OUT = ROOT / "html" / "python-numpy-roadmap.html"
DOCX_OUT = ROOT / "docs" / "python-numpy-roadmap.docx"

LEARNING_METHOD = """For every topic in this roadmap, study in this order:

1. Definition — What is it?
2. Purpose — Why do we use it?
3. Syntax — How do we write it?
4. Example — Simple code.
5. Output — What does the code return?
6. Explanation — Understand each line.
7. Real-world example — Where is it used?
8. Interview questions — What can interviewers ask?
9. Practice — Solve independently.

Goal: Finish fundamentals, manipulation, math, broadcasting, and linear algebra before Pandas."""

DETAILED: dict[int, str] = {
    1: """Definition: NumPy (Numerical Python) is an open-source library for fast numerical work on multidimensional arrays.

Purpose: Replace slow Python loops with vectorized C-level operations for data science, ML, and analytics.

Syntax: import numpy as np

Example:
import numpy as np
scores = np.array([70, 82, 91])
print(scores)

Output: [70 82 91]

Explanation: np.array() builds an ndarray. Operations on it run in compiled code, not per-element Python loops.

Real-world: Model features, image pixels, time-series windows, batch tensors.

Interview: "What is NumPy?" / "Why not plain lists?"

Practice: Create a 1D array of five marks and multiply every mark by 1.1.""",
    2: """Definition: We use NumPy when we need efficient numeric arrays and math at scale.

Purpose: Speed, memory, broadcasting, linear algebra, and integration with pandas, scikit-learn, and PyTorch.

Syntax: import numpy as np

Example:
import numpy as np
py_list = list(range(1_000_000))
%timeit sum(py_list)
arr = np.arange(1_000_000)
%timeit arr.sum()

Output: NumPy sum is typically much faster on large data.

Explanation: Homogeneous ndarray storage and vectorization avoid Python object overhead.

Real-world: ETL pipelines, feature engineering, training data matrices.

Interview: Speed, memory, ndarray, ecosystem.

Practice: Compare list * 2 vs np.array(list) * 2.""",
    3: """Definition: ndarray (n-dimensional array) is NumPy's main object — a homogeneous, fixed-size grid of values.

Purpose: Unified structure for 1D vectors, 2D tables, 3D volumes, etc.

Syntax: arr = np.array(data)

Example:
import numpy as np
a1 = np.array([1, 2, 3])
a2 = np.array([[1, 2], [3, 4]])
print(type(a1), a1.ndim, a2.shape)

Output: <class 'numpy.ndarray'> 1 (2, 2)

Explanation: All elements share one dtype. Shape describes dimensions.

Real-world: Feature matrix (rows=samples, cols=features).

Interview: ndarray vs list.

Practice: Build 1D and 2D arrays; print ndim, shape, size.""",
    4: """Definition: Lists are general Python sequences; NumPy arrays are typed, fixed-shape numerical grids.

Purpose: Pick lists for mixed types and small scripts; pick arrays for numeric bulk work.

Syntax: np.array(list_obj)

Example:
import numpy as np
L = [1, 2, 3]
A = np.array(L)
print(L * 2)
print(A * 2)

Output: [1, 2, 3, 1, 2, 3] vs [2 4 6]

Explanation: List * 2 repeats; array * 2 multiplies element-wise.

Real-world: Sales CSV columns loaded into ndarray for stats.

Interview: Type homogeneity, speed, broadcasting.

Practice: Store the same numbers in list and array; compare + and *.""",
    12: """Definition: np.zeros(shape) creates an array of zeros.

Purpose: Allocate a matrix before filling (weights, masks, grids).

Syntax: np.zeros((rows, cols), dtype=float)

Example:
import numpy as np
z = np.zeros((2, 3))
print(z)

Output: [[0. 0. 0.] [0. 0. 0.]]

Real-world: Initialize gradient buffers, empty image channels.

Interview: zeros vs ones vs empty.

Practice: Create 3×3 zeros, then set the diagonal to 1.""",
    15: """Definition: np.arange(start, stop, step) builds a range like range() but as an array.

Purpose: Integer or float sequences with a fixed step.

Syntax: np.arange(0, 10, 2)

Example:
import numpy as np
print(np.arange(0, 10, 2))

Output: [0 2 4 6 8]

Interview vs linspace: arange uses step; linspace uses count and endpoints.

Practice: Build even numbers 2–20 with arange.""",
    16: """Definition: np.linspace(start, stop, num) returns evenly spaced values including endpoints.

Purpose: Sampling continuous intervals (plots, thresholds).

Syntax: np.linspace(0, 1, 5)

Example:
import numpy as np
print(np.linspace(0, 100, 5))

Output: [  0.  25.  50.  75. 100.]

Interview: arange(step) vs linspace(count).

Practice: Ten points between 0 and 100.""",
    42: """Definition: reshape() returns a new view or array with different shape (same total size).

Purpose: Turn 1D data into matrices for linear algebra or images.

Syntax: arr.reshape(3, 3) or arr.reshape(-1, 3)

Example:
import numpy as np
a = np.arange(9)
b = a.reshape(3, 3)
print(b)

Output: 3×3 matrix 0–8

Interview: reshape vs resize; -1 inference.

Practice: Reshape 1–12 into 3×4.""",
    114: """Definition: Broadcasting lets NumPy apply operations on arrays of different shapes by stretching smaller arrays safely.

Purpose: Avoid explicit loops when adding vector to matrix, etc.

Syntax: Automatic when shapes are compatible per NumPy rules.

Example:
import numpy as np
M = np.array([[1, 2, 3], [4, 5, 6]])
v = np.array([10, 20, 30])
print(M + v)

Output: [[11 22 33] [14 25 36]]

Interview: broadcast rules (align trailing dimensions).

Practice: Add shape (3,) bias to shape (5, 3) data.""",
}

INTERVIEW_ANSWERS = {
    "What is the difference between arange() and linspace()?": """Ans:
arange: fixed step between values (like range). May not hit exact endpoint.
linspace: fixed number of points; includes both endpoints.
Example: np.arange(0, 1, 0.3) vs np.linspace(0, 1, 4).""",
    "What is the difference between reshape() and resize()?": """Ans:
reshape: returns new shape (often view); total elements unchanged.
resize: changes shape in place; may repeat or drop elements if size changes.""",
    "What is the difference between flatten() and ravel()?": """Ans:
ravel: 1D view when possible (shares memory).
flatten: always copies to new 1D array.""",
    "What is the difference between axis=0 and axis=1?": """Ans:
For 2D: axis=0 is down rows (column-wise agg); axis=1 is across columns (row-wise agg).
sum(axis=0) → one value per column.""",
    "What is the difference between copy() and view()?": """Ans:
view shares data; copy owns separate buffer. Changing view affects original unless copied.""",
    "What is the difference between np.dot() and *?": """Ans:
* is element-wise multiply (same shape/broadcast).
np.dot/@ is matrix multiplication (linear algebra rules).""",
}

PRACTICE_CODE: dict[int, str] = {
    1: "import numpy as np\nprint(np.arange(1, 11))",
    2: "import numpy as np\nprint(np.zeros((3, 3)))",
    3: "import numpy as np\nprint(np.ones((4, 4)))",
    4: "import numpy as np\nprint(np.arange(2, 21, 2))",
    5: "import numpy as np\nprint(np.linspace(0, 100, 10))",
    6: "import numpy as np\nprint(np.eye(3))",
    7: "import numpy as np\na = np.array([[1, 2], [3, 4]])\nprint(a.ndim, a.shape, a.size)",
    13: "import numpy as np\na = np.array([10, 20, 30, 40])\nprint(np.sum(a), np.mean(a))",
    16: "import numpy as np\na = np.array([30, 60, 45, 80])\nprint(a[a > 50])",
    17: "import numpy as np\na = np.array([30, 60, 45, 80])\nprint(np.where(a < 50, 0, a))",
    21: "import numpy as np\nA = np.array([[1, 2], [3, 4]])\nB = np.array([[5, 6], [7, 8]])\nprint(A @ B)",
}


def parse_outline(text: str) -> list[tuple[int, str, list[str]]]:
    parts: list[tuple[int, str, list[str]]] = []
    current_num = 0
    current_title = ""
    current_qs: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("NUMPY"):
            continue
        m = re.match(r"^PART\s+(\d+):\s*(.+)$", line, re.I)
        if m:
            if current_title:
                parts.append((current_num, current_title, current_qs))
            current_num = int(m.group(1))
            current_title = m.group(2).strip()
            current_qs = []
            continue
        current_qs.append(line)
    if current_title:
        parts.append((current_num, current_title, current_qs))
    return parts


def guess_code(title: str) -> str:
    title_l = title.lower()
    if "np." in title or "()" in title:
        m = re.search(r"(np\.[\w.]+)", title)
        if m:
            fn = m.group(1)
            if "zeros" in fn:
                return f"import numpy as np\nprint({fn}((2, 3)))"
            if "ones" in fn:
                return f"import numpy as np\nprint({fn}((2, 2)))"
            if "eye" in fn or "identity" in fn:
                return f"import numpy as np\nprint({fn}(3))"
            if "arange" in fn:
                return "import numpy as np\nprint(np.arange(0, 10, 2))"
            if "linspace" in fn:
                return "import numpy as np\nprint(np.linspace(0, 1, 5))"
            if "sqrt" in title_l:
                return "import numpy as np\nprint(np.sqrt([4, 9, 16]))"
            return f"import numpy as np\n# see docs for {fn}\narr = np.array([1, 2, 3])\nprint(arr)"
    if "1d" in title_l or "2d" in title_l:
        return "import numpy as np\na = np.array([10, 20, 30])\nm = np.array([[1, 2], [3, 4]])\nprint(a[0], m[1, 0])"
    if "axis" in title_l:
        return "import numpy as np\nm = np.array([[1, 2], [3, 4]])\nprint(m.sum(axis=0), m.sum(axis=1))"
    return "import numpy as np\narr = np.array([1, 2, 3, 4])\nprint(arr)"


def generic_answer(title: str, part_name: str) -> str:
    code = guess_code(title)
    return f"""Definition: {title}

Purpose: Part of {part_name} in the NumPy learning path — supports numerical pipelines before Pandas/ML.

Syntax: import numpy as np (then the function, method, or attribute from the topic title).

Example:
{code}

Output: Run the cell above; verify shape and values match your expectation.

Explanation: Works on ndarray objects with vectorized operations (faster than Python loops).

Real-world: Tabular numeric features, metrics dashboards, model inputs, image/audio grids.

Interview: Be ready to define the topic, show one line of syntax, and compare with a related API (e.g. list vs array).

Practice: Recreate the example with your own data; print ndim, shape, dtype."""


def build_source() -> str:
    text = OUTLINE.read_text(encoding="utf-8")
    parts = parse_outline(text)
    lines = [
        "=======",
        "NUMPY – COMPLETE LEARNING ROADMAP",
        "Topics, Questions, Answers, and Practical Examples",
        "=======",
        "",
        LEARNING_METHOD,
        "",
        "=======",
    ]
    qglobal = 0
    for pnum, ptitle, questions in parts:
        sec_num = f"{pnum:02d}"
        lines.append(f"{sec_num}. {ptitle}")
        lines.append("=" * 70)
        lines.append("")
        for title in questions:
            qglobal += 1
            lines.append(f"Q{qglobal}. {title}")
            if qglobal in DETAILED:
                lines.append(f"Ans: {DETAILED[qglobal]}")
            elif pnum == 19 and title in INTERVIEW_ANSWERS:
                lines.append(INTERVIEW_ANSWERS[title])
            elif pnum == 20:
                code = PRACTICE_CODE.get(
                    qglobal - sum(len(p[2]) for p in parts if p[0] < 20),
                    guess_code(title),
                )
                # practice local index
                local_i = questions.index(title) + 1
                code = PRACTICE_CODE.get(local_i, code)
                lines.append(
                    f"Ans: Task: {title}\n\nExample solution:\n{code}"
                )
            else:
                lines.append(f"Ans: {generic_answer(title, ptitle)}")
            lines.append("")
    lines.append("END OF NUMPY ROADMAP")
    return "\n".join(lines)


def load_numpy_builder():
    path = ROOT / ".bin" / "build_python_numpy.py"
    spec = importlib.util.spec_from_file_location("build_python_numpy", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    source = build_source()
    SRC.write_text(source, encoding="utf-8")
    bpn = load_numpy_builder()
    bpn.SRC = SRC
    bpn.HTML_OUT = HTML_OUT
    bpn.DOCX_OUT = DOCX_OUT
    sections = bpn.parse(source)
    html = bpn.build_html(sections)
    html = html.replace(
        "<title>NumPy · Interview Preparation</title>",
        "<title>NumPy · Complete Learning Roadmap</title>",
    )
    html = html.replace(
        "<h1>NumPy Interview</h1>",
        "<h1>NumPy Roadmap</h1>",
    )
    html = html.replace(
        "<p class=\"sub\">Beginner → advanced · full prep</p>",
        '<p class="sub">189 topics · interview · practice</p>',
    )
    html = html.replace(
        "<h1>NumPy Complete Interview Preparation</h1>",
        "<h1>NumPy – Complete Learning Roadmap</h1>",
    )
    html = html.replace(
        "<p>Beginner to advanced: fundamentals through coding programs, differences, outputs, scenarios, rapid-fire and a 7-day roadmap.</p>",
        "<p>Topics, questions, answers, and examples. Study each topic with Definition → Purpose → Syntax → Example → Output → Explanation → Real-world → Interview → Practice. Also open <a href=\"python-numpy.html\" style=\"color:#7dcea0\">full interview pack</a>.</p>",
    )
    HTML_OUT.write_text(html, encoding="utf-8")
    bpn.build_docx(sections)
    # fix docx title
    from docx import Document

    doc = Document(DOCX_OUT)
    if doc.paragraphs:
        doc.paragraphs[0].text = "NumPy – Complete Learning Roadmap"
    doc.save(DOCX_OUT)
    qs = sum(len(bpn.parse_questions(s["body"])) for s in sections if s["kind"] == "section")
    print(f"sections={len(sections)} questions={qs}")
    print(f"wrote {SRC}")
    print(f"wrote {HTML_OUT} ({HTML_OUT.stat().st_size} bytes)")
    print(f"wrote {DOCX_OUT} ({DOCX_OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
