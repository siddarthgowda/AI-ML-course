#!/usr/bin/env python3
"""Build python-file-handling.html and python-file-handling.docx from interview Q&A source."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / ".bin" / "python-file-handling-source.txt"
HTML_OUT = ROOT / "html" / "python-file-handling.html"
DOCX_OUT = ROOT / "docs" / "python-file-handling.docx"

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
      grid-template-columns: 280px minmax(0, 860px);
      gap: 0;
      max-width: 1160px;
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
      padding: 16px 18px 14px;
      margin: 0 0 12px;
    }
    article h2 {
      margin: 0 0 8px;
      font-size: 16px;
      font-weight: 650;
    }
    .num {
      color: var(--accent);
      font-variant-numeric: tabular-nums;
      margin-right: 6px;
    }
    .body p { margin: 0 0 8px; }
    .body p.label { margin-top: 10px; font-weight: 600; }
    .body ul, .body ol { margin: 0 0 10px; padding-left: 20px; }
    .body li { margin: 2px 0; }
    .subhead {
      margin: 22px 0 10px;
      font-size: 14px;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: var(--muted);
    }
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
      padding: 10px 12px;
      overflow: auto;
      margin: 8px 0 0;
    }
    pre code { background: transparent; padding: 0; font-size: 13px; }
    .qmeta { color: var(--muted); font-size: 13px; margin: 0 0 18px; }
    .rf {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px 16px;
      font-size: 14px;
    }
    .rf div { border-bottom: 1px solid var(--line); padding: 4px 0; }
    .rf .q { color: var(--muted); }
    @media (max-width: 900px) {
      .layout { grid-template-columns: 1fr; }
      nav { position: relative; height: auto; max-height: 40vh; }
      .rf { grid-template-columns: 1fr; }
    }
"""


def nice_title(title: str) -> str:
    t = title.strip().title()
    for a, b in [
        ("Oops", "OOPs"),
        ("Oop", "OOP"),
        ("Abc", "ABC"),
        ("Mro", "MRO"),
        ("Json", "JSON"),
        ("Solid", "SOLID"),
        (" And ", " and "),
        (" Of ", " of "),
        (" In ", " in "),
        (" For ", " for "),
        (" To ", " to "),
        (" On ", " on "),
        (" Vs ", " vs "),
        (" Or ", " or "),
    ]:
        t = t.replace(a, b)
    return t


def parse(text: str):
    lines = text.replace("\r\n", "\n").split("\n")
    sections = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        m = re.match(r"^PART\s+(\d+):\s*(.+)$", s, re.I)
        if m:
            num = int(m.group(1))
            title = nice_title(m.group(2))
            i += 1
            while i < len(lines) and (
                not lines[i].strip() or lines[i].strip().startswith("----")
            ):
                i += 1
            body = []
            while i < len(lines):
                t = lines[i].strip()
                if re.match(r"^PART\s+\d+:", t, re.I):
                    break
                if t.startswith("END OF OOPS"):
                    break
                if t.startswith("====") and "END" in "".join(lines[max(0, i - 1) : i + 2]):
                    break
                body.append(lines[i])
                i += 1
            sections.append({"num": num, "title": title, "body": "\n".join(body).strip()})
            continue
        if s.startswith("END OF OOPS"):
            break
        i += 1
    return sections


def parse_questions(body: str):
    items = []
    # also capture subsection banners like ---------------- INHERITANCE ----------------
    parts = re.split(r"(?=^Q\d+\.|^-{5,}\s*[A-Z].*\s*-{5,})", body, flags=re.M)
    current_sub = None
    for part in parts:
        part = part.strip()
        if not part:
            continue
        sub = re.match(r"^-{5,}\s*(.+?)\s*-{5,}$", part)
        if sub:
            current_sub = nice_title(sub.group(1))
            items.append({"kind": "sub", "title": current_sub})
            continue
        # module banners like ---------------- ABC MODULE ----------------
        m = re.match(r"^Q(\d+)\.\s*(.*)$", part, re.S)
        if not m:
            continue
        qn = int(m.group(1))
        rest = m.group(2).strip()
        if re.search(r"(?m)^Ans:\s*", rest):
            qtext, ans = re.split(r"(?m)^Ans:\s*", rest, maxsplit=1)
            q, a = qtext.strip(), ans.strip()
        elif re.search(r"(?m)^Answer:\s*", rest):
            qtext, ans = re.split(r"(?m)^Answer:\s*", rest, maxsplit=1)
            q = qtext.strip() or f"Output question {qn}"
            a = "Answer:\n" + ans.strip()
        else:
            lines = rest.split("\n")
            if lines and (lines[0].strip().endswith("?") or len(lines[0].strip()) < 100):
                q = lines[0].strip()
                a = "\n".join(lines[1:]).strip()
            else:
                q = f"Question {qn}"
                a = rest
        items.append({"kind": "q", "n": qn, "q": q, "a": a})
    return items


def inline(text: str) -> str:
    esc = html.escape(text)
    esc = re.sub(r"`([^`]+)`", r"<code>\1</code>", esc)
    esc = re.sub(r"\b(__[a-zA-Z0-9_]+__)\b", r"<code>\1</code>", esc)
    esc = re.sub(r"@([a-zA-Z_][a-zA-Z0-9_]*)", r"<code>@\1</code>", esc)
    esc = re.sub(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\(\)", r"<code>\1()</code>", esc)
    return esc


def looks_code(chunk: str) -> bool:
    lines = [ln for ln in chunk.split("\n") if ln.strip()]
    if not lines:
        return False
    hits = 0
    for ln in lines:
        st = ln.strip()
        if st.startswith(("Output:", "Answer:", "OUTPUT:", "Class:", "Object:", "Objects:", "Attributes:", "Methods:", "Procedural:", "OOPs:", "Instance variable:", "Class variable:", "self =", "cls =", "Public =", "Protected =", "Private =", "Abstraction =", "Encapsulation =", "Overloading =", "Overriding =", "Module =", "Package =", "Has-a =", "Is-a =", "Aggregation =", "Composition =", "Shallow =", "Deep =", "isinstance =", "issubclass =", "Pickle =", "JSON =", "Abstract class =", "Normal class =", "__dict__ =", "__slots__ =", "S =", "O =", "L =", "I =", "D =", "Important:", "IMPORTANT:", "Example:", "Functions:", "Components:", "Becomes approximately:")):
            continue
        if (
            st.startswith(("import ", "from ", "print(", "class ", "def ", "s1 =", "s2 =", "obj =", "e1 =", "c =", "b =", "a =", "n1 =", "n2 =", "r1 =", "car =", "animals =", "pass"))
            or re.match(r"^[a-zA-Z_][\w\.]*\s*=", st)
            or st.startswith("@")
            or st in {")", "]:", "}"}
        ):
            hits += 1
    return hits >= max(1, (len(lines) + 1) // 2)


FENCE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.S)


def format_answer(ans: str) -> str:
    if not ans:
        return ""
    parts = []
    pos = 0
    for match in FENCE.finditer(ans):
        before = ans[pos : match.start()]
        if before.strip():
            parts.append(format_answer_chunks(before))
        code = match.group(1).rstrip("\n")
        parts.append(f"<pre><code>{html.escape(code)}</code></pre>")
        pos = match.end()
    tail = ans[pos:]
    if tail.strip():
        parts.append(format_answer_chunks(tail))
    return "\n".join(part for part in parts if part)


def format_answer_chunks(ans: str) -> str:
    if not ans:
        return ""
    parts = []
    chunks = re.split(r"\n\s*\n", ans)
    for chunk in chunks:
        chunk = chunk.strip("\n")
        if not chunk.strip():
            continue
        lines = chunk.split("\n")

        if looks_code(chunk) or chunk.strip().startswith(("Output:", "Answer:", "OUTPUT:")):
            for label in ("Output:", "Answer:", "OUTPUT:"):
                if f"\n{label}" in chunk or chunk.startswith(label):
                    if chunk.startswith(label):
                        rest = chunk[len(label) :].strip()
                        parts.append(f'<p class="label">{label}</p>')
                        if rest:
                            parts.append(f"<pre><code>{html.escape(rest)}</code></pre>")
                        break
                    code, out = chunk.split(f"\n{label}", 1)
                    if code.strip():
                        parts.append(f"<pre><code>{html.escape(code.strip())}</code></pre>")
                    parts.append(f'<p class="label">{label}</p>')
                    if out.strip():
                        parts.append(f"<pre><code>{html.escape(out.strip())}</code></pre>")
                    break
            else:
                parts.append(f"<pre><code>{html.escape(chunk.strip())}</code></pre>")
            continue

        # labeled bullets / comparison
        if any(
            re.match(r"^\d+\.\s+", ln.strip()) or ln.strip().startswith("- ") or (
                ln.strip().endswith(":") and len(ln.strip()) < 40
            )
            for ln in lines
        ):
            items = []
            for ln in lines:
                st = ln.strip()
                if not st:
                    continue
                if st.endswith(":") and not re.match(r"^\d+\.", st) and not st.startswith("-") and not looks_code(st):
                    if items:
                        parts.append("<ul>" + "".join(items) + "</ul>")
                        items = []
                    parts.append(f'<p class="label">{html.escape(st)}</p>')
                elif st.startswith("- ") or re.match(r"^\d+\.\s+", st):
                    st2 = re.sub(r"^(-\s+|\d+\.\s+)", "", st)
                    items.append(f"<li>{inline(st2)}</li>")
                else:
                    # continuation under label like "Blueprint." lines
                    if items is not None and (
                        st.startswith(("- ",)) is False
                        and (
                            st[0].islower()
                            or st.startswith(
                                (
                                    "Blueprint",
                                    "Defines",
                                    "Created",
                                    "Instance",
                                    "Has ",
                                    "Belongs",
                                    "Usually",
                                    "Each ",
                                    "Shared",
                                    "Access",
                                    "Focuses",
                                    "Requires",
                                    "Supports",
                                    "Current",
                                    "Uses ",
                                    "No ",
                                    "Used ",
                                    "Readable",
                                    "Unambiguous",
                                    "Weak ",
                                    "Strong ",
                                    "Called",
                                    "Accessed",
                                    "Python",
                                    "Single",
                                    "Multiple",
                                    "Checks",
                                    "Stores",
                                    "Declares",
                                    "Actual",
                                    "A way",
                                    "New ",
                                    "Recursively",
                                    "Cannot",
                                    "Can generally",
                                    "Language",
                                    "Special",
                                    "Exception",
                                )
                            )
                        )
                    ):
                        items.append(f"<li>{inline(st)}</li>")
                    else:
                        if items:
                            parts.append("<ul>" + "".join(items) + "</ul>")
                            items = []
                        parts.append(f"<p>{inline(st)}</p>")
            if items:
                parts.append("<ul>" + "".join(items) + "</ul>")
            continue

        for ln in lines:
            st = ln.strip()
            if not st:
                continue
            if st.endswith(":") and len(st) < 40 and not looks_code(st):
                parts.append(f'<p class="label">{html.escape(st)}</p>')
            else:
                parts.append(f"<p>{inline(st)}</p>")
    return "\n".join(parts)


def format_quick_revision(body: str) -> str:
    lines = [ln.strip() for ln in body.split("\n") if ln.strip()]
    # Priority / numbered list section
    if any(re.match(r"^\d+\.\s+", ln) for ln in lines) and not any(
        "=" in ln and "?" in ln for ln in lines
    ):
        parts = []
        items = []
        for ln in lines:
            if ln.endswith(":") and not re.match(r"^\d+\.", ln):
                if items:
                    parts.append("<ol>" + "".join(items) + "</ol>")
                    items = []
                parts.append(f'<p class="label">{html.escape(ln)}</p>')
            elif re.match(r"^\d+\.\s+", ln):
                item_text = re.sub(r"^\d+\.\s+", "", ln)
                items.append(f"<li>{inline(item_text)}</li>")
            else:
                if items:
                    parts.append("<ol>" + "".join(items) + "</ol>")
                    items = []
                parts.append(f"<p>{inline(ln)}</p>")
        if items:
            parts.append("<ol>" + "".join(items) + "</ol>")
        return "\n".join(parts)

    cells = []
    for ln in lines:
        if "=" in ln and not ln.startswith("Q") and not looks_code(ln):
            left, right = ln.split("=", 1)
            cells.append(
                f'<div><div class="q">{html.escape(left.strip())}</div>'
                f"<div>{inline(right.strip())}</div></div>"
            )
        else:
            cells.append(f"<div><div>{inline(ln)}</div></div>")
    return f'<div class="rf">{"".join(cells)}</div>'


def build_html(sections) -> str:
    toc = []
    main = []
    q_total = 0

    for sec in sections:
        sid = f"part-{sec['num']:02d}"
        label = f"Part {sec['num']}: {sec['title']}"
        toc.append(f'<p class="toc-stage">{html.escape(label)}</p>')
        toc.append(f'<a href="#{sid}">{html.escape(label)}</a>')

        if sec["num"] == 1:
            main.append('<h1 class="stage">Core File Handling</h1>')
        elif sec["num"] == 8:
            main.append('<h1 class="stage">Modules</h1>')
        elif sec["num"] == 17:
            main.append('<h1 class="stage">Practice</h1>')
        elif sec["num"] == 21:
            main.append('<h1 class="stage">Revision</h1>')

        main.append(f'<h1 class="stage" id="{sid}">{html.escape(label)}</h1>')

        if any(k in sec["title"].lower() for k in ("quick revision", "rapid-fire", "most important")):
            # strip any Q blocks if present — part 21 is key=value
            # after last question? body is revision table only plus maybe no Qs
            # extract text after last Q if any
            body = sec["body"]
            qs = parse_questions(body)
            if qs and all(x.get("kind") == "q" for x in qs):
                # shouldn't happen for 21
                pass
            # remove leading Q blocks if mixed
            if re.search(r"^Q\d+\.", body, re.M):
                # take content that looks like key = value
                rev_lines = []
                for ln in body.split("\n"):
                    st = ln.strip()
                    if st and "=" in st and not st.startswith("Q") and not st.startswith("Ans"):
                        rev_lines.append(st)
                body = "\n".join(rev_lines)
            main.append(
                f'<article class="topic"><div class="body">{format_quick_revision(body)}</div></article>'
            )
            continue

        items = parse_questions(sec["body"])
        if not items:
            main.append(
                f'<article class="topic"><div class="body">{format_answer(sec["body"])}</div></article>'
            )
            continue

        for item in items:
            if item["kind"] == "sub":
                main.append(f'<p class="subhead">{html.escape(item["title"])}</p>')
                continue
            q_total += 1
            q = item["q"]
            if looks_code(q):
                head = f'<h2><span class="num">Q{item["n"]}</span></h2><pre><code>{html.escape(q)}</code></pre>'
            else:
                head = f'<h2><span class="num">Q{item["n"]}</span> {html.escape(q)}</h2>'
            toc.append(f'<a href="#q{item["n"]}">Q{item["n"]}. {html.escape(q[:55] + ("…" if len(q)>55 else ""))}</a>')
            main.append(
                f'<article class="topic" id="q{item["n"]}">{head}'
                f'<div class="body">{format_answer(item["a"])}</div></article>'
            )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<title>File Handling · Interview Notes</title>
<style>{CSS}</style>
</head>
<body>
<div class="layout">
<nav>
<h1>File Handling</h1>
<p class="sub">Complete interview notes</p>
{''.join(toc)}
</nav>
<main>
<div class="intro">
<h1>File Handling / Classes — Interview Q&amp;A</h1>
<p>Basics through modules (os, shutil, pathlib, csv, json, pickle), encoding, compression, coding, scenarios and rapid-fire.</p>
</div>
<p class="qmeta">{q_total} questions across {len(sections)} parts.</p>
{''.join(main)}
</main>
</div>
</body>
</html>
"""


def write_answer_docx(doc, ans: str) -> None:
    from docx.shared import Pt

    pos = 0
    for match in FENCE.finditer(ans):
        before = ans[pos : match.start()]
        if before.strip():
            write_plain_docx(doc, before)
        paragraph = doc.add_paragraph()
        run = paragraph.add_run(match.group(1).rstrip("\n"))
        run.font.name = "Courier New"
        run.font.size = Pt(9)
        pos = match.end()
    tail = ans[pos:]
    if tail.strip():
        write_plain_docx(doc, tail)


def write_plain_docx(doc, ans: str) -> None:
    from docx.shared import Pt

    for chunk in re.split(r"\n\s*\n", ans):
        chunk = chunk.strip()
        if not chunk:
            continue
        if looks_code(chunk) or chunk.startswith(("Output:", "Answer:")):
            paragraph = doc.add_paragraph()
            run = paragraph.add_run(chunk)
            run.font.name = "Courier New"
            run.font.size = Pt(9)
        else:
            for ln in chunk.split("\n"):
                st = ln.strip()
                if not st:
                    continue
                if st.startswith("- ") or re.match(r"^\d+\.\s+", st):
                    st2 = re.sub(r"^(-\s+|\d+\.\s+)", "", st)
                    doc.add_paragraph(st2, style="List Bullet")
                else:
                    doc.add_paragraph(st)


def build_docx(sections):
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    doc.add_heading("File Handling / Classes — Interview Q&A", 0)
    doc.add_paragraph(
        "Complete interview questions and answers: class/object through SOLID, "
        "coding, outputs, scenarios and quick revision."
    )

    for sec in sections:
        doc.add_heading(f'Part {sec["num"]}: {sec["title"]}', level=1)
        if any(k in sec["title"].lower() for k in ("quick revision", "rapid-fire", "most important")):
            for ln in sec["body"].split("\n"):
                st = ln.strip()
                if not st:
                    continue
                if re.match(r"^\d+\.\s+", st):
                    doc.add_paragraph(re.sub(r"^\d+\.\s+", "", st), style="List Number")
                else:
                    doc.add_paragraph(st)
            continue
        items = parse_questions(sec["body"])
        if not items:
            for ln in sec["body"].split("\n"):
                if ln.strip():
                    doc.add_paragraph(ln.strip())
            continue
        for item in items:
            if item["kind"] == "sub":
                doc.add_heading(item["title"], level=2)
                continue
            doc.add_heading(f'Q{item["n"]}. {item["q"]}', level=2)
            write_answer_docx(doc, item["a"])

    doc.save(DOCX_OUT)


def main():
    text = SRC.read_text(encoding="utf-8")
    sections = parse(text)
    HTML_OUT.write_text(build_html(sections), encoding="utf-8")
    build_docx(sections)
    print(f"sections={len(sections)}")
    for s in sections:
        items = parse_questions(s["body"])
        qs = sum(1 for x in items if x.get("kind") == "q")
        print(f"  {s['num']:2d} {s['title'][:40]:40} qs={qs}")
    print(f"wrote {HTML_OUT} ({HTML_OUT.stat().st_size} bytes)")
    print(f"wrote {DOCX_OUT} ({DOCX_OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
