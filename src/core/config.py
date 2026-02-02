"""
Centralized configuration module.

Keeps all timing, layout, color, and asset path settings in one place.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple
import pygame

import settings


pygame.init()
_SCREEN_INFO = pygame.display.Info()


@dataclass
class DisplayConfig:
    # Use actual screen dimensions
    base_width: int = int(_SCREEN_INFO.current_w * 0.8)
    base_height: int = int(_SCREEN_INFO.current_h * 0.8)
    min_width: int = 800
    min_height: int = 600
    max_width: int = _SCREEN_INFO.current_w
    max_height: int = _SCREEN_INFO.current_h
    fullscreen_menubar_margin: int = 50

    logo_width_ratio: float = 0.4
    slider_margin_ratio: float = 0.1
    slider_width_ratio: float = 0.8

    bg_color: Tuple[int, int, int] = (210, 245, 130)
    menu_bg_color: Tuple[int, int, int] = (0, 157, 198)
    error_color: Tuple[int, int, int] = (200, 30, 30)
    text_color: Tuple[int, int, int] = (39, 39, 39)
    prompt_color: Tuple[int, int, int] = (242, 214, 75)

    slider_knob_color: Tuple[int, int, int] = (7, 165, 224)
    slider_track_color: Tuple[int, int, int] = (39, 39, 39)

    color_key: Tuple[int, int, int] = (0,0,0)

@dataclass
class TimingConfig:
    word_duration_default: int = 220
    word_duration_min: int = settings.DURATA_MIN
    word_duration_max: int = settings.DURATA_MAX
    mask_duration: int = 400

    logo_fade_duration: int = 3500
    intro_table_duration: int = settings.INTRO_TABLE_DURATION
    book_frame_duration: int = 220
    state_fade_duration: int = 1600


@dataclass
class FontConfig:
    font_path: str = "assets/fonts/static/Cinzel-SemiBold.ttf"
    main_size: int = 45
    slider_label_size: int = 13
    menu_size: int = 26
    about_size: int = 14
    instruction_size: int = 18
    pause_size: int = 38


@dataclass
class SliderConfig:
    initial_x: int = 100
    initial_y: int = 50
    base_width: int = 400
    width_scale_factor: float = 0.7
    knob_radius: int = 12
    track_height: int = 4
    tick_factors: Tuple[float, ...] = (0.0, 0.25, 0.5, 0.75, 1.0)


@dataclass
class PathConfig:
    logo_title: str = "assets/logo/tachistostory_title.png"
    window_icon: str = "assets/tachistostory_icon.png"
    bg_menu_table_book: str = "assets/gfx/bg/bg_menu_table_book.png"
    bg_menu_table: str = "assets/gfx/bg/bg_menu_table.png"
    bg_istructions: str = "assets/gfx/bg/bg_istructions.png"
    book_master_sheet: str = "assets/gfx/book/book_master_sheet.png"
    book_open_bg: str = "assets/gfx/book/book_open_idle_64_sheet.png"


@dataclass
class BookConfig:
    bottom_margin: int = -130

@dataclass
class MusicConfig:
    background_music: str = "assets/sounds/fantasy_music.mp3"
    volume: float = 0.2
    loop: bool = True
    

@dataclass
class AppConfig:
    display: DisplayConfig = field(default_factory=DisplayConfig)
    timing: TimingConfig = field(default_factory=TimingConfig)
    font: FontConfig = field(default_factory=FontConfig)
    slider: SliderConfig = field(default_factory=SliderConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    book: BookConfig = field(default_factory=BookConfig)
    music: MusicConfig = field(default_factory=MusicConfig)

config = AppConfig()
