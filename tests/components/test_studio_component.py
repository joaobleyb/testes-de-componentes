import pytest
from src.studio_service import StudioService
from src.artist_repository import ArtistRepository
from src.studio_room_repository import StudioRoomRepository
from src.session_repository import SessionRepository
from src.waitlist_repository import WaitlistRepository


@pytest.fixture
def service():
    return StudioService(
        StudioRoomRepository(),
        ArtistRepository(),
        SessionRepository(),
        WaitlistRepository()
    )