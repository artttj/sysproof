"""Grade the cross-model G3 run. Input: a JSON array of
{model, arm, rep, solution_code, verdict}. Output: a per (model, arm) table of
reuse rate and trap-caught (correct) rate, plus a CSV. Uses the same grader and
reuse check as the main study, with the host package as support_dir.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

from harness.grader import grade
from harness.reuse_check import reused_host_package

ROOT = Path(__file__).resolve().parent
HOSTREPO = ROOT / "hostrepo"
G3_TEST = (ROOT / "tasks_grounded" / "G3-contract-error" / "hidden_test.py").read_text()


def main(runs_path: str) -> None:
    runs = json.loads(Path(runs_path).read_text())
    scratch = ROOT / ".scratch_xmodel"
    agg = defaultdict(lambda: {"n": 0, "reuse": 0, "trap": 0, "pass": 0})
    rows = ["model,arm,rep,passed,trap_caught,reused"]
    for r in runs:
        code = r.get("solution_code", "") or ""
        cid = f'{r["model"]}_{r["arm"]}_{r["rep"]}'
        gr = grade(code, G3_TEST, scratch / cid, support_dir=HOSTREPO)
        reused = reused_host_package(code, "newsroom")
        k = (r["model"], r["arm"])
        agg[k]["n"] += 1
        agg[k]["reuse"] += int(reused)
        agg[k]["trap"] += int(gr.traps_caught)
        agg[k]["pass"] += int(gr.actually_passed)
        rows.append(f'{r["model"]},{r["arm"]},{r["rep"]},{gr.actually_passed},{gr.traps_caught},{reused}')

    out_csv = ROOT / "results_xmodel.csv"
    out_csv.write_text("\n".join(rows) + "\n")

    print(f"\n{'model':8} {'arm':12} {'n':>3}  {'reuse':>8}  {'correct(trap)':>14}  {'all-pass':>9}")
    print("-" * 62)
    for (model, arm) in sorted(agg):
        a = agg[(model, arm)]
        n = a["n"]
        print(f"{model:8} {arm:12} {n:>3}  "
              f"{a['reuse']:>3}/{n} {100*a['reuse']//n:>3}%  "
              f"{a['trap']:>3}/{n} {100*a['trap']//n:>3}%   "
              f"{a['pass']:>3}/{n}")
    print(f"\nwrote {out_csv}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "xmodel_runs.json")
