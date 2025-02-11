from model.service.db_service import DBService
from controller.base_controller import BaseController

class PaymentController(BaseController):
    def __init__(self, db_service: DBService):
        self.db_service = db_service

    @BaseController.exception_handler
    def get_all_payments(self):
        query = "SELECT * FROM payments"
        return self.db_service.fetch_all(query)

    @BaseController.exception_handler
    def add_payment(self, user_id, reservation_id, amount, status="pending"):
        query = """
        INSERT INTO payments (user_id, reservation_id, amount, payment_status) 
        VALUES (%s, %s, %s, %s)
        """
        params = (user_id, reservation_id, amount, status)
        self.db_service.execute_query(query, params)
        return "✅ پرداخت با موفقیت ثبت شد."

    @BaseController.exception_handler
    def update_payment(self, payment_id, status):
        query = "UPDATE payments SET payment_status = %s WHERE id = %s"
        self.db_service.execute_query(query, (status, payment_id))
        return "✅ وضعیت پرداخت با موفقیت بروزرسانی شد."

    @BaseController.exception_handler
    def process_payment(self, user_id, reservation_id):
        query = """
        SELECT total_price, is_canceled 
        FROM ticket_bookings 
        WHERE id = %s AND user_id = %s
        """
        result = self.db_service.fetch_one(query, (reservation_id, user_id))

        if not result:
            return False, "❌ رزرو موردنظر یافت نشد."

        total_price = result["total_price"]
        is_canceled = result["is_canceled"]

        if is_canceled:
            return False, "❌ این رزرو لغو شده و قابل پرداخت نیست."

        check_payment_query = """
        SELECT id FROM payments WHERE reservation_id = %s AND payment_status = 'completed'
        """
        existing_payment = self.db_service.fetch_one(check_payment_query, (reservation_id,))

        if existing_payment:
            return False, "❌ این رزرو قبلاً پرداخت شده است."

        add_payment_query = """
        INSERT INTO payments (user_id, reservation_id, amount, payment_status) 
        VALUES (%s, %s, %s, 'completed')
        """
        self.db_service.execute_query(add_payment_query, (user_id, reservation_id, total_price))

        return True, "✅ پرداخت با موفقیت انجام شد."

    @BaseController.exception_handler
    def get_user_payments(self, user_id):
        query = """
        SELECT p.id, p.reservation_id, p.amount, p.payment_status, p.payment_date, 
               m.name AS movie_name, s.start_time
        FROM payments p
        JOIN ticket_bookings tb ON p.reservation_id = tb.id
        JOIN showtimes s ON tb.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        WHERE p.user_id = %s
        """
        return self.db_service.fetch_all(query, (user_id,))
