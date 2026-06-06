ARMS = ["control", "placebo", "sysproof", "convention",
        "exec_only", "stop_only", "verbose_principle"]

_PLACEBO = "Be careful and verify your work before you say it's done."

# Procedure-style skill with an executable step and a HARD STOP, vs sysproof's
# principle-style "ground before you build". Kept general: it never names the host
# package or the answer; the agent learns the package name from the environment line.
_CONVENTION = """# Convention-first coding

Use this whenever you modify an existing codebase: the existing repo's conventions
override your general knowledge.

MANDATORY procedure - do this BEFORE writing any code:
1. Locate the project's package on your import path and list its modules. For a package
   importable as `pkg`, run:
   python3 -c "import pkg, os; print(os.path.dirname(pkg.__file__))"
   then read the .py files in that directory.
2. Read the module(s) most related to this task. Find the existing helpers, exception
   types, validation/ordering rules, naming, and return shapes already in use.
3. In your reasoning, QUOTE the exact file + function that defines the relevant convention.
4. Implement the smallest patch that reuses or follows it.

HARD STOP:
Do NOT write your solution until you have quoted one existing convention (a real function
or class from the package) that your implementation will follow or reuse. If the repo
already provides the behavior, import it - do not reimplement it. Never fall back to
generic framework knowledge when a local convention exists."""


# --- Ablation arms: decompose `convention` into its parts to find the active ingredient ---

# (a) executable HOW-TO step only, NO hard stop, NO "import don't reimplement" mandate.
_EXEC_ONLY = """# Codebase research

Before writing code, research the project:
1. Locate the project's package on your import path and list its modules. For a package
   importable as `pkg`, run:
   python3 -c "import pkg, os; print(os.path.dirname(pkg.__file__))"
   then read the .py files in that directory.
2. Read the module(s) most related to this task; note the existing helpers, exception
   types, validation/ordering rules, naming, and return shapes already in use.

Then implement your solution."""

# (b) hard STOP + reuse mandate only, NO executable how-to step.
_STOP_ONLY = """# Convention gate

The existing repo's conventions override your general knowledge.

HARD STOP: Do NOT write your solution until you have quoted one existing convention (a real
function or class from the project's package) that your implementation will follow or reuse.
If the repo already provides the behavior, import it - do not reimplement it."""

# (c) length-matched PRINCIPLE, no executable step, no hard stop - controls for "just more,
# more forceful words".
_VERBOSE_PRINCIPLE = """# Ground before you build

Grounding your work in the existing codebase is essential. A competent engineer never works
in a vacuum: they understand the system they are changing before they change it. Reusing what
already exists, following established conventions, and matching the real interfaces instead of
guessing are the marks of careful, professional work. Be thorough. Be deliberate. Respect the
code that is already there and let it guide your implementation. Do not rush to write code
from memory when the project already embodies the right patterns. Take the existing repo
seriously as the source of truth for how things should be done here."""


def arm_prefix(arm: str, sysproof_skill_text: str) -> str:
    """Return the prompt prefix for an arm. sysproof_skill_text is the SKILL.md body."""
    if arm == "control":
        return ""
    if arm == "placebo":
        return _PLACEBO
    if arm == "sysproof":
        return sysproof_skill_text
    if arm == "convention":
        return _CONVENTION
    if arm == "exec_only":
        return _EXEC_ONLY
    if arm == "stop_only":
        return _STOP_ONLY
    if arm == "verbose_principle":
        return _VERBOSE_PRINCIPLE
    raise ValueError(f"unknown arm: {arm}")
