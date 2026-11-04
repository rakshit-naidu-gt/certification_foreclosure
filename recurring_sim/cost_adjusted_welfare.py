import numpy as np
from scipy.optimize import brentq
import json
import os
HERE = os.path.dirname(os.path.abspath(__file__))

# Same calibration as sweep_sim.py's SWEEP 2 (regulator's problem, rho=0.30 fixed),
# extended to also track long-run average investment cost, not only quality.
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
    return brentq(foc_residual, lo, hi, args=(q, p), xtol=1e-12)

def q_star(p):
    return np.sqrt(p * beta * a**2 * b / (2*delta)) - 1.0

c_delta = (delta / a)**2  # steady-state investment rate at ANY of the model's steady states

def simulate_recurring(tau, T=400, q0=0.30):
    q = q0
    qs, cs = [q], []
    for t in range(T):
        p = rho * p_H if q >= tau else p_H
        c = optimal_c(q, p)
        cs.append(c)
        q = q + a*np.sqrt(c) - delta
        qs.append(q)
    return qs, cs

qL = q_star(rho * p_H)
qH = q_star(p_H)
print(f"q*(p_L) at rho=0.30: {qL:.4f}, q*(p_H): {qH:.4f}, c_delta (steady-state investment, any regime): {c_delta:.6f}")
print()

tau_grid = np.round(np.arange(0.30, 1.56, 0.05), 2)
results = []
for tau in tau_grid:
    if tau <= qL:
        case = "A"
        W = qL
        Cost = c_delta  # steady state forever, at ANY tau in this flat region
    elif tau <= qH:
        case = "B"
        qs, cs = simulate_recurring(tau, T=800, q0=0.30)
        tail_q = qs[400:]
        tail_c = cs[400:]
        W = float(np.mean(tail_q))
        Cost = float(np.mean(tail_c))
    else:
        case = "C"
        qs, cs = simulate_recurring(tau, T=800, q0=0.30)
        W = float(qs[-1])
        Cost = float(np.mean(cs[400:]))  # converges to c_delta once at q*(p_H)
    results.append({"tau": float(tau), "case": case, "W": W, "Cost": Cost})
    print(f"tau={tau:5.2f}  case={case}  W(tau)={W:.4f}  Cost(tau)={Cost:.6f}")

# ---- Check monotonicity of quality-only W within Case B (sanity check vs. existing fig:tausweep) ----
caseB = [r for r in results if r["case"] == "B"]
W_monotonic = all(caseB[i+1]["W"] >= caseB[i]["W"] - 1e-6 for i in range(len(caseB)-1))
print(f"\nW(tau) (quality only) monotonically non-decreasing within Case B? {W_monotonic}")

# ---- Cost-adjusted welfare W_c(tau) = W(tau) - kappa * Cost(tau), sweep kappa ----
# NOTE: an earlier version of this sweep only tested kappa up to 10.0 and reported
# (in the paper text) that the upper-boundary optimum was robust "for every kappa,
# however large" -- a claim the code never actually tested. Extending the sweep
# well beyond the originally-tested range shows that claim is false: the optimum
# does flip to the *opposite* boundary (tau near q*(p_L), i.e. Case A) once kappa
# is large enough, since the Case A branch is exactly flat in both W and Cost
# (constant qL, c_delta) while Case B's upper edge pays a small Cost premium above
# c_delta for a large W premium -- a tradeoff that only favors quality up to a
# finite kappa. The wider grid below locates that crossover explicitly instead of
# assuming (as the text previously did) that it doesn't exist.
print("\n=== Cost-adjusted welfare W_c(tau) = W(tau) - kappa*Cost(tau) ===")
kappas = [0.0, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0, 500.0, 1000.0, 1500.0, 1600.0, 1700.0, 2000.0, 5000.0]
achievable = [r for r in results if r["tau"] < qH]  # Cases A/B only: tau where certification is ever achieved
crossover_kappa = None
for kappa in kappas:
    Wc = [(r["tau"], r["W"] - kappa * r["Cost"]) for r in achievable]
    argmax_tau, max_Wc = max(Wc, key=lambda x: x[1])
    is_boundary = argmax_tau >= achievable[-1]["tau"] - 1e-9
    if not is_boundary and crossover_kappa is None:
        crossover_kappa = kappa
    print(f"kappa={kappa:7.1f}  argmax tau = {argmax_tau:.2f}  (W_c={max_Wc:.4f})  "
          f"{'[still pushed to Case-B/C boundary]' if is_boundary else '[flipped to the OTHER boundary, Case A]'}")

print(f"\nFirst tested kappa at which the argmax flips away from the upper boundary: "
      f"{crossover_kappa}" if crossover_kappa is not None else
      "\nNo flip found within the tested kappa range.")

with open(os.path.join(HERE, "cost_welfare_data.json"), "w") as f:
    json.dump({
        "results": results, "c_delta": c_delta, "q_star_pL": qL, "q_star_pH": qH,
        "kappas_tested": kappas, "crossover_kappa": crossover_kappa,
    }, f, indent=1)
print("\nsaved cost_welfare_data.json")
