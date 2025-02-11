from model.service.db_service import DBService

class TicketBookingController:
    def __init__(self, db_service: DBService):
        self.db_service = db_service

    def book_ticket(self, user_id, showtime_id, selected_seats, ticket_price):
        reserved_seats_query = "SELECT seat_numbers FROM ticket_bookings WHERE showtime_id = %s AND is_canceled = FALSE"
        reserved_seats_result = self.db_service.fetch_all(reserved_seats_query, (showtime_id,))

        reserved_seats = set()
        for row in reserved_seats_result:
            reserved_seats.update(map(int, row['seat_numbers'].split(',')))

        if any(seat in reserved_seats for seat in selected_seats):
            return False, "❌ برخی از صندلی‌های انتخاب‌شده قبلاً رزرو شده‌اند!"

        total_price = len(selected_seats) * ticket_price
        seat_numbers = ",".join(map(str, selected_seats))

        query_booking = """
        INSERT INTO ticket_bookings (user_id, showtime_id, seats_reserved, total_price, seat_numbers, booking_time, is_canceled)
        VALUES (%s, %s, %s, %s, %s, NOW(), FALSE)
        """
        success_booking = self.db_service.execute_query(query_booking, (
            user_id, showtime_id, len(selected_seats), total_price, seat_numbers))

        if not success_booking:
            return False, "❌ خطا در ثبت رزرو."

        insert_reservation_query = """
        INSERT INTO reservations (user_id, movie_id, showtime_id, ticket_count, status, created_at)
        VALUES (%s, (SELECT movie_id FROM showtimes WHERE id = %s), %s, %s, 'pending', NOW())
        """
        success_reservation = self.db_service.execute_query(insert_reservation_query, (
            user_id, showtime_id, showtime_id, len(selected_seats)))

        if success_reservation:
            return True, "✅ رزرو با موفقیت انجام شد."
        return False, "❌ خطا در ثبت اطلاعات رزرو."

    def get_ticket_price(self, showtime_id):
        query = "SELECT ticket_price FROM showtimes WHERE id = %s"
        result = self.db_service.fetch_one(query, (showtime_id,))
        return result['ticket_price'] if result and 'ticket_price' in result else 0

    def get_user_bookings(self, user_id):
        query = """
        SELECT tb.id, s.start_time, m.name AS movie_name, tb.seats_reserved, tb.total_price, tb.booking_time, tb.is_canceled, tb.seat_numbers
        FROM ticket_bookings tb
        JOIN showtimes s ON tb.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        WHERE tb.user_id = %s
        """
        return self.db_service.fetch_all(query, (user_id,))

    def get_hall_info_by_showtime(self, showtime_id):
        query = "SELECT hall_id, available_seats FROM showtimes WHERE id = %s"
        result = self.db_service.fetch_one(query, (showtime_id,))
        if result:
            return result['hall_id'], result['available_seats']
        return None

    def cancel_booking(self, booking_id):
        query_get_seats = "SELECT showtime_id, seat_numbers FROM ticket_bookings WHERE id = %s AND is_canceled = FALSE"
        booking_info = self.db_service.fetch_one(query_get_seats, (booking_id,))

        if not booking_info:
            return False, "❌ امکان لغو این رزرو وجود ندارد."

        showtime_id = booking_info['showtime_id']
        canceled_seats = booking_info['seat_numbers']

        query_cancel = "UPDATE ticket_bookings SET is_canceled = TRUE WHERE id = %s"
        success = self.db_service.execute_query(query_cancel, (booking_id,))

        if success:
            query_update_showtime = """
            UPDATE showtimes 
            SET available_seats = CONCAT_WS(',', available_seats, %s) 
            WHERE id = %s
            """
            self.db_service.execute_query(query_update_showtime, (canceled_seats, showtime_id))

            return True, "✅ رزرو با موفقیت لغو شد و صندلی‌ها آزاد شدند."
        return False, "❌ امکان لغو این رزرو وجود ندارد."

    def delete_booking(self, booking_id):
        query = "DELETE FROM ticket_bookings WHERE id = %s AND is_canceled = TRUE"
        success = self.db_service.execute_query(query, (booking_id,))
        if success:
            return True, "✅ رزرو با موفقیت حذف شد."
        return False, "❌ امکان حذف رزرو وجود ندارد. ابتدا رزرو را لغو کنید!"
