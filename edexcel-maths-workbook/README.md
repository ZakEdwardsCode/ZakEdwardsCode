# Edexcel A-Level Maths (9MA0) past-paper workbooks

Print **real Pearson Edexcel past-paper questions** sorted by topic, on the original exam pages with
their answer space, so you can write straight on them. Stack them by module, by subtopic, by skill
or any mix, with the matching mark-scheme pages at the back.

- **396 questions**: every 9MA0 paper from the Specimen to June 2025 (Papers 1, 2, 3 Statistics and
  3 Mechanics), plus the June 2017 and June 2018 legacy C1 and C2 papers for extra algebra,
  coordinate geometry and series practice.
- Every question is tagged by hand to the 19 subtopics in `workbook/taxonomy.json`; Paper 3
  questions are also tagged by skill (projectiles, moments, hypothesis testing, normal distribution, ...).
- Each printed page is labelled with its topic, paper and question number, its marks, and
  **☐ Todo ☐ Mastered Score __ / N** boxes. The booklet's first pages are a checklist of every question.

## Quick start

```bash
pip install -r requirements.txt
python build_workbook.py papers                                  # 5 module booklets + 19 topic booklets
python build_workbook.py papers --topics 1.5 3.3                 # one booklet: circles + trig identities
python build_workbook.py papers --modules 4 --years 2022 2023 2024 2025
python build_workbook.py papers --skills projectile moments --ms inline
python build_workbook.py papers --modules 1 2 --per-topic        # one file per subtopic in modules 1-2
python build_workbook.py papers --papers 3S                      # only Paper 3 statistics questions
```

The first run downloads the official question papers and mark schemes (about 45 MB) into
`papers_cache/`. Booklets go to `out/past-papers/`. Options:

| option | meaning |
| --- | --- |
| `--modules 1 3` | everything in those modules |
| `--topics 1.2 4.1` | specific subtopics |
| `--skills projectile` | Paper 3 skills (substring match) |
| `--years 2023 2024` | exam years (2017 = specimen and legacy 2017) |
| `--papers 1 2 3S 3M C1 C2` | restrict to papers |
| `--primary-only` | only questions whose main topic is selected (default also includes questions where it is a secondary topic) |
| `--ms back/inline/none` | mark schemes at the back (default), straight after each question, or none |
| `--one-file` / `--per-topic` | how to split the selection |

In one booklet a question appears once, under the first selected topic it is tagged with.

## Copyright

The papers are © Pearson Education Ltd. They are **not** stored in this repository: the tool downloads
the copies published for students (via Physics & Maths Tutor) and builds booklets on your own machine
for personal revision. `workbook/past_papers.json` only holds page numbers, marks and topic tags.

## Extra: generated practice questions

`python build_workbook.py build` makes unlimited original exam-style questions (164 generators,
computed answers, Edexcel-style mark schemes) for extra drilling once the real questions run out.
See `python build_workbook.py build --help`.

## Layout

```
build_workbook.py            CLI (papers, fetch, build, suggest, list)
workbook/past_papers.json    index: every question's pages, mark-scheme pages, marks, tags
workbook/pastpapers.py       download, select, stamp and assemble booklets
workbook/taxonomy.json       modules, subtopics, skills
tools/build_index.py         regenerates the index (split papers, map mark schemes, apply tools/tags.py)
tools/tags.py                hand-checked topic tags for every question
tests/check_index.py         validates the index against the downloaded PDFs
```

When a new series is released: add it to `_SERIES` in `workbook/pastpapers.py`, tag its questions in
`tools/tags.py`, then run `python tools/build_index.py papers_cache` and `python tests/check_index.py`.
