"""
Base State - Abstract base class for all game states.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from src.core.state_machine import StateMachine


class BaseState(ABC):
    """Abstract base class for all game states."""

    def __init__(self, state_machine: "StateMachine", name: str):
        self.state_machine = state_machine
        self.name = name

    def on_enter(self) -> None:
        """Called once when entering this state."""
        pass

    def on_exit(self) -> None:
        """Called once when leaving this state."""
        pass

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Process input events for this state."""
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update state logic."""
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Render this state to the screen."""
        pass
