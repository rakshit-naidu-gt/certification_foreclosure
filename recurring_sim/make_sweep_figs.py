import json
import matplotlib
import os
HERE = os.path.dirname(os.path.abspath(__file__))
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open(os.path.join(HERE, "sweep_data.json")) as f:
    d = json.load(f)

plt.rcParams.update({
    "font.size": 9,
    "font.family": "serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# Figure: Sweep 1 (rho, fixed tau=0.8) -- robustness + heterogeneous firms
s1 = d["sweep1_rho"]
rhos = [x["rho"] for x in s1]
qavgs = [x["q_avg"] for x in s1]
cases = [x["case"] for x in s1]
colorsA = "#c0522a"
colorsB = "#2a3a8c"

fig, ax = plt.subplots(figsize=(3.4, 2.4))
rhoA = [r for r, c in zip(rhos, cases) if c == "A"]
qA = [q for q, c in zip(qavgs, cases) if c == "A"]
rhoB = [r for r, c in zip(rhos, cases) if c == "B"]
qB = [q for q, c in zip(qavgs, cases) if c == "B"]
ax.plot(rhoB, qB, "o-", color=colorsB, ms=3, lw=1.3, label="Case B: cycling (time-avg.)")
ax.plot(rhoA, qA, "s-", color=colorsA, ms=3, lw=1.3, label="Case A: sustained")
ax.axvline(d["rho_A_cutoff_tau080"], color="#888888", lw=0.9, linestyle=":")
ax.text(d["rho_A_cutoff_tau080"]+0.02, 0.45, r"$\rho_A(\tau{=}0.8)$", fontsize=7, color="#666666")
ax.axhline(d["tau_default"], color="#aaaaaa", lw=0.7, linestyle="--", zorder=0)
ax.text(0.06, d["tau_default"]+0.03, r"$\tau$", fontsize=7.5, color="#999999")
ax.set_xlabel(r"safe-harbor discount $\rho$")
ax.set_ylabel(r"long-run quality")
ax.legend(fontsize=6.3, frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figures", "fig_rhosweep.pdf"))
plt.close(fig)

# Figure: Sweep 2 (tau, fixed rho=0.30) -- regulator's problem
s2 = d["sweep2_tau"]
taus = [x["tau"] for x in s2]
Ws = [x["W"] for x in s2]
cases2 = [x["case"] for x in s2]

fig, ax = plt.subplots(figsize=(3.4, 2.4))
colmap = {"A": "#c0522a", "B": "#2a3a8c", "C": "#1baf7a"}
for case in ["A", "B", "C"]:
    xs = [t for t, c in zip(taus, cases2) if c == case]
    ys = [w for w, c in zip(Ws, cases2) if c == case]
    if xs:
        ax.plot(xs, ys, "o-", color=colmap[case], ms=2.5, lw=1.3, label=f"Case {case}")
ax.axhline(d["q_star_pH"], color="#888888", lw=0.8, linestyle=":")
ax.text(0.35, d["q_star_pH"]+0.03, r"$q^*(p_H)$", fontsize=7, color="#666666")
ax.set_xlabel(r"threshold $\tau$")
ax.set_ylabel(r"long-run welfare $W(\tau)$")
ax.legend(fontsize=6.5, frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figures", "fig_tausweep.pdf"))
plt.close(fig)
print("both sweep figures written")
