from model.service.db_service import DBService
from model.entity.ticket_booking import TicketBooking

class TicketBookingRepository:
    def __init__(self, db_service: DBService):
        self.db_service = db_service

    def book_ticket(self, user_id, showtime_id, seats_reserved, seat_numbers, total_price):
        query = """
        INSERT INTO ticket_bookings (user_id, showtime_id, seats_reserved, seat_numbers, total_price, booking_time, is_canceled)
        VALUES (%s, %s, %s, %s, %s, NOW(), FALSE)
        """
        params = (user_id, showtime_id, seats_reserved, seat_numbers, total_price)
        return self.db_service.execute_query(query, params)

    def get_user_bookings(self, user_id):
        query = """
        SELECT id, user_id, showtime_id, seats_reserved, seat_numbers, total_price, booking_time, is_canceled 
        FROM ticket_bookings WHERE user_id = %s ORDER BY booking_time DESC
        """
        rows = self.db_service.fetch_all(query, (user_id,))
        return [TicketBooking(*row) for row in rows]

    def get_booking_by_id(self, booking_id):
        query = """
        SELECT id, user_id, showtime_id, seats_reserved, seat_numbers, total_price, booking_time, is_canceled 
        FROM ticket_bookings WHERE id = %s
        """
        row = self.db_service.fetch_one(query, (booking_id,))
        return TicketBooking(*row) if row else None

    def cancel_booking(self, booking_id):
        query = """
        UPDATE ticket_bookings SET is_canceled = TRUE WHERE id = %s AND is_canceled = FALSE
        """
        return self.db_service.execute_query(query, (booking_id,))

    def delete_booking(self, booking_id):
        query = "DELETE FROM ticket_bookings WHERE id = %s AND is_canceled = TRUE"
        return self.db_service.execute_query(query, (booking_id,))
