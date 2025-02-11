from model.service.db_service import DBService


class BaseRepository:
    def __init__(self, db_service: DBService):
        self.db_service = db_service

    def execute_query(self, query, params=None):
        return self.db_service.execute_query(query, params)

    def fetch_all(self, query, params=None):
        return self.db_service.fetch_all(query, params)

    def fetch_one(self, query, params=None):
        return self.db_service.fetch_one(query, params)
