"""
File selection (drag & drop) state.
"""

from __future__ import annotations

import pygame
from src.states.base_state import BaseState


class FileSelectionState(BaseState):
    """Shows the drag & drop file selection screen."""

    def __init__(self, state_machine, name: str = "file_selection"):
        super().__init__(state_machine, name)

    @property
    def app(self):
        return self.state_machine.app

    def on_enter(self) -> None:
        self.app.tempo_inizio_stato = pygame.time.get_ticks()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        # File drop is handled globally in app.handle_global_events
        pass

    def update(self, delta_time: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        """Render file selection/drop screen."""
        screen.fill(self.app.menu_bg_color)
        
        win_w, win_h = screen.get_size()
        
        prompt = self.app.font_attes.render(
            "Drag a .txt or .doc/.docx file here to start",
            True,
            self.app.bg_color
        )
        prompt_rect = prompt.get_rect(center=(win_w // 2, win_h // 2))
        screen.blit(prompt, prompt_rect)
