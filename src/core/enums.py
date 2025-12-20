"""
Shared enums for state and error types.
"""

from __future__ import annotations

from enum import Enum, auto


class Error(Enum):
    EMPTY = auto()
    EXCEPTION = auto()
    INVALID = auto()


class State(Enum):
    MENU_START = auto()
    INTRO_TABLE = auto()
    INTRO_BOOK_OPEN = auto()
    TRANSITION = auto()
    FILE = auto()
    ISTRUCTION = auto()
    SHOW_WORD = auto()
    SHOW_MASK = auto()
    END = auto()
