"""
Participant Form State - handles participant name/code entry and selection.
"""
from __future__ import annotations

import pygame
from typing import TYPE_CHECKING

from src.states.base_state import BaseState
from src.core.form_manager import FormModality
from src.core.form_state import FormState

if TYPE_CHECKING:
    from src.core.state_machine import StateMachine
    from src.core.GameContext import GameContext


class ParticipantFormState(BaseState):
    """State for participant name/code entry and selection.
    
    Supports two modalities:
    - NEW: user types a participant name/code
    - EXISTING: user selects from saved participants
    """

    def __init__(self, state_machine: StateMachine, context: GameContext, name: str = "participant_form"):
        super().__init__(state_machine, name)
        self.context = context
        
        # UI positions (will be updated in on_enter)
        self.input_rect: pygame.Rect = pygame.Rect(0, 0, 400, 50)
        self.submit_button_rect: pygame.Rect = pygame.Rect(0, 0, 200, 50)
        self.toggle_button_rect: pygame.Rect = pygame.Rect(0, 0, 200, 40)
        self.list_start_y: int = 0
        self.list_item_height: int = 40
        
        # Colors (designed for book_open_bg background)
        self.bg_color = (240, 240, 240)
        self.text_color = (60, 40, 30)
        self.input_bg = (255, 250, 240, 200)
        self.input_border = (120, 90, 60)
        self.input_focus_border = (160, 110, 50)
        self.error_color = (200, 50, 30)
        self.button_bg = (100, 75, 50)
        self.button_hover = (130, 100, 65)
        self.button_text = (255, 250, 240)
        self.list_item_bg = (255, 250, 240, 180)
        self.list_item_hover = (245, 235, 215)
        self.list_item_selected = (140, 105, 60)
        self.delete_btn_bg = (180, 50, 40)
        self.delete_btn_hover = (210, 70, 55)
        self.delete_btn_text = (255, 255, 255)
        
        # Delete button rects (one per list item, rebuilt each frame)
        self.delete_btn_rects: list[pygame.Rect] = []
        
        # Scaled list width (updated in _update_layout)
        self.list_width: int = 400
        
        # Input focus
        self.input_focused: bool = False

    @property
    def app(self):
        """Access main app via state machine."""
        return self.state_machine.app if self.state_machine else None

    @property
    def form_manager(self):
        """Access form manager from context."""
        return self.context.form_manager

    def on_enter(self) -> None:
        """Setup when entering state."""
        # Load existing participants if entering EXISTING mode
        if self.form_manager.form_modality == FormModality.EXISTING:
            self.form_manager.load_users(self.context.registry)
        
        # Calculate UI positions based on screen size
        if self.app and self.app.screen:
            win_w, win_h = self.app.screen.get_size()
            self._update_layout(win_w, win_h)

    def _update_layout(self, win_w: int, win_h: int) -> None:
        """Update UI element positions based on window size."""
        center_x = win_w // 2
        
        # Scale factors relative to a 1024x768 reference
        sx = win_w / 1024
        sy = win_h / 768
        s = min(sx, sy)  # uniform scale
        
        # Input field (centered, upper third)
        input_w = max(int(400 * sx), 200)
        input_h = max(int(50 * sy), 30)
        self.input_rect = pygame.Rect(
            center_x - input_w // 2, 
            win_h // 3 - input_h // 2, 
            input_w, 
            input_h
        )
        
        # Submit button (below input)
        submit_w = max(int(300 * sx), 150)
        submit_h = max(int(60 * sy), 35)
        self.submit_button_rect = pygame.Rect(
            center_x - submit_w // 2,
            self.input_rect.bottom + int(30 * sy),
            submit_w,
            submit_h
        )
        
        # Toggle button (bottom)
        toggle_w = max(int(320 * sx), 160)
        toggle_h = max(int(70 * sy), 40)
        self.toggle_button_rect = pygame.Rect(
            center_x - toggle_w // 2,
            win_h - toggle_h - int(50 * sy),
            toggle_w,
            toggle_h
        )
        
        # List display area (for EXISTING mode)
        self.list_start_y = win_h // 4
        self.list_item_height = max(int(40 * sy), 25)
        self.list_width = max(int(400 * sx), 220)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Handle user input events."""
        # Handle resize events first
        for event in events:
            if event.type in (pygame.VIDEORESIZE, pygame.WINDOWRESIZED):
                if self.app and self.app.screen:
                    win_w, win_h = self.app.screen.get_size()
                    self._update_layout(win_w, win_h)

        if self.form_manager.form_modality == FormModality.NEW:
            self._handle_new_mode_events(events)
        else:
            self._handle_existing_mode_events(events)

    def _handle_new_mode_events(self, events: list[pygame.event.Event]) -> None:
        """Handle events in NEW mode (text input)."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if clicked on input field
                self.input_focused = self.input_rect.collidepoint(event.pos)
                
                # Check if clicked submit button
                if self.submit_button_rect.collidepoint(event.pos):
                    self._submit_form()
                
                # Check if clicked toggle button
                if self.toggle_button_rect.collidepoint(event.pos):
                    self._toggle_modality()
            
            elif event.type == pygame.KEYDOWN:
                if self.input_focused:
                    if event.key == pygame.K_RETURN:
                        self._submit_form()
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove last character
                        current = self.form_manager.form.actual_name
                        self.form_manager.form.on_change_name(current[:-1])
                    elif event.key == pygame.K_ESCAPE:
                        self.input_focused = False
                    elif event.unicode:
                        # Add character
                        current = self.form_manager.form.actual_name
                        self.form_manager.form.on_change_name(current + event.unicode)

    def _handle_existing_mode_events(self, events: list[pygame.event.Event]) -> None:
        """Handle events in EXISTING mode (list selection)."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if clicked toggle button
                if self.toggle_button_rect.collidepoint(event.pos):
                    self._toggle_modality()
                
                # Check if clicked submit button
                elif self.submit_button_rect.collidepoint(event.pos):
                    self._submit_form()
                
                # Check if clicked on a delete (x) button
                elif self._check_delete_click(event.pos):
                    pass  # deletion handled
                
                # Check if clicked on list item
                else:
                    self._check_list_click(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.form_manager.move_selection(-1)
                elif event.key == pygame.K_DOWN:
                    self.form_manager.move_selection(1)
                elif event.key == pygame.K_RETURN:
                    self._submit_form()

    def _check_delete_click(self, pos: tuple[int, int]) -> bool:
        """Check if user clicked on a delete (x) button. Returns True if handled."""
        for i, rect in enumerate(self.delete_btn_rects):
            if rect.collidepoint(pos):
                self.form_manager.delete_user(i, self.context.registry)
                self.delete_btn_rects = []  # will be rebuilt on next render
                return True
        return False

    def _check_list_click(self, pos: tuple[int, int]) -> None:
        """Check if user clicked on a list item."""
        if not self.form_manager.users:
            return
        
        x, y = pos
        if y < self.list_start_y:
            return
        
        clicked_index = (y - self.list_start_y) // self.list_item_height
        if 0 <= clicked_index < len(self.form_manager.users):
            self.form_manager.selected_index = clicked_index

    def _toggle_modality(self) -> None:
        """Toggle between NEW and EXISTING modes."""
        self.form_manager.toggle_modality(self.context.registry)
        self.input_focused = False

    def _submit_form(self) -> None:
        """Submit the form and attach participant to session."""
        result = self.form_manager.submit()
        
        if result is None:
            # Validation error - stay in form
            return
        
        if result[0] == "new":
            # NEW mode: create new participant
            participant_name = result[1]
            self.context.session.attach_participant(
                participant_code=participant_name,
                secret_key=self.context.secret_key,
                display_name=participant_name,
                names_registry=self.context.registry,
            )
            print(f"New participant created: {participant_name}")
            self._proceed_to_next_state()
        
        elif result[0] == "existing":
            # EXISTING mode: attach existing participant
            pseudonym_int, display_name = result[1], result[2]
            self.context.session.attach_existing_participant(
                participant_pseudonym=pseudonym_int,
                display_name=display_name,
                names_registry=self.context.registry,
            )
            print(f"Existing participant selected: {display_name}")
            self._proceed_to_next_state()

    def _proceed_to_next_state(self) -> None:
        """Move to the next state after successful form submission."""
        if self.app:
            self.app.request_state_change("intro_book_idle")

    def update(self, delta_time: float) -> None:
        """Update state (currently no animation/updates needed)."""
        pass

    def render(self, screen: pygame.Surface) -> None:
        """Render the form UI."""
        # Background (use book_open_bg from assets, fallback to solid color)
        if self.app and self.app.book_open_bg:
            screen.blit(self.app.book_open_bg, (0, 0))
        else:
            screen.fill(self.bg_color)
        
        # Title
        self._render_title(screen)
        
        if self.form_manager.form_modality == FormModality.NEW:
            self._render_new_mode(screen)
        else:
            self._render_existing_mode(screen)
        
        # Toggle button
        self._render_toggle_button(screen)

    def _render_title(self, screen: pygame.Surface) -> None:
        """Render the form title."""
        if not self.app or not self.app.font:
            return
        
        win_w = screen.get_width()
        title = "Enter Participant Name" if self.form_manager.form_modality == FormModality.NEW else "Select Participant"
        
        title_surf = self.app.font.render(title, True, self.text_color)
        title_surf.set_colorkey(self.app.color_key)
        title_rect = title_surf.get_rect(centerx=win_w // 2, y=50)
        screen.blit(title_surf, title_rect)

    def _draw_alpha_rect(self, screen: pygame.Surface, color: tuple, rect: pygame.Rect) -> None:
        """Draw a filled rectangle with optional alpha transparency."""
        if len(color) == 4:
            surf = pygame.Surface(rect.size, pygame.SRCALPHA)
            surf.fill(color)
            screen.blit(surf, rect.topleft)
        else:
            pygame.draw.rect(screen, color, rect)

    def _render_new_mode(self, screen: pygame.Surface) -> None:
        """Render NEW mode UI (text input)."""
        if not self.app or not self.app.font:
            return
        
        # Input field background
        border_color = self.input_focus_border if self.input_focused else self.input_border
        self._draw_alpha_rect(screen, self.input_bg, self.input_rect)
        pygame.draw.rect(screen, border_color, self.input_rect, 2)
        
        # Input text
        text = self.form_manager.form.actual_name or ""
        text_surf = self.app.font.render(text, True, self.text_color)
        text_surf.set_colorkey(self.app.color_key)
        text_rect = text_surf.get_rect(
            midleft=(self.input_rect.left + 10, self.input_rect.centery)
        )
        screen.blit(text_surf, text_rect)
        
        # Error message
        if self.form_manager.form.state == FormState.ERROR:
            error_surf = self.app.font.render(
                self.form_manager.form.error_message, 
                True, 
                self.error_color
            )
            error_surf.set_colorkey(self.app.color_key)
            error_rect = error_surf.get_rect(
                centerx=self.input_rect.centerx,
                top=self.input_rect.bottom + 5
            )
            screen.blit(error_surf, error_rect)
        
        # Submit button
        self._render_button(
            screen,
            self.submit_button_rect,
            "Submit",
            self.button_bg,
            self.button_hover
        )

    def _render_existing_mode(self, screen: pygame.Surface) -> None:
        """Render EXISTING mode UI (list selection)."""
        if not self.app or not self.app.font:
            return
        
        if not self.form_manager.has_any_users():
            # No saved participants
            msg_surf = self.app.font.render(
                "No saved participants", 
                True, 
                self.text_color
            )
            msg_surf.set_colorkey(self.app.color_key)
            msg_rect = msg_surf.get_rect(
                centerx=screen.get_width() // 2,
                centery=screen.get_height() // 2
            )
            screen.blit(msg_surf, msg_rect)
            return
        
        # Render list of participants
        win_w = screen.get_width()
        list_x = win_w // 2 - self.list_width // 2
        
        # Rebuild delete button rects list
        self.delete_btn_rects = []
        
        for i, (pseudonym, display_name) in enumerate(self.form_manager.users):
            y = self.list_start_y + i * self.list_item_height
            item_h = self.list_item_height - 5
            item_rect = pygame.Rect(list_x, y, self.list_width, item_h)
            
            # Background
            if i == self.form_manager.selected_index:
                bg_color = self.list_item_selected
                text_color = self.button_text
            else:
                bg_color = self.list_item_bg
                text_color = self.text_color
            
            self._draw_alpha_rect(screen, bg_color, item_rect)
            pygame.draw.rect(screen, self.input_border, item_rect, 1)
            
            # Text
            text_surf = self.app.font.render(display_name, True, text_color)
            text_surf.set_colorkey(self.app.color_key)
            text_rect = text_surf.get_rect(
                midleft=(item_rect.left + 10, item_rect.centery)
            )
            screen.blit(text_surf, text_rect)
            
            # Delete (x) button — small red square on the right
            btn_size = max(item_h - 8, 16)
            btn_rect = pygame.Rect(
                item_rect.right - btn_size - 4,
                item_rect.top + (item_h - btn_size) // 2,
                btn_size,
                btn_size
            )
            self.delete_btn_rects.append(btn_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            btn_color = self.delete_btn_hover if btn_rect.collidepoint(mouse_pos) else self.delete_btn_bg
            pygame.draw.rect(screen, btn_color, btn_rect, border_radius=3)
            
            # Draw "x" text centered in the button
            x_surf = self.app.font.render("x", True, self.delete_btn_text)
            x_surf.set_colorkey(self.app.color_key)
            x_rect = x_surf.get_rect(center=btn_rect.center)
            screen.blit(x_surf, x_rect)
        
        # Submit button
        self._render_button(
            screen,
            self.submit_button_rect,
            "Select",
            self.button_bg,
            self.button_hover
        )

    def _render_toggle_button(self, screen: pygame.Surface) -> None:
        """Render the mode toggle button."""
        if not self.app or not self.app.font:
            return
        
        label = "Users Saved" if self.form_manager.form_modality == FormModality.NEW else "Create New"
        self._render_button(
            screen,
            self.toggle_button_rect,
            label,
            (100, 100, 100),
            (130, 130, 130)
        )

    def _render_button(
        self, 
        screen: pygame.Surface, 
        rect: pygame.Rect, 
        text: str,
        bg_color: tuple[int, int, int],
        hover_color: tuple[int, int, int]
    ) -> None:
        """Render a button with hover effect."""
        if not self.app or not self.app.font:
            return
        
        # Check hover
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)
        color = hover_color if is_hover else bg_color
        
        # Draw button
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, self.input_border, rect, 2)
        
        # Draw text
        text_surf = self.app.font.render(text, True, self.button_text)
        text_surf.set_colorkey(self.app.color_key)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
