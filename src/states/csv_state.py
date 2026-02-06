"""
CSV Export State - asks user to export session logs after presentation ends.
"""

from __future__ import annotations

import pygame
from src.states.base_state import BaseState
from src.core.config import config


class CsvState(BaseState):
    """Shows end-of-session screen and asks if user wants to export CSV/JSON logs."""

    # Export status
    ASKING = "asking"
    EXPORTING = "exporting"
    SUCCESS = "success"
    ERROR = "error"

    def __init__(self, state_machine, name: str = "csv_export"):
        super().__init__(state_machine, name)
        self.status: str = self.ASKING
        self.message: str = ""
        self.exported_paths: dict[str, object] = {}

        # Button rects (calculated in _update_layout)
        self.yes_button_rect: pygame.Rect = pygame.Rect(0, 0, 180, 55)
        self.no_button_rect: pygame.Rect = pygame.Rect(0, 0, 180, 55)
        self.done_button_rect: pygame.Rect = pygame.Rect(0, 0, 280, 65)

        # Colors
        self.yes_color = (60, 140, 60)
        self.yes_hover = (80, 170, 80)
        self.no_color = (160, 60, 60)
        self.no_hover = (190, 80, 80)
        self.done_color = (80, 80, 80)
        self.done_hover = (110, 110, 110)
        self.button_text_color = (255, 255, 255)

    @property
    def app(self):
        return self.state_machine.app

    def on_enter(self) -> None:
        self.status = self.ASKING
        self.message = ""
        self.exported_paths = {}
        if self.app and self.app.screen:
            win_w, win_h = self.app.screen.get_size()
            self._update_layout(win_w, win_h)

    def _update_layout(self, win_w: int, win_h: int) -> None:
        """Update button positions based on window size."""
        center_x = win_w // 2
        button_y = int(win_h * 0.55)
        gap = 30

        self.yes_button_rect = pygame.Rect(
            center_x - 180 - gap // 2, button_y + 80 , 180, 55
        )
        self.no_button_rect = pygame.Rect(
            center_x + gap // 2, button_y + 80 , 180, 55
        )
        self.done_button_rect = pygame.Rect(
            center_x - 140, int(win_h * 0.75), 280, 65
        )

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.status == self.ASKING:
                    if self.yes_button_rect.collidepoint(event.pos):
                        self._do_export()
                    elif self.no_button_rect.collidepoint(event.pos):
                        self._skip_export()
                elif self.status in (self.SUCCESS, self.ERROR):
                    if self.done_button_rect.collidepoint(event.pos):
                        self._go_to_file_selection()

            elif event.type == pygame.KEYDOWN:
                if self.status == self.ASKING:
                    if event.key == pygame.K_y or event.key == pygame.K_RETURN:
                        self._do_export()
                    elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                        self._skip_export()
                elif self.status in (self.SUCCESS, self.ERROR):
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_ESCAPE):
                        self._go_to_file_selection()

    def _do_export(self) -> None:
        """Export session logs via SessionController."""
        self.status = self.EXPORTING
        try:
            results = self.app.controller.export_all()
            self.exported_paths = results
            self.status = self.SUCCESS
            self.message = "Export completed!"
            print("  ✓ CSV/JSON export completed:")
            for key, path in results.items():
                print(f"    - {key}: {path}")
        except Exception as e:
            self.status = self.ERROR
            self.message = f"Export failed: {e}"
            print(f"  ⚠ Export failed: {e}")

    def _skip_export(self) -> None:
        """Skip export and go back to file selection."""
        print("  → Export skipped by user")
        self._go_to_file_selection()

    def _go_to_file_selection(self) -> None:
        """Reset and go back to file selection for a new session."""
        self.app.reset()
        if self.state_machine:
            self.state_machine.change_state("file_selection")

    def update(self, delta_time: float) -> None:
        # Recalculate layout on resize
        if self.app and self.app.screen:
            win_w, win_h = self.app.screen.get_size()
            self._update_layout(win_w, win_h)

    def render(self, screen: pygame.Surface) -> None:
        # Background
        if self.app.bg_istructions:
            screen.blit(self.app.bg_istructions, (0, 0))
        else:
            screen.fill(self.app.bg_color)

        if self._is_fade_active():
            return

        win_w, win_h = screen.get_size()

        if self.status == self.ASKING:
            self._render_asking(screen, win_w, win_h)
        elif self.status == self.SUCCESS:
            self._render_success(screen, win_w, win_h)
        elif self.status == self.ERROR:
            self._render_error(screen, win_w, win_h)

    def _render_asking(self, screen: pygame.Surface, win_w: int, win_h: int) -> None:
        """Render the export question UI."""
        # Title
        title = self.app.font.render("End of list", True, config.display.text_color)
        title.set_colorkey(self.app.color_key)
        title_rect = title.get_rect(centerx=win_w // 2, centery=int(win_h * 0.30))
        screen.blit(title, title_rect)

        # Question
        question = self.app.font_attes.render(
            "Do you want to export the session data?",
            True, config.display.text_color
        )
        question.set_colorkey(self.app.color_key)
        q_rect = question.get_rect(centerx=win_w // 2, centery=int(win_h * 0.42))
        screen.blit(question, q_rect)

        # Session summary info
        session = self.app.context.session
        info_lines = [
            f"Words presented: {session.total_words}",
            f"Participant: {session.participant_display_name or 'N/A'}",
            f"File: {session.input_file_name or 'N/A'}",
        ]
        y_info = int(win_h * 0.48)
        for line in info_lines:
            info_surf = self.app.font_about.render(line, True, config.display.text_color)
            info_surf.set_colorkey(self.app.color_key)
            info_rect = info_surf.get_rect(centerx=win_w // 2, top=y_info)
            screen.blit(info_surf, info_rect)
            y_info = info_rect.bottom + 4

        # Yes / No buttons
        self._render_button(screen, self.yes_button_rect, "Yes (Y)",
                            self.yes_color, self.yes_hover)
        self._render_button(screen, self.no_button_rect, "No (N)",
                            self.no_color, self.no_hover)

    def _render_success(self, screen: pygame.Surface, win_w: int, win_h: int) -> None:
        """Render export success screen."""
        # Title
        title = self.app.font.render("Export completed!", True, config.display.text_color)
        title.set_colorkey(self.app.color_key)
        title_rect = title.get_rect(centerx=win_w // 2, centery=int(win_h * 0.25))
        screen.blit(title, title_rect)

        # List exported files
        y = int(win_h * 0.35)
        for key, path in self.exported_paths.items():
            label = key.replace("_", " ").title()
            file_name = str(path).split("/")[-1] if "/" in str(path) else str(path)
            text = f"✓ {label}: {file_name}"
            surf = self.app.font_about.render(text, True, config.display.text_color)
            surf.set_colorkey(self.app.color_key)
            rect = surf.get_rect(centerx=win_w // 2, top=y)
            screen.blit(surf, rect)
            y = rect.bottom + 6

        # Output directory
        out_dir = str(self.app.context.output_dir)
        dir_surf = self.app.font_about.render(
            f"Saved to: {out_dir}", True, config.display.text_color
        )
        dir_surf.set_colorkey(self.app.color_key)
        dir_rect = dir_surf.get_rect(centerx=win_w // 2, top=y + 15)
        screen.blit(dir_surf, dir_rect)

        # Done button
        self._render_button(screen, self.done_button_rect, "Continue (ENTER)",
                            self.done_color, self.done_hover)

    def _render_error(self, screen: pygame.Surface, win_w: int, win_h: int) -> None:
        """Render export error screen."""
        # Title
        title = self.app.font.render("Export failed", True, (200, 50, 30))
        title.set_colorkey(self.app.color_key)
        title_rect = title.get_rect(centerx=win_w // 2, centery=int(win_h * 0.30))
        screen.blit(title, title_rect)

        # Error message
        err_surf = self.app.font_attes.render(
            self.message, True, config.display.text_color
        )
        err_surf.set_colorkey(self.app.color_key)
        err_rect = err_surf.get_rect(centerx=win_w // 2, centery=int(win_h * 0.45))
        screen.blit(err_surf, err_rect)

        # Done button
        self._render_button(screen, self.done_button_rect, "Continue (ENTER)",
                            self.done_color, self.done_hover)

    def _render_button(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        text: str,
        bg_color: tuple[int, int, int],
        hover_color: tuple[int, int, int],
    ) -> None:
        """Render a button with hover effect."""
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)
        color = hover_color if is_hover else bg_color

        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255, 60), rect, 2, border_radius=8)

        text_surf = self.app.font_attes.render(text, True, self.button_text_color)
        text_surf.set_colorkey(self.app.color_key)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    def _is_fade_active(self) -> bool:
        """Check if global fade transition is active."""
        return hasattr(self.app, "fade_active") and self.app.fade_active
