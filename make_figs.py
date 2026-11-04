import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("sim_data.json") as f:
    d = json.load(f)

t_star = d["t_star"]
tau = d["tau"]
t = list(range(len(d["q_foreclosure"])))

plt.rcParams.update({
    "font.size": 9,
    "font.family": "serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# Figure 1: q_t trajectories
fig, ax = plt.subplots(figsize=(3.4, 2.4))
ax.plot(t, d["q_foreclosure"], color="#2a3a8c", lw=1.6, label="Foreclosure model")
ax.plot(t, d["q_ablation"], color="#c0522a", lw=1.6, linestyle="--", label="No-discount ablation")
ax.axhline(tau, color="#888888", lw=0.8, linestyle=":", zorder=0)
ax.text(0.5, tau + 0.03, r"$\tau$", color="#888888", fontsize=8)
ax.axvline(t_star, color="#555555", lw=0.9, linestyle="-", alpha=0.6)
ax.annotate("certified", xy=(t_star, ax.get_ylim()[1] if False else 1.35),
            xytext=(t_star + 1, 1.28), fontsize=7.5, color="#555555")
ax.set_xlabel(r"period $t$")
ax.set_ylabel(r"fairness quality $q_t$")
ax.legend(fontsize=7, frameon=False, loc="lower right")
fig.tight_layout()
fig.savefig("figures/fig_q.pdf")
plt.close(fig)

# Figure 2: c_t trajectories
fig, ax = plt.subplots(figsize=(3.4, 2.4))
ax.plot(t, d["c_foreclosure"], color="#2a3a8c", lw=1.6, label="Foreclosure model")
ax.plot(t, d["c_ablation"], color="#c0522a", lw=1.6, linestyle="--", label="No-discount ablation")
ax.axvline(t_star, color="#555555", lw=0.9, linestyle="-", alpha=0.6)
ax.annotate("certified", xy=(t_star, 0.22),
            xytext=(t_star + 1, 0.20), fontsize=7.5, color="#555555")
ax.set_xlabel(r"period $t$")
ax.set_ylabel(r"investment $c_t$")
ax.legend(fontsize=7, frameon=False, loc="upper right")
fig.tight_layout()
fig.savefig("figures/fig_c.pdf")
plt.close(fig)

print("figures written")
print("q_foreclosure peak at t=%d value=%.4f, final=%.4f" % (t_star, d["q_foreclosure"][t_star], d["q_foreclosure"][-1]))
print("c drop: t=%d->%d : %.4f -> %.4f" % (t_star-1, t_star, d["c_foreclosure"][t_star-1], d["c_foreclosure"][t_star]))
