from base_service import BaseService

class ReservationService(BaseService):
    def __init__(self, reservation_repository):
        super().__init__(reservation_repository)

    def get_upcoming_reservation(self):
        return self.repository.get_upcoming_reservation()
