class ReservationController:
    def __init__(self, db_service):
        if not hasattr(db_service, "fetch_all"):
            raise AttributeError("db_service باید متد fetch_all داشته باشد!")
        self.db_service = db_service

    def get_user_reservations(self, user_id):
        query = """
        SELECT r.id, r.user_id, r.movie_id, r.showtime_id, m.name AS movie_name, 
               s.start_time, s.ticket_price, r.ticket_count, r.status, r.created_at, 
               COALESCE(p.payment_status, 'pending') AS payment_status
        FROM reservations r
        JOIN movies m ON r.movie_id = m.id
        JOIN showtimes s ON r.showtime_id = s.id  -- اضافه شد
        LEFT JOIN payments p ON r.id = p.reservation_id
        WHERE r.user_id = %s
        """
        results = self.db_service.fetch_all(query, (user_id,))

        print(f"📌 داده‌های دریافتی از get_user_reservations: {results}")

        reservations = [
            {
                "id": row["id"],
                "user_id": row["user_id"],
                "movie_id": row["movie_id"],
                "showtime_id": row["showtime_id"],
                "movie_name": row["movie_name"],
                "start_time": row["start_time"],
                "ticket_price": row["ticket_price"],
                "ticket_count": row["ticket_count"],
                "total_price": row["ticket_price"] * row["ticket_count"],  # مبلغ کل اضافه شد
                "status": row["status"],
                "created_at": row["created_at"],
                "payment_status": row["payment_status"]
            }
            for row in results
        ]
        return reservations

    def pay_reservation(self, reservation_id):
        query = "SELECT payment_status FROM payments WHERE reservation_id = %s"
        existing_payment = self.db_service.fetch_one(query, (reservation_id,))

        if existing_payment and existing_payment["payment_status"] == "completed":
            return False, "این رزرو قبلاً پرداخت شده است."

        update_query = """
        UPDATE payments 
        SET payment_status = 'completed', payment_date = NOW()
        WHERE reservation_id = %s
        """
        success = self.db_service.execute_query(update_query, (reservation_id,))

        if success:
            return True, "پرداخت با موفقیت انجام شد."
        return False, "خطا در پردازش پرداخت."

    def delete_reservation(self, reservation_id):
        query = "SELECT status FROM reservations WHERE id = %s"
        result = self.db_service.fetch_one(query, (reservation_id,))

        if not result:
            return False, "❌ رزرو مورد نظر یافت نشد."

        status = result["status"]

        if status != "pending":
            return False, "⚠️ فقط رزروهای در انتظار پرداخت قابل حذف هستند."

        payment_check = "SELECT payment_status FROM payments WHERE reservation_id = %s"
        payment_result = self.db_service.fetch_one(payment_check, (reservation_id,))

        if payment_result and payment_result["payment_status"] == "completed":
            return False, "❌ رزرو پرداخت شده را نمی‌توان حذف کرد."

        delete_query = "DELETE FROM reservations WHERE id = %s"
        self.db_service.execute_query(delete_query, (reservation_id,))
        return True, "✅ رزرو با موفقیت حذف شد."
