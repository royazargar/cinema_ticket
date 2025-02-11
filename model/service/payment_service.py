from base_service import BaseService

class PaymentService(BaseService):
    def __init__(self, payment_repository):
        super().__init__(payment_repository)

    def process_payment(self, payment_data):
        return self.repository.create(payment_data)
