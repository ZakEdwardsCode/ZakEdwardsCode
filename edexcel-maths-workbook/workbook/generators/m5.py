"""Module 5: Applied — statistics & mechanics (Paper 3). g = 9.8 m s^-2."""
import math
from fractions import Fraction as F

import sympy as sp

from ..core import L, M, Q, dp, fr, gen, nz, pick, sf, signed, term, t

G = 9.8


def binom_pmf(n, p, r):
    return math.comb(n, r) * p ** r * (1 - p) ** (n - r)


def binom_cdf(n, p, r):
    return sum(binom_pmf(n, p, i) for i in range(0, r + 1)) if r >= 0 else 0.0


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def inv_phi(p):
    lo, hi = -10.0, 10.0
    for _ in range(100):
        m = (lo + hi) / 2
        if phi(m) < p:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def p4(v):
    return f"{v:.4f}"


# ------------------------------------------------------------------ 5.1 statistics
@gen("5.1", "Binomial distribution")
def binom_probs(rng):
    n = rng.randint(8, 30)
    p = pick(rng, [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6])
    a = rng.randint(1, max(2, int(n * p)))
    b = rng.randint(int(n * p), min(n - 1, int(n * p) + 5))
    return Q(f"$X \\sim \\mathrm{{B}}({n}, {p})$. Find\n(a) $\\mathrm{{P}}(X = {a})$,  (b) $\\mathrm{{P}}(X \\leq {b})$,  (c) $\\mathrm{{P}}(X > {a})$,  (d) $\\mathrm{{P}}({a} < X \\leq {b})$.",
             ("(a)", 2, p4(binom_pmf(n, p, a)), [f"M1 $^{{{n}}}C_{{{a}}}({p})^{{{a}}}({round(1-p,2)})^{{{n-a}}}$", "A1"]),
             ("(b)", 1, p4(binom_cdf(n, p, b)), ["B1"]),
             ("(c)", 2, p4(1 - binom_cdf(n, p, a)), [f"M1 $1 - \\mathrm{{P}}(X \\leq {a})$", "A1"]),
             ("(d)", 2, p4(binom_cdf(n, p, b) - binom_cdf(n, p, a)), [f"M1 $\\mathrm{{P}}(X \\leq {b}) - \\mathrm{{P}}(X \\leq {a})$", "A1"]))


@gen("5.1", "Hypothesis testing: critical regions and p-values", difficulty=2)
def binom_critical(rng):
    for _ in range(50):
        q = _binom_critical(rng)
        if q is not None:
            return q
    raise RuntimeError("no critical region found")


def _binom_critical(rng):
    n = pick(rng, [10, 12, 15, 20, 25, 30, 40, 50])
    p = pick(rng, [0.2, 0.25, 0.3, 0.4, 0.5])
    tail = pick(rng, ["lower", "upper", "two"])
    alpha = pick(rng, [0.05, 0.1]) if tail != "two" else pick(rng, [0.05, 0.1])
    a_tail = alpha / 2 if tail == "two" else alpha
    lo_c = max([c for c in range(n + 1) if binom_cdf(n, p, c) <= a_tail], default=None)
    hi_c = min([c for c in range(n + 1) if 1 - binom_cdf(n, p, c - 1) <= a_tail], default=None)
    parts = []
    if tail in ("lower", "two") and lo_c is not None:
        parts.append(f"$X \\leq {lo_c}$")
    if tail in ("upper", "two") and hi_c is not None:
        parts.append(f"$X \\geq {hi_c}$")
    actual = (binom_cdf(n, p, lo_c) if lo_c is not None and tail != "upper" else 0) + (1 - binom_cdf(n, p, hi_c - 1) if hi_c is not None and tail != "lower" else 0)
    if len(parts) < (2 if tail == "two" else 1):
        return None
    h1 = {"lower": "<", "upper": ">", "two": "\\neq"}[tail]
    return Q(f"A random variable $X \\sim \\mathrm{{B}}({n}, p)$. A test of $\\mathrm{{H}}_0: p = {p}$ against $\\mathrm{{H}}_1: p {h1} {p}$ is carried out at the {int(alpha*100)}% level{' (with half in each tail)' if tail == 'two' else ''}.\n(a) Find the critical region.\n(b) State the actual significance level of the test.",
             ("(a)", 3, " or ".join(parts), ["M1 uses cumulative probabilities from $\\mathrm{B}(" + f"{n}, {p}" + ")$", "A1 critical value(s)", "A1 correct region"]),
             ("(b)", 1, p4(actual), ["B1"]), difficulty=2)


@gen("5.1", "Hypothesis testing: critical regions and p-values", difficulty=2)
def binom_test(rng):
    n = pick(rng, [15, 20, 25, 30, 40])
    p = pick(rng, [0.2, 0.3, 0.35, 0.4, 0.5])
    direction = pick(rng, ["increase", "decrease"])
    if direction == "increase":
        obs = int(n * p) + rng.randint(2, 6)
        pv = 1 - binom_cdf(n, p, obs - 1)
        expr = f"\\mathrm{{P}}(X \\geq {obs})"
    else:
        obs = max(0, int(n * p) - rng.randint(2, 5))
        pv = binom_cdf(n, p, obs)
        expr = f"\\mathrm{{P}}(X \\leq {obs})"
    alpha = pick(rng, [0.05, 0.1])
    rej = pv < alpha
    ctx = pick(rng, ["a seed company claims that {p:.0%} of its seeds produce red flowers", "a website claims that {p:.0%} of visitors make a purchase", "{p:.0%} of patients normally recover within a week"]).format(p=p)
    return Q(f"Historically, {ctx}. After a change, a random sample of ${n}$ is taken and ${obs}$ are found to have the property. Test, at the {int(alpha*100)}% level, whether there is evidence that the proportion has {direction}d. State your hypotheses clearly.",
             ("", 5, f"$\\mathrm{{H}}_0: p = {p}$, $\\mathrm{{H}}_1: p {'>' if direction == 'increase' else '<'} {p}$; ${expr} = {p4(pv)}$ {'<' if rej else '>'} ${alpha}$; " + ("reject $\\mathrm{H}_0$: evidence" if rej else "do not reject $\\mathrm{H}_0$: insufficient evidence") + f" that the proportion has {direction}d",
              ["B1 both hypotheses in terms of $p$", f"M1 $\\mathrm{{B}}({n}, {p})$ used", "A1 $p$-value", "M1 compares with significance level", "A1 conclusion in context"]), difficulty=2)


@gen("5.1", "Normal distribution")
def normal_probs(rng):
    mu = rng.randint(20, 200)
    sd = rng.randint(2, 25)
    a = mu + round(rng.uniform(-1.8, -0.2) * sd, 1)
    b = mu + round(rng.uniform(0.2, 1.8) * sd, 1)
    pa, pb = phi((a - mu) / sd), phi((b - mu) / sd)
    return Q(f"$X \\sim \\mathrm{{N}}({mu}, {sd}^{{2}})$. Find\n(a) $\\mathrm{{P}}(X < {b})$,  (b) $\\mathrm{{P}}(X > {a})$,  (c) $\\mathrm{{P}}({a} < X < {b})$.",
             ("(a)", 1, p4(pb), ["B1"]), ("(b)", 1, p4(1 - pa), ["B1"]), ("(c)", 2, p4(pb - pa), ["M1", "A1"]))


@gen("5.1", "Normal distribution", difficulty=2)
def normal_inverse(rng):
    mu = rng.randint(30, 120)
    sd = rng.randint(3, 15)
    p = pick(rng, [0.05, 0.1, 0.2, 0.25, 0.8, 0.9, 0.95, 0.975])
    a = mu + inv_phi(p) * sd
    return Q(f"$X \\sim \\mathrm{{N}}({mu}, {sd}^{{2}})$. Find the value of $a$ such that $\\mathrm{{P}}(X < a) = {p}$.",
             ("", 3, f"$a = {sf(a, 4)}$", [f"M1 $z = {inv_phi(p):.4f}$", "M1 $\\frac{a - " + str(mu) + "}{" + str(sd) + "} = z$", "A1"]), difficulty=2)


@gen("5.1", "Normal distribution", difficulty=3)
def normal_find_params(rng):
    mu, sd = rng.randint(40, 150), rng.randint(4, 20)
    p1, p2 = pick(rng, [(0.1, 0.8), (0.2, 0.9), (0.05, 0.7), (0.15, 0.95), (0.3, 0.85)])
    a, b = mu + inv_phi(p1) * sd, mu + inv_phi(p2) * sd
    a, b = round(a, 1), round(b, 1)
    z1, z2 = inv_phi(p1), inv_phi(p2)
    sd2 = (b - a) / (z2 - z1)
    mu2 = a - z1 * sd2
    return Q(f"$X \\sim \\mathrm{{N}}(\\mu, \\sigma^{{2}})$. Given $\\mathrm{{P}}(X < {a}) = {p1}$ and $\\mathrm{{P}}(X > {b}) = {round(1-p2, 2)}$, find $\\mu$ and $\\sigma$.",
             ("", 6, f"$\\mu = {sf(mu2, 4)}$, $\\sigma = {sf(sd2, 3)}$", [f"B1 $z = {z1:.4f}$", f"B1 $z = {z2:.4f}$", f"M1 $\\frac{{{a} - \\mu}}{{\\sigma}} = {z1:.4f}$", "M1 second equation", "M1 solves simultaneously", "A1 both"]), difficulty=3)


@gen("5.1", "Normal approximation to binomial", difficulty=2)
def normal_approx(rng):
    n = rng.randint(60, 200)
    p = pick(rng, [0.3, 0.4, 0.45, 0.5, 0.55, 0.6])
    mu, var = n * p, n * p * (1 - p)
    k = int(mu) + rng.randint(-8, 8)
    approx = phi((k + 0.5 - mu) / math.sqrt(var))
    exact = binom_cdf(n, p, k)
    return Q(f"$X \\sim \\mathrm{{B}}({n}, {p})$.\n(a) Explain why a normal approximation is suitable.\n(b) Use it to estimate $\\mathrm{{P}}(X \\leq {k})$.",
             ("(a)", 1, f"$n$ is large and $np = {sf(mu,3)}$, $n(1-p) = {sf(n-mu,3)}$ are both greater than 5 ($p$ not close to 0 or 1)", ["B1"]),
             ("(b)", 4, f"$Y \\sim \\mathrm{{N}}({sf(mu,4)}, {sf(var,4)})$, $\\mathrm{{P}}(Y < {k}.5) = {p4(approx)}$ (exact {p4(exact)})", ["B1 mean and variance", "M1 continuity correction", "M1 standardises", "A1"]), difficulty=2)


@gen("5.1", "Hypothesis testing: normal mean and correlation", difficulty=3)
def normal_mean_test(rng):
    mu0, sd = rng.randint(50, 200), rng.randint(5, 20)
    n = pick(rng, [16, 20, 25, 36, 40, 50])
    shift = round(rng.uniform(0.3, 1.3) * sd / math.sqrt(n) * pick(rng, [1, -1]) * 2, 1)
    xbar = mu0 + shift
    z = (xbar - mu0) / (sd / math.sqrt(n))
    alpha = pick(rng, [0.05, 0.01])
    tail = "greater" if shift > 0 else "less"
    pv = 1 - phi(z) if shift > 0 else phi(z)
    rej = pv < alpha
    return Q(f"The masses of items are normally distributed with standard deviation ${sd}$ g. The mean is claimed to be ${mu0}$ g. A random sample of ${n}$ items has mean ${xbar}$ g. Test, at the {int(alpha*100)}% level, whether the mean is {tail} than ${mu0}$ g.",
             ("", 6, f"$\\bar{{X}} \\sim \\mathrm{{N}}({mu0}, \\frac{{{sd}^{{2}}}}{{{n}}})$; $z = {z:.3f}$, $p$-value ${p4(pv)}$; " + ("reject $\\mathrm{H}_0$" if rej else "do not reject $\\mathrm{H}_0$"),
              [f"B1 $\\mathrm{{H}}_0: \\mu = {mu0}$, $\\mathrm{{H}}_1: \\mu {'>' if shift > 0 else '<'} {mu0}$", "M1 distribution of $\\bar{X}$", "M1 standardises", "A1 $p$-value or $z$ vs critical value", "M1 comparison", "A1 conclusion in context"]), difficulty=3)


# 5% one-tailed critical values of the PMCC (Pearson Edexcel formula booklet)
PMCC_5 = {6: 0.7293, 7: 0.6694, 8: 0.6215, 9: 0.5822, 10: 0.5494, 11: 0.5214, 12: 0.4973, 13: 0.4762, 14: 0.4575, 15: 0.4409, 16: 0.4259, 17: 0.4124, 18: 0.4000, 19: 0.3887, 20: 0.3783}


@gen("5.1", "Correlation and regression", difficulty=2)
def pmcc_test(rng):
    n = pick(rng, list(PMCC_5))
    cv = PMCC_5[n]
    r = round(rng.uniform(cv - 0.2, cv + 0.25), 3) * pick(rng, [1, 1, -1])
    sign = ">" if r > 0 else "<"
    rej = abs(r) > cv
    return Q(f"A sample of ${n}$ pairs gives a product moment correlation coefficient $r = {r}$. Test, at the 5% level, whether there is evidence of a {'positive' if r > 0 else 'negative'} correlation in the population. (One-tailed critical value: ${cv}$.)",
             ("", 4, f"$\\mathrm{{H}}_0: \\rho = 0$, $\\mathrm{{H}}_1: \\rho {sign} 0$; $|r| {'>' if rej else '<'} {cv}$ so " + ("reject $\\mathrm{H}_0$: evidence of correlation" if rej else "do not reject $\\mathrm{H}_0$"),
              ["B1 hypotheses in terms of $\\rho$", "M1 compares with critical value", "A1 decision", "A1 context"]), difficulty=2)


@gen("5.1", "Correlation and regression")
def regression_interpret(rng):
    a, b = round(rng.uniform(2, 40), 1), round(rng.uniform(-3, 5), 2)
    xv = rng.randint(5, 30)
    ctx = pick(rng, [("daily mean temperature (°C)", "ice creams sold"), ("hours of revision", "test score"), ("daily rainfall (mm)", "umbrellas sold")])
    return Q(f"The regression line of $y$, {ctx[1]}, on $x$, {ctx[0]}, is $y = {a} {'+' if b >= 0 else '-'} {abs(b)}x$.\n(a) Interpret the gradient in context.\n(b) Estimate $y$ when $x = {xv}$ and comment on reliability if the data ranged from 2 to 20.",
             ("(a)", 1, f"each extra unit of $x$ changes {ctx[1]} by ${b}$", ["B1"]),
             ("(b)", 2, f"${sf(a + b*xv, 3)}$; " + ("interpolation, so reliable" if 2 <= xv <= 20 else "extrapolation, so unreliable"), ["B1", "B1"]))


@gen("5.1", "Probability: Venn diagrams and set notation")
def venn(rng):
    tot = pick(rng, [50, 60, 80, 100, 120])
    both = rng.randint(4, tot // 5)
    a_only = rng.randint(5, tot // 3)
    b_only = rng.randint(5, tot // 3)
    neither = tot - both - a_only - b_only
    if neither < 0:
        return venn(rng)
    pA, pB, pAB = F(a_only + both, tot), F(b_only + both, tot), F(both, tot)
    ind = pA * pB == pAB
    return Q(f"In a group of ${tot}$ students, ${a_only + both}$ study Art, ${b_only + both}$ study Biology and ${neither}$ study neither.\n(a) Draw a Venn diagram.\n(b) Find $\\mathrm{{P}}(A \\cap B)$, $\\mathrm{{P}}(A \\cup B')$ and $\\mathrm{{P}}(A \\mid B)$.\n(c) Determine whether $A$ and $B$ are independent.",
             ("(a)", 3, f"Art only ${a_only}$, both ${both}$, Biology only ${b_only}$, neither ${neither}$", ["B1 both", "B1 only regions", "B1 neither"]),
             ("(b)", 4, f"${fr(pAB)}$; ${fr(F(a_only + both + neither, tot))}$; ${fr(F(both, b_only + both))}$", ["B1", "M1A1", "B1"]),
             ("(c)", 2, f"$\\mathrm{{P}}(A)\\mathrm{{P}}(B) = {fr(pA * pB)}$ " + ("$=$" if ind else "$\\neq$") + f" ${fr(pAB)}$ so " + ("independent" if ind else "not independent"), ["M1", "A1"]))


@gen("5.1", "Conditional probability and tree diagrams", difficulty=2)
def tree(rng):
    pA = pick(rng, [F(1, 4), F(1, 3), F(2, 5), F(3, 10), F(1, 5)])
    pBA, pBnA = pick(rng, [F(2, 3), F(3, 4), F(9, 10), F(4, 5)]), pick(rng, [F(1, 10), F(1, 5), F(1, 4), F(1, 3)])
    pB = pA * pBA + (1 - pA) * pBnA
    post = pA * pBA / pB
    ev, cond, cond_given = pick(rng, [("Ben is late for school", "it rains on a given day", "it rained"),
                                      ("a person tests positive", "a person has a condition", "the person has the condition"),
                                      ("a student passes the test", "a student attends revision sessions", "the student attended revision")])
    return Q(f"The probability that {cond} is ${fr(pA)}$. If so, the probability that {ev} is ${fr(pBA)}$; otherwise it is ${fr(pBnA)}$.\n(a) Find the probability that {ev}.\n(b) Given that {ev}, find the probability that {cond_given}.",
             ("(a)", 3, f"${fr(pB)}$", ["M1 tree diagram / sum of two products", "A1 one product", "A1"]),
             ("(b)", 3, f"${fr(post)}$", ["M1 $\\frac{\\mathrm{P}(A \\cap B)}{\\mathrm{P}(B)}$", "A1ft numerator", "A1"]), difficulty=2)


@gen("5.1", "Measures of location and spread, coding")
def summary_stats(rng):
    n = rng.randint(10, 30)
    data = [rng.randint(10, 60) for _ in range(n)]
    sx, sxx = sum(data), sum(v * v for v in data)
    mean = sx / n
    sd = math.sqrt(sxx / n - mean ** 2)
    a, b = rng.randint(2, 20), pick(rng, [2, 5, 10])
    return Q(f"For ${n}$ values of $x$: $\\sum x = {sx}$ and $\\sum x^{{2}} = {sxx}$.\n(a) Find the mean and standard deviation of $x$.\n(b) The data are coded using $y = \\frac{{x - {a}}}{{{b}}}$. Find the mean and standard deviation of $y$.",
             ("(a)", 3, f"mean ${sf(mean, 4)}$, s.d. ${sf(sd, 4)}$", ["B1 mean", "M1 $\\sqrt{\\frac{\\sum x^{2}}{n} - \\bar{x}^{2}}$", "A1"]),
             ("(b)", 2, f"mean ${sf((mean - a)/b, 4)}$, s.d. ${sf(sd/b, 4)}$", ["B1ft", "B1ft"]))


@gen("5.1", "Histograms, box plots, cumulative frequency, outliers")
def histogram_fd(rng):
    bounds = [0, 10, 20, 30, 50, 80]
    freqs = [rng.randint(4, 30) for _ in range(5)]
    fds = [f / (bounds[i + 1] - bounds[i]) for i, f in enumerate(freqs)]
    q1, q3 = rng.randint(20, 35), rng.randint(40, 55)
    iqr = q3 - q1
    rows = ", ".join(f"${bounds[i]} \\leq t < {bounds[i+1]}$: ${freqs[i]}$" for i in range(5))
    return Q(f"The times, $t$ minutes, taken by some students are grouped as: {rows}.\n(a) Find the frequency density of each class for a histogram.\n(b) For a different data set, $Q_1 = {q1}$ and $Q_3 = {q3}$. Outliers are values more than $1.5 \\times$ IQR beyond the quartiles. Find the outlier boundaries.",
             ("(a)", 2, ", ".join(sf(v, 3) for v in fds), ["M1 frequency $\\div$ class width", "A1"]),
             ("(b)", 2, f"below ${q1 - 1.5*iqr:g}$ or above ${q3 + 1.5*iqr:g}$", ["M1 IQR $= " + str(iqr) + "$", "A1"]))


SAMPLING = [
    ("Populations and sampling methods", "Describe how to take a simple random sample of 40 students from a school of 900.", "number students 1 to 900 (sampling frame); use a random number generator to pick 40 distinct numbers; ignore repeats", 3),
    ("Populations and sampling methods", "A company has 120 managers and 480 workers. Explain how to take a stratified sample of 50 employees, and give one advantage.", "10 managers and 40 workers chosen randomly from each stratum; advantage: proportional representation of each group", 3),
    ("Populations and sampling methods", "Give one advantage and one disadvantage of quota sampling compared with stratified sampling.", "advantage: no sampling frame needed, quick; disadvantage: not random, interviewer bias", 2),
    ("Populations and sampling methods", "Explain the difference between a census and a sample, giving one advantage of each.", "census: every member, fully accurate; sample: subset, quicker/cheaper/less data", 2),
    ("Populations and sampling methods", "Describe how to take a systematic sample of 20 from a list of 500 customers.", "every 25th customer after a random start between 1 and 25", 2),
    ("The large data set", "Using your knowledge of the large data set, explain why daily mean windspeed for Leeming may contain the entry 'n/a' and how you would clean such data.", "data not recorded/available; remove those days before calculating statistics", 2),
    ("The large data set", "Explain why data from the large data set for Perth (Australia) in May might not be suitable for estimating UK summer rainfall.", "different hemisphere/season and climate; not representative of UK summer", 2),
    ("The large data set", "The large data set records 'tr' for daily total rainfall. State what this means and the value used in calculations.", "trace: less than 0.05 mm; treated as 0", 2),
]


def _bank_gen(skill):
    def fn(rng):
        _, qtext, ans, m = pick(rng, [b for b in SAMPLING if b[0] == skill])
        return Q(qtext, ("", m, ans, ["B1 per valid point"] * m))
    fn.__name__ = "bank_" + skill.split()[0].lower()
    return gen("5.1", skill)(fn)


for _skill in ("Populations and sampling methods", "The large data set"):
    _bank_gen(_skill)


# ------------------------------------------------------------------ 5.2 mechanics
@gen("5.2", "Constant acceleration: suvat")
def suvat(rng):
    u = rng.randint(0, 20)
    a = pick(rng, [0.5, 1.2, 2, 2.5, 3, -1.5, -2, 0.8])
    tt = rng.randint(3, 12)
    v = u + a * tt
    s = u * tt + 0.5 * a * tt ** 2
    if v < 0:
        a = abs(a)
        v, s = u + a * tt, u * tt + 0.5 * a * tt ** 2
    return Q(f"A car moves along a straight road with constant acceleration. It passes point $A$ with speed ${u}$ m s$^{{-1}}$ and passes point $B$ ${tt}$ s later with speed ${v:g}$ m s$^{{-1}}$.\n(a) Find the acceleration.\n(b) Find the distance $AB$.",
             ("(a)", 2, f"${a:g}$ m s$^{{-2}}$", ["M1 $v = u + at$", "A1"]), ("(b)", 2, f"${s:g}$ m", ["M1 $s = \\frac{1}{2}(u + v)t$", "A1"]))


@gen("5.2", "Constant acceleration: suvat", difficulty=2)
def vertical(rng):
    u = rng.randint(5, 25)
    h = rng.randint(0, 40)
    tmax = u / G
    H = h + u * u / (2 * G)
    # time to hit ground: -h = u t - 4.9 t^2
    tg = (u + math.sqrt(u * u + 2 * G * h)) / G
    return Q(f"A ball is projected vertically upwards at ${u}$ m s$^{{-1}}$ from a point ${h}$ m above the ground.\n(a) Find the greatest height above the ground.\n(b) Find the time taken to reach the ground.\n(c) State one modelling assumption.",
             ("(a)", 3, f"${sf(H)}$ m", ["M1 $v^{2} = u^{2} + 2as$ with $v = 0$", "A1 height above start", "A1"]),
             ("(b)", 3, f"${sf(tg)}$ s", [f"M1 $-{h} = {u}t - 4.9t^{{2}}$", "M1 solves", "A1"]),
             ("(c)", 1, "particle; no air resistance; $g$ constant", ["B1"]), difficulty=2)


@gen("5.2", "Motion graphs")
def vt_graph(rng):
    v = rng.randint(6, 30)
    t1, t2, t3 = rng.randint(2, 10), rng.randint(5, 30), rng.randint(2, 12)
    dist = 0.5 * t1 * v + t2 * v + 0.5 * t3 * v
    return Q(f"A train starts from rest and accelerates uniformly for ${t1}$ s to ${v}$ m s$^{{-1}}$, travels at this speed for ${t2}$ s, then decelerates uniformly to rest in ${t3}$ s.\n(a) Sketch a velocity-time graph.\n(b) Find the total distance travelled.\n(c) Find the deceleration.",
             ("(a)", 2, "trapezium shape", ["B1 shape", "B1 values"]), ("(b)", 2, f"${dist:g}$ m", ["M1 area of trapezium", "A1"]), ("(c)", 1, f"${sf(v/t3)}$ m s$^{{-2}}$", ["B1"]))


@gen("5.2", "Variable acceleration with calculus", difficulty=2)
def variable_acc(rng):
    a, b, c = nz(rng, -3, 3), rng.randint(-10, 10), rng.randint(0, 12)
    vt = a * t ** 2 + b * t + c
    T = rng.randint(1, 5)
    acc = sp.diff(vt, t).subs(t, T)
    s = sp.integrate(vt, (t, 0, T))
    return Q(f"A particle moves in a straight line with velocity $v = {L(vt)}$ m s$^{{-1}}$ at time $t$ s.\n(a) Find the acceleration when $t = {T}$.\n(b) Find the displacement from the starting point when $t = {T}$.",
             ("(a)", 2, f"${L(acc)}$ m s$^{{-2}}$", ["M1 differentiates", "A1"]), ("(b)", 3, f"${L(s)}$ m", ["M1 integrates", "M1 limits / $c = 0$", "A1"]), difficulty=2)


@gen("5.2", "2D motion with vectors", difficulty=2)
def vectors_kin(rng):
    u = (rng.randint(-5, 5), rng.randint(-5, 5))
    a = (nz(rng, -3, 3), nz(rng, -3, 3))
    T = rng.randint(2, 6)
    v = (u[0] + a[0] * T, u[1] + a[1] * T)
    sp_ = math.hypot(*v)
    ang = math.degrees(math.acos(v[0] / sp_)) if sp_ else 0.0
    return Q(f"A particle has initial velocity $({u[0]}\\mathbf{{i}} {signed(u[1], chr(92)+'mathbf{j}')})$ m s$^{{-1}}$ and constant acceleration $({a[0]}\\mathbf{{i}} {signed(a[1], chr(92)+'mathbf{j}')})$ m s$^{{-2}}$. Find its speed after ${T}$ s and the angle its direction of motion makes with $\\mathbf{{i}}$.",
             ("", 4, f"$\\mathbf{{v}} = {v[0]}\\mathbf{{i}} {signed(v[1], chr(92)+'mathbf{j}')}$; speed ${sf(sp_)}$ m s$^{{-1}}$; angle ${ang:.1f}^\\circ$ from $\\mathbf{{i}}$", ["M1 $\\mathbf{v} = \\mathbf{u} + \\mathbf{a}t$", "A1", "M1 magnitude", "A1 angle"]), difficulty=2)


@gen("5.2", "Connected particles and pulleys", difficulty=2)
def pulley(rng):
    m1, m2 = sorted(rng.sample(range(1, 9), 2))
    a = (m2 - m1) * G / (m1 + m2)
    T = m1 * (G + a)
    h = rng.randint(1, 4)
    v = math.sqrt(2 * a * h)
    return Q(f"Particles $A$ (${m1}$ kg) and $B$ (${m2}$ kg) are connected by a light inextensible string over a smooth fixed pulley. The system is released from rest with $B$ ${h}$ m above the ground.\n(a) Find the acceleration of the system and the tension in the string.\n(b) Find the speed with which $B$ hits the ground.\n(c) State how you used the fact that the string is inextensible.",
             ("(a)", 5, f"$a = {sf(a)}$ m s$^{{-2}}$, $T = {sf(T)}$ N", [f"M1 equation for $B$: ${m2}g - T = {m2}a$", f"M1 equation for $A$: $T - {m1}g = {m1}a$", "A1 both correct", "A1 $a$", "A1 $T$"]),
             ("(b)", 2, f"${sf(v)}$ m s$^{{-1}}$", ["M1 $v^{2} = 2as$", "A1"]), ("(c)", 1, "both particles have the same acceleration (magnitude)", ["B1"]), difficulty=2)


@gen("5.2", "Inclined planes", difficulty=2)
def incline_friction(rng):
    m = rng.randint(2, 10)
    tanv = pick(rng, [(3, 4, 5), (5, 12, 13), (7, 24, 25)])
    sinA, cosA = F(tanv[0], tanv[2]), F(tanv[1], tanv[2])
    mu = pick(rng, [0.1, 0.2, 0.25, 0.3])
    R = m * G * float(cosA)
    fr_ = mu * R
    a = G * float(sinA) - fr_ / m
    if a <= 0:
        mu = 0.1
        fr_ = mu * R
        a = G * float(sinA) - fr_ / m
    return Q(f"A particle of mass ${m}$ kg slides down a rough plane inclined at $\\alpha$ to the horizontal, where $\\tan\\alpha = {fr(sinA/cosA)}$. The coefficient of friction is ${mu}$.\nFind the normal reaction and the acceleration of the particle.",
             ("", 6, f"$R = {sf(R)}$ N, $a = {sf(a)}$ m s$^{{-2}}$", [f"B1 $\\sin\\alpha = {fr(sinA)}$, $\\cos\\alpha = {fr(cosA)}$", "M1 resolves perpendicular", "A1 $R$", "M1 $F = \\mu R$", "M1 Newton II along the plane", "A1 $a$"]), difficulty=2)


@gen("5.2", "Friction")
def friction_horizontal(rng):
    m, P = rng.randint(2, 12), rng.randint(20, 80)
    mu = pick(rng, [0.1, 0.2, 0.25, 0.3, 0.4])
    Fmax = mu * m * G
    if P <= Fmax:
        return Q(f"A box of mass ${m}$ kg rests on rough horizontal ground ($\\mu = {mu}$). A horizontal force of ${P}$ N is applied. Determine whether the box moves.",
                 ("", 3, f"$F_{{max}} = {sf(Fmax)}$ N $\\geq {P}$ N so it stays at rest (friction $= {P}$ N)", ["M1 $R = mg$", "M1 $\\mu R$", "A1 conclusion"]))
    a = (P - Fmax) / m
    return Q(f"A box of mass ${m}$ kg on rough horizontal ground ($\\mu = {mu}$) is pulled by a horizontal force of ${P}$ N. Find its acceleration.",
             ("", 4, f"${sf(a)}$ m s$^{{-2}}$", ["M1 $R = " + str(m) + "g$", "M1 $F = \\mu R$", "M1 $P - F = ma$", "A1"]))


@gen("5.2", "Newton's laws and resolving forces", difficulty=2)
def equilibrium(rng):
    w = rng.randint(10, 60)
    a1, a2 = pick(rng, [(30, 60), (40, 50), (45, 45), (20, 70), (35, 55)])
    # strings at a1, a2 to the horizontal holding weight w
    T1 = w * math.cos(math.radians(a2)) / math.sin(math.radians(a1 + a2))
    T2 = w * math.cos(math.radians(a1)) / math.sin(math.radians(a1 + a2))
    return Q(f"A particle of weight ${w}$ N hangs in equilibrium from two light strings inclined at ${a1}^\\circ$ and ${a2}^\\circ$ to the horizontal. Find the tension in each string.",
             ("", 5, f"$T_1 = {sf(T1)}$ N (at ${a1}^\\circ$), $T_2 = {sf(T2)}$ N (at ${a2}^\\circ$)", ["M1 resolves horizontally", "M1 resolves vertically", "A1 equations", "M1 solves", "A1 both"]), difficulty=2)


@gen("5.2", "Moments, equilibrium and centre of mass", difficulty=2)
def beam(rng):
    Lb = pick(rng, [4, 5, 6, 8, 10])
    W = rng.randint(50, 200)
    load = rng.randint(20, 150)
    d = round(rng.uniform(0.5, Lb - 0.5) * 2) / 2
    # supports at ends A (0) and B (Lb)
    RB = (W * Lb / 2 + load * d) / Lb
    RA = W + load - RB
    return Q(f"A uniform beam $AB$ of length ${Lb}$ m and weight ${W}$ N rests horizontally on supports at $A$ and $B$. A load of ${load}$ N is placed ${d:g}$ m from $A$. Find the reactions at the supports, and state one modelling assumption.",
             ("", 5, f"$R_A = {sf(RA)}$ N, $R_B = {sf(RB)}$ N", ["M1 moments about $A$", "A1", "M1 resolves vertically", "A1", "B1 uniform rod / load as particle"]), difficulty=2)


@gen("5.2", "Projectiles", difficulty=2)
def projectile(rng):
    U = rng.randint(10, 35)
    tri = pick(rng, [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13)])
    sinA, cosA = tri[0] / tri[2], tri[1] / tri[2]
    ux, uy = U * cosA, U * sinA
    T = 2 * uy / G
    Rg = ux * T
    H = uy ** 2 / (2 * G)
    return Q(f"A particle is projected from a point $O$ on horizontal ground with speed ${U}$ m s$^{{-1}}$ at angle $\\alpha$ above the horizontal, where $\\tan\\alpha = {fr(F(tri[0], tri[1]))}$.\nFind (a) the time of flight, (b) the range, (c) the greatest height.",
             ("(a)", 3, f"${sf(T)}$ s", [f"B1 components ${ux:g}$ and ${uy:g}$", "M1 $0 = U\\sin\\alpha\\, t - 4.9t^{2}$", "A1"]),
             ("(b)", 2, f"${sf(Rg)}$ m", ["M1 horizontal distance", "A1"]), ("(c)", 2, f"${sf(H)}$ m", ["M1 $v^{2} = u^{2} - 2gs$", "A1"]), difficulty=2)


@gen("5.2", "Quantities and units, modelling assumptions")
def modelling_terms(rng):
    term_, meaning = pick(rng, [("light", "has negligible mass, so tension is the same throughout"), ("inextensible", "does not stretch, so connected particles have equal acceleration"),
                                ("smooth", "no friction acts"), ("particle", "dimensions negligible; no rotation, mass at a point"), ("uniform rod", "mass evenly distributed so weight acts at the midpoint"),
                                ("rigid", "does not bend"), ("lamina", "a flat object with negligible thickness")])
    return Q(f"In mechanics, explain the meaning of the modelling term '{term_}' and its effect on calculations.", ("", 2, meaning, ["B1 meaning", "B1 effect"]))
