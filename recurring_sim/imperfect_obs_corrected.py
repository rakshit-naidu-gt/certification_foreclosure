"""
Corrected simulation of Proposition (imperfect observation), matching the model
exactly as stated in files/model.tex: scrutiny p(q) is evaluated at the CURRENT
state q (eq:pt-noisy), and the firm's optimal investment c*(q,p) solves the
ORIGINAL one-period FOC beta*p*|L'(q+f(c)-delta)|*f'(c)=1 with p=p(q,sigma) held
fixed (p does not depend on c here, since it is a function of the pre-investment
state q, not of the post-investment state q'=q+f(c)-delta).

This differs from recurring_sim/imperfect_obs.py, which evaluates p at the
POST-investment state q' and adds an extra |p'(q')|L(q') term to the FOC -- a
different specification not matched by the proposition as written in the paper.

Purpose: determine, for the model actually stated in the paper, whether the
claimed "no cycling for any sigma>0" holds, or whether (as the analytical
correction in math-proof-solo/proof.md predicts) the steady state q**(sigma)
becomes unstable and cycling persists for sufficiently small sigma.
"""
import numpy as np
from scipy.optimize import brentq
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

a, b, beta, delta, tau, p_H = 0.30, 6.80, 0.95, 0.045, 0.80, 1.0
rho = 0.30
p_L = rho * p_H


def pi_smooth(q, sigma):
    x = np.clip(-(q - tau) / sigma, -700, 700)
    return 1.0 / (1.0 + np.exp(x))


def p_of_q(q, sigma):
    return p_H - pi_smooth(q, sigma) * (p_H - p_L)


def foc_residual(c, q, sigma):
    p = p_of_q(q, sigma)
    q2 = q + a * np.sqrt(c) - delta
    q2c = max(q2, -0.999)
    Lp_abs = b / (q2c + 1.0) ** 2
    fp = a / (2 * np.sqrt(c))
    return beta * p * Lp_abs * fp - 1.0


def optimal_c(q, sigma, c_max=50.0):
    lo, hi = 1e-12, c_max
    if foc_residual(hi, q, sigma) > 0:
        hi *= 10
    return brentq(foc_residual, lo, hi, args=(q, sigma), xtol=1e-14, rtol=1e-13)


def simulate(sigma, T=4000, q0=0.30):
    q = q0
    qs = [q]
    for _ in range(T):
        c = optimal_c(q, sigma)
        q = q + a * np.sqrt(c) - delta
        qs.append(q)
    return np.array(qs)


def q_star_closed_form(p):
    return np.sqrt(p * beta * a ** 2 * b / (2 * delta)) - 1.0


def P_of_q(q):
    # P(q) = 1/(beta f'(c_delta) |L'(q)|), the level of p at which q is a fixed point
    c_delta = (delta / a) ** 2
    fp_cdelta = a / (2 * np.sqrt(c_delta))
    Lp_abs = b / (q + 1.0) ** 2
    return 1.0 / (beta * fp_cdelta * Lp_abs)


q_L = q_star_closed_form(p_L)
q_H = q_star_closed_form(p_H)
print(f"q_L=q*(p_L)={q_L:.6f}  q_H=q*(p_H)={q_H:.6f}  tau={tau}")

# find q** for a given sigma by bisection on P(q) = p(q,sigma)
def find_qstar(sigma):
    def resid(q):
        return p_of_q(q, sigma) - P_of_q(q)
    return brentq(resid, q_L + 1e-9, q_H - 1e-9, xtol=1e-13)


def kprime_at(sigma):
    qstar = find_qstar(sigma)
    hstep = max(1e-7, 1e-5 * abs(qstar))

    def k(q):
        c = optimal_c(q, sigma)
        return q + a * np.sqrt(c) - delta

    return (k(qstar + hstep) - k(qstar - hstep)) / (2 * hstep)


# instability threshold: the sigma at which the fixed point's slope k'(q**) crosses -1
sigma_0 = brentq(lambda s: kprime_at(s) + 1.0, 0.004, 0.01, xtol=1e-10)
print(f"\nInstability threshold sigma_0 (k'(q**)=-1): {sigma_0:.6f}  "
      f"(q**(sigma_0)={find_qstar(sigma_0):.6f})\n")

sigmas = sorted([1.0, 0.7, 0.5, 0.3, 0.2, 0.1, 0.07, 0.05, 0.03, 0.02, 0.015, 0.01,
                 sigma_0, 0.006, 0.005, 0.004, 0.003, 0.002, 0.0015, 0.001, 0.0008,
                 0.0006, 0.0005, 0.0003, 0.0002, 0.0001, 0.00005, 0.00002, 0.00001],
                reverse=True)

results = []
for s in sigmas:
    qstar = find_qstar(s)
    kprime = kprime_at(s)
    qs = simulate(s, T=6000, q0=0.30)
    tail = qs[4000:]
    spread = float(tail.max() - tail.min())
    converged = spread < 1e-4
    results.append({
        "sigma": s, "qstar_fixedpoint": qstar, "kprime_at_qstar": kprime,
        "sim_tail_mean": float(tail.mean()), "sim_tail_min": float(tail.min()),
        "sim_tail_max": float(tail.max()), "sim_tail_spread": spread,
        "sim_converged": converged,
    })
    print(f"sigma={s:<10g} q**={qstar:.6f}  k'(q**)={kprime:+8.4f}  "
          f"sim_tail=[{tail.min():.4f},{tail.max():.4f}] mean={tail.mean():.5f}  "
          f"converged={converged}")

with open(os.path.join(HERE, "imperfect_obs_corrected_data.json"), "w") as f:
    json.dump({
        "results": results, "q_L": q_L, "q_H": q_H, "tau": tau,
        "sigma_0": sigma_0, "qstar_at_sigma0": find_qstar(sigma_0),
        "q_star_pH": q_H, "hard_threshold_cycling_mean": 0.8125,
    }, f, indent=1)
print("saved imperfect_obs_corrected_data.json")
