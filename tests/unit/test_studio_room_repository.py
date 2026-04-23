import pytest
from src.studio_room_repository import StudioRoomRepository


def test_exists_returns_true_for_existing_room():
    repo = StudioRoomRepository()
    assert repo.exists(1) is True


def test_is_available_returns_true_for_available_room():
    repo = StudioRoomRepository()
    assert repo.is_available(1) is True


def test_is_available_returns_false_for_unavailable_room():
    repo = StudioRoomRepository()
    assert repo.is_available(3) is False


def test_mark_unavailable_changes_room_state():
    repo = StudioRoomRepository()
    repo.mark_unavailable(1)
    assert repo.is_available(1) is False


def test_mark_available_changes_room_state():
    repo = StudioRoomRepository()
    repo.mark_available(3)
    assert repo.is_available(3) is True


def test_mark_unavailable_raises_for_unknown_room():
    repo = StudioRoomRepository()
    with pytest.raises(ValueError, match="Studio room not found"):
        repo.mark_unavailable(999)
