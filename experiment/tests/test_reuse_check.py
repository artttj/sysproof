from harness.reuse_check import reused_host_package

def test_detects_import_from_host():
    assert reused_host_package("from newsroom.text import slugify\n", "newsroom") is True

def test_detects_plain_import():
    assert reused_host_package("import newsroom.dates\n", "newsroom") is True

def test_false_when_reinvented():
    assert reused_host_package("import re\ndef f(x): return x\n", "newsroom") is False
