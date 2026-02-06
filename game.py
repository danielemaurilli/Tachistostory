"""
Tachistostory - Core Game Application
Main tachistoscope application class - coordinates managers and state machine.
"""

import os
import sys
import traceback
from typing import Optional

import pygame
from pygame.locals import RESIZABLE

from src.core.config import config
from src.core.enums import Error, State
from src.core.window_manager import WindowManager
from src.core.asset_manager import AssetManager
from src.core.layout_manager import LayoutManager
from src.core.word_manager import WordManager
from src.core.music_manager import MusicManager
from src.core.fade_controller import FadeController
from src.core.GameContext import GameContext
from src.core.session_controller import SessionController


# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Screen dimensions (captured from actual display)
_display_info = pygame.display.Info()
SCREEN_MAX_W = _display_info.current_w
SCREEN_MAX_H = _display_info.current_h


class Tachistostory:
    """Main tachistoscope application - coordinates managers and state machine."""

    def __init__(self):
        # ==================== MANAGERS ====================
        self.window = WindowManager(SCREEN_MAX_W, SCREEN_MAX_H)
        self.assets = AssetManager()
        self.layout = LayoutManager()
        self.words = WordManager()
        self.music = MusicManager()
        self.fade = FadeController()
        self.context = GameContext()
        self.context.secret_key = os.urandom(32)
        self.controller = SessionController(self.context)

        # ==================== STATE ====================
        self.state_machine = None
        self.stato_presentazione = State.MENU_START
        self.in_pausa = False
        self.avanti = False

        # ==================== ERROR HANDLING ====================
        self.mostra_errore = False
        self.messaggio_errore = ""
        self.tipo_errore: Optional[Error] = None
        self.tempo_errore = 0

    # ========================================================================
    # COMPATIBILITY PROPERTIES (for existing states)
    # ========================================================================
    
    # Window properties
    @property
    def screen(self) -> Optional[pygame.Surface]:
        return self.window.screen
    
    @property
    def screen_width(self) -> int:
        return self.window.width
    
    @property
    def screen_height(self) -> int:
        return self.window.height
    
    @property
    def min_width(self) -> int:
        return self.window.min_width
    
    @property
    def min_height(self) -> int:
        return self.window.min_height

    # Colors (from config)
    @property
    def bg_color(self):
        return config.display.bg_color
    
    @property
    def menu_bg_color(self):
        return config.display.menu_bg_color
    
    @property
    def error_color(self):
        return config.display.error_color
    
    @property
    def prompt_color(self):
        return config.display.prompt_color
    
    @property
    def text_color(self):
        return config.display.text_color
    
    @property
    def color_key(self):
        return config.display.color_key

    # Assets
    @property
    def logo_image(self):
        return self.assets.logo_image
    
    @property
    def bg_menu(self):
        return self.assets.bg_menu
    
    @property
    def bg_tavolo(self):
        return self.assets.bg_tavolo
    
    @property
    def bg_istructions(self):
        return self.assets.bg_istructions
    
    @property
    def book_open_bg(self):
        return self.assets.book_open_bg
    
    @property
    def book_frames(self):
        return self.assets.book_frames
    
    @property
    def book_frames_scaled(self):
        return self.assets.book_frames_scaled
    
    @property
    def sprite_libro_chiuso(self):
        return self.assets.sprite_libro_chiuso

    # Fonts
    @property
    def font(self):
        return self.layout.font
    
    @property
    def font_attes(self):
        return self.layout.font_attes
    
    @property
    def font_ms(self):
        return self.layout.font_ms
    
    @property
    def font_istruzioni(self):
        return self.layout.font_istruzioni
    
    @property
    def font_about(self):
        return self.layout.font_about
    
    @property
    def font_pausa(self):
        return self.layout.font_pausa

    # Slider
    @property
    def x_slider(self):
        return self.layout.x_slider
    
    @x_slider.setter
    def x_slider(self, value):
        self.layout.x_slider = value
    
    @property
    def y_slider(self):
        return self.layout.y_slider
    
    @y_slider.setter
    def y_slider(self, value):
        self.layout.y_slider = value
    
    @property
    def slider_width(self):
        return self.layout.slider_width
    
    @slider_width.setter
    def slider_width(self, value):
        self.layout.slider_width = value
    
    @property
    def posizione_cursore(self):
        return self.layout.posizione_cursore
    
    @posizione_cursore.setter
    def posizione_cursore(self, value):
        self.layout.posizione_cursore = value
    
    @property
    def pomello_radius(self):
        return self.layout.pomello_radius
    
    @property
    def lista_fattori(self):
        return self.layout.lista_fattori

    # Word/Phrase data
    @property
    def file_caricato(self) -> bool:
        return self.words.file_loaded
    
    @file_caricato.setter
    def file_caricato(self, value: bool):
        self.words.file_loaded = value
    
    @property
    def nome_file(self):
        return self.words.file_name
    
    @nome_file.setter
    def nome_file(self, value):
        self.words.file_name = value
    
    @property
    def num_parole(self):
        return self.words.word_count
    
    @property
    def lista_parole(self):
        return self.words.words
    
    @property
    def indice_parola(self):
        return self.words.current_index
    
    @indice_parola.setter
    def indice_parola(self, value):
        self.words.set_index(value)
    
    @property
    def parola_corrente(self):
        return self.words.current_word
    
    @property
    def parola_mascherata(self):
        return self.words.masked_word
    
    @property
    def phrases_list(self):
        return self.words.phrases
    
    @property
    def phrases_index(self):
        return self.words.phrase_index
    
    @property
    def phrases_total(self):
        return self.words.phrase_count
    
    @property
    def word_to_phrase_map(self):
        return self.words.word_to_phrase_map

    # Timing
    @property
    def durata_parola_ms(self):
        return self.layout.durata_parola_ms
    
    @durata_parola_ms.setter
    def durata_parola_ms(self, value):
        self.layout.durata_parola_ms = value
    
    @property
    def durata_maschera_ms(self):
        return config.timing.mask_duration

    # Fade
    @property
    def fade_enabled(self):
        return self.fade.enabled
    
    @fade_enabled.setter
    def fade_enabled(self, value):
        self.fade.enabled = value
    
    @property
    def fade_active(self):
        return self.fade.is_active
    
    @property
    def fade_duration_ms(self):
        return self.fade.duration_ms

    # Music
    @property
    def music_fade_duration(self):
        return self.music.fade_duration

    # ========================================================================
    # WINDOW MANAGEMENT
    # ========================================================================

    def get_screen(self) -> pygame.Surface:
        """Initialize and return the main display window."""
        return self.window.create_window()

    def caption_window(self) -> None:
        """Set the window caption/title."""
        self.window.set_caption()

    def iconifize(self) -> None:
        """Minimize the window."""
        self.window.iconify()

    def get_full_screen(self) -> None:
        """Toggle between normal and maximized window."""
        self.window.toggle_fullscreen()

    def updating(self) -> None:
        """Update the display."""
        self.window.update()

    # ========================================================================
    # LAYOUT
    # ========================================================================

    def aggiorna_layout(self) -> None:
        """Update UI layout based on current window size."""
        if self.window.screen is None:
            return
        
        size_changed = self.window.check_size_changed()
        layout_updated = self.layout.update(
            self.window.width, 
            self.window.height, 
            self.window.scale_factor
        )
        
        if size_changed or layout_updated:
            self.assets.scale_backgrounds(self.window.width, self.window.height)
            self.assets.scale_book_frames(self.window.width, self.window.height)

    def _update_slider_position(self) -> None:
        """Recalculate slider knob position from current duration."""
        self.layout._update_slider_position()

    # ========================================================================
    # WORD MANAGEMENT
    # ========================================================================

    def maschera_parola(self, parola: str) -> str:
        """Mask a word by replacing letters/digits with '#'."""
        from src.utils.text import mask_word
        return mask_word(parola)

    def go(self) -> None:
        """Advance to next word."""
        self.words.go_next()

    def back(self) -> None:
        """Go back to previous word."""
        self.words.go_previous()

    def set_word_index(self, new_index: int) -> None:
        """Set current word index (clamped) and sync phrase index."""
        self.words.set_index(new_index)

    # ========================================================================
    # FILE LOADING
    # ========================================================================

    def carica_parola_da_txt(self, nome_file: str):
        """Load words from a plain text file."""
        return self.words.load_txt(nome_file)

    def carica_parola_da_word(self, percorso: str):
        """Load words from a Word document (.doc/.docx)."""
        return self.words.load_docx(percorso)

    def load_music(self, path: str) -> None:
        """Load and start background music."""
        self.music.load_and_play(path)

    def reset(self) -> None:
        """Reset game to initial state."""
        self.stato_presentazione = State.FORM
        self.words.reset()
        self.in_pausa = False
        self.mostra_errore = False
        self.context.new_session()
        self.controller = SessionController(self.context)

    # ========================================================================
    # ASSETS
    # ========================================================================

    def load_assets(self) -> None:
        """Load all application assets with error handling."""
        self.assets.load_all(self.window.width, self.window.height)

    # ========================================================================
    # FILE DROP HANDLING
    # ========================================================================

    def _handle_dropfile(self, file_path: str) -> None:
        """Handle a dropped file event."""
        file_low = file_path.lower()

        try:
            if file_low.endswith((".docx", ".doc")):
                words = self.carica_parola_da_word(file_low)
            elif file_low.endswith(".txt"):
                words = self.carica_parola_da_txt(file_low)
            else:
                self._show_error(Error.INVALID, os.path.basename(file_low))
                return

            if words:
                self.words.file_name = os.path.splitext(os.path.basename(file_low))[0]
                self.words.file_loaded = True
                # Store file metadata in session
                from pathlib import Path
                self.controller.set_file_selected(Path(file_path))
                if self.state_machine:
                    self.state_machine.change_state("instruction")
            else:
                self._show_error(Error.EMPTY, "")

        except Exception as e:
            self._show_error(Error.EXCEPTION, str(e))
            traceback.print_exc()

    def _show_error(self, error_type: Error, message: str) -> None:
        """Show an error message."""
        self.mostra_errore = True
        self.tipo_errore = error_type
        self.messaggio_errore = message
        self.tempo_errore = pygame.time.get_ticks()

    # ========================================================================
    # EVENT HANDLING
    # ========================================================================

    def handle_global_events(self, events: list[pygame.event.Event]) -> None:
        """Handle global events (quit, file drop, resize, fullscreen, etc.)."""
        # Check if we're in a state that should block global keyboard shortcuts
        in_form = (
            self.state_machine is not None
            and self.state_machine.get_current_state_name() == "participant_form"
        )

        for event in events:
            # Quit
            if event.type == pygame.QUIT:
                if self.state_machine:
                    self.state_machine.quit()

            # File drop (also blocked in form - form handles its own flow)
            elif event.type == pygame.DROPFILE and not in_form:
                file_path = os.path.abspath(event.file)
                self._handle_dropfile(file_path)

            # Keyboard (blocked in form to avoid conflicts with text input)
            elif event.type == pygame.KEYDOWN and not in_form:
                if event.key == pygame.K_i:
                    self.iconifize()
                elif event.key == pygame.K_e:
                    self.reset()
                    if self.state_machine:
                        self.state_machine.change_state("participant_form")

            # Window resize
            elif event.type == pygame.VIDEORESIZE:
                self.window.handle_resize(event.w, event.h)
                self.aggiorna_layout()
            
            elif event.type == pygame.WINDOWRESIZED:
                if self.window.screen:
                    new_w, new_h = self.window.screen.get_size()
                    self.window.handle_resize(new_w, new_h)
                    self.aggiorna_layout()

    def _render_error_overlay(self, clock: pygame.time.Clock) -> bool:
        """Render error messages if present. Returns True if handled."""
        if not self.mostra_errore:
            return False

        elapsed = pygame.time.get_ticks() - self.tempo_errore
        if elapsed < 5000:
            win_w, win_h = self.window.size

            if self.tipo_errore == Error.EMPTY:
                msg = "Document not readable or empty. Please try again"
            elif self.tipo_errore == Error.EXCEPTION:
                msg = f"An error occurred: {self.messaggio_errore}"
            elif self.tipo_errore == Error.INVALID:
                msg = f"{self.messaggio_errore} is not valid. Please try again"
            else:
                msg = "Unknown error"

            text_surf = self.font_attes.render(msg, True, self.error_color)
            text_surf.set_colorkey(self.color_key)
            text_rect = text_surf.get_rect(centerx=win_w // 2, bottom=win_h - win_h // 3)
            self.window.screen.blit(text_surf, text_rect)
            return True

        self.mostra_errore = False
        return False

    # ========================================================================
    # MUSIC
    # ========================================================================

    def music_exe(self):
        """Load and execute music."""
        self.music.play_default()
    
    def music_fade_out(self, fade_duration_ms: int = 1000) -> None:
        """Fade out on instruction or presentation state."""
        self.music.fade_out_if_in_state(
            allowed_states=("instruction", "presentation"),
            duration_ms=fade_duration_ms
        )

    # ========================================================================
    # STATE TRANSITION FADE
    # ========================================================================

    def request_state_change(self, name: str) -> bool:
        """Request a state change with fade transition. Returns True if handled."""
        return self.fade.request_change(name)

    def _update_fade(self, delta_time: float) -> None:
        """Update fade alpha and switch states at full black."""
        self.fade.update(delta_time)

    def _render_fade_overlay(self, screen: pygame.Surface) -> None:
        """Render black fade overlay if active."""
        self.fade.render(screen)

    # ========================================================================
    # STATE MACHINE
    # ========================================================================

    def _build_state_machine(self) -> None:
        """Create and configure the state machine."""
        from src.core.state_machine import StateMachine
        from src.states import (
            CsvState,
            FileSelectionState,
            InstructionState,
            IntroBookOpenState,
            IntroBookIdleState,
            IntroTableState,
            MenuStartState,
            ParticipantFormState,
            PresentationState,
        )

        self.state_machine = StateMachine(self.window.screen, self)
        
        # Connect managers to state machine
        self.window.set_state_machine(self.state_machine)
        self.music.set_state_machine(self.state_machine)
        self.fade.set_state_machine(self.state_machine)
        
        # Register states
        self.state_machine.add_state("menu_start", MenuStartState(self.state_machine))
        self.state_machine.add_state("intro_table", IntroTableState(self.state_machine))
        self.state_machine.add_state("intro_book_open", IntroBookOpenState(self.state_machine))
        self.state_machine.add_state("intro_book_idle", IntroBookIdleState(self.state_machine))
        self.state_machine.add_state("file_selection", FileSelectionState(self.state_machine))
        self.state_machine.add_state("participant_form", ParticipantFormState(self.state_machine, self.context))
        self.state_machine.add_state("instruction", InstructionState(self.state_machine))
        self.state_machine.add_state("presentation", PresentationState(self.state_machine))
        self.state_machine.add_state("csv_export", CsvState(self.state_machine))
        self.state_machine.change_state("menu_start")

    # ========================================================================
    # MAIN LOOP
    # ========================================================================

    def setup(self) -> None:
        """Initialize screen, assets, and state machine."""
        self.get_screen()
        self.caption_window()
        self.layout.init_fonts(self.window.scale_factor)
        self.load_assets()
        self.aggiorna_layout()
        self._build_state_machine()
        self.music_exe()

    def run(self) -> None:
        """Run the main application loop."""
        self.setup()
        clock = pygame.time.Clock()

        if self.state_machine is None:
            return

        while self.state_machine.is_running():
            try:
                self.avanti = False
                events = pygame.event.get()

                self.handle_global_events(events)
                self.state_machine.handle_events(events)

                # Check for size changes
                self.aggiorna_layout()

                delta_time = clock.get_time() / 1000.0
                self._update_fade(delta_time)
                
                if self._render_error_overlay(clock):
                    if self.window.screen:
                        self._render_fade_overlay(self.window.screen)
                    self.updating()
                    clock.tick(60)
                    continue

                self.music_fade_out(self.music_fade_duration)
                    
                self.state_machine.update(delta_time)
                self.state_machine.render()
                if self.window.screen:
                    self._render_fade_overlay(self.window.screen)
                self.updating()
                clock.tick(60)

            except Exception as e:
                print(f"An error occurred: {e}")
                traceback.print_exc()
                pygame.quit()
                sys.exit()


__all__ = ["Tachistostory", "Error", "State"]
