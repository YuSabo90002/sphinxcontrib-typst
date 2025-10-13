"""
Tests for entry points configuration.
"""

import sys
from importlib.metadata import entry_points


def test_entry_point_registration():
    """Test that entry points are defined in pyproject.toml."""
    # Get entry points for sphinx.builders group
    if sys.version_info >= (3, 10):
        # Python 3.10+ uses select() method
        eps = entry_points(group="sphinx.builders")
    else:
        # Python 3.9 uses dict-like access
        all_eps = entry_points()
        eps = all_eps.get("sphinx.builders", [])

    # Convert to list of names
    ep_names = [ep.name for ep in eps]

    # Check that 'typst' entry point exists
    assert (
        "typst" in ep_names
    ), f"'typst' entry point not found in sphinx.builders. Found: {ep_names}"


def test_entry_point_value():
    """Test that the entry point points to the correct module."""
    # Get entry points for sphinx.builders group
    if sys.version_info >= (3, 10):
        eps = entry_points(group="sphinx.builders")
    else:
        all_eps = entry_points()
        eps = all_eps.get("sphinx.builders", [])

    # Find the typst entry point
    typst_ep = None
    for ep in eps:
        if ep.name == "typst":
            typst_ep = ep
            break

    assert typst_ep is not None, "'typst' entry point not found"

    # Check that it points to sphinxcontrib.typst
    assert (
        typst_ep.value == "sphinxcontrib.typst"
    ), f"Entry point value should be 'sphinxcontrib.typst', got '{typst_ep.value}'"
