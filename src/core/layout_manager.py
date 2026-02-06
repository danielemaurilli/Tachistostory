"""
Layout Manager - Gestione fonts, slider e layout UI.
"""
from typing import Optional, Tuple

import pygame

from src.core.config import config
from src.utils.paths import resource_path


class LayoutManager:
    """Gestisce fonts, slider e layout UI responsivo."""

    def __init__(self):
        self.font_path = resource_path(config.font.font_path)
        
        # Fonts
        self.font: Optional[pygame.font.Font] = None
        self.font_ms: Optional[pygame.font.Font] = None
        self.font_attes: Optional[pygame.font.Font] = None
        self.font_istruzioni: Optional[pygame.font.Font] = None
        self.font_about: Optional[pygame.font.Font] = None
        self.font_pausa: Optional[pygame.font.Font] = None
        
        # Base font size
        self._base_font = config.font.main_size
        
        # Slider
        self.x_slider = 100
        self.y_slider = 50
        self.slider_width = int(config.slider.base_width * config.slider.width_scale_factor)
        self.posizione_cursore = self.x_slider
        self.pomello_radius = config.slider.knob_radius
        self.lista_fattori = list(config.slider.tick_factors)
        
        # Current word duration
        self._durata_parola_ms = config.timing.word_duration_default
        
        # Track last size to avoid redundant updates
        self._last_size: Tuple[int, int] = (0, 0)

    @property
    def durata_parola_ms(self) -> int:
        return self._durata_parola_ms
    
    @durata_parola_ms.setter
    def durata_parola_ms(self, value: int) -> None:
        self._durata_parola_ms = value
        self._update_slider_position()

    def init_fonts(self, scale: float = 1.0) -> None:
        """Inizializza tutti i font con il fattore di scala dato."""
        self.font = pygame.font.Font(self.font_path, int(self._base_font * scale))
        self.font_ms = pygame.font.Font(
            self.font_path, int(config.font.slider_label_size * scale)
        )
        self.font_attes = pygame.font.Font(
            self.font_path, int(config.font.menu_size * scale)
        )
        self.font_istruzioni = pygame.font.Font(
            self.font_path, int(config.font.instruction_size * scale)
        )
        self.font_about = pygame.font.Font(
            self.font_path, int(config.font.about_size * scale)
        )
        self.font_pausa = pygame.font.Font(
            self.font_path, int(config.font.pause_size * scale)
        )

    def update(self, width: int, height: int, scale: float) -> bool:
        """Aggiorna il layout per le nuove dimensioni. Ritorna True se aggiornato."""
        if (width, height) == self._last_size:
            return False
        
        self._last_size = (width, height)
        self._update_fonts(scale)
        self._update_slider(width, height, scale)
        return True

    def _update_fonts(self, scale: float) -> None:
        """Aggiorna le dimensioni dei font."""
        self.font = pygame.font.Font(self.font_path, int(self._base_font * scale))
        self.font_ms = pygame.font.Font(
            self.font_path, int(config.font.slider_label_size * scale)
        )
        self.font_attes = pygame.font.Font(
            self.font_path, int(config.font.menu_size * scale)
        )
        self.font_istruzioni = pygame.font.Font(
            self.font_path, int(config.font.instruction_size * scale)
        )
        self.font_about = pygame.font.Font(
            self.font_path, int(config.font.about_size * scale)
        )
        self.font_pausa = pygame.font.Font(
            self.font_path, int(config.font.pause_size * scale)
        )

    def _update_slider(self, width: int, height: int, scale: float) -> None:
        """Aggiorna il layout dello slider."""
        base_x = int(width * config.display.slider_margin_ratio)
        base_width = int(width * config.display.slider_width_ratio)
        self.slider_width = int(base_width * 0.60)
        self.x_slider = base_x + int((base_width - self.slider_width) / 2)
        self.y_slider = int(height * config.display.slider_margin_ratio) + int(height * 0.15)
        self.pomello_radius = int(12 * scale)
        self._update_slider_position()

    def _update_slider_position(self) -> None:
        """Ricalcola la posizione del cursore dallo slider in base alla durata."""
        duration_range = config.timing.word_duration_max - config.timing.word_duration_min
        factor = (self._durata_parola_ms - config.timing.word_duration_min) / duration_range
        factor = max(0.0, min(1.0, factor))
        self.posizione_cursore = self.x_slider + factor * self.slider_width

    def get_duration_from_cursor(self, cursor_x: float) -> int:
        """Calcola la durata in ms dalla posizione del cursore."""
        if self.slider_width == 0:
            return config.timing.word_duration_default
        
        factor = (cursor_x - self.x_slider) / self.slider_width
        factor = max(0.0, min(1.0, factor))
        duration_range = config.timing.word_duration_max - config.timing.word_duration_min
        return int(config.timing.word_duration_min + factor * duration_range)
