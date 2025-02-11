from model.repository.base_repository import BaseRepository

class PaymentRepository(BaseRepository):
    def create_payment(self, user_id, reservation_id, amount, status="pending"):
        query = """
        INSERT INTO payments (user_id, reservation_id, amount, payment_status, payment_date)
        VALUES (%s, %s, %s, %s, NOW())
        """
        params = (user_id, reservation_id, amount, status)
        return self.execute_query(query, params)

    def get_all_payments(self):
        query = "SELECT * FROM payments"
        return self.fetch_all(query)

    def get_payment_by_id(self, payment_id):
        query = "SELECT * FROM payments WHERE id = %s"
        return self.fetch_one(query, (payment_id,))

    def update_payment(self, payment_id, amount, status):
        query = """
        UPDATE payments 
        SET amount = %s, payment_status = %s
        WHERE id = %s
        """
        params = (amount, status, payment_id)
        return self.execute_query(query, params)

    def delete_payment(self, payment_id):
        query = "DELETE FROM payments WHERE id = %s"
        return self.execute_query(query, (payment_id,))
