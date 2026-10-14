"""Hand-checked topic tags for every 9MA0 question (first tag = main topic).

Pure questions are tagged with subtopic ids from taxonomy.json. Paper 3 questions are tagged with
"5.1:<skill>" / "5.2:<skill>" so applied topics can be picked at skill level.
"""

S = {  # statistics skills
    "samp": "Populations and sampling methods", "meas": "Measures of location and spread, coding",
    "hist": "Histograms, box plots, cumulative frequency, outliers", "corr": "Correlation and regression",
    "lds": "The large data set", "venn": "Probability: Venn diagrams and set notation",
    "cond": "Conditional probability and tree diagrams", "bin": "Binomial distribution",
    "hbin": "Hypothesis testing: critical regions and p-values", "norm": "Normal distribution",
    "napp": "Normal approximation to binomial", "hnorm": "Hypothesis testing: normal mean and correlation",
    "disc": "Discrete probability distributions",
}
M = {  # mechanics skills
    "mod": "Quantities and units, modelling assumptions", "suvat": "Constant acceleration: suvat",
    "graph": "Motion graphs", "var": "Variable acceleration with calculus", "vec": "2D motion with vectors",
    "newton": "Newton's laws and resolving forces", "fric": "Friction", "conn": "Connected particles and pulleys",
    "incl": "Inclined planes", "mom": "Moments, equilibrium and centre of mass", "proj": "Projectiles",
}

PURE = {
    # Paper 1
    "P1-J18": ["3.2", "4.1", "3.2", "4.3 2.4", "4.1 3.3", "1.5 1.4", "4.2", "3.3", "4.1", "4.2", "2.3", "2.4", "4.2 2.1", "3.4"],
    "P1-J19": ["2.1", "4.3", "4.1", "2.3", "1.2 2.2", "3.3", "2.4", "4.2", "2.4", "2.1 2.2", "3.1", "4.1 2.2", "4.2 2.1", "4.1 3.2"],
    "P1-J22": ["2.2", "2.1", "1.5", "4.2", "1.4 1.3", "2.2 4.1", "2.1", "4.1 4.3", "4.4", "2.4", "4.2", "4.2", "3.1", "3.3", "4.1 3.2", "4.2 3.4"],
    "P1-J23": ["4.2", "2.1", "4.4", "3.2 4.1", "4.2", "2.4", "2.2", "3.2", "3.1", "1.5", "2.4", "4.1", "3.3", "2.1", "4.1"],
    "P1-J24": ["2.1", "2.3", "4.3", "4.1", "4.1", "2.2", "4.2", "2.2", "3.1", "4.2 4.1", "3.2", "3.3", "4.2", "4.2 4.1", "2.1"],
    "P1-J25": ["2.2", "1.5", "3.1", "2.1", "4.2", "1.3", "2.2 4.1", "2.1", "4.1 4.3", "4.4", "2.4", "2.1 1.3", "4.2", "3.3", "3.2", "4.2"],
    "P1-O20": ["2.3", "2.4", "4.4", "2.2", "3.1", "3.3", "4.2", "4.2", "4.1 2.2", "4.2", "3.2 1.5", "3.3", "3.1", "4.2 4.1", "4.1", "2.1"],
    "P1-O21": ["2.1", "1.2", "3.1", "4.3 4.1", "3.1", "4.4", "1.5", "2.4", "2.3 2.1", "3.3", "4.2", "1.2", "3.4", "4.1", "2.1"],
    "P1-SP": ["4.2", "2.3", "3.1", "4.4", "2.1 2.4", "1.2", "4.2", "3.1", "4.1", "2.2", "4.1", "4.2", "3.3", "3.4"],
    # Paper 2
    "P2-J18": ["2.2", "4.4", "2.1 2.2", "3.1", "4.3", "2.1 1.2", "3.3 3.2", "1.2", "4.1", "4.2", "2.1 4.1", "3.3", "4.2 4.1", "2.4 4.1"],
    "P2-J19": ["1.1", "4.2", "3.2", "3.4 1.5", "4.2", "2.2", "1.4", "3.1 2.4", "2.4", "4.4", "4.1 4.3", "3.3", "4.1", "4.2"],
    "P2-J22": ["2.2", "2.4", "3.1", "4.1", "4.2 2.4", "4.1 4.3", "2.3", "4.2", "3.3", "2.2", "2.1", "4.1 1.2", "4.4", "4.2 2.1", "3.1 3.3", "3.4 4.1"],
    "P2-J23": ["4.1", "3.1", "2.4", "2.4 4.1", "4.2 4.1", "4.4", "4.1", "3.3 3.1", "3.4 4.1", "2.1 4.2", "4.2", "2.2 2.4", "2.3", "3.3", "2.1"],
    "P2-J24": ["4.1", "3.1", "2.2", "3.1", "3.2", "4.3 4.1", "4.4", "3.3", "1.2", "3.4 4.1", "4.2", "4.2 2.1", "2.4", "1.5 1.3", "4.1 2.1"],
    "P2-J25": ["1.1", "4.2", "2.4", "3.2", "3.4 4.1", "3.2", "2.1", "4.1 2.2", "2.4 4.1", "4.2", "4.1 1.4", "2.2", "3.3", "4.4", "4.2"],
    "P2-O20": ["4.2", "4.4", "2.4", "2.3", "2.4", "4.2 2.1", "4.1 4.3", "4.2 2.1", "2.4", "3.3", "2.2", "4.2 3.4", "2.2 4.1", "1.5", "3.1", "2.1"],
    "P2-O21": ["3.1", "2.2", "2.4", "3.2", "4.1", "3.2", "4.2 4.1", "4.1", "3.1 3.2", "2.4", "2.2", "4.2", "4.1 3.4", "4.2", "3.3"],
    "P2-SP": ["3.2", "3.2", "2.4", "2.2", "1.2 1.3", "4.1 4.3", "4.2 2.4", "4.1", "1.5", "4.2 3.4", "3.1", "4.1", "3.3", "2.1"],
}

APPLIED = {
    "P3-J18": ["s:lds disc", "s:hnorm corr", "s:bin hbin", "s:samp meas", "s:norm",
               "m:var vec", "m:fric newton", "m:vec", "m:mom", "m:proj"],
    "P3S-J19": ["s:cond", "s:hist lds", "s:corr hnorm", "s:bin lds", "s:norm napp hnorm"],
    "P3M-J19": ["m:var vec", "m:vec", "m:conn incl fric", "m:mom", "m:proj"],
    "P3S-J22": ["s:bin", "s:norm hnorm", "s:lds meas", "s:hbin", "s:cond", "s:corr hnorm"],
    "P3M-J22": ["m:var vec", "m:incl fric newton", "m:newton vec", "m:mom", "m:proj"],
    "P3S-J23": ["s:venn", "s:bin hbin", "s:lds meas", "s:norm hnorm", "s:disc", "s:hist norm"],
    "P3M-J23": ["m:suvat", "m:fric newton", "m:var vec", "m:vec", "m:proj", "m:mom"],
    "P3S-J24": ["s:bin", "s:corr hnorm", "s:lds meas", "s:hbin", "s:norm hnorm", "s:venn cond"],
    "P3M-J24": ["m:fric", "m:graph", "m:incl fric", "m:vec var", "m:proj", "m:mom"],
    "P3S-J25": ["s:cond", "s:meas", "s:bin", "s:samp corr lds", "s:norm hnorm", "s:disc"],
    "P3M-J25": ["m:suvat", "m:fric newton", "m:newton vec", "m:var vec", "m:proj", "m:mom"],
    "P3S-O20": ["s:venn", "s:corr lds", "s:hist meas", "s:disc", "s:norm hnorm"],
    "P3M-O20": ["m:incl fric", "m:vec", "m:var vec", "m:mom", "m:proj"],
    "P3S-O21": ["s:bin hbin samp", "s:corr hnorm", "s:lds meas", "s:venn cond", "s:norm", "s:disc"],
    "P3M-O21": ["m:vec", "m:conn incl fric", "m:mom", "m:proj", "m:var vec"],
}

# June 2019 Paper 3 is image-only (no text layer), so its pages were mapped by hand.
MANUAL = {
    "P3S-J19": [  # (qp pages, marks, ms pages)
        ([2, 3, 4, 5], 8, [6, 6]), ([6, 7, 8, 9], 11, [7, 7]), ([10, 11, 12, 13], 9, [8, 8]),
        ([14, 15, 16, 17], 9, [9, 9]), ([18, 19, 20], 13, [10, 11])],
    "P3M-J19": [
        ([2, 3], 6, [6, 6]), ([4, 5], 8, [7, 8]), ([6, 7, 8, 9], 12, [9, 10]),
        ([10, 11, 12, 13], 11, [11, 14]), ([14, 15, 16, 17, 18, 19], 13, [15, 16])],
}


def expand(paper_id, i):
    """Tags for question i (0-based) of a paper: list of subtopic ids and skill names."""
    if paper_id in PURE:
        return {"topics": PURE[paper_id][i].split(), "skills": []}
    if paper_id in LEGACY:
        return {"topics": LEGACY[paper_id][i][3].split(), "skills": []}
    code = APPLIED[paper_id][i]
    kind, keys = code.split(":")
    table, sub = (S, "5.1") if kind == "s" else (M, "5.2")
    return {"topics": [sub], "skills": [table[k] for k in keys.split()]}

# Legacy Edexcel GCE papers (C1, C2; June 2017 and June 2018), included for extra depth in Modules 1-3.
# (qp pages, marks, ms pages, tags); marks are the mark-scheme totals.
LEGACY = {
    "C1-J17": [
        ([2, 3], 4, [9, 9], "4.2 1.1"),
        ([4, 5], 5, [10, 10], "4.1 1.1"),
        ([6, 7], 6, [11, 11], "3.1"),
        ([8, 9], 7, [12, 12], "3.1"),
        ([10, 11], 8, [13, 15], "1.2 2.2"),
        ([12, 13], 6, [16, 17], "1.2 2.4"),
        ([14, 15], 9, [18, 18], "4.1 4.2"),
        ([16, 17, 18, 19], 8, [19, 20], "1.4"),
        ([20, 21, 22, 23], 11, [21, 23], "2.2 1.3"),
        ([24, 25, 26, 27, 28], 11, [24, 25], "2.2"),
    ],
    "C1-J18": [
        ([2, 3], 5, [9, 9], "1.1"),
        ([4, 5], 7, [10, 10], "4.2 4.1"),
        ([6, 7], 6, [11, 11], "1.2"),
        ([8, 9, 10, 11], 7, [12, 12], "3.1"),
        ([12, 13, 14, 15], 5, [12, 13], "2.2"),
        ([16, 17], 7, [14, 14], "3.1"),
        ([18, 19], 8, [15, 15], "1.2 1.3"),
        ([20, 21, 22, 23], 8, [16, 17], "1.4"),
        ([24, 25, 26, 27], 12, [18, 19], "4.2 2.1"),
        ([28, 29, 30, 31, 32], 10, [20, 20], "4.1 1.4"),
    ],
    "C2-J17": [
        ([2, 3], 4, [7, 8], "2.3"),
        ([4, 5], 4, [8, 9], "3.2"),
        ([6, 7, 8, 9], 6, [9, 10], "4.2 2.4"),
        ([10, 11, 12, 13], 8, [10, 11], "3.2"),
        ([14, 15], 7, [11, 13], "1.5"),
        ([16, 17, 18, 19], 9, [12, 14], "2.1 2.4"),
        ([20, 21], 7, [14, 15], "2.4"),
        ([22, 23], 8, [15, 16], "3.3"),
        ([24, 25, 26, 27], 12, [16, 17], "3.1"),
        ([28, 29, 30, 31, 32], 10, [17, 19], "4.2 4.1"),
    ],
    "C2-J18": [
        ([2, 3], 5, [7, 8], "4.2"),
        ([4, 5], 7, [8, 9], "2.3"),
        ([6, 7, 8, 9], 8, [9, 10], "2.1"),
        ([10, 11, 12, 13], 9, [10, 11], "3.2"),
        ([14, 15, 16, 17], 10, [11, 12], "1.5"),
        ([18, 19], 7, [12, 14], "3.1"),
        ([20, 21, 22, 23], 8, [14, 15], "2.4"),
        ([24, 25, 26, 27], 9, [15, 16], "3.3"),
        ([28, 29, 30, 31, 32], 12, [16, 18], "4.1 4.2"),
    ],
}
