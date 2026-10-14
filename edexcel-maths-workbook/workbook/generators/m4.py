"""Module 4: Calculus & vectors (4.1 - 4.4). Answers are computed with sympy."""
import math
from fractions import Fraction as F

import sympy as sp

from ..core import L, M, Q, dp, fr, gen, nz, pick, poly, sf, signed, term, x, y, t

u = sp.Symbol("u")


def tidy(e):
    return sp.simplify(sp.factor(sp.simplify(e)))


def rand_inner(rng):
    return pick(rng, [x ** 2 + nz(rng, -5, 5), rng.randint(2, 5) * x + nz(rng, -6, 6), x ** 3 - rng.randint(1, 4), 1 + rng.randint(2, 4) * x ** 2])


# ------------------------------------------------------------------ 4.1
@gen("4.1", "Differentiation from first principles", difficulty=2)
def first_principles(rng):
    a, b, c = nz(rng, -4, 4), rng.randint(-6, 6), rng.randint(-5, 5)
    if rng.random() < 0.6:
        f = a * x ** 2 + b * x + c
        return Q(f"Prove, from first principles, that the derivative of ${L(f)}$ is ${L(sp.diff(f, x))}$.",
                 ("", 4, f"$\\lim_{{h \\to 0}} \\frac{{f(x+h) - f(x)}}{{h}} = \\lim_{{h \\to 0}}({L(sp.diff(f, x))} {signed(a,'h')}) = {L(sp.diff(f, x))}$",
                  ["B1 $f(x + h)$ expanded correctly", "M1 $\\frac{f(x+h) - f(x)}{h}$ simplified", "M1 limit as $h \\to 0$ taken with correct notation", "A1* complete proof"]), difficulty=2)
    f = a * x ** 3
    return Q(f"Prove, from first principles, that the derivative of ${L(f)}$ is ${L(sp.diff(f, x))}$.",
             ("", 5, f"$\\frac{{{a}(3x^{{2}}h + 3xh^{{2}} + h^{{3}})}}{{h}} \\to {L(sp.diff(f, x))}$ as $h \\to 0$", ["B1 $(x+h)^{3}$ expanded", "M1 difference quotient", "M1 divides by $h$", "M1 limit", "A1*"]), difficulty=2)


@gen("4.1", "Derivatives of sin x and cos x", difficulty=3)
def first_principles_sin(rng):
    fn = pick(rng, ["sin", "cos"])
    a = pick(rng, [1, 2, 3])
    return Q(f"Given that $\\theta$ is in radians, prove, from first principles, that the derivative of $\\{fn} {a if a > 1 else ''}x$ is ${'' if fn == 'sin' else '-'}{a if a>1 else ''}\\{'cos' if fn == 'sin' else 'sin'} {a if a > 1 else ''}x$.\nYou may assume that as $h \\to 0$, $\\frac{{\\sin h}}{{h}} \\to 1$ and $\\frac{{\\cos h - 1}}{{h}} \\to 0$.",
             ("", 5, "uses the addition formula, splits into the two standard limits", ["B1 uses $\\" + fn + "(A + B)$ expansion", "M1 difference quotient", "M1 groups terms with $\\sin " + (str(a) if a > 1 else "") + "h$ and $\\cos " + (str(a) if a > 1 else "") + "h - 1$", "M1 applies the limits", "A1* complete"]), difficulty=3)


@gen("4.1", "Exponentials and logarithms")
def diff_exp_log(rng):
    a, b = nz(rng, -5, 5), rng.randint(2, 5)
    c, d = nz(rng, -4, 4), rng.randint(1, 4)
    f = a * sp.exp(b * x) + c * sp.log(d * x) + pick(rng, [0, rng.randint(2, 9) ** x])
    return Q(f"Given $y = {L(f)}$, find $\\frac{{dy}}{{dx}}$.", ("", 3, f"$\\frac{{dy}}{{dx}} = {L(sp.diff(f, x))}$", ["B1 exponential term", "B1 log term", "B1 remaining term"]))


@gen("4.1", "Chain rule")
def chain(rng):
    inner = rand_inner(rng)
    outer = pick(rng, ["pow", "sqrt", "exp", "ln", "sin"])
    nn = rng.randint(3, 6)
    f = {"pow": inner ** nn, "sqrt": sp.sqrt(inner), "exp": sp.exp(inner), "ln": sp.log(inner), "sin": sp.sin(inner)}[outer]
    return Q(f"Differentiate $y = {L(f)}$ with respect to $x$.", ("", 2, f"${L(sp.factor(sp.diff(f, x)) if outer=='pow' else sp.diff(f, x))}$", ["M1 chain rule form", "A1"]))


@gen("4.1", "Product rule")
def product(rng):
    p1 = pick(rng, [x ** rng.randint(1, 3), (x + nz(rng, -4, 4)) ** 2, rng.randint(2, 5) * x])
    p2 = pick(rng, [sp.exp(rng.randint(-3, 3) or 2 * x), sp.sin(rng.randint(1, 4) * x), sp.log(x), sp.cos(2 * x), sp.sqrt(1 + x)])
    f = p1 * p2
    return Q(f"Find $\\frac{{dy}}{{dx}}$ when $y = {L(f)}$.", ("", 3, f"${L(sp.diff(f, x))}$", ["M1 $u'v + uv'$ form", "A1 one term", "A1 fully correct"]))


@gen("4.1", "Quotient rule")
def quotient(rng):
    num = pick(rng, [x ** 2 + nz(rng, -5, 5), sp.exp(2 * x), sp.sin(x), rng.randint(2, 6) * x + nz(rng, -5, 5)])
    den = pick(rng, [x + nz(rng, -5, 5), sp.cos(x), x ** 2 + rng.randint(1, 5), 1 + sp.exp(x)])
    f = num / den
    d = sp.together(sp.diff(f, x))
    n_, d_ = sp.fraction(d)
    return Q(f"Use the quotient rule to find $\\frac{{dy}}{{dx}}$ when $y = {L(f)}$, simplifying the numerator.", ("", 3, f"$\\frac{{{L(sp.expand(n_))}}}{{{L(d_)}}}$", ["M1 $\\frac{vu' - uv'}{v^{2}}$", "A1 correct unsimplified", "A1 simplified"]))


@gen("4.1", "Implicit differentiation", difficulty=2)
def implicit(rng):
    a, b, c = nz(rng, -3, 3), nz(rng, -3, 3), rng.randint(1, 3)
    x0, y0 = nz(rng, -3, 3), nz(rng, -3, 3)
    G = x ** 2 + a * x * y + c * y ** 2 + b * y
    k = G.subs({x: x0, y: y0})
    dydx = -sp.diff(G, x) / sp.diff(G, y)
    val = dydx.subs({x: x0, y: y0})
    if sp.diff(G, y).subs({x: x0, y: y0}) == 0:
        return implicit(rng)
    m = -1 / val if val != 0 else None
    return Q(f"A curve has equation ${L(G)} = {k}$.\n(a) Find $\\frac{{dy}}{{dx}}$ in terms of $x$ and $y$.\n(b) Find the gradient of the curve at the point $({x0}, {y0})$." + ("\n(c) Find the equation of the normal at this point in the form $y = mx + c$." if m is not None else ""),
             ("(a)", 4, f"$\\frac{{dy}}{{dx}} = {L(sp.simplify(dydx))}$", ["M1 differentiates $y$ terms with $\\frac{dy}{dx}$", "B1 product rule on $xy$", "M1 collects $\\frac{dy}{dx}$", "A1"]),
             ("(b)", 1, f"${L(val)}$", ["B1ft"]),
             *([("(c)", 2, f"$y = {L(sp.expand(m * x + y0 - m * x0))}$", ["M1 normal gradient and point", "A1"])] if m is not None else []), difficulty=2)


@gen("4.1", "Parametric differentiation", difficulty=2)
def param_diff(rng):
    a, b = nz(rng, -4, 4), rng.randint(1, 4)
    xt = pick(rng, [t ** 2 + a, b * t ** 3, sp.exp(t) + a, 2 * sp.sin(t)])
    yt = pick(rng, [t ** 3 - b * t, 4 * t + a, sp.exp(2 * t), 3 * sp.cos(t)])
    t0 = pick(rng, [1, 2, -1]) if not xt.has(sp.sin) else sp.pi / pick(rng, [3, 6, 4])
    d = sp.simplify(sp.diff(yt, t) / sp.diff(xt, t))
    v = sp.simplify(d.subs(t, t0))
    return Q(f"A curve has parametric equations $x = {L(xt)}$, $y = {L(yt)}$.\nFind $\\frac{{dy}}{{dx}}$ in terms of $t$, and its value when $t = {L(t0)}$.",
             ("", 4, f"$\\frac{{dy}}{{dx}} = {L(d)}$; at $t = {L(t0)}$: ${L(v)}$", ["B1 $\\frac{dx}{dt}$", "B1 $\\frac{dy}{dt}$", "M1 divides correctly", "A1 value"]), difficulty=2)


@gen("4.1", "Second derivatives, stationary points, convex / concave, inflection", difficulty=2)
def stationary(rng):
    r1, r2 = sorted(rng.sample(range(-4, 5), 2))
    a = pick(rng, [1, -1, 2])
    d = sp.expand(3 * a * (x - r1) * (x - r2))
    f = sp.integrate(d, x) + rng.randint(-6, 6)
    pts = []
    for r in (r1, r2):
        dd = sp.diff(f, x, 2).subs(x, r)
        pts.append(f"$({r}, {L(f.subs(x, r))})$ " + ("minimum" if dd > 0 else "maximum"))
    xi = F(r1 + r2, 2)
    return Q(f"The curve $C$ has equation $y = {L(f)}$.\n(a) Find the coordinates of the stationary points of $C$ and determine their nature.\n(b) Find the range of values of $x$ for which $C$ is concave.",
             ("(a)", 6, "; ".join(pts), ["M1 differentiates", "M1 sets $\\frac{dy}{dx} = 0$ and solves", "A1 $x$ values", "A1 $y$ values", "M1 second derivative test", "A1 natures"]),
             ("(b)", 2, f"$x {'<' if a > 0 else '>'} {fr(xi)}$", ["M1 $\\frac{d^{2}y}{dx^{2}} < 0$", "A1"]), difficulty=2)


@gen("4.1", "Tangents and normals")
def tangent_normal(rng):
    f = rng.randint(1, 3) * x ** 2 + nz(rng, -6, 6) * x + rng.randint(-5, 5) + pick(rng, [0, rng.randint(1, 8) / x, 2 * sp.sqrt(x)])
    x0 = rng.randint(1, 4)
    y0, m = f.subs(x, x0), sp.diff(f, x).subs(x, x0)
    which = pick(rng, ["tangent", "normal"])
    mm = m if which == "tangent" else -1 / m
    c = sp.nsimplify(y0 - mm * x0)
    return Q(f"Find an equation of the {which} to the curve $y = {L(f)}$ at the point where $x = {x0}$.",
             ("", 4, f"$y = {L(sp.expand(mm * x + c))}$", ["M1 differentiates", f"A1 gradient ${L(m)}$", "M1 " + ("tangent" if which == "tangent" else "uses $-1/m$") + " and point", "A1"]))


@gen("4.1", "Optimisation", difficulty=3)
def optimise_box(rng):
    kind = rng.randrange(2)
    if kind == 0:
        V = pick(rng, [500, 1000, 250, 2000])
        r = sp.Symbol("r", positive=True)
        A = 2 * sp.pi * r ** 2 + 2 * V / r
        rs = sp.solve(sp.diff(A, r), r)[0]
        return Q(f"A closed cylindrical can has volume ${V}$ cm$^3$ and radius $r$ cm.\n(a) Show that the surface area is $A = 2\\pi r^{{2}} + \\frac{{{2*V}}}{{r}}$.\n(b) Find the value of $r$ that minimises $A$ and the minimum area, to 3 significant figures.\n(c) Justify that this is a minimum.",
                 ("(a)", 3, "$h = \\frac{" + str(V) + "}{\\pi r^{2}}$ substituted into $2\\pi r^{2} + 2\\pi rh$", ["B1 volume equation", "M1 substitutes $h$", "A1*"]),
                 ("(b)", 4, f"$r = {sf(float(rs))}$, $A = {sf(float(A.subs(r, rs)))}$ cm$^2$", ["M1 differentiates", "M1 sets $= 0$", "A1 $r$", "A1 $A$"]),
                 ("(c)", 2, "$\\frac{d^{2}A}{dr^{2}} = 4\\pi + \\frac{" + str(4 * V) + "}{r^{3}} > 0$", ["M1", "A1"]), difficulty=3)
    L0 = pick(rng, [12, 18, 24, 30])
    V = x * (L0 - 2 * x) ** 2
    xs = F(L0, 6)
    return Q(f"An open box is made from a square sheet of card of side ${L0}$ cm by cutting a square of side $x$ cm from each corner and folding up the sides.\n(a) Show that the volume is $V = x({L0} - 2x)^{{2}}$.\n(b) Find the value of $x$ that maximises $V$ and the maximum volume.",
             ("(a)", 2, "base side $" + str(L0) + " - 2x$, height $x$", ["M1", "A1*"]),
             ("(b)", 5, f"$x = {fr(xs)}$, $V = {L(V.subs(x, sp.Rational(xs.numerator, xs.denominator)))}$ cm$^3$", ["M1 expands and differentiates", "A1", "M1 solves $V' = 0$ (rejects $x = " + str(L0 // 2) + "$)", "A1 $x$", "A1 $V$"]), difficulty=3)


@gen("4.1", "Connected rates of change", difficulty=2)
def rates(rng):
    kind = rng.randrange(3)
    rate = rng.randint(2, 20)
    if kind == 0:
        r0 = rng.randint(2, 10)
        drdt = rate / (4 * math.pi * r0 ** 2)
        return Q(f"Air is pumped into a spherical balloon at ${rate}$ cm$^3$ s$^{{-1}}$. Find the rate at which the radius is increasing when the radius is ${r0}$ cm.",
                 ("", 4, f"${sf(drdt)}$ cm s$^{{-1}}$", ["B1 $\\frac{dV}{dr} = 4\\pi r^{2}$", "M1 chain rule $\\frac{dr}{dt} = \\frac{dV}{dt} \\div \\frac{dV}{dr}$", "M1 substitutes", "A1"]), difficulty=2)
    if kind == 1:
        s0 = rng.randint(2, 12)
        dAdt = 2 * s0 * rate / 10
        return Q(f"The side of a square increases at ${rate/10}$ cm s$^{{-1}}$. Find the rate of increase of the area when the side is ${s0}$ cm.",
                 ("", 3, f"${sf(dAdt)}$ cm$^2$ s$^{{-1}}$", ["B1 $\\frac{dA}{dx} = 2x$", "M1 chain rule", "A1"]), difficulty=2)
    r0 = rng.randint(2, 8)
    dAdt = 2 * math.pi * r0 * rate / 10
    return Q(f"A circular ripple spreads so that its radius increases at ${rate/10}$ m s$^{{-1}}$. Find the rate of increase of its area when the radius is ${r0}$ m.",
             ("", 3, f"${sf(dAdt)}$ m$^2$ s$^{{-1}}$", ["B1 $\\frac{dA}{dr} = 2\\pi r$", "M1", "A1"]), difficulty=2)


# ------------------------------------------------------------------ 4.2
@gen("4.2", "Standard integrals")
def integrate_powers(rng):
    a, b, c = nz(rng, -6, 6), rng.randint(1, 8), nz(rng, -5, 5)
    p = pick(rng, [F(1, 2), F(3, 2), F(-1, 2), F(-2), F(-3)])
    f = a * x ** 2 + b * x ** sp.Rational(p.numerator, p.denominator) + c
    return Q(f"Find $\\int \\left({L(f)}\\right) dx$, simplifying each term.", ("", 3, f"${L(sp.integrate(f, x))} + c$", ["M1 raises a power by 1", "A1 two terms", "A1 all terms and $+ c$"]))


@gen("4.2", "Standard integrals")
def definite_basic(rng):
    a, b = rng.randint(1, 3), nz(rng, -6, 6)
    lo, hi = rng.randint(1, 2), rng.randint(3, 5)
    f = a * x ** 2 + b / x ** 2 + pick(rng, [0, sp.exp(x), 1 / x])
    v = sp.integrate(f, (x, lo, hi))
    return Q(f"Find the exact value of $\\int_{{{lo}}}^{{{hi}}} \\left({L(f)}\\right) dx$.", ("", 4, f"${L(sp.simplify(v))}$", ["M1 integrates", "A1", "M1 substitutes limits", "A1 exact"]))


@gen("4.2", "Integrating f(ax + b)")
def integrate_linear(rng):
    a, b = rng.randint(2, 6), nz(rng, -7, 7)
    kind = rng.randrange(4)
    lin = a * x + b
    p = rng.randint(3, 6)
    f = [lin ** p, sp.exp(lin), sp.cos(lin), 1 / lin][kind]
    I = [lin ** (p + 1) / (a * (p + 1)), sp.exp(lin) / a, sp.sin(lin) / a, sp.log(sp.Abs(lin)) / a][kind]
    return Q(f"Find $\\int {L(f)}\\, dx$.", ("", 2, f"${L(I)} + c$", [f"M1 correct form, divides by ${a}$", "A1"]))


@gen("4.2", "Reverse chain rule", difficulty=2)
def reverse_chain(rng):
    kind = rng.randrange(3)
    a = rng.randint(1, 6)
    if kind == 0:
        nn = rng.randint(3, 6)
        f = x * (x ** 2 + a) ** nn
        I = (x ** 2 + a) ** (nn + 1) / (2 * (nn + 1))
    elif kind == 1:
        f = (2 * x + 1) / (x ** 2 + x + a)
        I = sp.log(x ** 2 + x + a)
    else:
        kk = rng.randint(2, 4)
        f = x * sp.exp(kk * x ** 2)
        I = sp.exp(kk * x ** 2) / (2 * kk)
    return Q(f"Find $\\int {L(f)}\\, dx$.", ("", 3, f"${L(I)} + c$", ["M1 recognises $f'(x)g(f(x))$ form", "M1 adjusts constant", "A1"]), difficulty=2)


@gen("4.2", "Using trig identities in integration", difficulty=2)
def trig_identity_integral(rng):
    kind = rng.randrange(3)
    kk = rng.randint(1, 4)
    f = [sp.sin(kk * x) ** 2, sp.cos(kk * x) ** 2, sp.tan(kk * x) ** 2][kind]
    I = [x / 2 - sp.sin(2 * kk * x) / (4 * kk), x / 2 + sp.sin(2 * kk * x) / (4 * kk), sp.tan(kk * x) / kk - x][kind]
    hint = ["$\\sin^{2}A = \\frac{1}{2}(1 - \\cos 2A)$", "$\\cos^{2}A = \\frac{1}{2}(1 + \\cos 2A)$", "$\\tan^{2}A = \\sec^{2}A - 1$"][kind]
    return Q(f"Find $\\int {L(f)}\\, dx$.", ("", 3, f"${L(I)} + c$", [f"M1 uses {hint}", "M1 integrates", "A1"]), difficulty=2)


@gen("4.2", "Integration by substitution", difficulty=3)
def substitution(rng):
    a = rng.randint(1, 5)
    kind = rng.randrange(2)
    if kind == 0:
        f = x * sp.sqrt(x + a)
        lo, hi = -a + pick(rng, [0, 1]), pick(rng, [5, 12, 21]) - a
        v = sp.integrate(f, (x, lo, hi))
        return Q(f"Use the substitution $u = x + {a}$ to find the exact value of $\\int_{{{lo}}}^{{{hi}}} x\\sqrt{{x + {a}}}\\, dx$.",
                 ("", 6, f"${L(sp.nsimplify(v))}$", ["B1 $dx = du$, new limits", "M1 $\\int (u - " + str(a) + ")u^{\\frac{1}{2}}\\, du$", "M1 integrates", "A1", "M1 limits", "A1 exact"]), difficulty=3)
    f = x / (x ** 2 + a) ** 2
    I = sp.integrate(f, x)
    return Q(f"Use the substitution $u = x^{{2}} + {a}$ to find $\\int \\frac{{x}}{{(x^{{2}} + {a})^{{2}}}}\\, dx$.",
             ("", 4, f"${L(I)} + c$", ["B1 $du = 2x\\, dx$", "M1 $\\frac{1}{2}\\int u^{-2}\\, du$", "M1 integrates", "A1 in terms of $x$"]), difficulty=3)


@gen("4.2", "Integration by parts", difficulty=2)
def by_parts(rng):
    kind = rng.randrange(4)
    kk = rng.randint(1, 3)
    f = [x * sp.exp(kk * x), x * sp.cos(kk * x), x ** 2 * sp.log(x), x * sp.sin(kk * x)][kind]
    if kind == 2:
        v = sp.integrate(f, (x, 1, sp.E))
        return Q(f"Find the exact value of $\\int_{{1}}^{{e}} x^{{2}}\\ln x\\, dx$.", ("", 5, f"${L(sp.simplify(v))}$", ["M1 parts with $u = \\ln x$", "A1", "M1 second integral", "M1 limits", "A1"]), difficulty=2)
    return Q(f"Use integration by parts to find $\\int {L(f)}\\, dx$.", ("", 4, f"${L(sp.integrate(f, x))} + c$", ["M1 $u = x$", "A1 correct first stage", "M1 integrates second term", "A1"]), difficulty=2)


@gen("4.2", "Integration with partial fractions", difficulty=2)
def integ_partial(rng):
    a, b = rng.randint(1, 4), rng.randint(1, 4)
    if a == b:
        b += 1
    A, B = nz(rng, -4, 4), nz(rng, -4, 4)
    num = sp.expand(A * (x + b) + B * (x + a))
    den = sp.expand((x + a) * (x + b))
    v = sp.integrate(num / den, (x, 0, rng.randint(1, 3)))
    hi = [s for s in [1, 2, 3] if sp.integrate(num / den, (x, 0, s)) == v][0]
    return Q(f"Find the exact value of $\\int_{{0}}^{{{hi}}} \\frac{{{L(num)}}}{{{L(den)}}}\\, dx$, giving your answer as a single logarithm.",
             ("", 5, f"${L(sp.logcombine(sp.expand_log(v, force=True), force=True))}$", ["M1 partial fractions", "A1", "M1 integrates to $\\ln$ terms", "M1 limits", "A1"]), difficulty=2)


@gen("4.2", "Areas under curves and between curves", difficulty=2)
def area_between(rng):
    p, q = sorted(rng.sample(range(-3, 6), 2))
    m, c = nz(rng, -3, 3), rng.randint(-4, 4)
    # curve y = line - (x-p)(x-q)*a ; line above curve between p and q if a > 0... use curve below line
    a = pick(rng, [1, 2])
    line = m * x + c
    curve = sp.expand(line + a * (x - p) * (x - q))
    area = sp.integrate(line - curve, (x, p, q))
    return Q(f"The line $y = {L(line)}$ and the curve $y = {L(curve)}$ intersect at two points.\n(a) Find the $x$-coordinates of the points of intersection.\n(b) Find the exact area of the region enclosed between the line and the curve.",
             ("(a)", 2, f"$x = {p}$, $x = {q}$", ["M1 equates", "A1"]),
             ("(b)", 4, f"${L(area)}$", ["M1 $\\int (\\text{line} - \\text{curve})\\, dx$", "M1 integrates", "M1 limits", "A1"]), difficulty=2)


@gen("4.2", "Trapezium rule")
def trapezium(rng):
    f = pick(rng, [sp.sqrt(1 + x ** 3), sp.log(1 + x ** 2), sp.exp(-x ** 2) * 10, x * sp.sqrt(x + 1)])
    a, n_ = 0, pick(rng, [4, 5, 6])
    h = pick(rng, [F(1, 2), F(1, 4)]) if n_ == 4 else F(1, 2)
    b = a + h * n_
    xs = [a + h * i for i in range(n_ + 1)]
    ys = [float(f.subs(x, sp.Rational(v.numerator, v.denominator))) for v in xs]
    est = float(h) / 2 * (ys[0] + ys[-1] + 2 * sum(ys[1:-1]))
    exact = float(sp.Integral(f, (x, a, sp.Rational(b.numerator, b.denominator))).evalf())
    table = ", ".join(f"$x = {fr(v)}$: $y = {yv:.4f}$" for v, yv in zip(xs, ys))
    return Q(f"Use the trapezium rule with {n_} strips of equal width to estimate $\\int_{{{a}}}^{{{fr(b)}}} {L(f)}\\, dx$, giving your answer to 3 significant figures. State whether your answer is an over- or under-estimate, given the shape of the curve.",
             ("", 4, f"{table}; estimate ${sf(est)}$ ({'overestimate' if est > exact else 'underestimate'}; true value ${sf(exact, 4)}$)",
              [f"B1 $h = {fr(h)}$", "B1 $y$ values", "M1 $\\frac{h}{2}[y_0 + y_n + 2(\\ldots)]$", "A1"]))


@gen("4.2", "Separable differential equations", difficulty=2)
def separable(rng):
    kind = rng.randrange(3)
    if kind == 0:
        kk, y0 = rng.randint(1, 4), rng.randint(1, 6)
        sol = y0 * sp.exp(kk * x ** 2 / 2)
        return Q(f"Solve $\\frac{{dy}}{{dx}} = {kk if kk > 1 else ''}xy$, given $y = {y0}$ when $x = 0$. Give $y$ in terms of $x$.",
                 ("", 5, f"$y = {L(sol)}$", ["M1 separates $\\int \\frac{1}{y}\\, dy = \\int " + str(kk) + "x\\, dx$", "A1 $\\ln y = " + L(sp.Rational(kk, 2) * x ** 2) + " + c$", "M1 uses condition", "M1 exponentiates", "A1"]), difficulty=2)
    if kind == 1:
        a, y0 = rng.randint(1, 4), rng.randint(1, 5)
        return Q(f"Find the particular solution of $\\frac{{dy}}{{dx}} = \\frac{{{a}x^{{2}}}}{{y}}$, $y > 0$, for which $y = {y0}$ when $x = 0$.",
                 ("", 4, f"$y = \\sqrt{{{L(sp.Rational(2 * a, 3) * x ** 3)} + {y0*y0}}}$", ["M1 $\\int y\\, dy = \\int " + str(a) + "x^{2}\\, dx$", "A1 $\\frac{y^{2}}{2} = \\frac{" + str(a) + "x^{3}}{3} + c$", "M1 condition", "A1"]), difficulty=2)
    kk, T0, Ta = round(rng.uniform(0.02, 0.1), 2), rng.randint(70, 95), rng.randint(15, 25)
    tt = rng.randint(5, 20)
    Tt = Ta + (T0 - Ta) * math.exp(-kk * tt)
    return Q(f"A cup of tea cools in a room at ${Ta}^\\circ$C. Its temperature $\\theta$ after $t$ minutes satisfies $\\frac{{d\\theta}}{{dt}} = -{kk}(\\theta - {Ta})$. Initially $\\theta = {T0}$.\n(a) Show that $\\theta = {Ta} + {T0-Ta}e^{{-{kk}t}}$.\n(b) Find the temperature after ${tt}$ minutes.",
             ("(a)", 4, "separate, integrate to $\\ln(\\theta - " + str(Ta) + ") = -" + str(kk) + "t + c$, use $t = 0$", ["M1 separates", "A1", "M1 condition", "A1*"]),
             ("(b)", 1, f"${sf(Tt)}^\\circ$C", ["B1"]), difficulty=2)


@gen("4.2", "Modelling with differential equations", difficulty=2)
def form_de(rng):
    ctx = pick(rng, [("The rate of increase of a population $P$ is proportional to $P$", r"\frac{dP}{dt} = kP"),
                     ("The rate at which the volume $V$ of a raindrop decreases is proportional to its surface area, which is proportional to $V^{\\frac{2}{3}}$", r"\frac{dV}{dt} = -kV^{\frac{2}{3}}"),
                     ("The rate at which the temperature $\\theta$ of a liquid falls is proportional to the difference between $\\theta$ and room temperature $20^\\circ$C", r"\frac{d\theta}{dt} = -k(\theta - 20)"),
                     ("The rate of change of the height $h$ of water in a leaking tank is proportional to $\\sqrt{h}$", r"\frac{dh}{dt} = -k\sqrt{h}")])
    return Q(f"{ctx[0]}. Write down a differential equation to model this situation, defining any constant you use.",
             ("", 2, f"${ctx[1]}$, $k > 0$ a constant", ["M1 correct derivative and proportionality", "A1 sign and constant defined"]), difficulty=2)


@gen("4.2", "Integration as the limit of a sum")
def limit_sum(rng):
    a, b = rng.randint(0, 2), rng.randint(3, 6)
    f = pick(rng, [x ** 2, 3 * x ** 2 + 1, sp.sqrt(x), 2 * x + 5])
    ft = f"\\left({L(f)}\\right)" if f.is_Add else L(f)
    return Q(f"Write $\\lim_{{\\delta x \\to 0}} \\sum_{{x={a}}}^{{{b}}} {ft}\\,\\delta x$ as an integral and hence find its exact value.",
             ("", 3, f"$\\int_{{{a}}}^{{{b}}} {ft}\\, dx = {L(sp.integrate(f, (x, a, b)))}$", ["B1 integral form", "M1 integrates", "A1"]))


# ------------------------------------------------------------------ 4.3
def _cubic(rng):
    while True:
        co = [1, nz(rng, -4, 4), nz(rng, -6, 6), nz(rng, -9, 9)]
        f = sum(c * x ** (3 - i) for i, c in enumerate(co))
        rr = [float(sp.re(r)) for r in sp.Poly(f, x).nroots() if abs(sp.im(r)) < 1e-9]
        good = [r for r in rr if abs(r - round(r)) > 0.15 and abs(r - round(r) - 0.5) > 0.05]
        if good:
            return f, good[0]


@gen("4.3", "Locating roots by change of sign")
def change_sign(rng):
    f, r = _cubic(rng)
    a = math.floor(r)
    fa, fb = float(f.subs(x, a)), float(f.subs(x, a + 1))
    return Q(f"$f(x) = {L(f)}$. Show that the equation $f(x) = 0$ has a root $\\alpha$ in the interval $[{a}, {a+1}]$.",
             ("", 2, f"$f({a}) = {fa:g}$, $f({a+1}) = {fb:g}$; sign change and $f$ is continuous, so a root lies in the interval", ["M1 evaluates both", "A1 sign change, continuity, conclusion"]))


@gen("4.3", "When change of sign fails", difficulty=2)
def sign_fail(rng):
    a = nz(rng, -4, 4)
    kind = rng.randrange(2)
    if kind == 0:
        return Q(f"Explain why the change of sign method fails to locate the root of $f(x) = (x {signed(-a)[1:]})^{{2}}$ and why considering $f(x) = \\frac{{1}}{{x {signed(-a)[1:]}}}$ on $[{a-1}, {a+1}]$ would be misleading.",
                 ("", 2, f"repeated root at $x = {a}$: no sign change; $\\frac{{1}}{{x - {a}}}$ changes sign across an asymptote, not a root", ["B1", "B1"]), difficulty=2)
    return Q(f"$f(x) = \\tan x$. Explain why $f(1.5) > 0$ and $f(1.6) < 0$ does not imply a root in $[1.5, 1.6]$.",
             ("", 1, "$\\tan x$ is discontinuous at $x = \\frac{\\pi}{2} \\approx 1.571$ (vertical asymptote)", ["B1"]), difficulty=2)


@gen("4.3", "Fixed-point iteration x = g(x)", difficulty=2)
def iteration(rng):
    a, b = rng.randint(2, 6), rng.randint(1, 9)
    # x^3 - a x - b = 0 -> x = cbrt(a x + b)
    g = lambda v: (a * v + b) ** (1 / 3)
    x0 = rng.randint(1, 3)
    xs = [x0]
    for _ in range(3):
        xs.append(g(xs[-1]))
    v = x0
    for _ in range(80):
        v = g(v)
    return Q(f"(a) Show that $x^{{3}} - {a}x - {b} = 0$ can be written as $x = \\sqrt[3]{{{a}x + {b}}}$.\n(b) Using $x_{{n+1}} = \\sqrt[3]{{{a}x_{{n}} + {b}}}$ with $x_{{0}} = {x0}$, find $x_{{1}}$, $x_{{2}}$ and $x_{{3}}$ to 4 decimal places.\n(c) Show that the root is ${v:.3f}$ to 3 decimal places.",
             ("(a)", 1, "rearranges", ["B1*"]), ("(b)", 3, ", ".join(f"$x_{i} = {xs[i]:.4f}$" for i in (1, 2, 3)), ["M1", "A1 $x_1$", "A1 $x_2, x_3$"]),
             ("(c)", 2, f"$f({v-0.0005:.4f})$ and $f({v+0.0005:.4f})$ have opposite signs", ["M1 interval bounds", "A1 conclusion"]), difficulty=2)


@gen("4.3", "Newton-Raphson method", difficulty=2)
def newton(rng):
    f, r = _cubic(rng)
    x0 = round(r) + (0.5 if r > round(r) else -0.5)
    fp = sp.diff(f, x)
    x1 = x0 - float(f.subs(x, x0)) / float(fp.subs(x, x0))
    x2 = x1 - float(f.subs(x, x1)) / float(fp.subs(x, x1))
    return Q(f"$f(x) = {L(f)}$. Taking $x_{{0}} = {x0}$ as a first approximation to a root of $f(x) = 0$, apply the Newton-Raphson method twice to find $x_{{2}}$ to 3 decimal places.",
             ("", 4, f"$x_1 = {x1:.4f}$, $x_2 = {x2:.3f}$", [f"B1 $f'(x) = {L(fp)}$", "M1 $x_0 - \\frac{f(x_0)}{f'(x_0)}$", "A1 $x_1$", "A1 $x_2$"]), difficulty=2)


@gen("4.3", "Staircase and cobweb diagrams", difficulty=2)
def cobweb(rng):
    kk = pick(rng, [F(1, 2), F(-1, 2), 2, -2, F(3, 4), F(-3, 4)])
    conv = abs(kk) < 1
    shape = "staircase" if kk > 0 else "cobweb"
    return Q(f"An iteration $x_{{n+1}} = g(x_{{n}})$ has a fixed point $\\alpha$, and $g'(\\alpha) = {fr(kk)}$. State whether the iteration converges to $\\alpha$ for a starting value close to $\\alpha$, and whether the diagram is a staircase or a cobweb.",
             ("", 2, f"{'converges' if conv else 'diverges'} ($|g'(\\alpha)| {'<' if conv else '>'} 1$); {shape} diagram", ["B1 convergence with reason", "B1 shape"]), difficulty=2)


@gen("4.3", "Applications to modelling", difficulty=3)
def nr_model(rng):
    a = rng.randint(20, 60)
    # profit P = a x e^{-0.1x} - ... use a root: e^{0.5 t} = a - 2t
    f = sp.exp(sp.Rational(1, 2) * t) - (a - 2 * t)
    root = sp.nsolve(f, t, 6)
    return Q(f"The height difference between two tanks is modelled by $f(t) = e^{{0.5t}} - {a} + 2t$, $t \\geq 0$. The tanks are level when $f(t) = 0$.\nUse the Newton-Raphson method with $t_{{0}} = 6$ to find this time to 2 decimal places.",
             ("", 4, f"$t = {float(root):.2f}$", ["B1 $f'(t) = 0.5e^{0.5t} + 2$", "M1 applies the formula", "A1 first iterate", "A1 converged value"]), difficulty=3)


# ------------------------------------------------------------------ 4.4
def vec(a, b, c):
    out = []
    for coef, e in ((a, "i"), (b, "j"), (c, "k")):
        if coef == 0:
            continue
        tex = rf"\mathbf{{{e}}}" if abs(coef) == 1 else rf"{abs(coef)}\mathbf{{{e}}}"
        out.append(("-" if coef < 0 else "+", tex))
    if not out:
        return r"\mathbf{0}"
    s = ("-" if out[0][0] == "-" else "") + out[0][1]
    for sign, tex in out[1:]:
        s += f" {sign} {tex}"
    return s


@gen("4.4", "Magnitude and direction")
def magnitude(rng):
    a, b, c = pick(rng, [(1, 2, 2), (2, 3, 6), (1, 4, 8), (2, 6, 9), (3, 4, 12), (4, 4, 7), (6, 6, 7)])
    s = [pick(rng, [1, -1]) for _ in range(3)]
    v = (a * s[0], b * s[1], c * s[2])
    m = int(math.sqrt(a * a + b * b + c * c))
    return Q(f"$\\mathbf{{a}} = {vec(*v)}$. Find $|\\mathbf{{a}}|$ and a unit vector in the direction of $\\mathbf{{a}}$.",
             ("", 2, f"$|\\mathbf{{a}}| = {m}$; $\\frac{{1}}{{{m}}}({vec(*v)})$", ["B1", "B1ft"]))


@gen("4.4", "Position vectors and distance")
def distance3d(rng):
    A = [rng.randint(-6, 6) for _ in range(3)]
    B = [rng.randint(-6, 6) for _ in range(3)]
    d = [B[i] - A[i] for i in range(3)]
    d2 = sum(v * v for v in d)
    return Q(f"Points $A$ and $B$ have position vectors ${vec(*A)}$ and ${vec(*B)}$.\n(a) Find $\\overrightarrow{{AB}}$.\n(b) Find the exact distance $AB$.\n(c) Find the position vector of the midpoint of $AB$.",
             ("(a)", 1, f"${vec(*d)}$", ["B1"]), ("(b)", 2, f"$\\sqrt{{{d2}}}$" if math.isqrt(d2) ** 2 != d2 else f"${math.isqrt(d2)}$", ["M1", "A1"]),
             ("(c)", 1, "$" + vec(*[F(A[i] + B[i], 2) for i in range(3)]).replace("\\mathbf", "\\mathbf") + "$" if all((A[i] + B[i]) % 2 == 0 for i in range(3)) else "$\\frac{1}{2}(" + vec(*[A[i] + B[i] for i in range(3)]) + ")$", ["B1"]))


@gen("4.4", "Angles with axes", difficulty=2)
def angle_axis(rng):
    v = [nz(rng, -6, 6) for _ in range(3)]
    axis = pick(rng, [("x", 0), ("y", 1), ("z", 2)])
    m = math.sqrt(sum(c * c for c in v))
    ang = math.degrees(math.acos(v[axis[1]] / m))
    return Q(f"Find the angle that the vector ${vec(*v)}$ makes with the positive ${axis[0]}$-axis, to 1 decimal place.",
             ("", 2, f"${ang:.1f}^\\circ$", [f"M1 $\\cos\\theta = \\frac{{{v[axis[1]]}}}{{\\sqrt{{{sum(c*c for c in v)}}}}}$", "A1"]), difficulty=2)


@gen("4.4", "Geometric problems with vectors", difficulty=2)
def parallelogram(rng):
    A, B, C = ([rng.randint(-5, 5) for _ in range(3)] for _ in range(3))
    D = [A[i] + C[i] - B[i] for i in range(3)]
    return Q(f"$ABCD$ is a parallelogram with $A({', '.join(map(str, A))})$, $B({', '.join(map(str, B))})$ and $C({', '.join(map(str, C))})$. Find the coordinates of $D$.",
             ("", 3, f"$D({', '.join(map(str, D))})$", ["M1 $\\overrightarrow{AD} = \\overrightarrow{BC}$", "M1 $\\overrightarrow{OD} = \\overrightarrow{OA} + \\overrightarrow{BC}$", "A1"]), difficulty=2)


@gen("4.4", "3D coordinates and i, j, k notation")
def collinear(rng):
    A = [rng.randint(-5, 5) for _ in range(3)]
    d = [nz(rng, -3, 3) for _ in range(3)]
    kk = rng.randint(2, 4)
    B = [A[i] + d[i] for i in range(3)]
    Cp = [A[i] + kk * d[i] for i in range(3)]
    return Q(f"Show that the points $A({', '.join(map(str, A))})$, $B({', '.join(map(str, B))})$ and $C({', '.join(map(str, Cp))})$ are collinear, and find the ratio $AB : BC$.",
             ("", 3, f"$\\overrightarrow{{AC}} = {kk}\\overrightarrow{{AB}}$ with common point $A$; $AB : BC = 1 : {kk-1}$", ["M1 finds two vectors", "A1 scalar multiple + common point", "B1 ratio"]))


@gen("4.4", "Vectors in mechanics", difficulty=2)
def resultant_force(rng):
    F1 = [nz(rng, -8, 8) for _ in range(3)]
    F2 = [rng.randint(-8, 8) for _ in range(3)]
    m = rng.randint(2, 6)
    Rv = [F1[i] + F2[i] for i in range(3)]
    mag = math.sqrt(sum(c * c for c in Rv))
    return Q(f"Two forces $\\mathbf{{F}}_1 = ({vec(*F1)})$ N and $\\mathbf{{F}}_2 = ({vec(*F2)})$ N act on a particle of mass ${m}$ kg. Find the magnitude of the acceleration of the particle.",
             ("", 3, f"${sf(mag/m)}$ m s$^{{-2}}$", ["M1 resultant force", "M1 $\\mathbf{F} = m\\mathbf{a}$", "A1"]), difficulty=2)
