from src.logging.session_logger import DisplayNameRegistry
from dataclasses import dataclass, field
from enum import Enum


class FormState(Enum):
    """Form state."""

    IDLE = "idle"
    EDITING = "editing"
    VALIDATING = "validating"
    ERROR = "error"
    SUCCESS = "success"


@dataclass
class Form:
    """State container for the name form."""

    actual_name: str = ""
    state: FormState = field(default=FormState.IDLE)
    error_message: str = ""
    is_submitting: bool = False
    touched: bool = False
    confirmed_name: str = ""
    max_length: int = 15

    _not_permitted_chars = set("'?!:.,;|/[](){}#§+*^%&=")

    def _clean_name(self) -> str:
        """Trim and collapse spaces."""
        return " ".join(self.actual_name.strip().split())

    def _convert_name(self, name: str) -> str:
        """Normalize final name."""
        return " ".join(name.split()).lower()

    def on_change_name(self, new_value: str) -> None:
        """Update input while typing."""
        self.actual_name = new_value
        self.touched = True
        if self.state in (FormState.IDLE, FormState.ERROR):
            self.state = FormState.EDITING
        self.error_message = ""

    def on_blur_name(self) -> bool:
        """Validate on input blur."""
        self.touched = True
        return self.validate_name()

    def validate_name(self) -> bool:
        """Validate current input and set form state."""
        self.state = FormState.VALIDATING
        clean = self._clean_name()

        if not clean:
            self.state = FormState.ERROR
            self.error_message = "Name is required."
            return False
        if len(clean) > self.max_length:
            self.state = FormState.ERROR
            self.error_message = f"Name must be <= {self.max_length} characters."
            return False
        if any(ch in self._not_permitted_chars for ch in clean):
            self.state = FormState.ERROR
            self.error_message = "Name contains invalid characters."
            return False

        self.state = FormState.SUCCESS
        self.error_message = ""
        return True

    def submit_name(self) -> str:
        """Submit form and return confirmed name or error message."""
        self.is_submitting = True
        self.touched = True
        try:
            if not self.validate_name():
                return self.error_message
            self.confirmed_name = self._convert_name(self._clean_name())
            return self.confirmed_name
        finally:
            self.is_submitting = False

    def naming(self) -> str:
        """Backward-compatible alias."""
        return self.submit_name()

    def reset(self) -> None:
        """Reset form values and state."""
        self.actual_name = ""
        self.state = FormState.IDLE
        self.error_message = ""
        self.is_submitting = False
        self.touched = False
        self.confirmed_name = ""

    