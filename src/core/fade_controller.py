"""
Fade Controller - Gestione transizioni fade tra stati.
"""
from typing import Optional, TYPE_CHECKING

import pygame

from src.core.config import config

if TYPE_CHECKING:
    from src.core.state_machine import StateMachine


class FadeController:
    """Gestisce le transizioni fade tra stati."""

    def __init__(self):
        self.enabled = True
        self.duration_ms = config.timing.state_fade_duration
        
        self._active = False
        self._direction = "out"  # "out" = fade to black, "in" = fade from black
        self._alpha = 0.0
        self._next_state: Optional[str] = None
        
        self._state_machine: Optional["StateMachine"] = None

    @property
    def is_active(self) -> bool:
        return self._active

    @property
    def alpha(self) -> float:
        return self._alpha

    def set_state_machine(self, sm: "StateMachine") -> None:
        """Imposta il riferimento alla state machine."""
        self._state_machine = sm

    def request_change(self, state_name: str) -> bool:
        """Richiede un cambio stato con transizione fade. Ritorna True se gestito."""
        if not self.enabled or self.duration_ms <= 0:
            return False
        
        if self._active:
            # Already fading - update target
            self._next_state = state_name
            return True
        
        self._active = True
        self._direction = "out"
        self._alpha = 0.0
        self._next_state = state_name
        return True

    def update(self, delta_time: float) -> None:
        """Aggiorna l'alpha del fade e cambia stato quando necessario."""
        if not self._active or self.duration_ms <= 0:
            return

        step = 255 * (delta_time * 1000.0) / self.duration_ms

        if self._direction == "out":
            self._alpha = min(255.0, self._alpha + step)
            if self._alpha >= 255.0:
                # Switch state at full black
                if self._state_machine and self._next_state:
                    self._state_machine._change_state_immediate(self._next_state)
                self._direction = "in"
        else:
            self._alpha = max(0.0, self._alpha - step)
            if self._alpha <= 0.0:
                self._active = False
                self._next_state = None

    def render(self, screen: pygame.Surface) -> None:
        """Renderizza l'overlay nero se il fade è attivo."""
        if not self._active:
            return
        
        overlay = pygame.Surface(screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(int(self._alpha))
        screen.blit(overlay, (0, 0))

    def reset(self) -> None:
        """Resetta lo stato del fade."""
        self._active = False
        self._direction = "out"
        self._alpha = 0.0
        self._next_state = None
