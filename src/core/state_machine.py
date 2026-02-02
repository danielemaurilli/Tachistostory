"""
State Machine for managing application flow.
"""

from __future__ import annotations

from typing import Dict, Optional
import pygame

from src.core.config import config
from src.states.base_state import BaseState


class StateMachine:
    """Simple state machine with immediate transitions."""

    def __init__(self, screen: pygame.Surface, app: object):
        self.screen = screen
        self.app = app
        self.config = config
        self._states: Dict[str, BaseState] = {}
        self._current_state: Optional[BaseState] = None
        self._current_state_name: Optional[str] = None
        self._running = True

    def add_state(self, name: str, state: BaseState) -> None:
        self._states[name] = state

    def has_state(self, name: str) -> bool:
        return name in self._states

    def change_state(self, name: str) -> None:
        if name not in self._states:
            print(f"Warning: state '{name}' not found")
            return
        if self._current_state is self._states[name]:
            return
        if self._current_state is None:
            self._change_state_immediate(name)
            return
        if hasattr(self.app, "request_state_change"):
            if self.app.request_state_change(name):
                return
        self._change_state_immediate(name)

    def change_state_immediate(self, name: str) -> None:
        """Change state without fade transition."""
        if name not in self._states:
            print(f"Warning: state '{name}' not found")
            return
        if self._current_state is self._states[name]:
            return
        self._change_state_immediate(name)

    def _change_state_immediate(self, name: str) -> None:
        if self._current_state is not None:
            self._current_state.on_exit()
        self._current_state = self._states[name]
        self._current_state_name = name
        self._current_state.on_enter()
        # Ensure layout is updated after state change
        if hasattr(self.app, 'aggiorna_layout'):
            self.app.aggiorna_layout()

    def get_current_state_name(self) -> Optional[str]:
        return self._current_state_name

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if not self._running:
                break
            if self._current_state is not None:
                self._current_state.handle_events([event])

    def update(self, delta_time: float) -> None:
        if self._current_state is not None:
            self._current_state.update(delta_time)

    def render(self) -> None:
        if self._current_state is not None:
            self._current_state.render(self.screen)

    def quit(self) -> None:
        self._running = False

    def is_running(self) -> bool:
        return self._running
