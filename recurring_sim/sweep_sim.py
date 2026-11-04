import numpy as np
from scipy.optimize import brentq
import json
import os
HERE = os.path.dirname(os.path.abspath(__file__))

a, b, beta, delta, tau_default, p_H = 0.30, 6.80, 0.95, 0.045, 0.80, 1.0

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

def q_star(p):
    return np.sqrt(p * beta * a**2 * b / (2*delta)) - 1.0

def simulate_recurring(rho, tau, T=300, q0=0.30):
    q = q0
    qs, regime = [q], []
    for t in range(T):
        p = rho*p_H if q >= tau else p_H
        c = optimal_c(q, p)
        q = q + a*np.sqrt(c) - delta
        qs.append(q)
        regime.append("shielded" if p < p_H else "exposed")
    return qs, regime

# ============ SWEEP 1: over rho, fixed tau=0.8 (feeds robustness analysis + heterogeneous firms) ============
print("=== SWEEP 1: rho in [0.05, 0.95], tau=0.80 fixed ===")
print(f"{'rho':>6} {'q*(rho*pH)':>12} {'case':>6} {'q_avg(tail)':>12}")
rho_grid = np.round(np.arange(0.05, 0.96, 0.05), 2)
sweep1 = []
for rho in rho_grid:
    qL = q_star(rho)
    if tau_default <= qL:
        case = "A"
        qavg = qL  # sustained, converges exactly to qL
    else:
        case = "B"
        qs, regime = simulate_recurring(rho, tau_default, T=300)
        tail = qs[150:]
        qavg = float(np.mean(tail))
    sweep1.append({"rho": float(rho), "q_star_pL": float(qL), "case": case, "q_avg": float(qavg)})
    print(f"{rho:6.2f} {qL:12.4f} {case:>6} {qavg:12.4f}")

qH = q_star(p_H)
rho_A_cutoff = None
# find rho_A(tau) solving q_star(rho*p_H)=tau  =>  rho = tau_arg
# q_star(p)=tau => sqrt(p*beta*a^2*b/(2delta)) - 1 = tau => p = (tau+1)^2 / (beta*a^2*b/(2*delta))
rho_A_cutoff = (tau_default+1)**2 / (beta * a**2 * b / (2*delta)) / p_H
print(f"\nq*(p_H) = {qH:.4f}")
print(f"Closed-form cutoff rho_A(tau=0.80) solving q*(rho*p_H)=tau: rho_A = {rho_A_cutoff:.4f}")

# ============ SWEEP 2: over tau, fixed rho=0.30 (feeds regulator's problem) ============
print()
print("=== SWEEP 2: tau in [0.30, 1.55], rho=0.30 fixed (regulator's problem) ===")
qL_030 = q_star(0.30)
print(f"q*(p_L) at rho=0.30: {qL_030:.4f}, q*(p_H): {qH:.4f}")
tau_grid = np.round(np.arange(0.30, 1.56, 0.05), 2)
sweep2 = []
for tau in tau_grid:
    if tau <= qL_030:
        case = "A"
        W = qL_030
    elif tau <= qH:
        case = "B"
        qs, regime = simulate_recurring(0.30, tau, T=400, q0=0.30)
        tail = qs[200:]
        W = float(np.mean(tail))
    else:
        case = "C"
        qs, regime = simulate_recurring(0.30, tau, T=400, q0=0.30)
        W = float(qs[-1])  # converges to q*(p_H) permanently exposed
    sweep2.append({"tau": float(tau), "case": case, "W": float(W)})
    print(f"tau={tau:5.2f}  case={case}  W(tau)={W:.4f}")

# check monotonicity of W within case B region
caseB_pts = [(s['tau'], s['W']) for s in sweep2 if s['case']=='B']
is_monotonic = all(caseB_pts[i+1][1] >= caseB_pts[i][1] - 1e-6 for i in range(len(caseB_pts)-1))
print(f"\nW(tau) monotonically non-decreasing within Case B region? {is_monotonic}")
print(f"Case B tau range: {caseB_pts[0][0]} to {caseB_pts[-1][0]}")
print(f"W at start of Case B: {caseB_pts[0][1]:.4f}, W at end of Case B: {caseB_pts[-1][1]:.4f}")

with open(os.path.join(HERE, "sweep_data.json"), "w") as f:
    json.dump({
        "sweep1_rho": sweep1, "sweep2_tau": sweep2,
        "q_star_pH": qH, "q_star_pL_030": qL_030,
        "rho_A_cutoff_tau080": rho_A_cutoff,
        "tau_default": tau_default,
    }, f, indent=1)
print("\nsweep data saved")
