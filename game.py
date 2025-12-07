"""
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
        self.lista_parole = []
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
