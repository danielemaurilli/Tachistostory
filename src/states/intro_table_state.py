"""
Intro table state (table with closed book).
"""

from __future__ import annotations

import pygame
from src.states.base_state import BaseState
from src.core.config import config


class IntroTableState(BaseState):
    """Shows table background with closed book, auto-transitions after timeout."""

    def __init__(self, state_machine, name: str = "intro_table"):
        super().__init__(state_machine, name)
        self.start_time: int = 0

    @property
    def app(self):
        return self.state_machine.app

    def on_enter(self) -> None:
        self.start_time = pygame.time.get_ticks()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.state_machine.change_state("intro_book_open")

    def update(self, delta_time: float) -> None:
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed > config.timing.intro_table_duration:
            self.state_machine.change_state("intro_book_open")

    def render(self, screen: pygame.Surface) -> None:
        """Render table with closed book."""
        # Draw background
        if self.app.bg_tavolo:
            screen.blit(self.app.bg_tavolo, (0, 0))
        else:
            screen.fill(self.app.menu_bg_color)

        # Draw closed book sprite
        frames = self.app.book_frames_scaled or [self.app.sprite_libro_chiuso]
        if frames and frames[0]:
            libro = frames[0]
            rect = libro.get_rect(
                centerx=self.app.screen_width // 2,
                bottom=self.app.screen_height - config.book.bottom_margin
            )
            screen.blit(libro, rect)
