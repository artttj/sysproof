import tempfile
from pathlib import Path
from harness.grader import grade

REUSE_TEST = (
    "import solution\n"
    "def test_trap():\n"
    "    assert solution.f() == 42\n"
)
SOLUTION_USES_SUPPORT = "from support_pkg import answer\ndef f():\n    return answer()\n"


def test_support_dir_is_importable_in_scratch():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        support = td / "support"
        (support / "support_pkg").mkdir(parents=True)
        (support / "support_pkg" / "__init__.py").write_text("def answer():\n    return 42\n")
        scratch = td / "scratch"
        res = grade(SOLUTION_USES_SUPPORT, REUSE_TEST, scratch, support_dir=support)
        assert res.actually_passed is True
        assert res.traps_caught is True
