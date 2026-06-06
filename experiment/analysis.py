"""Statistics + charts for the sysproof A/B experiment.

Run as a script:  python analysis.py results.csv
Produces console tables and charts/ figures.
"""
import math
import sys
from collections import defaultdict
from pathlib import Path

from scipy.stats import fisher_exact, norm

from harness.results import read_rows, false_done

Z = norm.ppf(0.975)  # 1.959963...


def wilson_ci(events: int, n: int, z: float = Z) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = events / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    lo = 0.0 if events == 0 else max(0.0, center - half)
    hi = 1.0 if events == n else min(1.0, center + half)
    return (lo, hi)


def arr_rrr(p_control: float, p_treat: float) -> tuple[float, float]:
    arr = p_control - p_treat
    rrr = arr / p_control if p_control > 0 else 0.0
    return (arr, rrr)


def false_done_rate_by_arm(rows) -> dict:
    agg = defaultdict(lambda: {"events": 0, "n": 0})
    for r in rows:
        a = agg[r.arm]
        a["n"] += 1
        if false_done(r.claimed_done, r.actually_passed):
            a["events"] += 1
    for a in agg.values():
        a["rate"] = a["events"] / a["n"] if a["n"] else 0.0
        a["ci"] = wilson_ci(a["events"], a["n"])
    return dict(agg)


def fisher_holm(treat, comparators) -> dict:
    """treat=(name,events,n); comparators=list of (name,events,n).

    2x2 per comparison: rows = [treat, comparator], cols = [false_done, ok].
    Holm-correct the p-values across the comparisons.
    """
    t_name, t_ev, t_n = treat
    raw = []
    for c_name, c_ev, c_n in comparators:
        table = [[t_ev, t_n - t_ev], [c_ev, c_n - c_ev]]
        _, p = fisher_exact(table, alternative="two-sided")
        raw.append((c_name, p))
    # Holm: sort ascending, multiply by (m - rank)
    m = len(raw)
    order = sorted(range(m), key=lambda i: raw[i][1])
    out = {}
    prev = 0.0
    for rank, idx in enumerate(order):
        name, p = raw[idx]
        p_holm = min(1.0, p * (m - rank))
        p_holm = max(p_holm, prev)  # enforce monotonicity
        prev = p_holm
        out[name] = {"p_raw": p, "p_holm": p_holm}
    return out


def cluster_bootstrap_diff(rows, arm_a: str, arm_b: str, iters: int = 10000, seed: int = 7):
    """Bootstrap the (arm_a - arm_b) false-done rate difference by resampling TASKS.

    Honest about clustering: reps within a task are not independent, so we resample
    whole tasks with replacement rather than individual runs.
    """
    import random
    rng = random.Random(seed)
    by_task = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by_task[r.task][r.arm].append(false_done(r.claimed_done, r.actually_passed))
    tasks = list(by_task.keys())

    def rate(sample_tasks, arm):
        ev = n = 0
        for t in sample_tasks:
            vals = by_task[t][arm]
            ev += sum(vals)
            n += len(vals)
        return ev / n if n else 0.0

    diffs = []
    for _ in range(iters):
        sample = [rng.choice(tasks) for _ in tasks]
        diffs.append(rate(sample, arm_a) - rate(sample, arm_b))
    diffs.sort()
    lo = diffs[int(0.025 * iters)]
    hi = diffs[int(0.975 * iters)]
    point = rate(tasks, arm_a) - rate(tasks, arm_b)
    return {"diff": point, "ci": (lo, hi)}


def _main(csv_path: str):
    rows = read_rows(Path(csv_path))
    by = false_done_rate_by_arm(rows)
    print("False-done rate by arm:")
    for arm in ("control", "placebo", "sysproof"):
        if arm in by:
            a = by[arm]
            print(f"  {arm:9s} {a['events']:3d}/{a['n']:<3d} = {a['rate']:.1%}  "
                  f"95% CI [{a['ci'][0]:.1%}, {a['ci'][1]:.1%}]")

    if "sysproof" in by and "control" in by:
        comps = [(n, by[n]["events"], by[n]["n"]) for n in ("control", "placebo") if n in by]
        res = fisher_holm(("sysproof", by["sysproof"]["events"], by["sysproof"]["n"]), comps)
        print("\nPairwise vs sysproof (Fisher exact, Holm-corrected):")
        for name, r in res.items():
            arr, rrr = arr_rrr(by[name]["rate"], by["sysproof"]["rate"])
            print(f"  vs {name:9s} p_holm={r['p_holm']:.4g}  ARR={arr:.1%}  RRR={rrr:.0%}")
        print("\nCluster bootstrap (resampling tasks), control - sysproof:")
        cb = cluster_bootstrap_diff(rows, "control", "sysproof")
        print(f"  diff={cb['diff']:.1%}  95% CI [{cb['ci'][0]:.1%}, {cb['ci'][1]:.1%}]")

    _chart(by, Path("charts/false_done_by_arm.png"))
    print("\nChart written to charts/false_done_by_arm.png")


def _chart(by: dict, out: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    arms = [a for a in ("control", "placebo", "sysproof") if a in by]
    rates = [by[a]["rate"] for a in arms]
    errs = [[by[a]["rate"] - by[a]["ci"][0] for a in arms],
            [by[a]["ci"][1] - by[a]["rate"] for a in arms]]
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(arms, rates, yerr=errs, capsize=8, color=["#bbb", "#88a", "#3a7"])
    ax.set_ylabel("False-done rate")
    ax.set_title("False-done rate by arm (95% Wilson CI)")
    for i, r in enumerate(rates):
        ax.text(i, r, f"{r:.0%}", ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(out, dpi=120)


if __name__ == "__main__":
    _main(sys.argv[1] if len(sys.argv) > 1 else "results.csv")
