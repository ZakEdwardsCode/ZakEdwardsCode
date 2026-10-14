"""Question selection, PDF splicing for imported past papers, and the page-tagging helper."""
from __future__ import annotations

import csv
import io
import json
import random
import re
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

from . import generators  # noqa: F401  (registers generators)
from .core import REGISTRY, load_json
from .pdf import build_module_pdf


def select_questions(subtopic: str, count: int, seed: int):
    """Draw `count` distinct questions, covering every skill before repeating one, easiest first."""
    gens = REGISTRY.get(subtopic, [])
    if not gens or count <= 0:
        return []
    rng = random.Random(f"{seed}:{subtopic}")
    by_skill: dict[str, list] = {}
    for g in gens:
        by_skill.setdefault(g.skill, []).append(g)
    skills = list(by_skill)
    rng.shuffle(skills)
    out, seen, attempts, i = [], set(), 0, 0
    while len(out) < count and attempts < count * 40:
        skill = skills[i % len(skills)]
        g = rng.choice(by_skill[skill])
        q = g(random.Random(rng.getrandbits(64)))
        key = (q.stem, tuple(p.answer for p in q.parts))
        attempts += 1
        i += 1
        if key in seen:
            continue
        seen.add(key)
        out.append(q)
    out.sort(key=lambda q: q.difficulty)
    return out


def read_imports(path):
    """CSV columns: subtopic,label,pdf,pages,ms_pdf,ms_pages (pages like '3-5,7')."""
    if not path:
        return {}
    base = Path(path).parent
    out: dict[str, list] = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if not row.get("subtopic") or not row.get("pdf"):
                continue
            row = {k: (v or "").strip() for k, v in row.items()}
            for key in ("pdf", "ms_pdf"):
                if row.get(key) and not Path(row[key]).is_absolute():
                    row[key] = str(base / row[key])
            out.setdefault(row["subtopic"], []).append(row)
    return out


def parse_pages(spec):
    pages = []
    for part in re.split(r"[,\s]+", spec or ""):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            pages += list(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return pages


def _stamp(page, label):
    w, h = float(page.mediabox.width), float(page.mediabox.height)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    c.setFillColor(HexColor("#ffffff"))
    c.rect(w - 245, h - 26, 235, 18, stroke=0, fill=1)
    c.setFillColor(HexColor("#1d2433"))
    c.setFont("Sans", 8)
    c.drawRightString(w - 14, h - 20, f"{label}   ☐ Todo   ☐ Mastered")
    c.save()
    buf.seek(0)
    page.merge_page(PdfReader(buf).pages[0])
    return page


def splice_imports(pdf_path, markers, imports):
    """Insert the user's own past-paper pages after the marker pages recorded during the build."""
    if not markers:
        return
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    inserts: dict[int, list] = {}
    for (kind, sub), page_no in markers.items():
        for it in imports.get(sub, []):
            src = it["pdf"] if kind == "q" else it.get("ms_pdf")
            spec = it["pages"] if kind == "q" else it.get("ms_pages")
            if not src or not spec:
                continue
            r = PdfReader(src)
            for p in parse_pages(spec):
                if 1 <= p <= len(r.pages):
                    pg = r.pages[p - 1]
                    inserts.setdefault(page_no, []).append(_stamp(pg, it["label"]) if kind == "q" else pg)
    for i, page in enumerate(reader.pages, 1):
        writer.add_page(page)
        for extra in inserts.get(i, []):
            writer.add_page(extra)
    with open(pdf_path, "wb") as fh:
        writer.write(fh)


def build(modules=None, per_subtopic=None, per_skill=3, seed=2026, out_dir="out", imports_csv=None, include_notes=True, pagesize="a4", combined=True, working_space=True):
    from reportlab.lib.pagesizes import A4, letter
    tax = load_json("taxonomy.json")
    notes = load_json("notes.json")
    videos = load_json("videos.json")
    imports = read_imports(imports_csv)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    made = []
    manifest = {"seed": seed, "per_skill": per_skill, "per_subtopic": per_subtopic, "files": [], "questions": []}
    for m in tax["modules"]:
        if modules and int(m["id"][1:]) not in modules:
            continue
        qs = {s["id"]: select_questions(s["id"], per_subtopic or per_skill * len(s["skills"]), seed) for s in m["subtopics"]}
        mod_imports = {s["id"]: imports.get(s["id"], []) for s in m["subtopics"] if imports.get(s["id"])}
        slug = re.sub(r"[^A-Za-z0-9]+", "-", m["title"]).strip("-")
        path = out / f"Module{m['id'][1:]}-{slug}.pdf"
        markers = build_module_pdf(str(path), m, tax["qualification"], qs, notes, videos, seed, mod_imports, include_notes,
                                   A4 if pagesize == "a4" else letter, working_space)
        splice_imports(str(path), markers, mod_imports)
        made.append(path)
        npages = len(PdfReader(str(path)).pages)
        manifest["files"].append({"module": m["id"], "file": path.name, "pages": npages, "questions": sum(len(v) for v in qs.values())})
        for sid, ql in qs.items():
            for q in ql:
                manifest["questions"].append({"id": q.qid, "subtopic": sid, "skill": q.skill, "marks": q.marks, "difficulty": q.difficulty})
        print(f"  {path}  ({sum(len(v) for v in qs.values())} questions, {len(PdfReader(str(path)).pages)} pages)")
    if combined and len(made) > 1:
        w = PdfWriter()
        for p in made:
            w.append(str(p))
        cpath = out / "All-Modules-Workbook.pdf"
        with open(cpath, "wb") as fh:
            w.write(fh)
        made.append(cpath)
        manifest["files"].append({"module": "all", "file": cpath.name, "pages": len(PdfReader(str(cpath)).pages), "questions": len(manifest["questions"])})
        print(f"  {cpath}  (combined)")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    return made


KEYWORDS = {
    "1.1": ["surd", "rationalise", "indices", "simplify fully", "factorise fully"], "1.2": ["discriminant", "completing the square", "real roots", "quadratic"],
    "1.3": ["simultaneous", "inequalit", "set notation", "region"], "1.4": ["gradient", "perpendicular", "straight line", "midpoint"],
    "1.5": ["circle", "centre", "radius", "tangent to the circle"], "2.1": ["proof", "prove", "contradiction", "partial fractions", "factor theorem"],
    "2.2": ["modulus", "inverse", "composite", "domain", "range", "transformation", "f^-1", "fg("], "2.3": ["binomial expansion", "ascending powers", "valid"],
    "2.4": ["log", "ln", "exponential", "e^"], "3.1": ["arithmetic", "geometric", "sum to infinity", "series", "sequence", "u_n"],
    "3.2": ["radian", "sector", "arc", "sec", "cosec", "cot", "small angle", "arcsin", "arccos"], "3.3": ["cos(", "r cos", "double angle", "identity", "tan 2"],
    "3.4": ["parametric"], "4.1": ["differentiate", "dy/dx", "stationary", "tangent", "normal", "rate of", "first principles", "implicit"],
    "4.2": ["integrate", "integral", "area", "trapezium", "differential equation", "by parts", "substitution"], "4.3": ["newton-raphson", "iteration", "root", "change of sign"],
    "4.4": ["vector", "i + ", "position vector"], "5.1": ["probability", "distribution", "hypothesis", "sample", "mean", "standard deviation", "correlation", "large data set"],
    "5.2": ["particle", "acceleration", "velocity", "force", "friction", "pulley", "moment", "projectile", "rod", "plane"],
}


def suggest(pdf_path):
    """Print a best-guess subtopic for each page of a past paper, plus CSV rows to paste into imports.csv."""
    r = PdfReader(pdf_path)
    rows = []
    for i, page in enumerate(r.pages, 1):
        text = (page.extract_text() or "").lower()
        scores = {k: sum(text.count(w) for w in ws) for k, ws in KEYWORDS.items()}
        best = sorted(scores.items(), key=lambda kv: -kv[1])[:2]
        if best[0][1] == 0:
            continue
        qn = re.findall(r"^\s*(\d{1,2})\.\s", page.extract_text() or "", re.M)
        label = f"{Path(pdf_path).stem} p{i}" + (f" Q{qn[0]}" if qn else "")
        print(f"page {i:>3}: {best[0][0]} (score {best[0][1]})" + (f", or {best[1][0]}" if best[1][1] else "") + (f"  questions starting: {', '.join(qn)}" if qn else ""))
        rows.append(f'{best[0][0]},"{label}",{pdf_path},{i},,')
    print("\n# CSV rows (check the subtopic, add ms_pdf/ms_pages):\nsubtopic,label,pdf,pages,ms_pdf,ms_pages")
    print("\n".join(rows))
