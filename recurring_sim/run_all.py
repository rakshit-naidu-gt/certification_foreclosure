"""Single entry point: regenerates every data file and figure used by the paper.

Run from anywhere (paths are resolved relative to this script's location):

    python3 recurring_sim/run_all.py

Order matters: each "data" script must run before the "figure" script(s) that
consume its output JSON. Scripts with no downstream figure (boundary_check,
convergence_check, tau_boundary_check, functional_form_check, aggregate_welfare,
primitives_sweep) only print verification numbers quoted in the text, or a
robustness-check table.
"""
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PIPELINE = [
    # -- data-generating scripts (each writes a *_data.json consumed below) --
    "recurring_audit_sim.py",   # -> recurring_data.json
    "sweep_sim.py",             # -> sweep_data.json
    "imperfect_obs_corrected.py",  # -> imperfect_obs_corrected_data.json (see its docstring:
                                    # supersedes imperfect_obs.py, which solved a different,
                                    # unintended FOC and is kept only for reference)
    "cost_adjusted_welfare.py",  # -> cost_welfare_data.json
    # -- figure-generating scripts (each reads the corresponding *_data.json) --
    "make_recurring_fig.py",
    "make_sweep_figs.py",
    "make_imperfect_obs_fig.py",
    "make_cost_welfare_fig.py",
    # -- print-only verification / robustness scripts (no figure output) --
    "boundary_check.py",
    "convergence_check.py",
    "tau_boundary_check.py",
    "functional_form_check.py",
    "aggregate_welfare.py",     # reads sweep_data.json, prints aggregate-welfare numbers
    "primitives_sweep.py",      # -> primitives_sweep_data.json (beta/delta robustness)
]


def main():
    for script in PIPELINE:
        path = os.path.join(HERE, script)
        print(f"\n{'='*70}\nrunning {script}\n{'='*70}")
        result = subprocess.run([sys.executable, path], cwd=HERE)
        if result.returncode != 0:
            print(f"FAILED: {script} exited with code {result.returncode}", file=sys.stderr)
            sys.exit(result.returncode)

    # the two baseline (non-recurring) simulation figures live at the repo root
    repo_root = os.path.dirname(HERE)
    print(f"\n{'='*70}\nrunning make_figs.py (repo root)\n{'='*70}")
    result = subprocess.run([sys.executable, "make_figs.py"], cwd=repo_root)
    if result.returncode != 0:
        print("FAILED: make_figs.py", file=sys.stderr)
        sys.exit(result.returncode)

    print("\nAll data files and figures regenerated successfully.")


if __name__ == "__main__":
    main()
