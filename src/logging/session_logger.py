"""
Session logger config
"""
from dataclasses import dataclass, field
from enum import Enum
import csv
from datetime import datetime
import hashlib
import hmac
import json
import platform
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Sequence, Any
import uuid

if TYPE_CHECKING:
    from game import State


# Classes for WordEvent
class StimulusType(str, Enum):
    WORD = 'word'
    PHRASE = 'phrase'
    SENTENCE = 'sentence'

class ResponseStatus(str, Enum):
    CORRECT = 'correct'
    WRONG = 'wrong'
    NULL = 'null'

class ErrorType(str, Enum):
    OMISSION = 'omission'
    COMMISSION = 'commission'
    NULL = 'null'

@dataclass
class WordEvent:
    #identity
    session_id: Optional[uuid.UUID] = None
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    trial_index: int = 0

    #stimulus
    stimulus_text: str = field(default='')   
    stimulus_type: StimulusType = StimulusType.WORD
    stimulus_source: str = ''

    #timing
    duration_ms: int = 0
    shown_at_ms: int = 0
    hidden_at_ms: int = 0

    #context
    word_level_speed: Optional[int] = None
    game_state: Optional["State"] = None

    #performance
    response_status: ResponseStatus = ResponseStatus.NULL
    response_time_ms: Optional[int] = None
    is_correct: Optional[bool] = None
    error_type: ErrorType = ErrorType.NULL

    @property
    def actual_duration_ms(self) -> Optional[int]:
        data = self.hidden_at_ms - self.shown_at_ms
        if data > 0:
            return data
        else:
            return None

    def to_csv_row(self, participant_pseudonym: Optional[int] = None) -> dict[str, object]:
        return {
            "session_id": str(self.session_id) if self.session_id else "",
            "participant_pseudonym": int(participant_pseudonym) if participant_pseudonym is not None else "",
            "event_id": str(self.event_id),
            "trial_index": self.trial_index,
            "stimulus_text": self.stimulus_text,
            "stimulus_type": self.stimulus_type.value,
            "stimulus_source": self.stimulus_source,
            "duration_ms": self.duration_ms,
            "shown_at_ms": self.shown_at_ms,
            "hidden_at_ms": self.hidden_at_ms,
            "actual_duration_ms": self.actual_duration_ms if self.actual_duration_ms is not None else "",
            "word_level_speed": self.word_level_speed if self.word_level_speed is not None else "",
            "game_state": str(self.game_state) if self.game_state is not None else "",
            "response_status": self.response_status.value,
            "response_time_ms": self.response_time_ms if self.response_time_ms is not None else "",
            "is_correct": self.is_correct if self.is_correct is not None else "",
            "error_type": self.error_type.value,
        }


#Classes for PauseEvent
class ReasonState(str, Enum):
    MANUAL_PAUSE = 'manual pause'
    ALT_TAB = 'alt-tab'
    FOCUS_LOSS = 'focus loss'

@dataclass
class PauseEvent:
    pause_id: Optional[uuid.UUID] = None
    session_id: Optional[uuid.UUID] = None
    is_in_pause: bool = False
    start_ms: Optional[int] = 0
    end_ms: Optional[int] = 0 
    reason: Optional[ReasonState] = None
    
    def duration_ms(self) -> Optional[int]:
        if self.start_ms is None or self.end_ms is None:
            return None
        data = self.end_ms - self.start_ms
        if data >= 0:
            return data
        return None

    def to_csv_row(self, participant_pseudonym: Optional[int] = None) -> dict[str, object]:
        return {
            "session_id": str(self.session_id) if self.session_id else "",
            "participant_pseudonym": int(participant_pseudonym) if participant_pseudonym is not None else "",
            "pause_id": self.pause_id if self.pause_id is not None else "",
            "start_ms": self.start_ms if self.start_ms is not None else "",
            "end_ms": self.end_ms if self.end_ms is not None else "",
            "duration_ms": self.duration_ms() if self.duration_ms() is not None else "",
            "reason": self.reason.value if self.reason is not None else "",
        }

#Participant pseydonymization

DEFAULT_DISPLAY_NAMES_PATH = Path.home() / ".tachistostory" / "participant_display_names.json"

def _ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def pseudonym_int_hmac(participant_code:str, 
                       secret_key:bytes, bits: int = 63, 
                       namespace:str = 'tachistostory:v1') -> int:
    """Return a stable, non-reversible pseudonym int derived from a participant_code
    
    
        - Deterministic: same code + same key -> same pseydonym
        - Non-reversible: cannot recover the code from the pseudonym
        - bits = 63 fits safely in signed BIGINT
        
        Note: `namespace` prevents collisions if the same code/ key if reused across different apps
        """
    
    msg = f"{namespace}:{participant_code}".encode('utf-8')
    digest = hmac.new(secret_key, msg, hashlib.sha256).digest()
    n = int.from_bytes(digest, byteorder="big", signed=False)
    return n & ((1 << bits) - 1)

@dataclass
class DisplayNameRegistry:
    """Stores an optional mapping: pseudonym_int -> display_name.
    
        Use for UI/report labeling only. Avoid personale identifiers in display_name.
    """
    
    path: Path = DEFAULT_DISPLAY_NAMES_PATH
    
    def load(self) -> dict[str,str]:
        if not self.path.exists():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        return {str(k): str(v) for k,v in data.items()}
    
    def save(self, mapping: dict[str, str]) -> None:
        _ensure_parent_dir(self.path)
        self.path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2, sort_keys=True), encoding='utf-8')

    def set_name(self, pseudonym_int: int, display_name: str)-> None:
        mapping = self.load()
        mapping[str(int(pseudonym_int))] = display_name
        self.save(mapping)

    def get_name(self, pseudonym_int:int) -> Optional[str]:
        mapping = self.load()
        return mapping.get(str(int(pseudonym_int)))
    
    def delete_name(self, psudonym_int:int) -> None:
        mapping = self.load()
        key = str(int(psudonym_int))
        if key in mapping:
            del mapping[key]
            self.save(mapping)

    def name_exists(self, display_name: str) -> bool:
        """Verifica se un display_name è già presente nel registry."""
        mapping = self.load()
        return display_name in mapping.values()
    
    def pseudonym_exists(self, pseudonym_int: int) -> bool:
        """Verifica se uno pseudonimo è già presente nel registry."""
        mapping = self.load()
        return str(int(pseudonym_int)) in mapping
    
    def set_name_if_not_exists(self, pseudonym_int: int, display_name: str) -> bool:
        """Imposta il nome solo se lo pseudonimo non esiste già.
        
        Returns:
            True se il nome è stato aggiunto, False se esisteva già.
        """
        mapping = self.load()
        key = str(int(pseudonym_int))
        if key in mapping:
            return False
        mapping[key] = display_name
        self.save(mapping)
        return True
    
    def set_name_if_unique(self, pseudonym_int: int, display_name: str) -> bool:
        """Imposta il nome solo se né lo pseudonimo né il display_name esistono già.
        
        Returns:
            True se il nome è stato aggiunto, False se esisteva già un duplicato.
        """
        mapping = self.load()
        key = str(int(pseudonym_int))
        if key in mapping or display_name in mapping.values():
            return False
        mapping[key] = display_name
        self.save(mapping)
        return True

@dataclass
class SessionData:
    # ID
    session_id: Optional[uuid.UUID] = None
    
    # Store ONLY the pseudonym in logs/exports.
    participant_pseudonym: Optional[int] = None

    # Optional: admin-provided participant code kept in-memory only.
    # Do not serialize/export this field if you aim for pseudonymized logs.
    participant_code_raw: Optional[str] = field(default=None, repr=False)

    # Optional: UI label (avoid personal identifiers)
    participant_display_name: Optional[str] = None

    started_at_ms: int = 0
    ended_at_ms: int = 0
    date_local: str = field(default_factory=lambda:datetime.now().date().isoformat())

    # Input/Context
    # These are intended to be set when a stimulus/source file is selected.
    input_file_name: str = ''
    input_file_relpath: str = ""
    input_file_hash: Optional[str] = None
    input_file_size_bytes: Optional[int] = None
    input_file_origin: str = "unknown"
    platform_os: str = field(default_factory=platform.system)

    # config
    profile_name: Optional[str] = None
    setting_snapshot: Optional[dict[str, Any]] = None

    #Events
    word_events: list[WordEvent] = field(default_factory=list)
    pause_events: list[PauseEvent] = field(default_factory=list)
    notes: Optional[str] = None

    #metrics
    total_words: int = 0
    total_paused_ms: int = 0
    total_active_ms: int = 0
    accuracy: str = ''
    
    def setter(self, file_path: Path, assets_root: Path | None = None) -> None:
        self.input_file_name = file_path.name
        self.input_file_size_bytes = file_path.stat().st_size

        h = hashlib.sha256()
        with file_path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        self.input_file_hash = h.hexdigest()

        if assets_root is not None:
            try:
                self.input_file_relpath = str(file_path.resolve().relative_to(assets_root.resolve()))
                self.input_file_origin = "assets"
                return
            except ValueError:
                pass

        self.input_file_relpath = ""
        self.input_file_origin = "external_drop"

    def avg_actual_duration_ms(self) -> float:
        """Calcola la durata media effettiva degli eventi word nella sessione."""
        if not self.word_events:
            return 0.0
        
        durations = [e.actual_duration_ms for e in self.word_events if e.actual_duration_ms is not None]
        if not durations:
            return 0.0
        
        return sum(durations) / len(durations)
       
    def accuracy_calc(self, press_space: int, press_back: int, total_words: int) -> str:
        if total_words <= 0:
            return "0%"

        correct = press_space
        wrong = press_back
        score = (correct - wrong) / total_words * 100

        # limita tra 0 e 100
        score = max(0.0, min(100.0, score))

        return f"{score:.1f}%"
        
        

    def attach_participant(
        self,
        participant_code: str,
        secret_key: bytes,
        display_name: Optional[str] = None,
        names_registry: Optional[DisplayNameRegistry] = None,
        bits: int = 63,
    ) -> None:
        """Assign a stable, non-reversible pseudonym for an admin-provided participant code."""
        self.participant_code_raw = participant_code
        self.participant_pseudonym = pseudonym_int_hmac(participant_code, secret_key, bits=bits)

        if display_name is not None:
            self.participant_display_name = display_name
            (names_registry or DisplayNameRegistry()).set_name(self.participant_pseudonym, display_name)
        else:
            # Try to load a previously stored label, if any
            self.participant_display_name = (names_registry or DisplayNameRegistry()).get_name(self.participant_pseudonym)


# -----------------------------
# CSV export utilities
# -----------------------------

def export_word_events_csv(
    events: Sequence[WordEvent],
    session: SessionData,
    csv_path: Path | str,
    include_display_name: bool = True,
) -> Path:
    """Export WordEvent list to CSV.

    Exports ONLY pseudonym-based identifiers (participant_pseudonym).
    Raw participant_code is never written.
    """
    path = Path(csv_path)
    _ensure_parent_dir(path)

    # Build header from first row template (stable order)
    base_fields = list(WordEvent().to_csv_row(participant_pseudonym=0).keys())
    extra_fields: list[str] = []
    if include_display_name:
        extra_fields.append("participant_display_name")

    fieldnames = base_fields + extra_fields

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for ev in events:
            row = ev.to_csv_row(participant_pseudonym=session.participant_pseudonym)
            if include_display_name:
                row["participant_display_name"] = session.participant_display_name or ""
            writer.writerow(row)

    return path


def export_pause_events_csv(
    events: Sequence[PauseEvent],
    session: SessionData,
    csv_path: Path | str,
    include_display_name: bool = True,
) -> Path:
    """Export PauseEvent list to CSV.

    Exports ONLY pseudonym-based identifiers (participant_pseudonym).
    Raw participant_code is never written.
    """
    path = Path(csv_path)
    _ensure_parent_dir(path)

    base_fields = list(PauseEvent().to_csv_row(participant_pseudonym=0).keys())
    extra_fields: list[str] = []
    if include_display_name:
        extra_fields.append("participant_display_name")

    fieldnames = base_fields + extra_fields

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for ev in events:
            row = ev.to_csv_row(participant_pseudonym=session.participant_pseudonym)
            if include_display_name:
                row["participant_display_name"] = session.participant_display_name or ""
            writer.writerow(row)

    return path


def export_session_summary_csv(
    session: SessionData,
    word_events: Sequence[WordEvent] | None,
    pause_events: Sequence[PauseEvent] | None,
    csv_path: Path | str,
) -> Path:
    """Export a 1-row session summary CSV (useful for quick analyses).

    Only pseudonym identifiers are exported.
    """
    path = Path(csv_path)
    _ensure_parent_dir(path)

    word_events = word_events or []
    pause_events = pause_events or []

    total_trials = len(word_events)
    total_correct = sum(1 for e in word_events if e.is_correct is True)
    total_wrong = sum(1 for e in word_events if e.is_correct is False)
    mean_rt = (
        sum(e.response_time_ms for e in word_events if e.response_time_ms is not None) /
        max(1, sum(1 for e in word_events if e.response_time_ms is not None))
    )

    total_pause_ms = sum((p.duration_ms() or 0) for p in pause_events)

    row = {
        "session_id": str(session.session_id) if session.session_id else "",
        "participant_pseudonym": int(session.participant_pseudonym) if session.participant_pseudonym is not None else "",
        "participant_display_name": session.participant_display_name or "",
        "total_trials": total_trials,
        "total_correct": total_correct,
        "total_wrong": total_wrong,
        "mean_response_time_ms": round(mean_rt, 2) if mean_rt is not None else "",
        "total_pause_ms": total_pause_ms,
        "num_pauses": len(pause_events),
    }

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    return path


@dataclass
class SessionLogger():
    session: SessionData
    _pause_start_ms: Optional[int] = None
    _pause_reason: Optional[ReasonState] = None

    def start_session(self, session_id: uuid.UUID, started_at_ms:int) -> None:
        """Initialize session and time"""
        self.session.session_id = session_id
        self.session.started_at_ms = started_at_ms

    def trial_index(self) -> int:
        """Return the current trial index for the next WordEvent.

        In this logger, trial_index corresponds to the number of WordEvents already logged.
        """
        return len(self.session.word_events)

    def set_in_pause(self, is_in_pause: bool, now_ms: int, reason: Optional[ReasonState] = None) -> None:
        """Update pause state.

        Call this when the game enters/leaves pause.
        - When entering pause (is_in_pause=True), we store the start tick.
        - When leaving pause (is_in_pause=False), we create a PauseEvent and append it.
        """
        if is_in_pause:
            # Entering pause
            if self._pause_start_ms is None:
                self._pause_start_ms = now_ms
                self._pause_reason = reason
            return

        # Leaving pause
        if self._pause_start_ms is None:
            # Not previously in pause; nothing to close.
            return

        pe = PauseEvent(
            pause_id=uuid.uuid4(),
            session_id=self.session.session_id,
            start_ms=self._pause_start_ms,
            end_ms=now_ms,
            reason=self._pause_reason,
        )
        self.session.pause_events.append(pe)

        # Reset pause tracking
        self._pause_start_ms = None
        self._pause_reason = None

    def log_word_event(
        self,
        stimulus_text: str,
        shown_at_ms: int,
        hidden_at_ms: int,
        *,
        stimulus_type: StimulusType = StimulusType.WORD,
        stimulus_source: str = "",
        duration_ms: int = 0,
        word_level_speed: Optional[int] = None,
        game_state: Optional["State"] = None,
        response_status: ResponseStatus = ResponseStatus.NULL,
        response_time_ms: Optional[int] = None,
        is_correct: Optional[bool] = None,
        error_type: ErrorType = ErrorType.NULL,
    ) -> WordEvent:
        """Create and append a WordEvent to the current session.

        - session_id is taken from the active SessionData
        - trial_index is derived from the number of word_events already logged
        """
        we = WordEvent(
            session_id=self.session.session_id,
            trial_index=self.trial_index(),
            stimulus_text=stimulus_text,
            stimulus_type=stimulus_type,
            stimulus_source=stimulus_source,
            duration_ms=duration_ms,
            shown_at_ms=shown_at_ms,
            hidden_at_ms=hidden_at_ms,
            word_level_speed=word_level_speed,
            game_state=game_state,
            response_status=response_status,
            response_time_ms=response_time_ms,
            is_correct=is_correct,
            error_type=error_type,
        )
        self.session.word_events.append(we)
        return we
    
    def log_pause(
        self,
        start_ms: int,
        end_ms: int,
        *,
        reason: Optional[ReasonState] = None,
        pause_id: Optional[uuid.UUID] = None,
    ) -> PauseEvent:
        """Create, append, and return a PauseEvent for the current session."""
        pe = PauseEvent(
            pause_id=pause_id or uuid.uuid4(),
            session_id=self.session.session_id,
            start_ms=start_ms,
            end_ms=end_ms,
            reason=reason,
        )
        self.session.pause_events.append(pe)
        return pe
    
    def end_session(self, ended_at_ms: int) -> None:
        """Finalize the current session and compute summary metrics.

        - Closes an open pause (if any)
        - Sets ended_at_ms
        - Computes total_words, total_paused_ms, total_active_ms
        - Computes accuracy from is_correct when available
        """
        # Require an active session
        if self.session.session_id is None:
            return

        # If a pause is currently open, close it at session end
        if self._pause_start_ms is not None:
            self.set_in_pause(False, ended_at_ms)

        self.session.ended_at_ms = ended_at_ms

        # total words/trials
        self.session.total_words = len(self.session.word_events)

        # total paused ms
        total_paused = 0
        for p in self.session.pause_events:
            total_paused += (p.duration_ms() or 0)
        self.session.total_paused_ms = total_paused

        # total active ms (clamped)
        total_session_ms = self.session.ended_at_ms - self.session.started_at_ms
        active_ms = total_session_ms - self.session.total_paused_ms
        self.session.total_active_ms = active_ms if active_ms > 0 else 0

        # accuracy: prefer per-event correctness when present
        attempted = 0
        correct = 0
        for e in self.session.word_events:
            if e.is_correct is True:
                attempted += 1
                correct += 1
            elif e.is_correct is False:
                attempted += 1

        if attempted > 0:
            score = (correct / attempted) * 100
            self.session.accuracy = f"{score:.1f}%"
        else:
            self.session.accuracy = "0%"

    def export_csv(self, output_dir: Path | str, include_display_name: bool = True) -> tuple[Path, Path, Path]:
        """Export current session logs to CSV files.

        Call this after `end_session(...)` so summary metrics are finalized.

        Returns:
            (word_events_csv_path, pause_events_csv_path, summary_csv_path)
        """
        # Require an active session
        if self.session.session_id is None:
            raise RuntimeError("No active session to export")

        # 1) Normalize output_dir
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # 2) Build stable filenames
        date_tag = self.session.date_local or datetime.now().date().isoformat()
        sid = str(self.session.session_id)

        words_path = out_dir / f"{date_tag}_session-{sid}_word_events.csv"
        pauses_path = out_dir / f"{date_tag}_session-{sid}_pause_events.csv"
        summary_path = out_dir / f"{date_tag}_session-{sid}_summary.csv"

        # 3) Export
        export_word_events_csv(
            events=self.session.word_events,
            session=self.session,
            csv_path=words_path,
            include_display_name=include_display_name,
        )
        export_pause_events_csv(
            events=self.session.pause_events,
            session=self.session,
            csv_path=pauses_path,
            include_display_name=include_display_name,
        )
        export_session_summary_csv(
            session=self.session,
            word_events=self.session.word_events,
            pause_events=self.session.pause_events,
            csv_path=summary_path,
        )

        return words_path, pauses_path, summary_path

    def export_json(self, output_path: Path | str) -> Path:
        """Export the full session (session + events) as JSON.

        Privacy:
        - `participant_code_raw` is never exported
        - no absolute file paths are exported (only name/relpath/hash/size/origin)
        """
        if self.session.session_id is None:
            raise RuntimeError("No active session to export")

        path = Path(output_path)
        _ensure_parent_dir(path)

        # ---- Serialize session (exclude participant_code_raw) ----
        session_dict: dict[str, Any] = {
            "session_id": str(self.session.session_id),
            "participant_pseudonym": int(self.session.participant_pseudonym) if self.session.participant_pseudonym is not None else None,
            "participant_display_name": self.session.participant_display_name,
            "started_at_ms": self.session.started_at_ms,
            "ended_at_ms": self.session.ended_at_ms,
            "date_local": self.session.date_local,
            # input/context (no absolute paths)
            "input_file_name": self.session.input_file_name,
            "input_file_relpath": self.session.input_file_relpath,
            "input_file_hash": self.session.input_file_hash,
            "input_file_size_bytes": self.session.input_file_size_bytes,
            "input_file_origin": self.session.input_file_origin,
            "platform_os": self.session.platform_os,
            # config
            "profile_name": self.session.profile_name,
            "setting_snapshot": self.session.setting_snapshot,
            # metrics
            "total_words": self.session.total_words,
            "total_paused_ms": self.session.total_paused_ms,
            "total_active_ms": self.session.total_active_ms,
            "accuracy": self.session.accuracy,
            "notes": self.session.notes,
        }

        # ---- Serialize events ----
        word_events_out: list[dict[str, Any]] = []
        for e in self.session.word_events:
            word_events_out.append({
                "session_id": str(e.session_id) if e.session_id else None,
                "event_id": str(e.event_id),
                "trial_index": e.trial_index,
                "stimulus_text": e.stimulus_text,
                "stimulus_type": e.stimulus_type.value,
                "stimulus_source": e.stimulus_source,
                "duration_ms": e.duration_ms,
                "shown_at_ms": e.shown_at_ms,
                "hidden_at_ms": e.hidden_at_ms,
                "actual_duration_ms": e.actual_duration_ms,
                "word_level_speed": e.word_level_speed,
                "game_state": str(e.game_state) if e.game_state is not None else None,
                "response_status": e.response_status.value,
                "response_time_ms": e.response_time_ms,
                "is_correct": e.is_correct,
                "error_type": e.error_type.value,
            })

        pause_events_out: list[dict[str, Any]] = []
        for p in self.session.pause_events:
            pause_events_out.append({
                "pause_id": str(p.pause_id) if p.pause_id else None,
                "session_id": str(p.session_id) if p.session_id else None,
                "is_in_pause": p.is_in_pause,
                "start_ms": p.start_ms,
                "end_ms": p.end_ms,
                "duration_ms": p.duration_ms(),
                "reason": p.reason.value if p.reason is not None else None,
            })

        payload: dict[str, Any] = {
            "session": session_dict,
            "word_events": word_events_out,
            "pause_events": pause_events_out,
        }

        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
