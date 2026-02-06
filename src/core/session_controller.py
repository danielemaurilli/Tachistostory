from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from src.core.GameContext import GameContext
from typing import Optional
import uuid

@dataclass
class SessionController:
    context: GameContext

    #=================== FILE =====================================================
    def set_file_selected(self, file_path: Path) -> None:
        """Set the selected stimulus/source file and snapshot its metadata into SessionData."""
        self.context.selected_file_path = file_path
        self.context.session.set_input_file(file_path, assets_root=self.context.assets_root)
    
    #=================== PARTICIPANT ================================================
    def attach_new_user(self, name: str) -> None:
        self.context.session.attach_participant(participant_code=name, 
                                                secret_key=self.context.secret_key,
                                                display_name=name,
                                                names_registry=self.context.registry)
        
    def attach_existing_user(self, pseudonym_int:int, display_name: Optional[str] = None) -> None:
        self.context.session.attach_existing_participant(participant_pseudonym=pseudonym_int,
                                                         display_name=display_name,
                                                         names_registry= self.context.registry)
    

    #====================== SESSION LIFECYCLE ======================
    def start_session(self, now_ms: int, session_id: Optional[uuid.UUID] = None) -> uuid.UUID:
        if self.context.selected_file_path is None:
            raise RuntimeError("No file selected")
        elif self.context.session.participant_pseudonym is None:
            raise RuntimeError('No participant attached') 
        
        sid = session_id or uuid.uuid4()
        self.context.logger.start_session(session_id=sid, started_at_ms=now_ms)
        return sid
    
    def end_session(self, now_ms:int) -> None:
        self.context.logger.end_session(ended_at_ms=now_ms)
    
    # ==================== EXPORT ======================================
    def export_all(self) -> dict[str, Path]:
        out_dir = self.context.output_dir.expanduser()
        out_dir.mkdir(parents=True, exist_ok=True)

        csv_words, csv_pauses, csv_summary = self.context.logger.export_csv(
            out_dir, include_display_name=self.context.include_display_name
        )
        json_path = out_dir / f"{self.context.session.date_local}_session-{self.context.session.session_id}.json"
        self.context.logger.export_json(json_path)

        return {
            "word_events_csv": csv_words,
            "pause_events_csv": csv_pauses,
            "summary_csv": csv_summary,
            "session_json": json_path,
        }