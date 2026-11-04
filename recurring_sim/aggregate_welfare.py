import json
import numpy as np
import os
HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "sweep_data.json")) as f:
    d = json.load(f)

s1 = d["sweep1_rho"]
rhos = np.array([x["rho"] for x in s1])
qavgs = np.array([x["q_avg"] for x in s1])
cases = [x["case"] for x in s1]
q_star_pH = d["q_star_pH"]

print(f"q_star(p_H) = {q_star_pH:.4f}  (no-safe-harbor benchmark)")
print(f"rho grid: {rhos.min()} to {rhos.max()}, n={len(rhos)}")
print()

# Aggregate welfare under rho_i ~ Uniform(0.05, 0.95), matching the sweep range exactly
# Trapezoidal integration of q_avg(rho) over rho, divided by range = E[W_i]
E_W = np.trapezoid(qavgs, rhos) / (rhos.max() - rhos.min())
welfare_loss = q_star_pH - E_W
pct_loss = 100 * welfare_loss / q_star_pH

print("=== Aggregate welfare under rho_i ~ Uniform(0.05, 0.95) ===")
print(f"E[W_i] (population average long-run quality) = {E_W:.4f}")
print(f"No-safe-harbor benchmark q*(p_H) = {q_star_pH:.4f}")
print(f"Aggregate welfare loss = {welfare_loss:.4f} ({pct_loss:.1f}% of benchmark)")

# Fraction of firms in each case
rho_A = d["rho_A_cutoff_tau080"]
frac_caseB = (rho_A - rhos.min()) / (rhos.max() - rhos.min())
frac_caseA = 1 - frac_caseB
print()
print(f"rho_A cutoff = {rho_A:.4f}")
print(f"Fraction of firms in Case B (cycling): {frac_caseB*100:.1f}%")
print(f"Fraction of firms in Case A (sustained): {frac_caseA*100:.1f}%")

# Also compute for a second, more realistic distribution: Beta-like skew toward higher rho
# (most firms have modest safe-harbor effects, few have very strong ones) - Beta(4,2) rescaled to (0.05,0.95)
from scipy.stats import beta as beta_dist
xs = np.linspace(0.05, 0.95, 500)
# interpolate qavgs onto fine grid
qavgs_fine = np.interp(xs, rhos, qavgs)
weights = beta_dist.pdf((xs-0.05)/0.9, 4, 2) / 0.9
weights /= np.trapezoid(weights, xs)  # normalize
E_W_beta = np.trapezoid(qavgs_fine * weights, xs)
welfare_loss_beta = q_star_pH - E_W_beta
pct_loss_beta = 100 * welfare_loss_beta / q_star_pH
frac_caseB_beta = np.trapezoid(weights[xs < rho_A], xs[xs < rho_A])

print()
print("=== Robustness: rho_i ~ Beta(4,2) rescaled to (0.05,0.95), skewed toward WEAKER safe-harbor effect (higher rho) ===")
print(f"E[W_i] = {E_W_beta:.4f}, welfare loss = {welfare_loss_beta:.4f} ({pct_loss_beta:.1f}%)")
print(f"Fraction of firms in Case B under this distribution: {frac_caseB_beta*100:.1f}%")
