from src.artist_repository import ArtistRepository


def test_exists_returns_true_for_known_artist():
    repo = ArtistRepository()
    assert repo.exists(10) is True


def test_exists_returns_false_for_unknown_artist():
    repo = ArtistRepository()
    assert repo.exists(999) is False


def test_is_blocked_returns_true_when_artist_is_blocked():
    repo = ArtistRepository()
    assert repo.is_blocked(20) is True


def test_has_paid_subscription_returns_false_when_subscription_is_unpaid():
    repo = ArtistRepository()
    assert repo.has_paid_subscription(30) is False
