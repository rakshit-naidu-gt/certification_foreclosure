import json
import matplotlib
import os
HERE = os.path.dirname(os.path.abspath(__file__))
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

with open(os.path.join(HERE, "imperfect_obs_corrected_data.json")) as f:
    d = json.load(f)

res = sorted(d["results"], key=lambda x: x["sigma"])
sigmas = np.array([r["sigma"] for r in res])
qstars = np.array([r["qstar_fixedpoint"] for r in res])
converged = np.array([r["sim_converged"] for r in res])
tail_min = np.array([r["sim_tail_min"] for r in res])
tail_max = np.array([r["sim_tail_max"] for r in res])

plt.rcParams.update({
    "font.size": 9,
    "font.family": "serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(3.6, 2.6))

# the (unique) fixed point q**(sigma), stable or not
ax.plot(sigmas, qstars, "-", color="#2a3a8c", lw=1.2, label=r"fixed point $q^{**}(\sigma)$")
ax.plot(sigmas[converged], qstars[converged], "o", color="#2a3a8c", ms=3.5,
        label="stable (sim. converges)")
ax.plot(sigmas[~converged], qstars[~converged], "x", color="#c0522a", ms=4,
        label="unstable (sim. cycles)")

# shade the simulated oscillation band where the fixed point is unstable
ax.fill_between(sigmas[~converged], tail_min[~converged], tail_max[~converged],
                 color="#c0522a", alpha=0.18, linewidth=0)

ax.axvline(d["sigma_0"], color="#555555", lw=0.8, linestyle=":")
ax.text(d["sigma_0"] * 1.15, 0.985, r"$\sigma_0$", fontsize=7.5, color="#444444")

ax.axhline(d["tau"], color="#888888", lw=0.8, linestyle=":")
ax.text(1.5e-5, d["tau"] + 0.006, r"$\tau$", fontsize=7.5, color="#666666")
ax.axhline(d["hard_threshold_cycling_mean"], color="#1baf7a", lw=0.8, linestyle="-.")
ax.text(1.5e-5, d["hard_threshold_cycling_mean"] + 0.012,
        "hard-threshold\ncycling mean", fontsize=5.8, color="#0f8a5c")

ax.set_xscale("log")
ax.set_xlabel(r"observation noise $\sigma$")
ax.set_ylabel(r"quality")
ax.legend(fontsize=5.5, loc="upper left", frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figures", "fig_imperfectobs.pdf"))
plt.close(fig)
print("figure written")
