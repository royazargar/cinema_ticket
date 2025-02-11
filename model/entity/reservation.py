class Reservation:
    def __init__(self, id, user_id, movie_id, showtime_id, ticket_count, status, created_at=None):
        self.id = id
        self.user_id = user_id
        self.movie_id = movie_id
        self.showtime_id = showtime_id
        self.ticket_count = ticket_count
        self.status = status
        self.created_at = created_at

    def is_pending(self):
        return self.status == "pending"
