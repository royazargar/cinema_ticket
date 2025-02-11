class PaymentListController:
    def __init__(self, db_service):
        self.db_service = db_service

    def get_user_payments(self, user_id):
        query = """
        SELECT id, reservation_id, amount, payment_status, payment_date 
        FROM payments WHERE user_id = %s ORDER BY payment_date DESC
        """
        results = self.db_service.fetch_all(query, (user_id,))

        payments = [
            {
                "id": row["id"],
                "reservation_id": row["reservation_id"],
                "amount": row["amount"],
                "status": row["payment_status"],
                "date": row["payment_date"]
            }
            for row in results
        ]
        return payments
