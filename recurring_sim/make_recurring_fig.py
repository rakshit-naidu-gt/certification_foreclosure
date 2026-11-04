import json
import matplotlib
import os
HERE = os.path.dirname(os.path.abspath(__file__))
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open(os.path.join(HERE, "recurring_data.json")) as f:
    d = json.load(f)

tau = d["tau"]
t = list(range(len(d["caseB_q"])))

plt.rcParams.update({
    "font.size": 9,
    "font.family": "serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(3.4, 2.4))
ax.plot(t, d["caseB_q"], color="#2a3a8c", lw=1.3, label=r"Case B ($\rho=0.30$): perpetual cycling")
ax.plot(t, d["caseA_q"], color="#c0522a", lw=1.3, linestyle="--", label=r"Case A ($\rho=0.60$): sustained")
ax.axhline(tau, color="#888888", lw=0.8, linestyle=":", zorder=0)
ax.text(60, tau + 0.04, r"$\tau$", color="#888888", fontsize=8)
ax.axhline(d["q_star_pH"], color="#999999", lw=0.7, linestyle="-.", zorder=0)
ax.text(2, d["q_star_pH"] + 0.03, r"$q^*(p_H)$ (no-safe-harbor benchmark)", color="#777777", fontsize=6.3)
ax.set_xlim(0, 120)
# the data never exceeds ~0.97, so extending the axis to 1.65 opens a clear band
# (above the curves, below/around the two reference-line labels) for the legend,
# which previously sat at "center right" directly on top of both plotted lines.
ax.set_ylim(0.2, 1.65)
ax.set_xlabel(r"period $t$")
ax.set_ylabel(r"fairness quality $q_t$")
ax.legend(fontsize=6.3, frameon=False, loc="upper left", bbox_to_anchor=(0.0, 0.80))
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figures", "fig_recurring.pdf"))
plt.close(fig)
print("figure written")
