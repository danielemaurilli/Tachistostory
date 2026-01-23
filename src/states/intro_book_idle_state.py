"""
Intro book idle state - Shows static book image with zoom effect.
"""

from __future__ import annotations

import pygame
from src.states.base_state import BaseState
from src.core.config import config
from src.utils.images import load_image_asset, scale_image_cover


class IntroBookIdleState(BaseState):
    """Shows a static book image, then zooms to center."""

    def __init__(self, state_machine, name: str = "intro_book_idle"):
        super().__init__(state_machine, name)
        # Static image variables
        self.animation_start: int = 0
        self.book_image: pygame.Surface | None = None
        self.book_image_scaled: pygame.Surface | None = None
        
        # Phase timing
        self.static_phase_duration: int = 3500  # Show static image for 3.5 seconds
        self.static_phase_complete: bool = False
        
        # Zoom variables
        self.zoom_phase: bool = False
        self.zoom_start_time: int = 0
        self.zoom_progress: float = 0.0
        self.zoom_duration: int = 2000  # Zoom duration in ms
        self.zoom_scale_start: float = 1.0
        self.zoom_scale_end: float = 2.5  # Zoom factor
        self.zoom_completed: bool = False

        # Fade timing
        self.entry_fade_duration: int = 500
        self.exit_fade_duration: int = 500
        self.exit_fade_threshold: float = 0.85
        self.entry_fade_start: int = 0
        self.exit_fade_active: bool = False
        self.exit_fade_start: int = 0
        self.pending_exit_state: str | None = None

    @property
    def app(self):
        return self.state_machine.app

    def on_enter(self) -> None:
        """Load book image and reset animation state."""
        self.animation_start = pygame.time.get_ticks()
        self.static_phase_complete = False
        self.zoom_phase = False
        self.zoom_start_time = 0
        self.zoom_progress = 0.0
        self.zoom_completed = False
        self.entry_fade_start = pygame.time.get_ticks()
        self.exit_fade_start = 0
        self.exit_fade_active = False
        self.pending_exit_state = None
        
        # Load and scale the book image
        self._load_book_image()

    def _load_book_image(self) -> None:
        """Load and scale the static book image."""
        try:
            self.book_image = load_image_asset(config.paths.book_open_bg)
            self._scale_book_image()
            print(f"  ✓ Book image loaded")
        except Exception as e:
            print(f"  ⚠ Book image not found: {e}")
            # Fallback to last frame of book_frames
            if self.app.book_frames_scaled:
                self.book_image = self.app.book_frames_scaled[-1]
                self.book_image_scaled = self.book_image

    def _scale_book_image(self) -> None:
        """Scale book image to cover the entire screen."""
        if not self.book_image:
            return
        
        screen_w = self.app.screen_width
        screen_h = self.app.screen_height
        
        # Use scale_image_cover to fill the entire screen
        self.book_image_scaled = scale_image_cover(self.book_image, screen_w, screen_h)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    # Skip to file selection
                    self._start_exit_fade("file_selection")

    def update(self, delta_time: float) -> None:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.animation_start
        
        # Phase 1: Static image display
        if not self.static_phase_complete:
            if elapsed >= self.static_phase_duration:
                self.static_phase_complete = True
                self.zoom_phase = True
                self.zoom_start_time = pygame.time.get_ticks()
        
        # Phase 2: Zoom animation
        if self.zoom_phase and not self.zoom_completed:
            zoom_elapsed = pygame.time.get_ticks() - self.zoom_start_time
            self.zoom_progress = min(zoom_elapsed / self.zoom_duration, 1.0)
            
            if self.zoom_progress >= 1.0:
                self.zoom_completed = True
                self._start_exit_fade("file_selection")

        if self.exit_fade_active and self.pending_exit_state:
            exit_elapsed = pygame.time.get_ticks() - self.exit_fade_start
            if exit_elapsed >= self.exit_fade_duration:
                self.state_machine.change_state_immediate(self.pending_exit_state)

    def render(self, screen: pygame.Surface) -> None:
        """Render book image with optional zoom effect."""
        if not self.book_image_scaled:
            screen.fill((0, 0, 0))
            return

        # Zoom phase rendering
        if self.zoom_phase:
            # Easing function (ease-out quad for smooth deceleration)
            eased_progress = 1 - (1 - self.zoom_progress) ** 2
            
            # Calculate current scale
            scale = self.zoom_scale_start + (self.zoom_scale_end - self.zoom_scale_start) * eased_progress
            
            # Scale the image
            orig_w, orig_h = self.book_image_scaled.get_size()
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)
            scaled_image = pygame.transform.smoothscale(self.book_image_scaled, (new_w, new_h))
            
            # Center the zoomed image
            image_rect = scaled_image.get_rect(
                centerx=self.app.screen_width // 2,
                centery=self.app.screen_height // 2
            )
            screen.blit(scaled_image, image_rect)
        else:
            # Static phase - blit fullscreen image at (0, 0)
            screen.blit(self.book_image_scaled, (0, 0))

        self._render_fade_overlay(screen)

    def _start_exit_fade(self, next_state: str) -> None:
        if self.exit_fade_active:
            return
        self.exit_fade_active = True
        self.exit_fade_start = pygame.time.get_ticks()
        self.pending_exit_state = next_state

    def _render_fade_overlay(self, screen: pygame.Surface) -> None:
        now = pygame.time.get_ticks()
        alpha = 0

        # Entry fade: black -> transparent before zoom starts
        if not self.zoom_phase:
            entry_elapsed = now - self.entry_fade_start
            if entry_elapsed < self.entry_fade_duration:
                alpha = int(255 * (1 - entry_elapsed / self.entry_fade_duration))

        # Exit fade: transparent -> black near end of zoom
        if self.zoom_phase and not self.exit_fade_active:
            if self.zoom_progress >= self.exit_fade_threshold:
                self._start_exit_fade("file_selection")

        if self.exit_fade_active:
            exit_elapsed = now - self.exit_fade_start
            alpha = max(alpha, int(255 * min(exit_elapsed / self.exit_fade_duration, 1.0)))

        if alpha > 0:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            screen.blit(overlay, (0, 0))
