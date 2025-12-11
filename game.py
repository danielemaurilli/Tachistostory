"""
Tachistostory - Core Game Logic
Main tachistoscope application class with word presentation and display logic.
"""

import pygame
from pygame.locals import RESIZABLE
import sys
import os
import docx2txt
import settings 
from enum import Enum, auto
from typing import List, Optional, Tuple

# Initialize Pygame BEFORE creating the class
pygame.init()
pygame.font.init()

# Get screen dimensions before creating any window
_SCREEN_INFO = pygame.display.Info()
SCREEN_MAX_W = _SCREEN_INFO.current_w
SCREEN_MAX_H = _SCREEN_INFO.current_h

# Layout constants
LOGO_WIDTH_RATIO = 0.4
SLIDER_MARGIN_RATIO = 0.1
SLIDER_WIDTH_RATIO = 0.8
FULLSCREEN_MENUBAR_MARGIN = 50
PUNCTUATION_CHARS = ',.:;?!-_"\''
KEPT_PUNCTUATION = ':.,;,!?'


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


def load_image_asset(relative_path: str) -> pygame.Surface:
    """Load an image from assets using a PyInstaller-friendly path."""
    return pygame.image.load(resource_path(relative_path)).convert_alpha()


class Error(Enum):
    """
    Docstring per Error
    """
    EMPTY = auto()
    EXCEPTION = auto()
    INVALID = auto ()

class State(Enum):
    """Application states for the tachistoscope."""
    FILE = auto()         # Waiting for file
    ISTRUCTION = auto()   # Instructions screen
    SHOW_WORD = auto()    # Displaying word
    SHOW_MASK = auto()    # Displaying mask
    END = auto()          # Presentation finished


class Tachistostory:
    """Main tachistoscope application class."""
    
    def __init__(self):
        # Screen setup
        self.screen: Optional[pygame.Surface] = None
        self.base_width = 600
        self.base_height = 800
        self.screen_width = self.base_width
        self.screen_height = self.base_height

        # Color settings
        self.bg_color = (210, 245, 130)
        self.menu_bg_color = (0, 157, 198)
        self.error_color = (200, 30, 30)
        
        # Logo
        self.logo_image: Optional[pygame.Surface] = None
        self.logo_icon: Optional[pygame.Surface] = None
        
        # Instructions screen
        self.nome_file: Optional[str] = None
        self.num_parole: Optional[int] = None

        # Base font
        self.font: Optional[pygame.font.Font] = None

        # Presentation state
        self.stato_presentazione = State.FILE
        
        # File loaded flag
        self.file_caricato = False
        self.percorso_file: Optional[str] = None

        # Word presentation duration
        self.tempo_inizio_stato: Optional[int] = None
        self.durata_parola_ms = 220
        self.durata_maschera_ms = 400
        
        # Word list initialization
        self.lista_parole: List[str] = []
        self.indice_parola = 0
        self.parola_corrente = ""
        self.parola_mascherata = ""

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
        self.font_attes = pygame.font.SysFont('Helvetica', self.base_font_attesa, bold=False, italic=True)
        self.font_ms = pygame.font.SysFont('Helvetica', self.base_font_ms, bold=False, italic=False)
        self.font_istruzioni = pygame.font.SysFont('Helvetica', self.base_font_istruzioni, bold=False, italic=False)
        self.font_about = pygame.font.SysFont('Helvetica', self.base_font_about, bold=False, italic=True)
        self.font_pausa = pygame.font.SysFont('Helvetica', self.base_font_pausa, True, False)

        # Error message
        self.error_text: Optional[pygame.Surface] = None
        self.invalid_text: Optional[pygame.Surface] = None
        self.empty_text: Optional[pygame.Surface] = None
        self.tempo_errore = 0
        self.mostra_errore = False
        self.messaggio_errore = ""

        # Full-screen toggle
        self.full_screen = False

        # Layout size tracking
        self.last_layout_size: Tuple[int, int] = (self.screen_width, self.screen_height)

    # ========================================================================
    # WINDOW SETUP
    # ========================================================================
    
    def get_screen(self) -> pygame.Surface:
        """Initialize and return the main display window."""
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height], RESIZABLE)
        self.logo_icon = load_image_asset(os.path.join("assets", "Tachistostory.png"))
        pygame.display.set_icon(self.logo_icon)
        return self.screen
    
    # ========================================================================
    # WORD MASKING
    # ========================================================================
    
    def maschera_parola(self, parola: str) -> str:
        """
        Mask a word by replacing letters and digits with '#'.
        
        Args:
            parola: The word to mask
            
        Returns:
            Masked string with '#' replacing alphanumeric characters
        """
        masked_chars = []
        for char in parola:
            if char in KEPT_PUNCTUATION or char == " ":
                masked_chars.append(char)
            elif char.isalnum():
                masked_chars.append("#")
            else:
                masked_chars.append("#")
        return "".join(masked_chars)

    def go(self):
        """
        Go ahead to the next word with '->'
        """
        if self.lista_parole:
            aug = self.indice_parola + 1
            if aug < len(self.lista_parole):   
                self.indice_parola = aug
                self.parola_corrente = self.lista_parole[aug]
                self.parola_mascherata = self.maschera_parola(self.parola_corrente)
   

    def back(self):
        """
        Go back to the back word with '<-'
        """
        if self.lista_parole:
            aug = self.indice_parola - 1
            if aug < len(self.lista_parole) and aug >= -1:   
                self.indice_parola = aug
                self.parola_corrente = self.lista_parole[aug]
                self.parola_mascherata = self.maschera_parola(self.parola_corrente)
   
            
    # ========================================================================
    # FILE LOADING
    # ========================================================================
    
    def _pulisci_e_carica_parole(self, testo: str) -> List[str]:
        """
        Extract and clean words from text content.
        
        Args:
            testo: Raw text content
            
        Returns:
            List of cleaned words
        """
        lista_parole = []
        for riga in testo.splitlines():
            riga_pulita = riga.strip()
            if riga_pulita:
                parole_nella_riga = riga_pulita.split()
                for parola in parole_nella_riga:
                    # Remove punctuation and digits from word edges
                    parola_pulita = parola.strip(PUNCTUATION_CHARS + '1234567890')
                    if parola_pulita:
                        lista_parole.append(parola_pulita)
        return lista_parole
    
    def carica_parola_da_txt(self, nome_file: str) -> List[str]:
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
        if not os.path.exists(nome_file):
            raise FileNotFoundError(f"File not found: {nome_file}")
            
        with open(nome_file, 'r', encoding='utf-8') as file:
            testo = file.read()
        
        lista_parole = self._pulisci_e_carica_parole(testo)
        
        if not lista_parole:
            raise ValueError("Il file è vuoto")
        
        self.lista_parole = lista_parole
        self.indice_parola = 0
        self.parola_corrente = self.lista_parole[0]
        self.parola_mascherata = self.maschera_parola(self.parola_corrente)
        
        return lista_parole

    def carica_parola_da_word(self, percorso: str) -> List[str]:
        """
        Load words from a Microsoft Word document (.doc or .docx).
        
        Args:
            percorso: Path to the Word document
            
        Returns:
            List of cleaned words
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the document is empty
        """
        if not os.path.exists(percorso):
            raise FileNotFoundError(f"File not found: {percorso}")
        
        testo = docx2txt.process(percorso)
        lista_parole = self._pulisci_e_carica_parole(testo)
        
        if not lista_parole:
            raise ValueError("Word document appears to be empty after conversion.")
        
        self.lista_parole = lista_parole
        self.indice_parola = 0
        self.parola_corrente = self.lista_parole[0]
        self.parola_mascherata = self.maschera_parola(self.parola_corrente)
        
        return lista_parole
    
    def reset(self):
        self.stato_presentazione = State.FILE
        self.file_caricato = False
        self.percorso_file = None
        self.nome_file = None
        self.num_parole = None
        self.lista_parole = []
        self.indice_parola = 0
        self.parola_corrente = ""
        self.parola_mascherata = ""
        self.in_pausa = False
        self.mostra_errore = False

    # ========================================================================
    # SCREEN FUNCTIONS
    # ========================================================================
    
    def iconifize(self) -> None:
        """Minimize the window (iconify)."""
        pygame.display.iconify()

    def get_full_screen(self) -> None:
        """
        Toggle between normal window and maximized window.
        
        Note: Not true fullscreen, but a maximized resizable window.
        """
        if not self.full_screen:
            # Use global constants defined at module startup
            self.screen_width = SCREEN_MAX_W
            self.screen_height = SCREEN_MAX_H - FULLSCREEN_MENUBAR_MARGIN
            
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

    def assicura_layout_size(self) -> None:
        """
        Ensure layout is updated when window size changes.
        
        Checks if window size has changed and triggers layout update if needed.
        """
        if self.screen is None:
            return
            
        win_w, win_h = self.screen.get_size()
        if (win_w, win_h) != self.last_layout_size:
            self.screen_width = win_w
            self.screen_height = win_h
            self.aggiorna_layout()
            self.last_layout_size = (win_w, win_h)

    def aggiorna_layout(self) -> None:
        """
        Update UI layout based on current window size.
        
        Recalculates font sizes, slider positions, and other UI elements
        to scale proportionally with window size.
        """
        if self.screen is None:
            return
            
        new_w, new_h = self.screen.get_size()
        self.screen_width = new_w
        self.screen_height = new_h

        scale = min(
            new_w / self.base_width,
            new_h / self.base_height
        )

        self._aggiorna_fonts(scale)
        self._aggiorna_slider_layout(scale)

    def _aggiorna_fonts(self, scale: float) -> None:
        """Update font sizes based on scale factor."""
        # Main fonts
        font_size = int(self.base_font * scale)
        font_ms_size = int(self.base_font_ms * scale)
        self.font = pygame.font.SysFont('Helvetica', font_size, bold=False, italic=False)
        self.font_ms = pygame.font.SysFont('Helvetica', font_ms_size, bold=False, italic=False)

        # Screen-specific fonts
        dim_attesa = int(self.base_font_attesa * scale)
        dim_istruzioni = int(self.base_font_istruzioni * scale)
        dim_about = int(self.base_font_about * scale)
        dim_pausa = int(self.base_font_pausa * scale)

        self.font_attes = pygame.font.SysFont('Helvetica', dim_attesa, False, True)
        self.font_istruzioni = pygame.font.SysFont('Helvetica', dim_istruzioni, False, False)
        self.font_about = pygame.font.SysFont('Helvetica', dim_about, False, True)
        self.font_pausa = pygame.font.SysFont('Helvetica', dim_pausa, True, False)

    def _aggiorna_slider_layout(self, scale: float) -> None:
        """Update slider layout based on scale factor."""
        self.x_slider = int(self.screen_width * SLIDER_MARGIN_RATIO)
        self.slider_width = int(self.screen_width * SLIDER_WIDTH_RATIO)
        self.y_slider = int(self.screen_height * SLIDER_MARGIN_RATIO)
        self.pomello_radius = int(12 * scale)
        self.helper_slider(settings.DURATA_MIN, settings.DURATA_MAX)

    # ========================================================================
    # UI ELEMENTS
    # ========================================================================
    
    def caption_window(self) -> None:
        """Set the window caption/title."""
        pygame.display.set_caption('Tachistostory')
    
    def get_font(self) -> pygame.font.Font:
        """Initialize the main font at base size."""
        self.font = pygame.font.SysFont('Helvetica', self.base_font, bold=False, italic=False)
        return self.font
    
    def color(self) -> None:
        """Fill the screen with background color."""
        if self.screen is not None:
            self.screen.fill(self.bg_color)
            
    def updating(self) -> None:
        """Update the display."""
        pygame.display.update()
    
    def scrivi_testo_centrato(self, parola: str) -> None:
        """
        Render centered text on the screen.
        
        Args:
            parola: The word/text to display
        """
        if self.screen is None or self.font is None:
            return
            
        parola_centrata = self.font.render(parola, True, (39, 39, 39))
        testo_rect = parola_centrata.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2)
        )
        self.screen.blit(parola_centrata, testo_rect)
    
    def pannello_informativo(self) -> None:
        """
        Display information panel at bottom of screen.
        
        Shows current word position and total word count,
        or completion message when finished.
        """
        if self.screen is None or self.font is None:
            return
            
        if self.stato_presentazione != State.END:
            indice_umano = self.indice_parola + 1
            totale = len(self.lista_parole)
            testo_pannello = self.font.render(
                f"Word {indice_umano}/{totale}", 
                True, 
                (39, 39, 39)
            )
        else:
            testo_pannello = self.font.render(
                "Parole terminate!", 
                True, 
                (39, 39, 39)
            )
        
        testo_rect = testo_pannello.get_rect(
            centerx=self.screen_width // 2,
            bottom=self.screen_height - 20
        )
        self.screen.blit(testo_pannello, testo_rect)

    def error_message(self, e: Exception) -> None:
        """Display error message on screen."""
        if self.screen is None:
            return
            
        win_w, win_h = self.screen.get_size()
        self.mostra_errore = True
        self.error_text = self.font_attes.render(
            f"An error occurred: {e}, please try again", 
            True, 
            self.error_color
        )
        error_text_rect = self.error_text.get_rect(
            centerx=win_w // 2,
            bottom=self.screen_height - win_h // 3
        )
        self.screen.blit(self.error_text, error_text_rect)

    def invalid_message(self, file: str) -> None:
        """Display invalid file message on screen."""
        if self.screen is None:
            return
            
        win_w, win_h = self.screen.get_size()
        self.mostra_errore = True
        self.invalid_text = self.font_attes.render(
            f'{file} is not valid. Please try again', 
            True, 
            self.error_color
        )
        invalid_text_rect = self.invalid_text.get_rect(
            centerx=win_w // 2,
            bottom=self.screen_height - win_h // 3
        )
        self.screen.blit(self.invalid_text, invalid_text_rect)

    def empty_message(self) -> None:
        """Display empty document message on screen."""
        if self.screen is None:
            return
            
        win_w, win_h = self.screen.get_size()
        self.mostra_errore = True
        self.empty_text = self.font_attes.render(
            'Document not readable or empty. Please try again', 
            True, 
            self.error_color
        )
        empty_text_rect = self.empty_text.get_rect(
            centerx=win_w // 2,
            bottom=self.screen_height - win_h // 3
        )
        self.screen.blit(self.empty_text, empty_text_rect)

    # ========================================================================
    # SLIDER
    # ========================================================================
    
    def disegna_slider(self) -> None:
        """
        Draw the duration slider with tick marks and current position.
        
        Displays slider bar, tick marks at 0%, 25%, 50%, 75%, 100%,
        duration labels in milliseconds, and draggable knob.
        """
        if self.screen is None:
            return
            
        # Draw slider bar
        pygame.draw.rect(
            self.screen, 
            (39, 39, 39), 
            rect=(self.x_slider, self.y_slider - 2, self.slider_width, 4)
        )
        
        # Draw tick marks and labels
        for fattore in self.lista_fattori:
            x_tacca = self.x_slider + fattore * self.slider_width
            durata_tacca = settings.DURATA_MIN + fattore * (settings.DURATA_MAX - settings.DURATA_MIN)
            durata_int = int(durata_tacca)
            
            stringa = self.font_ms.render(f"{durata_int} ms", True, (39, 39, 39))
            pygame.draw.rect(
                self.screen,
                (39, 39, 39), 
                rect=(x_tacca - 2, self.y_slider - 8, 2, 16)
            )
            
            rect = stringa.get_rect()
            rect.centerx = x_tacca
            rect.top = self.y_slider + 20
            self.screen.blit(stringa, rect)
        
        # Draw knob
        pygame.draw.circle(
            self.screen, 
            (7, 165, 224), 
            (int(self.posizione_cursore), self.y_slider),
            self.pomello_radius
        )

    def helper_slider(self, durata_min: float, durata_max: float) -> None:
        """
        Calculate slider knob position based on current duration.
        
        Args:
            durata_min: Minimum duration in milliseconds
            durata_max: Maximum duration in milliseconds
        """
        durata = self.durata_parola_ms
        fattore = (durata - durata_min) / (durata_max - durata_min)
        fattore = max(0.0, min(1.0, fattore))  # Clamp between 0 and 1
        self.posizione_cursore = self.x_slider + fattore * self.slider_width

    # ========================================================================
    # ASSETS & SCREENS
    # ========================================================================
    
    def load_assets(self) -> None:
        """Load application assets (logo, icons, etc.)."""
        self.logo_image = load_image_asset(os.path.join("assets", "Tachistostory_logo.png"))

    def disegna_schermata_attesa(self) -> None:
        """
        Draw the waiting screen (file drop screen).
        
        Displays logo and instructions to drag & drop a file.
        """
        if self.screen is None:
            return
            
        self.screen.fill(self.menu_bg_color)
        
        if self.logo_image:
            win_w, win_h = pygame.display.get_window_size()
            larghezza_target = win_w * LOGO_WIDTH_RATIO
            logo_w, logo_h = self.logo_image.get_size()
            scala = larghezza_target / logo_w
            new_w = int(logo_w * scala)
            new_h = int(logo_h * scala)
            x_logo = (win_w - new_w) / 2
            y_logo = win_h / 3 - new_h / 2
            
            logo_scaled = pygame.transform.smoothscale(self.logo_image, (new_w, new_h))
            self.screen.blit(logo_scaled, (x_logo, y_logo))
            
            font_attesa_file = self.font_attes.render(
                "Drag a .txt or .doc/.docx file here to start", 
                True, 
                self.bg_color
            )
            font_rect = font_attesa_file.get_rect()
            font_rect.centerx = win_w // 2
            font_rect.top = y_logo + new_h + 40
            self.screen.blit(font_attesa_file, font_rect)
    
    def disegna_schermata_istruzioni(self) -> None:
        """
        Draw the instructions screen.
        
        Displays file information, word count, and keyboard command reference.
        """
        if self.screen is None:
            return
            
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
            centerx=win_w // 2,
            top=titolo_rect.bottom + 30
        )
        self.screen.blit(nome_surf, nome_rect)

        # Word count
        num_text = f'Number of words: {self.num_parole}' if self.num_parole is not None else 'Number of words: -'
        num_surf = self.font_attes.render(num_text, True, self.bg_color)
        num_rect = num_surf.get_rect(
            centerx=win_w // 2,
            top=nome_rect.bottom + 10
        )
        self.screen.blit(num_surf, num_rect)

        # Commands legend title
        legenda_surf = self.font_istruzioni.render('Main Commands', True, self.bg_color)
        legenda_rect = legenda_surf.get_rect(
            centerx=win_w // 2,
            top=num_rect.bottom + 40
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
                centerx=win_w // 2,
                top=y
            )
            self.screen.blit(riga_surf, riga_rect)
            y = riga_rect.bottom + 5

        # About footer
        about = self.font_about.render(
            'Created by Daniele Maurilli | maurillidaniele@gmail.com | github.com/danielemaurilli', 
            True, 
            self.bg_color
        )
        about_rect = about.get_rect(
            centerx=win_w // 2,
            bottom=win_h - 15
        )
        self.screen.blit(about, about_rect)

    def disegna_schermata_di_pausa(self) -> None:
        """
        Draw the pause screen.
        
        Displays 'PAUSE' message in the center of the screen.
        """
        if self.screen is None:
            return
            
        self.screen.fill(self.menu_bg_color)
        win_w, win_h = self.screen.get_size()
        scritta_pausa = self.font_pausa.render('PAUSE', True, self.bg_color)
        scritta_pausa_rect = scritta_pausa.get_rect(
            centerx=win_w // 2,
            top=win_h // 2
        )
        self.screen.blit(scritta_pausa, scritta_pausa_rect)
