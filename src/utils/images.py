"""
Image utilities for loading and scaling assets.
"""

from __future__ import annotations

from typing import Optional, List

import pygame

from src.utils.paths import resource_path


def load_image_asset(relative_path: str) -> pygame.Surface:
    """Load an image from assets using a PyInstaller-friendly path."""
    return pygame.image.load(resource_path(relative_path)).convert_alpha()


def scale_image_cover(image: pygame.Surface, target_width: int, target_height: int) -> pygame.Surface:
    """
    Scale an image to cover the target area while preserving aspect ratio.
    """
    img_w, img_h = image.get_size()
    img_ratio = img_w / img_h
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        new_h = target_height
        new_w = int(new_h * img_ratio)
    else:
        new_w = target_width
        new_h = int(new_w / img_ratio)

    scaling_factor = max(new_w / img_w, new_h / img_h)

    if scaling_factor > 4:
        scaled = pygame.transform.scale2x(image)
        scaled = pygame.transform.scale2x(scaled)
        scaled = pygame.transform.scale2x(scaled)
        scaled = pygame.transform.smoothscale(scaled, (new_w, new_h))
    elif scaling_factor > 2:
        scaled = pygame.transform.scale2x(image)
        scaled = pygame.transform.scale2x(scaled)
        scaled = pygame.transform.smoothscale(scaled, (new_w, new_h))
    elif scaling_factor > 1.5:
        scaled = pygame.transform.scale2x(image)
        scaled = pygame.transform.smoothscale(scaled, (new_w, new_h))
    else:
        scaled = pygame.transform.smoothscale(image, (new_w, new_h))

    result = pygame.Surface((target_width, target_height))
    result.fill((0, 0, 0))

    x_offset = (target_width - new_w) // 2
    y_offset = (target_height - new_h) // 2
    result.blit(scaled, (x_offset, y_offset))

    return result


def scale_surface_to_fit(surface: pygame.Surface, max_width: int, max_height: int) -> pygame.Surface:
    """Scale a surface to fit within max_width/max_height keeping aspect ratio."""
    src_w, src_h = surface.get_size()
    if src_w == 0 or src_h == 0:
        return surface
    scale = min(max_width / src_w, max_height / src_h)
    if scale <= 0:
        return surface
    new_size = (max(1, int(src_w * scale)), max(1, int(src_h * scale)))
    return pygame.transform.smoothscale(surface, new_size)


def extract_sprite_frames(
    sheet: pygame.Surface,
    num_frames: Optional[int] = None,
    layout: str = "horizontal",
) -> List[pygame.Surface]:
    """Extract individual frames from a sprite sheet."""
    frames: List[pygame.Surface] = []
    sheet_w, sheet_h = sheet.get_size()

    if num_frames is None:
        if layout == "horizontal":
            num_frames = max(1, sheet_w // sheet_h)
        elif layout == "vertical":
            num_frames = max(1, sheet_h // sheet_w)
        else:
            num_frames = 1

    if layout == "horizontal":
        frame_w = sheet_w // num_frames
        frame_h = sheet_h
        for i in range(num_frames):
            x = i * frame_w
            frame = sheet.subsurface((x, 0, frame_w, frame_h))
            frames.append(frame.copy().convert_alpha())
    elif layout == "vertical":
        frame_w = sheet_w
        frame_h = sheet_h // num_frames
        for i in range(num_frames):
            frame = sheet.subsurface((0, i * frame_h, frame_w, frame_h))
            frames.append(frame.copy().convert_alpha())
    else:
        cols = int(num_frames ** 0.5)
        rows = (num_frames + cols - 1) // cols
        frame_w = sheet_w // cols
        frame_h = sheet_h // rows
        for i in range(num_frames):
            row = i // cols
            col = i % cols
            frame = sheet.subsurface((col * frame_w, row * frame_h, frame_w, frame_h))
            frames.append(frame.copy().convert_alpha())

    non_empty_frames = [
        f
        for f in frames
        if f.get_bounding_rect(min_alpha=1).width > 0
        and f.get_bounding_rect(min_alpha=1).height > 0
    ]
    return non_empty_frames or frames
