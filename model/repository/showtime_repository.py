from model.repository.base_repository import BaseRepository

class ShowtimeRepository(BaseRepository):
    def create_showtime(self, movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, ticket_price):
        query = """
        INSERT INTO showtimes (movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, ticket_price, is_deleted)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE)
        """
        params = (movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, ticket_price)
        return self.execute_query(query, params)

    def get_all_showtimes(self):
        query = """
        SELECT id, movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, ticket_price 
        FROM showtimes WHERE is_deleted = FALSE
        """
        return self.fetch_all(query)

    def get_showtime_by_id(self, showtime_id):
        query = """
        SELECT id, movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, ticket_price 
        FROM showtimes WHERE id = %s AND is_deleted = FALSE
        """
        params = (showtime_id,)
        return self.fetch_one(query, params)

    def update_showtime(self, showtime_id, movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, ticket_price):
        query = """
        UPDATE showtimes 
        SET movie_id = %s, hall_id = %s, start_time = %s, start_date = %s, end_date = %s, movie_duration = %s, 
            available_seats = %s, ticket_price = %s
        WHERE id = %s AND is_deleted = FALSE
        """
        params = (movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, ticket_price, showtime_id)
        return self.execute_query(query, params)

    def delete_showtime(self, showtime_id):
        query = "UPDATE showtimes SET is_deleted = TRUE WHERE id = %s"
        params = (showtime_id,)
        return self.execute_query(query, params)
