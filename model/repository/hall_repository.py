from model.repository.base_repository import BaseRepository

class HallRepository(BaseRepository):
    def __init__(self, db_service):
        super().__init__(db_service)

    def get_all_halls(self):
        query = "SELECT * FROM halls WHERE is_deleted = FALSE"
        return self.db_service.fetch_all(query)

    def get_hall_by_id(self, hall_id):
        query = "SELECT * FROM halls WHERE id = %s AND is_deleted = FALSE"
        return self.db_service.fetch_one(query, (hall_id,))

    def add_hall(self, name, seat_count):
        query = "INSERT INTO halls (name, seat_count) VALUES (%s, %s)"
        self.db_service.execute_query(query, (name, seat_count))

    def update_hall(self, hall_id, name, seat_count):
        query = "UPDATE halls SET name = %s, seat_count = %s WHERE id = %s"
        self.db_service.execute_query(query, (name, seat_count, hall_id))

    def delete_hall(self, hall_id):
        query = "UPDATE halls SET is_deleted = TRUE WHERE id = %s"
        self.db_service.execute_query(query, (hall_id,))
