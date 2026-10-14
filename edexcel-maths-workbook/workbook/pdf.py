"""Print layout: one PDF per module with tick boxes, working space and mark schemes."""
from __future__ import annotations

import os
from datetime import date
from xml.sax.saxutils import escape

import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)

from . import mathrender
from .mathrender import markup


_FONT_DIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
for name, file in [("Serif", "STIXGeneral.ttf"), ("Serif-Bold", "STIXGeneralBol.ttf"), ("Serif-Italic", "STIXGeneralItalic.ttf"),
                   ("Serif-BoldItalic", "STIXGeneralBolIta.ttf"), ("Sans", "DejaVuSans.ttf"), ("Sans-Bold", "DejaVuSans-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(_FONT_DIR, file)))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold", italic="Serif-Italic", boldItalic="Serif-BoldItalic")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans", boldItalic="Sans-Bold")

INK = colors.HexColor("#1d2433")
MUTED = colors.HexColor("#5b6478")
RULE = colors.HexColor("#c9cedb")
GRID = colors.HexColor("#e3e7ef")
ACCENT = colors.HexColor("#1f5fae")
TINT = colors.HexColor("#eef3fb")
GOOD = colors.HexColor("#1e7a4f")

ST = {
    "body": ParagraphStyle("body", fontName="Serif", fontSize=11, leading=15, textColor=INK, autoLeading="max"),
    "small": ParagraphStyle("small", fontName="Serif", fontSize=9.5, leading=12.5, textColor=INK, autoLeading="max"),
    "tiny": ParagraphStyle("tiny", fontName="Sans", fontSize=7.5, leading=9.5, textColor=MUTED),
    "label": ParagraphStyle("label", fontName="Sans-Bold", fontSize=7.5, leading=10, textColor=MUTED),
    "qhead": ParagraphStyle("qhead", fontName="Sans-Bold", fontSize=9.5, leading=12, textColor=INK),
    "h1": ParagraphStyle("h1", fontName="Sans-Bold", fontSize=22, leading=27, textColor=INK, spaceAfter=4),
    "h2": ParagraphStyle("h2", fontName="Sans-Bold", fontSize=15, leading=19, textColor=INK),
    "h3": ParagraphStyle("h3", fontName="Sans-Bold", fontSize=10.5, leading=14, textColor=ACCENT, spaceBefore=6, spaceAfter=2),
    "marks": ParagraphStyle("marks", fontName="Serif-Bold", fontSize=11, leading=15, alignment=TA_RIGHT, textColor=INK),
    "center": ParagraphStyle("center", fontName="Sans", fontSize=9, leading=12, alignment=TA_CENTER, textColor=MUTED),
}
BOX = '<font name="Sans" size="11">☐</font>'


def rich(text, style="body"):
    st = ST[style] if isinstance(style, str) else style
    return Paragraph(markup(text, st.fontSize), st)


class WorkingSpace(Flowable):
    """Squared-paper box for handwritten working."""

    def __init__(self, height, label="Working", grid=5 * mm):
        super().__init__()
        self.h, self.label, self.grid = height, label, grid

    def wrap(self, aw, ah):
        self.w = aw
        return aw, self.h

    def draw(self):
        c = self.canv
        c.setStrokeColor(GRID)
        c.setLineWidth(0.35)
        g = self.grid
        xx = g
        while xx < self.w:
            c.line(xx, 0, xx, self.h)
            xx += g
        yy = g
        while yy < self.h:
            c.line(0, yy, self.w, yy)
            yy += g
        c.setStrokeColor(RULE)
        c.setLineWidth(0.8)
        c.roundRect(0, 0, self.w, self.h, 3, stroke=1, fill=0)
        c.setFillColor(MUTED)
        c.setFont("Sans", 6.5)
        c.drawString(4, self.h - 9, self.label.upper())


class LinedBox(Flowable):
    """Ruled box for notes."""

    def __init__(self, height, label="My notes"):
        super().__init__()
        self.h, self.label = height, label

    def wrap(self, aw, ah):
        self.w = aw
        return aw, self.h

    def draw(self):
        c = self.canv
        c.setStrokeColor(GRID)
        c.setLineWidth(0.5)
        yy = 8 * mm
        while yy < self.h - 6 * mm:
            c.line(6, yy, self.w - 6, yy)
            yy += 8 * mm
        c.setStrokeColor(RULE)
        c.roundRect(0, 0, self.w, self.h, 3)
        c.setFillColor(MUTED)
        c.setFont("Sans", 6.5)
        c.drawString(4, self.h - 9, self.label.upper())


class Marker(Flowable):
    """Zero-size flowable that records the page it lands on (used to splice imported PDFs)."""

    def __init__(self, registry, key):
        super().__init__()
        self.registry, self.key = registry, key

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        self.registry[self.key] = self.canv.getPageNumber()


def _dots(d):
    return "●" * d + "○" * (3 - d)


def question_block(q, number, show_space=True):
    head = Table([[Paragraph(f"Q{number}", ST["qhead"]),
                   Paragraph(f"{escape(q.skill)} &nbsp;<font color='#5b6478'>{_dots(q.difficulty)}</font>", ST["label"]),
                   Paragraph(f"[{q.marks} mark{'s' if q.marks != 1 else ''}]", ST["label"]),
                   Paragraph(f"{BOX} Todo &nbsp;&nbsp;{BOX} Mastered", ST["qhead"])]],
                 colWidths=[23 * mm, None, 22 * mm, 46 * mm])
    head.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0, 0), (-1, -1), TINT),
                              ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                              ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("ALIGN", (3, 0), (3, 0), "RIGHT")]))
    flow = [head, Spacer(1, 4)]
    labels = [p.text for p in q.parts]
    stem_lines, part_lines = [], {}
    for line in (q.stem or "").split("\n"):
        tag = line[:3]
        if tag in labels and tag and sum(line.count(l) for l in labels if l) == 1:
            part_lines[tag] = line
        else:
            stem_lines.append(line)
    stem = "\n".join(stem_lines).strip()
    if stem:
        flow.append(rich(stem))
        flow.append(Spacer(1, 3))
    rows = []
    for p in q.parts:
        text = part_lines.get(p.text, p.text or "")
        rows.append([rich(text, "body"), Paragraph(f"({p.marks})", ST["marks"])])
    t = Table(rows, colWidths=[None, 14 * mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    flow.append(t)
    blocks = [KeepTogether(flow)]
    if show_space:
        h = min(max(26 * mm, 14 * mm + q.marks * 8.5 * mm), 120 * mm)
        blocks.append(Spacer(1, 3))
        blocks.append(WorkingSpace(h))
    blocks.append(Spacer(1, 9))
    return blocks


def checklist_table(items, cols=("Learnt", "Practised", "Mastered")):
    data = [[Paragraph("Skill", ST["label"])] + [Paragraph(c, ST["label"]) for c in cols]]
    for it in items:
        data.append([rich(it, "small")] + [Paragraph(BOX, ST["center"]) for _ in cols])
    t = Table(data, colWidths=[None] + [21 * mm] * len(cols), repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("ALIGN", (1, 0), (-1, -1), "CENTER"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def boxed(flowables, bg=TINT):
    t = Table([[f] for f in flowables], colWidths=[None])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def subtopic_intro(sub, notes, videos, include_notes=True):
    out = [Paragraph(f"{sub['id']} &nbsp;{escape(sub['title'])}", ST["h2"]), Spacer(1, 4)]
    n = notes.get(sub["id"])
    if include_notes and n:
        out.append(rich(n["summary"], "small"))
        out.append(Paragraph("Key facts", ST["h3"]))
        out.append(boxed([rich("• " + k, "small") for k in n["key"]]))
        out.append(Paragraph("Method", ST["h3"]))
        out += [rich("• " + m, "small") for m in n["method"]]
        out.append(Paragraph("Exam traps", ST["h3"]))
        out += [rich("• " + m, "small") for m in n["traps"]]
        out.append(rich("**In the exam:** " + n["exam"], "small"))
    out.append(Paragraph("Specification checklist", ST["h3"]))
    out.append(checklist_table([s[0] for s in sub["skills"]]))
    v = videos.get("subtopics", {}).get(sub["id"])
    if v:
        out.append(Paragraph("Videos (click to open)", ST["h3"]))
        lines = []
        for r in v["recap"][:3]:
            lines.append(f"{BOX} <b>Recap</b> — <a href='https://youtu.be/{r['id']}' color='#1f5fae'>{escape(r['title'])}</a> <font color='#5b6478'>({r['channel']})</font>")
        for s in v["skills"]:
            for vid in s["videos"][:1]:
                lines.append(f"{BOX} {escape(s['name'])} — <a href='https://youtu.be/{vid['id']}' color='#1f5fae'>{escape(vid['title'])}</a> <font color='#5b6478'>({vid['channel']})</font>")
        out += [Paragraph(l, ST["small"]) for l in lines]
    return out


def answer_block(q, number):
    flow = [Paragraph(f"Q{number} &nbsp;<font color='#5b6478' size='8'>{escape(q.skill)} · {q.marks} marks</font>", ST["qhead"])]
    for p in q.parts:
        lab = (p.text + " ") if p.text else ""
        flow.append(rich(f"**{lab}**{p.answer}" if lab else p.answer, "small"))
        if p.scheme:
            flow.append(rich("   " + "   ·   ".join(s for s in p.scheme if s), ST["tiny"]))
    flow.append(Spacer(1, 5))
    return KeepTogether(flow)


class Doc(BaseDocTemplate):
    def __init__(self, path, title, footer, pagesize=A4):
        super().__init__(path, pagesize=pagesize, leftMargin=17 * mm, rightMargin=17 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
                         title=title, author="Edexcel 9MA0 workbook builder")
        self.footer = footer
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate(id="cover", frames=[frame]), PageTemplate(id="main", frames=[frame], onPage=self._decorate)])

    def _decorate(self, c, d):
        c.saveState()
        c.setFont("Sans", 7.5)
        c.setFillColor(MUTED)
        c.drawString(self.leftMargin, 9 * mm, self.footer)
        c.drawRightString(self.pagesize[0] - self.rightMargin, 9 * mm, f"{c.getPageNumber()}")
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.line(self.leftMargin, 12.5 * mm, self.pagesize[0] - self.rightMargin, 12.5 * mm)
        c.restoreState()


def cover(module, qual, counts, seed, imported):
    total = sum(counts.values())
    out = [Spacer(1, 30 * mm), Paragraph(escape(qual), ST["label"]), Spacer(1, 4),
           Paragraph(f"Module {module['id'][1:]}", ST["h1"]), Paragraph(escape(module["title"]), ST["h2"]), Spacer(1, 6),
           Paragraph(f"{escape(module['papers'])} · {total} practice questions · answers and mark schemes at the back", ST["small"]), Spacer(1, 14)]
    rows = [[Paragraph("Subtopic", ST["label"]), Paragraph("Questions", ST["label"]), Paragraph("Done", ST["label"])]]
    for s in module["subtopics"]:
        rows.append([Paragraph(f"{s['id']} &nbsp;{escape(s['title'])}", ST["body"]), Paragraph(str(counts[s['id']] + imported.get(s['id'], 0)), ST["body"]), Paragraph(f"____ / {counts[s['id']] + imported.get(s['id'], 0)}", ST["body"])])
    t = Table(rows, colWidths=[None, 25 * mm, 30 * mm])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    out += [t, Spacer(1, 14), Paragraph("How to use this workbook", ST["h3"]),
            rich("1. Read the key facts and watch one video for the subtopic. Tick the skills checklist as you go.", "small"),
            rich("2. Attempt each question in the squared working space without notes. Mark it with the scheme at the back.", "small"),
            rich("3. Tick **Todo** when you have attempted it and **Mastered** only when you can redo it cold a week later.", "small"),
            rich("4. Copy any mistakes into the notes box at the end of the subtopic. Rebuild the workbook with a new seed for fresh questions.", "small"),
            Spacer(1, 10), Paragraph(f"Name ________________________ &nbsp;&nbsp; Started ____________ &nbsp;&nbsp; Built {date.today():%d %b %Y}, seed {seed}", ST["small"])]
    return out


def build_module_pdf(path, module, qual, questions, notes, videos, seed, imports=None, include_notes=True, pagesize=A4, show_space=True):
    """questions: dict subtopic_id -> list[Question]. imports: dict subtopic -> list of import dicts (count only here)."""
    imports = imports or {}
    markers: dict = {}
    counts = {s["id"]: len(questions.get(s["id"], [])) for s in module["subtopics"]}
    imported_counts = {k: len(v) for k, v in imports.items()}
    doc = Doc(path, f"Module {module['id'][1:]} — {module['title']}", f"Edexcel A-Level Maths 9MA0 · Module {module['id'][1:]}: {module['title']}", pagesize)
    story = cover(module, qual, counts, seed, imported_counts) + [NextPageTemplate("main"), PageBreak()]
    for s in module["subtopics"]:
        story += subtopic_intro(s, notes, videos, include_notes)
        story.append(PageBreak())
        for i, q in enumerate(questions.get(s["id"], []), 1):
            q.qid = f"{s['id']}.{i:02d}"
            story += question_block(q, q.qid, show_space)
        if imports.get(s["id"]):
            story.append(CondPageBreak(60 * mm))
            story.append(Paragraph(f"{s['id']} Your past-paper questions", ST["h3"]))
            for it in imports[s["id"]]:
                story.append(Paragraph(f"{BOX} Todo &nbsp;{BOX} Mastered &nbsp;&nbsp; {escape(it['label'])} <font color='#5b6478'>(pages follow)</font>", ST["small"]))
            story.append(Marker(markers, ("q", s["id"])))
            story.append(PageBreak())
        story.append(CondPageBreak(70 * mm))
        story.append(LinedBox(68 * mm, f"My notes — {s['id']} {s['title']}: mistakes to remember"))
        story.append(PageBreak())
    story.append(Paragraph("Answers and mark schemes", ST["h1"]))
    story.append(rich("M = method mark, A = accuracy mark (depends on the preceding M), B = independent mark, ft = follow-through, * = given answer. Numerical answers are to 3 s.f. unless stated.", "small"))
    story.append(Spacer(1, 8))
    for s in module["subtopics"]:
        story.append(CondPageBreak(40 * mm))
        story.append(Paragraph(f"{s['id']} {escape(s['title'])}", ST["h3"]))
        for q in questions.get(s["id"], []):
            story.append(answer_block(q, q.qid))
        if imports.get(s["id"]):
            story.append(Paragraph(f"Mark schemes for your past-paper questions ({s['id']}) follow.", ST["small"]))
            story.append(Marker(markers, ("ms", s["id"])))
            story.append(PageBreak())
    doc.build(story)
    return markers
