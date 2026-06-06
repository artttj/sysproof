"""General grader for cross-arm / cross-model grounded runs.

Usage: grade_grounded.py <runs.json> <task_id>
  runs.json: array of {model?, arm, rep, solution_code, verdict}
  task_id  : a directory name under tasks_grounded/ (e.g. G4-constraint-dedupe)

Groups by (model, arm); reports reuse of the host package, trap-caught (correct),
and all-pass. Writes results_<task_id>.csv.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

from harness.grader import grade
from harness.reuse_check import reused_host_package

ROOT = Path(__file__).resolve().parent
HOSTREPO = ROOT / "hostrepo"


def main(runs_path: str, task_id: str) -> None:
    test = (ROOT / "tasks_grounded" / task_id / "hidden_test.py").read_text()
    runs = json.loads(Path(runs_path).read_text())
    scratch = ROOT / ".scratch_grounded" / task_id
    agg = defaultdict(lambda: {"n": 0, "reuse": 0, "trap": 0, "pass": 0})
    rows = ["model,arm,rep,passed,trap_caught,reused"]
    for r in runs:
        code = r.get("solution_code", "") or ""
        model = r.get("model", "model")
        cid = f'{model}_{r["arm"]}_{r["rep"]}'
        gr = grade(code, test, scratch / cid, support_dir=HOSTREPO)
        reused = reused_host_package(code, "newsroom")
        k = (model, r["arm"])
        agg[k]["n"] += 1
        agg[k]["reuse"] += int(reused)
        agg[k]["trap"] += int(gr.traps_caught)
        agg[k]["pass"] += int(gr.actually_passed)
        rows.append(f'{model},{r["arm"]},{r["rep"]},{gr.actually_passed},{gr.traps_caught},{reused}')
    (ROOT / f"results_{task_id}.csv").write_text("\n".join(rows) + "\n")

    print(f"\n{task_id}")
    print(f"{'model':8} {'arm':22} {'n':>3}  {'reuse':>8}  {'correct(trap)':>14}  {'all-pass':>9}")
    print("-" * 72)
    for k in sorted(agg):
        a = agg[k]
        n = a["n"]
        print(f"{k[0]:8} {k[1]:22} {n:>3}  "
              f"{a['reuse']:>3}/{n} {100*a['reuse']//n:>3}%  "
              f"{a['trap']:>3}/{n} {100*a['trap']//n:>3}%   "
              f"{a['pass']:>3}/{n}")
    print(f"\nwrote results_{task_id}.csv")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
