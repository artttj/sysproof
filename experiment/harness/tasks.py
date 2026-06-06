from dataclasses import dataclass
from pathlib import Path
import yaml

from harness.arms import arm_prefix

_RETURN_CONTRACT = (
    "Return your implementation as a complete, self-contained Python module "
    "(the `solution_code` field) that defines the requested function(s). "
    "Then state your verdict on its own line, exactly `VERDICT: DONE` if you "
    "believe the task is fully and correctly complete, otherwise `VERDICT: NOT_DONE`."
)


@dataclass(frozen=True)
class Task:
    id: str
    trap_family: str
    prompt: str
    dir: Path


def load_task(task_dir: Path) -> Task:
    meta = yaml.safe_load((task_dir / "meta.yaml").read_text())
    prompt = (task_dir / "prompt.md").read_text().strip()
    return Task(id=meta["id"], trap_family=meta["trap_family"], prompt=prompt, dir=task_dir)


def build_prompt(task: Task, arm: str, sysproof_skill_text: str) -> str:
    prefix = arm_prefix(arm, sysproof_skill_text)
    shared_tail = f"{task.prompt}\n\n{_RETURN_CONTRACT}"
    return f"{prefix}\n\n{shared_tail}".strip() if prefix else shared_tail
