"""
Music Manager - Gestione audio e musica.
"""
from typing import Optional, TYPE_CHECKING

import pygame

from src.core.config import config

if TYPE_CHECKING:
    from src.core.state_machine import StateMachine


class MusicManager:
    """Gestisce la musica di background e gli effetti audio."""

    def __init__(self):
        self.current_track: Optional[str] = None
        self.volume = config.music.volume
        self.loop = config.music.loop
        self.fade_duration: int = 7000
        
        self._state_machine: Optional["StateMachine"] = None

    def set_state_machine(self, sm: "StateMachine") -> None:
        """Imposta il riferimento alla state machine."""
        self._state_machine = sm

    def load_and_play(self, path: Optional[str] = None) -> bool:
        """Carica e avvia la musica. Ritorna True se caricata con successo."""
        track = path or config.music.background_music
        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.set_volume(self.volume)
            loops = -1 if self.loop else 0
            pygame.mixer.music.play(loops=loops)
            self.current_track = track
            return True
        except Exception as e:
            print(f"⚠ Errore caricamento musica: {e}")
            return False

    def play_default(self) -> bool:
        """Avvia la musica di default."""
        return self.load_and_play(config.music.background_music)

    def stop(self) -> None:
        """Ferma la musica."""
        pygame.mixer.music.stop()

    def pause(self) -> None:
        """Mette in pausa la musica."""
        pygame.mixer.music.pause()

    def unpause(self) -> None:
        """Riprende la musica."""
        pygame.mixer.music.unpause()

    def set_volume(self, volume: float) -> None:
        """Imposta il volume (0.0 - 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

    def fade_out(self, duration_ms: Optional[int] = None) -> None:
        """Sfuma la musica in uscita."""
        if not self.is_playing:
            return
        
        fade_time = duration_ms or self.fade_duration
        pygame.mixer.music.fadeout(fade_time)

    def fade_out_if_in_state(self, allowed_states: tuple[str, ...], duration_ms: Optional[int] = None) -> None:
        """Sfuma la musica solo se si è in uno degli stati specificati."""
        try:
            if not self._state_machine:
                return
            
            current_state = self._state_machine.get_current_state_name()
            if current_state not in allowed_states:
                return
            
            self.fade_out(duration_ms)
        except Exception as e:
            print(f"⚠ Error fade music: {e}")

    @property
    def is_playing(self) -> bool:
        """Ritorna True se la musica sta suonando."""
        return pygame.mixer.music.get_busy()
