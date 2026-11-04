import json
import matplotlib
import os
HERE = os.path.dirname(os.path.abspath(__file__))
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open(os.path.join(HERE, "cost_welfare_data.json")) as f:
    d = json.load(f)

plt.rcParams.update({
    "font.size": 9,
    "font.family": "serif",
    "axes.spines.top": False,
})

results = d["results"]
taus = [r["tau"] for r in results]
Ws = [r["W"] for r in results]
Costs = [r["Cost"] for r in results]
cases = [r["case"] for r in results]
colmap = {"A": "#c0522a", "B": "#2a3a8c", "C": "#1baf7a"}

fig, ax1 = plt.subplots(figsize=(3.4, 2.4))
quality_handle = None
for case in ["A", "B", "C"]:
    xs = [t for t, c in zip(taus, cases) if c == case]
    ys = [w for w, c in zip(Ws, cases) if c == case]
    if xs:
        (h,) = ax1.plot(xs, ys, "o-", color=colmap[case], ms=2.5, lw=1.3)
        if quality_handle is None:
            quality_handle = h  # representative handle for the single "quality" legend entry
ax1.axhline(d["q_star_pH"], color="#888888", lw=0.8, linestyle=":")
ax1.set_xlabel(r"threshold $\tau$")
ax1.set_ylabel(r"long-run quality $W(\tau)$")

ax2 = ax1.twinx()
ax2.spines["right"].set_visible(True)
(cost_handle,) = ax2.plot(taus, Costs, "^--", color="#7a2ab0", ms=2.5, lw=1.0, alpha=0.85)
ax2.set_ylabel(r"long-run avg. investment $\mathrm{Cost}(\tau)$", color="#7a2ab0")
ax2.tick_params(axis="y", labelcolor="#7a2ab0")

# Twin axes each autoscale independently, so no in-plot corner is reliably
# clear of both curves (the cost curve's own right-axis scaling can put its
# peak anywhere regardless of the quality axis's range). Placing the legend
# outside the axes entirely, above the plot, sidesteps that.
ax1.legend([quality_handle, cost_handle], ["quality (A/B/C)", "cost"],
           fontsize=6.3, frameon=False, loc="lower center",
           bbox_to_anchor=(0.5, 1.02), ncol=2)

fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figures", "fig_costwelfare.pdf"), bbox_inches="tight")
print("saved figures/fig_costwelfare.pdf")
