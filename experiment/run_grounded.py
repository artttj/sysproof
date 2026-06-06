import argparse
import json
from pathlib import Path

import yaml

from harness.arms import ARMS, arm_prefix
from harness.grader import grade
from harness.results import Row, write_rows
from harness.reuse_check import reused_host_package
from harness.verdict import parse_verdict

ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "tasks_grounded"
HOSTREPO = ROOT / "hostrepo"
SKILL = Path.home() / ".claude/skills/sysproof/SKILL.md"


def load_grounded(task_id):
    d = TASKS / task_id
    meta = yaml.safe_load((d / "meta.yaml").read_text())
    return {
        "id": task_id,
        "trap_family": meta["trap_family"],
        "prompt": (d / "prompt.md").read_text(),
        "hidden_test": (d / "hidden_test.py").read_text(),
    }


def build_cells(reps, prompt_dir):
    prompt_dir.mkdir(parents=True, exist_ok=True)
    skill_text = SKILL.read_text()
    task_ids = sorted(p.name for p in TASKS.iterdir() if p.is_dir())
    cells = []
    for tid in task_ids:
        t = load_grounded(tid)
        for arm in ARMS:
            for rep in range(reps):
                cid = f"{tid}|{arm}|{rep}"
                body = arm_prefix(arm, skill_text) + "\n\n" + t["prompt"]
                (prompt_dir / f"{cid.replace('|', '_')}.txt").write_text(body)
                cells.append({"id": cid, "task": tid, "arm": arm, "rep": rep})
    (ROOT / "grounded_cells.json").write_text(json.dumps(cells, indent=1))
    return cells


def grade_runs(cells_path, runs_path, out_path):
    cells = {c["id"]: c for c in json.loads(Path(cells_path).read_text())}
    runs = json.loads(Path(runs_path).read_text())
    tests = {tid: load_grounded(tid)["hidden_test"] for tid in {c["task"] for c in cells.values()}}
    rows = []
    scratch_root = ROOT / ".scratch_grounded"
    for r in runs:
        cid = r["id"]
        c = cells[cid]
        code = r.get("solution_code", "")
        verdict = parse_verdict(r.get("verdict", "")) or "NOT_DONE"
        gr = grade(code, tests[c["task"]], scratch_root / cid.replace("|", "_"),
                   support_dir=HOSTREPO)
        reused = reused_host_package(code, "newsroom")
        rows.append(Row(
            task=c["task"], arm=c["arm"], rep=c["rep"],
            claimed_done=(verdict == "DONE"),
            actually_passed=gr.actually_passed,
            traps_caught=gr.traps_caught,
            verdict_raw=r.get("verdict", ""),
        ))
        print(f"{cid}: pass={gr.actually_passed} traps={gr.traps_caught} reused={reused}")
    write_rows(rows, Path(out_path))
    print(f"wrote {len(rows)} rows to {out_path}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cells")
    c.add_argument("--reps", type=int, default=10)
    c.add_argument("--prompt-dir", type=Path, default=ROOT / ".cellprompts_grounded")
    g = sub.add_parser("grade")
    g.add_argument("--cells", type=Path, default=ROOT / "grounded_cells.json")
    g.add_argument("--runs", type=Path, required=True)
    g.add_argument("--out", type=Path, default=ROOT / "results_grounded.csv")
    a = ap.parse_args()
    if a.cmd == "cells":
        cells = build_cells(a.reps, a.prompt_dir)
        print(f"wrote {len(cells)} cells and prompts to {a.prompt_dir}")
    else:
        grade_runs(a.cells, a.runs, a.out)


if __name__ == "__main__":
    main()
