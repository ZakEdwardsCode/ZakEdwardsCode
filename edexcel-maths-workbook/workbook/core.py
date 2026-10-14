"""Question model, generator registry and maths formatting helpers."""
from __future__ import annotations

import json
import math
import re
import random
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

import sympy as sp

DATA = Path(__file__).parent
x, y, t, k, n, theta = sp.symbols("x y t k n theta")


@dataclass
class Part:
    text: str          # rich text: plain words with $inline maths$
    marks: int
    answer: str        # final answer (rich text)
    scheme: list[str] = field(default_factory=list)  # Edexcel-style mark lines, e.g. "M1 ..."


@dataclass
class Question:
    stem: str
    parts: list[Part]
    subtopic: str = ""
    skill: str = ""
    source: str = "Generated"
    difficulty: int = 1
    qid: str = ""
    figure: object = None  # optional reportlab Drawing

    @property
    def marks(self) -> int:
        return sum(p.marks for p in self.parts)


@dataclass
class Generator:
    fn: object
    subtopic: str
    skill: str
    difficulty: int
    weight: int

    def __call__(self, rng: random.Random) -> Question:
        q = self.fn(rng)
        q.subtopic, q.skill = self.subtopic, q.skill or self.skill
        q.difficulty = max(q.difficulty, self.difficulty)
        return q


REGISTRY: dict[str, list[Generator]] = {}


def gen(subtopic: str, skill: str, difficulty: int = 1, weight: int = 1):
    """Register a randomised question generator for a subtopic/skill."""
    def deco(fn):
        REGISTRY.setdefault(subtopic, []).append(Generator(fn, subtopic, skill, difficulty, weight))
        return fn
    return deco


def Q(stem: str, *parts: tuple, difficulty: int = 1, source: str = "Generated", figure=None) -> Question:
    """Shorthand: Q(stem, (text, marks, answer, [scheme...]), ...)."""
    ps = [Part(p[0], p[1], p[2], list(p[3]) if len(p) > 3 else []) for p in parts]
    return Question(stem=stem, parts=ps, difficulty=difficulty, source=source, figure=figure)


def load_json(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- formatting

def L(expr) -> str:
    """LaTeX for a sympy expression, restricted to what matplotlib mathtext renders."""
    if isinstance(expr, (int, Fraction)):
        expr = sp.Rational(expr.numerator, expr.denominator) if isinstance(expr, Fraction) else sp.Integer(expr)
    s = sp.latex(expr, ln_notation=True, mul_symbol=None, inv_trig_style="power", fold_func_brackets=True)
    s = re.sub(r"\\left\(\\left\|\{(.+?)\}\\right\| \\right\)", r"|\1|", s)
    s = re.sub(r"\\ln\{\\left\((\d+) \\right\)\}", r"\\ln \1", s)
    s = s.replace(r"\operatorname{", r"\mathrm{").replace(r"\left|", "|").replace(r"\right|", "|")
    s = s.replace(r"\cdot", r"\times")
    return s


def M(expr) -> str:
    """Inline maths: $...$ around L(expr)."""
    return f"${L(expr)}$"


def poly(coeffs, var="x") -> str:
    """LaTeX polynomial from descending integer/Fraction coefficients, skipping zeros."""
    deg = len(coeffs) - 1
    out = []
    for i, c in enumerate(coeffs):
        p = deg - i
        if c == 0:
            continue
        c = Fraction(c)
        sign = "-" if c < 0 else "+"
        a = abs(c)
        if a.denominator != 1:
            mag = rf"\frac{{{a.numerator}}}{{{a.denominator}}}"
        elif a == 1 and p != 0:
            mag = ""
        else:
            mag = str(a.numerator)
        term = mag + ("" if p == 0 else var if p == 1 else f"{var}^{{{p}}}")
        out.append((sign, term))
    if not out:
        return "0"
    s = ("-" if out[0][0] == "-" else "") + out[0][1]
    for sign, term in out[1:]:
        s += f" {sign} {term}"
    return s


def signed(c, var: str = "") -> str:
    """'+ 3x' / '- 3x' for building expressions."""
    c = Fraction(c)
    if c == 0:
        return ""
    a = abs(c)
    mag = (str(a) if a.denominator == 1 else rf"\frac{{{a.numerator}}}{{{a.denominator}}}")
    if a == 1 and var:
        mag = ""
    return f" {'-' if c < 0 else '+'} {mag}{var}"


def fr(v) -> str:
    """LaTeX for a Fraction / int."""
    v = Fraction(v)
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def sf(v: float, n: int = 3) -> str:
    """Round to n significant figures, Edexcel style (no trailing exponent)."""
    if v == 0:
        return "0"
    digits = n - int(math.floor(math.log10(abs(v)))) - 1
    r = round(v, digits)
    if digits <= 0:
        return str(int(r))
    return f"{r:.{digits}f}"


def dp(v: float, n: int = 2) -> str:
    return f"{v:.{n}f}"


def nz(rng: random.Random, lo: int, hi: int, exclude=(0,)) -> int:
    while True:
        v = rng.randint(lo, hi)
        if v not in exclude:
            return v


def pick(rng: random.Random, seq):
    return seq[rng.randrange(len(seq))]


def term(c, var: str = "x") -> str:
    """Leading term c*var as LaTeX: 3x, -x, x, \\frac{1}{2}x."""
    c = Fraction(c)
    if c == 1:
        return var
    if c == -1:
        return "-" + var
    return fr(c) + var


def quad_roots_tex(a: int, b: int, c: int) -> str:
    """Roots of ax^2+bx+c as a single (-b ± s√r)/2a expression, simplified."""
    from math import gcd as _g
    d = b * b - 4 * a * c
    s, r = 1, d
    for f in range(int(math.isqrt(d)), 1, -1):
        if d % (f * f) == 0:
            s, r = f, d // (f * f)
            break
    den = 2 * a
    g = _g(_g(abs(b), s), abs(den))
    b2, s2, den2 = -b // g, s // g, den // g
    if den2 < 0:
        b2, s2, den2 = -b2, s2, -den2
    rt = (str(s2) if s2 != 1 else "") + rf"\sqrt{{{r}}}"
    num = (f"{b2} \\pm {rt}" if b2 else rf"\pm {rt}")
    return num if den2 == 1 else rf"\frac{{{num}}}{{{den2}}}"


def asc(expr, var=x, upto: int = 6) -> str:
    """LaTeX of a polynomial in ascending powers (binomial-expansion style)."""
    expr = sp.expand(expr)
    out = []
    for i in range(upto + 1):
        c = expr.coeff(var, i)
        if c == 0:
            continue
        tex = L(c * var ** i) if i else L(c)
        if out:
            out.append(("- " + tex[1:].lstrip()) if tex.startswith("-") else ("+ " + tex))
        else:
            out.append(tex)
    return " ".join(out) or "0"
