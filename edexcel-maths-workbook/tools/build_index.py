"""Regenerate workbook/past_papers.json from the downloaded papers (maintainer tool).

    python tools/build_index.py [cache_dir]

9MA0 papers: each question starts on a new page and runs over 'Question N continued' pages; the
marks come from the '(Total for Question N is M marks)' lines and mark-scheme pages from the
'(N marks)' totals. Image-only and legacy papers use the hand-checked maps in tools/pagemaps.py.
IAL and 2014-16 legacy papers use the checked page maps in tools/extra_pages.json.
Every question then gets its hand-checked skill codes from tools/skill_tags.txt.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from map_ms import map_ms  # noqa: E402
from split_qp import split_qp  # noqa: E402
import pagemaps  # noqa: E402
from workbook.pastpapers import SOURCES, cache_path  # noqa: E402

cache = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "papers_cache"
TAGS = {}
for line in (ROOT / "tools" / "skill_tags.txt").read_text(encoding="utf-8").splitlines():
    if line.strip() and not line.startswith("#"):
        qid, *codes = line.split()
        TAGS[qid] = [] if codes == ["-"] else codes


def tagged(qid, q):
    skills = TAGS[qid]
    topics = list(dict.fromkeys(c.rsplit(".", 1)[0] for c in skills))
    return {"id": qid, "n": q["n"], "marks": q["marks"], "pages": q["pages"], "ms_pages": list(q["ms_pages"]),
            "skills": skills, "topics": topics, **({} if skills else {"off_spec": True})}


out = []
for src in SOURCES:
    qp, ms = cache_path(cache, src["qp"]), cache_path(cache, src["ms"])
    maps = pagemaps.LEGACY.get(src["id"]) or pagemaps.MANUAL.get(src["id"])
    if maps:
        qs = [{"n": i + 1, "pages": pages, "marks": mk, "ms_pages": msr} for i, (pages, mk, msr) in enumerate(maps)]
    else:
        qs = split_qp(str(qp))
        mapped, _ = map_ms(str(ms), [q["marks"] for q in qs])
        for q, r in zip(qs, mapped):
            q["ms_pages"] = list(r)
    out.append({**{k: src[k] for k in ("id", "label", "paper", "series", "year", "qp", "ms")}, **({"legacy": True} if src.get("legacy") else {}),
                "questions": [tagged(f"{src['id']}-Q{q['n']}", q) for q in qs]})
for p in json.loads((ROOT / "tools" / "extra_pages.json").read_text(encoding="utf-8")):
    out.append({**{k: v for k, v in p.items() if k != "questions"}, "questions": [tagged(f"{p['id']}-Q{q['n']}", q) for q in p["questions"]]})
for p in out:
    print(f"{p['id']:9s} {len(p['questions']):2d} questions, {sum(q['marks'] for q in p['questions'])} marks")
(ROOT / "workbook" / "past_papers.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
qs = [q for p in out for q in p["questions"]]
print(f"{len(out)} papers, {len(qs)} questions ({sum(1 for q in qs if q['skills'])} on the taxonomy)")
