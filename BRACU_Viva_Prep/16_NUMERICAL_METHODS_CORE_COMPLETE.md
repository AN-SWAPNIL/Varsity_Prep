# Bismillah.

# Numerical Methods — Core-Complete Viva Recall

> **Source boundary:** no local Numerical Methods slide folder exists in this workspace. This is a standard-core supplement. It focuses on the equations, assumptions, stopping rules, error analysis, and algorithms expected in a CSE viva.

A numerical answer is not only a decimal. A strong answer states:

- the mathematical problem;
- the approximation method;
- assumptions for convergence;
- stopping/error criterion;
- time/space cost and numerical failure modes.

---

# 1. Error, floating point, conditioning, and stability

## 1.1 Error measures

For true value `x` and approximation `x_hat`:

```text
absolute error = |x-x_hat|
relative error = |x-x_hat|/|x|, when x != 0
percentage error = 100 * relative error
```

Absolute error has the unit/scale of the quantity; relative error compares across scales. Near true value zero, relative error is undefined or uninformative, so use an application-appropriate absolute scale.

## 1.2 Round-off and truncation

- **Round-off error:** finite representation/arithmetic.
- **Truncation/discretization error:** replace an infinite/continuous process by finite terms/steps.
- **Data/model error:** input itself is measured/estimated or the mathematical model is approximate.

Smaller step size reduces many truncation errors but can increase round-off/cancellation and computation. “Use the smallest possible `h`” is wrong.

## 1.3 Floating-point model

A normalized binary floating-point number has sign, significand, and exponent. Many decimals such as `0.1` have no finite binary representation.

A standard first-order model is

```text
fl(a op b)=(a op b)(1+delta), |delta|<=u,
```

when no overflow/underflow and the exact result is normal; `u` is unit roundoff. Floating-point addition is not associative:

```text
(a+b)+c may differ from a+(b+c).
```

## 1.4 Catastrophic cancellation

Subtracting nearly equal numbers removes leading significant digits. Example:

```text
sqrt(1+x)-1
```

for small `x` is better evaluated as

```text
x/(sqrt(1+x)+1).
```

The expressions are algebraically identical but numerically different.

## 1.5 Conditioning versus stability

- **Conditioning** belongs to the mathematical problem: how much the exact output changes for small input perturbations.
- **Stability** belongs to the algorithm: whether rounding/intermediate errors are amplified unnecessarily.

For differentiable scalar `y=f(x)`, a local relative condition number is

```text
kappa(x)=|x f'(x)/f(x)|
```

when defined. Roughly, relative output error can be `kappa` times relative input error.

A **backward stable** algorithm returns the exact solution of a nearby input problem. Stability cannot remove sensitivity inherent in an ill-conditioned problem.

## 1.6 Convergence order

If errors satisfy

```text
|e_(k+1)| ≈ C |e_k|^p,
```

then `p=1` is linear, `p=2` quadratic, and `1<p<2` superlinear. The claim is usually local and requires assumptions.

---

# 2. Root finding

We seek `x*` such that `f(x*)=0`.

## 2.1 Bisection

Assume `f` continuous on `[a,b]` and `f(a)f(b)<0`. Repeatedly halve and keep a sign-changing half.

```text
while (b-a)/2 > tolerance:
    m=(a+b)/2
    if f(m)==0: return m
    if f(a)f(m)<0: b=m
    else: a=m
return (a+b)/2
```

After `n` bisections, interval width is `(b-a)/2^n`; midpoint error is at most `(b-a)/2^(n+1)`. To ensure width at most `epsilon`:

```text
n >= ceil(log2((b-a)/epsilon)).
```

Bisection is robust and linearly convergent. It needs a sign-changing bracket and can miss an even-multiplicity root where the sign does not change.

## 2.2 False position (regula falsi)

Keep a sign-changing bracket but choose the x-intercept of the secant:

```text
c = (a f(b)-b f(a))/(f(b)-f(a)).
```

It preserves bracketing but one endpoint can stagnate on strongly curved functions. Illinois/modified methods reduce this issue.

## 2.3 Fixed-point iteration

Rewrite root problem as `x=g(x)` and iterate

```text
x_(k+1)=g(x_k).
```

If `g` maps an interval to itself and `|g'(x)|<=L<1` there, it is a contraction with a unique fixed point and linear convergence. An algebraically valid rearrangement may diverge when `|g'|>1`.

## 2.4 Newton-Raphson

Linearize using the tangent at `x_k`:

```text
0 ≈ f(x_k)+f'(x_k)(x_(k+1)-x_k)
x_(k+1)=x_k-f(x_k)/f'(x_k).
```

For a simple root, sufficient smoothness, nonzero derivative, and a close initial guess, convergence is quadratic. It may diverge, cycle, hit a tiny derivative, or converge to an unintended root.

For a root of multiplicity `m`, ordinary Newton becomes linear; modified Newton

```text
x_(k+1)=x_k-m f(x_k)/f'(x_k)
```

can restore quadratic convergence when `m` is known.

## 2.5 Secant method

Approximate the derivative from two previous points:

```text
x_(k+1)=x_k-f(x_k)(x_k-x_(k-1))/(f(x_k)-f(x_(k-1))).
```

It avoids analytic derivatives and has superlinear order about `1.618`, but is not bracket-preserving and can divide by a tiny difference.

## 2.6 Safe stopping

Use a combination:

```text
|f(x_k)| <= residual_tolerance
|x_k-x_(k-1)| <= abs_tol + rel_tol*|x_k|
```

Declare convergence only when the chosen residual/step tolerance rule passes—commonly require both tests unless there is a justified alternative. The iteration cap is a **failure guard**, not a convergence test:

```text
for k = 1 .. max_iterations:
    compute x_k
    if residual_test AND step_test: return CONVERGED
return NOT_CONVERGED_WITHIN_LIMIT
```

Equivalently, continue only while `iteration < max_iterations`; if the cap is reached without tolerance success, abort and report nonconvergence. A small step does not guarantee a small residual if the iteration stagnates; a small residual may not imply a small x-error near an ill-conditioned root.

---

# 3. Linear systems

Solve `Ax=b`.

## 3.1 Gaussian elimination with partial pivoting

At column `k`, choose the row with largest `|a_ik|` among `i>=k`, swap, then eliminate below.

```text
for k=0..n-2:
    p=argmax_(i=k..n-1) |A[i,k]|
    if A[p,k] approximately 0: singular/rank deficient
    swap rows p,k in A and b
    for i=k+1..n-1:
        m=A[i,k]/A[k,k]
        for j=k+1..n-1: A[i,j]-=m*A[k,j]
        b[i]-=m*b[k]
back substitute
```

Time is `Theta(n^3)`; storage is `Theta(n^2)` in dense form. Partial pivoting limits growth from small pivots and is stable for most practical matrices, though it is not an absolute guarantee for every constructed case.

Do not calculate determinants/inverses to solve a general system when elimination/factorization is available.

## 3.2 LU factorization

Factor `PA=LU` with pivoting, where `L` is lower triangular and `U` upper. Solve:

```text
Ly=Pb   by forward substitution
Ux=y    by back substitution
```

Factorization costs `Theta(n^3)` once; each new right-hand side costs `Theta(n^2)`. Elimination multipliers form `L`.

## 3.3 Cholesky

For a symmetric positive-definite matrix:

```text
A=LL^T
```

Cholesky uses about half the work/storage of general LU and is numerically stable under its assumptions. If the matrix is not positive definite, the square-root pivot can fail.

## 3.4 Residual versus error

Residual is `r=b-A x_hat`; solution error is `e=x-x_hat`. Since

```text
A e = r, e=A^(-1)r,
```

a small residual can coexist with large error when `A` is ill-conditioned. Matrix condition number under a norm is

```text
kappa(A)=||A|| ||A^(-1)||.
```

## 3.5 Jacobi iteration

Split `A=D+L+U`:

```text
x^(k+1)=D^(-1)(b-(L+U)x^k).
```

Each component uses only previous-iteration values, so Jacobi is parallel-friendly.

## 3.6 Gauss-Seidel

Use new components immediately:

```text
(D+L)x^(k+1)=b-Ux^k.
```

It often converges faster than Jacobi but is more sequential. Both converge for strictly diagonally dominant matrices; Gauss-Seidel also converges for symmetric positive-definite matrices. The exact general condition is spectral radius of the iteration matrix `<1`.

Stop using residual norm and an iteration cap, not only component change.

---

# 4. Interpolation

Interpolation passes exactly through given data; regression approximates noisy data.

## 4.1 Lagrange polynomial

For distinct nodes `(x_i,y_i)`, the unique degree at most `n` interpolant is

```text
P_n(x)=sum_(i=0)^n y_i L_i(x)
L_i(x)=product_(j!=i) (x-x_j)/(x_i-x_j).
```

Each basis satisfies `L_i(x_j)=1` when `i=j`, otherwise `0`. Direct evaluation is conceptually simple but rebuilding after a new node is expensive; barycentric form improves numerical evaluation.

## 4.2 Newton divided differences

```text
P_n(x)=f[x0]
      +f[x0,x1](x-x0)
      +...
      +f[x0,...,xn] product_(j=0)^(n-1)(x-x_j).
```

Divided differences:

```text
f[x_i,x_(i+1)] = (f[x_(i+1)]-f[x_i])/(x_(i+1)-x_i)
f[x_i,...,x_(i+k)] =
 (f[x_(i+1),...,x_(i+k)]-f[x_i,...,x_(i+k-1)])/(x_(i+k)-x_i)
```

Adding a node appends one coefficient; nested multiplication evaluates efficiently.

## 4.3 Interpolation error

If `f` has `n+1` derivatives, for some `xi` in the node interval:

```text
f(x)-P_n(x)=f^(n+1)(xi)/(n+1)! * product_(i=0)^n (x-x_i).
```

High-degree equally spaced interpolation can oscillate near endpoints (Runge phenomenon). More points do not automatically improve it; Chebyshev-like nodes or piecewise splines help.

## 4.4 Cubic splines

Fit a cubic on each interval with continuity of value, first derivative, and second derivative at interior knots. Add two boundary conditions:

- natural: endpoint second derivatives zero;
- clamped: endpoint first derivatives specified;
- other not-a-knot/periodic choices.

The coefficient system is tridiagonal and solvable in `O(n)`. Splines give local control and avoid much global oscillation.

---

# 5. Least squares and regression

For overdetermined `Ax≈b`, minimize

```text
||Ax-b||_2^2.
```

Setting gradient zero gives normal equations:

```text
A^T A x = A^T b.
```

For line `y≈a+bx`, the residuals are vertical y-errors. Normal equations are easy but square the condition number roughly; QR factorization is more numerically stable. SVD is robust for rank deficiency and reveals small singular directions, at greater cost.

Regression does not pass through all points. It estimates a model under an error criterion; interpolation assumes exact values at nodes.

---

# 6. Numerical differentiation

Taylor expansion gives finite-difference formulas.

## 6.1 First derivative

Forward:

```text
f'(x) ≈ [f(x+h)-f(x)]/h       error O(h)
```

Backward has `O(h)`. Central:

```text
f'(x) ≈ [f(x+h)-f(x-h)]/(2h)  error O(h^2)
```

## 6.2 Second derivative

```text
f''(x) ≈ [f(x+h)-2f(x)+f(x-h)]/h^2   error O(h^2).
```

Very small `h` causes cancellation/round-off amplification. Higher-order formulas use more samples and may amplify noisy measurement data.

---

# 7. Numerical integration

Approximate `I=int_a^b f(x) dx`.

## 7.1 Trapezoidal rule

Single interval:

```text
T=(b-a)[f(a)+f(b)]/2.
```

Composite with `n` equal subintervals, `h=(b-a)/n`:

```text
T_n=h[ f(x0)/2 + sum_(i=1)^(n-1) f(x_i) + f(x_n)/2 ].
```

For sufficiently smooth `f`, global error is `O(h^2)`; exact error involves `-(b-a)h^2 f''(xi)/12`.

## 7.2 Simpson’s 1/3 rule

Fit a quadratic across two subintervals:

```text
S=(h/3)[f(x0)+4f(x1)+f(x2)].
```

Composite Simpson requires even `n`:

```text
S_n=(h/3)[f(x0)+f(x_n)
    +4 sum_(odd i) f(x_i)
    +2 sum_(even interior i) f(x_i)].
```

Global error is `O(h^4)` under a bounded fourth derivative. Simpson is exact for polynomials through degree 3 despite using quadratic interpolation due to cancellation/symmetry.

## 7.3 Gaussian quadrature

An `n`-point Gauss-Legendre rule chooses nodes/weights to integrate polynomials through degree `2n-1` exactly on `[-1,1]`. Map a general interval with

```text
x=(a+b)/2 + (b-a)t/2,
dx=(b-a)dt/2.
```

Gaussian rules are powerful for smooth functions but do not automatically handle discontinuities/singularities; subdivide or transform appropriately.

## 7.4 Adaptive integration

Compare a coarse estimate with two refined half-interval estimates; subdivide where the discrepancy is too large. Allocate tolerance among children and cap recursion/depth. Adaptive methods focus work where the function is difficult.

---

# 8. Initial-value ODE methods

Solve

```text
y'=f(t,y), y(t0)=y0.
```

## 8.1 Euler method

Use tangent slope at the beginning:

```text
y_(n+1)=y_n+h f(t_n,y_n).
```

Local truncation error is `O(h^2)` per step; global error over a fixed interval is `O(h)`. Euler is simple but can be inaccurate/unstable.

## 8.2 Heun / explicit trapezoid (RK2)

Predict then average slopes:

```text
k1=f(t_n,y_n)
k2=f(t_n+h, y_n+h k1)
y_(n+1)=y_n+h(k1+k2)/2
```

Global order is 2.

## 8.3 Classical RK4

```text
k1=f(t_n,y_n)
k2=f(t_n+h/2, y_n+h k1/2)
k3=f(t_n+h/2, y_n+h k2/2)
k4=f(t_n+h,   y_n+h k3)

y_(n+1)=y_n+h(k1+2k2+2k3+k4)/6
```

Global order is 4 under smoothness assumptions. It evaluates `f` four times per step.

## 8.4 Stability and stiffness

For test equation `y'=lambda y`, Euler gives amplification `1+h lambda`. It is stable only where `|1+h lambda|<1`. A stiff system has rapidly decaying modes that force an explicit method to take tiny stability-limited steps even when the desired solution changes slowly. Implicit methods enlarge the stability region but require solving equations each step.

## 8.5 Adaptive step size

Embedded Runge-Kutta pairs estimate error using two orders from shared stages. If error is too large, reject and reduce `h`; if small, increase it within safety bounds. Control both absolute and relative tolerance per component.

---

# 9. Eigenvalue approximation

## 9.1 Power method

To estimate the dominant eigenvalue/eigenvector:

```text
choose nonzero x
repeat:
    y=A x
    x=y/||y||
    lambda=(x^T A x)/(x^T x)   # Rayleigh quotient
```

If `A` has a unique dominant magnitude eigenvalue and the initial vector has a nonzero component in its eigenvector direction, convergence rate is roughly `|lambda_2/lambda_1|^k` (under diagonalizable/simple assumptions).

It fails/slows when dominant magnitudes tie, the initial component is zero, or eigenvectors/conditioning are problematic. Inverse iteration targets an eigenvalue near a shift but needs repeated linear solves/factorization.

---

# 10. Worked method-selection map

| Problem | Reliable first method | Faster/advanced option | Main trap |
|---|---|---|---|
| Bracketed scalar root | bisection | safeguarded Newton/secant | sign change/continuity assumptions |
| Smooth root, derivative available | Newton | higher-order/safeguarded method | initial guess/tiny derivative |
| Dense linear system | pivoted elimination/LU | QR/SVD as conditioning requires | no-pivot instability |
| SPD linear system | Cholesky | iterative CG for large sparse | verify SPD |
| Smooth interpolation | Newton/barycentric | cubic spline | high-degree equal-node oscillation |
| Noisy curve fit | QR least squares | SVD/regularization | interpolation is wrong goal |
| Smooth integral | composite Simpson | Gaussian/adaptive quadrature | even-n and smoothness |
| Nonstiff ODE | RK4/adaptive RK | embedded high-order | stability/step control |
| Dominant eigenpair | power iteration | Arnoldi/Lanczos/shift-invert | spectral gap |

---

# 11. High-probability viva questions

## “Which is better, bisection or Newton?”

Neither universally. Bisection is slower but guaranteed under a valid bracket/continuity. Newton is locally quadratic but needs derivatives/good initialization and can fail. A hybrid keeps the bracket and takes Newton steps only when safe.

## “Why partial pivoting?”

Dividing by a tiny pivot amplifies round-off and multipliers. Swap in the largest-magnitude available column pivot to reduce that risk; it also detects zero pivot/rank issues.

## “Can residual be small while error is large?”

Yes, for ill-conditioned `A`, because `e=A^(-1)r`. The condition number relates residual/input perturbation to possible solution error.

## “Why central difference is better?”

Taylor expansions from `x+h` and `x-h` cancel the first-order error term, giving `O(h^2)` rather than `O(h)`, at the cost of two-sided samples.

## “Is Simpson always better than trapezoid?”

For sufficiently smooth functions at comparable step size it has higher order, but nonsmoothness, singularities, noisy data, odd interval counts, and cost can change the choice.

## “Why not choose extremely small h?”

Truncation may fall, but round-off/cancellation and step count grow. Total error often has an optimal finite scale.

## “Interpolation versus regression?”

Interpolation exactly matches nodes and assumes them exact; regression minimizes an error criterion for noisy/overdetermined data and normally does not pass through every point.

## “Local versus global ODE error?”

Local truncation error is one step assuming the starting value exact; global error accumulates propagated local errors over many steps. Euler is local `O(h^2)` but global `O(h)`.

---

# 12. Final numerical-methods self-test

- [ ] Distinguish absolute/relative, round-off/truncation, conditioning/stability.
- [ ] Derive and compare bisection, fixed point, Newton, secant, and false position.
- [ ] Calculate bisection iteration count and state safe stopping rules.
- [ ] Perform pivoted elimination, LU solves, and explain Cholesky assumptions.
- [ ] Derive Jacobi/Gauss-Seidel updates and convergence conditions.
- [ ] Build Lagrange/Newton interpolation and state the remainder term.
- [ ] Explain splines, least squares, QR versus normal equations.
- [ ] Derive forward/central differences and the step-size trade-off.
- [ ] Write composite trapezoid/Simpson formulas and error orders.
- [ ] Trace Euler, Heun, and RK4; explain stiffness and stability.
- [ ] Trace the power method and state its spectral-gap assumption.
