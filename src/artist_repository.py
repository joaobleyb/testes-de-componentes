class ArtistRepository:
    def __init__(self):
        self._artists = {
            10: {"name": "Ana", "blocked": False, "subscription_paid": True},
            20: {"name": "Bruno", "blocked": True, "subscription_paid": True},
            30: {"name": "Carla", "blocked": False, "subscription_paid": False},
            40: {"name": "Diego", "blocked": False, "subscription_paid": True},
            50: {"name": "Novo", "blocked": False, "subscription_paid": True}
        }

    def exists(self, artist_id: int) -> bool:
        return artist_id in self._artists

    def is_blocked(self, artist_id: int) -> bool:
        if artist_id not in self._artists:
            return False
        return self._artists[artist_id]["blocked"]

    def has_paid_subscription(self, artist_id: int) -> bool:
        if artist_id not in self._artists:
            return False
        return self._artists[artist_id]["subscription_paid"]
