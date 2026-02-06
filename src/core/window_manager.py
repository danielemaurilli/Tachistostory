"""
Window Manager - Gestione finestra e display.
"""
from typing import Optional, Tuple, TYPE_CHECKING

import pygame
from pygame.locals import RESIZABLE

from src.core.config import config
from src.utils.images import load_image_asset

if TYPE_CHECKING:
    from src.core.state_machine import StateMachine


class WindowManager:
    """Gestisce la finestra principale e le operazioni di display."""

    # Reference resolution for scaling (design target)
    REFERENCE_WIDTH = 1280
    REFERENCE_HEIGHT = 720

    def __init__(self, max_w: int, max_h: int):
        self._max_w = max_w
        self._max_h = max_h
        
        # Use 80% of screen size as base
        self.base_width = int(max_w * 0.8)
        self.base_height = int(max_h * 0.8)
        
        # Minimum size = base size
        self.min_width = self.base_width
        self.min_height = self.base_height
        
        self.width = self.base_width
        self.height = self.base_height
        self.full_screen = False
        
        self._screen: Optional[pygame.Surface] = None
        self._logo_icon: Optional[pygame.Surface] = None
        self._last_size: Tuple[int, int] = (self.width, self.height)
        
        # Reference to state machine for screen sync
        self._state_machine: Optional["StateMachine"] = None

    @property
    def screen(self) -> Optional[pygame.Surface]:
        return self._screen
    
    @property
    def size(self) -> Tuple[int, int]:
        return (self.width, self.height)
    
    @property
    def scale_factor(self) -> float:
        """Calcola il fattore di scala rispetto alla risoluzione di riferimento."""
        scale = min(
            self.width / self.REFERENCE_WIDTH,
            self.height / self.REFERENCE_HEIGHT
        )
        return max(scale, 0.4)  # Minimum scale for readability
    
    def set_state_machine(self, sm: "StateMachine") -> None:
        """Imposta il riferimento alla state machine per sincronizzare lo screen."""
        self._state_machine = sm

    def create_window(self) -> pygame.Surface:
        """Crea e restituisce la finestra principale."""
        self._screen = pygame.display.set_mode(
            [self.width, self.height], RESIZABLE
        )
        self._logo_icon = load_image_asset(config.paths.window_icon)
        pygame.display.set_icon(self._logo_icon)
        return self._screen

    def set_caption(self, title: str = "Tachistostory") -> None:
        """Imposta il titolo della finestra."""
        pygame.display.set_caption(title)

    def iconify(self) -> None:
        """Minimizza la finestra."""
        pygame.display.iconify()

    def toggle_fullscreen(self) -> None:
        """Alterna tra normale e fullscreen."""
        if not self.full_screen:
            self.width = self._max_w
            self.height = self._max_h - config.display.fullscreen_menubar_margin
            self.full_screen = True
        else:
            self.width = self.base_width
            self.height = self.base_height
            self.full_screen = False

        self._screen = pygame.display.set_mode(
            (self.width, self.height), RESIZABLE
        )
        self._sync_state_machine()

    def handle_resize(self, new_w: int, new_h: int) -> bool:
        """Gestisce il resize della finestra. Ritorna True se la dimensione è cambiata."""
        # Enforce minimum size
        target_w = max(new_w, self.min_width)
        target_h = max(new_h, self.min_height)
        
        if (target_w, target_h) == self._last_size:
            return False
        
        self.width = target_w
        self.height = target_h
        self._screen = pygame.display.set_mode(
            (self.width, self.height), RESIZABLE
        )
        self._last_size = (target_w, target_h)
        self._sync_state_machine()
        return True

    def check_size_changed(self) -> bool:
        """Controlla se la dimensione è cambiata (per resize non gestiti da eventi)."""
        if self._screen is None:
            return False
        
        new_w, new_h = self._screen.get_size()
        
        # Also check window size (may differ on macOS during resize)
        try:
            win_w, win_h = pygame.display.get_window_size()
            if win_w != new_w or win_h != new_h:
                new_w = max(win_w, self.min_width)
                new_h = max(win_h, self.min_height)
                self._screen = pygame.display.set_mode((new_w, new_h), RESIZABLE)
                self._sync_state_machine()
        except Exception:
            pass
        
        self.width = new_w
        self.height = new_h
        
        if (new_w, new_h) == self._last_size:
            return False
        
        self._last_size = (new_w, new_h)
        return True

    def update(self) -> None:
        """Aggiorna il display."""
        pygame.display.update()

    def _sync_state_machine(self) -> None:
        """Sincronizza lo screen con la state machine."""
        if self._state_machine:
            self._state_machine.screen = self._screen
