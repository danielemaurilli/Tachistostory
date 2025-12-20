"""
Path utilities for resource management.

Provides helper functions for building platform-independent paths
that work in both development and PyInstaller bundled environments.
"""

from __future__ import annotations

import os
import sys


def resource_path(*path_parts: str) -> str:
    """
    Get absolute path to a resource (works for dev and PyInstaller).

    Args:
        *path_parts: Path components to join (like os.path.join)

    Returns:
        Absolute path to resource
    """
    relative_path = os.path.join(*path_parts)
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
