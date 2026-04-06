"""
Utility functions for the NBA Fatigue + Availability Risk Engine project.
"""

from pathlib import Path


def ensure_directory(path: Path) -> None:
    """
    Create a directory if it does not already exist.

    Parameters
    ----------
    path : Path
        Directory path to create.
    """
    path.mkdir(parents=True, exist_ok=True)