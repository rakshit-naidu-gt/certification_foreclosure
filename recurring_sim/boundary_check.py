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
    return brentq(foc_residual, lo, hi, args=(q, p), xtol=1e-13)

def q_star(p):
    return np.sqrt(p * beta * a**2 * b / (2*delta)) - 1.0

# exact closed-form cutoff
rho_A = (tau + 1)**2 / (beta * a**2 * b / (2*delta)) / p_H
print(f"Exact closed-form rho_A(tau=0.80) = {rho_A:.6f}")
print(f"Check: q_star(rho_A * p_H) = {q_star(rho_A):.6f}  (should equal tau={tau})")
print()

def simulate_recurring(rho, T=8000, q0=None):
    q = q0 if q0 is not None else tau  # start AT tau to minimize transient
    qs, regime = [q], []
    for t in range(T):
        p = rho*p_H if q >= tau else p_H
        c = optimal_c(q, p)
        q = q + a*np.sqrt(c) - delta
        qs.append(q)
        regime.append("shielded" if p < p_H else "exposed")
    return qs, regime

# Fine sweep right around rho_A, both sides
print("=== FINE SWEEP around rho_A, long horizon (T=8000, tail from t=4000) ===")
print(f"{'rho':>10} {'side':>6} {'W(rho) or q*(rho pH)':>22}")

deltas = [0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002, 0.0001]
results = []
for d in sorted(deltas, reverse=True):
    rho_below = rho_A - d
    qs, regime = simulate_recurring(rho_below, T=8000)
    tail = qs[4000:]
    W_below = float(np.mean(tail))
    tail_min, tail_max = min(tail), max(tail)
    results.append({"rho": rho_below, "side": "B (below)", "W": W_below, "min": tail_min, "max": tail_max})
    print(f"{rho_below:10.4f} {'B':>6} {W_below:22.6f}   (tail range [{tail_min:.4f}, {tail_max:.4f}])")

    rho_above = rho_A + d
    W_above = q_star(rho_above)  # exact closed form in Case A
    results.append({"rho": rho_above, "side": "A (above)", "W": W_above})
    print(f"{rho_above:10.4f} {'A':>6} {W_above:22.6f}   (closed-form exact)")

print()
print(f"Limit from below (smallest d={min(deltas)}): W = {[r['W'] for r in results if r['side']=='B (below)' and abs(r['rho']-(rho_A-min(deltas)))<1e-9][0]:.6f}")
print(f"Limit from above (smallest d={min(deltas)}): W = {[r['W'] for r in results if r['side']=='A (above)' and abs(r['rho']-(rho_A+min(deltas)))<1e-9][0]:.6f}")
print(f"tau = {tau}")

with open(os.path.join(HERE, "boundary_data.json"), "w") as f:
    json.dump({"rho_A": rho_A, "tau": tau, "results": results}, f, indent=1)
