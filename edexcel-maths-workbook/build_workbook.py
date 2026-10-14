#!/usr/bin/env python3
"""Build printable Edexcel A-Level Maths (9MA0) workbooks.

Examples:
  python build_workbook.py build                         # all 5 modules, 3 questions per spec skill (~430)
  python build_workbook.py build --modules 1 4 --per-skill 6 --seed 7
  python build_workbook.py build --imports my_papers/imports.csv
  python build_workbook.py suggest my_papers/June-2019-Paper-1.pdf
  python build_workbook.py list
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="build module PDFs")
    b.add_argument("--modules", type=int, nargs="*", help="module numbers 1-5 (default: all)")
    b.add_argument("--per-skill", type=int, default=3, help="questions per specification skill (default 3, no upper limit)")
    b.add_argument("--per-subtopic", type=int, help="fixed number of questions per subtopic (overrides --per-skill)")
    b.add_argument("--seed", type=int, default=2026, help="change for a fresh set of questions")
    b.add_argument("--out", default="out")
    b.add_argument("--imports", help="CSV of your own past-paper pages to splice in")
    b.add_argument("--no-notes", action="store_true", help="omit key facts / method / traps pages")
    b.add_argument("--no-working-space", action="store_true", help="compact layout without squared working boxes")
    b.add_argument("--letter", action="store_true", help="US Letter instead of A4")
    b.add_argument("--no-combined", action="store_true", help="skip the all-modules PDF")
    s = sub.add_parser("suggest", help="tag the pages of a past-paper PDF with likely subtopics")
    s.add_argument("pdf")
    sub.add_parser("list", help="show the taxonomy and generator coverage")
    a = ap.parse_args()

    from workbook import builder
    from workbook.core import REGISTRY, load_json

    if a.cmd == "build":
        builder.build(a.modules, a.per_subtopic, a.per_skill, a.seed, a.out, a.imports, not a.no_notes, "letter" if a.letter else "a4",
                      not a.no_combined, not a.no_working_space)
    elif a.cmd == "suggest":
        builder.suggest(a.pdf)
    else:
        tax = load_json("taxonomy.json")
        for m in tax["modules"]:
            print(f"Module {m['id'][1:]}: {m['title']}")
            for s in m["subtopics"]:
                gens = REGISTRY.get(s["id"], [])
                print(f"  {s['id']} {s['title']:<38} {len(gens):>3} generators, {len({g.skill for g in gens})}/{len(s['skills'])} skills")


if __name__ == "__main__":
    main()
