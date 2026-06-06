import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from defusedxml.ElementTree import parse as safe_parse  # hardened XML parsing

GRADE_TIMEOUT_SECONDS = 60


@dataclass(frozen=True)
class GradeResult:
    actually_passed: bool
    traps_caught: bool
    n_tests: int


def grade(solution_code: str, hidden_test_code: str, scratch_dir: Path,
          support_dir: Path | None = None) -> GradeResult:
    """Write solution + hidden test to an isolated scratch dir, run pytest, parse junit XML.

    actually_passed = every test passed and at least one test ran.
    traps_caught    = every test named test_trap* passed (and at least one exists).
    support_dir     = optional dir whose contents are copied into scratch first, so
                      solution + test can import a host package (repo-grounded suite).
                      Default None preserves the construction-suite behavior exactly.
    """
    import shutil
    scratch_dir.mkdir(parents=True, exist_ok=True)
    if support_dir is not None:
        for child in Path(support_dir).iterdir():
            dest = scratch_dir / child.name
            if child.is_dir():
                shutil.copytree(child, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(child, dest)
    (scratch_dir / "solution.py").write_text(solution_code)
    (scratch_dir / "test_hidden.py").write_text(hidden_test_code)
    xml = scratch_dir / "out.xml"

    try:
        subprocess.run(
            [sys.executable, "-m", "pytest", "test_hidden.py",
             f"--junitxml={xml.name}", "-p", "no:cacheprovider", "-q"],
            cwd=scratch_dir, capture_output=True, timeout=GRADE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return GradeResult(False, False, 0)

    if not xml.exists():
        return GradeResult(False, False, 0)  # collection error (e.g. syntax error)

    root = safe_parse(xml).getroot()
    cases = root.iter("testcase")
    n = 0
    all_pass = True
    trap_total = trap_pass = 0
    for c in cases:
        n += 1
        failed = any(child.tag in ("failure", "error") for child in c)
        if failed:
            all_pass = False
        if c.get("name", "").startswith("test_trap"):
            trap_total += 1
            if not failed:
                trap_pass += 1

    actually_passed = all_pass and n > 0
    traps_caught = trap_total > 0 and trap_pass == trap_total
    return GradeResult(actually_passed, traps_caught, n)
