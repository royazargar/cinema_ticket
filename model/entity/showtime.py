class Showtime:
    def __init__(self, id, movie_id, hall_id, start_time, available_seats, start_date, end_date, movie_duration, ticket_price=0, is_deleted=False):
        self.id = id
        self.movie_id = movie_id
        self.hall_id = hall_id
        self.start_time = start_time
        self.available_seats = available_seats
        self.start_date = start_date
        self.end_date = end_date
        self.movie_duration = movie_duration
        self.ticket_price = ticket_price
        self.is_deleted = is_deleted

    def to_dict(self):
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "hall_id": self.hall_id,
            "start_time": self.start_time,
            "available_seats": self.available_seats,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "movie_duration": self.movie_duration,
            "ticket_price": self.ticket_price,
            "is_deleted": self.is_deleted
        }

    @staticmethod
    def from_dict(data):
        return Showtime(
            id=data.get("id"),
            movie_id=data.get("movie_id"),
            hall_id=data.get("hall_id"),
            start_time=data.get("start_time"),
            available_seats=data.get("available_seats"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            movie_duration=data.get("movie_duration"),
            ticket_price=data.get("ticket_price", 0),
            is_deleted=data.get("is_deleted", False)
        )
