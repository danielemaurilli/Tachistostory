import csv
import hashlib
import uuid
from pathlib import Path

from src.logging.session_logger import (
    DisplayNameRegistry,
    PauseEvent,
    ReasonState,
    ResponseStatus,
    SessionData,
    StimulusType,
    WordEvent,
    export_pause_events_csv,
    export_session_summary_csv,
    export_word_events_csv,
    pseudonym_int_hmac,
)


def test_pseudonym_int_hmac_is_deterministic_and_bounded() -> None:
    secret = b"secret-key"
    code = "ABC123"
    bits = 63

    a = pseudonym_int_hmac(code, secret, bits=bits)
    b = pseudonym_int_hmac(code, secret, bits=bits)
    c = pseudonym_int_hmac(code, b"other-key", bits=bits)

    assert a == b
    assert 0 <= a < (1 << bits)
    assert a != c


def test_word_event_actual_duration_ms() -> None:
    ev = WordEvent(shown_at_ms=100, hidden_at_ms=150)
    assert ev.actual_duration_ms == 50

    ev.hidden_at_ms = 90
    assert ev.actual_duration_ms is None


def test_pause_event_duration_ms() -> None:
    ev = PauseEvent(start_ms=200, end_ms=350, reason=ReasonState.MANUAL_PAUSE)
    assert ev.duration_ms() == 150

    ev.end_ms = 100
    assert ev.duration_ms() is None

    ev.start_ms = None
    assert ev.duration_ms() is None


def test_display_name_registry_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "names.json"
    registry = DisplayNameRegistry(path=path)

    assert registry.get_name(1) is None
    registry.set_name(1, "Alice")

    assert registry.get_name(1) == "Alice"
    assert registry.name_exists("Alice") is True
    assert registry.pseudonym_exists(1) is True

    registry.delete_name(1)
    assert registry.get_name(1) is None


def test_session_data_setter_sets_hash_and_origin(tmp_path: Path) -> None:
    assets_root = tmp_path / "assets"
    assets_root.mkdir()
    file_path = assets_root / "text.txt"
    content = b"hello"
    file_path.write_bytes(content)

    session = SessionData()
    session.setter(file_path, assets_root=assets_root)

    assert session.input_file_name == "text.txt"
    assert session.input_file_size_bytes == len(content)
    assert session.input_file_hash == hashlib.sha256(content).hexdigest()
    assert session.input_file_origin == "assets"
    assert session.input_file_relpath == "text.txt"


def test_session_data_setter_external_drop(tmp_path: Path) -> None:
    assets_root = tmp_path / "assets"
    assets_root.mkdir()
    file_path = tmp_path / "external.txt"
    file_path.write_text("x", encoding="utf-8")

    session = SessionData()
    session.setter(file_path, assets_root=assets_root)

    assert session.input_file_origin == "external_drop"
    assert session.input_file_relpath == ""


def test_export_word_events_csv(tmp_path: Path) -> None:
    session = SessionData(
        session_id=uuid.uuid4(),
        participant_pseudonym=123,
        participant_display_name="Test User",
    )
    event = WordEvent(
        session_id=session.session_id,
        trial_index=1,
        stimulus_text="ciao",
        stimulus_type=StimulusType.WORD,
        response_status=ResponseStatus.CORRECT,
        shown_at_ms=0,
        hidden_at_ms=100,
    )

    path = export_word_events_csv([event], session, tmp_path / "words.csv", include_display_name=True)
    rows = list(csv.DictReader(path.open(encoding="utf-8")))

    assert rows[0]["participant_pseudonym"] == "123"
    assert rows[0]["participant_display_name"] == "Test User"
    assert rows[0]["stimulus_text"] == "ciao"


def test_export_pause_events_csv(tmp_path: Path) -> None:
    session = SessionData(participant_pseudonym=555, participant_display_name="User B")
    event = PauseEvent(session_id=session.session_id, start_ms=10, end_ms=40, reason=ReasonState.ALT_TAB)

    path = export_pause_events_csv([event], session, tmp_path / "pauses.csv", include_display_name=True)
    rows = list(csv.DictReader(path.open(encoding="utf-8")))

    assert rows[0]["participant_pseudonym"] == "555"
    assert rows[0]["participant_display_name"] == "User B"
    assert rows[0]["duration_ms"] == "30"


def test_export_session_summary_csv(tmp_path: Path) -> None:
    session = SessionData(
        session_id=uuid.uuid4(),
        participant_pseudonym=7,
        participant_display_name="User C",
    )
    word_events = [
        WordEvent(is_correct=True, response_time_ms=100),
        WordEvent(is_correct=False, response_time_ms=300),
    ]
    pause_events = [PauseEvent(start_ms=0, end_ms=200)]

    path = export_session_summary_csv(session, word_events, pause_events, tmp_path / "summary.csv")
    row = next(csv.DictReader(path.open(encoding="utf-8")))

    assert row["participant_pseudonym"] == "7"
    assert row["total_trials"] == "2"
    assert row["total_correct"] == "1"
    assert row["total_wrong"] == "1"
    assert row["mean_response_time_ms"] == "200.0"
    assert row["total_pause_ms"] == "200"
