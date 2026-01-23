"""
Instruction state - Shows file info and keyboard commands.
"""

from __future__ import annotations

import pygame
from src.states.base_state import BaseState
from src.core.config import DisplayConfig


class InstructionState(BaseState):
    """Shows file info and instructions screen."""

    COMMANDS = [
        "- Press ENTER to start",
        "- SPACE: advance to next word (after mask)",
        "- P: pause / resume presentation",
        "- R: restart from first word",
        "- F: toggle fullscreen",
        "- I: minimize window (iconify)",
        "- E: reset the game",
        '- "<--": go back to the previous word',
        '- "-->" : go ahead to the next word',
    ]

    def __init__(self, state_machine, name: str = "instruction"):
        super().__init__(state_machine, name)

    @property
    def app(self):
        return self.state_machine.app

    def on_enter(self) -> None:
        pass

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.state_machine.change_state("presentation")

    def update(self, delta_time: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        """Render instruction screen with file info and commands."""
        # Draw background
        if self.app.bg_istructions:
            screen.blit(self.app.bg_istructions, (0, 0))
        else:
            screen.fill(self.app.menu_bg_color)
        win_w, win_h = screen.get_size()

        # Title
        title_surf = self.app.font.render("Tachistoscope Instructions", True, self.app.text_color)
        title_surf.set_colorkey((self.app.color_key))
        title_rect = title_surf.get_rect(center=(win_w // 2, win_h // 6 + 100))
        screen.blit(title_surf, title_rect)

        # File info
        if len(self.app.nome_file) < 25:
            nome_text = f'Loaded file: "{self.app.nome_file}"' if self.app.nome_file else "Loaded file: -"
        else:
            nome_text = f'Loaded file: "{self.app.nome_file[:25]}..."' if self.app.nome_file else "Loaded file: -"
        nome_surf = self.app.font_attes.render(nome_text, True, self.app.text_color)
        nome_surf.set_colorkey(self.app.color_key)
        nome_rect = nome_surf.get_rect(centerx=win_w // 2, top=title_rect.bottom + 30)
        screen.blit(nome_surf, nome_rect)

        # Word count
        num_text = f"Number of words: {self.app.num_parole}" if self.app.num_parole else "Number of words: -"
        num_surf = self.app.font_attes.render(num_text, True, self.app.text_color)
        num_surf.set_colorkey(self.app.color_key)
        num_rect = num_surf.get_rect(centerx=win_w // 2, top=nome_rect.bottom + 10)
        screen.blit(num_surf, num_rect)

        # Commands title
        legend_surf = self.app.font_istruzioni.render("Main Commands", True, self.app.text_color)
        legend_surf.set_colorkey(self.app.color_key)
        legend_rect = legend_surf.get_rect(centerx=win_w // 2, top=num_rect.bottom + 40)
        screen.blit(legend_surf, legend_rect)

        # Command lines
        y = legend_rect.bottom + 15
        for cmd in self.COMMANDS:
            cmd_surf = self.app.font_istruzioni.render(cmd, True, self.app.text_color)
            cmd_surf.set_colorkey(self.app.color_key)
            cmd_rect = cmd_surf.get_rect(centerx=win_w // 2, top=y)
            screen.blit(cmd_surf, cmd_rect)
            y = cmd_rect.bottom + 5

        # About footer
        about = self.app.font_about.render(
            "Created by Daniele Maurilli | maurillidaniele@gmail.com | github.com/danielemaurilli",
            True,
            self.app.text_color,
        )
        about.set_colorkey(self.app.color_key)
        about_rect = about.get_rect(centerx=win_w // 2, bottom=win_h )

        screen.blit(about, about_rect)
