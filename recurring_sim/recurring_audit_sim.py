import numpy as np
from scipy.optimize import brentq
import json
import os
HERE = os.path.dirname(os.path.abspath(__file__))

a, b, beta, delta, tau, p_H = 0.30, 6.80, 0.95, 0.045, 0.80, 1.0

def foc_residual(c, q, p):
    q2 = q + a*np.sqrt(c) - delta
    q2 = max(q2, -0.999)
    Lp_abs = b / (q2 + 1.0)**2
    fp = a / (2*np.sqrt(c))
    return beta * p * Lp_abs * fp - 1.0

def optimal_c(q, p, c_max=50.0):
    lo, hi = 1e-8, c_max
    if foc_residual(hi, q, p) > 0:
        hi *= 10
    return brentq(foc_residual, lo, hi, args=(q, p), xtol=1e-12)

# Closed-form steady state, including the beta discount factor:
# q*(p) = sqrt(p*beta*a^2*b/(2*delta)) - 1
def q_star_closed_form(p):
    return np.sqrt(p * beta * a**2 * b / (2*delta)) - 1.0

def q_star_numeric(p, q0=0.5, T=2000, tol=1e-9):
    q = q0
    for _ in range(T):
        c = optimal_c(q, p)
        q_next = q + a*np.sqrt(c) - delta
        if abs(q_next - q) < tol:
            return q_next
        q = q_next
    return q

for label, p in [("p_H", p_H), ("p_L (rho=0.30)", 0.30*p_H), ("p_L (rho=0.60)", 0.60*p_H)]:
    cf = q_star_closed_form(p)
    num = q_star_numeric(p)
    print(f"{label}: closed-form q* = {cf:.4f}, numeric fixed-point q* = {num:.4f}, diff = {abs(cf-num):.2e}")

print()
print(f"tau = {tau}")
print(f"Case check rho=0.30: q*(p_L)={q_star_closed_form(0.30):.4f} < tau={tau} <= q*(p_H)={q_star_closed_form(p_H):.4f} -> {q_star_closed_form(0.30) < tau <= q_star_closed_form(p_H)}  [Case B expected]")
print(f"Case check rho=0.60: tau={tau} <= q*(p_L)={q_star_closed_form(0.60):.4f} -> {tau <= q_star_closed_form(0.60)}  [Case A expected]")

def simulate_recurring(rho, T=120, q0=0.30):
    q = q0
    qs, cs, ps, regime = [q], [], [], []
    for t in range(T):
        p = rho*p_H if q >= tau else p_H
        c = optimal_c(q, p)
        q = q + a*np.sqrt(c) - delta
        qs.append(q); cs.append(c); ps.append(p)
        regime.append("shielded" if p < p_H else "exposed")
    return qs, cs, ps, regime

print()
print("=== CASE B (rho=0.30): expect perpetual cycling ===")
qs_b, cs_b, ps_b, reg_b = simulate_recurring(0.30, T=120)
print("last 20 q values:", [round(x,4) for x in qs_b[-20:]])
tail = qs_b[40:]
print(f"tail (t>=40) min={min(tail):.4f} max={max(tail):.4f} mean={np.mean(tail):.4f}")
print(f"q*(p_H) = {q_star_closed_form(p_H):.4f}  -- mean strictly below this? {np.mean(tail) < q_star_closed_form(p_H)}")
# count regime switches in tail to confirm genuine cycling (not converged to a point)
switches = sum(1 for i in range(41, 120) if reg_b[i] != reg_b[i-1])
print(f"number of regime switches after t=40: {switches}  (>0 confirms genuine cycling, not convergence)")

print()
print("=== CASE A (rho=0.60): expect convergence to a sustained steady state >= tau ===")
qs_a, cs_a, ps_a, reg_a = simulate_recurring(0.60, T=120)
print("last 10 q values:", [round(x,4) for x in qs_a[-10:]])
print(f"converged near q*(p_L) = {q_star_closed_form(0.60):.4f}?  last value = {qs_a[-1]:.4f}")
switches_a = sum(1 for i in range(41, 120) if reg_a[i] != reg_a[i-1])
print(f"number of regime switches after t=40 (case A): {switches_a}  (0 confirms settled/no cycling)")

# Save data for figure
data = {
    "tau": tau,
    "q_star_pH": q_star_closed_form(p_H),
    "q_star_pL_030": q_star_closed_form(0.30),
    "q_star_pL_060": q_star_closed_form(0.60),
    "caseB_q": [round(x,4) for x in qs_b],
    "caseB_c": [round(x,4) for x in cs_b],
    "caseA_q": [round(x,4) for x in qs_a],
    "caseA_c": [round(x,4) for x in cs_a],
}
with open(os.path.join(HERE, "recurring_data.json"), "w") as f:
    json.dump(data, f)
print("\ndata saved")

print()
print("=== Closed form vs. numeric fixed point, high precision (T=6000) ===")
for label, p in [("p_H", p_H), ("p_L (rho=0.30)", 0.30), ("p_L (rho=0.60)", 0.60)]:
    cf = q_star_closed_form(p)
    num = q_star_numeric(p, T=6000)
    print(f"{label}: closed-form q* = {cf:.6f}, numeric (T=6000) = {num:.6f}, diff = {abs(cf-num):.2e}")

print()
print("=== Cycle statistics for Case B (rho=0.30), tail t>=60 ===")
tail60 = qs_b[60:]
print(f"min={min(tail60):.4f} max={max(tail60):.4f} mean={np.mean(tail60):.4f}")
print(f"q*(p_H) = {q_star_closed_form(p_H):.4f}")
print(f"mean strictly below q*(p_H)? {np.mean(tail60) < q_star_closed_form(p_H)}")

# estimate cycle period: count period between successive upward regime-switch events (exposed->shielded)
switch_times = [t for t in range(1,120) if reg_b[t]=="shielded" and reg_b[t-1]=="exposed"]
print(f"upward (exposed->shielded) switch times: {switch_times}")
if len(switch_times) >= 3:
    periods = [switch_times[i+1]-switch_times[i] for i in range(len(switch_times)-1)]
    print(f"cycle periods between switches: {periods}")
