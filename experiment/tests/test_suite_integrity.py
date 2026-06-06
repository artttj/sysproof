from pathlib import Path
import pytest
from harness.grader import grade

TASKS = sorted((Path(__file__).parent.parent / "tasks").glob("*/"))
VALID_FAMILIES = {"edge_case", "false_done", "intent_drift"}

@pytest.mark.parametrize("task_dir", TASKS, ids=lambda p: p.name)
def test_reference_passes_everything(task_dir, tmp_path):
    ref = (task_dir / "reference.py").read_text()
    hidden = (task_dir / "hidden_test.py").read_text()
    r = grade(ref, hidden, tmp_path / task_dir.name)
    assert r.actually_passed, f"{task_dir.name}: reference must pass all hidden tests"
    assert r.traps_caught, f"{task_dir.name}: reference must satisfy the trap test"

@pytest.mark.parametrize("task_dir", TASKS, ids=lambda p: p.name)
def test_naive_triggers_trap(task_dir, tmp_path):
    naive = (task_dir / "naive.py").read_text()
    hidden = (task_dir / "hidden_test.py").read_text()
    r = grade(naive, hidden, tmp_path / task_dir.name)
    assert not r.traps_caught, f"{task_dir.name}: naive solution must miss the trap"

@pytest.mark.parametrize("task_dir", TASKS, ids=lambda p: p.name)
def test_has_trap_and_core_and_valid_family(task_dir):
    import yaml
    hidden = (task_dir / "hidden_test.py").read_text()
    meta = yaml.safe_load((task_dir / "meta.yaml").read_text())
    assert meta["trap_family"] in VALID_FAMILIES
    assert "def test_trap" in hidden, "needs a trap test"
    core = [ln for ln in hidden.splitlines() if ln.strip().startswith("def test_") and "test_trap" not in ln]
    assert core, "needs at least one non-trap core test"
