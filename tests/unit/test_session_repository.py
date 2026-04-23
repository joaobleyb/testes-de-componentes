import pytest
from src.session_repository import SessionRepository


def test_create_session_registers_active_session():
    repo = SessionRepository()
    repo.create_session(10, 1)
    assert repo.has_active_session(1) is True


def test_count_active_sessions_counts_only_artist_sessions():
    repo = SessionRepository()
    repo.create_session(10, 1)
    repo.create_session(10, 2)
    repo.create_session(40, 3)
    assert repo.count_active_sessions(10) == 2


def test_is_room_with_artist_returns_true_for_matching_session():
    repo = SessionRepository()
    repo.create_session(10, 1)
    assert repo.is_room_with_artist(10, 1) is True


def test_close_session_removes_active_session():
    repo = SessionRepository()
    repo.create_session(10, 1)
    repo.close_session(10, 1)
    assert repo.has_active_session(1) is False


def test_close_session_raises_for_unknown_session():
    repo = SessionRepository()
    with pytest.raises(ValueError, match="Active session not found"):
        repo.close_session(10, 1)
