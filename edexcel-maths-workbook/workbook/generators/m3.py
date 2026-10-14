"""Module 3: Sequences & trigonometry (3.1 - 3.4)."""
import math
from fractions import Fraction as F

import sympy as sp

from ..core import L, M, Q, asc, dp, fr, gen, nz, pick, sf, signed, term, x, t


def roots_deg(f, lo=0.0, hi=360.0, step=0.05):
    """All roots of f (degrees) on [lo, hi] by sign change + bisection, plus touching zeros."""
    out = []
    a = lo
    fa = f(a)
    while a < hi - 1e-12:
        b = min(a + step, hi)
        fb = f(b)
        if fa == 0:
            out.append(a)
        elif fa * fb < 0:
            l, r = a, b
            for _ in range(60):
                m = (l + r) / 2
                if f(l) * f(m) <= 0:
                    r = m
                else:
                    l = m
            out.append((l + r) / 2)
        elif abs(fa) < 1e-9:
            out.append(a)
        a, fa = b, fb
    if abs(f(hi)) < 1e-9:
        out.append(hi)
    res = []
    for r in out:
        if not res or abs(r - res[-1]) > 1e-4:
            res.append(r)
    return res


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def deg_list(rs, d=1):
    return ", ".join(f"{r:.{d}f}^\\circ" for r in rs)


S, C, T = math.sin, math.cos, math.tan
R = math.radians

# ------------------------------------------------------------------ 3.1
@gen("3.1", "Arithmetic sequences")
def ap_two_terms(rng):
    a, d = rng.randint(-10, 20), nz(rng, -6, 9)
    p, q = rng.randint(3, 8), rng.randint(10, 25)
    up, uq = a + (p - 1) * d, a + (q - 1) * d
    nn = rng.randint(20, 50)
    s = F(nn, 2) * (2 * a + (nn - 1) * d)
    return Q(f"The {ordinal(p)} term of an arithmetic sequence is ${up}$ and the {ordinal(q)} term is ${uq}$.\n(a) Find the first term and the common difference.\n(b) Find the sum of the first ${nn}$ terms.",
             ("(a)", 3, f"$a = {a}$, $d = {d}$", [f"M1 $a + {p-1}d = {up}$ and $a + {q-1}d = {uq}$", "A1 $d$", "A1 $a$"]),
             ("(b)", 2, f"$S_{{{nn}}} = {fr(s)}$", [f"M1 $\\frac{{{nn}}}{{2}}(2a + {nn-1}d)$", "A1"]))


@gen("3.1", "Arithmetic series", difficulty=2)
def ap_find_n(rng):
    a, d = rng.randint(2, 15), rng.randint(2, 7)
    nn = rng.randint(10, 40)
    s = nn * (2 * a + (nn - 1) * d) // 2 if (nn * (2 * a + (nn - 1) * d)) % 2 == 0 else None
    if s is None:
        nn += 1
        s = nn * (2 * a + (nn - 1) * d) // 2
    return Q(f"An arithmetic series has first term ${a}$ and common difference ${d}$. The sum of the first $n$ terms is ${s}$.\nShow that ${d}n^{{2}} {signed(2*a-d,'n')} - {2*s} = 0$ and hence find $n$.",
             ("", 4, f"$n = {nn}$", ["M1 uses $S_n = \\frac{n}{2}(2a + (n-1)d)$", "A1* rearranges to the given quadratic", "M1 solves", f"A1 $n = {nn}$ (reject negative)"]), difficulty=2)


@gen("3.1", "Geometric sequences")
def gp_terms(rng):
    a = rng.randint(2, 50)
    r = pick(rng, [F(1, 2), F(2), F(3), F(-1, 2), F(2, 3), F(3, 4), F(-2)])
    p, q = 2, rng.randint(4, 6)
    up, uq = a * r ** (p - 1), a * r ** (q - 1)
    return Q(f"The second term of a geometric sequence is ${fr(up)}$ and the {ordinal(q)} term is ${fr(uq)}$. Given that the common ratio is {'positive' if r > 0 else 'negative'}, find the common ratio and the first term.",
             ("", 4, f"$r = {fr(r)}$, $a = {a}$", [f"M1 $\\frac{{ar^{{{q-1}}}}}{{ar}} = r^{{{q-2}}}$", f"A1 $r = {fr(r)}$", "M1 substitutes back", "A1 $a$"]))


@gen("3.1", "Geometric series")
def gp_sum(rng):
    a = rng.randint(2, 30)
    r = pick(rng, [1.05, 1.1, 0.9, 0.8, 1.2, 0.75, 1.5])
    nn = rng.randint(8, 20)
    s = a * (r ** nn - 1) / (r - 1)
    return Q(f"A geometric series has first term ${a}$ and common ratio ${r}$. Find the sum of the first ${nn}$ terms, giving your answer to 3 significant figures.",
             ("", 2, f"${sf(s)}$", [f"M1 $\\frac{{{a}(1 - {r}^{{{nn}}})}}{{1 - {r}}}$", "A1"]))


@gen("3.1", "Sum to infinity", difficulty=2)
def gp_infinity(rng):
    r = pick(rng, [F(1, 2), F(1, 3), F(2, 3), F(3, 4), F(-1, 2), F(1, 4), F(2, 5)])
    a = rng.randint(2, 12) * r.denominator
    sinf = a / (1 - r)
    u2 = a * r
    rr = sp.Symbol("r")
    roots = sp.solve(sp.nsimplify(sinf) * rr ** 2 - sp.nsimplify(sinf) * rr + sp.nsimplify(u2), rr)
    keep = [v for v in roots if abs(float(v)) < 1]
    drop = [v for v in roots if abs(float(v)) >= 1]
    ans = "$r = " + ", ".join(L(v) for v in keep) + "$" + ("" if not drop else " (reject $r = " + ", ".join(L(v) for v in drop) + "$ since $|r| \\geq 1$)")
    return Q(f"A geometric series has second term ${fr(u2)}$ and sum to infinity ${fr(sinf)}$.\n(a) Show that ${fr(sinf)}r^{{2}} - {fr(sinf)}r{signed(u2)} = 0$.\n(b) Hence find the possible values of the common ratio, $r$, explaining why any value must be rejected.",
             ("(a)", 3, "given", [f"M1 $ar = {fr(u2)}$", f"M1 $\\frac{{a}}{{1 - r}} = {fr(sinf)}$", "A1* eliminates $a$"]),
             ("(b)", 3, ans, ["M1 solves the quadratic", "A1 roots", "B1 requires $|r| < 1$ for a sum to infinity"]), difficulty=2)


@gen("3.1", "Sigma notation")
def sigma_ap(rng):
    a, b = nz(rng, -4, 7), rng.randint(-9, 9)
    lo, hi = rng.randint(1, 5), rng.randint(15, 40)
    tot = sum(a * r + b for r in range(lo, hi + 1))
    return Q(f"Find $\\sum_{{r={lo}}}^{{{hi}}}({term(a,'r')}{signed(b)})$.",
             ("", 3, f"${tot}$", [f"M1 recognises an arithmetic series with ${hi-lo+1}$ terms", f"M1 first term ${a*lo+b}$, last term ${a*hi+b}$", "A1"]))


@gen("3.1", "Sigma notation", difficulty=2)
def sigma_gp(rng):
    a, r = rng.randint(2, 9), pick(rng, [2, 3, F(1, 2)])
    nn = rng.randint(6, 12)
    tot = sum(a * F(r) ** k for k in range(1, nn + 1))
    return Q(f"Find the exact value of $\\sum_{{k=1}}^{{{nn}}} {a}\\left({fr(r)}\\right)^{{k}}$.",
             ("", 3, f"${fr(tot)}$", ["M1 geometric with $a = " + fr(a * F(r)) + "$, $r = " + fr(r) + "$", "M1 sum formula", "A1"]), difficulty=2)


@gen("3.1", "Recurrence relations, increasing / decreasing / periodic")
def recurrence(rng):
    kk, c, u1 = nz(rng, -3, 3), rng.randint(-5, 5), rng.randint(-4, 6)
    us = [u1]
    for _ in range(3):
        us.append(kk * us[-1] + c)
    return Q(f"A sequence is defined by $u_{{1}} = {u1}$, $u_{{n+1}} = {term(kk,'u_{n}')}{signed(c)}$. Find $u_{{2}}$, $u_{{3}}$ and $u_{{4}}$, and state whether the sequence is increasing, decreasing or neither.",
             ("", 3, f"$u_2 = {us[1]}$, $u_3 = {us[2]}$, $u_4 = {us[3]}$; " + ("increasing" if us[1] > us[0] and us[2] > us[1] and us[3] > us[2] else "decreasing" if us[1] < us[0] and us[2] < us[1] and us[3] < us[2] else "neither"),
              ["M1 uses the recurrence", "A1 all three terms", "B1 description"]))


@gen("3.1", "Recurrence relations, increasing / decreasing / periodic", difficulty=2)
def periodic(rng):
    kk = rng.randint(2, 6)
    u1 = rng.randint(1, 5)
    if u1 == kk:
        u1 += 1
    nn = rng.randint(20, 60)
    seq = [u1, F(kk, u1)]
    s = sum(seq[i % 2] for i in range(nn))
    return Q(f"A sequence is defined by $u_{{1}} = {u1}$, $u_{{n+1}} = \\frac{{{kk}}}{{u_{{n}}}}$.\n(a) Show that the sequence is periodic and state its order.\n(b) Find $\\sum_{{r=1}}^{{{nn}}} u_{{r}}$.",
             ("(a)", 2, f"$u_2 = {fr(seq[1])}$, $u_3 = {u1}$; period 2", ["M1 finds $u_2$, $u_3$", "A1 order 2"]),
             ("(b)", 2, f"${fr(s)}$", ["M1 counts complete cycles", "A1"]), difficulty=2)


@gen("3.1", "Modelling with series", difficulty=2)
def series_model(rng):
    a = rng.randint(18, 35) * 1000
    pct = rng.randint(2, 6)
    r = 1 + pct / 100
    target = pick(rng, [40000, 45000, 50000, 60000])
    if a * r ** 3 > target:
        target = int(a * 2)
    nn = math.ceil(math.log(target / a) / math.log(r)) + 1
    yrs = 10
    tot = a * (r ** yrs - 1) / (r - 1)
    return Q(f"Sam's salary in year 1 is £{a:,}. It increases by {pct}% each year.\n(a) Find the first year in which Sam's salary exceeds £{target:,}.\n(b) Find the total Sam earns over the first {yrs} years, to the nearest £.",
             ("(a)", 3, f"year {nn}", [f"M1 ${a}({r})^{{n-1}} > {target}$", "M1 logs", f"A1 year {nn}"]),
             ("(b)", 2, f"£{round(tot):,}", ["M1 geometric sum", "A1"]), difficulty=2)


# ------------------------------------------------------------------ 3.2
@gen("3.2", "Radian measure")
def radians_convert(rng):
    d = pick(rng, [30, 45, 60, 120, 135, 150, 210, 225, 270, 300, 315, 330, 75, 15])
    v = F(d, 180)
    r2 = pick(rng, [F(5, 6), F(7, 4), F(2, 3), F(11, 6), F(5, 4), F(3, 2)])
    return Q(f"(a) Convert ${d}^\\circ$ to radians, giving your answer as an exact multiple of $\\pi$.\n(b) Convert ${fr(r2)}\\pi$ radians to degrees.",
             ("(a)", 1, f"${fr(v)}\\pi$", ["B1"]), ("(b)", 1, f"${int(r2*180)}^\\circ$", ["B1"]))


@gen("3.2", "Arc length")
def arc_sector(rng):
    r = rng.randint(3, 15)
    th = round(rng.uniform(0.4, 2.6), 2)
    arc, area = r * th, 0.5 * r * r * th
    return Q(f"A sector $OAB$ of a circle has radius ${r}$ cm and angle ${th}$ radians at the centre $O$.\n(a) Find the length of the arc $AB$.\n(b) Find the perimeter of the sector.\n(c) Find the area of the sector.",
             ("(a)", 1, f"${sf(arc)}$ cm", ["B1 $r\\theta$"]), ("(b)", 1, f"${sf(arc + 2*r)}$ cm", ["B1ft"]), ("(c)", 2, f"${sf(area)}$ cm$^2$", ["M1 $\\frac{1}{2}r^{2}\\theta$", "A1"]))


@gen("3.2", "Sector and segment areas", difficulty=2)
def segment(rng):
    r = rng.randint(4, 12)
    th = round(rng.uniform(0.6, 2.4), 2)
    seg = 0.5 * r * r * (th - math.sin(th))
    return Q(f"The chord $AB$ subtends an angle of ${th}$ radians at the centre $O$ of a circle of radius ${r}$ cm. Find the area of the minor segment cut off by $AB$, giving your answer to 3 significant figures.",
             ("", 4, f"${sf(seg)}$ cm$^2$", ["M1 sector area $\\frac{1}{2}r^{2}\\theta$", "M1 triangle area $\\frac{1}{2}r^{2}\\sin\\theta$", "M1 subtracts", "A1"]), difficulty=2)


@gen("3.2", "Small angle approximations", difficulty=2)
def small_angle(rng):
    a, b, c = rng.randint(1, 5), rng.randint(1, 4), rng.randint(2, 5)
    th = sp.Symbol("theta")
    choice = rng.randrange(3)
    if choice == 0:
        e = (1 - sp.cos(a * th)) / (th * sp.sin(b * th))
        approx = sp.Rational(a * a, 2 * b)
        tex = rf"\frac{{1 - \cos {a if a > 1 else ''}\theta}}{{\theta \sin {b if b > 1 else ''}\theta}}"
    elif choice == 1:
        e = (sp.sin(a * th) + sp.tan(b * th)) / (c * th)
        approx = sp.Rational(a + b, c)
        tex = rf"\frac{{\sin {a if a>1 else ''}\theta + \tan {b if b>1 else ''}\theta}}{{{c}\theta}}"
    else:
        e = sp.cos(a * th) + th * sp.sin(b * th)
        approx = 1 + (sp.Rational(-a * a, 2) + b) * th ** 2
        tex = rf"\cos {a if a>1 else ''}\theta + \theta\sin {b if b>1 else ''}\theta"
    return Q(f"Given that $\\theta$ is small, use the small angle approximations to find an approximation for ${tex}$" + (" as a constant." if choice < 2 else " in the form $p + q\\theta^{2}$."),
             ("", 3, f"${L(approx)}$", ["M1 uses $\\sin\\theta \\approx \\theta$, $\\cos\\theta \\approx 1 - \\frac{\\theta^{2}}{2}$, $\\tan\\theta \\approx \\theta$", "M1 simplifies", "A1"]), difficulty=2)


@gen("3.2", "sec, cosec and cot")
def sec_equation(rng):
    fn, val = pick(rng, [("sec", 2), ("sec", -2), ("cosec", 2), ("cosec", -1.5), ("cot", 1), ("cot", -0.5), ("sec", 3), ("cosec", 4)])
    f = {"sec": lambda d: 1 / C(R(d)) - val if abs(C(R(d))) > 1e-9 else 1e9,
         "cosec": lambda d: 1 / S(R(d)) - val if abs(S(R(d))) > 1e-9 else 1e9,
         "cot": lambda d: C(R(d)) - val * S(R(d))}[fn]
    rs = [r for r in roots_deg(f, 0, 360) if abs(r - 360) > 1e-6]
    base = {"sec": "cos", "cosec": "sin", "cot": "tan"}[fn]
    return Q(f"Solve, for $0 \\leq x < 360^\\circ$, $\\mathrm{{{fn}}}\\,x = {val}$, giving your answers to 1 decimal place.",
             ("", 3, f"$x = {deg_list(rs)}$", [f"M1 $\\{base} x = {fr(F(1)/F(str(val)))}$" if fn != "cot" else f"M1 $\\tan x = {fr(F(1)/F(str(val)))}$", "A1 one value", "A1 all values"]))


@gen("3.2", "Identities 1 + tan^2 = sec^2 and 1 + cot^2 = cosec^2", difficulty=2)
def sec2_equation(rng):
    # a sec^2 x + b tan x + c = 0 -> a(1 + tan^2) + b tan + c = 0 with nice tan roots
    t1, t2 = pick(rng, [(1, 2), (1, -2), (-1, 3), (2, -3), (1, -1), (F(1, 2), 1), (-1, -2)])
    a = 1
    b, c0 = -(F(t1) + F(t2)), F(t1) * F(t2)
    # tan^2 + b tan + c0 = 0 => sec^2 + b tan + c0 - 1 = 0
    f = lambda d: T(R(d)) ** 2 + float(b) * T(R(d)) + float(c0) if abs(C(R(d))) > 1e-6 else 1e9
    rs = [r for r in roots_deg(f, 0, 360) if abs(r - 360) > 1e-6 and abs(C(R(r))) > 1e-6]
    return Q(f"Solve, for $0 \\leq x < 360^\\circ$, $\\sec^{{2}} x {signed(b,'\\tan x')} {signed(c0-1)} = 0$.".replace("  ", " "),
             ("", 5, f"$x = {deg_list(rs)}$", ["M1 uses $\\sec^{2} x = 1 + \\tan^{2} x$", f"M1 $\\tan^{{2}} x{signed(b,'\\tan x')}{signed(c0)} = 0$", f"A1 $\\tan x = {fr(t1)}, {fr(t2)}$", "M1 finds angles in range", "A1 all"]), difficulty=2)


@gen("3.2", "Inverse trig functions arcsin, arccos, arctan")
def arc_exact(rng):
    fn, val, ans = pick(rng, [("arcsin", r"\frac{1}{2}", r"\frac{\pi}{6}"), ("arccos", r"-\frac{1}{2}", r"\frac{2\pi}{3}"), ("arctan", r"\sqrt{3}", r"\frac{\pi}{3}"),
                               ("arcsin", r"-\frac{\sqrt{2}}{2}", r"-\frac{\pi}{4}"), ("arccos", "0", r"\frac{\pi}{2}"), ("arctan", "-1", r"-\frac{\pi}{4}"), ("arccos", r"\frac{\sqrt{3}}{2}", r"\frac{\pi}{6}")])
    return Q(f"Find the exact value of $\\mathrm{{{fn}}}\\left({val}\\right)$ in radians, and state the domain and range of $y = \\mathrm{{{fn}}}\\,x$.",
             ("", 3, f"${ans}$; " + {"arcsin": r"domain $-1 \leq x \leq 1$, range $-\frac{\pi}{2} \leq y \leq \frac{\pi}{2}$",
                                     "arccos": r"domain $-1 \leq x \leq 1$, range $0 \leq y \leq \pi$",
                                     "arctan": r"domain $x \in \mathbb{R}$, range $-\frac{\pi}{2} < y < \frac{\pi}{2}$"}[fn], ["B1 value", "B1 domain", "B1 range"]))


# ------------------------------------------------------------------ 3.3
@gen("3.3", "Addition formulae")
def exact_compound(rng):
    fn, ang, ans, split = pick(rng, [("sin", 75, r"\frac{\sqrt{6} + \sqrt{2}}{4}", "45 + 30"), ("cos", 75, r"\frac{\sqrt{6} - \sqrt{2}}{4}", "45 + 30"),
                                      ("sin", 15, r"\frac{\sqrt{6} - \sqrt{2}}{4}", "45 - 30"), ("cos", 15, r"\frac{\sqrt{6} + \sqrt{2}}{4}", "45 - 30"),
                                      ("tan", 75, r"2 + \sqrt{3}", "45 + 30"), ("tan", 15, r"2 - \sqrt{3}", "45 - 30"), ("cos", 105, r"\frac{\sqrt{2} - \sqrt{6}}{4}", "60 + 45")])
    return Q(f"Using an appropriate addition formula, find the exact value of $\\{fn}\\,{ang}^\\circ$.",
             ("", 3, f"${ans}$", [f"M1 writes ${ang} = {split}$", "M1 correct expansion with exact values", "A1"]))


@gen("3.3", "Double-angle formulae", difficulty=2)
def double_angle_values(rng):
    p, q, h = pick(rng, [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)])
    quad = pick(rng, ["acute", "obtuse"])
    sinA = F(p, h)
    cosA = F(q, h) if quad == "acute" else -F(q, h)
    s2, c2 = 2 * sinA * cosA, cosA ** 2 - sinA ** 2
    t2 = s2 / c2
    return Q(f"Given that $\\sin A = {fr(sinA)}$ and that $A$ is {quad}, find the exact values of\n(a) $\\sin 2A$,  (b) $\\cos 2A$,  (c) $\\tan 2A$.",
             ("(a)", 2, f"${fr(s2)}$", [f"M1 $\\cos A = {fr(cosA)}$", "A1"]), ("(b)", 1, f"${fr(c2)}$", ["B1"]), ("(c)", 1, f"${fr(t2)}$", ["B1ft"]), difficulty=2)


@gen("3.3", "Harmonic form R cos(x ± a), R sin(x ± a)", difficulty=3)
def r_form(rng):
    a, b = pick(rng, [(3, 4), (4, 3), (5, 12), (1, 1), (2, 1), (1, 3), (12, 5), (2, 3), (6, 8)])
    form = pick(rng, ["cos-", "sin+", "cos+", "sin-"])
    Rv = math.hypot(a, b)
    alpha = math.degrees(math.atan2(b, a)) if form in ("cos-", "sin+") else math.degrees(math.atan2(b, a))
    # cos-: a cos x + b sin x = R cos(x - alpha), tan alpha = b/a
    # sin+: a sin x + b cos x = R sin(x + alpha), tan alpha = b/a
    # cos+: a cos x - b sin x = R cos(x + alpha)
    # sin-: a sin x - b cos x = R sin(x - alpha)
    expr = {"cos-": f"{a if a>1 else ''}\\cos x + {b if b>1 else ''}\\sin x", "sin+": f"{a if a>1 else ''}\\sin x + {b if b>1 else ''}\\cos x",
            "cos+": f"{a if a>1 else ''}\\cos x - {b if b>1 else ''}\\sin x", "sin-": f"{a if a>1 else ''}\\sin x - {b if b>1 else ''}\\cos x"}[form]
    target = {"cos-": r"R\cos(x - \alpha)", "sin+": r"R\sin(x + \alpha)", "cos+": r"R\cos(x + \alpha)", "sin-": r"R\sin(x - \alpha)"}[form]
    fx = {"cos-": lambda d: a * C(R(d)) + b * S(R(d)), "sin+": lambda d: a * S(R(d)) + b * C(R(d)),
          "cos+": lambda d: a * C(R(d)) - b * S(R(d)), "sin-": lambda d: a * S(R(d)) - b * C(R(d))}[form]
    k = round(rng.uniform(0.3, 0.9) * Rv, 1)
    rs = [r for r in roots_deg(lambda d: fx(d) - k, 0, 360) if r < 360 - 1e-6]
    Rtex = str(int(Rv)) if abs(Rv - round(Rv)) < 1e-9 else rf"\sqrt{{{a*a+b*b}}}"
    return Q(f"(a) Express ${expr}$ in the form ${target}$, where $R > 0$ and $0 < \\alpha < 90^\\circ$. Give $\\alpha$ to 2 decimal places.\n(b) Hence solve ${expr} = {k}$ for $0 \\leq x < 360^\\circ$, giving answers to 1 decimal place.\n(c) State the maximum value of ${expr}$.",
             ("(a)", 3, f"$R = {Rtex}$, $\\alpha = {alpha:.2f}^\\circ$", ["B1 $R$", f"M1 $\\tan\\alpha = {fr(F(b, a))}$", "A1 $\\alpha$"]),
             ("(b)", 4, f"$x = {deg_list(rs)}$", ["M1 divides by $R$ and uses inverse function", "A1 first angle", "M1 second angle in range", "A1 both"]),
             ("(c)", 1, f"${Rtex}$", ["B1ft"]), difficulty=3)


@gen("3.3", "Solving trig equations", difficulty=2)
def trig_quadratic(rng):
    fn = pick(rng, ["sin", "cos"])
    r1, r2 = pick(rng, [(F(1, 2), 2), (F(-1, 2), 3), (F(1, 3), -1), (F(2, 3), F(-1, 2)), (1, F(-1, 4)), (F(1, 2), -1), (F(-1, 3), 2)])
    # identity variant: write in terms of the other function
    A, B, Cc = 1, -(F(r1) + F(r2)), F(r1) * F(r2)
    den = math.lcm(A, B.denominator, Cc.denominator)
    A2, B2, C2 = den * A, den * B, den * Cc
    other = "cos" if fn == "sin" else "sin"
    # A2 fn^2 + B2 fn + C2 = 0 ; replace fn^2 = 1 - other^2:  -A2 other^2 + B2 fn + A2 + C2 = 0
    stem = f"{A2}\\{other}^{{2}} x {signed(-B2, chr(92)+fn+' x')} {signed(-(A2 + C2))} = 0"
    f = (lambda d: A2 * S(R(d)) ** 2 + float(B2) * S(R(d)) + float(C2)) if fn == "sin" else (lambda d: A2 * C(R(d)) ** 2 + float(B2) * C(R(d)) + float(C2))
    rs = [r for r in roots_deg(f, 0, 360) if r < 360 - 1e-6]
    valid = [fr(v) for v in (F(r1), F(r2)) if abs(v) <= 1]
    return Q(f"Solve, for $0 \\leq x < 360^\\circ$, ${stem}$, giving your answers to 1 decimal place.".replace("  ", " "),
             ("", 6, f"$x = {deg_list(rs)}$", [f"M1 uses $\\{other}^{{2}} x = 1 - \\{fn}^{{2}} x$", f"A1 ${A2}\\{fn}^{{2}} x {signed(B2, chr(92)+fn+' x')} {signed(C2)} = 0$", "M1 solves quadratic",
                                               f"A1 $\\{fn} x = {', '.join(valid)}$" + (" (reject values outside $[-1, 1]$)" if len(valid) < 2 else ""), "M1 finds angles", "A1 all, no extras"]), difficulty=2)


@gen("3.3", "Solving trig equations")
def trig_multiple_angle(rng):
    fn = pick(rng, ["sin", "cos", "tan"])
    m = pick(rng, [2, 3])
    shift = pick(rng, [0, 0, 20, 30, -15, 45])
    val = pick(rng, [0.5, -0.5, 0.3, -0.7, 0.8]) if fn != "tan" else pick(rng, [1, -1, 2, 0.5, -3])
    g = {"sin": S, "cos": C, "tan": T}[fn]
    f = lambda d: g(R(m * d + shift)) - val if fn != "tan" or abs(C(R(m * d + shift))) > 1e-6 else 1e9
    rs = [r for r in roots_deg(f, 0, 180) if r < 180 - 1e-6 and (fn != "tan" or abs(f(r)) < 1e-6)]
    inner = f"{m}x" + (f" {'+' if shift > 0 else '-'} {abs(shift)}^\\circ" if shift else "")
    return Q(f"Solve, for $0 \\leq x < 180^\\circ$, $\\{fn}({inner}) = {val}$, giving your answers to 1 decimal place.",
             ("", 4, f"$x = {deg_list(rs)}$", [f"M1 adjusts the interval for ${inner}$", "A1 one correct angle", "M1 uses symmetry/period to find others", "A1 all, no extras"]))


@gen("3.3", "Proving trig identities", difficulty=2)
def prove_identity(rng):
    lhs, rhs, hint = pick(rng, [
        (r"\frac{1 - \cos 2\theta}{\sin 2\theta}", r"\tan\theta", r"$\cos 2\theta = 1 - 2\sin^{2}\theta$, $\sin 2\theta = 2\sin\theta\cos\theta$"),
        (r"\frac{\sin\theta}{1 + \cos\theta} + \frac{1 + \cos\theta}{\sin\theta}", r"2\,\mathrm{cosec}\,\theta", "common denominator, $\\sin^{2} + \\cos^{2} = 1$"),
        (r"(\sec\theta - \tan\theta)(\sec\theta + \tan\theta)", "1", "difference of two squares and $\\sec^{2} = 1 + \\tan^{2}$"),
        (r"\cot\theta + \tan\theta", r"2\,\mathrm{cosec}\,2\theta", "write in $\\sin$, $\\cos$; use $\\sin 2\\theta$"),
        (r"\frac{\cos 2\theta}{\cos\theta + \sin\theta}", r"\cos\theta - \sin\theta", "$\\cos 2\\theta = \\cos^{2} - \\sin^{2}$, difference of two squares"),
        (r"\sin 3\theta", r"3\sin\theta - 4\sin^{3}\theta", "$\\sin(2\\theta + \\theta)$, then double-angle formulae"),
        (r"\frac{1 + \tan^{2}\theta}{1 - \tan^{2}\theta}", r"\sec 2\theta", "multiply through by $\\cos^{2}\\theta$")])
    return Q(f"Prove that ${lhs} \\equiv {rhs}$.", ("", 4, "Proof using " + hint, ["M1 correct identity used", "M1 manipulates towards RHS", "M1 second identity/simplification", "A1* fully correct proof"]), difficulty=2)


@gen("3.3", "Modelling with trig functions", difficulty=2)
def trig_model(rng):
    A, B, w, ph = rng.randint(6, 12), round(rng.uniform(1.5, 4.5), 1), 30, rng.randint(0, 3) * 15
    hmax, hmin = A + B, A - B
    return Q(f"The depth of water, $D$ metres, in a harbour $t$ hours after midnight is modelled by $D = {A} + {B}\\sin({w}t{'+' + str(ph) if ph else ''})^\\circ$, $0 \\leq t < 24$.\n(a) State the maximum depth and find the first time it occurs.\n(b) A boat needs at least ${A}$ m of water. For how long, in each 12-hour period, can it enter the harbour?",
             ("(a)", 3, f"${hmax}$ m at $t = {fr(F(90 - ph, w))}$ hours", ["B1 max", "M1 sets the angle to $90^\\circ$", "A1 time"]),
             ("(b)", 2, "6 hours", ["M1 $\\sin \\geq 0$ for half of each cycle", "A1"]), difficulty=2)


# ------------------------------------------------------------------ 3.4
@gen("3.4", "Parametric to Cartesian")
def param_to_cart(rng):
    a, b, c = nz(rng, -4, 4), rng.randint(-5, 5), rng.randint(-5, 5)
    e = sp.expand(((x - b) / a) ** 2 + c)
    return Q(f"A curve has parametric equations $x = {L(a*t + b)}$, $y = t^{{2}} {signed(c)}$. Find a Cartesian equation of the curve in the form $y = f(x)$.",
             ("", 2, f"$y = {L(e)}$", [f"M1 $t = \\frac{{{L(x - b)}}}{{{a}}}$", "A1"]))


@gen("3.4", "Trig parametric conversions", difficulty=2)
def param_trig(rng):
    a, b = rng.randint(2, 6), rng.randint(2, 6)
    p, q = rng.randint(-3, 3), rng.randint(-3, 3)
    kind = rng.randrange(3)
    if kind == 0:
        return Q(f"A curve $C$ has parametric equations $x = {a}\\cos t {signed(p)}$, $y = {b}\\sin t {signed(q)}$, $0 \\leq t < 2\\pi$. Find a Cartesian equation of $C$ and describe the curve.".replace("  ", " "),
                 ("", 3, f"$\\frac{{(x {signed(-p)[1:] if p else ''})^{{2}}}}{{{a*a}}} + \\frac{{(y {signed(-q)[1:] if q else ''})^{{2}}}}{{{b*b}}} = 1$".replace("(x )", "x").replace("(y )", "y") + ("; a circle" if a == b else "; an ellipse"),
                  ["M1 isolates $\\cos t$ and $\\sin t$", "M1 uses $\\sin^{2} t + \\cos^{2} t = 1$", "A1"]), difficulty=2)
    if kind == 1:
        return Q(f"A curve has parametric equations $x = \\sin t$, $y = {a}\\cos 2t$, $-\\frac{{\\pi}}{{2}} \\leq t \\leq \\frac{{\\pi}}{{2}}$. Show that a Cartesian equation is $y = {a} - {2*a}x^{{2}}$ and state the domain of $x$.",
                 ("", 3, f"$y = {a}(1 - 2\\sin^{{2}} t) = {a} - {2*a}x^{{2}}$, $-1 \\leq x \\leq 1$", ["M1 $\\cos 2t = 1 - 2\\sin^{2} t$", "A1*", "B1 domain"]), difficulty=2)
    return Q(f"A curve has parametric equations $x = {a}\\sec t$, $y = {b}\\tan t$. Find a Cartesian equation of the curve.",
             ("", 3, f"$\\frac{{x^{{2}}}}{{{a*a}}} - \\frac{{y^{{2}}}}{{{b*b}}} = 1$", ["M1 $\\sec^{2} t - \\tan^{2} t = 1$", "M1 substitutes", "A1"]), difficulty=2)


@gen("3.4", "Intersections with parametric curves", difficulty=2)
def param_intersect(rng):
    t1, t2 = sorted(rng.sample(range(-4, 5), 2))
    # curve x = t^2, y = 2t ; line through two param points
    p1, p2 = (t1 * t1, 2 * t1), (t2 * t2, 2 * t2)
    if t1 + t2 == 0:
        return Q(f"The curve $C$ has parametric equations $x = t^{{2}}$, $y = 2t$. Find the values of $t$ where $C$ meets the line $x = {t1*t1}$, and the coordinates of these points.",
                 ("", 3, f"$t = \\pm {abs(t1)}$: $({t1*t1}, {2*t1})$ and $({t1*t1}, {-2*t1})$", ["M1 $t^{2} = " + str(t1 * t1) + "$", "A1 $t$", "A1 points"]), difficulty=2)
    m = F(p2[1] - p1[1], p2[0] - p1[0])
    c = p1[1] - m * p1[0]
    return Q(f"The curve $C$ has parametric equations $x = t^{{2}}$, $y = 2t$. The line $y = {fr(m)}x {signed(c)}$ meets $C$ at two points. Find the coordinates of these points.",
             ("", 4, f"$({p1[0]}, {p1[1]})$ and $({p2[0]}, {p2[1]})$", ["M1 substitutes parametric forms into the line", "A1 quadratic in $t$", "M1 solves", "A1 both points"]), difficulty=2)


@gen("3.4", "Sketching parametric curves")
def param_axes(rng):
    a, b, c = nz(rng, -3, 3), rng.randint(-6, 6), rng.randint(1, 5)
    # x = a t + b ; y = t^2 - c^2 -> meets x-axis at t = ±c
    pts = sorted({a * c + b, -a * c + b})
    return Q(f"A curve has parametric equations $x = {L(a*t + b)}$, $y = t^{{2}} - {c*c}$. Find the coordinates of the points where the curve meets the $x$-axis, and the point where $t = 0$.",
             ("", 3, ", ".join(f"$({p}, 0)$" for p in pts) + f"; $t = 0$ gives $({b}, {-c*c})$", ["M1 $y = 0 \\Rightarrow t = \\pm " + str(c) + "$", "A1 both points", "B1"]))


@gen("3.4", "Modelling with parametric equations", difficulty=2)
def param_model(rng):
    u, a = rng.randint(10, 30), rng.randint(30, 60)
    ux, uy = u * math.cos(R(a)), u * math.sin(R(a))
    tt = 2 * uy / 9.8
    return Q(f"A ball is kicked from ground level. Its position after $t$ seconds is modelled by $x = {ux:.2f}t$, $y = {uy:.2f}t - 4.9t^{{2}}$ (metres).\n(a) Find the time when the ball lands.\n(b) Find the horizontal distance travelled.\n(c) Find a Cartesian equation of its path.",
             ("(a)", 2, f"$t = {sf(tt)}$ s", ["M1 $y = 0$", "A1"]), ("(b)", 1, f"${sf(ux*tt)}$ m", ["B1ft"]),
             ("(c)", 2, f"$y = {sf(uy/ux)}x - {sf(4.9/ux**2)}x^{{2}}$", ["M1 eliminates $t$", "A1"]), difficulty=2)
