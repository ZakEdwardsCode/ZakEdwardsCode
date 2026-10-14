# Edexcel A-Level Maths (9MA0) workbook builder

Builds printable, modular practice workbooks for Pearson Edexcel A-Level Mathematics, one PDF per
module, using the full specification taxonomy (5 modules, 19 subtopics, 144 skills).

Each PDF has:

- a cover with a per-subtopic progress table,
- for every subtopic: key facts, method, exam traps, a **Learnt / Practised / Mastered** skills
  checklist and clickable YouTube links (TLMaths, ExamSolutions, Bicen Maths) with tick boxes,
- exam-style questions, each with marks, a difficulty rating, a **☐ Todo ☐ Mastered** box and a
  squared working-space block sized to the marks,
- a ruled "My notes" box at the end of each subtopic,
- answers and Edexcel-style mark schemes (M/A/B marks) at the back.

`dist/` holds a ready-built set (seed 2026, 3 questions per skill = 432 questions).

## Quick start

```bash
pip install -r requirements.txt
python build_workbook.py build                      # all modules -> out/
python build_workbook.py build --modules 4 --per-skill 8 --seed 11
python build_workbook.py build --no-working-space   # compact revision version
python build_workbook.py list                       # taxonomy + generator coverage
```

Change `--seed` for a completely new set of questions. There is no upper limit on
`--per-skill`/`--per-subtopic`: questions are generated, not looked up.

## Where the questions come from

Pearson's past papers are copyright, and there is no public API for them, so the tool does not scrape
or redistribute them. Instead:

1. **Generated questions (default).** 164 randomised generators, written in the style and mark
   allocation of 9MA0 questions. Every answer is computed (sympy for algebra and calculus, a
   numerical root finder for trig equations, exact binomial/normal calculations for statistics), so
   the mark scheme always matches the question. Run `python tests/check_generators.py` to exercise
   every generator over many seeds.
2. **Your own past papers (optional).** Download papers and mark schemes from the Pearson
   qualifications website (or your school), then splice the exact pages into the right subtopic:

   ```bash
   python build_workbook.py suggest papers/June-2019-Paper-1.pdf   # guesses a subtopic per page
   python build_workbook.py build --imports papers/imports.csv
   ```

   `imports.csv` columns: `subtopic,label,pdf,pages,ms_pdf,ms_pages` (paths relative to the CSV,
   pages like `3-4`). Imported question pages are stamped with a Todo/Mastered box; mark-scheme pages
   go into that module's answer section. These stay on your machine.

## Layout

```
build_workbook.py          CLI
workbook/taxonomy.json     modules, subtopics, skills (single source of truth)
workbook/notes_src.py      key facts / methods / traps (-> notes.json)
workbook/videos.json       curated YouTube links per skill and per subtopic
workbook/generators/m1-m5  question generators, registered per subtopic and skill
workbook/pdf.py            reportlab layout (tick boxes, working space, mark schemes)
workbook/builder.py        question selection, PDF splicing, page tagging
tests/check_generators.py  smoke test for every generator
```

Maths is typeset with matplotlib's mathtext (no LaTeX install needed) in STIX, close to the
Times-style setting used on the real papers.
