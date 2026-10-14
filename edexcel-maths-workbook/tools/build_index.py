"""Regenerate workbook/past_papers.json from the downloaded papers (maintainer tool).

    python tools/build_index.py [cache_dir]

Splits each question paper into questions (each 9MA0 question starts on a new page and runs over
'Question N continued' pages), reads the marks, maps mark-scheme pages from the '(N marks)' totals,
and applies the hand-checked tags in tools/tags.py.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from map_ms import map_ms  # noqa: E402
from split_qp import split_qp  # noqa: E402
import tags  # noqa: E402
from workbook.pastpapers import SOURCES, cache_path  # noqa: E402

cache = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "papers_cache"
out = []
for src in SOURCES:
    qp, ms = cache_path(cache, src["qp"]), cache_path(cache, src["ms"])
    if src["id"] in tags.LEGACY:
        qs = [{"n": i + 1, "pages": pages, "marks": mk, "ms_pages": msr} for i, (pages, mk, msr, _) in enumerate(tags.LEGACY[src["id"]])]
    elif src["id"] in tags.MANUAL:
        qs = [{"n": i + 1, "pages": pages, "marks": mk, "ms_pages": msr} for i, (pages, mk, msr) in enumerate(tags.MANUAL[src["id"]])]
    else:
        qs = split_qp(str(qp))
        mapped, found = map_ms(str(ms), [q["marks"] for q in qs])
        for q, r in zip(qs, mapped):
            q["ms_pages"] = list(r)
    questions = []
    for i, q in enumerate(qs):
        t = tags.expand(src["id"], i)
        questions.append({"id": f"{src['id']}-Q{q['n']}", "n": q["n"], "marks": q["marks"],
                          "pages": q["pages"], "ms_pages": q["ms_pages"], **t})
    total = sum(q["marks"] for q in questions)
    print(f"{src['id']:8s} {len(questions):2d} questions, {total} marks")
    out.append({**{k: src[k] for k in ("id", "label", "paper", "series", "year", "qp", "ms")}, "questions": questions})
(ROOT / "workbook" / "past_papers.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print("questions:", sum(len(p["questions"]) for p in out))
