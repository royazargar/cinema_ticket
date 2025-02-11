from model.service.db_service import DBService
from controller.base_controller import BaseController

class HallController(BaseController):
    def __init__(self, db_service: DBService):
        super().__init__()
        self.db_service = db_service

    @BaseController.exception_handler
    def get_all_halls(self):
        query = "SELECT id, name, seat_count FROM halls WHERE is_deleted = FALSE"
        return self.db_service.fetch_all(query)

    @BaseController.exception_handler
    def get_hall_by_id(self, hall_id):
        query = "SELECT id, name, seat_count FROM halls WHERE id = %s AND is_deleted = FALSE"
        result = self.db_service.fetch_one(query, (hall_id,))
        return result

    @BaseController.exception_handler
    def add_hall(self, name, seat_count):
        if not all([name, isinstance(seat_count, int) and seat_count > 0]):
            return "❌ اطلاعات ورودی معتبر نیست."

        query = """
        INSERT INTO halls (name, seat_count, is_deleted) 
        VALUES (%s, %s, FALSE)
        """
        params = (name, seat_count)
        self.db_service.execute_query(query, params)
        return "✅ سالن جدید با موفقیت اضافه شد."

    @BaseController.exception_handler
    def update_hall(self, hall_id, name, seat_count):
        if not all([hall_id, name, isinstance(seat_count, int) and seat_count > 0]):
            return "❌ اطلاعات ورودی معتبر نیست."

        query = """
        UPDATE halls SET name = %s, seat_count = %s 
        WHERE id = %s AND is_deleted = FALSE
        """
        params = (name, seat_count, hall_id)
        self.db_service.execute_query(query, params)
        return "✅ اطلاعات سالن با موفقیت بروزرسانی شد."

    @BaseController.exception_handler
    def delete_hall(self, hall_id):
        if not hall_id:
            return "❌ شناسه سالن معتبر نیست."

        query = "UPDATE halls SET is_deleted = TRUE WHERE id = %s"
        self.db_service.execute_query(query, (hall_id,))
        return "✅ سالن با موفقیت حذف شد."
