from base_service import BaseService

class ShowtimeService(BaseService):
    def __init__(self, showtime_repository):
        super().__init__(showtime_repository)

    def get_upcoming_showtimes(self):
        return self.repository.get_upcoming_showtimes()
