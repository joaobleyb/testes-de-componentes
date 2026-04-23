import pytest
from unittest.mock import Mock
from src.studio_service import StudioService


def make_service():
    studio_room_repository = Mock()
    artist_repository = Mock()
    session_repository = Mock()
    waitlist_repository = Mock()
    service = StudioService(
        studio_room_repository,
        artist_repository,
        session_repository,
        waitlist_repository,
    )
    return service, studio_room_repository, artist_repository, session_repository, waitlist_repository


def test_reserve_room_raises_when_parameters_are_missing():
    service, *_ = make_service()
    with pytest.raises(ValueError, match="Artist ID and room ID are required"):
        service.reserve_room(None, 1)


def test_reserve_room_returns_false_when_artist_does_not_exist():
    service, _, artist_repository, _, _ = make_service()
    artist_repository.exists.return_value = False
    assert service.reserve_room(999, 1) is False


def test_reserve_room_creates_session_when_all_rules_are_satisfied():
    service, studio_room_repository, artist_repository, session_repository, waitlist_repository = make_service()

    artist_repository.exists.return_value = True
    studio_room_repository.exists.return_value = True
    artist_repository.is_blocked.return_value = False
    artist_repository.has_paid_subscription.return_value = True
    studio_room_repository.is_available.return_value = True
    session_repository.count_active_sessions.return_value = 0
    waitlist_repository.next_artist.return_value = None
    waitlist_repository.has_waitlist.return_value = False

    result = service.reserve_room(10, 1)

    assert result is True
    studio_room_repository.mark_unavailable.assert_called_once_with(1)
    session_repository.create_session.assert_called_once_with(10, 1)


def test_close_room_session_returns_false_when_session_does_not_exist():
    service, _, _, session_repository, _ = make_service()
    session_repository.is_room_with_artist.return_value = False
    assert service.close_room_session(10, 1) is False


def test_join_waitlist_adds_artist_when_rules_are_satisfied():
    service, studio_room_repository, artist_repository, session_repository, waitlist_repository = make_service()

    artist_repository.exists.return_value = True
    studio_room_repository.exists.return_value = True
    artist_repository.is_blocked.return_value = False
    artist_repository.has_paid_subscription.return_value = True
    studio_room_repository.is_available.return_value = False
    waitlist_repository.has_waitlist.return_value = False
    session_repository.is_room_with_artist.return_value = False

    result = service.join_waitlist(10, 1)

    assert result is True
    waitlist_repository.add_to_waitlist.assert_called_once_with(10, 1)


def test_join_waitlist_raises_when_parameters_are_missing():
    service, *_ = make_service()
    with pytest.raises(ValueError, match="Artist ID and room ID are required"):
        service.join_waitlist(None, 1)
