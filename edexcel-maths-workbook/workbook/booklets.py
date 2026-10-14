"""`build_workbook.py papers`: decide which booklets to make and write them."""
import re
from pathlib import Path

from . import pastpapers as pp
from .core import load_json


def _slug(t):
    return re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-")


def run(a):
    missing = pp.fetch(a.cache, quiet=False)
    if missing:
        print(f"{len(missing)} papers could not be downloaded; booklets will skip their questions")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    tax = load_json("taxonomy.json")
    titles = pp.titles()
    filters = dict(years=a.years, papers=a.papers, primary_only=a.primary_only)
    include_ms, inline = a.ms != "none", a.ms == "inline"
    jobs = []
    selected = a.modules or a.topics or a.skills
    if not selected and not a.one_file:
        for m in tax["modules"]:
            jobs.append((f"Module {m['id'][1:]} — {m['title']}", f"Module{m['id'][1:]}-{_slug(m['title'])}", pp.select(modules=[int(m["id"][1:])], **filters)))
        for m in tax["modules"]:
            for s in m["subtopics"]:
                jobs.append((f"{s['id']} {s['title']}", f"Topic-{s['id']}-{_slug(s['title'])}", pp.select(topics=[s["id"]], **filters)))
    else:
        sections = pp.select(topics=a.topics, modules=a.modules, skills=a.skills, **filters)
        if a.per_topic:
            for sid, qs in sections.items():
                jobs.append((f"{sid} {titles[sid]}", f"Topic-{sid}-{_slug(titles[sid])}", {sid: qs}))
        else:
            parts = []
            if a.modules:
                parts.append("Modules " + ", ".join(map(str, a.modules)))
            if a.topics:
                parts.append("Topics " + ", ".join(a.topics))
            if a.skills:
                parts.append("Skills: " + ", ".join(a.skills))
            name = " + ".join(parts) or "All topics"
            jobs.append((name, "Selection-" + _slug(name), sections))
    sub = []
    if a.years:
        sub.append("years " + ", ".join(map(str, a.years)))
    if a.papers:
        sub.append("papers " + ", ".join(a.papers))
    for title, fname, sections in jobs:
        if not sections:
            print(f"  (no questions for {title})")
            continue
        sections = {k: [q for q in v if pp.cache_path(a.cache, q["qp"]).exists()] for k, v in sections.items()}
        path = out / f"{fname}.pdf"
        n = pp.build_booklet(str(path), title, sections, a.cache, include_ms, inline, " · ".join(sub))
        print(f"  {path}  ({sum(len(v) for v in sections.values())} questions, {n} pages)")
