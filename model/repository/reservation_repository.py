class ReservationRepository:
    def __init__(self, db_service):
        self.db_service = db_service

    def get_reservations_by_user(self, user_id):
        query = """
            SELECT id, user_id, movie_id, showtime_id, ticket_count, status, created_at
            FROM reservations
            WHERE user_id = %s
        """
        return self.db_service.fetch_all(query, (user_id,))

    def get_reservation_by_id(self, reservation_id):
        query = """
            SELECT id, user_id, movie_id, showtime_id, ticket_count, status, created_at
            FROM reservations
            WHERE id = %s
        """
        return self.db_service.fetch_one(query, (reservation_id,))

    def cancel_reservation(self, reservation_id):
        query = """
            UPDATE reservations 
            SET status = 'canceled' 
            WHERE id = %s
        """
        return self.db_service.execute_query(query, (reservation_id,))
