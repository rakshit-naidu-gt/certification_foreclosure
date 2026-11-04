"""Sweeps over the discount factor beta and the drift rate delta, holding the
rest of the baseline calibration fixed (a, b, tau=0.80, p_H=1.0, rho=0.30).
Companion to sweep_sim.py's rho- and tau-sweeps: together the four sweeps
(rho, tau, beta, delta) cover every primitive of the baseline calibration
that is not itself a functional-form choice (see functional_form_check.py
for the functional-form robustness check instead).
"""
import numpy as np
from scipy.optimize import brentq
import json
import os
HERE = os.path.dirname(os.path.abspath(__file__))

a, b, tau_default, p_H, rho_default = 0.30, 6.80, 0.80, 1.0, 0.30
beta_default, delta_default = 0.95, 0.045


def make_foc_residual(a, b, delta):
    def foc_residual(c, q, p, beta):
        q2 = q + a * np.sqrt(c) - delta
        q2 = max(q2, -0.999)
        Lp_abs = b / (q2 + 1.0) ** 2
        fp = a / (2 * np.sqrt(c))
        return beta * p * Lp_abs * fp - 1.0
    return foc_residual


def optimal_c(foc_residual, q, p, beta, c_max=50.0):
    lo, hi = 1e-8, c_max
    if foc_residual(hi, q, p, beta) > 0:
        hi *= 10
    return brentq(foc_residual, lo, hi, args=(q, p, beta), xtol=1e-12)


def q_star(p, beta, delta):
    return np.sqrt(p * beta * a**2 * b / (2 * delta)) - 1.0


def simulate_recurring(rho, tau, beta, delta, T=400, q0=0.30):
    foc_residual = make_foc_residual(a, b, delta)
    q = q0
    qs = [q]
    for _ in range(T):
        p = rho * p_H if q >= tau else p_H
        c = optimal_c(foc_residual, q, p, beta)
        q = q + a * np.sqrt(c) - delta
        qs.append(q)
    return qs


def run_sweep(param_name, grid, beta_fn, delta_fn):
    """beta_fn/delta_fn take the swept value and return the (beta, delta) to use."""
    rows = []
    for val in grid:
        beta, delta = beta_fn(val), delta_fn(val)
        qL = q_star(rho_default * p_H, beta, delta)
        qH = q_star(p_H, beta, delta)
        if tau_default <= qL:
            case, qavg = "A", qL
        elif tau_default < qH:
            case = "B"
            qs = simulate_recurring(rho_default, tau_default, beta, delta, T=400)
            qavg = float(np.mean(qs[200:]))
        else:
            case = "C"
            qs = simulate_recurring(rho_default, tau_default, beta, delta, T=400)
            qavg = float(qs[-1])
        rows.append({param_name: float(val), "beta": beta, "delta": delta,
                     "q_star_pL": float(qL), "q_star_pH": float(qH),
                     "case": case, "q_avg": qavg})
        print(f"{param_name}={val:6.4f}  beta={beta:.3f}  delta={delta:.4f}  "
              f"q*(pL)={qL:7.4f}  q*(pH)={qH:7.4f}  case={case}  q_avg={qavg:7.4f}")
    return rows


print("=== SWEEP 3: beta in [0.80, 0.99], delta/tau/rho at baseline ===")
beta_grid = np.round(np.arange(0.80, 0.991, 0.01), 3)
sweep_beta = run_sweep("beta", beta_grid, lambda v: v, lambda v: delta_default)

print("\n=== SWEEP 4: delta in [0.010, 0.090], beta/tau/rho at baseline ===")
delta_grid = np.round(np.arange(0.010, 0.0901, 0.005), 4)
sweep_delta = run_sweep("delta", delta_grid, lambda v: beta_default, lambda v: v)

with open(os.path.join(HERE, "primitives_sweep_data.json"), "w") as f:
    json.dump({"sweep3_beta": sweep_beta, "sweep4_delta": sweep_delta,
                "tau_default": tau_default, "rho_default": rho_default}, f, indent=1)
print("\nsaved primitives_sweep_data.json")
