from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from src.logging.session_logger import DisplayNameRegistry
from src.core.form_state import Form, FormState

class FormModality(Enum):
    """Which UI the form state is showing."""

    NEW = "new"
    EXISTING = "existing"

@dataclass
class FormManager:
    """Pure UI/state holder for the participant form.

    - NEW: user types a name/code
    - EXISTING: user selects an existing participant from registry

    This class should not depend on pygame or GameContext; states call its methods.
    """

    form: Form = field(default_factory=Form)
    form_modality: FormModality = FormModality.NEW

    # EXISTING mode list state
    users: list[tuple[int, str]] = field(default_factory=list)  # (pseudonym_int, display_name)
    users_loaded: bool = False
    selected_index: int = 0

    # Optional search/filter
    filter_query: str = ""

    def reset(self) -> None:
        """Reset to the initial NEW-mode state."""
        self.form = Form()
        self.form_modality = FormModality.NEW
        self.users = []
        self.users_loaded = False
        self.selected_index = 0
        self.filter_query = ""

    def toggle_modality(self, registry: Optional[DisplayNameRegistry] = None) -> FormModality:
        """Toggle NEW <-> EXISTING. If entering EXISTING, optionally load users."""
        if self.form_modality == FormModality.NEW:
            self.form_modality = FormModality.EXISTING
            if registry is not None:
                self.load_users(registry)
            return self.form_modality

        self.form_modality = FormModality.NEW
        return self.form_modality

    def load_users(self, registry: DisplayNameRegistry) -> None:
        """Load and sort users from DisplayNameRegistry."""
        mapping = registry.load()  # str(pseudonym) -> display_name
        items: list[tuple[int, str]] = []
        for k, v in mapping.items():
            try:
                items.append((int(k), str(v)))
            except ValueError:
                continue

        # Sort by display name (case-insensitive)
        items.sort(key=lambda x: x[1].casefold())
        self.users = items
        self.users_loaded = True
        self._clamp_selected_index()

    def has_any_users(self) -> bool:
        return len(self.users) > 0

    def delete_user(self, index: int, registry: DisplayNameRegistry) -> None:
        """Delete a user by list index from registry and local list."""
        if not self.users or not (0 <= index < len(self.users)):
            return
        pseudonym_int, display_name = self.users[index]
        registry.delete_name(pseudonym_int)
        self.users.pop(index)
        self._clamp_selected_index()

    def move_selection(self, delta: int) -> None:
        """Move selection up/down in EXISTING mode."""
        if not self.users:
            self.selected_index = 0
            return
        self.selected_index += int(delta)
        self._clamp_selected_index()

    def get_selected_user(self) -> Optional[tuple[int, str]]:
        """Return (pseudonym_int, display_name) for the current selection."""
        if not self.users:
            return None
        self._clamp_selected_index()
        return self.users[self.selected_index]

    def _clamp_selected_index(self) -> None:
        if not self.users:
            self.selected_index = 0
            return
        self.selected_index = max(0, min(self.selected_index, len(self.users) - 1))

    def submit(self) -> Optional[tuple[str, object]]:
        """Submit the form and return a normalized result.

        Returns:
            - ("new", confirmed_name: str) if NEW mode validated successfully
            - ("existing", pseudonym_int: int, display_name: str) if EXISTING mode has a selection
            - None if submission failed (and the manager/form state is updated accordingly)
        """
        if self.form_modality == FormModality.NEW:
            confirmed = self.form.naming()
            if self.form.state == FormState.SUCCESS:
                return ("new", confirmed)
            # Form.naming() already set ERROR state
            return None

        # EXISTING
        if not self.users:
            # No saved users to select
            self.form.state = FormState.ERROR
            self.form.error_message = "No saved users"
            return None

        selected = self.get_selected_user()
        if selected is None:
            self.form.state = FormState.ERROR
            self.form.error_message = "No selection"
            return None

        pseudonym_int, display_name = selected
        return ("existing", pseudonym_int, display_name)
