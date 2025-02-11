from datetime import datetime


class Payment:
    VALID_STATUSES = {"pending", "completed", "failed"}

    def __init__(
        self,
        id: int,
        user_id: int,
        reservation_id: int,
        amount: float,
        payment_status: str = "pending",
        payment_date: datetime = None
    ):
        self.id = id
        self.user_id = user_id
        self.reservation_id = reservation_id
        self.amount = amount
        self.payment_date = payment_date or datetime.now()

        if payment_status not in self.VALID_STATUSES:
            raise ValueError(f"❌ مقدار '{payment_status}' برای payment_status معتبر نیست. "
                             f"مقادیر مجاز: {self.VALID_STATUSES}")
        self.payment_status = payment_status

    def is_completed(self) -> bool:
        return self.payment_status == "completed"

    def mark_as_completed(self):
        self.payment_status = "completed"
        self.payment_date = datetime.now()

    def __repr__(self) -> str:
        return (
            f"Payment(id={self.id}, user_id={self.user_id}, reservation_id={self.reservation_id}, "
            f"amount={self.amount}, payment_status='{self.payment_status}', payment_date={self.payment_date})"
        )
