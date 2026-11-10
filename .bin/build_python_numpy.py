#!/usr/bin/env python3
"""Build NumPy interview prep HTML + DOCX."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / ".bin" / "python-numpy-source.txt"
HTML_OUT = ROOT / "html" / "python-numpy.html"
DOCX_OUT = ROOT / "docs" / "python-numpy.docx"

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
    .diff-row {
      display: grid;
      grid-template-columns: 180px 1fr;
      gap: 10px;
      border-top: 1px solid var(--line);
      padding: 8px 0;
      font-size: 14px;
    }
    .diff-row:first-child { border-top: none; }
    .diff-row strong { color: var(--accent); }
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
      .rf, .diff-row { grid-template-columns: 1fr; }
    }
"""


def nice_title(title: str) -> str:
    t = title.title()
    for a, b in [
        ("Numpy", "NumPy"),
        ("Nan", "NaN"),
        ("Based", "Based"),
        (" And ", " and "),
        (" Of ", " of "),
        (" For ", " for "),
        (" To ", " to "),
        (" On ", " on "),
        (" Vs ", " vs "),
    ]:
        t = t.replace(a, b)
    return t


def parse(text: str):
    lines = text.replace("\r\n", "\n").split("\n")
    sections = []
    i = 0
    # skip to first numbered section after CONTENTS
    while i < len(lines):
        s = lines[i].strip()
        m = re.match(r"^(\d{2})\.\s+(.+)$", s)
        if m and i + 1 < len(lines) and set(lines[i + 1].strip()) <= {"="}:
            # real section
            break
        if s.startswith("MOST IMPORTANT TOPICS") and i + 1 < len(lines) and set(lines[i + 1].strip()) <= {"="}:
            break
        if s.startswith("REMEMBER:"):
            break
        i += 1

    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("END OF NUMPY") or (s.startswith("====") and "END" in "".join(lines[max(0, i - 2) : i + 1])):
            # continue for REMEMBER / MOST IMPORTANT after end? handle below
            pass

        m = re.match(r"^(\d{2})\.\s+(.+)$", s)
        if m and i + 1 < len(lines) and set(lines[i + 1].strip()) <= {"="} and len(lines[i + 1].strip()) >= 10:
            num = int(m.group(1))
            title = nice_title(m.group(2).strip())
            i += 2
            body_lines = []
            while i < len(lines):
                t = lines[i].strip()
                if re.match(r"^(\d{2})\.\s+.+", t):
                    k = i + 1
                    if k < len(lines) and set(lines[k].strip()) <= {"="} and len(lines[k].strip()) >= 10:
                        break
                if t.startswith("MOST IMPORTANT TOPICS"):
                    break
                if t.startswith("END OF NUMPY"):
                    break
                if t.startswith("REMEMBER:"):
                    break
                body_lines.append(lines[i])
                i += 1
            sections.append(
                {
                    "kind": "section",
                    "num": num,
                    "title": title,
                    "body": "\n".join(body_lines).strip(),
                }
            )
            continue

        if s.startswith("MOST IMPORTANT TOPICS"):
            i += 1
            while i < len(lines) and (not lines[i].strip() or set(lines[i].strip()) <= {"="}):
                i += 1
            body = []
            while i < len(lines):
                t = lines[i].strip()
                if t.startswith("====") or t.startswith("END OF") or t.startswith("REMEMBER:"):
                    break
                body.append(lines[i])
                i += 1
            sections.append(
                {
                    "kind": "list",
                    "num": None,
                    "title": "Most Important Topics for Interviews",
                    "body": "\n".join(body).strip(),
                }
            )
            continue

        if s.startswith("REMEMBER:"):
            body = [s]
            i += 1
            while i < len(lines):
                t = lines[i].strip()
                if t.startswith("====") and "END" not in t:
                    # trailing banner
                    if i + 1 < len(lines) and not lines[i + 1].strip():
                        break
                if t.startswith("END OF"):
                    break
                body.append(lines[i])
                i += 1
            sections.append(
                {
                    "kind": "note",
                    "num": None,
                    "title": "Remember",
                    "body": "\n".join(body).strip(),
                }
            )
            continue

        i += 1
    return sections


def parse_questions(body: str):
    """Return list of {q, a} from Qn. / Ans: blocks."""
    items = []
    parts = re.split(r"(?=^Q\d+\.)", body, flags=re.M)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.match(r"^Q(\d+)\.\s*(.*)$", part, re.S)
        if not m:
            continue
        qn = m.group(1)
        rest = m.group(2).strip()
        # Ans: may be missing for coding-only
        if re.search(r"(?m)^Ans:\s*", rest):
            qtext, ans = re.split(r"(?m)^Ans:\s*", rest, maxsplit=1)
            q = qtext.strip()
            a = ans.strip()
        elif re.search(r"(?m)^Answer:\s*", rest):
            qtext, ans = re.split(r"(?m)^Answer:\s*", rest, maxsplit=1)
            q = qtext.strip() or f"Output question {qn}"
            a = "Answer:\n" + ans.strip()
        else:
            # question may be empty; rest is code example
            lines = rest.split("\n")
            # first line(s) until blank then code, or all is answer/code
            q = ""
            a = rest
            # If first non-empty looks like prose question ending with ?
            if lines and lines[0].strip().endswith("?"):
                q = lines[0].strip()
                a = "\n".join(lines[1:]).strip()
            elif lines and not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*\s*=", lines[0].strip()) and not lines[0].strip().startswith(("import ", "print(", "np.", "rng.")):
                # take first paragraph as question if short
                if len(lines[0].strip()) < 120 and not lines[0].strip().startswith("["):
                    q = lines[0].strip()
                    a = "\n".join(lines[1:]).strip()
        if not q:
            q = f"Question {qn}"
        # unwrap leading code-as-question for output qs where q was code
        items.append({"n": int(qn), "q": q, "a": a})
    return items


def inline(text: str) -> str:
    esc = html.escape(text)
    esc = re.sub(r"`([^`]+)`", r"<code>\1</code>", esc)
    esc = re.sub(r"\b(np\.[a-zA-Z_][\w\.]*)\b", r"<code>\1</code>", esc)
    esc = re.sub(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\(\)", r"<code>\1()</code>", esc)
    return esc


def looks_code(chunk: str) -> bool:
    lines = [ln for ln in chunk.split("\n") if ln.strip()]
    if not lines:
        return False
    hits = 0
    for ln in lines:
        st = ln.strip()
        if st.startswith(("Output:", "Answer:", "OUTPUT:", "Python List:", "NumPy Array:", "NumPy:", "Pandas:", "concatenate:", "stack:", "split =", "array_split =", "flatten():", "ravel():", "dot():", "matmul():", "loadtxt:", "genfromtxt:", "rand =", "randint =", "* =", "@ =", "Copy:", "View:", "arange():", "linspace():", "Module:", "Function:", "Example:")):
            continue
        if (
            st.startswith(("import ", "from ", "print(", "np.", "rng.", "pip "))
            or re.match(r"^[a-zA-Z_][\w\.]*\s*=", st)
            or st.startswith("[[")
            or (st.startswith("[") and st.endswith("]"))
            or st.startswith("<class")
        ):
            hits += 1
    return hits >= max(1, (len(lines) + 1) // 2)


def format_answer(ans: str) -> str:
    if not ans:
        return ""
    parts = []
    # normalize Output:/Answer:
    chunks = re.split(r"\n\s*\n", ans)
    for chunk in chunks:
        chunk = chunk.strip("\n")
        if not chunk.strip():
            continue
        lines = chunk.split("\n")
        # labeled comparison blocks
        if any(ln.strip().endswith(":") and len(ln.strip()) < 40 for ln in lines[:3]) and len(lines) >= 2:
            # render as paragraphs + bullets
            items = []
            for ln in lines:
                st = ln.strip()
                if not st:
                    continue
                if st.endswith(":") and not st.startswith(("import", "print", "np.", "a ", "b ")):
                    if items:
                        parts.append("<ul>" + "".join(items) + "</ul>")
                        items = []
                    parts.append(f'<p class="label">{html.escape(st)}</p>')
                elif st.startswith("- ") or re.match(r"^\d+\.\s+", st):
                    st2 = re.sub(r"^(-\s+|\d+\.\s+)", "", st)
                    items.append(f"<li>{inline(st2)}</li>")
                elif looks_code(st) or (items and st.startswith(" ")):
                    if items:
                        parts.append("<ul>" + "".join(items) + "</ul>")
                        items = []
                    # fall through later
                    parts.append(f"<p>{inline(st)}</p>")
                else:
                    if items and not st.startswith("-"):
                        # maybe still a bullet-like line under a label
                        if st[0].islower() or st.startswith(("Faster", "Efficient", "Useful", "Supports", "Generally", "Requires", "Built", "Can ", "Designed", "Main ", "Works ", "Numerical", "Data ", "Uses ", "Creates ", "Returns ", "Always ", "Modifies ", "Equal ", "Unequal", "Vertical", "Horizontal", "Independent", "Shares", "Number", "Dimension", "Step ", "Average", "Square", "Index", "Value", "Clean", "More ", "Random", "Suitable", "Simpler", "Flexible")):
                            items.append(f"<li>{inline(st)}</li>")
                        else:
                            if items:
                                parts.append("<ul>" + "".join(items) + "</ul>")
                                items = []
                            parts.append(f"<p>{inline(st)}</p>")
                    else:
                        parts.append(f"<p>{inline(st)}</p>")
            if items:
                parts.append("<ul>" + "".join(items) + "</ul>")
            continue

        if looks_code(chunk) or chunk.strip().startswith(("Output:", "Answer:", "OUTPUT:")):
            # split output
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

        # bullet list
        if all(
            (not ln.strip())
            or ln.strip().startswith("- ")
            or re.match(r"^\d+\.\s+", ln.strip())
            or ln.strip().endswith(":")
            for ln in lines
        ) and any(ln.strip().startswith("- ") or re.match(r"^\d+\.\s+", ln.strip()) for ln in lines):
            items = []
            for ln in lines:
                st = ln.strip()
                if not st:
                    continue
                if st.endswith(":") and not st.startswith("-"):
                    if items:
                        parts.append("<ul>" + "".join(items) + "</ul>")
                        items = []
                    parts.append(f'<p class="label">{html.escape(st)}</p>')
                else:
                    st2 = re.sub(r"^(-\s+|\d+\.\s+)", "", st)
                    items.append(f"<li>{inline(st2)}</li>")
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


def format_section_body(sec) -> str:
    body = sec["body"]
    title = sec["title"].lower()

    # Difference section (20): lines like "X vs Y: ..."
    if "difference-based" in title:
        rows = []
        for ln in body.split("\n"):
            st = ln.strip()
            if not st:
                continue
            if ":" in st:
                left, right = st.split(":", 1)
                rows.append(
                    f'<div class="diff-row"><strong>{html.escape(left.strip())}</strong>'
                    f"<span>{inline(right.strip())}</span></div>"
                )
            else:
                rows.append(f"<p>{inline(st)}</p>")
        return "".join(rows)

    # Rapid fire (25): Question?\nAnswer.
    if "rapid-fire" in title:
        lines = [ln.strip() for ln in body.split("\n") if ln.strip()]
        pairs = []
        i = 0
        while i < len(lines):
            q = lines[i]
            a = lines[i + 1] if i + 1 < len(lines) else ""
            # questions often end with ?
            if q.endswith("?") and a and not a.endswith("?"):
                pairs.append((q, a))
                i += 2
            else:
                pairs.append((q, ""))
                i += 1
        cells = []
        for q, a in pairs:
            cells.append(
                f'<div><div class="q">{html.escape(q)}</div><div>{inline(a)}</div></div>'
            )
        return f'<div class="rf">{"".join(cells)}</div>'

    # Roadmap / list / note without Qs
    if sec["kind"] in ("list", "note") or "roadmap" in title:
        parts = []
        for chunk in re.split(r"\n\s*\n", body):
            chunk = chunk.strip()
            if not chunk:
                continue
            lines = chunk.split("\n")
            if lines[0].strip().startswith("DAY ") or (
                lines[0].strip().endswith(":") and len(lines[0].strip()) < 40
            ):
                parts.append(f'<p class="label">{html.escape(lines[0].strip())}</p>')
                items = []
                for ln in lines[1:]:
                    st = ln.strip().lstrip("- ").strip()
                    if st:
                        items.append(f"<li>{inline(st)}</li>")
                if items:
                    parts.append("<ul>" + "".join(items) + "</ul>")
            elif all(re.match(r"^\d+\.\s+", ln.strip()) for ln in lines if ln.strip()):
                items = []
                for ln in lines:
                    st = re.sub(r"^\d+\.\s+", "", ln.strip())
                    if st:
                        items.append(f"<li>{inline(st)}</li>")
                parts.append("<ol>" + "".join(items) + "</ol>")
            else:
                for ln in lines:
                    st = ln.strip()
                    if st.startswith("- "):
                        # collect later
                        pass
                    if st:
                        parts.append(f"<p>{inline(st)}</p>")
        return "\n".join(parts)

    qs = parse_questions(body)
    if not qs:
        # fallback plain
        return format_answer(body)

    out = []
    for item in qs:
        qhtml = html.escape(item["q"]) if item["q"] else ""
        # if question itself is code-looking for output questions, show as pre
        if item["q"] and looks_code(item["q"]):
            head = f'<h2><span class="num">Q{item["n"]}</span></h2><pre><code>{html.escape(item["q"])}</code></pre>'
        else:
            head = f'<h2><span class="num">Q{item["n"]}</span> {qhtml}</h2>'
        out.append(
            f'<article class="topic" id="q{item["n"]}">{head}'
            f'<div class="body">{format_answer(item["a"])}</div></article>'
        )
    return "\n".join(out)


def build_html(sections) -> str:
    toc = []
    main = []
    q_total = 0
    for sec in sections:
        sid = re.sub(r"[^a-z0-9]+", "-", (f'{sec.get("num"):02d}-' if sec.get("num") else "") + sec["title"].lower()).strip("-")
        label = f'{sec["num"]:02d}. {sec["title"]}' if sec.get("num") else sec["title"]
        toc.append(f'<p class="toc-stage">{html.escape(label)}</p>')
        toc.append(f'<a href="#{sid}">{html.escape(label)}</a>')

        body_html = format_section_body(sec)
        # count questions for meta
        qs = parse_questions(sec["body"]) if sec["kind"] == "section" else []
        q_total += len(qs)

        if sec.get("num") == 1:
            main.append('<h1 class="stage">Core Topics</h1>')
        elif sec.get("num") == 20:
            main.append('<h1 class="stage">Interview Practice</h1>')
        elif sec.get("num") == 26 or sec["title"].startswith("Most Important"):
            main.append('<h1 class="stage">Plan &amp; Focus</h1>')

        # For Q sections, body already has articles; wrap with stage header only
        if qs:
            # add short TOC links for first few? skip to keep nav light — just section jump
            main.append(f'<h1 class="stage" id="{sid}">{html.escape(label)}</h1>')
            main.append(body_html)
        else:
            main.append(
                f'<article class="topic" id="{sid}"><h2>{html.escape(label)}</h2>'
                f'<div class="body">{body_html}</div></article>'
            )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<title>NumPy · Interview Preparation</title>
<style>{CSS}</style>
</head>
<body>
<div class="layout">
<nav>
<h1>NumPy Interview</h1>
<p class="sub">Beginner → advanced · full prep</p>
{''.join(toc)}
</nav>
<main>
<div class="intro">
<h1>NumPy Complete Interview Preparation</h1>
<p>Beginner to advanced: fundamentals through coding programs, differences, outputs, scenarios, rapid-fire and a 7-day roadmap.</p>
</div>
<p class="qmeta">{q_total} numbered questions across {sum(1 for s in sections if s.get('num'))} topics.</p>
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

    doc.add_heading("NumPy Complete Interview Preparation", 0)
    doc.add_paragraph("Beginner to advanced level. Theory, differences, outputs, scenarios, coding and revision.")

    for sec in sections:
        label = f'{sec["num"]:02d}. {sec["title"]}' if sec.get("num") else sec["title"]
        doc.add_heading(label, level=1)
        qs = parse_questions(sec["body"]) if sec["kind"] == "section" else []
        if qs:
            for item in qs:
                doc.add_heading(f'Q{item["n"]}. {item["q"]}', level=2)
                a = item["a"]
                for chunk in re.split(r"\n\s*\n", a):
                    chunk = chunk.strip()
                    if not chunk:
                        continue
                    if looks_code(chunk) or chunk.startswith(("Output:", "Answer:")):
                        p = doc.add_paragraph()
                        run = p.add_run(chunk)
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
        else:
            for ln in sec["body"].split("\n"):
                st = ln.strip()
                if not st:
                    continue
                if st.startswith("- ") or re.match(r"^\d+\.\s+", st):
                    st2 = re.sub(r"^(-\s+|\d+\.\s+)", "", st)
                    doc.add_paragraph(st2, style="List Bullet")
                else:
                    doc.add_paragraph(st)

    doc.save(DOCX_OUT)


def main():
    text = SRC.read_text(encoding="utf-8")
    sections = parse(text)
    HTML_OUT.write_text(build_html(sections), encoding="utf-8")
    build_docx(sections)
    print(f"sections={len(sections)}")
    for s in sections:
        qs = parse_questions(s["body"]) if s["kind"] == "section" else []
        print(f"  {s.get('num') or '-':>3} {s['title'][:42]:42} qs={len(qs)}")
    print(f"wrote {HTML_OUT} ({HTML_OUT.stat().st_size} bytes)")
    print(f"wrote {DOCX_OUT} ({DOCX_OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
