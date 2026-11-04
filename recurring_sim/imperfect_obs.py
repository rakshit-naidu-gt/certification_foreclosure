# SUPERSEDED: this script solves the FOC for scrutiny evaluated at the POST-investment
# state q_{t+1} (an extra |p'(q2)|*L(q2) term, see the comment below), which is not the
# specification in the paper's Proposition (imperfect observation): there, scrutiny
# p(q) is a function of the CURRENT state q (eq:pt-noisy), so p does not depend on c
# and the FOC is the original beta*p*|L'(q')|*f'(c)=1. See imperfect_obs_corrected.py,
# which implements the paper's actual model and is what run_all.py now runs; it finds
# that the steady state is unstable and cycling persists below sigma ~ 0.0063 at this
# calibration, contrary to what this script's results suggested. Kept only for
# reference; do not cite its output as verifying the proposition as stated.
import numpy as np
from scipy.optimize import brentq
import os
HERE = os.path.dirname(os.path.abspath(__file__))

a, b, beta, delta, tau, p_H = 0.30, 6.80, 0.95, 0.045, 0.80, 1.0
rho = 0.30
p_L = rho * p_H

def pi_smooth(q, sigma):
    x = np.clip(-(q - tau) / sigma, -700, 700)  # avoid overflow in exp for tiny sigma
    return 1.0 / (1.0 + np.exp(x))

def pi_deriv(q, sigma):
    p = pi_smooth(q, sigma)
    return p * (1.0 - p) / sigma

def p_of_q(q, sigma):
    return p_H - pi_smooth(q, sigma) * (p_H - p_L)

def p_deriv_abs(q, sigma):
    # |p'(q)| = (p_H - p_L) * pi'(q), since p(q) = p_H - pi(q)*(p_H-p_L) and p_H > p_L
    return (p_H - p_L) * pi_deriv(q, sigma)

# CORRECTED first-order condition for the q_{t+1}-based specification, where scrutiny
# is a smooth function of the state the firm's OWN investment produces (p depends on
# q2 = q + f(c) - delta, not on q itself). An earlier version of this script computed
# p at q2 but used the FOC for the exogenous-scrutiny case (beta*p*|L'(q2)|*f'(c) = 1),
# which silently drops a term: since q2 depends on c, differentiating the true
# objective J(c) = c + beta*p(q2)*L(q2) with respect to c via the chain rule gives
#   dJ/dc = 1 + beta*f'(c)*[p'(q2)*L(q2) + p(q2)*L'(q2)]
# so the correct stationarity condition is
#   beta*f'(c)*[p(q2)*|L'(q2)| + |p'(q2)|*L(q2)] = 1
# i.e. an extra |p'(q2)|*L(q2) term capturing the firm's incentive to invest in order
# to reduce its OWN future scrutiny probability, not just to reduce L(q2) directly.
# Omitting this term (as the old FOC did) understates optimal investment whenever
# p'(q2) is non-negligible, which turns out to change both the numbers and the
# qualitative shape of q**(sigma) substantially (see below).
def foc_residual(c, q, sigma):
    q2 = q + a*np.sqrt(c) - delta
    q2c = max(q2, -0.999)
    p = p_of_q(q2c, sigma)
    Lp_abs = b / (q2c + 1.0)**2
    L = b / (q2c + 1.0)
    pdabs = p_deriv_abs(q2c, sigma)
    fp = a / (2*np.sqrt(c))
    return beta * fp * (p * Lp_abs + pdabs * L) - 1.0

def optimal_c(q, sigma, c_max=50.0):
    lo, hi = 1e-9, c_max
    if foc_residual(hi, q, sigma) > 0:
        hi *= 10
    return brentq(foc_residual, lo, hi, args=(q, sigma), xtol=1e-12)

def simulate(sigma, T=4000, q0=0.30):
    q = q0
    qs = [q]
    for t in range(T):
        c = optimal_c(q, sigma)
        q = q + a*np.sqrt(c) - delta
        qs.append(q)
    return qs

def q_star_const(p):
    # closed-form steady state under a CONSTANT scrutiny level p (same formula as
    # recurring_audit_sim.py's q_star_closed_form), used below as the sigma->infinity
    # benchmark: as sigma grows, pi(q) -> 0.5 for any fixed q and pi'(q) -> 0, so the
    # corrected FOC converges to the constant-scrutiny FOC at p = (p_H+p_L)/2.
    return np.sqrt(p * beta * a**2 * b / (2*delta)) - 1.0

print(f"tau={tau}, rho={rho}, p_L={p_L}")
print(f"Discrete-model (sigma->0) cycling mean was 0.8125 (from earlier long-run simulation)")
print(f"Discrete-model q*(p_H) = 1.5417 (no-safe-harbor benchmark)")
p_avg = (p_H + p_L) / 2.0
q_star_avg = q_star_const(p_avg)
print(f"sigma->infinity benchmark: q*((p_H+p_L)/2={p_avg}) = {q_star_avg:.5f}")
print()

# Wide sweep, spanning many orders of magnitude in sigma, to check for cycling
# (rather than assuming, as an earlier version implicitly did by never testing far
# enough, that none occurs). No cycling was found anywhere in this range.
sweep_sigmas = [100000, 10000, 1000, 100, 10, 5, 2, 1.0, 0.8, 0.7, 0.6, 0.575, 0.55,
                0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001,
                0.0005, 0.0002, 0.0001, 0.00005, 0.00002, 0.00001]
results = []
for s in sweep_sigmas:
    qs = simulate(s, T=4000, q0=0.30)
    tail = np.array(qs[2000:])
    spread = float(tail.max() - tail.min())
    converged = spread < 1e-4
    results.append({"sigma": s, "qstar": float(tail.mean()), "spread": spread, "converged": converged})
    print(f"sigma={s:<10} q**={tail.mean():.5f}  spread={spread:.2e}  converged(no cycling)={converged}")

any_cycling = any(not r["converged"] for r in results)
print(f"\nCycling detected anywhere in the swept range? {any_cycling}")

peak = max(results, key=lambda r: r["qstar"])
print(f"Peak: sigma={peak['sigma']}, q**={peak['qstar']:.5f} "
      f"(vs. no-safe-harbor benchmark q*(p_H)=1.5417)")

import json
with open(os.path.join(HERE, "imperfect_obs_data.json"), "w") as f:
    json.dump({
        "results": results, "tau": tau, "q_star_pH": 1.541653, "cycling_mean": 0.8125,
        "q_star_avg_sigma_to_inf": q_star_avg, "p_avg": p_avg,
        "peak_sigma": peak["sigma"], "peak_qstar": peak["qstar"],
        "any_cycling_detected": any_cycling,
    }, f, indent=1)
print("saved")
