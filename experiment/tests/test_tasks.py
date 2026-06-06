from pathlib import Path
from harness.tasks import load_task, build_prompt

FIX = Path(__file__).parent / "fixture_task"

def test_load_task_reads_prompt_and_meta():
    t = load_task(FIX)
    assert t.id == "fixture"
    assert t.trap_family == "edge_case"
    assert "normalize_tags" in t.prompt

def test_build_prompt_control_has_no_prefix():
    t = load_task(FIX)
    p = build_prompt(t, arm="control", sysproof_skill_text="SKILL")
    assert p.startswith("normalize_tags".rjust(0) ) or "normalize_tags" in p
    assert "SKILL" not in p
    assert "VERDICT: DONE" in p  # shared scaffolding present in every arm

def test_build_prompt_sysproof_includes_skill():
    t = load_task(FIX)
    p = build_prompt(t, arm="sysproof", sysproof_skill_text="SKILL_BODY")
    assert "SKILL_BODY" in p
    assert "VERDICT: DONE" in p

def test_build_prompt_scaffolding_identical_across_arms():
    t = load_task(FIX)
    control = build_prompt(t, "control", "SKILL")
    sysproof = build_prompt(t, "sysproof", "SKILL")
    # the shared tail (task + return contract) must be byte-identical
    tail = "Implement `normalize_tags"
    assert control[control.index(tail):] == sysproof[sysproof.index(tail):]
