# Certification as Foreclosure — replication code

Code and simulation data supporting *Certification as Foreclosure: A Dynamic
Model of Compliance-Induced Investment Collapse in Algorithmic Audits*.

## Setup

```
pip install -r requirements.txt
```

Requires Python 3.9+ (developed against numpy 2.x / scipy 1.17 / matplotlib
3.10, but any reasonably recent versions listed in `requirements.txt` should
work).

## Reproducing everything

```
python3 recurring_sim/run_all.py
```

regenerates every data file (`*.json`) and every figure (`figures/*.pdf`)
used in the paper, in the correct dependency order, and prints every
numerical claim quoted in the text (steady-state values, kink-condition
checks, slope bounds, robustness sweeps) along the way. Each script can also
be run individually from anywhere — paths are resolved relative to the
script's own location, not the working directory.

## Layout

- `make_figs.py` (repo root) — the single-certification baseline simulation
  (Section 4.0: `fig_q.pdf`, `fig_c.pdf`), reading pre-generated `sim_data.json`.
- `recurring_sim/` — everything for the recurring-audit model (Sections 4.1
  onward) and the regulator's-problem extension (Section 6):

  | Script | Produces | Feeds |
  |---|---|---|
  | `recurring_audit_sim.py` | `recurring_data.json` | `make_recurring_fig.py` → `fig_recurring.pdf` |
  | `sweep_sim.py` | `sweep_data.json` (ρ-sweep and τ-sweep) | `make_sweep_figs.py` → `fig_rhosweep.pdf`, `fig_tausweep.pdf`; also `aggregate_welfare.py` |
  | `imperfect_obs.py` | `imperfect_obs_data.json` | `make_imperfect_obs_fig.py` → `fig_imperfectobs.pdf` |
  | `cost_adjusted_welfare.py` | `cost_welfare_data.json` | `make_cost_welfare_fig.py` → `fig_costwelfare.pdf` |
  | `primitives_sweep.py` | `primitives_sweep_data.json` (β-sweep and δ-sweep) | — (numbers quoted directly in Section 4.2's text) |
  | `boundary_check.py`, `convergence_check.py`, `tau_boundary_check.py`, `functional_form_check.py`, `aggregate_welfare.py` | — (print-only) | verification numbers and the Table~functionalform robustness check quoted in the text |

## What each sweep checks

- **ρ-sweep** (`sweep_sim.py`, Sweep 1): robustness of the Case A/B split and
  the cycling time-average across the safe-harbor discount ρ ∈ [0.05, 0.95];
  also the data source for the heterogeneous-firms and aggregate-welfare
  illustrations.
- **τ-sweep** (`sweep_sim.py`, Sweep 2): the regulator's-problem welfare curve
  W(τ) across the achievable threshold range, ρ = 0.30 fixed.
- **β-sweep and δ-sweep** (`primitives_sweep.py`): robustness of the Case B
  cycling result across the discount factor β ∈ [0.80, 0.99] and the drift
  rate δ ∈ [0.010, 0.090], holding the rest of the baseline calibration fixed.
  δ additionally traces the firm through all three regimes of Theorem 3 as
  it increases, consistent with Corollary `cor:deltacompstat`'s prediction
  that the steady state is strictly decreasing in δ.
- **σ-sweep** (`imperfect_obs.py`): the noisy-detection steady state
  q**(σ) as the logistic noise scale σ varies.
- **Functional-form check** (`functional_form_check.py`): re-runs the four
  central results under a structurally different (f, L) pair.
- **Cost-adjusted welfare** (`cost_adjusted_welfare.py`): tracks long-run
  average investment alongside quality across the τ-sweep, and checks
  whether a cost-penalized welfare objective W(τ) − κ·Cost(τ) ever produces
  an interior optimum, for κ ∈ [0, 1000].

## A note on scope

This release adds portable (`HERE`-relative) paths, the β/δ sweeps, and the
cost-adjusted welfare extension on top of the original calibration exercise;
it does not re-architect the existing scripts into a shared config module —
each script still declares its own copy of the baseline calibration
constants at the top, matching the convention already used throughout this
directory.
