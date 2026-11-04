import numpy as np
from scipy.optimize import brentq

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

rho_A = (tau + 1)**2 / (beta * a**2 * b / (2*delta)) / p_H
rho = rho_A - 0.0001  # the smallest gap from before

def simulate(T, q0=tau):
    q = q0
    qs = [q]
    for t in range(T):
        p = rho*p_H if q >= tau else p_H
        c = optimal_c(q, p)
        q = q + a*np.sqrt(c) - delta
        qs.append(q)
    return qs

# check the running time-average at increasing horizons, using progressively later tails
qs = simulate(200000)
qs = np.array(qs)
for T_end, tail_start in [(8000,4000), (20000,10000), (50000,25000), (100000,50000), (200000,100000)]:
    tail = qs[tail_start:T_end]
    print(f"T={T_end}, tail from {tail_start}: mean={tail.mean():.6f}, min={tail.min():.4f}, max={tail.max():.4f}")

print(f"\ntau = {tau}")
print(f"rho_A - rho = {rho_A - rho:.6f}")
