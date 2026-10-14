"""Smoke test: run every generator over many seeds and typeset all maths.

    python tests/check_generators.py [subtopic ...] [--seeds N]
"""
import random
import re
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workbook import generators  # noqa: F401,E402
from workbook.core import REGISTRY  # noqa: E402
from workbook.mathrender import math_image  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
seeds = int(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else 40
if "--seeds" in sys.argv:
    args = [a for a in args if a != str(seeds)]
MATH = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$", re.S)
fails = 0
total = 0
for sub, gens in sorted(REGISTRY.items()):
    if args and sub not in args:
        continue
    for g in gens:
        for s in range(seeds):
            total += 1
            try:
                q = g(random.Random(s))
                texts = [q.stem] + [p.text for p in q.parts] + [p.answer for p in q.parts] + [l for p in q.parts for l in p.scheme]
                for t in texts:
                    if t.count("$") % 2:
                        raise ValueError(f"unbalanced $ in: {t}")
                    for m in MATH.finditer(t):
                        math_image(m.group(1) or m.group(2))
            except Exception:
                fails += 1
                print(f"FAIL {sub} {g.fn.__name__} seed={s}")
                traceback.print_exc(limit=1)
                break
print(f"{total} runs, {fails} failing generators, {sum(len(v) for v in REGISTRY.values())} generators registered")
