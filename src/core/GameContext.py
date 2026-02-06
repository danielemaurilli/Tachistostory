from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from src.logging.session_logger import DisplayNameRegistry, SessionData, SessionLogger
from src.core.form_manager import FormManager


@dataclass
class GameContext:
    """Shared, long-lived app context.

    Holds cross-state dependencies and the *current* SessionData/SessionLogger pair.
    The logger is always kept consistent with the session.
    """

    # Core logging/session objects
    session: SessionData = field(default_factory=SessionData)
    logger: SessionLogger = field(init=False)

    # Persistent helpers
    registry: DisplayNameRegistry = field(default_factory=DisplayNameRegistry)
    form_manager: FormManager = field(default_factory=FormManager)
    secret_key: bytes = b""

    # Optional paths/config
    assets_root: Optional[Path] = None
    selected_file_path: Optional[Path] = None
    include_display_name: bool = True

    #Output directory — sibling folder to project root
    output_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent.parent.parent / "tachistostory log")

    def __post_init__(self) -> None:
        # Always bind logger to the current session
        self.logger = SessionLogger(self.session)

    def new_session(self) -> None:
        """Reset to a fresh session and re-bind the logger.

        Call this when the user starts a new run (e.g., from csv_state -> file_select_state).
        """
        self.session = SessionData()
        self.logger = SessionLogger(self.session)
        self.selected_file_path = None
        # Reset form manager for new participant entry
        self.form_manager.reset()

    def get_session_and_logger(self) -> tuple[SessionData, SessionLogger]:
        """Convenience accessor for states that want both objects."""
        return self.session, self.logger