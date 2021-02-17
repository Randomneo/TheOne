"""
Test main module
"""
from the_one import main


def test_main() -> None:
    """
    test main entry point
    """
    assert main() is None
