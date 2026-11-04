import numpy as np
from scipy.optimize import brentq
import json

a, b, beta, delta, p_H = 0.30, 6.80, 0.95, 0.045, 1.0
rho = 0.30

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
    return brentq(foc_residual, lo, hi, args=(q, p), xtol=1e-13)

def q_star(p):
    return np.sqrt(p * beta * a**2 * b / (2*delta)) - 1.0

q_star_pL = q_star(rho * p_H)
q_star_pH = q_star(p_H)
print(f"q_star(p_L) at rho=0.30 = {q_star_pL:.6f}  <- this is the Case A/B boundary for the tau-sweep")
print(f"q_star(p_H) = {q_star_pH:.6f}  <- this is the Case B/C boundary")
print()

def simulate_recurring(tau, T=8000, q0=None):
    q = q0 if q0 is not None else tau
    qs, regime = [q], []
    for t in range(T):
        p = rho*p_H if q >= tau else p_H
        c = optimal_c(q, p)
        q = q + a*np.sqrt(c) - delta
        qs.append(q)
        regime.append("shielded" if p < p_H else "exposed")
    return qs, regime

print("=== Fine sweep of tau around q*(p_L) boundary (Case A / Case B), tail from t=4000 ===")
deltas = [0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0001]
for d in sorted(deltas, reverse=True):
    tau_below = q_star_pL - d  # Case A: tau <= q*(p_L)
    W_A = q_star_pL  # Case A welfare is always exactly q*(p_L) regardless of tau, per Prop 5
    tau_above = q_star_pL + d  # Case B: tau > q*(p_L)
    qs, regime = simulate_recurring(tau_above, T=8000)
    tail = qs[4000:]
    W_B = float(np.mean(tail))
    print(f"tau={tau_below:.4f} (A, exact W={W_A:.6f})   |   tau={tau_above:.4f} (B, simulated W={W_B:.6f}, tail range [{min(tail):.4f},{max(tail):.4f}])")
