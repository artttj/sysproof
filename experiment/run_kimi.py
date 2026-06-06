"""Run the A/B cells against Ollama Cloud kimi-k2.6:cloud (reason-only, no shell).

kimi cannot iterate/execute, so this is the no-execution condition on a different
model family, with natural prompts. Same three arms. Output is raw text, so we use
a text return contract (fenced code block + VERDICT line) instead of structured
output, applied EQUALLY to all arms.

Usage:
  python run_kimi.py smoke           # one cell, print raw + parsed, validate parser
  python run_kimi.py run --reps 3    # full set -> kimi_cells.json + kimi_runs.json
"""
import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from harness.tasks import load_task
from harness.arms import ARMS, arm_prefix

ROOT = Path(__file__).parent
TASKS_DIR = ROOT / "tasks"
SKILL = (ROOT.parent / "plugins" / "sysproof" / "skills" / "sysproof" / "SKILL.md").read_text()
MODEL = "kimi-k2.6:cloud"

TEXT_CONTRACT = (
    "Return your implementation as a single fenced Python code block "
    "(```python ... ```) defining the requested function(s). After the code block, "
    "on its own line, write exactly `VERDICT: DONE` if you believe the task is fully "
    "and correctly complete, otherwise `VERDICT: NOT_DONE`."
)

_ANSI = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]")
_PRIV = re.compile(r"\[\?[0-9]+[hl]")
_THINK = re.compile(r"Thinking\.\.\..*?\.\.\.done thinking\.", re.DOTALL)
_FENCE = re.compile(r"```(?:python)?\s*(.*?)```", re.DOTALL)
_VERDICT = re.compile(r"VERDICT:\s*(DONE|NOT_DONE)", re.IGNORECASE)


def build_prompt(task, arm: str) -> str:
    prefix = arm_prefix(arm, SKILL)
    body = f"{task.prompt}\n\n{TEXT_CONTRACT}"
    return f"{prefix}\n\n{body}".strip() if prefix else body


def clean(raw: str) -> str:
    s = _ANSI.sub("", raw)
    s = _PRIV.sub("", s)
    s = _THINK.sub("", s)
    return s


def extract(raw: str) -> tuple[str, str]:
    s = clean(raw)
    m = _FENCE.search(s)
    if m:
        code = m.group(1).strip()
    else:  # fall back to first def/import onward
        idx = min((s.find(k) for k in ("def ", "import ", "from ") if s.find(k) >= 0),
                  default=-1)
        code = s[idx:].strip() if idx >= 0 else ""
    vm = _VERDICT.findall(s)
    verdict = vm[-1].upper() if vm else "NO_VERDICT"
    return code, verdict


def call_kimi(prompt: str, timeout: int = 240) -> str:
    # Long multiline prompts must go via stdin; passing as argv yields empty output.
    r = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt, capture_output=True, text=True, timeout=timeout,
    )
    return r.stdout


def cells(reps: int):
    out = []
    for td in sorted(d for d in TASKS_DIR.iterdir() if d.is_dir()):
        t = load_task(td)
        for arm in ARMS:
            for rep in range(reps):
                out.append({"id": f"{t.id}|{arm}|{rep}", "task": t.id,
                            "arm": arm, "rep": rep, "prompt": build_prompt(t, arm)})
    return out


def one(cell: dict) -> dict:
    try:
        raw = call_kimi(cell["prompt"])
        code, verdict = extract(raw)
    except subprocess.TimeoutExpired:
        code, verdict = "", "NO_VERDICT"
    return {"id": cell["id"], "task": cell["task"], "arm": cell["arm"],
            "rep": cell["rep"], "solution_code": code, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("smoke")
    r = sub.add_parser("run")
    r.add_argument("--reps", type=int, default=3)
    r.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    if a.cmd == "smoke":
        c = cells(1)[2]  # task 01, sysproof arm
        print("PROMPT HEAD:\n", c["prompt"][:200], "\n---")
        raw = call_kimi(c["prompt"])
        print("RAW (first 400):\n", raw[:400], "\n---")
        code, verdict = extract(raw)
        print("PARSED verdict:", verdict)
        print("PARSED code:\n", code[:400])
        return

    cs = cells(a.reps)
    json.dump([{k: v for k, v in c.items() if k != "prompt"} for c in cs],
              open(ROOT / "kimi_cells.json", "w"))
    runs = []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(one, c): c for c in cs}
        for i, f in enumerate(as_completed(futs), 1):
            runs.append(f.result())
            print(f"  {i}/{len(cs)} done", file=sys.stderr)
    runs.sort(key=lambda r: r["id"])
    json.dump(runs, open(ROOT / "kimi_runs.json", "w"))
    nv = sum(1 for r in runs if r["verdict"] == "NO_VERDICT")
    print(f"wrote {len(runs)} runs to kimi_runs.json (NO_VERDICT: {nv})")


if __name__ == "__main__":
    main()
