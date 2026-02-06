"""
Asset Manager - Caricamento e gestione asset grafici.
"""
from typing import List, Optional, Tuple

import pygame

from src.core.config import config
from src.utils.images import (
    extract_sprite_frames,
    load_image_asset,
    scale_image_cover,
    scale_surface_to_fit,
)


class AssetManager:
    """Gestisce il caricamento e lo scaling degli asset grafici."""

    def __init__(self):
        # Logo
        self.logo_image: Optional[pygame.Surface] = None
        
        # Background originali (per rescaling)
        self._bg_menu_original: Optional[pygame.Surface] = None
        self._bg_tavolo_original: Optional[pygame.Surface] = None
        self._bg_istructions_original: Optional[pygame.Surface] = None
        self._book_open_original: Optional[pygame.Surface] = None
        
        # Background scalati
        self.bg_menu: Optional[pygame.Surface] = None
        self.bg_tavolo: Optional[pygame.Surface] = None
        self.bg_istructions: Optional[pygame.Surface] = None
        self.book_open_bg: Optional[pygame.Surface] = None
        
        # Book frames
        self.book_frames: List[pygame.Surface] = []
        self.book_frames_scaled: List[pygame.Surface] = []
        self.sprite_libro_chiuso: Optional[pygame.Surface] = None
        
        self._loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def load_all(self, screen_width: int, screen_height: int) -> None:
        """Carica tutti gli asset dell'applicazione."""
        print("[LOADING] Caricamento asset...")
        
        self._load_logo()
        self._load_backgrounds(screen_width, screen_height)
        self._load_book_sprites(screen_width, screen_height)
        
        print("[LOADING] Caricamento asset completato\n")
        self._loaded = True

    def _load_logo(self) -> None:
        """Carica il logo principale."""
        try:
            self.logo_image = load_image_asset(config.paths.logo_title)
            self.logo_image.set_colorkey((0, 0, 0))
            print("  ✓ Logo principale caricato")
        except Exception as e:
            print(f"  ⚠ Logo principale non trovato: {e}")
            self.logo_image = None

    def _load_backgrounds(self, width: int, height: int) -> None:
        """Carica tutti i background."""
        # Menu background
        try:
            self._bg_menu_original = load_image_asset(config.paths.bg_menu_table_book)
            self.bg_menu = scale_image_cover(self._bg_menu_original, width, height)
            print("  ✓ Background menu caricato")
        except Exception as e:
            print(f"  ⚠ Background menu non trovato: {e}")
            self.bg_menu = self._create_placeholder((width, height), (50, 50, 100))

        # Table background
        try:
            self._bg_tavolo_original = load_image_asset(config.paths.bg_menu_table)
            self.bg_tavolo = scale_image_cover(self._bg_tavolo_original, width, height)
            print("  ✓ Background tavolo caricato")
        except Exception as e:
            print(f"  ⚠ Background tavolo non trovato: {e}")
            self.bg_tavolo = self.bg_menu
            if self._bg_menu_original:
                self._bg_tavolo_original = self._bg_menu_original

        # Instructions background
        try:
            self._bg_istructions_original = load_image_asset(config.paths.bg_istructions)
            self.bg_istructions = scale_image_cover(self._bg_istructions_original, width, height)
            print("  ✓ Background istruzioni caricato")
        except Exception as e:
            print(f"  ⚠ Background istruzioni non trovato: {e}")
            self.bg_istructions = self.bg_menu
            if self._bg_menu_original:
                self._bg_istructions_original = self._bg_menu_original

    def _load_book_sprites(self, width: int, height: int) -> None:
        """Carica gli sprite del libro."""
        # Book sprite sheet
        try:
            book_sheet = load_image_asset(config.paths.book_master_sheet)
            self.book_frames = extract_sprite_frames(book_sheet, layout="horizontal")
            for frame in self.book_frames:
                frame.set_colorkey((0, 0, 0))
            self.sprite_libro_chiuso = self.book_frames[0]
            self._scale_book_frames(width, height)
            print(f"  ✓ Sprite libro caricato ({len(self.book_frames)} frame)")
        except Exception as e:
            print(f"  ⚠ Sprite libro non trovato: {e}")
            placeholder = self._create_placeholder((640, 640), (139, 69, 19))
            self.book_frames = [placeholder] * 17
            self.sprite_libro_chiuso = placeholder
            self._scale_book_frames(width, height)

        # Book open background
        try:
            book_open = load_image_asset(config.paths.book_open_bg)
            self._book_open_original = book_open
            self.book_open_bg = scale_image_cover(self._book_open_original, width, height)
            print("  ✓ Background libro aperto caricato")
        except Exception as e:
            print(f"  ⚠ Background libro aperto non trovato: {e}")
            self.book_open_bg = self._create_placeholder((width, height), (255, 248, 220))

    def scale_backgrounds(self, width: int, height: int) -> None:
        """Riscala tutti i background alla nuova dimensione."""
        if self._bg_menu_original:
            self.bg_menu = scale_image_cover(self._bg_menu_original, width, height)
        if self._bg_tavolo_original:
            self.bg_tavolo = scale_image_cover(self._bg_tavolo_original, width, height)
        if self._bg_istructions_original:
            self.bg_istructions = scale_image_cover(self._bg_istructions_original, width, height)
        if self._book_open_original:
            self.book_open_bg = scale_image_cover(self._book_open_original, width, height)

    def scale_book_frames(self, width: int, height: int) -> None:
        """Riscala i frame del libro alla nuova dimensione."""
        self._scale_book_frames(width, height)

    def _scale_book_frames(self, width: int, height: int) -> None:
        """Riscala internamente i frame del libro."""
        if not self.book_frames:
            return
        max_w = int(width * 1.25)
        max_h = int(height * 1.25)
        self.book_frames_scaled = []
        for frame in self.book_frames:
            scaled = scale_surface_to_fit(frame, max_w, max_h)
            scaled.set_colorkey((0, 0, 0))
            self.book_frames_scaled.append(scaled)
        if self.book_frames_scaled:
            self.sprite_libro_chiuso = self.book_frames_scaled[0]

    def _create_placeholder(
        self, size: Tuple[int, int], color: Tuple[int, int, int]
    ) -> pygame.Surface:
        """Crea un placeholder colorato quando un asset manca."""
        surface = pygame.Surface(size)
        surface.fill(color)
        pygame.draw.line(surface, (255, 0, 0), (0, 0), size, 3)
        pygame.draw.line(surface, (255, 0, 0), (0, size[1]), (size[0], 0), 3)
        return surface.convert()
