from base_service import BaseService

class MovieService(BaseService):
    def __init__(self, movie_repository):
        super().__init__(movie_repository)

    def get_now_showing(self):
        return self.repository.get_now_showing()
