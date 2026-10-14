import re, glob, json, sys
from pypdf import PdfReader
CONT = re.compile(r"Question\s+(\d{1,2})\s+continued", re.I)
START = re.compile(r"(?:^|\n)\s*(\d{1,2})\s*\.(?!\d)")
TOTAL = re.compile(r"\(Total\s+for\s+Question\s+(\d{1,2})\s+is\s+(\d{1,2})\s+marks?\)", re.I)

def split_qp(path):
    r = PdfReader(path)
    qs = []  # dicts: n, pages, marks, section
    cur = None
    section = "A"
    for i, p in enumerate(r.pages, 1):
        t = p.extract_text() or ""
        if i == 1:
            continue
        c = CONT.search(t)
        totals = TOTAL.findall(t)
        started = None
        if not c:
            body = t.split("DO NOT WRITE IN THIS AREA")[-1]
            if cur is None:
                m1 = re.search(r"(?:^|\n)\s*1\s+[A-Z(]", body)
                if m1 and not START.search(body):
                    started = 1
            for m in ([] if started else START.finditer(body)):
                n = int(m.group(1))
                exp = (cur["n"] + 1) if cur else 1
                if n == exp or (n == 1 and cur and cur["n"] > 1):
                    started = n
                    break
        if started is not None:
            if started == 1 and cur:
                section = "B"
            cur = {"n": started, "pages": [i], "marks": None, "section": section, "text": t}
            qs.append(cur)
        elif c and cur and int(c.group(1)) == cur["n"]:
            cur["pages"].append(i)
        elif cur and not ("BLANK PAGE" in t and len(t) < 200) and "TOTAL FOR" not in t.upper()[:0]:
            # unlabeled page: continuation if it is not a blank/back page
            if len(t.strip()) > 60 and "TOTAL FOR PAPER" not in t.upper():
                cur["pages"].append(i)
        for qn, mk in totals:
            for q in reversed(qs):
                if q["n"] == int(qn):
                    q["marks"] = int(mk)
                    break
    return qs

if __name__ == "__main__":
    bad = 0
    for f in sorted(glob.glob("raw/*/QP/*.pdf")):
        qs = split_qp(f)
        ok = all(q["marks"] for q in qs)
        s = sum(q["marks"] or 0 for q in qs)
        if not ok or s not in (100, 50):
            bad += 1
        print(f"{'OK ' if ok and s in (100,50) else 'BAD'} {f.split('raw/')[1]:45s} q={len(qs):2d} total={s:3d} " + " ".join(f"{q['section'] if q['section']=='B' else ''}{q['n']}:{len(q['pages'])}p/{q['marks']}" for q in qs))
    print("bad", bad)
