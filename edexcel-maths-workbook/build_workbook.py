#!/usr/bin/env python3
"""Build printable Edexcel A-Level Maths (9MA0) workbooks.

Real past papers (downloads the official papers once, then cuts booklets on your machine):
  python build_workbook.py papers                       # one booklet per module + one per subtopic
  python build_workbook.py papers --topics 1.5 3.3      # just circles and trig identities, one booklet
  python build_workbook.py papers --modules 4 --years 2022 2023 2024 2025
  python build_workbook.py papers --skills 1.2.3 3.3.3 --per-topic   # one booklet per exact skill (discriminant, R-form)
  python build_workbook.py papers --skills projectile moments --ms inline
  python build_workbook.py papers --modules 1 2 3 4 5 --one-file   # everything in one stack

Generated practice questions (unlimited, with worked mark schemes):
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
    pp = sub.add_parser("papers", help="build printable booklets of real past-paper questions")
    pp.add_argument("--modules", type=int, nargs="*", help="module numbers 1-5")
    pp.add_argument("--topics", nargs="*", help="subtopic ids, e.g. 1.2 4.1")
    pp.add_argument("--skills", nargs="*", help="skill codes from `list` (e.g. 1.2.3 4.2.5) or words matched against skill names (e.g. projectile)")
    pp.add_argument("--years", type=int, nargs="*", help="exam years, e.g. 2022 2023 (2017 = specimen)")
    pp.add_argument("--papers", nargs="*", help="1, 2, 3, 3S (statistics), 3M (mechanics), IAL (or IAL-P1..IAL-P4), C1..C4")
    pp.add_argument("--primary-only", action="store_true", help="only questions whose main topic matches")
    pp.add_argument("--ms", choices=["back", "inline", "none"], default="back", help="mark schemes at the back (default), after each question, or none")
    pp.add_argument("--one-file", action="store_true", help="put the whole selection in a single booklet")
    pp.add_argument("--per-topic", action="store_true", help="one booklet per subtopic (or per skill, with --skills) in the selection")
    pp.add_argument("--cache", default="papers_cache", help="where downloaded papers are kept")
    pp.add_argument("--out", default="out/past-papers")
    sub.add_parser("fetch", help="download all question papers and mark schemes").add_argument("--cache", default="papers_cache")
    s = sub.add_parser("suggest", help="tag the pages of a past-paper PDF with likely subtopics")
    s.add_argument("pdf")
    sub.add_parser("list", help="show the taxonomy and generator coverage")
    a = ap.parse_args()

    from workbook import builder
    from workbook.core import REGISTRY, load_json

    if a.cmd == "build":
        builder.build(a.modules, a.per_subtopic, a.per_skill, a.seed, a.out, a.imports, not a.no_notes, "letter" if a.letter else "a4",
                      not a.no_combined, not a.no_working_space)
    elif a.cmd == "fetch":
        from workbook import pastpapers
        missing = pastpapers.fetch(a.cache)
        print("all papers downloaded" if not missing else f"{len(missing)} files failed; run again to retry")
    elif a.cmd == "papers":
        from workbook import booklets
        booklets.run(a)
    elif a.cmd == "suggest":
        builder.suggest(a.pdf)
    else:
        tax = load_json("taxonomy.json")
        for m in tax["modules"]:
            print(f"Module {m['id'][1:]}: {m['title']}")
            for s in m["subtopics"]:
                gens = REGISTRY.get(s["id"], [])
                print(f"  {s['id']} {s['title']:<38} {len(gens):>3} generators, {len({g.skill for g in gens})}/{len(s['skills'])} skills")
                for i, k in enumerate(s["skills"]):
                    print(f"      {s['id']}.{i:<3} {k[0]}")


if __name__ == "__main__":
    main()
