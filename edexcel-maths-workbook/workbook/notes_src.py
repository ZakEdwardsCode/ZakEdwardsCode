"""Source for notes.json — key facts, methods and exam traps per subtopic.
Run `python -m workbook.notes_src` to regenerate notes.json."""
import json
from pathlib import Path

N = {}

N["1.1"] = dict(
    summary="Manipulating powers, brackets and surds is the grammar of every later topic. Most marks are lost to sign slips and to not writing answers in the exact form asked for.",
    key=[r"$a^m \times a^n = a^{m+n}$, $\;a^m \div a^n = a^{m-n}$, $\;(a^m)^n = a^{mn}$",
         r"$a^{-n} = \frac{1}{a^n}$, $\;a^{\frac{1}{n}} = \sqrt[n]{a}$, $\;a^{\frac{m}{n}} = (\sqrt[n]{a})^m$, $\;a^0 = 1$",
         r"$\sqrt{ab} = \sqrt{a}\sqrt{b}$, $\;\sqrt{\frac{a}{b}} = \frac{\sqrt{a}}{\sqrt{b}}$",
         r"Rationalise $\frac{1}{a + \sqrt{b}}$ by multiplying top and bottom by $a - \sqrt{b}$",
         r"$a^2 - b^2 = (a - b)(a + b)$"],
    method=["Write every term as a power of the same base before combining.",
            "Turn roots into fractional powers before differentiating or integrating.",
            "Factorise fully: take out the HCF first, then look for a quadratic or difference of two squares.",
            "For surds, find the largest square factor: $\\sqrt{72} = \\sqrt{36}\\sqrt{2} = 6\\sqrt{2}$."],
    traps=["$(3x)^2 = 9x^2$, not $3x^2$.", "$\\sqrt{a + b} \\neq \\sqrt{a} + \\sqrt{b}$.",
           "$\\frac{1}{\\sqrt{x}} = x^{-\\frac{1}{2}}$ (the minus sign is the most dropped mark in Paper 1).",
           "'Factorise fully' means no common factor left inside any bracket."],
    exam="Appears as quick 2-4 mark openers on Paper 1 and Paper 2, and inside almost every calculus question.")

N["1.2"] = dict(
    summary="Quadratics are solved by factorising, completing the square or the formula. The discriminant tells you how many roots there are and powers many 'find k' questions.",
    key=[r"$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$",
         r"$x^2 + bx + c = \left(x + \frac{b}{2}\right)^2 - \frac{b^2}{4} + c$",
         r"Turning point of $y = a(x + p)^2 + q$ is $(-p, q)$",
         r"$b^2 - 4ac > 0$: two distinct roots; $= 0$: one repeated root; $< 0$: no real roots",
         r"Line $y = mx + c$ is a tangent to a curve when the resulting quadratic has $b^2 - 4ac = 0$"],
    method=["To complete the square with $a \\neq 1$, take $a$ out of the $x^2$ and $x$ terms first.",
            "For 'find the range of k', write the discriminant condition, then solve the resulting inequality (often itself a quadratic: sketch it!).",
            "Hidden quadratics: substitute $u = x^2$, $u = \\sqrt{x}$, $u = e^x$ or $u = 2^x$ and solve for $u$ first.",
            "Sketching: roots, $y$-intercept, turning point, and the shape from the sign of $a$."],
    traps=["Forgetting the 'show that' needs every line of algebra.", "Not rejecting impossible values of $u$ (e.g. $e^x = -2$).",
           "Mixing up $>$ and $\\geq$ for 'real roots' (which includes equal roots: $\\geq 0$)."],
    exam="Discriminant 'find k' questions are 4-5 marks; completing the square often leads into a graph or a transformation question.")

N["1.3"] = dict(
    summary="Solve linear/quadratic simultaneous equations by substitution, and solve inequalities using a sketch so you pick the right region. Answers often need set notation.",
    key=[r"Quadratic inequality: find critical values, sketch, choose inside ($a < x < b$) or outside ($x < a$ or $x > b$)",
         r"Set notation: $\{x : -2 < x < 5\}$, $\;\{x : x < 1\} \cup \{x : x > 4\}$",
         r"Dashed lines for $<$ or $>$; solid lines for $\leq$ or $\geq$",
         r"Multiplying or dividing an inequality by a negative reverses its sign"],
    method=["Linear + quadratic: rearrange the linear equation for one variable and substitute into the quadratic.",
            "Always find both coordinates of every intersection point.",
            "For 'both inequalities hold', draw both solution sets on one number line and take the overlap."],
    traps=["Writing $2 < x > 5$ (meaningless).", "Using 'and' when you mean 'or' for outside regions.",
           "Dividing by a variable that could be negative."],
    exam="Typical 5-7 mark question: simultaneous equations followed by an inequality or region shading.")

N["1.4"] = dict(
    summary="Straight lines: gradient, equations in different forms, parallel and perpendicular lines, distances and midpoints, and using lines as simple models.",
    key=[r"$m = \frac{y_2 - y_1}{x_2 - x_1}$, $\;y - y_1 = m(x - x_1)$",
         r"Parallel lines: $m_1 = m_2$; perpendicular lines: $m_1 m_2 = -1$",
         r"Midpoint $\left(\frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2}\right)$, length $\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$",
         r"$ax + by + c = 0$ with $a, b, c$ integers is a common required form"],
    method=["Perpendicular bisector: midpoint + negative reciprocal gradient.",
            "Area of a triangle formed with the axes: find both intercepts first.",
            "In modelling questions, interpret the gradient as a rate and the intercept as a starting value."],
    traps=["Leaving fractions when 'integers' are demanded.", "Swapping $x$ and $y$ differences in the gradient."],
    exam="Usually combined with circles or as part (a) of a longer coordinate geometry question.")

N["1.5"] = dict(
    summary="Circles: write the equation from centre and radius, complete the square to find centre and radius, and use circle properties (tangent perpendicular to radius, perpendicular bisector of a chord passes through the centre).",
    key=[r"$(x - a)^2 + (y - b)^2 = r^2$, centre $(a, b)$, radius $r$",
         r"$x^2 + y^2 + 2fx + 2gy + c = 0$ has centre $(-f, -g)$, $r = \sqrt{f^2 + g^2 - c}$",
         r"Tangent at $P$ is perpendicular to the radius at $P$",
         r"Perpendicular bisector of a chord passes through the centre; angle in a semicircle is $90^\circ$",
         r"Line meets circle: substitute, then $b^2 - 4ac$ tells you secant ($>0$), tangent ($=0$), miss ($<0$)"],
    method=["To find a circle through 3 points, intersect two perpendicular bisectors.",
            "For tangent lengths from an external point, use Pythagoras with the radius.",
            "To check if a point is inside, compare its distance from the centre with $r$."],
    traps=["Forgetting to square root $r^2$.", "Sign errors when completing the square: $(x - 3)^2$ means centre $x = +3$."],
    exam="Paper 1 or 2, 6-10 marks: often centre/radius then a tangent or an intersection with a line.")

N["2.1"] = dict(
    summary="Proof (deduction, exhaustion, contradiction, counter-example), algebraic fractions, polynomial division, the factor theorem and partial fractions.",
    key=[r"Even: $2n$; odd: $2n + 1$; consecutive: $n, n + 1$",
         r"Factor theorem: $f(a) = 0 \Leftrightarrow (x - a)$ is a factor; $f\left(\frac{b}{a}\right) = 0 \Leftrightarrow (ax - b)$ is a factor",
         r"$\frac{px + q}{(x - a)(x - b)} \equiv \frac{A}{x - a} + \frac{B}{x - b}$",
         r"Repeated factor: $\frac{\ldots}{(x - a)^2(x - b)} \equiv \frac{A}{x - a} + \frac{B}{(x - a)^2} + \frac{C}{x - b}$",
         r"Improper fraction (degree top $\geq$ degree bottom): divide first"],
    method=["Proof by contradiction: 'Assume the opposite...', reach an impossibility, then conclude.",
            "Partial fractions: multiply by the denominator, substitute the roots, compare coefficients for the rest.",
            "Proofs must end with a conclusion sentence that answers the question."],
    traps=["Proof by example is not a proof.", "Not stating the assumption explicitly in a contradiction proof.",
           "Forgetting the $\\frac{B}{(x - a)^2}$ term for a repeated factor."],
    exam="A proof question appears on nearly every Paper 1/2 (4-5 marks). Partial fractions feed into binomial expansion and integration.")

N["2.2"] = dict(
    summary="Functions: domain/range, composite and inverse functions, the modulus function, and transformations of graphs.",
    key=[r"$fg(x) = f(g(x))$: apply $g$ first",
         r"$f^{-1}$ exists only if $f$ is one-to-one; domain of $f^{-1}$ = range of $f$; $y = f^{-1}(x)$ is the reflection of $y = f(x)$ in $y = x$",
         r"$y = f(x) + a$: up $a$; $\;y = f(x + a)$: left $a$; $\;y = af(x)$: vertical stretch s.f. $a$; $\;y = f(ax)$: horizontal stretch s.f. $\frac{1}{a}$",
         r"$y = |f(x)|$: reflect negative parts up; $\;y = f(|x|)$: reflect the right-hand half in the $y$-axis"],
    method=["Solve $|f(x)| = g(x)$ by sketching both graphs, then solve $f(x) = g(x)$ and $-f(x) = g(x)$ and check each answer.",
            "To find an inverse: write $y = f(x)$, rearrange for $x$, swap letters.",
            "Combined transformations: do changes inside the bracket (horizontal) and outside (vertical) separately."],
    traps=["$f^{-1}(x) \\neq \\frac{1}{f(x)}$.", "$f(x + 2)$ moves the graph left, not right.",
           "Not rejecting modulus solutions that make the right-hand side negative."],
    exam="Functions questions are long (8-12 marks), mixing range, composite, inverse and a modulus sketch.")

N["2.3"] = dict(
    summary="Binomial expansion for positive integer powers (finite) and for any rational power (infinite, valid only for small $x$).",
    key=[r"$(a + b)^n = \sum_{r=0}^{n} \binom{n}{r} a^{n-r} b^r$",
         r"$(1 + x)^n = 1 + nx + \frac{n(n - 1)}{2!}x^2 + \frac{n(n - 1)(n - 2)}{3!}x^3 + \ldots$",
         r"For rational $n$, $(1 + bx)^n$ is valid for $|bx| < 1$, i.e. $|x| < \frac{1}{|b|}$",
         r"$(a + bx)^n = a^n\left(1 + \frac{b}{a}x\right)^n$, valid for $|x| < \frac{a}{|b|}$"],
    method=["Put brackets around the whole term, e.g. $(-3x)^2 = 9x^2$.",
            "For $(a + bx)^n$ take out $a^n$ first, then expand.",
            "With partial fractions: expand each fraction separately; the overall validity is the narrower interval."],
    traps=["Forgetting to raise $a$ to the power $n$ when factoring out.", "Not stating the range of validity.",
           "Sign errors with negative $n$: $(1 - x)^{-1} = 1 + x + x^2 + \\ldots$"],
    exam="4-6 marks; often followed by 'use your expansion to estimate...' with a substitution.")

N["2.4"] = dict(
    summary="Exponentials and logarithms: laws of logs, solving equations, $e^x$ and $\\ln x$, growth/decay models and reducing curves to straight lines.",
    key=[r"$\log_a x = n \Leftrightarrow a^n = x$",
         r"$\log_a(xy) = \log_a x + \log_a y$, $\;\log_a\frac{x}{y} = \log_a x - \log_a y$, $\;\log_a x^k = k\log_a x$",
         r"$\frac{d}{dx}e^{kx} = ke^{kx}$, $\;\ln(e^x) = x$, $\;e^{\ln x} = x$",
         r"$y = ab^x \Rightarrow \log y = \log a + x\log b$ (plot $\log y$ against $x$)",
         r"$y = ax^n \Rightarrow \log y = \log a + n\log x$ (plot $\log y$ against $\log x$)"],
    method=["Solve $a^x = b$ by taking logs: $x = \\frac{\\ln b}{\\ln a}$.",
            "For $e^{2x} - 5e^x + 6 = 0$ use $u = e^x$.",
            "In models $N = Ae^{kt}$: $A$ is the initial value; use one data point to find $k$."],
    traps=["$\\log(x + y) \\neq \\log x + \\log y$.", "Forgetting to reject $\\ln$ of a negative number.",
           "Leaving the answer in the wrong form (exact vs 3 s.f.)."],
    exam="Modelling questions (8-10 marks) are common in Paper 2; log-linear graphs appear regularly.")

N["3.1"] = dict(
    summary="Arithmetic and geometric sequences and series, sum to infinity, sigma notation, recurrence relations and modelling with series.",
    key=[r"AP: $u_n = a + (n - 1)d$, $\;S_n = \frac{n}{2}(2a + (n - 1)d) = \frac{n}{2}(a + l)$",
         r"GP: $u_n = ar^{n-1}$, $\;S_n = \frac{a(1 - r^n)}{1 - r}$, $\;S_\infty = \frac{a}{1 - r}$ for $|r| < 1$",
         r"$\sum_{r=1}^{n} 1 = n$; a sum of a linear expression is an arithmetic series",
         r"Recurrence $u_{n+1} = f(u_n)$: increasing if $u_{n+1} > u_n$ for all $n$; periodic if terms repeat"],
    method=["For 'find the first $n$ such that...', form an inequality and use logs (GP) or a quadratic (AP).",
            "Count terms carefully: $\\sum_{r=5}^{20}$ has 16 terms.",
            "In money problems, check whether the first year is $n = 1$ or $n = 0$."],
    traps=["Using $S_\\infty$ when $|r| \\geq 1$.", "Rounding $n$ down when the question needs the first value exceeding a target."],
    exam="Paper 1 or 2, 6-10 marks; modelling contexts (salaries, savings, running distance) are popular.")

N["3.2"] = dict(
    summary="Radians, arcs and sectors, small angle approximations, sec/cosec/cot, Pythagorean identities and inverse trig functions.",
    key=[r"$\pi$ rad $= 180^\circ$; arc $s = r\theta$, sector $A = \frac{1}{2}r^2\theta$, segment $= \frac{1}{2}r^2(\theta - \sin\theta)$",
         r"Small $\theta$ (radians): $\sin\theta \approx \theta$, $\;\tan\theta \approx \theta$, $\;\cos\theta \approx 1 - \frac{\theta^2}{2}$",
         r"$\sec x = \frac{1}{\cos x}$, $\;\mathrm{cosec}\, x = \frac{1}{\sin x}$, $\;\cot x = \frac{1}{\tan x}$",
         r"$1 + \tan^2 x = \sec^2 x$, $\;1 + \cot^2 x = \mathrm{cosec}^2 x$",
         r"$\arcsin$: $[-1, 1] \to [-\frac{\pi}{2}, \frac{\pi}{2}]$; $\arccos$: $[-1, 1] \to [0, \pi]$; $\arctan$: $\mathbb{R} \to (-\frac{\pi}{2}, \frac{\pi}{2})$"],
    method=["Set calculators to radians whenever $\\pi$ or arc/sector formulas appear.",
            "Equations with $\\sec^2$ and $\\tan$: replace $\\sec^2 x$ by $1 + \\tan^2 x$ to get a quadratic in $\\tan x$.",
            "Small angle: substitute, simplify, ignore powers of $\\theta$ above the one asked for."],
    traps=["Using degrees in $r\\theta$.", "Missing solutions from the second quadrant (CAST).",
           "Small angle approximations only work in radians."],
    exam="Sector/segment questions are 5-7 marks; trig equations with identities appear on every paper.")

N["3.3"] = dict(
    summary="Addition and double angle formulae, the harmonic form $R\\cos(x \\pm \\alpha)$, solving trig equations and proving identities, with modelling applications.",
    key=[r"$\sin(A \pm B) = \sin A\cos B \pm \cos A\sin B$",
         r"$\cos(A \pm B) = \cos A\cos B \mp \sin A\sin B$, $\;\tan(A \pm B) = \frac{\tan A \pm \tan B}{1 \mp \tan A\tan B}$",
         r"$\sin 2A = 2\sin A\cos A$, $\;\cos 2A = \cos^2 A - \sin^2 A = 2\cos^2 A - 1 = 1 - 2\sin^2 A$",
         r"$a\cos x + b\sin x = R\cos(x - \alpha)$ with $R = \sqrt{a^2 + b^2}$, $\tan\alpha = \frac{b}{a}$",
         r"Maximum of $R\cos(x - \alpha)$ is $R$ when $x = \alpha$; minimum $-R$"],
    method=["Solving $\\sin(2x + 30^\\circ) = k$: transform the interval first ($30 \\leq 2x + 30 < 750$), find all angles, then undo.",
            "Proofs: start from the more complicated side; convert everything to $\\sin$ and $\\cos$ if stuck.",
            "Harmonic form: expand $R\\cos(x - \\alpha)$, compare coefficients, divide to get $\\tan\\alpha$."],
    traps=["Dividing by $\\sin x$ or $\\cos x$ and losing solutions (factorise instead).",
           "Giving $\\alpha$ in degrees when the question works in radians (or vice versa)."],
    exam="The $R$-form question is a Paper 2 regular (8-10 marks) often with a modelling part (tides, Ferris wheels, temperature).")

N["3.4"] = dict(
    summary="Parametric equations: converting to Cartesian form, sketching, finding intersections, and modelling motion with a parameter.",
    key=[r"Eliminate $t$: make $t$ the subject of one equation and substitute",
         r"Trig parameters: use $\sin^2 t + \cos^2 t = 1$, $\;\sec^2 t = 1 + \tan^2 t$, $\;\cos 2t = 1 - 2\sin^2 t$",
         r"$x = a\cos t + p$, $y = a\sin t + q$ is the circle $(x - p)^2 + (y - q)^2 = a^2$",
         r"The domain of the Cartesian equation comes from the range of $x(t)$"],
    method=["For intersections with a line, substitute $x(t)$ and $y(t)$ into the line and solve for $t$.",
            "For axis crossings, set $x(t) = 0$ or $y(t) = 0$.",
            "In modelling, interpret $t$ (often time) and check the realistic range of $t$."],
    traps=["Forgetting to state the domain/range restrictions.", "Only giving $t$ values when coordinates are asked for."],
    exam="Paper 2, 6-10 marks; often joined with parametric differentiation or integration.")

N["4.1"] = dict(
    summary="Differentiation from first principles, standard derivatives, chain/product/quotient rules, implicit and parametric differentiation, stationary points, tangents, optimisation and rates of change.",
    key=[r"$f'(x) = \lim_{h \to 0}\frac{f(x + h) - f(x)}{h}$",
         r"$\frac{d}{dx}x^n = nx^{n-1}$, $\;\frac{d}{dx}e^{kx} = ke^{kx}$, $\;\frac{d}{dx}\ln x = \frac{1}{x}$, $\;\frac{d}{dx}a^x = a^x\ln a$",
         r"$\frac{d}{dx}\sin kx = k\cos kx$, $\;\frac{d}{dx}\cos kx = -k\sin kx$, $\;\frac{d}{dx}\tan kx = k\sec^2 kx$",
         r"Chain: $\frac{dy}{dx} = \frac{dy}{du}\frac{du}{dx}$; product: $u'v + uv'$; quotient: $\frac{vu' - uv'}{v^2}$",
         r"Parametric: $\frac{dy}{dx} = \frac{dy/dt}{dx/dt}$; implicit: $\frac{d}{dx}y^2 = 2y\frac{dy}{dx}$",
         r"Concave: $f''(x) < 0$; convex: $f''(x) > 0$; point of inflection: $f''$ changes sign"],
    method=["Stationary points: solve $f'(x) = 0$, then test with $f''(x)$ (or the gradient either side).",
            "Tangent: $y - y_1 = f'(x_1)(x - x_1)$; normal uses $-\\frac{1}{f'(x_1)}$.",
            "Connected rates: chain the known rate with a derivative from a formula, e.g. $\\frac{dr}{dt} = \\frac{dV}{dt} \\div \\frac{dV}{dr}$.",
            "Optimisation: write the quantity in one variable using the constraint, differentiate, set to 0, justify max/min."],
    traps=["Using degrees in trig derivatives (must be radians).", "Forgetting $\\frac{dy}{dx}$ on $y$ terms in implicit differentiation.",
           "Not justifying the nature of a stationary point when asked."],
    exam="The largest topic on Papers 1 and 2: expect 15-25 marks per paper across several questions.")

N["4.2"] = dict(
    summary="Integration: standard integrals, $f(ax + b)$, reverse chain rule, trig identities, substitution, parts, partial fractions, areas, the trapezium rule and differential equations.",
    key=[r"$\int x^n\,dx = \frac{x^{n+1}}{n + 1} + c\;(n \neq -1)$, $\;\int \frac{1}{x}\,dx = \ln|x| + c$",
         r"$\int e^{kx}\,dx = \frac{1}{k}e^{kx} + c$, $\;\int \cos kx\,dx = \frac{1}{k}\sin kx + c$, $\;\int \sin kx\,dx = -\frac{1}{k}\cos kx + c$",
         r"$\int \frac{f'(x)}{f(x)}\,dx = \ln|f(x)| + c$",
         r"By parts: $\int u\frac{dv}{dx}\,dx = uv - \int v\frac{du}{dx}\,dx$",
         r"Trapezium rule: $\int_a^b y\,dx \approx \frac{h}{2}[y_0 + y_n + 2(y_1 + \ldots + y_{n-1})]$",
         r"Separable: $\frac{dy}{dx} = f(x)g(y) \Rightarrow \int \frac{1}{g(y)}\,dy = \int f(x)\,dx$"],
    method=["Choose $u$ in parts as the thing that gets simpler when differentiated (LATE: Logs, Algebra, Trig, Exponentials); with $\\ln x$, always $u = \\ln x$.",
            "Substitution: change $dx$ and the limits; never mix $x$ and $u$.",
            "Areas below the $x$-axis come out negative; split the integral at the roots.",
            "Area between curves: $\\int (\\text{top} - \\text{bottom})\\,dx$."],
    traps=["Forgetting $+ c$ (or the modulus in $\\ln|x|$).", "Not changing limits in a substitution.",
           "Over/underestimate: trapezium rule overestimates for convex curves."],
    exam="Expect at least one 8-12 mark integration question per pure paper; DE modelling questions are common in Paper 2.")

N["4.3"] = dict(
    summary="Numerical methods: locating roots by change of sign, fixed-point iteration (and its staircase/cobweb diagrams), and the Newton-Raphson method.",
    key=[r"If $f$ is continuous on $[a, b]$ and $f(a)f(b) < 0$, there is a root in $(a, b)$",
         r"Iteration $x_{n+1} = g(x_n)$ converges near the root if $|g'(\alpha)| < 1$",
         r"Staircase when $0 < g'(\alpha) < 1$; cobweb when $-1 < g'(\alpha) < 0$",
         r"Newton-Raphson: $x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$"],
    method=["To show a root is $2.345$ to 3 d.p., check the sign of $f(2.3445)$ and $f(2.3455)$.",
            "Always state 'sign change and $f$ is continuous, so a root lies in the interval'.",
            "Newton-Raphson fails when $f'(x_n) = 0$ (horizontal tangent) or the start is near a turning point."],
    traps=["Forgetting the continuity statement.", "Rounding iterates too early.", "Using degrees in trig iterations."],
    exam="Paper 2, 5-8 marks; often the end of a calculus or modelling question.")

N["4.4"] = dict(
    summary="Vectors in 2D and 3D: magnitude and direction, position vectors, distances, geometric problems (parallel, collinear, ratios) and vectors in mechanics.",
    key=[r"$|a\mathbf{i} + b\mathbf{j} + c\mathbf{k}| = \sqrt{a^2 + b^2 + c^2}$; unit vector $\hat{\mathbf{a}} = \frac{\mathbf{a}}{|\mathbf{a}|}$",
         r"$\overrightarrow{AB} = \mathbf{b} - \mathbf{a}$; midpoint $\frac{1}{2}(\mathbf{a} + \mathbf{b})$",
         r"Angle with the $x$-axis: $\cos\theta_x = \frac{a}{|\mathbf{v}|}$ (similarly for $y$, $z$)",
         r"Parallel vectors are scalar multiples; collinear points share a point and a parallel direction"],
    method=["For a parallelogram $ABCD$: $\\overrightarrow{AD} = \\overrightarrow{BC}$.",
            "For ratio problems, write a path in two ways and compare coefficients of non-parallel vectors.",
            "In mechanics, resultant force $= m\\mathbf{a}$; speed is the magnitude of velocity."],
    traps=["$\\overrightarrow{AB} = \\mathbf{b} - \\mathbf{a}$, not $\\mathbf{a} - \\mathbf{b}$.", "Confusing position vector with displacement."],
    exam="Short 4-6 mark questions in pure; vector kinematics and forces in Paper 3 mechanics.")

N["5.1"] = dict(
    summary="Statistics (Paper 3 Section A): sampling, data presentation, the large data set, probability, binomial and normal distributions, regression/correlation and hypothesis testing.",
    key=[r"$X \sim \mathrm{B}(n, p)$: $\mathrm{P}(X = r) = \binom{n}{r}p^r(1 - p)^{n-r}$, mean $np$, variance $np(1 - p)$",
         r"$X \sim \mathrm{N}(\mu, \sigma^2)$: $Z = \frac{X - \mu}{\sigma} \sim \mathrm{N}(0, 1)$",
         r"Normal approximation to $\mathrm{B}(n, p)$: $\mathrm{N}(np, np(1 - p))$ with continuity correction",
         r"$\bar{X} \sim \mathrm{N}\left(\mu, \frac{\sigma^2}{n}\right)$ for a sample mean",
         r"$\mathrm{P}(A \mid B) = \frac{\mathrm{P}(A \cap B)}{\mathrm{P}(B)}$; independent iff $\mathrm{P}(A \cap B) = \mathrm{P}(A)\mathrm{P}(B)$",
         r"$\sigma^2 = \frac{\sum x^2}{n} - \bar{x}^2$; outlier rule: beyond $Q_1 - 1.5\,\mathrm{IQR}$ or $Q_3 + 1.5\,\mathrm{IQR}$"],
    method=["Hypothesis test template: hypotheses (parameter!), distribution under $\\mathrm{H}_0$, probability or critical region, compare, conclusion in context.",
            "Critical region: find the largest/smallest value whose tail probability is below the significance level.",
            "Histograms: frequency density = frequency $\\div$ class width; area represents frequency."],
    traps=["Writing hypotheses with $\\bar{x}$ or $X$ instead of $p$, $\\mu$ or $\\rho$.", "Conclusions with no context or that 'prove' something.",
           "Forgetting the continuity correction.", "Not knowing the large data set (stations, variables, 'tr', 'n/a')."],
    exam="Paper 3 Section A is 50 marks: around 5 questions mixing the topics above.")

N["5.2"] = dict(
    summary="Mechanics (Paper 3 Section B): modelling, kinematics (suvat, graphs, calculus, vectors), forces and Newton's laws, friction, connected particles, moments and projectiles.",
    key=[r"$v = u + at$, $\;s = ut + \frac{1}{2}at^2$, $\;s = vt - \frac{1}{2}at^2$, $\;v^2 = u^2 + 2as$, $\;s = \frac{1}{2}(u + v)t$",
         r"$v = \frac{dr}{dt}$, $\;a = \frac{dv}{dt}$; $\;r = \int v\,dt$, $\;v = \int a\,dt$",
         r"$\mathbf{F} = m\mathbf{a}$; weight $= mg$ with $g = 9.8$ m s$^{-2}$",
         r"Friction $F \leq \mu R$; limiting equilibrium/moving: $F = \mu R$",
         r"Moment = force $\times$ perpendicular distance; equilibrium: resultant force 0 and total moment 0",
         r"Projectiles: horizontal $x = U\cos\alpha\, t$; vertical $y = U\sin\alpha\, t - \frac{1}{2}gt^2$"],
    method=["Draw a force diagram for every body; resolve parallel and perpendicular to the motion.",
            "Connected particles: write $F = ma$ for each particle separately (same $a$, same $T$ for a light inextensible string).",
            "Moments: take moments about the point with the most unknown forces."],
    traps=["Using $g = 9.81$ or $10$ instead of $9.8$.", "Giving too many significant figures after using $g = 9.8$ (2 or 3 s.f.).",
           "Forgetting that friction opposes the direction of (potential) motion."],
    exam="Paper 3 Section B is 50 marks; projectiles, connected particles and moments are each worth 8-12 marks.")

if __name__ == "__main__":
    out = Path(__file__).with_name("notes.json")
    out.write_text(json.dumps(N, indent=1, ensure_ascii=False), encoding="utf-8")
    print("wrote", out, len(N), "subtopics")
