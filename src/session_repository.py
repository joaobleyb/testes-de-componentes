class SessionRepository:
    def __init__(self):
        self._active_sessions = []

    def create_session(self, artist_id: int, room_id: int) -> None:
        self._active_sessions.append({"artist_id": artist_id, "room_id": room_id})

    def has_active_session(self, room_id: int) -> bool:
        return any(session["room_id"] == room_id for session in self._active_sessions)

    def is_room_with_artist(self, artist_id: int, room_id: int) -> bool:
        return any(
            session["artist_id"] == artist_id and session["room_id"] == room_id
            for session in self._active_sessions
        )

    def count_active_sessions(self, artist_id: int) -> int:
        return sum(1 for session in self._active_sessions if session["artist_id"] == artist_id)

    def close_session(self, artist_id: int, room_id: int) -> None:
        for session in list(self._active_sessions):
            if session["artist_id"] == artist_id and session["room_id"] == room_id:
                self._active_sessions.remove(session)
                return
        raise ValueError("Active session not found")
