import re


def reused_host_package(solution_code: str, package: str) -> bool:
    """True if the solution imports anything from the host package (reuse signal),
    rather than reinventing it. Matches 'import pkg', 'import pkg.x', 'from pkg import'."""
    pat = re.compile(rf"^\s*(from\s+{re.escape(package)}(\.\w+)*\s+import\s+|import\s+{re.escape(package)}(\.\w+)*)", re.MULTILINE)
    return bool(pat.search(solution_code))
