class Movie:
    def __init__(self, id, name, genre, duration, description, is_deleted=False, created_at=None):
        self.id = id
        self.name = name
        self.genre = genre
        self.duration = duration
        self.description = description
        self.is_deleted = is_deleted
        self.created_at = created_at
