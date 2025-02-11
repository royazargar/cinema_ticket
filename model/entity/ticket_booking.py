class TicketBooking:
    def __init__(self, booking_id, user_id, showtime_id, seats_reserved, total_price, seat_numbers, booking_time,
                 is_canceled=False):
        self.booking_id = booking_id
        self.user_id = user_id
        self.showtime_id = showtime_id
        self.seats_reserved = seats_reserved
        self.total_price = total_price
        self.seat_numbers = seat_numbers
        self.booking_time = booking_time
        self.is_canceled = is_canceled

    def to_dict(self):
        return {
            "id": self.booking_id,
            "user_id": self.user_id,
            "showtime_id": self.showtime_id,
            "seats_reserved": self.seats_reserved,
            "total_price": self.total_price,
            "seat_numbers": self.seat_numbers,
            "booking_time": self.booking_time,
            "is_canceled": self.is_canceled
        }

    @staticmethod
    def from_dict(data):
        return TicketBooking(
            booking_id=data.get("id"),
            user_id=data.get("user_id"),
            showtime_id=data.get("showtime_id"),
            seats_reserved=data.get("seats_reserved"),
            total_price=data.get("total_price"),
            seat_numbers=data.get("seat_numbers"),
            booking_time=data.get("booking_time"),
            is_canceled=data.get("is_canceled", False)
        )
