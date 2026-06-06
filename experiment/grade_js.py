"""Grade the non-Python (Node ESM) requireField run. Input: JSON array of
{model, arm, rep, solution_code, verdict}. Writes each solution as solution.mjs
next to a copy of the host package, runs the hidden test with `node`, and checks
reuse by import. Mirrors the Python grader's contract.
"""
import json
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSDIR = ROOT / "js"
HOST = JSDIR / "newsroom"
TEST = (JSDIR / "hidden_test.mjs").read_text()
REUSE = re.compile(r"""from\s+['"][^'"]*newsroom""")


def reused(code: str) -> bool:
    return bool(REUSE.search(code or ""))


def grade_one(code: str, scratch: Path) -> bool:
    scratch.mkdir(parents=True, exist_ok=True)
    (scratch / "newsroom").mkdir(exist_ok=True)
    shutil.copy(HOST / "errors.mjs", scratch / "newsroom" / "errors.mjs")
    (scratch / "solution.mjs").write_text(code or "")
    (scratch / "hidden_test.mjs").write_text(TEST)
    try:
        r = subprocess.run(["node", "hidden_test.mjs"], cwd=scratch,
                           capture_output=True, timeout=30)
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def main(runs_path: str) -> None:
    runs = json.loads(Path(runs_path).read_text())
    scratch = ROOT / ".scratch_js"
    agg = defaultdict(lambda: {"n": 0, "pass": 0, "reuse": 0})
    rows = ["model,arm,rep,passed,reused"]
    for r in runs:
        code = r.get("solution_code", "") or ""
        cid = f'{r["model"]}_{r["arm"]}_{r["rep"]}'
        p = grade_one(code, scratch / cid)
        ru = reused(code)
        k = (r["model"], r["arm"])
        agg[k]["n"] += 1
        agg[k]["pass"] += int(p)
        agg[k]["reuse"] += int(ru)
        rows.append(f'{r["model"]},{r["arm"]},{r["rep"]},{p},{ru}')
    (ROOT / "results_js.csv").write_text("\n".join(rows) + "\n")
    print(f"\n{'model':8} {'arm':12} {'n':>3}  {'correct':>9}  {'reuse':>8}")
    print("-" * 44)
    for k in sorted(agg):
        a = agg[k]
        n = a["n"]
        print(f"{k[0]:8} {k[1]:12} {n:>3}  {a['pass']:>3}/{n} {100*a['pass']//n:>3}%  "
              f"{a['reuse']:>3}/{n} {100*a['reuse']//n:>3}%")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "js_runs.json")
