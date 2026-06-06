"""Build cells, (optionally) ingest workflow output, grade, write results.csv.

Two phases:
  python run_grade.py cells --reps 3 [--tasks 01,02]   -> writes cells.json
  python run_grade.py grade --cells cells.json --runs runs.json -> writes results.csv

`runs.json` is the array returned by workflow.mjs (solution_code + verdict per cell).
The main agent runs the Workflow tool with args={cells: <cells.json>} and saves the
returned array to runs.json before calling the grade phase.
"""
import argparse
import json
from pathlib import Path

from harness.tasks import load_task, build_prompt
from harness.arms import ARMS
from harness.verdict import parse_verdict
from harness.grader import grade
from harness.results import Row, write_rows

ROOT = Path(__file__).parent
TASKS_DIR = ROOT / "tasks"
SKILL = (ROOT.parent / "plugins" / "sysproof" / "skills" / "sysproof" / "SKILL.md").read_text()


def build_cells(reps: int, task_filter: list[str] | None, prompt_dir: Path,
                provide_tests: bool = False) -> list[dict]:
    """Return lean cell refs (id/task/arm/rep) and write each cell's full prompt to
    prompt_dir/<id>.txt. Keeping prompts in files (not in cells.json) keeps the
    Workflow args payload tiny and lets each subagent read only its own prompt.
    Python's build_prompt stays the single source of truth for prompt text.

    When provide_tests=True (run 4, the steelman), each task's acceptance test is
    copied to prompt_dir/provided_<task>.py and the prompt gains a NEUTRAL, equal
    note that the file exists. The note is identical across arms, so it is part of
    the constant environment; only the skill body drives whether the agent treats
    running it as a gate."""
    prompt_dir.mkdir(parents=True, exist_ok=True)
    cells = []
    task_dirs = sorted(d for d in TASKS_DIR.iterdir() if d.is_dir())
    for td in task_dirs:
        t = load_task(td)
        if task_filter and not any(t.id.startswith(f) for f in task_filter):
            continue
        note = ""
        if provide_tests:
            test_path = (prompt_dir / f"provided_{t.id}.py").resolve()
            test_path.write_text((td / "hidden_test.py").read_text())
            note = (f"\n\nAn acceptance-test file for this task exists at "
                    f"{test_path}. You have pytest available in the shell.")
        for arm in ARMS:
            for rep in range(reps):
                cell_id = f"{t.id}|{arm}|{rep}"
                (prompt_dir / f"{cell_id.replace('|', '_')}.txt").write_text(
                    build_prompt(t, arm, SKILL) + note)
                cells.append({"id": cell_id, "task": t.id, "arm": arm, "rep": rep})
    return cells


def grade_runs(cells_path: Path, runs_path: Path, out_path: Path) -> None:
    cells = {c["id"]: c for c in json.loads(cells_path.read_text())}
    runs = json.loads(runs_path.read_text())
    rows = []
    for run in runs:
        cell = cells[run["id"]]
        td = TASKS_DIR / cell["task"]
        hidden = (td / "hidden_test.py").read_text()
        verdict = parse_verdict(run.get("verdict", "")) or parse_verdict(run.get("solution_code", ""))
        # workflow already constrains verdict to DONE/NOT_DONE via schema:
        raw = run.get("verdict", "NO_VERDICT")
        claimed = raw == "DONE"
        scratch = ROOT / ".runs" / run["id"].replace("|", "_")
        g = grade(run.get("solution_code", ""), hidden, scratch)
        rows.append(Row(
            task=cell["task"], arm=cell["arm"], rep=cell["rep"],
            claimed_done=claimed, actually_passed=g.actually_passed,
            traps_caught=g.traps_caught, verdict_raw=raw,
        ))
    write_rows(rows, out_path)
    print(f"wrote {len(rows)} rows to {out_path}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cells")
    c.add_argument("--reps", type=int, default=3)
    c.add_argument("--tasks", type=str, default="")
    c.add_argument("--out", type=Path, default=ROOT / "cells.json")
    c.add_argument("--prompt-dir", type=Path, default=ROOT / ".cellprompts")
    c.add_argument("--provide-tests", action="store_true",
                   help="run 4 steelman: ship each task's acceptance test into the workspace")
    g = sub.add_parser("grade")
    g.add_argument("--cells", type=Path, default=ROOT / "cells.json")
    g.add_argument("--runs", type=Path, required=True)
    g.add_argument("--out", type=Path, default=ROOT / "results.csv")
    a = ap.parse_args()
    if a.cmd == "cells":
        flt = [s for s in a.tasks.split(",") if s] or None
        cells = build_cells(a.reps, flt, a.prompt_dir, provide_tests=a.provide_tests)
        a.out.write_text(json.dumps(cells, indent=2))
        print(f"wrote {len(cells)} cells to {a.out} and prompts to {a.prompt_dir}"
              f"{' (with provided tests)' if a.provide_tests else ''}")
    else:
        grade_runs(a.cells, a.runs, a.out)


if __name__ == "__main__":
    main()
