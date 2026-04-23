class WaitlistRepository:
    def __init__(self):
        self._waitlist = []

    def add_to_waitlist(self, artist_id: int, room_id: int) -> None:
        self._waitlist.append({"artist_id": artist_id, "room_id": room_id})

    def has_waitlist(self, artist_id: int, room_id: int) -> bool:
        return any(
            entry["artist_id"] == artist_id and entry["room_id"] == room_id
            for entry in self._waitlist
        )

    def has_any_waitlist(self, room_id: int) -> bool:
        return any(entry["room_id"] == room_id for entry in self._waitlist)

    def next_artist(self, room_id: int):
        for entry in self._waitlist:
            if entry["room_id"] == room_id:
                return entry["artist_id"]
        return None

    def remove_from_waitlist(self, artist_id: int, room_id: int) -> None:
        for entry in list(self._waitlist):
            if entry["artist_id"] == artist_id and entry["room_id"] == room_id:
                self._waitlist.remove(entry)
                return
        raise ValueError("Waitlist entry not found")
