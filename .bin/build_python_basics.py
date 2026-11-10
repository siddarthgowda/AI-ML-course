#!/usr/bin/env python3
"""Build python-basics.html and python-basics.docx from source text."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / ".bin" / "python-basics-source.txt"
HTML_OUT = ROOT / "html" / "python-basics.html"
DOCX_OUT = ROOT / "docs" / "python-basics.docx"


def parse(text: str):
    sections = []
    current = None
    q = None
    ans_lines: list[str] = []

    def clean_ans(lines: list[str]) -> str:
        cleaned = []
        for ln in lines:
            s = ln.strip()
            if s.startswith("----") or s.startswith("===="):
                continue
            cleaned.append(ln)
        return "\n".join(cleaned).strip()

    def flush_q():
        nonlocal q, ans_lines
        if current is not None and q is not None and current.get("kind") == "topic":
            a = clean_ans(ans_lines)
            if a or q:
                current["questions"].append({"q": q, "a": a})
        q = None
        ans_lines = []

    def flush_sec():
        nonlocal current
        flush_q()
        if current is not None:
            sections.append(current)
        current = None

    def start_banner(stripped: str) -> bool:
        nonlocal current
        if stripped.startswith("IMPORTANT DIFFERENCE"):
            flush_sec()
            current = {
                "kind": "list",
                "title": "Important Difference Questions",
                "items": [],
            }
            return True
        if stripped.startswith("IMPORTANT OUTPUT"):
            flush_sec()
            current = {
                "kind": "topic",
                "num": None,
                "title": "Important Output-Based Questions",
                "questions": [],
            }
            return True
        if stripped.startswith("IMPORTANT PRACTICAL"):
            flush_sec()
            current = {
                "kind": "list",
                "title": "Important Practical Coding Questions",
                "items": [],
            }
            return True
        if stripped.startswith("IMPORTANT MODULES"):
            flush_sec()
            current = {
                "kind": "modules",
                "title": "Important Modules Revision",
                "groups": [],
            }
            return True
        if stripped.startswith("PYTHON BUILT-IN"):
            flush_sec()
            current = {
                "kind": "modules",
                "title": "Python Built-in Functions",
                "groups": [],
            }
            return True
        if stripped.startswith("NEXT TOPIC") or stripped == "OBJECT-ORIENTED PROGRAMMING (OOP)":
            if current and current.get("title", "").startswith("Next Topic"):
                return True
            flush_sec()
            current = {
                "kind": "list",
                "title": "Next Topic — Object-Oriented Programming (OOP)",
                "items": [],
            }
            return True
        return False

    def is_section_break(s: str) -> bool:
        return bool(
            re.match(r"^Q\d+\.", s)
            or re.match(r"^TOPIC\s+\d+:", s)
            or s.startswith("====")
            or s.startswith("----")
            or s.startswith("IMPORTANT ")
            or s.startswith("PYTHON BUILT-IN")
            or s.startswith("NEXT TOPIC")
            or s.startswith("END OF PYTHON")
            or s == "OBJECT-ORIENTED PROGRAMMING (OOP)"
        )

    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        topic = re.match(r"^TOPIC\s+(\d+):\s*(.+)$", stripped)

        if stripped.startswith("====") or stripped.startswith("----"):
            i += 1
            continue
        if topic:
            flush_sec()
            current = {
                "kind": "topic",
                "num": int(topic.group(1)),
                "title": topic.group(2).strip().title(),
                "questions": [],
            }
            i += 1
            continue
        if start_banner(stripped):
            i += 1
            continue

        if stripped.startswith("PYTHON BASICS") or stripped.startswith(
            "COMPLETE QUESTION"
        ) or stripped.startswith("END OF PYTHON"):
            i += 1
            continue

        qm = re.match(r"^Q(\d+)\.\s*(.*)$", stripped)
        if qm and current is not None and current.get("kind") == "topic":
            flush_q()
            q = qm.group(2).strip() or f"Output question {qm.group(1)}"
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines) and lines[i].strip().upper().startswith("ANS"):
                i += 1
            ans_lines = []
            while i < len(lines):
                s = lines[i].strip()
                if is_section_break(s) and (
                    re.match(r"^Q\d+\.", s)
                    or re.match(r"^TOPIC\s+\d+:", s)
                    or s.startswith("IMPORTANT ")
                    or s.startswith("PYTHON BUILT-IN")
                    or s.startswith("NEXT TOPIC")
                    or s.startswith("END OF PYTHON")
                    or s == "OBJECT-ORIENTED PROGRAMMING (OOP)"
                    or s.startswith("====")
                ):
                    break
                if s.startswith("----"):
                    i += 1
                    continue
                ans_lines.append(lines[i])
                i += 1
            continue

        if current and current.get("kind") == "list":
            m = re.match(r"^(\d+)\.\s+(.+)$", stripped)
            if m:
                current["items"].append(m.group(2).strip())
            i += 1
            continue

        if current and current.get("kind") == "modules":
            if stripped.endswith(":") and len(stripped) < 40:
                current["groups"].append({"name": stripped.rstrip(":"), "items": []})
            elif stripped and current["groups"]:
                current["groups"][-1]["items"].append(stripped)
            elif stripped:
                current["groups"].append({"name": "", "items": [stripped]})
            i += 1
            continue

        i += 1

    flush_sec()
    return sections


def ans_to_html(ans: str) -> str:
    parts = []
    lines = ans.split("\n")
    buf_code: list[str] = []
    buf_p: list[str] = []
    in_code = False

    def flush_p():
        nonlocal buf_p
        text = "\n".join(buf_p).strip()
        if not text:
            buf_p = []
            return
        # bullets
        if all(
            re.match(r"^(\d+\.|[-*])\s+", ln.strip()) or not ln.strip()
            for ln in text.split("\n")
            if ln.strip()
        ) and any(re.match(r"^(\d+\.|[-*])\s+", ln.strip()) for ln in text.split("\n") if ln.strip()):
            items = []
            for ln in text.split("\n"):
                ln = ln.strip()
                if not ln:
                    continue
                ln = re.sub(r"^(\d+\.|[-*])\s+", "", ln)
                items.append(f"<li>{inline_code(ln)}</li>")
            parts.append("<ul>" + "".join(items) + "</ul>")
        else:
            for block in re.split(r"\n\s*\n", text):
                block = block.strip()
                if not block:
                    continue
                # OUTPUT / EXPLANATION labels
                esc = inline_code(html.escape(block).replace("\n", "<br>"))
                # fix double escape from inline_code on already escaped — redo simply
                parts.append(f"<p>{format_inline(block)}</p>")
        buf_p = []

    def flush_code():
        nonlocal buf_code, in_code
        if buf_code:
            code = "\n".join(buf_code).rstrip()
            parts.append(f"<pre><code>{html.escape(code)}</code></pre>")
        buf_code = []
        in_code = False

    code_hint = re.compile(
        r"^(def |class |import |from |with |for |while |if |elif |else:|try:|except |print\(|[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*|[a-zA-Z_]+\(|    |\t)"
    )

    for ln in lines:
        stripped = ln.strip()
        looks_code = bool(
            stripped
            and (
                code_hint.match(ln)
                or (in_code and (ln.startswith(" ") or ln.startswith("\t") or stripped in {")", "]", "}"}))
                or stripped.endswith(":")
                and any(
                    stripped.startswith(k)
                    for k in ("def ", "class ", "if ", "for ", "while ", "try", "with ", "else", "elif")
                )
            )
        )
        # Keep OUTPUT blocks as paragraphs
        if stripped.startswith("OUTPUT:") or stripped.startswith("EXPLANATION:") or stripped.startswith("Syntax:"):
            flush_code()
            flush_p()
            parts.append(f"<p><strong>{html.escape(stripped.split(':',1)[0])}:</strong> {format_inline(stripped.split(':',1)[1].strip()) if ':' in stripped else ''}</p>")
            continue
        if looks_code or (in_code and stripped == ""):
            flush_p()
            in_code = True
            buf_code.append(ln.rstrip("\n"))
            continue
        if in_code:
            flush_code()
        buf_p.append(ln)
    flush_code()
    flush_p()
    return "\n".join(parts) if parts else f"<p>{format_inline(ans)}</p>"


def format_inline(text: str) -> str:
    """Escape then wrap backtick-like tokens and common callables lightly."""
    esc = html.escape(text)
    # wrap code-looking tokens: foo(), __name__, *args, **kwargs, modes
    esc = re.sub(
        r"`([^`]+)`",
        r"<code>\1</code>",
        esc,
    )
    esc = re.sub(
        r"\b([a-zA-Z_][a-zA-Z0-9_]*)\(\)",
        r"<code>\1()</code>",
        esc,
    )
    esc = esc.replace("\n", "<br>")
    return esc


def inline_code(text: str) -> str:
    return format_inline(text)


CSS = """
    :root {
      color-scheme: dark;
      --bg: #181818;
      --panel: #202020;
      --text: #e8e8e8;
      --muted: #9a9a9a;
      --line: #3a3a3a;
      --accent: #7dcea0;
      --code-bg: #141414;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    .layout {
      display: grid;
      grid-template-columns: 280px minmax(0, 820px);
      gap: 0;
      max-width: 1120px;
      margin: 0 auto;
    }
    nav {
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: auto;
      padding: 20px 16px 40px;
      border-right: 1px solid var(--line);
      background: #161616;
    }
    nav h1 { font-size: 15px; margin: 0 0 4px; }
    nav .sub { color: var(--muted); font-size: 12px; margin: 0 0 16px; }
    nav a {
      display: block;
      color: var(--text);
      text-decoration: none;
      font-size: 12.5px;
      padding: 3px 0;
    }
    nav a:hover { color: var(--accent); }
    .toc-stage {
      margin: 14px 0 6px;
      color: var(--accent);
      font-size: 11px;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    main { padding: 28px 28px 80px; }
    .intro {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 18px 20px;
      margin: 0 0 20px;
    }
    .intro h1 { margin: 0 0 8px; font-size: 22px; }
    .intro p { margin: 0; color: var(--muted); }
    h1.stage {
      font-size: 13px;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--accent);
      margin: 36px 0 12px;
      padding-top: 8px;
    }
    article.topic {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 18px 20px 16px;
      margin: 0 0 14px;
    }
    article h2 {
      margin: 0 0 10px;
      font-size: 17px;
      font-weight: 650;
    }
    .num {
      color: var(--accent);
      font-variant-numeric: tabular-nums;
      margin-right: 6px;
    }
    .body p { margin: 0 0 8px; }
    .body ul, .body ol { margin: 0 0 10px; padding-left: 20px; }
    .body li { margin: 2px 0; }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 8px 0 12px;
      font-size: 14px;
    }
    th, td {
      border: 1px solid var(--line);
      padding: 6px 8px;
      text-align: left;
      vertical-align: top;
    }
    th { color: var(--muted); font-weight: 600; }
    code {
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 13px;
      background: #2a2a2a;
      padding: 1px 5px;
      border-radius: 4px;
    }
    pre {
      background: var(--code-bg);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px 14px;
      overflow: auto;
      margin: 10px 0 0;
    }
    pre code { background: transparent; padding: 0; font-size: 13px; }
    .qmeta { color: var(--muted); font-size: 13px; margin: 0 0 18px; }
    @media (max-width: 860px) {
      .layout { grid-template-columns: 1fr; }
      nav { position: relative; height: auto; max-height: 40vh; }
    }
"""


def build_html(sections) -> str:
    toc = []
    main = []
    qn = 0
    for sec in sections:
        sid = re.sub(r"[^a-z0-9]+", "-", sec["title"].lower()).strip("-")
        if sec["kind"] == "topic":
            label = (
                f"Topic {sec['num']}: {sec['title']}"
                if sec.get("num")
                else sec["title"]
            )
            toc.append(f'<p class="toc-stage">{html.escape(label)}</p>')
            main.append(f'<h1 class="stage" id="{sid}">{html.escape(label)}</h1>')
            for item in sec["questions"]:
                qn += 1
                qid = f"q{qn}"
                short = item["q"][:70] + ("…" if len(item["q"]) > 70 else "")
                toc.append(f'<a href="#{qid}">{qn}. {html.escape(short)}</a>')
                main.append(
                    f'<article class="topic" id="{qid}">'
                    f'<h2><span class="num">{qn}</span> {html.escape(item["q"])}</h2>'
                    f'<div class="body">{ans_to_html(item["a"])}</div></article>'
                )
        elif sec["kind"] == "list":
            toc.append(f'<p class="toc-stage">{html.escape(sec["title"])}</p>')
            toc.append(f'<a href="#{sid}">{html.escape(sec["title"])}</a>')
            items = "".join(
                f"<li>{html.escape(x)}</li>" for x in sec.get("items", [])
            )
            main.append(
                f'<h1 class="stage" id="{sid}">{html.escape(sec["title"])}</h1>'
                f'<article class="topic"><div class="body"><ol>{items}</ol></div></article>'
            )
        elif sec["kind"] == "modules":
            toc.append(f'<p class="toc-stage">{html.escape(sec["title"])}</p>')
            toc.append(f'<a href="#{sid}">{html.escape(sec["title"])}</a>')
            rows = []
            for g in sec.get("groups", []):
                name = html.escape(g.get("name") or "Other")
                items = ", ".join(f"<code>{html.escape(x)}</code>" for x in g.get("items", []))
                rows.append(f"<tr><td><strong>{name}</strong></td><td>{items}</td></tr>")
            table = (
                "<table><thead><tr><th>Module / Group</th><th>Functions</th></tr></thead>"
                f"<tbody>{''.join(rows)}</tbody></table>"
            )
            main.append(
                f'<h1 class="stage" id="{sid}">{html.escape(sec["title"])}</h1>'
                f'<article class="topic"><div class="body">{table}</div></article>'
            )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<title>Python Basics · Interview Questions</title>
<style>{CSS}</style>
</head>
<body>
<div class="layout">
<nav>
<h1>Python Basics</h1>
<p class="sub">Interview question bank · complete</p>
{''.join(toc)}
</nav>
<main>
<div class="intro">
<h1>Python Basics — Interview Questions</h1>
<p>Complete question bank covering introduction through decorators, plus differences, outputs, practicals, modules and built-ins. Next: OOP.</p>
</div>
<p class="qmeta">{qn} Q&amp;A items across topics 1–22 and extras.</p>
{''.join(main)}
</main>
</div>
</body>
</html>
"""


def build_docx(sections):
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    doc.add_heading("Python Basics — Interview Questions", 0)
    doc.add_paragraph(
        "Complete question bank covering introduction through decorators, "
        "plus differences, outputs, practicals, modules and built-ins."
    )

    qn = 0
    for sec in sections:
        if sec["kind"] == "topic":
            title = (
                f"Topic {sec['num']}: {sec['title']}"
                if sec.get("num")
                else sec["title"]
            )
            doc.add_heading(title, level=1)
            for item in sec["questions"]:
                qn += 1
                doc.add_heading(f"Q{qn}. {item['q']}", level=2)
                for block in item["a"].split("\n\n"):
                    block = block.strip()
                    if not block:
                        continue
                    # code-ish
                    if any(
                        block.startswith(k)
                        for k in ("def ", "import ", "from ", "with ", "for ", "try:")
                    ) or "\n    " in block:
                        p = doc.add_paragraph()
                        run = p.add_run(block)
                        run.font.name = "Courier New"
                        run.font.size = Pt(9)
                    else:
                        for ln in block.split("\n"):
                            m = re.match(r"^(\d+\.|[-*])\s+(.+)$", ln.strip())
                            if m:
                                doc.add_paragraph(m.group(2), style="List Bullet")
                            elif ln.strip():
                                doc.add_paragraph(ln.strip())
        elif sec["kind"] == "list":
            doc.add_heading(sec["title"], level=1)
            for i, item in enumerate(sec.get("items", []), 1):
                doc.add_paragraph(f"{i}. {item}")
        elif sec["kind"] == "modules":
            doc.add_heading(sec["title"], level=1)
            for g in sec.get("groups", []):
                name = g.get("name") or "Other"
                items = ", ".join(g.get("items", []))
                doc.add_paragraph(f"{name}: {items}")

    doc.save(DOCX_OUT)
    return qn


def main():
    text = SRC.read_text(encoding="utf-8")
    sections = parse(text)
    html_doc = build_html(sections)
    HTML_OUT.write_text(html_doc, encoding="utf-8")
    qn = build_docx(sections)
    print(f"sections={len(sections)} questions≈{qn}")
    print(f"wrote {HTML_OUT} ({HTML_OUT.stat().st_size} bytes)")
    print(f"wrote {DOCX_OUT} ({DOCX_OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
