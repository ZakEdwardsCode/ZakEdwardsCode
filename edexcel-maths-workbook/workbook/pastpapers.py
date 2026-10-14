"""Real Pearson Edexcel past-paper questions (9MA0, IAL P1-P4, legacy C1-C4): download, select by topic, stamp, print.

The papers themselves are not stored in this repository. `fetch()` downloads the official question
papers and mark schemes (as published by Pearson, mirrored by Physics & Maths Tutor) into a local
cache, and booklets are cut from those files on your machine for your own revision.
"""
from __future__ import annotations

import io
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .core import load_json

BASE = "https://pmt.physicsandmathstutor.com/download/Maths/A-level/Papers/Edexcel/"
_SERIES = [("SP", "Specimen", "Specimen", 2017), ("J18", "June 2018", "June 2018", 2018), ("J19", "June 2019", "June 2019", 2019),
           ("O20", "October 2020", "October 2020", 2020), ("O21", "October 2021", "October 2021", 2021), ("J22", "June 2022", "June 2022", 2022),
           ("J23", "June 2023", "June 2023", 2023), ("J24", "June 2024", "June 2024", 2024), ("J25", "June 2025", "June 2025", 2025)]


def _sources():
    out = []
    for code, fname, label, year in _SERIES:
        for paper, title in (("1", "Paper 1 (Pure 1)"), ("2", "Paper 2 (Pure 2)")):
            out.append({"id": f"P{paper}-{code}", "label": f"{label} {title}", "paper": paper, "series": label, "year": year,
                        "qp": f"Paper-{paper}/QP/{fname} QP.pdf", "ms": f"Paper-{paper}/MS/{fname} MS.pdf"})
        if code == "SP":
            continue  # the specimen Paper 3 has no answer spaces, so it is not useful for printing
        if code == "J18":
            out.append({"id": "P3-J18", "label": f"{label} Paper 3 (Statistics & Mechanics)", "paper": "3", "series": label, "year": year,
                        "qp": f"Paper-3/QP/{fname} QP.pdf", "ms": f"Paper-3/MS/{fname} MS.pdf"})
            continue
        for kind, name in (("S", "Stats"), ("M", "Mech")):
            out.append({"id": f"P3{kind}-{code}", "label": f"{label} Paper 3 {'Statistics' if kind == 'S' else 'Mechanics'}", "paper": "3" + kind,
                        "series": label, "year": year, "qp": f"Paper-3/QP/{fname} QP ({name}).pdf", "ms": f"Paper-3/MS/{fname} MS ({name}).pdf"})
    return out


LEGACY_BASE = "https://pmt.physicsandmathstutor.com/download/Maths/A-level/"


def _legacy():
    out = []
    for unit, name in (("C1", "Core Mathematics C1"), ("C2", "Core Mathematics C2")):
        for year in (2017, 2018):
            out.append({"id": f"{unit}-J{str(year)[2:]}", "label": f"June {year} {unit} (legacy)", "paper": unit, "series": f"June {year}", "year": year,
                        "qp": f"legacy/{unit}/Papers-Edexcel/QP/June {year} QP.pdf", "ms": f"legacy/{unit}/Papers-Edexcel/MS/June {year} MS.pdf",
                        "legacy": True})
    return out


SOURCES = _sources() + _legacy()


def cache_path(cache, rel):
    return Path(cache) / rel


def url(rel):
    if rel.startswith("legacy/"):
        return urllib.parse.quote(LEGACY_BASE + rel[len("legacy/"):], safe=":/")
    return urllib.parse.quote(BASE + rel, safe=":/")


def fetch(cache="papers_cache", quiet=False):
    """Download every question paper and mark scheme that is not already cached."""
    cache = Path(cache)
    todo = list(dict.fromkeys(rel for p in index() for rel in (p["qp"], p["ms"])))
    for rel in todo:
        dest = cache_path(cache, rel)
        if dest.exists() and dest.stat().st_size > 10_000:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(5):
            try:
                req = urllib.request.Request(url(rel), headers={"User-Agent": "Mozilla/5.0 (revision workbook builder)"})
                data = urllib.request.urlopen(req, timeout=60).read()
                if not data.startswith(b"%PDF"):
                    raise ValueError("not a PDF")
                dest.write_bytes(data)
                if not quiet:
                    print(f"  downloaded {rel} ({len(data) // 1024} KB)")
                break
            except Exception as e:  # noqa: BLE001
                if attempt == 4:
                    print(f"  FAILED {rel}: {e}")
                time.sleep(2 ** attempt)
    missing = [rel for rel in todo if not cache_path(cache, rel).exists()]
    return missing


def index():
    return load_json("past_papers.json")


def all_questions():
    out = []
    for p in index():
        for q in p["questions"]:
            out.append({**q, "paper_id": p["id"], "paper_label": p["label"], "year": p["year"], "qp": p["qp"], "ms": p["ms"], "paper": p["paper"]})
    return out


def _short(p_label, n):
    return f"{p_label} Q{n}"


def titles():
    """Section titles for subtopic ids ("1.2") and skill codes ("1.2.3")."""
    out = {}
    for m in load_json("taxonomy.json")["modules"]:
        for s in m["subtopics"]:
            out[s["id"]] = s["title"]
            for i, k in enumerate(s["skills"]):
                out[f"{s['id']}.{i}"] = f"{s['title']}: {k[0]}"
    return out


def select(topics=None, modules=None, skills=None, years=None, papers=None, primary_only=False):
    """Group matching questions into {section_id: [questions]} in syllabus order.

    Every question carries skill codes "S.T.I" (main skill first). Modules and topics give one
    section per subtopic; skills ("1.2.3" exact codes, or words matched against skill names) give
    one section per skill. A question appears once per booklet, under the first of its tags you
    selected; with primary_only it is only picked up by its main skill.
    """
    tax = load_json("taxonomy.json")
    names = titles()
    order = []
    for m in tax["modules"]:
        for s in m["subtopics"]:
            order.append(s["id"])
            order += [f"{s['id']}.{i}" for i in range(len(s["skills"]))]
    codes = [c for c in order if c.count(".") == 2]
    by_topic = set()
    for m in tax["modules"]:
        for s in m["subtopics"]:
            if (modules and int(m["id"][1:]) in modules) or (topics and s["id"] in topics):
                by_topic.add(s["id"])
    if not (topics or modules or skills):
        by_topic = {c for c in order if c.count(".") == 1}
    by_skill = set()
    for k in skills or []:
        if k in codes:
            by_skill.add(k)
        elif k.count(".") == 1 and k + ".0" in codes:
            by_skill |= {c for c in codes if c.startswith(k + ".")}
        else:
            by_skill |= {c for c in codes if k.lower() in names[c].lower()}

    def home(code):
        if code in by_skill:
            return code
        topic = code.rsplit(".", 1)[0]
        return topic if topic in by_topic else None

    sections: dict[str, list] = {}
    for q in sorted(all_questions(), key=lambda q: (-q["year"], q["paper"], q["n"])):
        if not q["skills"] or (years and q["year"] not in years):
            continue
        if papers and not any(q["paper"].upper().startswith(str(p).upper()) for p in papers):
            continue
        sid = next((h for h in map(home, q["skills"][:1] if primary_only else q["skills"]) if h), None)
        if sid:
            sections.setdefault(sid, []).append(q)
    return {sid: sections[sid] for sid in order if sid in sections}


def _stamp_overlay(page, left, right):
    """A white strip across the top of the visible (crop) area with the label and tick boxes.

    Uses the built-in Helvetica (not embedded) and drawn squares, so each stamp adds ~1 KB.
    `right` is a list of box labels, or a plain string.
    """
    mw, mh = float(page.mediabox.width), float(page.mediabox.height)
    cb = page.cropbox
    x0, x1, top = float(cb.left), float(cb.right), float(cb.top)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(mw, mh))
    c.setFillColor(HexColor("#ffffff"))
    c.rect(x0, top - 20, x1 - x0, 20, stroke=0, fill=1)
    c.setFillColor(HexColor("#1d2433"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x0 + 24, top - 13, left)
    c.setFont("Helvetica", 8)
    x = x1 - 24
    if isinstance(right, str):
        c.drawRightString(x, top - 13, right)
    else:
        for item in reversed(right):
            w = c.stringWidth(item, "Helvetica", 8)
            c.drawString(x - w, top - 13, item)
            x -= w + 12
            if not item.startswith("Score"):
                c.setStrokeColor(HexColor("#1d2433"))
                c.setLineWidth(0.7)
                c.rect(x, top - 14.5, 8, 8, stroke=1, fill=0)
                x -= 10
    c.setStrokeColor(HexColor("#9aa3b5"))
    c.setLineWidth(0.5)
    c.line(x0 + 24, top - 19, x1 - 24, top - 19)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def _stamped(page, left, right):
    page.merge_page(_stamp_overlay(page, left, right))
    return page


def build_booklet(path, title, sections, cache="papers_cache", include_ms=True, ms_inline=False, subtitle=""):
    """Write one printable PDF: cover + checklist, topic dividers, stamped question pages, mark schemes."""
    from . import pdf as layout  # registers fonts
    from reportlab.lib.units import mm
    from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle
    from xml.sax.saxutils import escape

    names = titles()
    readers: dict[str, PdfReader] = {}

    def reader(rel):
        if rel not in readers:
            readers[rel] = PdfReader(str(cache_path(cache, rel)))
        return readers[rel]

    # front matter: cover + checklist, rendered with reportlab
    total_q = sum(len(v) for v in sections.values())
    total_m = sum(q["marks"] for v in sections.values() for q in v)
    story = [Spacer(1, 18 * mm), Paragraph("Pearson Edexcel A-Level Mathematics · real past-paper questions (9MA0, IAL and legacy papers)", layout.ST["label"]),
             Spacer(1, 4), Paragraph(escape(title), layout.ST["h1"])]
    if subtitle:
        story.append(Paragraph(escape(subtitle), layout.ST["small"]))
    story += [Spacer(1, 4), Paragraph(f"{total_q} questions · {total_m} marks · printed on the original exam pages with their answer space"
                                      + (" · mark schemes " + ("after each question" if ms_inline else "at the back") if include_ms else ""), layout.ST["small"]),
              Spacer(1, 10)]
    for sid, qs in sections.items():
        rows = [[Paragraph(f"<b>{sid} {escape(names[sid])}</b>", layout.ST["small"]), Paragraph("Marks", layout.ST["label"]), Paragraph("Todo", layout.ST["label"]), Paragraph("Mastered", layout.ST["label"])]]
        for q in qs:
            extra = " — " + names[q["skills"][0]].split(": ", 1)[1]
            rows.append([Paragraph(escape(_short(q["paper_label"], q["n"]) + extra), layout.ST["small"]), Paragraph(str(q["marks"]), layout.ST["small"]),
                         Paragraph(layout.BOX, layout.ST["center"]), Paragraph(layout.BOX, layout.ST["center"])])
        t = Table(rows, colWidths=[None, 14 * mm, 14 * mm, 18 * mm], repeatRows=1)
        t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, layout.RULE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("ALIGN", (1, 0), (-1, -1), "CENTER"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
        story += [t, Spacer(1, 8)]
    story += [Spacer(1, 6), Paragraph(f"Built {date.today():%d %b %Y}. Questions © Pearson Education Ltd, for personal revision only.", layout.ST["tiny"])]

    # front matter and every divider page in ONE reportlab document, so fonts are embedded once
    dividers = [(f"{sid} {names[sid]}", f"{len(qs)} questions \u00b7 {sum(q['marks'] for q in qs)} marks") for sid, qs in sections.items()]
    if include_ms and not ms_inline:
        dividers.append(("Mark schemes", "In the same order as the questions. Each page is labelled with the question it belongs to."))
    marks_at: dict = {}
    flow = [layout.NextPageTemplate("main")] + story
    for k, (text, sub) in enumerate(dividers):
        flow += [PageBreak(), layout.Marker(marks_at, k), Spacer(1, 90 * mm), Paragraph(escape(text), layout.ST["h1"]), Paragraph(escape(sub), layout.ST["small"])]
    front = io.BytesIO()
    layout.Doc(front, title, f"Edexcel past papers \u00b7 {title}").build(flow)
    front.seek(0)
    fr = PdfReader(front)
    n_front = marks_at[0] - 1 if dividers else len(fr.pages)
    writer = PdfWriter()
    for pg in fr.pages[:n_front]:
        writer.add_page(pg)
    div_iter = iter(range(len(dividers)))

    def add_divider(_text=None, _sub=None):
        k = next(div_iter)
        writer.add_page(fr.pages[marks_at[k] - 1])

    def add_pages(rel, pages, left, right):
        r = reader(rel)
        for p in pages:
            if 1 <= p <= len(r.pages):
                writer.add_page(_stamped(r.pages[p - 1], left, right))

    for sid, qs in sections.items():
        add_divider(f"{sid} {names[sid]}", f"{len(qs)} questions · {sum(q['marks'] for q in qs)} marks")
        for q in qs:
            label = f"{sid} {names[sid]}  |  {_short(q['paper_label'], q['n'])}  |  {q['marks']} marks"
            add_pages(q["qp"], q["pages"], label, ["Todo", "Mastered", "Score ____ / " + str(q["marks"])])
            if include_ms and ms_inline:
                a, b = q["ms_pages"]
                add_pages(q["ms"], range(a, b + 1), "Mark scheme  |  " + _short(q["paper_label"], q["n"]), "rows for Q" + str(q["n"]))
            if len(writer.pages) % 2 and False:
                pass
    if include_ms and not ms_inline:
        add_divider("Mark schemes", "In the same order as the questions. Each page is labelled with the question it belongs to.")
        for sid, qs in sections.items():
            for q in qs:
                a, b = q["ms_pages"]
                add_pages(q["ms"], range(a, b + 1), f"Mark scheme  |  {_short(q['paper_label'], q['n'])}", f"{sid} {names[sid]}  |  rows for Q{q['n']}")
    with open(path, "wb") as fh:
        writer.write(fh)
    _optimise(path)
    return len(writer.pages)


def _optimise(path):
    """Shrink the file with pikepdf (object streams, recompression) when it is installed."""
    try:
        import pikepdf
    except ImportError:
        return
    tmp = str(path) + ".tmp"
    with pikepdf.open(path) as pdf:
        pdf.remove_unreferenced_resources()
        pdf.save(tmp, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate, recompress_flate=True)
    Path(tmp).replace(path)
