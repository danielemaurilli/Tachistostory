"""
Presentation state (word/mask/end + pause overlay + slider).
"""

from __future__ import annotations

import pygame

from src.core.config import config
from src.core.enums import State
from src.states.base_state import BaseState


class PresentationState(BaseState):
    """Handles word presentation loop, pause, and slider interaction."""

    def __init__(self, state_machine, name: str = "presentation"):
        super().__init__(state_machine, name)
        # State-specific timing
        self.state_start_time: int = 0
        # Slider state
        self.slider_dragging: bool = False

    @property
    def app(self):
        return self.state_machine.app

    def on_enter(self) -> None:
        self.app.stato_presentazione = State.SHOW_WORD
        self.state_start_time = pygame.time.get_ticks()
        self.app.in_pausa = False
        self.app.avanti = False
        self.slider_dragging = False

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            # Slider mouse handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if self._is_on_slider_knob(mouse_x, mouse_y):
                    self.slider_dragging = True

            elif event.type == pygame.MOUSEMOTION and self.slider_dragging:
                mouse_x, _ = event.pos
                self._update_slider_from_mouse(mouse_x)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.slider_dragging = False

            # Keyboard handling specific to presentation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.app.in_pausa = not self.app.in_pausa
                    self.state_start_time = pygame.time.get_ticks()
                elif event.key == pygame.K_SPACE:
                    self.app.avanti = True
                elif event.key == pygame.K_r:
                    self.app.set_word_index(0)
                    self.app.stato_presentazione = State.SHOW_WORD
                    self.state_start_time = pygame.time.get_ticks()
                elif event.key == pygame.K_RIGHT:
                    self.app.go()
                    self.state_start_time = pygame.time.get_ticks()
                elif event.key == pygame.K_LEFT:
                    self.app.back()
                    self.state_start_time = pygame.time.get_ticks()

    def _is_on_slider_knob(self, x: int, y: int) -> bool:
        """Check if position is on slider knob."""
        return (
            abs(x - self.app.posizione_cursore) < 20
            and abs(y - self.app.y_slider) < 20
        )

    def _update_slider_from_mouse(self, mouse_x: int) -> None:
        """Update slider value from mouse position."""
        x_min = self.app.x_slider
        x_max = self.app.x_slider + self.app.slider_width
        
        # Clamp position
        if mouse_x < x_min:
            self.app.posizione_cursore = x_min
        elif mouse_x > x_max:
            self.app.posizione_cursore = x_max
        else:
            self.app.posizione_cursore = mouse_x

        # Calculate duration from position
        factor = (self.app.posizione_cursore - x_min) / (x_max - x_min)
        self.app.durata_parola_ms = (
            config.timing.word_duration_min
            + factor * (config.timing.word_duration_max - config.timing.word_duration_min)
        )

    def update(self, delta_time: float) -> None:
        if self.app.in_pausa:
            return

        elapsed = pygame.time.get_ticks() - self.state_start_time

        if self.app.stato_presentazione == State.SHOW_WORD:
            if elapsed >= self.app.durata_parola_ms:
                self.app.stato_presentazione = State.SHOW_MASK
                self.state_start_time = pygame.time.get_ticks()

        elif self.app.stato_presentazione == State.SHOW_MASK:
            if elapsed >= self.app.durata_maschera_ms and self.app.avanti:
                next_index = self.app.indice_parola + 1
                if next_index < len(self.app.lista_parole):
                    self.app.set_word_index(next_index)
                    self.app.stato_presentazione = State.SHOW_WORD
                    self.state_start_time = pygame.time.get_ticks()
                else:
                    self.app.stato_presentazione = State.END
                self.app.avanti = False

    def render(self, screen: pygame.Surface) -> None:
        if self.app.in_pausa:
            self._render_pause(screen)
            return

        # Background
        if self.app.bg_istructions:
            screen.blit(self.app.bg_istructions, (0, 0))
        else:
            screen.fill(self.app.bg_color)

        # Don't render text during fade transition
        if self._is_fade_active():
            return

        # Slider
        self._render_slider(screen)

        # Word display
        if self.app.stato_presentazione == State.SHOW_WORD:
            self._render_centered_text(screen, self.app.parola_corrente)
        elif self.app.stato_presentazione == State.SHOW_MASK:
            self._render_centered_text(screen, self.app.parola_mascherata)
        elif self.app.stato_presentazione == State.END:
            self._render_centered_text(screen, "End of list")

        # Panels
        if self.app.stato_presentazione != State.END:
            self._render_word_panel(screen)
            self._render_phrases_panel(screen)
        else:
            self._render_end_panel(screen)

    def _render_pause(self, screen: pygame.Surface) -> None:
        """Render pause overlay."""
        screen.fill(self.app.menu_bg_color)
        win_w, win_h = screen.get_size()
        pause_surf = self.app.font_pausa.render("PAUSE", True, self.app.text_color)
        pause_surf.set_colorkey(self.app.color_key)
        pause_rect = pause_surf.get_rect(center=(win_w // 2, win_h // 2))
        screen.blit(pause_surf, pause_rect)

    def _render_centered_text(self, screen: pygame.Surface, text: str) -> None:
        """Render text centered on screen."""
        text_surf = self.app.font.render(text, True, config.display.text_color)
        text_surf.set_colorkey((self.app.color_key))
        text_rect = text_surf.get_rect(
            center=(self.app.screen_width // 2, self.app.screen_height // 2)
        )
        screen.blit(text_surf, text_rect)

    def _render_slider(self, screen: pygame.Surface) -> None:
        """Render duration slider with ticks and labels."""
        # Track
        pygame.draw.rect(
            screen,
            config.display.slider_track_color,
            (self.app.x_slider, self.app.y_slider - 2, self.app.slider_width, 4),
        )

        # Tick marks and labels
        for factor in self.app.lista_fattori:
            x_tick = self.app.x_slider + factor * self.app.slider_width
            duration = config.timing.word_duration_min + factor * (
                config.timing.word_duration_max - config.timing.word_duration_min
            )

            # Tick mark
            pygame.draw.rect(
                screen,
                config.display.slider_track_color,
                (x_tick - 2, self.app.y_slider - 8, 2, 16),
            )

            # Duration label
            label = self.app.font_ms.render(f"{int(duration)} ms", True, config.display.text_color)
            label.set_colorkey(self.app.color_key)
            label_rect = label.get_rect(centerx=x_tick, top=self.app.y_slider + 20)
            screen.blit(label, label_rect)

        # Knob
        pygame.draw.circle(
            screen,
            config.display.slider_knob_color,
            (int(self.app.posizione_cursore), self.app.y_slider),
            self.app.pomello_radius,
        )

    def _render_word_panel(self, screen: pygame.Surface) -> None:
        """Render word count panel."""
        human_index = self.app.indice_parola + 1
        total = len(self.app.lista_parole)
        text_surf = self.app.font.render(f"Word: {human_index}/{total}", True, config.display.text_color)
        text_surf.set_colorkey(self.app.color_key)
        text_surf.set_alpha(230)
        text_rect = text_surf.get_rect(
            centerx=self.app.screen_width // 2 - 250,
            bottom=self.app.screen_height - 50,
        )
        screen.blit(text_surf, text_rect)

    def _render_phrases_panel(self, screen: pygame.Surface) -> None:
        """Render phrase count panel."""
        total = self.app.phrases_total
        phrases = (self.app.phrases_index + 1) if total > 0 else 0
        text_surf = self.app.font.render(f"Phrases: {phrases}/{total}", True, config.display.text_color)
        text_surf.set_colorkey(self.app.color_key)
        text_surf.set_alpha(230)
        text_rect = text_surf.get_rect(
            centerx=self.app.screen_width // 2 + 250,
            bottom=self.app.screen_height - 50,
        )
        screen.blit(text_surf, text_rect)

    def _render_end_panel(self, screen: pygame.Surface) -> None:
        """Render end of words message."""
        text_surf = self.app.font.render("The words are ended", True, config.display.text_color)
        text_surf.set_colorkey(self.app.color_key)
        text_surf.set_alpha(230)
        text_rect = text_surf.get_rect(
            centerx=self.app.screen_width // 2,
            bottom=self.app.screen_height - 50,
        )
        screen.blit(text_surf, text_rect)

    def _is_fade_active(self) -> bool:
        """Check if global fade transition is active."""
        return hasattr(self.app, "fade_active") and self.app.fade_active