"""Module 1: Core foundation & coordinate geometry (1.1 - 1.5)."""
from fractions import Fraction as F
from math import gcd, isqrt

import sympy as sp

from ..core import L, M, Q, fr, gen, nz, pick, poly, quad_roots_tex, sf, signed, term, x, y


def sqfree_split(n):
    a = 1
    for f in range(isqrt(n), 1, -1):
        if n % (f * f) == 0:
            return f, n // (f * f)
    return a, n


def surd(a, b):
    """a*sqrt(b) as LaTeX."""
    if b == 1:
        return str(a)
    return ("" if a == 1 else "-" if a == -1 else str(a)) + rf"\sqrt{{{b}}}"


# ------------------------------------------------------------------ 1.1
@gen("1.1", "Index laws")
def indices_simplify(rng):
    a, b = rng.randint(2, 5), rng.randint(2, 4)
    p, c = rng.randint(2, 5), rng.randint(1, 6)
    d = rng.randint(2, 6)
    expr = rf"\frac{{({a}x^{{{p}}})^{{{b}}}}}{{{d}x^{{{c}}}}}"
    coeff = F(a ** b, d)
    power = p * b - c
    ans = sp.Rational(coeff.numerator, coeff.denominator) * sp.Symbol("x") ** power
    return Q(f"Simplify fully ${expr}$.",
             ("", 2, M(ans), [f"M1 uses $(x^m)^n = x^{{mn}}$ to get ${a**b}x^{{{p*b}}}$", f"A1 ${L(ans)}$"]))


@gen("1.1", "Negative and fractional indices")
def frac_index_eval(rng):
    base, q = pick(rng, [(2, 3), (3, 3), (4, 2), (5, 2), (2, 5), (3, 2), (6, 2), (10, 3), (2, 2), (7, 2), (4, 3)])
    p = pick(rng, [p for p in (1, 2, 3, 4, -1, -2, -3) if p % q and abs(p) * q <= 12 or p in (1, -1)])
    val = base ** q
    num = F(base) ** p
    return Q(f"Without using a calculator, find the exact value of ${val}^{{{fr(F(p, q))}}}$.",
             ("", 2, f"${fr(num)}$", [f"M1 ${val}^{{1/{q}}} = {base}$", f"A1 ${fr(num)}$"]))


@gen("1.1", "Negative and fractional indices", difficulty=2)
def write_as_power(rng):
    a = rng.randint(2, 9)
    p, q = pick(rng, [(1, 2), (3, 2), (1, 3), (2, 3), (5, 2)])
    root = r"\sqrt{x}" if (p, q) == (1, 2) else (rf"\sqrt{{x^{{{p}}}}}" if q == 2 else (r"\sqrt[3]{x}" if p == 1 else rf"\sqrt[3]{{x^{{{p}}}}}"))
    b = rng.randint(2, 9)
    c = rng.randint(1, 3)
    expr = rf"\frac{{{a}x^{{{c}}} - {b}}}{{{root}}}"
    e1, e2 = F(c) - F(p, q), -F(p, q)
    ans = f"${a}x^{{{fr(e1)}}} - {b}x^{{{fr(e2)}}}$"
    return Q(f"Write ${expr}$ in the form $Ax^{{m}} + Bx^{{n}}$, where $A$, $B$, $m$ and $n$ are constants.",
             ("", 3, ans, [f"M1 ${root} = x^{{{fr(F(p, q))}}}$", "M1 divides each term (subtracts powers)", "A1 " + ans]))


@gen("1.1", "Index laws", difficulty=2)
def index_equation(rng):
    b = pick(rng, [2, 3])
    m1, m2, m3 = pick(rng, [(1, 2, 3), (2, 1, 3), (1, 3, 2), (3, 1, 2)]) if b == 2 else pick(rng, [(1, 2, 3), (2, 1, 2)])
    base1, base2, base3 = b ** m1, b ** m2, b ** m3
    p, c = rng.randint(1, 4), rng.randint(-3, 5)
    # base1^x * base2^(x+p) = base3^c  =>  m1 x + m2 (x+p) = m3 c
    sol = F(m3 * c - m2 * p, m1 + m2)
    return Q(f"Solve ${base1}^{{x}} \\times {base2}^{{x+{p}}} = {base3}^{{{c}}}$." if c >= 0 else
             f"Solve ${base1}^{{x}} \\times {base2}^{{x+{p}}} = {base3}^{{{c}}}$.",
             ("", 3, f"$x = {fr(sol)}$", [f"M1 writes every term as a power of {b}", f"M1 ${term(m1)} + {'' if m2 == 1 else m2}(x + {p}) = {m3*c}$", f"A1 $x = {fr(sol)}$"]))


@gen("1.1", "Surds")
def surd_simplify(rng):
    a, b = rng.randint(2, 6), pick(rng, [2, 3, 5, 6, 7])
    c, d = rng.randint(2, 6), b
    n1, n2 = a * a * b, c * c * d
    tot = a + c if rng.random() < 0.6 else a - c
    sign = "+" if tot == a + c else "-"
    return Q(f"Simplify $\\sqrt{{{n1}}} {sign} \\sqrt{{{n2}}}$, giving your answer in the form $k\\sqrt{{{b}}}$.",
             ("", 2, f"${surd(tot, b)}$" if tot not in (0,) else "$0$", [f"M1 $\\sqrt{{{n1}}} = {a}\\sqrt{{{b}}}$ or $\\sqrt{{{n2}}} = {c}\\sqrt{{{d}}}$", f"A1 ${surd(tot, b)}$"]))


@gen("1.1", "Rationalising denominators")
def rationalise(rng):
    while True:
        a, p, s = rng.randint(1, 9), rng.randint(1, 5), pick(rng, [2, 3, 5, 6, 7])
        den = p * p - s
        if den != 0:
            break
    sign = pick(rng, ["+", "-"])
    expr = sp.Integer(a) / (p + (1 if sign == "+" else -1) * sp.sqrt(s))
    ans = sp.radsimp(expr)
    return Q(f"Express $\\frac{{{a}}}{{{p} {sign} \\sqrt{{{s}}}}}$ in the form $a + b\\sqrt{{{s}}}$, where $a$ and $b$ are rational.",
             ("", 3, M(sp.expand(ans)), [f"M1 multiplies numerator and denominator by ${p} {'-' if sign=='+' else '+'} \\sqrt{{{s}}}$",
                                         f"M1 denominator $= {den}$", f"A1 ${L(sp.expand(ans))}$"]))


@gen("1.1", "Rationalising denominators", difficulty=2)
def rationalise_hard(rng):
    s = pick(rng, [2, 3, 5, 7])
    a, b, c, d = nz(rng, -5, 5), nz(rng, 1, 4), rng.randint(1, 5), nz(rng, 1, 3)
    if c * c == d * d * s:
        c += 1
    expr = (a + b * sp.sqrt(s)) / (c + d * sp.sqrt(s))
    ans = sp.expand(sp.radsimp(expr))
    return Q(f"Show that $\\frac{{{a} + {b}\\sqrt{{{s}}}}}{{{c} + {surd(d, s)}}}$ can be written as $p + q\\sqrt{{{s}}}$, where $p$ and $q$ are rational, and find $p$ and $q$.".replace("+ -", "- "),
             ("", 4, M(ans), [f"M1 multiplies by ${c} - {surd(d, s)}$", "M1 expands numerator (4 terms)", f"M1 denominator ${c*c - d*d*s}$", f"A1 ${L(ans)}$"]),
             difficulty=2)


@gen("1.1", "Expanding brackets")
def expand_triple(rng):
    a, b, c = nz(rng, -6, 6), nz(rng, -6, 6), nz(rng, -5, 5)
    m = rng.randint(1, 3)
    e = (x + a) * (x + b) * (m * x + c)
    return Q(f"Expand and simplify ${L(x + a)}\\,(x {'+' if b>0 else '-'} {abs(b)})({L(m*x + c)})$.".replace("\\,(", "(").replace(f"${L(x+a)}", f"$({L(x+a)})"),
             ("", 3, M(sp.expand(e)), ["M1 expands two brackets correctly", "M1 multiplies by third bracket", f"A1 ${L(sp.expand(e))}$"]))


@gen("1.1", "Factorising")
def factorise_cubic(rng):
    a, b = nz(rng, -7, 7), nz(rng, -7, 7)
    k = pick(rng, [1, 2, 3])
    choice = rng.random()
    if choice < 0.5:
        e = sp.expand(k * x * (x + a) * (x + b))
        ans = sp.factor(e)
        return Q(f"Factorise fully ${L(e)}$.", ("", 3, M(ans), [f"M1 takes out ${L(k*x)}$", "M1 attempts to factorise the quadratic", f"A1 ${L(ans)}$"]))
    p, q = rng.randint(1, 6), rng.randint(2, 7)
    e = sp.expand(k * x * (q * q * x * x - p * p))
    ans = sp.factor(e)
    return Q(f"Factorise fully ${L(e)}$.", ("", 3, M(ans), [f"M1 takes out a common factor ${L(k*x)}$", "M1 difference of two squares", f"A1 ${L(ans)}$"]))


# ------------------------------------------------------------------ 1.2
@gen("1.2", "Solving by factorising")
def solve_factorise(rng):
    p, q = rng.randint(1, 3), nz(rng, -7, 7)
    r, s = rng.randint(1, 3), nz(rng, -7, 7)
    e = sp.expand((p * x + q) * (r * x + s))
    sols = sorted({F(-q, p), F(-s, r)})
    return Q(f"Solve ${L(e)} = 0$.",
             ("", 3, ", ".join(f"$x = {fr(v)}$" for v in sols), [f"M1 factorises: $({L(p*x+q)})({L(r*x+s)})$", "A1 one correct root", "A1 both roots"]))


@gen("1.2", "Completing the square")
def cts_monic(rng):
    b, c = nz(rng, -6, 6) * 2 if rng.random() < 0.6 else nz(rng, -9, 9), rng.randint(-10, 15)
    p = F(b, 2)
    q = c - p * p
    return Q(f"(a) Write $x^{{2}} {signed(b,'x')} {signed(c)}$ in the form $(x + p)^{{2}} + q$, where $p$ and $q$ are constants.\n(b) Hence state the coordinates of the turning point of $y = x^{{2}}{signed(b,'x')}{signed(c)}$.".replace("  ", " "),
             ("(a)", 2, f"$(x {signed(p)[1:]})^{{2}} {signed(q) or '+ 0'}$", ["B1 $p = " + fr(p) + "$", "M1A1 $q = " + fr(q) + "$" if True else ""]),
             ("(b)", 1, f"$({fr(-p)}, {fr(q)})$", ["B1ft"]))


@gen("1.2", "Completing the square", difficulty=2)
def cts_nonmonic(rng):
    a = pick(rng, [2, 3, -2, -1, 4])
    p, q = nz(rng, -4, 4), rng.randint(-9, 9)
    e = sp.expand(a * (x + p) ** 2 + q)
    return Q(f"Express ${L(e)}$ in the form $a(x + b)^{{2}} + c$, where $a$, $b$ and $c$ are integers. Hence state the {'minimum' if a>0 else 'maximum'} value of ${L(e)}$.",
             ("", 4, f"${a}(x {signed(p)[1:]})^{{2}} {signed(q) or '+ 0'}$; {'minimum' if a>0 else 'maximum'} value ${q}$",
              [f"B1 $a = {a}$", f"M1 $b = {p}$", f"A1 $c = {q}$", f"B1ft {'min' if a>0 else 'max'} value $= {q}$"]),
             difficulty=2)


@gen("1.2", "Quadratic formula")
def qformula(rng):
    while True:
        a, b, c = rng.randint(1, 4), nz(rng, -9, 9), nz(rng, -9, 9)
        d = b * b - 4 * a * c
        if d > 0 and isqrt(d) ** 2 != d:
            break
    sols = sp.solve(a * x ** 2 + b * x + c, x)
    return Q(f"Solve ${poly([a, b, c])} = 0$, giving your answers in exact simplified surd form.",
             ("", 3, f"$x = {quad_roots_tex(a, b, c)}$", ["M1 correct substitution into the formula", f"M1 discriminant $= {d}$", "A1 both roots, simplified"]))


@gen("1.2", "The discriminant", difficulty=2)
def discriminant_k(rng):
    # k x^2 + b x + (k + c) = 0 has equal roots, or equation with parameter in constant
    b, a = nz(rng, -8, 8), rng.randint(1, 3)
    mode = rng.random()
    if mode < 0.5:
        # a x^2 + b x + k = 0 has two distinct real roots -> k < b^2/(4a)
        crit = F(b * b, 4 * a)
        ask = pick(rng, ["two distinct real roots", "no real roots"])
        ans = f"$k < {fr(crit)}$" if ask.startswith("two") else f"$k > {fr(crit)}$"
        return Q(f"The equation ${poly([a, b, 0])} + k = 0$, where $k$ is a constant, has {ask}. Find the range of possible values of $k$.",
                 ("", 3, ans, ["M1 uses $b^{2} - 4ac$ with $a = " + str(a) + "$, $b = " + str(b) + "$, $c = k$", "M1 correct inequality " + ("$>0$" if ask.startswith("two") else "$<0$"), "A1 " + ans]), difficulty=2)
    # k x^2 + (k+p) x + q = 0? keep tractable: x^2 + k x + c = 0 equal roots -> k = ±2sqrt(c)
    c = pick(rng, [4, 9, 16, 25, 36, 1])
    r = isqrt(c)
    return Q(f"The equation $x^{{2}} + kx + {c} = 0$ has equal roots. Find the possible values of $k$.",
             ("", 3, f"$k = \\pm {2*r}$", [f"M1 $k^{{2}} - 4({c}) = 0$", "A1 $k^{2} = " + str(4 * c) + "$", f"A1 $k = \\pm {2*r}$"]), difficulty=2)


@gen("1.2", "The discriminant", difficulty=3)
def discriminant_quad_in_k(rng):
    # kx^2 + 2k x + (p - k)?? use: x^2 + (k + a) x + (k + b) = 0 no real roots -> (k+a)^2 - 4(k+b) < 0
    a, b = rng.randint(-3, 4), rng.randint(0, 6)
    # (k+a)^2 - 4k - 4b < 0 -> k^2 + (2a-4)k + a^2 - 4b < 0
    kk = sp.Symbol("k")
    expr = sp.expand((kk + a) ** 2 - 4 * (kk + b))
    roots = sp.solve(expr, kk)
    if len(roots) < 2 or any(not r.is_real for r in roots):
        return discriminant_k(rng)
    r1, r2 = sorted(roots, key=lambda r: float(r))
    return Q(f"The equation $x^{{2}} + (k {signed(a)[1:] if a else '+ 0'})x + (k {signed(b)[1:] if b else '+ 0'}) = 0$, where $k$ is a constant, has no real roots.\n(a) Show that ${L(expr)} < 0$.\n(b) Hence find the set of possible values of $k$.".replace("(k + 0)", "k"),
             ("(a)", 3, f"${L(expr)} < 0$", ["M1 uses $b^{2} - 4ac < 0$", "M1 expands", "A1* given answer, no errors"]),
             ("(b)", 3, f"${L(r1)} < k < {L(r2)}$", ["M1 solves the quadratic to find critical values", "M1 chooses the inside region", f"A1 ${L(r1)} < k < {L(r2)}$"]), difficulty=3)


@gen("1.2", "Hidden quadratics", difficulty=2)
def hidden_quadratic(rng):
    mode = rng.random()
    if mode < 0.5:
        r1, r2 = rng.randint(1, 5), rng.randint(1, 5)
        if r1 == r2:
            r2 += 1
        s, p = r1 + r2, r1 * r2
        return Q(f"Solve $x - {s}\\sqrt{{x}} + {p} = 0$.",
                 ("", 4, f"$x = {r1*r1}$, $x = {r2*r2}$", ["M1 lets $u = \\sqrt{x}$", f"M1 $(u - {r1})(u - {r2}) = 0$", "M1 squares to find $x$", "A1 both values"]), difficulty=2)
    a, b = rng.randint(1, 3), rng.randint(2, 4)
    if a == b:
        b += 1
    s, p = a * a + b * b, a * a * b * b
    return Q(f"Find all real solutions of $x^{{4}} - {s}x^{{2}} + {p} = 0$.",
             ("", 4, f"$x = \\pm {a}$, $x = \\pm {b}$", ["M1 lets $u = x^{2}$", f"M1 $(u - {a*a})(u - {b*b}) = 0$", "M1 square roots", "A1 all four"]), difficulty=2)


@gen("1.2", "Quadratic functions and graphs")
def sketch_info(rng):
    p, q = nz(rng, -6, 6), nz(rng, -6, 6)
    if p == q:
        q = -p if p else 3
    a = pick(rng, [1, -1])
    e = sp.expand(a * (x - p) * (x - q))
    vx = F(p + q, 2)
    vy = a * (vx - p) * (vx - q)
    return Q(f"The curve $C$ has equation $y = {L(e)}$.\n(a) Find the coordinates of the points where $C$ meets the coordinate axes.\n(b) Find the coordinates of the turning point of $C$, stating whether it is a maximum or a minimum.",
             ("(a)", 3, f"$({min(p,q)}, 0)$, $({max(p,q)}, 0)$, $(0, {a*p*q})$", ["M1 factorises or solves $y = 0$", "A1 both $x$-intercepts", "B1 $y$-intercept"]),
             ("(b)", 3, f"$({fr(vx)}, {fr(vy)})$, {'minimum' if a>0 else 'maximum'}", ["M1 symmetry or completing the square for $x$", "A1 coordinates", "B1 nature"]))


# ------------------------------------------------------------------ 1.3
@gen("1.3", "Linear simultaneous equations")
def lin_sim(rng):
    xs, ys = nz(rng, -6, 6), nz(rng, -6, 6)
    while True:
        a, b, c, d = nz(rng, -5, 5), nz(rng, -5, 5), nz(rng, -5, 5), nz(rng, -5, 5)
        if a * d - b * c != 0:
            break
    e1, e2 = a * xs + b * ys, c * xs + d * ys
    return Q(f"Solve the simultaneous equations\n$${term(a, 'x')}{signed(b,'y')} = {e1}$$$${term(c, 'x')}{signed(d,'y')} = {e2}$$".replace("$$$$", "$$\n$$"),
             ("", 3, f"$x = {xs}$, $y = {ys}$", ["M1 eliminates one variable", "A1 one value", "A1 both"]))


@gen("1.3", "Linear and quadratic simultaneous equations", difficulty=2)
def lin_quad(rng):
    # y = m x + c meets y = x^2 + bx + d at integer points
    x1, x2 = nz(rng, -5, 5), nz(rng, -5, 5)
    if x1 == x2:
        x2 = -x1 if x1 else 2
    m, c = nz(rng, -4, 4), rng.randint(-6, 6)
    # x^2 + bx + d - (m x + c) = (x - x1)(x - x2) => b - m = -(x1+x2), d - c = x1 x2
    b, d = m - (x1 + x2), c + x1 * x2
    pts = sorted([(x1, m * x1 + c), (x2, m * x2 + c)])
    return Q(f"Solve the simultaneous equations\n$$y {signed(-m,'x')}{signed(-c)} = 0$$\n$$y = {poly([1, b, d])}$$".replace("y  ", "y "),
             ("", 6, "; ".join(f"$x = {px}, y = {py}$" for px, py in pts),
              ["M1 substitutes linear into quadratic", f"A1 $x^{{2}}{signed(-(x1+x2),'x')}{signed(x1*x2)} = 0$", "M1 solves 3TQ", "A1 both $x$ values", "M1 substitutes back", "A1 both pairs"]), difficulty=2)


@gen("1.3", "Linear inequalities")
def lin_ineq(rng):
    a, b, c, d = rng.randint(2, 7), nz(rng, -9, 9), rng.randint(1, 6), nz(rng, -9, 9)
    if a == c:
        a += 1
    # a x + b > c x + d -> (a - c) x > d - b
    rhs = F(d - b, a - c)
    return Q(f"Find the set of values of $x$ for which ${a}x {signed(b)[1:]} > {c}x {signed(d)[1:]}$.",
             ("", 2, f"$x > {fr(rhs)}$", ["M1 collects terms", f"A1 $x > {fr(rhs)}$"]))


@gen("1.3", "Quadratic inequalities")
def quad_ineq(rng):
    p, q = sorted(rng.sample(range(-7, 8), 2))
    a = pick(rng, [1, 1, 2])
    e = sp.expand(a * (x - p) * (x - q))
    sign = pick(rng, ["<", ">", r"\leq", r"\geq"])
    inside = sign in ("<", r"\leq")
    s2 = "<" if sign == "<" else r"\leq" if sign == r"\leq" else ">" if sign == ">" else r"\geq"
    if inside:
        ans = f"${p} {s2} x {s2} {q}$"
        setn = rf"\{{x : {p} {s2} x {s2} {q}\}}"
    else:
        lo = "<" if sign == ">" else r"\leq"
        ans = f"$x {lo} {p}$ or $x {s2} {q}$"
        setn = rf"\{{x : x {lo} {p}\}} \cup \{{x : x {s2} {q}\}}"
    return Q(f"Find the set of values of $x$ for which ${L(e)} {sign} 0$. Give your answer in set notation.",
             ("", 3, ans + f", i.e. ${setn}$", [f"M1 critical values $x = {p}, {q}$", "M1 chooses " + ("inside" if inside else "outside") + " region", "A1 correct set notation"]))


@gen("1.3", "Inequalities on graphs and regions", difficulty=2)
def region(rng):
    a = rng.randint(1, 3)
    c = rng.randint(2, 9)
    m = nz(rng, -3, 3)
    return Q(f"On a sketch, shade the region $R$ satisfying $y > {poly([a, 0, 0])} {signed(-c)}$ and $y < {poly([m, 0])} {signed(c)}$.\nUse dashed or solid lines appropriately and find the $x$-coordinates of the points where the boundaries meet.".replace("  ", " "),
             ("", 4, f"Boundaries are dashed (strict). Intersections where ${poly([a, -m, -2*c])} = 0$: " + ", ".join(f"$x = {L(s)}$" for s in sp.solve(a * x ** 2 - m * x - 2 * c, x)),
              ["B1 parabola and line sketched", "B1 dashed lines", "M1 solves for intersections", "A1 region R shaded between the curves"]), difficulty=2)


@gen("1.3", "Set notation for solutions", difficulty=2)
def both_ineq(rng):
    p, q = sorted(rng.sample(range(-6, 7), 2))
    e = sp.expand((x - p) * (x - q))
    c = rng.randint(p, q + 3)
    return Q(f"Find the set of values of $x$ for which both $x{signed(-c)} < 0$ and ${L(e)} < 0$. Give your answer in set notation.",
             ("", 4, f"$\\{{x : {p} < x < {min(q, c)}\\}}$" if c > p else "no values (empty set)", ["B1 $x < " + str(c) + "$", f"M1A1 ${p} < x < {q}$", "A1 combined set"]), difficulty=2)


# ------------------------------------------------------------------ 1.4
@gen("1.4", "Gradient and y = mx + c")
def line_two_points(rng):
    while True:
        x1, y1, x2, y2 = (rng.randint(-8, 8) for _ in range(4))
        if x1 != x2 and y1 != y2:
            break
    m = F(y2 - y1, x2 - x1)
    a, b = m.numerator * -1, m.denominator
    c = -(a * x1 + b * y1)
    g = gcd(gcd(abs(a), abs(b)), abs(c)) or 1
    a, b, c = a // g, b // g, c // g
    if a < 0:
        a, b, c = -a, -b, -c
    return Q(f"The points $A({x1}, {y1})$ and $B({x2}, {y2})$ lie on the line $l$. Find an equation for $l$ in the form $ax + by + c = 0$, where $a$, $b$ and $c$ are integers.",
             ("", 4, f"${term(a, 'x')}{signed(b,'y')}{signed(c)} = 0$", [f"M1 gradient $= {fr(m)}$", "M1 uses $y - y_1 = m(x - x_1)$", "A1 any correct form", "A1 integer form"]))


@gen("1.4", "Parallel and perpendicular lines")
def perp_through(rng):
    m = F(nz(rng, -5, 5), pick(rng, [1, 2, 3]))
    c = rng.randint(-8, 8)
    px, py = rng.randint(-6, 6), rng.randint(-6, 6)
    mp = -1 / m
    cp = py - mp * px
    which = pick(rng, ["perpendicular", "parallel"])
    mm = mp if which == "perpendicular" else m
    cc = py - mm * px
    return Q(f"The line $l_1$ has equation $y = {fr(m)}x {signed(c)}$.\nThe line $l_2$ is {which} to $l_1$ and passes through $P({px}, {py})$. Find an equation of $l_2$ in the form $y = mx + c$.".replace("x  ", "x "),
             ("", 3, f"$y = {fr(mm)}x {signed(cc)}$", ["B1 gradient " + f"${fr(mm)}$", "M1 uses the point", f"A1 $y = {fr(mm)}x {signed(cc)}$"]))


@gen("1.4", "Length and midpoint")
def length_mid(rng):
    x1, y1 = rng.randint(-8, 8), rng.randint(-8, 8)
    dx, dy = pick(rng, [(3, 4), (5, 12), (6, 8), (2, 3), (1, 7), (4, 4), (8, 15), (2, 5)])
    x2, y2 = x1 + dx * pick(rng, [1, -1]), y1 + dy * pick(rng, [1, -1])
    d2 = dx * dx + dy * dy
    a, b = sqfree_split(d2)
    return Q(f"$A$ is the point $({x1}, {y1})$ and $B$ is the point $({x2}, {y2})$.\n(a) Find the midpoint of $AB$.\n(b) Find the exact length of $AB$, simplifying your answer.",
             ("(a)", 1, f"$({fr(F(x1+x2,2))}, {fr(F(y1+y2,2))})$", ["B1"]),
             ("(b)", 2, f"${surd(a, b)}$", [f"M1 $\\sqrt{{{dx}^{{2}} + {dy}^{{2}}}}$", f"A1 ${surd(a, b)}$"]))


@gen("1.4", "y - y1 = m(x - x1) and ax + by + c = 0", difficulty=2)
def perp_bisector(rng):
    x1, y1 = rng.randint(-6, 6) * 2, rng.randint(-6, 6) * 2
    x2, y2 = rng.randint(-6, 6) * 2, rng.randint(-6, 6) * 2
    if x1 == x2 or y1 == y2:
        x2, y2 = x1 + 4, y1 + 6
    mx, my = F(x1 + x2, 2), F(y1 + y2, 2)
    m = -F(x2 - x1, y2 - y1)
    a, b = -m.numerator, m.denominator
    c = -(a * mx + b * my)
    g = gcd(gcd(abs(a), abs(b)), abs(int(c))) or 1
    a, b, c = a // g, b // g, int(c) // g
    if a < 0:
        a, b, c = -a, -b, -c
    return Q(f"Find the equation of the perpendicular bisector of the line segment joining $P({x1}, {y1})$ and $Q({x2}, {y2})$. Give your answer in the form $ax + by + c = 0$, where $a$, $b$ and $c$ are integers.",
             ("", 5, f"${term(a, 'x')}{signed(b,'y')}{signed(c)} = 0$", ["B1 midpoint $(" + fr(mx) + ", " + fr(my) + ")$", "M1 gradient of $PQ$", f"M1 perpendicular gradient ${fr(m)}$", "M1 line through midpoint", "A1 integer form"]), difficulty=2)


@gen("1.4", "Modelling with straight lines", difficulty=2)
def model_line(rng):
    c0, rate = rng.randint(20, 60), rng.randint(5, 25)
    t1, t2 = rng.randint(2, 5), rng.randint(8, 14)
    c1, c2 = c0 + rate * t1, c0 + rate * t2
    item = pick(rng, [("A plumber charges a fixed call-out fee plus an hourly rate", "hours", "£"), ("The cost of hiring a van is a fixed fee plus a charge per day", "days", "£")])
    return Q(f"{item[0]}. A job lasting {t1} {item[1]} costs {item[2]}{c1} and a job lasting {t2} {item[1]} costs {item[2]}{c2}. The cost $C$ is modelled as a linear function of the time $t$.\n(a) Find an equation linking $C$ and $t$.\n(b) Interpret the gradient and the intercept in context.\n(c) State a limitation of the model.",
             ("(a)", 3, f"$C = {rate}t + {c0}$", ["M1 gradient $= " + str(rate) + "$", "M1 substitutes a point", f"A1 $C = {rate}t + {c0}$"]),
             ("(b)", 2, f"{item[2]}{rate} per {item[1][:-1]}; fixed charge {item[2]}{c0}", ["B1 gradient", "B1 intercept"]),
             ("(c)", 1, "e.g. charges may be per part-hour / discounts for long jobs", ["B1 sensible limitation"]), difficulty=2)


# ------------------------------------------------------------------ 1.5
@gen("1.5", "Completing the square to find centre and radius")
def circle_centre(rng):
    a, b = nz(rng, -7, 7), nz(rng, -7, 7)
    r2 = pick(rng, [4, 9, 16, 25, 36, 49, 8, 12, 18, 20, 45, 50])
    c = a * a + b * b - r2
    ra, rb = sqfree_split(r2)
    return Q(f"The circle $C$ has equation $x^{{2}} + y^{{2}} {signed(-2*a,'x')} {signed(-2*b,'y')} {signed(c)} = 0$. Find the coordinates of the centre of $C$ and the exact radius of $C$.".replace("  ", " "),
             ("", 4, f"centre $({a}, {b})$, radius ${surd(ra, rb)}$", ["M1 completes the square in $x$ and $y$", "A1 centre", "M1 $r^{2} = " + f"{a*a}+{b*b}-({c})" + "$", f"A1 $r = {surd(ra, rb)}$"]))


@gen("1.5", "Equation of a circle")
def circle_diameter(rng):
    while True:
        x1, y1, x2, y2 = (rng.randint(-8, 8) for _ in range(4))
        if (x1 + x2) % 2 == 0 and (y1 + y2) % 2 == 0 and (x1, y1) != (x2, y2):
            break
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    r2 = (x1 - cx) ** 2 + (y1 - cy) ** 2
    return Q(f"The points $A({x1}, {y1})$ and $B({x2}, {y2})$ are the ends of a diameter of the circle $C$. Find an equation for $C$.",
             ("", 4, f"$(x {signed(-cx)[1:] if cx else ''})^{{2}} + (y {signed(-cy)[1:] if cy else ''})^{{2}} = {r2}$".replace("(x )", "x").replace("(y )", "y"),
              [f"M1A1 centre $({cx}, {cy})$", f"M1 $r^{{2}} = {r2}$", "A1 equation"]))


@gen("1.5", "Tangents and normals to circles", difficulty=2)
def circle_tangent(rng):
    a, b = rng.randint(-5, 5), rng.randint(-5, 5)
    dx, dy = pick(rng, [(3, 4), (4, 3), (5, 12), (12, 5), (1, 2), (2, 1), (1, 3), (3, 1), (2, 2)])
    dx *= pick(rng, [1, -1]); dy *= pick(rng, [1, -1])
    px, py = a + dx, b + dy
    r2 = dx * dx + dy * dy
    # tangent perpendicular to radius gradient dy/dx => m = -dx/dy
    A, B, C = dx, dy, -(dx * px + dy * py)
    g = gcd(gcd(abs(A), abs(B)), abs(C)) or 1
    A, B, C = A // g, B // g, C // g
    if A < 0:
        A, B, C = -A, -B, -C
    return Q(f"The circle $C$ has centre $({a}, {b})$ and passes through the point $P({px}, {py})$.\n(a) Find an equation for $C$.\n(b) Find an equation of the tangent to $C$ at $P$, giving your answer in the form $ax + by + c = 0$.",
             ("(a)", 2, f"$(x {signed(-a)[1:] if a else ''})^{{2}} + (y {signed(-b)[1:] if b else ''})^{{2}} = {r2}$".replace("(x )", "x").replace("(y )", "y"), ["M1 radius$^{2}$ by Pythagoras", "A1"]),
             ("(b)", 4, f"${term(A, 'x')}{signed(B,'y')}{signed(C)} = 0$", [f"M1 gradient of radius ${fr(F(dy, dx))}$", f"M1 tangent gradient ${fr(F(-dx, dy))}$", "M1 line through $P$", "A1"]), difficulty=2)


@gen("1.5", "Intersections of lines and circles", difficulty=2)
def line_circle_k(rng):
    a, b = rng.randint(-4, 4), rng.randint(-4, 4)
    r2 = pick(rng, [5, 10, 8, 13, 20, 18])
    m = nz(rng, -3, 3)
    # y = m x + k tangent: distance from (a,b) to line = r -> |m a - b + k| / sqrt(m^2+1) = r
    s = sp.sqrt(r2 * (m * m + 1))
    k1, k2 = sorted([b - m * a - s, b - m * a + s], key=float)
    return Q(f"The circle $C$ has equation $(x {signed(-a)[1:] if a else ''})^{{2}} + (y {signed(-b)[1:] if b else ''})^{{2}} = {r2}$ and the line $l$ has equation $y = {poly([m, 0])} + k$, where $k$ is a constant.\nGiven that $l$ is a tangent to $C$, find the exact possible values of $k$.".replace("(x )", "x").replace("(y )", "y"),
             ("", 5, f"$k = {L(sp.simplify(k1))}$ or $k = {L(sp.simplify(k2))}$", ["M1 substitutes the line into the circle", "A1 correct 3TQ in $x$", "M1 uses $b^{2} - 4ac = 0$", "M1 solves for $k$", "A1 both values"]), difficulty=2)


@gen("1.5", "Chords and perpendicular bisectors", difficulty=3)
def circle_three_points(rng):
    a, b = rng.randint(-4, 4), rng.randint(-4, 4)
    pts = pick(rng, [[(5, 0), (-5, 0), (3, 4)], [(5, 0), (0, 5), (-3, -4)], [(3, 4), (-4, 3), (4, -3)], [(0, 5), (4, 3), (-5, 0)]])
    P = [(a + u, b + v) for u, v in pts]
    return Q(f"The points $P{P[0]}$, $Q{P[1]}$ and $R{P[2]}$ lie on a circle $C$.\n(a) Find the equations of the perpendicular bisectors of $PQ$ and $QR$.\n(b) Hence find the centre and radius of $C$.".replace(", ", ", "),
             ("(a)", 4, "two lines through the midpoints, perpendicular to $PQ$ and $QR$", ["M1A1 first bisector", "M1A1 second bisector"]),
             ("(b)", 3, f"centre $({a}, {b})$, radius $5$", ["M1 solves simultaneously", "A1 centre", "B1 radius"]), difficulty=3)


@gen("1.5", "Circle theorems in coordinate geometry", difficulty=2)
def semicircle(rng):
    a, b = rng.randint(-3, 3), rng.randint(-3, 3)
    P, Q2, R = (a - 5, b), (a + 5, b), (a + 3, b + 4)
    m1 = F(R[1] - P[1], R[0] - P[0]); m2 = F(R[1] - Q2[1], R[0] - Q2[0])
    return Q(f"The points $A{P}$, $B{Q2}$ and $C{R}$ lie on a circle.\n(a) Show that $AC$ is perpendicular to $BC$.\n(b) Hence explain why $AB$ is a diameter and find an equation of the circle.",
             ("(a)", 3, f"gradients ${fr(m1)}$ and ${fr(m2)}$; product $-1$", ["M1 gradient of $AC$", "M1 gradient of $BC$", "A1 product $= -1$ so perpendicular"]),
             ("(b)", 3, f"angle in a semicircle is $90^\\circ$; $(x {signed(-a)[1:] if a else ''})^{{2}} + (y {signed(-b)[1:] if b else ''})^{{2}} = 25$".replace("(x )", "x").replace("(y )", "y"),
              ["B1 angle in semicircle", "M1 centre = midpoint of $AB$", "A1 equation"]), difficulty=2)
