from base_service import BaseService

class UserService(BaseService):
    def __init__(self, user_repository):
        super().__init__(user_repository)

    def get_active_users(self):
        return self.repository.get_active_users()
