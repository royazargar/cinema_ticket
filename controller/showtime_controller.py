from model.service.db_service import DBService
from controller.base_controller import BaseController


class ShowtimeController(BaseController):
    def __init__(self, db_service: DBService):
        super().__init__()
        self.db_service = db_service

    @BaseController.exception_handler
    def is_showtime_conflicting(self, hall_id, start_time, start_date, movie_duration):

        query = """
            SELECT id FROM showtimes 
            WHERE hall_id = %s 
            AND start_date = %s 
            AND (
                (start_time <= %s AND ADDTIME(start_time, SEC_TO_TIME(movie_duration * 60)) > %s)  -- تداخل از قبل یا داخل بازه
                OR (start_time >= %s AND start_time < ADDTIME(%s, SEC_TO_TIME(%s * 60)))  -- تداخل بعدی
            ) 
            AND is_deleted = FALSE
            """
        params = (hall_id, start_date, start_time, start_time, start_time, start_time, movie_duration)
        existing_showtime = self.db_service.fetch_one(query, params)

        return existing_showtime is not None

    @BaseController.exception_handler
    def get_all_showtimes(self):
        query = """
        SELECT id, movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, ticket_price
        FROM showtimes WHERE is_deleted = FALSE
        """
        return self.db_service.fetch_all(query)

    @BaseController.exception_handler
    def get_hall_info_by_showtime(self, showtime_id):
        query = "SELECT hall_id, available_seats FROM showtimes WHERE id = %s"
        result = self.db_service.fetch_one(query, (showtime_id,))
        if result:
            return result['hall_id'], result['available_seats']
        return None

    @BaseController.exception_handler
    def get_showtimes_by_movie(self, movie_id):
        if not movie_id:
            return []

        query = """
        SELECT id, hall_id, start_time, start_date, end_date, available_seats, ticket_price
        FROM showtimes
        WHERE movie_id = %s AND is_deleted = FALSE
        """
        return self.db_service.fetch_all(query, (movie_id,))

    @BaseController.exception_handler
    def get_reserved_seats(self, showtime_id):
        query = "SELECT seat_numbers FROM ticket_bookings WHERE showtime_id = %s"
        reserved_seats = self.db_service.fetch_all(query, (showtime_id,))

        all_seats = []
        for row in reserved_seats:
            if row['seat_numbers']:
                all_seats.extend(map(int, row['seat_numbers'].split(',')))

        return all_seats

    @BaseController.exception_handler
    def get_ticket_price(self, showtime_id):
        query = "SELECT ticket_price FROM showtimes WHERE id = %s"
        result = self.db_service.fetch_one(query, (showtime_id,))
        return result["ticket_price"] if result else None

    @BaseController.exception_handler
    def add_showtime(self, movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats,
                     ticket_price):
        if self.is_showtime_conflicting(hall_id, start_time, start_date, movie_duration):
            return "❌ تداخل سانس وجود دارد. لطفاً زمان دیگری را انتخاب کنید."

        query = """
            INSERT INTO showtimes (movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, ticket_price, is_deleted) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE)
            """
        params = (movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, ticket_price)
        self.db_service.execute_query(query, params)
        return "✅ سانس جدید با موفقیت اضافه شد."

    @BaseController.exception_handler
    def update_showtime(self, showtime_id, movie_id, hall_id, start_time, start_date, end_date, movie_duration,
                        available_seats, ticket_price):
        if self.is_showtime_conflicting(hall_id, start_time, start_date, movie_duration):
            return "❌ تداخل سانس وجود دارد. لطفاً زمان دیگری را انتخاب کنید."

        query = """
            UPDATE showtimes 
            SET movie_id = %s, hall_id = %s, start_time = %s, start_date = %s, end_date = %s, movie_duration = %s, available_seats = %s, ticket_price = %s
            WHERE id = %s AND is_deleted = FALSE
            """
        params = (
        movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, ticket_price, showtime_id)
        self.db_service.execute_query(query, params)
        return "✅ اطلاعات سانس با موفقیت بروزرسانی شد."

    @BaseController.exception_handler
    def delete_showtime(self, showtime_id):
        if not showtime_id:
            return "❌ شناسه زمان نمایش معتبر نیست."

        query = "UPDATE showtimes SET is_deleted = TRUE WHERE id = %s"
        self.db_service.execute_query(query, (showtime_id,))
        return "✅ زمان نمایش با موفقیت حذف شد."
