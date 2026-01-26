"""
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
from src.loaders.file_loader import FileLoader, LoadedText, LoadMusic
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
pygame.mixer.init()

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

        #===================== MUSIC ========================================
        self.background_music = config.music.background_music
        self.loop = config.music.loop
        self.volume = config.music.volume

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

    def load_music(self, path: str) -> None:
        """Load and start background music."""
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(config.music.volume)
        loops = -1 if config.music.loop else 0
        pygame.mixer.music.play(loops=loops)
        self.background_music = path


    def reset(self) -> None:
        """Reset game to initial state."""
        self.stato_presentazione = State.FILE
        self.file_caricato = False
        self.nome_file = None
        self.num_parole = None
        self.lista_parole = []
        self.indice_parola = 0
        self.parola_corrente = ""
        self.parola_mascherata = ""
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
    # MUSIC
    # ========================================================================

    def music_exe(self):
        """Load and execute music."""
        try:
            self.load_music(config.music.background_music)
        except Exception as e:
            print(f"⚠ Errore caricamento musica: {e}")

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
