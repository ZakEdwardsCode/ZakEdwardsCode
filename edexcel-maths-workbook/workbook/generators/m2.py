"""Module 2: Functions, expansions & advanced algebra (2.1 - 2.4)."""
import math
from fractions import Fraction as F

import sympy as sp

from ..core import L, M, Q, asc, dp, fr, gen, nz, pick, poly, sf, signed, term, x

PROOFS = [
    ("Proof by deduction", "Prove that the sum of any three consecutive integers is divisible by 3.",
     "Let the integers be $n$, $n+1$, $n+2$. Sum $= 3n + 3 = 3(n+1)$, a multiple of 3.", 3),
    ("Proof by deduction", "Prove that the difference between the squares of two consecutive odd numbers is a multiple of 8.",
     "$(2n+1)^{2} - (2n-1)^{2} = 8n$, which is a multiple of 8.", 3),
    ("Proof by deduction", "Prove that $x^{2} - 6x + 11 > 0$ for all real values of $x$.",
     "$x^{2} - 6x + 11 = (x-3)^{2} + 2$; $(x-3)^{2} \\geq 0$ so the expression $\\geq 2 > 0$.", 3),
    ("Proof by deduction", "Prove that $(n + 3)^{2} - (n - 3)^{2}$ is a multiple of 12 for all integers $n$.",
     "Expands to $12n$, so it is a multiple of 12.", 2),
    ("Proof by exhaustion", "Prove that for all integers $n$ with $1 \\leq n \\leq 6$, $n^{2} + 2$ is not divisible by 4.",
     "Check $n = 1..6$: $3, 6, 11, 18, 27, 38$; none divisible by 4.", 2),
    ("Proof by exhaustion", "Prove that the square of any integer is either a multiple of 3 or one more than a multiple of 3.",
     "Cases $n = 3k$: $9k^{2}$; $n = 3k \\pm 1$: $9k^{2} \\pm 6k + 1 = 3(3k^{2} \\pm 2k) + 1$.", 4),
    ("Proof by exhaustion", "Prove that $n^{3} - n$ is even for all positive integers $n$.",
     "$n^{3} - n = (n-1)n(n+1)$; or cases $n$ even/odd: even $\\times$ anything is even.", 3),
    ("Proof by contradiction", "Prove by contradiction that $\\sqrt{2}$ is irrational.",
     "Assume $\\sqrt{2} = \\frac{a}{b}$ in lowest terms; $a^{2} = 2b^{2}$ so $a$ even, $a = 2c$; then $b^{2} = 2c^{2}$ so $b$ even; contradiction with lowest terms.", 5),
    ("Proof by contradiction", "Prove by contradiction that there are infinitely many prime numbers.",
     "Assume finitely many $p_1,\\ldots,p_n$; $N = p_1 p_2 \\cdots p_n + 1$ leaves remainder 1 on division by each; so $N$ is prime or has a prime factor not in the list; contradiction.", 5),
    ("Proof by contradiction", "Prove by contradiction that if $n^{2}$ is even then $n$ is even.",
     "Assume $n$ odd, $n = 2k+1$; $n^{2} = 4k^{2} + 4k + 1 = 2(2k^{2}+2k) + 1$ is odd; contradiction.", 4),
    ("Proof by contradiction", "Prove by contradiction that there are no positive integer solutions to $x^{2} - y^{2} = 1$.",
     "$(x-y)(x+y) = 1$ forces $x - y = x + y = 1$, so $y = 0$, not positive; contradiction.", 4),
    ("Disproof by counter-example", "Show that the statement '$n^{2} + n + 41$ is prime for every positive integer $n$' is false.",
     "$n = 40$: $1681 = 41^{2}$ (or $n = 41$).", 2),
    ("Disproof by counter-example", "Disprove: 'if $a > b$ then $a^{2} > b^{2}$ for all real $a, b$'.",
     "$a = 1$, $b = -2$: $a > b$ but $1 < 4$.", 2),
    ("Disproof by counter-example", "Disprove: '$2^{n} - 1$ is prime for every prime $n$'.",
     "$n = 11$: $2047 = 23 \\times 89$.", 2),
]


def _proof_gen(skill):
    def fn(rng):
        _, stmt, ans, marks = pick(rng, [p for p in PROOFS if p[0] == skill])
        return Q(stmt, ("", marks, ans, ["B1 sets up correctly (algebraic form / cases / assumption)", "M1 valid algebra or reasoning", "A1 conclusion stated in words"]))
    fn.__name__ = "proof_" + skill.split()[-1].replace("-", "_")
    return gen("2.1", skill, difficulty=2 if "contradiction" in skill else 1)(fn)


for _skill in ("Proof by deduction", "Proof by exhaustion", "Proof by contradiction", "Disproof by counter-example"):
    _proof_gen(_skill)


@gen("2.1", "Polynomial division")
def poly_divide(rng):
    a, b, c = nz(rng, -6, 6), nz(rng, -6, 6), nz(rng, -6, 6)
    lead = pick(rng, [1, 2, 3])
    f = sp.expand((lead * x + a) * (x + b) * (x + c))
    q = sp.expand((lead * x + a) * (x + c))
    return Q(f"Divide ${L(f)}$ by $(x {signed(b)[1:]})$ and hence factorise ${L(f)}$ completely.",
             ("", 4, f"quotient ${L(q)}$; ${L(sp.factor(f))}$", ["M1 long division to obtain $" + term(lead) + "x^{2} + ...$", "A1 quotient", "M1 factorises quadratic", "A1 full factorisation"]))


@gen("2.1", "Factor theorem", difficulty=2)
def factor_theorem(rng):
    r1, r2, r3 = nz(rng, -4, 4), nz(rng, -5, 5), nz(rng, -5, 5)
    lead = pick(rng, [1, 2])
    f = sp.expand(lead * (x - r1) * (x - r2) * (x - r3))
    co = sp.Poly(f, x).all_coeffs()
    # hide the x coefficient as p
    p = co[2]
    shown = f"{poly([co[0], co[1]]).replace('x','x^{3}',1).replace('x^{3}^{3}','x^{3}') if False else L(co[0]*x**3 + co[1]*x**2)} + px {signed(co[3])}"
    return Q(f"$f(x) = {shown}$, where $p$ is a constant.\nGiven that $(x {signed(-r1)[1:]})$ is a factor of $f(x)$,\n(a) find the value of $p$,\n(b) hence factorise $f(x)$ completely.",
             ("(a)", 2, f"$p = {p}$", [f"M1 sets $f({r1}) = 0$", f"A1 $p = {p}$"]),
             ("(b)", 4, M(sp.factor(f)), ["M1 divides by the factor", "A1 quadratic factor", "M1 factorises", "A1"]), difficulty=2)


@gen("2.1", "Factor theorem")
def remainder_check(rng):
    r = nz(rng, -4, 4)
    co = [rng.randint(1, 3), nz(rng, -6, 6), nz(rng, -9, 9), rng.randint(-12, 12)]
    f = sum(c * x ** (3 - i) for i, c in enumerate(co))
    val = f.subs(x, r)
    return Q(f"$f(x) = {L(f)}$.\nUse the factor theorem to determine whether $(x {signed(-r)[1:]})$ is a factor of $f(x)$.",
             ("", 2, f"$f({r}) = {val}$, so {'it is' if val == 0 else 'it is not'} a factor", [f"M1 evaluates $f({r})$", "A1 value and conclusion"]))


@gen("2.1", "Partial fractions")
def partial_linear(rng):
    a, b = nz(rng, -5, 5), nz(rng, -5, 5)
    if a == b:
        b = a + 1
    A, B = nz(rng, -6, 6), nz(rng, -6, 6)
    num = sp.expand(A * (x + b) + B * (x + a))
    den = sp.expand((x + a) * (x + b))
    return Q(f"Express $\\frac{{{L(num)}}}{{{L(den)}}}$ in partial fractions.",
             ("", 3, f"$\\frac{{{A}}}{{{L(x+a)}}} {'+' if B>0 else '-'} \\frac{{{abs(B)}}}{{{L(x+b)}}}$", ["M1 correct form and factorised denominator", "M1 substitutes or compares coefficients", "A1 both constants"]))


@gen("2.1", "Partial fractions with repeated factors", difficulty=2)
def partial_repeated(rng):
    a, b = nz(rng, -4, 4), nz(rng, -4, 4)
    if a == b:
        b = a + 2
    A, B, C = nz(rng, -5, 5), nz(rng, -5, 5), nz(rng, -5, 5)
    num = sp.expand(A * (x + a) * (x + b) + B * (x + b) + C * (x + a) ** 2)
    den = (x + a) ** 2 * (x + b)
    return Q(f"Given that $\\frac{{{L(num)}}}{{{L(den)}}} \\equiv \\frac{{A}}{{{L(x+a)}}} + \\frac{{B}}{{({L(x+a)})^{{2}}}} + \\frac{{C}}{{{L(x+b)}}}$, find the values of $A$, $B$ and $C$.",
             ("", 4, f"$A = {A}$, $B = {B}$, $C = {C}$", ["M1 multiplies through by the denominator", f"B1 $B = {B}$ (substitute $x = {-a}$)", f"B1 $C = {C}$ (substitute $x = {-b}$)", "A1 $A$ by comparing $x^{2}$ coefficients"]), difficulty=2)


@gen("2.1", "Algebraic fractions")
def simplify_fraction(rng):
    a, b, c = nz(rng, -6, 6), nz(rng, -6, 6), nz(rng, -6, 6)
    if b == c:
        c = b + 1
    k = pick(rng, [1, 2, 3])
    num = sp.expand(k * (x + a) * (x + b))
    den = sp.expand((x + a) * (x + c))
    return Q(f"Simplify fully $\\frac{{{L(num)}}}{{{L(den)}}}$.", ("", 3, M(sp.cancel(num / den)), ["M1 factorises numerator", "M1 factorises denominator", "A1 cancelled form"]))


# ------------------------------------------------------------------ 2.2
@gen("2.2", "Composite functions")
def composite(rng):
    a, b = nz(rng, -5, 5), rng.randint(-6, 6)
    c, d = rng.randint(1, 4), rng.randint(-5, 5)
    f = a * x + b
    g = c * x ** 2 + d
    v = rng.randint(-3, 3)
    fg = sp.expand(f.subs(x, g))
    return Q(f"The functions $f$ and $g$ are defined by $f(x) = {L(f)}$, $x \\in \\mathbb{{R}}$ and $g(x) = {L(g)}$, $x \\in \\mathbb{{R}}$.\n(a) Find $fg({v})$.\n(b) Find $gf(x)$ in its simplest form.\n(c) Find an expression for $f^{{-1}}(x)$.",
             ("(a)", 2, f"${fg.subs(x, v)}$", [f"M1 $g({v}) = {g.subs(x, v)}$", "A1"]),
             ("(b)", 2, f"${L(sp.expand(g.subs(x, f)))}$", ["M1 substitutes $f$ into $g$", "A1"]),
             ("(c)", 2, f"$f^{{-1}}(x) = {L(sp.together((x - b) / a))}$", ["M1 rearranges $y = " + L(f) + "$", "A1"]))


@gen("2.2", "Inverse functions", difficulty=2)
def inverse_rational(rng):
    while True:
        a, b, c, d = nz(rng, -5, 5), rng.randint(-6, 6), rng.randint(1, 3), nz(rng, -5, 5)
        if a * d - b * c != 0:
            break
    f = (a * x + b) / (c * x + d)
    inv = sp.simplify((-d * x + b) / (c * x - a))
    return Q(f"$f(x) = \\frac{{{L(a*x+b)}}}{{{L(c*x+d)}}}$, $x \\in \\mathbb{{R}}$, $x \\neq {fr(F(-d, c))}$.\n(a) Find $f^{{-1}}(x)$.\n(b) State the domain of $f^{{-1}}$.",
             ("(a)", 3, f"$f^{{-1}}(x) = \\frac{{{L(-d*x+b)}}}{{{L(c*x-a)}}}$", ["M1 swaps $x$ and $y$ or rearranges", "M1 collects $y$ terms", "A1"]),
             ("(b)", 1, f"$x \\in \\mathbb{{R}}, x \\neq {fr(F(a, c))}$", ["B1 range of $f$ is all reals except " + f"${fr(F(a, c))}$"]), difficulty=2)


@gen("2.2", "Mappings and functions, domain and range")
def range_quadratic(rng):
    p, q = nz(rng, -5, 5), rng.randint(-9, 9)
    lo = rng.randint(-6, p - 1) if rng.random() < 0.5 else None
    f = sp.expand((x - p) ** 2 + q)
    if lo is None:
        return Q(f"The function $f$ is defined by $f(x) = {L(f)}$, $x \\in \\mathbb{{R}}$. Find the range of $f$, and explain why $f$ does not have an inverse.",
                 ("", 3, f"$f(x) \\geq {q}$; $f$ is many-to-one", ["M1 completes the square", f"A1 $f(x) \\geq {q}$", "B1 many-to-one"]))
    return Q(f"The function $f$ is defined by $f(x) = {L(f)}$, $x \\geq {p}$. Find the range of $f$ and the domain of $f^{{-1}}$.",
             ("", 3, f"$f(x) \\geq {q}$; domain of $f^{{-1}}$ is $x \\geq {q}$", ["M1 completes the square", "A1 range", "B1ft domain of inverse = range of $f$"]))


@gen("2.2", "Solving modulus equations and inequalities", difficulty=2)
def modulus_eq(rng):
    a, b = rng.randint(1, 4), nz(rng, -8, 8)
    c, d = pick(rng, [1, -1, 2, -2, 3]), rng.randint(-6, 6)
    sols = []
    for s in (1, -1):
        # s(a x + b) = c x + d
        if s * a - c == 0:
            continue
        xv = F(d - s * b, s * a - c)
        if c * xv + d >= 0:
            sols.append(xv)
    sols = sorted(set(sols))
    ans = ", ".join(f"$x = {fr(v)}$" for v in sols) or "no solutions"
    return Q(f"Solve $|{L(a*x+b)}| = {L(c*x+d)}$.",
             ("", 4, ans, ["M1 solves $" + L(a * x + b) + " = " + L(c * x + d) + "$", "M1 solves $-(" + L(a * x + b) + ") = " + L(c * x + d) + "$", "M1 checks the RHS is non-negative / rejects invalid roots", "A1 " + ans]), difficulty=2)


@gen("2.2", "Solving modulus equations and inequalities")
def modulus_ineq(rng):
    a, b, c = rng.randint(1, 4), nz(rng, -9, 9), rng.randint(1, 9)
    lo, hi = F(-c - b, a), F(c - b, a)
    sign = pick(rng, ["<", ">"])
    ans = f"${fr(lo)} < x < {fr(hi)}$" if sign == "<" else f"$x < {fr(lo)}$ or $x > {fr(hi)}$"
    return Q(f"Solve $|{L(a*x+b)}| {sign} {c}$.", ("", 3, ans, [f"M1 $-{c} < {L(a*x+b)} < {c}$ or equivalent critical values", "A1 critical values", "A1 correct region"]))


@gen("2.2", "Transformations y = af(x), f(x)+a, f(x+a), f(ax)")
def transform_point(rng):
    px, py = rng.randint(-6, 6), rng.randint(-6, 6)
    kind = pick(rng, ["af", "f+a", "fx+a", "fax", "-f", "f-x"])
    a = pick(rng, [2, 3, -2, F(1, 2), 4])
    if kind == "af":
        e, img = f"y = {fr(a)}f(x)", (px, a * py)
    elif kind == "f+a":
        e, img = f"y = f(x){signed(a)}", (px, py + a)
    elif kind == "fx+a":
        e, img = f"y = f(x{signed(a)})", (px - a, py)
    elif kind == "fax":
        e, img = f"y = f({fr(a)}x)", (F(px) / a, py)
    elif kind == "-f":
        e, img = "y = -f(x)", (px, -py)
    else:
        e, img = "y = f(-x)", (-px, py)
    return Q(f"The curve $y = f(x)$ has a maximum point at $({px}, {py})$. Write down the coordinates of the corresponding point on the curve with equation ${e}$, and describe the transformation.",
             ("", 2, f"$({fr(img[0])}, {fr(img[1])})$", ["B1 coordinates", "B1 transformation described fully"]))


@gen("2.2", "Modulus graphs y = |f(x)| and y = f(|x|)", difficulty=2)
def modulus_graph(rng):
    p, q = sorted(rng.sample(range(-5, 6), 2))
    f = sp.expand((x - p) * (x - q))
    vx = F(p + q, 2)
    vy = (vx - p) * (vx - q)
    return Q(f"Given $f(x) = {L(f)}$,\n(a) sketch $y = |f(x)|$, stating the coordinates of any points where the graph meets the axes and the coordinates of its maximum turning point,\n(b) sketch $y = f(|x|)$, stating where it meets the axes.",
             ("(a)", 4, f"touches $x$-axis at ${p}$ and ${q}$; $y$-intercept ${abs(p*q)}$; maximum at $({fr(vx)}, {fr(-vy)})$", ["B1 shape (reflected part above axis)", "B1 $x$-intercepts", "B1 $y$-intercept", "B1 turning point"]),
             ("(b)", 3, "symmetric in the $y$-axis: reflect the part for $x \\geq 0$; $x$-intercepts " + ", ".join(f"${v}$" for v in sorted({abs(p), -abs(p), abs(q), -abs(q)}) if (v >= 0 and v in (p, q)) or (v < 0 and -v in (p, q))) + (" none" if max(p, q) < 0 else "") + f"; $y$-intercept ${p*q}$",
              ["B1 symmetry in $y$-axis", "B1 intercepts", "B1 shape"]), difficulty=2)


@gen("2.2", "Combining transformations", difficulty=2)
def combine_transform(rng):
    a, b, c = pick(rng, [2, 3, -1, -2]), nz(rng, -4, 4), nz(rng, -5, 5)
    return Q(f"The curve $y = x^{{2}}$ is transformed onto $y = {a}(x {signed(b)[1:]})^{{2}} {signed(c)}$. Describe fully a sequence of transformations that maps the first curve onto the second.",
             ("", 3, f"translation by $\\left({-b}, 0\\right)$; vertical stretch scale factor ${a}$" + (" (including reflection in the $x$-axis)" if a < 0 else "") + f"; translation by $\\left(0, {c}\\right)$",
              ["B1 horizontal translation", "B1 stretch (and reflection)", "B1 vertical translation in a valid order"]), difficulty=2)


# ------------------------------------------------------------------ 2.3
@gen("2.3", "(a + b)^n for positive integer n")
def binom_int(rng):
    a, b, nn = pick(rng, [1, 2, 3]), nz(rng, -4, 4), rng.randint(4, 8)
    e = sp.expand((a + b * x) ** nn)
    terms = [e.coeff(x, i) for i in range(4)]
    s = " + ".join(f"{L(c * x**i)}" for i, c in enumerate(terms)).replace("+ -", "- ")
    return Q(f"Find the first 4 terms, in ascending powers of $x$, of the binomial expansion of $({a} {signed(b,'x')[1:]})^{{{nn}}}$, giving each term in its simplest form.",
             ("", 4, f"${s}$", ["B1 first term", "M1 correct binomial coefficients with powers of " + f"${b}x$", "A1 two terms correct", "A1 all correct"]))


@gen("2.3", "(a + b)^n for positive integer n", difficulty=2)
def binom_coeff_k(rng):
    nn, r = rng.randint(5, 9), rng.randint(2, 3)
    kk = nz(rng, -4, 4)
    target = math.comb(nn, r) * kk ** r
    return Q(f"In the binomial expansion of $(1 + kx)^{{{nn}}}$, where $k$ is a constant, the coefficient of $x^{{{r}}}$ is ${target}$. Find the possible value{'s' if r % 2 == 0 else ''} of $k$.",
             ("", 3, f"$k = {'\\pm ' if r % 2 == 0 else ''}{abs(kk) if r % 2 == 0 else kk}$", [f"M1 $^{{{nn}}}C_{{{r}}}k^{{{r}}} = {target}$", f"A1 $k^{{{r}}} = {kk**r}$", "A1"]), difficulty=2)


@gen("2.3", "(1 + x)^n for rational n", difficulty=2)
def binom_rational(rng):
    nn = pick(rng, [F(1, 2), F(-1, 2), F(-1), F(-2), F(1, 3), F(-1, 3), F(3, 2), F(-3, 2)])
    b = pick(rng, [2, 3, 4, -2, -3, F(1, 2)])
    e = sp.series((1 + sp.Rational(b.numerator, b.denominator) * x if isinstance(b, F) else 1 + b * x) ** sp.Rational(nn.numerator, nn.denominator), x, 0, 4).removeO()
    terms = " + ".join(L(e.coeff(x, i) * x ** i) for i in range(4)).replace("+ -", "- ")
    val = F(1) / abs(F(b))
    return Q(f"(a) Find the binomial expansion of $(1 {signed(b,'x')})^{{{fr(nn)}}}$, in ascending powers of $x$, up to and including the term in $x^{{3}}$.\n(b) State the range of values of $x$ for which the expansion is valid.",
             ("(a)", 4, f"${terms}$", ["M1 correct structure $1 + nx + \\frac{n(n-1)}{2!}x^{2} + ...$", "B1 $1 + ...x$", "A1 $x^{2}$ term", "A1 $x^{3}$ term"]),
             ("(b)", 1, f"$|x| < {fr(val)}$", ["B1"]), difficulty=2)


@gen("2.3", "(a + bx)^n for rational n", difficulty=3)
def binom_a_bx(rng):
    a2 = pick(rng, [4, 9, 16, 25])
    nn = pick(rng, [F(1, 2), F(-1, 2), F(-3, 2)])
    b = nz(rng, -3, 3)
    expr = (a2 + b * x) ** sp.Rational(nn.numerator, nn.denominator)
    e = sp.series(expr, x, 0, 3).removeO()
    terms = " + ".join(L(sp.nsimplify(e.coeff(x, i)) * x ** i) for i in range(3)).replace("+ -", "- ")
    return Q(f"Find the first three terms, in ascending powers of $x$, of the binomial expansion of $({a2} {signed(b,'x')[1:]})^{{{fr(nn)}}}$, giving each coefficient as a simplified fraction, and state the range of validity.",
             ("", 5, f"${terms}$, valid for $|x| < {fr(F(a2, abs(b)))}$", [f"M1 takes out ${a2}^{{{fr(nn)}}}$", "M1 expands $(1 + kx)^{n}$", "A1 two terms", "A1 three terms", "B1 validity"]), difficulty=3)


@gen("2.3", "Range of validity")
def validity(rng):
    a, b = rng.randint(1, 9), nz(rng, -6, 6)
    nn = pick(rng, ["-2", r"\frac{1}{2}", r"-\frac{1}{3}", "-1"])
    return Q(f"State the set of values of $x$ for which the binomial expansion of $({a} {signed(b,'x')[1:]})^{{{nn}}}$ is valid.",
             ("", 1, f"$|x| < {fr(F(a, abs(b)))}$", ["B1"]))


@gen("2.3", "Approximations using expansions", difficulty=2)
def binom_estimate(rng):
    # (1 - 2x)^(1/2) with x = 0.01 etc to estimate sqrt
    xv = pick(rng, [F(1, 100), F(1, 50), F(1, 20), F(1, 10)])
    k = pick(rng, [2, 4, -2])
    e = sp.series(sp.sqrt(1 + k * x), x, 0, 3).removeO()
    approx = e.subs(x, sp.Rational(xv.numerator, xv.denominator))
    inside = 1 + k * xv
    return Q(f"(a) Expand $\\sqrt{{1 {signed(k,'x')}}}$ in ascending powers of $x$ up to and including the term in $x^{{2}}$.\n(b) By substituting $x = {fr(xv)}$, find an approximation for $\\sqrt{{{fr(inside)}}}$, giving your answer to 5 decimal places.",
             ("(a)", 3, f"${asc(e)}$", ["M1 binomial with $n = \\frac{1}{2}$", "A1", "A1"]),
             ("(b)", 2, f"${float(approx):.5f}$", ["M1 substitutes", "A1"]), difficulty=2)


@gen("2.3", "Using partial fractions with expansions", difficulty=3)
def binom_partial(rng):
    a, b = rng.randint(1, 3), rng.randint(1, 3)
    A, B = nz(rng, -4, 4), nz(rng, -4, 4)
    f = A / (1 + a * x) + B / (1 - b * x)
    num = sp.expand(A * (1 - b * x) + B * (1 + a * x))
    den = sp.expand((1 + a * x) * (1 - b * x))
    e = sp.series(f, x, 0, 3).removeO()
    return Q(f"$f(x) = \\frac{{{L(num)}}}{{{L(den)}}}$.\n(a) Express $f(x)$ in partial fractions.\n(b) Hence find the series expansion of $f(x)$ in ascending powers of $x$ up to and including the term in $x^{{2}}$, and state the range of validity.",
             ("(a)", 3, f"$\\frac{{{A}}}{{1 + {a if a>1 else ''}x}} + \\frac{{{B}}}{{1 - {b if b>1 else ''}x}}$".replace("+ \\frac{-", "- \\frac{"), ["M1 form", "A1 one constant", "A1 both"]),
             ("(b)", 4, f"${asc(e)}$, $|x| < {fr(F(1, max(a, b)))}$", ["M1 expands $(1+ax)^{-1}$", "M1 expands $(1-bx)^{-1}$", "A1 combined", "B1 validity"]), difficulty=3)


# ------------------------------------------------------------------ 2.4
@gen("2.4", "Solving exponential equations")
def solve_exp(rng):
    a, b = pick(rng, [2, 3, 5, 7]), rng.randint(5, 90)
    c = rng.randint(1, 4)
    v = (math.log(b) / math.log(a) - c) if rng.random() < 0.5 else None
    if v is None:
        return Q(f"Solve ${a}^{{x}} = {b}$, giving your answer to 3 significant figures.", ("", 2, f"$x = {sf(math.log(b)/math.log(a))}$", ["M1 $x = \\frac{\\ln " + str(b) + "}{\\ln " + str(a) + "}$", "A1"]))
    return Q(f"Solve ${a}^{{x + {c}}} = {b}$, giving your answer to 3 significant figures.", ("", 2, f"$x = {sf(v)}$", ["M1 takes logs of both sides", "A1"]))


@gen("2.4", "Solving exponential equations", difficulty=2)
def exp_two_bases(rng):
    a, b = pick(rng, [(2, 3), (3, 5), (2, 5), (5, 7), (3, 7)])
    p, q = rng.randint(1, 3), rng.randint(1, 3)
    # a^(x+p) = b^(x-q) -> (x+p) ln a = (x - q) ln b -> x = -(p ln a + q ln b)/(ln a - ln b)
    v = -(p * math.log(a) + q * math.log(b)) / (math.log(a) - math.log(b))
    return Q(f"Solve ${a}^{{x+{p}}} = {b}^{{x-{q}}}$, giving your answer to 3 significant figures.",
             ("", 4, f"$x = {sf(v)}$", ["M1 takes logs", "M1 expands and collects $x$ terms", "M1 makes $x$ the subject", "A1"]), difficulty=2)


@gen("2.4", "Laws of logarithms", difficulty=2)
def log_equation(rng):
    base = pick(rng, [2, 3])
    r = rng.randint(1, 6)
    a = rng.randint(1, 6)
    kk = r * (r + a)
    p = round(math.log(kk, base))
    if base ** p != kk:
        # use form log(x) + log(x + a) = log(kk)
        return Q(f"Solve $\\log_{{{base}}} x + \\log_{{{base}}}(x + {a}) = \\log_{{{base}}} {kk}$.",
                 ("", 4, f"$x = {r}$ (reject $x = {-r-a}$)", ["M1 $\\log(x(x+" + str(a) + "))$", "M1 forms quadratic", "A1 solves", "A1 rejects negative root"]), difficulty=2)
    return Q(f"Solve $\\log_{{{base}}} x + \\log_{{{base}}}(x + {a}) = {p}$.",
             ("", 4, f"$x = {r}$ (reject $x = {-r-a}$)", ["M1 combines logs", f"M1 $x(x + {a}) = {base}^{{{p}}}$", "A1 solves", "A1 rejects negative root"]), difficulty=2)


@gen("2.4", "Laws of logarithms")
def log_express(rng):
    a, b, c = rng.randint(2, 4), rng.randint(1, 3), pick(rng, [2, 3, 5])
    return Q(f"Given that $p = \\log_{{{c}}} a$ and $q = \\log_{{{c}}} b$, express $\\log_{{{c}}}\\left(\\frac{{a^{{{a}}}\\sqrt{{b}}}}{{{c}b^{{{b}}}}}\\right)$ in terms of $p$ and $q$.",
             ("", 3, f"${a}p{signed(F(1,2)-b,'q')} - 1$", ["M1 uses addition/subtraction law", "M1 uses power law", "A1"]))


@gen("2.4", "e^x and ln x", difficulty=2)
def e_hidden_quad(rng):
    r1, r2 = rng.randint(1, 6), rng.randint(1, 6)
    if r1 == r2:
        r2 += 1
    s, p = r1 + r2, r1 * r2
    sols = [f"$x = \\ln {r}$" if r != 1 else "$x = 0$" for r in (r1, r2)]
    return Q(f"Solve $e^{{2x}} - {s}e^{{x}} + {p} = 0$, giving your answers as exact values.",
             ("", 4, ", ".join(sols), ["M1 lets $u = e^{x}$", f"M1 $(u - {r1})(u - {r2}) = 0$", "M1 takes $\\ln$", "A1 both exact"]), difficulty=2)


@gen("2.4", "e^x and ln x")
def ln_solve(rng):
    a, b, c = rng.randint(2, 5), rng.randint(1, 9), rng.randint(1, 4)
    return Q(f"Solve $\\ln({a}x - {b}) = {c}$, giving your answer in exact form.",
             ("", 2, f"$x = \\frac{{e^{{{c}}} + {b}}}{{{a}}}$", [f"M1 ${a}x - {b} = e^{{{c}}}$", "A1"]))


@gen("2.4", "Exponential growth and decay models", difficulty=2)
def exp_model(rng):
    A = rng.randint(2, 9) * 100
    kval = pick(rng, [0.02, 0.05, 0.08, 0.12, 0.15])
    t1 = rng.randint(3, 10)
    N1 = A * math.exp(kval * t1)
    N1r = round(N1)
    kk = math.log(N1r / A) / t1
    target = A * pick(rng, [2, 3, 5])
    tt = math.log(target / A) / kk
    ctx = pick(rng, [("bacteria in a culture", "hours"), ("rabbits on an island", "years"), ("followers of an account", "weeks")])
    return Q(f"The number of {ctx[0]}, $N$, is modelled by $N = Ae^{{kt}}$, where $t$ is the time in {ctx[1]}. Initially $N = {A}$, and when $t = {t1}$, $N = {N1r}$.\n(a) Find the value of $k$ to 3 significant figures.\n(b) Find the time when $N$ first exceeds ${target}$.\n(c) Give one reason why this model may not be realistic in the long term.",
             ("(a)", 3, f"$k = {sf(kk)}$", [f"B1 $A = {A}$", f"M1 ${N1r} = {A}e^{{{t1}k}}$", "A1"]),
             ("(b)", 2, f"$t = {sf(tt)}$ {ctx[1]}", ["M1 sets up and takes logs", "A1"]),
             ("(c)", 1, "unlimited growth; limited food/space/resources", ["B1"]), difficulty=2)


@gen("2.4", "Non-linear data: log y against x and log y against log x", difficulty=2)
def log_linear(rng):
    if rng.random() < 0.5:
        a, b = rng.randint(2, 20), pick(rng, [1.2, 1.5, 2, 2.5, 0.8])
        c, m = math.log10(a), math.log10(b)
        return Q(f"Two variables are believed to be related by $y = ab^{{x}}$. A graph of $\\log_{{10}} y$ against $x$ is a straight line with gradient ${dp(m,3)}$ and vertical intercept ${dp(c,3)}$. Find the values of $a$ and $b$ to 2 significant figures.",
                 ("", 4, f"$a = {sf(10**round(c,3),2)}$, $b = {sf(10**round(m,3),2)}$", ["M1 $\\log y = \\log a + x\\log b$", f"M1 $\\log a = {dp(c,3)}$", "A1 $a$", "A1 $b$"]), difficulty=2)
    a, nn = rng.randint(2, 15), pick(rng, [0.5, 1.5, 2, 2.5, 3, -1])
    c = math.log10(a)
    return Q(f"Two variables are believed to be related by $y = ax^{{n}}$. A graph of $\\log_{{10}} y$ against $\\log_{{10}} x$ is a straight line passing through $(0, {dp(c,3)})$ with gradient ${nn}$. Find $a$ to 2 significant figures and state $n$.",
             ("", 3, f"$a = {sf(10**round(c,3),2)}$, $n = {nn}$", ["M1 $\\log y = \\log a + n\\log x$", "A1 $n$", "A1 $a$"]), difficulty=2)


@gen("2.4", "Gradient of e^kx")
def grad_ekx(rng):
    A, kk, t0 = rng.randint(2, 50), pick(rng, [0.1, 0.2, 0.3, -0.1, -0.25, 0.05]), rng.randint(1, 10)
    g = A * kk * math.exp(kk * t0)
    return Q(f"The mass, $m$ grams, of a substance is $m = {A}e^{{{kk}t}}$. Find the rate of change of $m$ when $t = {t0}$, giving your answer to 3 significant figures.",
             ("", 2, f"${sf(g)}$ g per unit time", [f"M1 $\\frac{{dm}}{{dt}} = {sf(A*kk,3)}e^{{{kk}t}}$", "A1"]))


@gen("2.4", "Exponential functions and graphs")
def exp_graph(rng):
    a, b = rng.randint(1, 6), nz(rng, -6, 6)
    kk = pick(rng, [1, 2, -1, -2])
    return Q(f"Sketch the curve $y = {a}e^{{{term(kk,'x')}}} {signed(b)}$, stating the coordinates of the $y$-intercept and the equation of the asymptote.",
             ("", 3, f"$y$-intercept $(0, {a+b})$; asymptote $y = {b}$", ["B1 shape (" + ("increasing" if kk > 0 else "decreasing") + ")", "B1 intercept", "B1 asymptote"]))


@gen("2.2", "Modulus function y = |x|")
def modulus_vertex(rng):
    a, b, c = pick(rng, [1, 2, 3, -1, -2]), nz(rng, -5, 5), rng.randint(-6, 6)
    yint = a * abs(b) + c
    roots = []
    if a != 0 and F(-c, a) >= 0:
        d = F(-c, a)
        roots = sorted({b - d, b + d})
    return Q(f"Sketch $y = {term(a, '')}|x {signed(-b)[1:]}| {signed(c)}$, giving the coordinates of the vertex and of any points where the graph meets the axes.".replace("  ", " "),
             ("", 4, f"V-shape {'(inverted) ' if a < 0 else ''}with vertex $({b}, {c})$; $y$-intercept $(0, {yint})$" + ("; $x$-intercepts " + ", ".join(f"$({fr(r)}, 0)$" for r in roots) if roots else "; no $x$-intercepts"),
              ["B1 V shape, correct orientation", "B1 vertex", "B1 $y$-intercept", "B1 $x$-intercepts (or none)"]))
