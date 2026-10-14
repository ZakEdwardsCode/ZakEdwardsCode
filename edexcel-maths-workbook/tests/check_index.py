"""Check the past-paper index: totals per paper, page ranges inside each PDF (needs the cache)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pypdf import PdfReader  # noqa: E402

from workbook import pastpapers as pp  # noqa: E402

cache = sys.argv[1] if len(sys.argv) > 1 else "papers_cache"
bad = 0
for p in pp.index():
    total = sum(q["marks"] for q in p["questions"])
    expect = 75 if p.get("legacy") or p["id"].startswith("C") else 50 if p["id"].startswith(("P3S", "P3M")) else 100
    nq = len(PdfReader(str(pp.cache_path(cache, p["qp"]))).pages) if pp.cache_path(cache, p["qp"]).exists() else None
    nm = len(PdfReader(str(pp.cache_path(cache, p["ms"]))).pages) if pp.cache_path(cache, p["ms"]).exists() else None
    for q in p["questions"]:
        if not q["topics"] or (nq and max(q["pages"]) > nq) or (nm and q["ms_pages"][1] > nm):
            print("BAD", q["id"]); bad += 1
    if total != expect:
        print("BAD total", p["id"], total, expect); bad += 1
print(f"{len(pp.index())} papers, {len(pp.all_questions())} questions, {bad} problems")
