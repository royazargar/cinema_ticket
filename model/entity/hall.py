class Hall:
    def __init__(self, id, name, seat_count, is_deleted=False, created_at=None):
        self.id = id
        self.name = name
        self.seat_count = seat_count
        self.is_deleted = is_deleted
        self.created_at = created_at