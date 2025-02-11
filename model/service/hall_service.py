from base_service import BaseService

class HallService(BaseService):
    def __init__(self, hall_repository):
        super().__init__(hall_repository)

    def get_available_halls(self):
        return self.repository.get_all_halls()
