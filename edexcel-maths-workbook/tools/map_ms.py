import re
from pypdf import PdfReader
TOT = re.compile(r"\(\s*(?:Total\s*)?(\d{1,2})\s*marks?\s*\)|\bTotal\s*(\d{1,2})\s*(?:marks?)?(?=\s*(?:\||\n|$))|\(\s*Total\s*(\d{1,2})\s*\)", re.I)
HEAD = re.compile(r"Question\s*\|?\s*(?:Number\s*\|?\s*)?Scheme\s*\|?\s*Marks(?:\s*\|?\s*AOs?)?\s*\|?\s*(\d{1,2})\s*\.?\s*(?=\(|[a-z]\b|\||\s)")
GUIDE = ("general marking guidance", "general principles", "general instructions", "edexcel and btec", "mark scheme (results)")


def map_ms(path, marks):
    """Page ranges (start, end) per question, from '(N marks)' closers plus 'Question Scheme Marks n' headers."""
    r = PdfReader(path)
    texts = [(p.extract_text() or "") for p in r.pages]
    n = len(marks)
    guide_end = 0
    for i, t in enumerate(texts[:10], 1):
        if TOT.search(t) and not any(g in t.lower() for g in GUIDE):
            break
        if any(g in t.lower() for g in GUIDE):
            guide_end = i
    heads = {}
    closers = []
    for i in range(guide_end + 1, len(texts) + 1):
        t = texts[i - 1]
        for m in HEAD.finditer(t.replace("\n", " | ")):
            q = int(m.group(1))
            if 1 <= q <= n and q not in heads:
                heads[q] = i
        for m in TOT.finditer(t):
            closers.append((i, m.end() / max(1, len(t)), int(m.group(1) or m.group(2) or m.group(3))))
    ends = [None] * n
    k = 0
    for qi, mk in enumerate(marks):
        for j in range(k, min(k + 4, len(closers))):
            if closers[j][2] == mk and (not heads.get(qi + 2) or closers[j][0] <= heads[qi + 2]):
                ends[qi] = closers[j]
                k = j + 1
                break
    starts = [None] * n
    for qi in range(n):
        if qi == 0 and closers:
            starts[qi] = min(heads.get(1, 999), closers[0][0])
        elif heads.get(qi + 1):
            starts[qi] = heads[qi + 1]
        elif qi == 0:
            starts[qi] = closers[0][0] if closers else guide_end + 1
        elif ends[qi - 1]:
            pg, frac, _ = ends[qi - 1]
            starts[qi] = pg if frac < 0.8 else pg + 1
    for qi in range(n):
        if starts[qi] is None:
            starts[qi] = (ends[qi - 1][0] if qi and ends[qi - 1] else starts[qi - 1])
    last = max(i for i, t in enumerate(texts, 1) if len(t.strip()) > 300)
    out = []
    for qi in range(n):
        e = ends[qi][0] if ends[qi] else starts[qi]
        if qi + 1 < n:
            nxt = starts[qi + 1]
            if nxt > e:
                e = nxt - 1 if not (ends[qi] and ends[qi][0] == nxt) else nxt
            # a question whose closer sits on the page where the next one starts keeps just that page
        else:
            e = max(e, last)
        out.append((starts[qi], max(e, starts[qi])))
    found = sum(1 for e in ends if e)
    return out, found


QNUM = re.compile(r"(?:^|\n)\s*(?:Q\s*)?(\d{1,2})\s*\.?\s*(?:\(\s*[a-z]{1,4}\s*\)|\s(?=\(?[a-z]{1,3}\)))", re.I)


def map_ms_by_numbers(path, n):
    """Fallback: find the first page where each question number labels a mark-scheme row."""
    r = PdfReader(path)
    texts = [(p.extract_text() or "") for p in r.pages]
    guide_end = 0
    for i, t in enumerate(texts[:12], 1):
        if any(g in t.lower() for g in GUIDE) or "general principles" in t.lower():
            guide_end = i
    first = {}
    expect = 1
    for i in range(guide_end + 1, len(texts) + 1):
        for m in QNUM.finditer(texts[i - 1]):
            q = int(m.group(1))
            if q == expect or (q == expect + 1 and expect > 1):
                first.setdefault(q, i)
                expect = q + 1
    starts = []
    for q in range(1, n + 1):
        starts.append(first.get(q))
    for k in range(n):
        if starts[k] is None:
            starts[k] = starts[k - 1] if k else guide_end + 1
    last = max(i for i, t in enumerate(texts, 1) if len(t.strip()) > 300)
    out = []
    for k in range(n):
        e = (starts[k + 1] if k + 1 < n else last)
        if k + 1 < n and starts[k + 1] > starts[k]:
            e = starts[k + 1]  # include the boundary page; a question can end on the page where the next starts
        out.append((starts[k], max(e, starts[k])))
    return out, sum(1 for q in range(1, n + 1) if q in first)
