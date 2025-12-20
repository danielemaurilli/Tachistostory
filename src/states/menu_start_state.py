"""
Menu start state - Initial screen with logo fade-in animation.
"""

from __future__ import annotations

import pygame
from src.states.base_state import BaseState
from src.core.config import config


class MenuStartState(BaseState):
    """Initial menu screen with logo fade-in."""

    def __init__(self, state_machine, name: str = "menu_start"):
        super().__init__(state_machine, name)
        # State-specific variables
        self.fade_start_time: int = 0
        self.fade_complete: bool = False

    @property
    def app(self):
        return self.state_machine.app

    def on_enter(self) -> None:
        """Reset fade animation on entering state."""
        self.fade_start_time = pygame.time.get_ticks()
        self.fade_complete = False

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.state_machine.change_state("intro_table")

    def update(self, delta_time: float) -> None:
        # Check if fade is complete
        elapsed = pygame.time.get_ticks() - self.fade_start_time
        if elapsed >= config.timing.logo_fade_duration:
            self.fade_complete = True

    def render(self, screen: pygame.Surface) -> None:
        """Render menu start screen with logo fade-in."""
        # Draw background
        if self.app.bg_menu:
            screen.blit(self.app.bg_menu, (0, 0))
        else:
            screen.fill(self.app.menu_bg_color)

        # Draw logo with fade effect
        if self.app.logo_image:
            win_w, win_h = screen.get_size()
            
            # Calculate logo size (40% of window width)
            target_width = win_w * config.display.logo_width_ratio
            logo_w, logo_h = self.app.logo_image.get_size()
            scale = target_width / logo_w
            new_w = int(logo_w * scale)
            new_h = int(logo_h * scale)
            
            # Position logo
            x_logo = (win_w - new_w) // 2
            y_logo = win_h // 3 - new_h // 2

            # Calculate fade alpha (quadratic ease-in)
            elapsed = pygame.time.get_ticks() - self.fade_start_time
            progress = min(elapsed / config.timing.logo_fade_duration, 1.0)
            alpha = int(min((progress ** 2) * 255, 255))

            # Create faded logo
            logo_fade = self.app.logo_image.copy()
            logo_fade.set_alpha(alpha)
            logo_fade.set_colorkey((0, 0, 0))
            logo_scaled = pygame.transform.smoothscale(logo_fade, (new_w, new_h))
            screen.blit(logo_scaled, (x_logo, y_logo))

            # Blinking "Press ENTER" text after fade complete
            if self.fade_complete:
                cycle = pygame.time.get_ticks() % 1000
                if cycle < 500:
                    prompt = self.app.font_attes.render(
                        "Premi INVIO per iniziare",
                        True,
                        config.display.prompt_color
                    )
                    prompt.set_colorkey((0, 0, 0))
                    prompt_rect = prompt.get_rect(
                        centerx=win_w // 2,
                        top=y_logo + new_h + 100
                    )
                    screen.blit(prompt, prompt_rect)
