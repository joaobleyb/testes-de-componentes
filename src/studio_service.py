class StudioService:
    def __init__(self, studio_room_repository, artist_repository, session_repository, waitlist_repository):
        self.studio_room_repository = studio_room_repository
        self.artist_repository = artist_repository
        self.session_repository = session_repository
        self.waitlist_repository = waitlist_repository

    def reserve_room(self, artist_id: int, room_id: int) -> bool:
        if not artist_id or not room_id:
            raise ValueError("Artist ID and room ID are required")

        if not self.artist_repository.exists(artist_id):
            return False

        if not self.studio_room_repository.exists(room_id):
            return False

        if self.artist_repository.is_blocked(artist_id):
            return False

        if not self.artist_repository.has_paid_subscription(artist_id):
            return False

        next_artist = self.waitlist_repository.next_artist(room_id)
        if next_artist is not None and next_artist != artist_id:
            return False

        if next_artist is None and not self.studio_room_repository.is_available(room_id):  # Adicionado o 'next_artist is None' para verificar se nao existe proximo artista na fila,
            return False                                                                   # para ai sim marcar como available

        if self.session_repository.count_active_sessions(artist_id) >= 2:
            return False

        self.studio_room_repository.mark_unavailable(room_id)
        self.session_repository.create_session(artist_id, room_id)

        if self.waitlist_repository.has_waitlist(artist_id, room_id):
            self.waitlist_repository.remove_from_waitlist(artist_id, room_id)

        return True

    def close_room_session(self, artist_id: int, room_id: int) -> bool:
        if not artist_id or not room_id:
            raise ValueError("Artist ID and room ID are required")

        if not self.session_repository.is_room_with_artist(artist_id, room_id):
            return False

        self.session_repository.close_session(artist_id, room_id)

        if not self.waitlist_repository.has_any_waitlist(room_id):
            self.studio_room_repository.mark_available(room_id)

        return True

    def join_waitlist(self, artist_id: int, room_id: int) -> bool:
        if not artist_id or not room_id:
            raise ValueError("Artist ID and room ID are required")

        if not self.artist_repository.exists(artist_id):
            return False

        if not self.studio_room_repository.exists(room_id):
            return False

        if self.artist_repository.is_blocked(artist_id):
            return False

        if not self.artist_repository.has_paid_subscription(artist_id):
            return False

        if self.studio_room_repository.is_available(room_id):
            return False

        if self.waitlist_repository.has_waitlist(artist_id, room_id):
            return False

        if self.session_repository.is_room_with_artist(artist_id, room_id):
            return False

        self.waitlist_repository.add_to_waitlist(artist_id, room_id)
        return True
