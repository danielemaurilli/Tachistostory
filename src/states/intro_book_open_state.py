"""
Intro book opening animation state.
"""

from __future__ import annotations

import pygame
from src.states.base_state import BaseState
from src.core.config import config


class IntroBookOpenState(BaseState):
    """Shows the book opening animation."""

    def __init__(self, state_machine, name: str = "intro_book_open"):
        super().__init__(state_machine, name)
        self.animation_start: int = 0
        self.animation_completed: bool = False

    @property
    def app(self):
        return self.state_machine.app

    def on_enter(self) -> None:
        self.animation_start = pygame.time.get_ticks()
        self.animation_completed = False

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.state_machine.change_state("file_selection")

    def update(self, delta_time: float) -> None:
        # Auto-transition after animation completes (with small delay)
        if self.animation_completed:
            elapsed_since_complete = pygame.time.get_ticks() - self.animation_start
            total_duration = len(self.app.book_frames) * config.timing.book_frame_duration + 500
            if elapsed_since_complete > total_duration:
                self.state_machine.change_state("file_selection")

    def render(self, screen: pygame.Surface) -> None:
        """Render book opening animation."""
        # Draw background
        if self.app.bg_tavolo:
            screen.blit(self.app.bg_tavolo, (0, 0))
        else:
            screen.fill(self.app.menu_bg_color)

        frames = self.app.book_frames_scaled or self.app.book_frames
        if not frames:
            return

        # Calculate current frame
        if self.animation_completed:
            frame_index = len(frames) - 1
        else:
            elapsed = pygame.time.get_ticks() - self.animation_start
            frame_duration = config.timing.book_frame_duration
            frame_index = int(elapsed / frame_duration)

            if frame_index >= len(frames) - 1:
                frame_index = len(frames) - 1
                self.animation_completed = True

        # Draw current frame
        current_frame = frames[frame_index]
        frame_rect = current_frame.get_rect(
            centerx=self.app.screen_width // 2,
            bottom=self.app.screen_height - config.book.bottom_margin
        )
        screen.blit(current_frame, frame_rect)
