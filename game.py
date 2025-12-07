"""
<<<<<<< HEAD
Tachistostory - Core Game Application
Main tachistoscope application class - manages window, assets, and state machine.
"""

import os
import sys
import traceback
from typing import List, Optional, Tuple

import pygame
from pygame.locals import RESIZABLE

from src.core.config import config
from src.core.enums import Error, State
from src.loaders.file_loader import FileLoader, LoadedText
from src.utils.images import (
    extract_sprite_frames,
    load_image_asset,
    scale_image_cover,
    scale_surface_to_fit,
)
from src.utils.paths import resource_path
from src.utils.text import mask_word

# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen dimensions (captured before window creation)
SCREEN_MAX_W = config.display.max_width
SCREEN_MAX_H = config.display.max_height


class Tachistostory:
    """Main tachistoscope application - window, assets, state machine coordinator."""

    def __init__(self):
        # ==================== WINDOW ====================
        self.screen: Optional[pygame.Surface] = None
        self.base_width = config.display.base_width
        self.base_height = config.display.base_height
        self.screen_width = self.base_width
        self.screen_height = self.base_height
        self.full_screen = False
        self.last_layout_size: Tuple[int, int] = (self.screen_width, self.screen_height)

        # ==================== COLORS ====================
        self.bg_color = config.display.bg_color
        self.menu_bg_color = config.display.menu_bg_color
        self.error_color = config.display.error_color
        self.prompt_color = config.display.prompt_color
        self.text_color = config.display.text_color
        self.color_key = config.display.color_key

        # ==================== ASSETS ====================
        self.logo_image: Optional[pygame.Surface] = None
        self.logo_icon: Optional[pygame.Surface] = None
        self.bg_menu: Optional[pygame.Surface] = None
        self.bg_tavolo: Optional[pygame.Surface] = None
        self.bg_istructions: Optional[pygame.Surface] = None
        self.book_frames: List[pygame.Surface] = []
        self.book_frames_scaled: List[pygame.Surface] = []
        self.sprite_libro_chiuso: Optional[pygame.Surface] = None
        self.book_open_bg: Optional[pygame.Surface] = None

        # ==================== FONTS ====================
        self.font_path = resource_path(config.font.font_path)
        self.base_font = config.font.main_size
        self.font: Optional[pygame.font.Font] = None
        self.font_attes = pygame.font.Font(self.font_path, config.font.menu_size)
        self.font_ms = pygame.font.Font(self.font_path, config.font.slider_label_size)
        self.font_istruzioni = pygame.font.Font(self.font_path, config.font.instruction_size)
        self.font_about = pygame.font.Font(self.font_path, config.font.about_size)
        self.font_pausa = pygame.font.Font(self.font_path, config.font.pause_size)

        # ==================== FILE/WORD DATA ====================
        self.file_caricato = False
        self.nome_file: Optional[str] = None
        self.num_parole: Optional[int] = None
        self.lista_parole: List[str] = []
        self.indice_parola = 0
        self.parola_corrente = ""
        self.parola_mascherata = ""
        self.phrases_list: List[str] = []
        self.phrases_index = 0
        self.phrases_total = 0
        self.word_to_phrase_map: List[int] = []

        # ==================== PRESENTATION STATE ====================
        self.stato_presentazione = State.MENU_START
        self.in_pausa = False
        self.avanti = False
        self.durata_parola_ms = config.timing.word_duration_default
        self.durata_maschera_ms = config.timing.mask_duration

        # ==================== SLIDER ====================
        self.x_slider = 100
        self.y_slider = 50
        self.slider_width = int(config.slider.base_width * config.slider.width_scale_factor)
        self.posizione_cursore = self.x_slider
        self.pomello_radius = config.slider.knob_radius
        self.lista_fattori = list(config.slider.tick_factors)

        # ==================== ERROR HANDLING ====================
        self.mostra_errore = False
        self.messaggio_errore = ""
        self.tipo_errore: Optional[Error] = None
        self.tempo_errore = 0

        # ==================== STATE MACHINE ====================
        self.state_machine = None

        # ==================== STATE TRANSITION FADE ====================
        self.fade_enabled = True
        self.fade_active = False
        self.fade_direction = "out"
        self.fade_alpha = 0.0
        self.fade_next_state: Optional[str] = None
        self.fade_duration_ms = config.timing.state_fade_duration

    # ========================================================================
    # WINDOW MANAGEMENT
    # ========================================================================

    def get_screen(self) -> pygame.Surface:
        """Initialize and return the main display window."""
        self.screen = pygame.display.set_mode(
            [self.screen_width, self.screen_height], RESIZABLE
        )
        self.logo_icon = load_image_asset(config.paths.logo_title)
        pygame.display.set_icon(self.logo_icon)
        return self.screen

    def caption_window(self) -> None:
        """Set the window caption/title."""
        pygame.display.set_caption("Tachistostory")

    def iconifize(self) -> None:
        """Minimize the window."""
        pygame.display.iconify()

    def get_full_screen(self) -> None:
        """Toggle between normal and maximized window."""
        if not self.full_screen:
            self.screen_width = SCREEN_MAX_W
            self.screen_height = SCREEN_MAX_H - config.display.fullscreen_menubar_margin
            self.full_screen = True
        else:
            self.screen_width = self.base_width
            self.screen_height = self.base_height
            self.full_screen = False

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), RESIZABLE
        )
        if self.state_machine:
            self.state_machine.screen = self.screen

    def updating(self) -> None:
        """Update the display."""
        pygame.display.update()

    # ========================================================================
    # LAYOUT
    # ========================================================================

    def aggiorna_layout(self) -> None:
        """Update UI layout based on current window size."""
        if self.screen is None:
            return

        new_w, new_h = self.screen.get_size()
        self.screen_width = new_w
        self.screen_height = new_h

        scale = min(new_w / self.base_width, new_h / self.base_height)

        self._aggiorna_fonts(scale)
        self._aggiorna_slider_layout(scale)
        self._scala_backgrounds()
        self._scale_book_frames()

    def _aggiorna_fonts(self, scale: float) -> None:
        """Update font sizes based on scale factor."""
        self.font = pygame.font.Font(self.font_path, int(self.base_font * scale))
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

    def _aggiorna_slider_layout(self, scale: float) -> None:
        """Update slider layout based on scale factor."""
        base_x = int(self.screen_width * config.display.slider_margin_ratio)
        base_width = int(self.screen_width * config.display.slider_width_ratio)
        self.slider_width = int(base_width * 0.60)
        self.x_slider = base_x + int((base_width - self.slider_width) / 2)
        self.y_slider = int(self.screen_height * config.display.slider_margin_ratio) + int(self.screen_height * 0.15)
        self.pomello_radius = int(12 * scale)
        self._update_slider_position()

    def _update_slider_position(self) -> None:
        """Recalculate slider knob position from current duration."""
        duration_range = config.timing.word_duration_max - config.timing.word_duration_min
        factor = (self.durata_parola_ms - config.timing.word_duration_min) / duration_range
        factor = max(0.0, min(1.0, factor))
        self.posizione_cursore = self.x_slider + factor * self.slider_width

    def _scala_backgrounds(self) -> None:
        """Scale background images to current window size."""
        if hasattr(self, "_bg_menu_original"):
            self.bg_menu = scale_image_cover(
                self._bg_menu_original, self.screen_width, self.screen_height
            )
        if hasattr(self, "_bg_tavolo_original"):
            self.bg_tavolo = scale_image_cover(
                self._bg_tavolo_original, self.screen_width, self.screen_height
            )
        if hasattr(self, "_bg_istructions_original"):
            self.bg_istructions = scale_image_cover(
                self._bg_istructions_original, self.screen_width, self.screen_height
            )
        if hasattr(self, "_book_open_original"):
            self.book_open_bg = scale_image_cover(
                self._book_open_original, self.screen_width, self.screen_height
            )

    def _scale_book_frames(self) -> None:
        """Pre-scale book frames for current screen size."""
        if not self.book_frames:
            return
        max_w = int(self.screen_width * 1.25)
        max_h = int(self.screen_height * 1.25)
        self.book_frames_scaled = []
        for frame in self.book_frames:
            scaled = scale_surface_to_fit(frame, max_w, max_h)
            scaled.set_colorkey((0, 0, 0))
            self.book_frames_scaled.append(scaled)
        if self.book_frames_scaled:
            self.sprite_libro_chiuso = self.book_frames_scaled[0]

    # ========================================================================
    # WORD MANAGEMENT
    # ========================================================================

    def maschera_parola(self, parola: str) -> str:
        """Mask a word by replacing letters/digits with '#'."""
        return mask_word(parola)

    def go(self) -> None:
        """Advance to next word."""
        self.set_word_index(self.indice_parola + 1)

    def back(self) -> None:
        """Go back to previous word."""
        self.set_word_index(self.indice_parola - 1)

    def set_word_index(self, new_index: int) -> None:
        """Set current word index (clamped) and sync phrase index."""
        if not self.lista_parole:
            return

        new_index = max(0, min(new_index, len(self.lista_parole) - 1))
        self.indice_parola = new_index
        self.parola_corrente = self.lista_parole[new_index]
        self.parola_mascherata = self.maschera_parola(self.parola_corrente)
        self._sync_phrase_index()

    def _sync_phrase_index(self) -> None:
        """Update phrases_index based on current word index."""
        if self.word_to_phrase_map and 0 <= self.indice_parola < len(self.word_to_phrase_map):
            self.phrases_index = self.word_to_phrase_map[self.indice_parola]
        else:
            self.phrases_index = 0

    # ========================================================================
    # FILE LOADING
    # ========================================================================

    def carica_parola_da_txt(self, nome_file: str) -> List[str]:
        """Load words from a plain text file."""
        loaded = FileLoader.load_txt(nome_file)
        self._apply_loaded_text(loaded)
        return self.lista_parole

    def carica_parola_da_word(self, percorso: str) -> List[str]:
        """Load words from a Word document (.doc/.docx)."""
        loaded = FileLoader.load_docx(percorso)
        self._apply_loaded_text(loaded)
        return self.lista_parole

    def _apply_loaded_text(self, loaded: LoadedText) -> None:
        """Apply loaded text data to app state."""
        self.lista_parole = loaded.words
        self.word_to_phrase_map = loaded.word_to_phrase_map
        self.phrases_list = loaded.phrases_list
        self.phrases_total = loaded.phrases_total

        if self.lista_parole:
            self.set_word_index(0)
        else:
            self.indice_parola = 0
            self.parola_corrente = ""
            self.parola_mascherata = ""
            self.phrases_index = 0

    def reset(self) -> None:
        """Reset game to initial state."""
        self.stato_presentazione = State.FILE
        self.file_caricato = False
        self.nome_file = None
        self.num_parole = None
=======
Tachistostory - Core Game Logic
Main tachistoscope application class with word presentation and display logic.
"""

import pygame
from pygame.locals import *
import sys
import os
import docx2txt
import settings 

# Initialize Pygame BEFORE creating the class
pygame.init()
pygame.font.init()

# Get screen dimensions before creating any window
_SCREEN_INFO = pygame.display.Info()
SCREEN_MAX_W = _SCREEN_INFO.current_w
SCREEN_MAX_H = _SCREEN_INFO.current_h


def resource_path(relative_path: str) -> str:
    """
    Returns the correct path for assets in both development and PyInstaller builds.
    
    Args:
        relative_path: Path relative to the application root
        
    Returns:
        Absolute path to the resource
    """
    try:
        # When the app is packaged with PyInstaller
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        # When running in development (VS Code, etc.)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Tachistostory:
    """Main tachistoscope application class."""
    
    def __init__(self):
        # Screen setup
        self.screen = None
        self.base_width = 600
        self.base_height = 800
        self.screen_width = self.base_width
        self.screen_height = self.base_height

        # Color settings
        self.bg_color = (210, 245, 130)
        self.menu_bg_color = (0, 157, 198)
        
        # Logo
        self.logo_image = None
        self.larghezza_target = self.screen_width * 0.4
        
        # Instructions screen
        self.nome_file = None
        self.num_parole = None

        # Base font
        self.font = None

        # Presentation state
        # Possible states: 'attesa_file', 'istruzioni', 'show_word', 'show_mask', 'fine'
        self.stato_presentazione = 'attesa_file'
        
        # File loaded flag
        self.file_caricato = False
        self.percorso_file = None

        # Word presentation duration
        self.tempo_inizio_stato = None
        self.durata_parola_ms = 220
        self.durata_maschera_ms = 400
        
        # Word list initialization
>>>>>>> 1982162 (Initial commit)
        self.lista_parole = []
        self.indice_parola = 0
        self.parola_corrente = ""
        self.parola_mascherata = ""
<<<<<<< HEAD
        self.phrases_list = []
        self.phrases_index = 0
        self.phrases_total = 0
        self.word_to_phrase_map = []
        self.in_pausa = False
        self.mostra_errore = False

    # ========================================================================
    # ASSETS
    # ========================================================================

    def load_assets(self) -> None:
        """Load all application assets with error handling."""
        print("[LOADING] Caricamento asset...")

        # Logo
        try:
            self.logo_image = load_image_asset(config.paths.logo_title)
            self.logo_image.set_colorkey((0, 0, 0))
            print("  ✓ Logo principale caricato")
        except Exception as e:
            print(f"  ⚠ Logo principale non trovato: {e}")
            self.logo_image = None

        # Background menu
        try:
            self._bg_menu_original = load_image_asset(config.paths.bg_menu_table_book)
            self.bg_menu = scale_image_cover(
                self._bg_menu_original, self.screen_width, self.screen_height
            )
            print("  ✓ Background menu caricato")
        except Exception as e:
            print(f"  ⚠ Background menu non trovato: {e}")
            self.bg_menu = self._create_placeholder((self.screen_width, self.screen_height), (50, 50, 100))

        # Background table
        try:
            self._bg_tavolo_original = load_image_asset(config.paths.bg_menu_table)
            self.bg_tavolo = scale_image_cover(
                self._bg_tavolo_original, self.screen_width, self.screen_height
            )
            print("  ✓ Background tavolo caricato")
        except Exception as e:
            print(f"  ⚠ Background tavolo non trovato: {e}")
            self.bg_tavolo = self.bg_menu
            if hasattr(self, "_bg_menu_original"):
                self._bg_tavolo_original = self._bg_menu_original

        # Background istructions
        try:
            self._bg_istructions_original = load_image_asset(config.paths.bg_istructions)
            self.bg_istructions = scale_image_cover(
                self._bg_istructions_original, self.screen_width, self.screen_height
            )
            print("  ✓ Background istruzioni caricato")
        except Exception as e:
            print(f"  ⚠ Background istruzioni non trovato: {e}")
            self.bg_istructions = self.bg_menu
            if hasattr(self, "_bg_menu_original"):
                self._bg_istructions_original = self._bg_menu_original

        # Book sprite sheet
        try:
            book_sheet = load_image_asset(config.paths.book_master_sheet)
            self.book_frames = extract_sprite_frames(book_sheet, layout="horizontal")
            for frame in self.book_frames:
                frame.set_colorkey((0, 0, 0))
            self.sprite_libro_chiuso = self.book_frames[0]
            self._scale_book_frames()
            print(f"  ✓ Sprite libro caricato ({len(self.book_frames)} frame)")
        except Exception as e:
            print(f"  ⚠ Sprite libro non trovato: {e}")
            placeholder = self._create_placeholder((640, 640), (139, 69, 19))
            self.book_frames = [placeholder] * 17
            self.sprite_libro_chiuso = placeholder
            self._scale_book_frames()

        # Book open background
        try:
            book_open = load_image_asset(config.paths.book_open_bg)
            self._book_open_original = book_open if not self.book_frames else self.book_frames[-1]
            self.book_open_bg = scale_image_cover(
                self._book_open_original, self.screen_width, self.screen_height
            )
            print("  ✓ Background libro aperto caricato")
        except Exception as e:
            print(f"  ⚠ Background libro aperto non trovato: {e}")
            self.book_open_bg = self._create_placeholder(
                (self.screen_width, self.screen_height), (255, 248, 220)
            )

        print("[LOADING] Caricamento asset completato\n")

    def _create_placeholder(
        self, size: Tuple[int, int], color: Tuple[int, int, int]
    ) -> pygame.Surface:
        """Create a colored placeholder surface when asset is missing."""
        surface = pygame.Surface(size)
        surface.fill(color)
        pygame.draw.line(surface, (255, 0, 0), (0, 0), size, 3)
        pygame.draw.line(surface, (255, 0, 0), (0, size[1]), (size[0], 0), 3)
        return surface.convert()

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
                self.nome_file = os.path.splitext(os.path.basename(file_low))[0]
                self.file_caricato = True
                self.num_parole = len(self.lista_parole)
                if self.state_machine:
                    self.state_machine.change_state("instruction")
                if not self.full_screen:
                    self.get_full_screen()
                    self.aggiorna_layout()
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
        for event in events:
            current_state = (
                self.state_machine.get_current_state_name() if self.state_machine else None
            )

            # Quit
            if event.type == pygame.QUIT:
                if self.state_machine:
                    self.state_machine.quit()

            # File drop
            elif event.type == pygame.DROPFILE:
                file_path = os.path.abspath(event.file)
                self._handle_dropfile(file_path)

            # Keyboard
            elif event.type == pygame.KEYDOWN:
                # Iconify
                if event.key == pygame.K_i:
                    self.iconifize()
                # Fullscreen toggle (except in instruction state)
                elif event.key == pygame.K_f and current_state != "instruction":
                    self.get_full_screen()
                    self.aggiorna_layout()
                # Reset game
                elif event.key == pygame.K_e:
                    self.reset()
                    if self.state_machine:
                        self.state_machine.change_state("file_selection")

            # Window resize
            elif event.type == pygame.VIDEORESIZE:
                if current_state == "instruction":
                    continue

                self.screen_width = max(event.w, config.display.min_width)
                self.screen_height = max(event.h, config.display.min_height)
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height), RESIZABLE
                )
                if self.state_machine:
                    self.state_machine.screen = self.screen
                self.aggiorna_layout()

    def _render_error_overlay(self, clock: pygame.time.Clock) -> bool:
        """Render error messages if present. Returns True if handled."""
        if not self.mostra_errore:
            return False

        elapsed = pygame.time.get_ticks() - self.tempo_errore
        if elapsed < 5000:
            win_w, win_h = self.screen.get_size()

            if self.tipo_errore == Error.EMPTY:
                msg = "Document not readable or empty. Please try again"
            elif self.tipo_errore == Error.EXCEPTION:
                msg = f"An error occurred: {self.messaggio_errore}"
            elif self.tipo_errore == Error.INVALID:
                msg = f"{self.messaggio_errore} is not valid. Please try again"
            else:
                msg = "Unknown error"

            text_surf = self.font_attes.render(msg, True, self.error_color)
            text_rect = text_surf.get_rect(centerx=win_w // 2, bottom=win_h - win_h // 3)
            self.screen.blit(text_surf, text_rect)
            return True

        self.mostra_errore = False
        return False

    # ========================================================================
    # STATE TRANSITION FADE
    # ========================================================================

    def request_state_change(self, name: str) -> bool:
        """Request a state change with fade transition. Returns True if handled."""
        if not self.fade_enabled or self.fade_duration_ms <= 0:
            return False
        if self.fade_active:
            self.fade_next_state = name
            return True
        self.fade_active = True
        self.fade_direction = "out"
        self.fade_alpha = 0.0
        self.fade_next_state = name
        return True

    def _update_fade(self, delta_time: float) -> None:
        """Update fade alpha and switch states at full black."""
        if not self.fade_active or self.fade_duration_ms <= 0:
            return

        step = 255 * (delta_time * 1000.0) / self.fade_duration_ms

        if self.fade_direction == "out":
            self.fade_alpha = min(255.0, self.fade_alpha + step)
            if self.fade_alpha >= 255.0:
                if self.state_machine and self.fade_next_state:
                    self.state_machine._change_state_immediate(self.fade_next_state)
                self.fade_direction = "in"
        else:
            self.fade_alpha = max(0.0, self.fade_alpha - step)
            if self.fade_alpha <= 0.0:
                self.fade_active = False
                self.fade_next_state = None

    def _render_fade_overlay(self, screen: pygame.Surface) -> None:
        """Render black fade overlay if active."""
        if not self.fade_active:
            return
        overlay = pygame.Surface(screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(int(self.fade_alpha))
        screen.blit(overlay, (0, 0))

    # ========================================================================
    # STATE MACHINE
    # ========================================================================

    def _build_state_machine(self) -> None:
        """Create and configure the state machine."""
        from src.core.state_machine import StateMachine
        from src.states import (
            FileSelectionState,
            InstructionState,
            IntroBookOpenState,
            IntroBookIdleState,
            IntroTableState,
            MenuStartState,
            PresentationState,
        )

        self.state_machine = StateMachine(self.screen, self)
        self.state_machine.add_state("menu_start", MenuStartState(self.state_machine))
        self.state_machine.add_state("intro_table", IntroTableState(self.state_machine))
        self.state_machine.add_state("intro_book_open", IntroBookOpenState(self.state_machine))
        self.state_machine.add_state("intro_book_idle", IntroBookIdleState(self.state_machine))
        self.state_machine.add_state("file_selection", FileSelectionState(self.state_machine))
        self.state_machine.add_state("instruction", InstructionState(self.state_machine))
        self.state_machine.add_state("presentation", PresentationState(self.state_machine))
        self.state_machine.change_state("menu_start")

    # ========================================================================
    # MAIN LOOP
    # ========================================================================

    def setup(self) -> None:
        """Initialize screen, assets, and state machine."""
        self.get_screen()
        self.caption_window()
        self.font = pygame.font.Font(self.font_path, self.base_font)
        self.load_assets()
        self._update_slider_position()
        self._build_state_machine()

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

                delta_time = clock.get_time() / 1000.0
                self._update_fade(delta_time)

                if self._render_error_overlay(clock):
                    if self.screen:
                        self._render_fade_overlay(self.screen)
                    self.updating()
                    clock.tick(60)
                    continue

                self.state_machine.update(delta_time)
                self.state_machine.render()
                if self.screen:
                    self._render_fade_overlay(self.screen)
                self.updating()
                clock.tick(60)

            except Exception as e:
                print(f"An error occurred: {e}")
                traceback.print_exc()
                pygame.quit()
                sys.exit()


__all__ = ["Tachistostory", "Error", "State"]
=======

        # Pause state
        self.in_pausa = False

        # Forward button
        self.avanti = False
        
        # Slider coordinates
        self.x_slider = 100
        self.y_slider = 50
        self.base_y_slider = 50
        self.posizione_cursore = self.x_slider
        self.slider_drag = False
        self.pomello_radius = 12
        self.base_slider_width = 400
        self.slider_width = int(self.base_slider_width * 0.7)
        
        # Slider ticks
        self.lista_fattori = [0.0, 0.25, 0.5, 0.75, 1.0]

        # Font sizes
        self.base_font = 60
        self.base_font_ms = 14
        self.base_font_attesa = 25
        self.base_font_about = 16
        self.base_font_istruzioni = 28
        self.base_font_pausa = 60
        
        # Initialize fonts
        self.font_attes = pygame.font.SysFont('Calibri', self.base_font_attesa, bold=False, italic=True)
        self.font_ms = pygame.font.SysFont('Calibri', self.base_font_ms, bold=False, italic=False)
        self.font_istruzioni = pygame.font.SysFont('Calibri', self.base_font_istruzioni, bold=False, italic=False)
        self.font_about = pygame.font.SysFont('Calibri', self.base_font_about, bold=False, italic=True)
        self.font_pausa = pygame.font.SysFont('Calibri', self.base_font_pausa, True, False)

        # Full-screen toggle
        self.full_screen = False

        # Layout size tracking
        self.last_layout_size = (self.screen_width, self.screen_height)

    # ========================================================================
    # WINDOW SETUP
    # ========================================================================
    
    def display(self):
        """Initialize and return the main display window."""
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height], RESIZABLE)
        return self.screen
    
    # ========================================================================
    # WORD MASKING
    # ========================================================================
    
    def maschera_parola(self, parola):
        """
        Mask a word by replacing letters and digits with '#'.
        
        Args:
            parola: The word to mask
            
        Returns:
            Masked string with '#' replacing alphanumeric characters
        """
        nuova_parola = []
        for lettera in parola:
            if lettera.isalpha() or lettera.isdigit():
                nuova_parola.append("#")
            elif lettera == " ":
                nuova_parola.append(" ")
            elif lettera in [":",".",";",",",'!','?']:
                nuova_parola.append(lettera)
            else:
                nuova_parola.append("#")
        stringa = ""
        stringa_mascherata = stringa.join(nuova_parola)
        return stringa_mascherata

    # ========================================================================
    # FILE LOADING
    # ========================================================================
    
    def carica_parola_da_txt(self, nome_file):
        """
        Load words from a plain text file.
        
        Args:
            nome_file: Path to the .txt file
            
        Returns:
            List of cleaned words
            
        Raises:
            ValueError: If the file is empty
            FileNotFoundError: If the file doesn't exist
        """
        if os.path.exists(nome_file):
            with open(nome_file, 'r', encoding='utf-8') as file:
                lista_parole = []
                caratteri_da_rimuovere = ',.:;?!-_"\'1234567890'
                for riga in file:
                    riga_pulita = riga.strip()
                    if riga_pulita:
                        # Split line into individual words
                        parole_nella_riga = riga_pulita.split()
                        for parola in parole_nella_riga:
                            # Remove punctuation from each word
                            parola_pulita = parola.strip(caratteri_da_rimuovere)
                            if parola_pulita:  # Only add if not empty
                                lista_parole.append(parola_pulita)
            self.lista_parole = lista_parole
            if lista_parole:
                self.indice_parola = 0
                self.parola_corrente = self.lista_parole[0]
                self.parola_mascherata = self.maschera_parola(self.parola_corrente)
            else:
                raise ValueError("Il file è vuoto")
            return lista_parole
        raise FileNotFoundError(f"File not found: {nome_file}")

    def carica_parola_da_word(self, testo):
        """
        Load words from a Microsoft Word document (.doc or .docx).
        
        Args:
            testo: Path to the Word document
            
        Returns:
            List of cleaned words, or None if empty
            
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        if os.path.exists(testo):
            self.testo = docx2txt.process(testo)

            # Convert to word list using same logic as txt file loader
            lista_parole = []
            caratteri_da_rimuovere = ',.:;?!-_"\'1234567890'
            for riga in self.testo.splitlines():
                riga_pulita = riga.strip()
                if riga_pulita:
                    parole_nella_riga = riga_pulita.split()
                    for parola in parole_nella_riga:
                        parola_pulita = parola.strip(caratteri_da_rimuovere)
                        if parola_pulita:
                            lista_parole.append(parola_pulita)

            if lista_parole:
                self.lista_parole = lista_parole
                self.indice_parola = 0
                self.parola_corrente = self.lista_parole[0]
                self.parola_mascherata = self.maschera_parola(self.parola_corrente)
                return lista_parole  
            else:
                print("Word document appears to be empty after conversion.")
                return None  
        else:
            raise FileNotFoundError(f"File not found: {testo}")

    # ========================================================================
    # SCREEN FUNCTIONS
    # ========================================================================
    
    def iconifize(self):
        """Minimize the window (iconify)."""
        self.iconify = pygame.display.iconify()
        return self.iconify

    def get_full_screen(self):
        """
        Toggle between normal window and maximized window.
        
        Note: Not true fullscreen, but a maximized resizable window.
        """
        if not self.full_screen:
            # Use global constants defined at module startup
            self.screen_width = SCREEN_MAX_W
            self.screen_height = SCREEN_MAX_H - 50  # Margin for menu bar
            
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height),
                RESIZABLE
            )
            self.full_screen = True
        else:
            # Return to normal window with borders
            self.screen_width = self.base_width
            self.screen_height = self.base_height
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height),
                RESIZABLE
            )
            self.full_screen = False

        # Note: Don't call aggiorna_layout here to avoid duplicate calls
        # It will be called explicitly after this function

    def assicura_layout_size(self):
        """
        Ensure layout is updated when window size changes.
        
        Checks if window size has changed and triggers layout update if needed.
        """
        win_w, win_h = self.screen.get_size()
        if (win_w, win_h) == self.last_layout_size:
            pass
        else:
            self.screen_width = win_w
            self.screen_height = win_h
            self.aggiorna_layout()
            self.last_layout_size = (win_w, win_h)

    def aggiorna_layout(self):
        """
        Update UI layout based on current window size.
        
        Recalculates font sizes, slider positions, and other UI elements
        to scale proportionally with window size.
        """
        new_w, new_h = self.screen.get_size()
        self.screen_width = new_w
        self.screen_height = new_h

        scale = min(
            new_w / self.base_width,
            new_h / self.base_height
        )

        # Current fonts (scaled, not base)
        font_size = int(self.base_font * scale)
        font_ms_size = int(self.base_font_ms * scale)
        self.font = pygame.font.SysFont('Calibri', font_size, bold=False, italic=False)
        self.font_ms = pygame.font.SysFont('Calibri', font_ms_size, bold=False, italic=False)

        # Slider layout: 10% margin on sides, bar is 80% of screen width
        self.x_slider = int(self.screen_width * 0.1)
        self.slider_width = int(self.screen_width * 0.8)
        self.y_slider = int(self.screen_height * 0.1)
        # Knob radius (scaled)
        self.pomello_radius = int(12 * scale)
        self.helper_slider(settings.DURATA_MIN, settings.DURATA_MAX)

        # Instructions screen fonts
        dim_titolo = int(self.base_font * scale)
        dim_ms = int(self.base_font_ms * scale)
        dim_attesa = int(self.base_font_attesa * scale)
        dim_istruzioni = int(self.base_font_istruzioni * scale)
        dim_about = int(self.base_font_about * scale)
        dim_pausa = int(self.base_font_pausa * scale)

        self.font = pygame.font.SysFont('Calibri', dim_titolo, False, False)
        self.font_ms = pygame.font.SysFont('Calibri', dim_ms, False, False)
        self.font_attes = pygame.font.SysFont('Calibri', dim_attesa, False, False)
        self.font_istruzioni = pygame.font.SysFont('Calibri', dim_istruzioni, False, False)
        self.font_about = pygame.font.SysFont('Calibri', dim_about, False, True)
        self.font_pausa = pygame.font.SysFont('Calibri', dim_pausa, True, False)

    # ========================================================================
    # UI ELEMENTS
    # ========================================================================
    
    def caption_window(self):
        """Set the window caption/title."""
        self.caption = pygame.display.set_caption('Tachistostory')
        return self.caption
    
    def get_font(self):
        """Initialize the main font at base size."""
        self.font = pygame.font.SysFont('Calibri', self.base_font, bold=False, italic=False)
        return self.font
    
    def color(self):
        """Fill the screen with background color."""
        if self.screen is not None:
            self.screen.fill(self.bg_color)
            
    def updating(self):
        """Update the display."""
        self.update = pygame.display.update()
        return self.update
    
    def scrivi_testo_centrato(self, parola):
        """
        Render centered text on the screen.
        
        Args:
            parola: The word/text to display
        """
        parola_centrata = self.font.render(parola, True , (39,39,39))
        testo_rect = parola_centrata.get_rect(
            center = (self.screen_width // 2, self.screen_height // 2)
        )
        self.screen.blit(parola_centrata, testo_rect)
    
    def pannello_informativo(self):
        """
        Display information panel at bottom of screen.
        
        Shows current word position and total word count,
        or completion message when finished.
        """
        if self.stato_presentazione != 'fine':
            self.indice_umano = self.indice_parola + 1
            self.totale = len(self.lista_parole)
            self.testo_pannello = self.font.render(f"Word {self.indice_umano}/{self.totale}", True, (39,39,39))
            testo_rect = self.testo_pannello.get_rect(
                centerx=self.screen_width // 2,
                bottom=self.screen_height - 20
            )
            self.screen.blit(self.testo_pannello, testo_rect)
        elif self.stato_presentazione == 'fine':
            self.testo_pannello = self.font.render(f"Parole terminate!", True, (39,39,39))
            testo_rect = self.testo_pannello.get_rect(
                centerx=self.screen_width // 2,
                bottom=self.screen_height - 20
            )
            self.screen.blit(self.testo_pannello, testo_rect)

    # ========================================================================
    # SLIDER
    # ========================================================================
    
    def disegna_slider(self):
        """
        Draw the duration slider with tick marks and current position.
        
        Displays slider bar, tick marks at 0%, 25%, 50%, 75%, 100%,
        duration labels in milliseconds, and draggable knob.
        """
        self.barra = pygame.draw.rect (
            self.screen, 
            (39,39,39), 
            rect=(self.x_slider, self.y_slider-2, self.slider_width, 4 ))   
        for fattore in self.lista_fattori:
            x_tacca = self.x_slider + fattore * self.slider_width
            durata_tacca = settings.DURATA_MIN + fattore * (settings.DURATA_MAX-settings.DURATA_MIN)
            durata_int= int (durata_tacca)
            stringa = self.font_ms.render(f"{durata_int} ms", True, (39,39,39))
            self.tacca = pygame.draw.rect (
            self.screen,
            (39,39,39), 
            rect=(x_tacca - 2, self.y_slider - 8, 2, 16)  
            )
            self.rect = stringa.get_rect()
            self.rect.centerx = x_tacca
            self.rect.top = self.y_slider + 20
            self.screen.blit(stringa, self.rect)
        self.pomello = pygame.draw.circle(
            self.screen, 
            (7, 165, 224), 
            (self.posizione_cursore, self.y_slider),
            self.pomello_radius)

    def helper_slider(self, durata_min, durata_max):
        """
        Calculate slider knob position based on current duration.
        
        Args:
            durata_min: Minimum duration in milliseconds
            durata_max: Maximum duration in milliseconds
        """
        durata = self.durata_parola_ms
        fattore = (durata - durata_min) / (durata_max - durata_min)
        if fattore < 0:
            fattore = 0
        if fattore > 1:
            fattore = 1
        self.posizione_cursore = self.x_slider + fattore * self.slider_width

    # ========================================================================
    # ASSETS & SCREENS
    # ========================================================================
    
    def load_assets(self):
        """Load application assets (logo, icons, etc.)."""
        assets_logo_path = resource_path(os.path.join("assets","Tachistostory_logo.png"))
        self.logo_image = pygame.image.load(assets_logo_path).convert_alpha()

    def disegna_schermata_attesa(self):
        """
        Draw the waiting screen (file drop screen).
        
        Displays logo and instructions to drag & drop a file.
        """
        self.screen.fill(self.menu_bg_color)
        if self.logo_image:
            win_w, win_h = pygame.display.get_window_size()
            self.larghezza_target = win_w * 0.4
            logo_w, logo_h = self.logo_image.get_size()
            scala = self.larghezza_target / logo_w
            new_w = int(logo_w* scala)
            new_h = int(logo_h * scala)
            x_logo = (win_w-new_w) / 2
            y_logo = win_h / 3 - new_h / 2
            logo_scaled = pygame.transform.smoothscale(self.logo_image, (new_w, new_h))
            self.screen.blit(logo_scaled, (x_logo, y_logo))
            font_attesa_file = self.font_attes.render("Drag a .txt or .doc/.docx file here to start", True, self.bg_color)
            font = font_attesa_file.get_rect()
            font.centerx = win_w // 2
            font.top = y_logo + new_h + 40
            self.screen.blit(font_attesa_file, font)
    
    def disegna_schermata_istruzioni(self):
        """
        Draw the instructions screen.
        
        Displays file information, word count, and keyboard command reference.
        """
        # Background
        self.screen.fill(self.menu_bg_color)
        win_w, win_h = self.screen.get_size()

        # Title
        titolo_surf = self.font.render('Tachistoscope Instructions', True, self.bg_color)
        titolo_rect = titolo_surf.get_rect(center=(win_w // 2, win_h // 6))
        self.screen.blit(titolo_surf, titolo_rect)

        # File info
        nome_text = f'Loaded file: "{self.nome_file}"' if self.nome_file else 'Loaded file: -'
        nome_surf = self.font_attes.render(nome_text, True, self.bg_color)
        nome_rect = nome_surf.get_rect(
            centerx = win_w // 2,
            top     = titolo_rect.bottom + 30
        )
        self.screen.blit(nome_surf, nome_rect)

        # Word count
        num_text = f'Number of words: {self.num_parole}' if self.num_parole is not None else 'Number of words: -'
        num_surf = self.font_attes.render(num_text, True, self.bg_color)
        num_rect = num_surf.get_rect(
            centerx = win_w // 2,
            top     = nome_rect.bottom + 10
        )
        self.screen.blit(num_surf, num_rect)

        # Commands legend title
        legenda_surf = self.font_istruzioni.render('Main Commands', True, self.bg_color)
        legenda_rect = legenda_surf.get_rect(
            centerx = win_w // 2,
            top     = num_rect.bottom + 40
        )
        self.screen.blit(legenda_surf, legenda_rect)

        # Command lines
        righe_comandi = [
            '- Press ENTER to start',
            '- SPACE: advance to next word (after mask)',
            '- P: pause / resume presentation',
            '- R: restart from first word',
            '- F: toggle fullscreen',
            '- I: minimize window (iconify)'
        ]

        y = legenda_rect.bottom + 15
        for riga in righe_comandi:
            riga_surf = self.font_istruzioni.render(riga, True, self.bg_color)
            riga_rect = riga_surf.get_rect(
                centerx = win_w // 2,
                top     = y
            )
            self.screen.blit(riga_surf, riga_rect)
            y = riga_rect.bottom + 5

        # About footer
        about = self.font_about.render('Created by Daniele Maurilli | maurillidaniele@gmail.com | github.com/danielemaurilli', True, self.bg_color)
        about_rect = about.get_rect(
            centerx = win_w // 2,
            bottom = win_h - 15
        )
        self.screen.blit (about, about_rect)

    def disegna_schermata_di_pausa(self):
        """
        Draw the pause screen.
        
        Displays 'PAUSE' message in the center of the screen.
        """
        self.screen.fill(self.menu_bg_color)
        win_w, win_h = self.screen.get_size()
        scritta_pausa = self.font_pausa.render('PAUSE', True, self.bg_color)
        scritta_pausa_rect = scritta_pausa.get_rect(
            centerx = win_w // 2,
            top = win_h // 2
        )
        self.screen.blit(scritta_pausa, scritta_pausa_rect)
>>>>>>> 1982162 (Initial commit)
