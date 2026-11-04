import numpy as np
from scipy.optimize import brentq

beta, delta, tau, p_H = 0.95, 0.045, 3.80, 1.0

# Alternative functional forms: f(c) = a*c^(1/3) (cube root, steeper diminishing returns than sqrt)
#                                L(q) = b*exp(-q) (exponential decay, vs original rational decay)
a2, b2 = 0.55, 3.20

def f2(c):
    return a2 * c**(1/3)
def f2p(c):
    return (a2/3) * c**(-2/3)
def L2(q):
    return b2 * np.exp(-q)
def L2p(q):
    return -b2 * np.exp(-q)

# sanity check assumptions: f increasing/concave (f'>0, f''<0), L decreasing/convex (L'<0, L''>0)
cs = np.linspace(0.001, 5, 50)
assert all(f2p(c) > 0 for c in cs), "f' not positive"
fpp = lambda c: -(2*a2/9)*c**(-5/3)
assert all(fpp(c) < 0 for c in cs), "f'' not negative"
qs_check = np.linspace(-0.5, 3, 50)
assert all(L2p(q) < 0 for q in qs_check), "L' not negative"
Lpp = lambda q: b2*np.exp(-q)
assert all(Lpp(q) > 0 for q in qs_check), "L'' not positive"
print("Assumptions 1-2 verified for f(c)=a*c^(1/3), L(q)=b*exp(-q)")

def foc_residual(c, q, p):
    q2 = q + f2(c) - delta
    return beta * p * (-L2p(q2)) * f2p(c) - 1.0

def optimal_c(q, p, c_max=200.0):
    lo, hi = 1e-9, c_max
    if foc_residual(hi, q, p) > 0:
        hi *= 10
    return brentq(foc_residual, lo, hi, args=(q, p), xtol=1e-12)

p_L_rho03 = 0.30 * p_H

# Check 1: discrete investment collapse at q=tau (Proposition 1 analog)
c_star_H = optimal_c(tau, p_H)
c_star_L = optimal_c(tau, p_L_rho03)
print(f"\n=== Check 1: Discrete investment collapse (Prop 1 analog) ===")
print(f"c*(p_H) = {c_star_H:.4f}, c*(p_L, rho=0.30) = {c_star_L:.4f}")
print(f"c*(p_L) < c*(p_H)? {c_star_L < c_star_H}  (confirms Prop 1's qualitative claim)")

# Check 2: kink condition (Corollary 1 analog): c*(p_L) < delta <= c*(p_H)
print(f"\n=== Check 2: Kink condition (Corollary 1 analog) ===")
f_cH = f2(c_star_H); f_cL = f2(c_star_L)
print(f"f(c*(p_H)) = {f_cH:.4f}, f(c*(p_L)) = {f_cL:.4f}, delta = {delta}")
print(f"CORRECT check: f(c*(p_L)) < delta <= f(c*(p_H))? {f_cL < delta <= f_cH}")

# Check 3: single-certification kink simulation
def simulate_single_cert(rho, T=300, q0=0.30):
    q = q0
    certified = False
    qs, cs_list = [q], []
    for t in range(T):
        if q >= tau and not certified:
            certified = True
        p = rho*p_H if certified else p_H
        c = optimal_c(q, p)
        q = q + f2(c) - delta
        qs.append(q); cs_list.append(c)
    return qs, cs_list

qs, cs_list = simulate_single_cert(0.30, T=300)
peak_t = int(np.argmax(qs))
print(f"\n=== Check 3: Single-certification kink simulation, rho=0.30 ===")
print(f"q0={qs[0]:.4f}, peak q={max(qs):.4f} at t={peak_t}, final q={qs[-1]:.4f}")
print(f"Kink present (peak strictly interior, declines after)? {peak_t < len(qs)-1 and qs[-1] < max(qs)}")

# Check 4: recurring-audit cycling (Proposition 3 Case (b) analog)
def q_star(p, lo=-2, hi=10):
    # solve f(c_delta) = delta for c_delta, then beta*p*|L'(q*)|*f'(c_delta) = 1 for q*
    def cdelta_resid(c):
        return f2(c) - delta
    c_delta = brentq(cdelta_resid, 1e-9, 100)
    fp_cdelta = f2p(c_delta)
    def qstar_resid(q):
        return beta*p*(-L2p(q))*fp_cdelta - 1.0
    return brentq(qstar_resid, lo, hi)

qsH = q_star(p_H)
qsL_03 = q_star(p_L_rho03)
print(f"\n=== Check 4: Recurring-audit cycling (Prop 3 Case (b) analog) ===")
print(f"q*(p_H) = {qsH:.4f}, q*(p_L, rho=0.30) = {qsL_03:.4f}, tau = {tau}")
print(f"Case B condition q*(p_L) < tau <= q*(p_H)? {qsL_03 < tau <= qsH}")

def simulate_recurring(rho, T=300, q0=0.30):
    q = q0
    qs = [q]; regime = []
    for t in range(T):
        p = rho*p_H if q >= tau else p_H
        c = optimal_c(q, p)
        q = q + f2(c) - delta
        qs.append(q)
        regime.append("shielded" if p < p_H else "exposed")
    return qs, regime

qs_rec, regime = simulate_recurring(0.30, T=300)
tail = qs_rec[150:]
switches = sum(1 for i in range(151, 300) if regime[i] != regime[i-1])
print(f"Recurring-audit tail (t>=150): min={min(tail):.4f}, max={max(tail):.4f}, mean={np.mean(tail):.4f}")
print(f"Regime switches in tail: {switches} (>0 confirms genuine cycling under a different functional form)")
print(f"Mean strictly below q*(p_H)={qsH:.4f}? {np.mean(tail) < qsH}")
