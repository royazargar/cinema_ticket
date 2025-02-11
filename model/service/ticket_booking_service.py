from base_service import BaseService

class TicketBookingService(BaseService):
    def __init__(self, ticket_booking_repository):
        super().__init__(ticket_booking_repository)

    def get_now_showing(self):
        return self.repository.get_now_showing()
