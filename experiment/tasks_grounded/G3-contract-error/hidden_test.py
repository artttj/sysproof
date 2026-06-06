import solution
from newsroom.errors import FeedError


def test_core_passes_when_present():
    assert solution.require_field({"title": "x"}, "title") is True


def test_trap_raises_feederror_not_valueerror():
    raised = None
    try:
        solution.require_field({"title": ""}, "title")
    except FeedError as e:
        raised = e
    except Exception as e:  # a ValueError or anything else fails the trap
        raised = e
    assert isinstance(raised, FeedError)
    assert hasattr(raised, "code")
