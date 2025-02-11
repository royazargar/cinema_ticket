from model.service.db_service import DBService
from model.entity.movie import Movie

class MovieRepository:
    def __init__(self, db_service: DBService):
        self.db_service = db_service

    def get_all_movies(self):
        query = "SELECT id, name, genre, duration, description, created_at FROM movies WHERE is_deleted = FALSE"
        rows = self.db_service.fetch_all(query)
        return [Movie(*row) for row in rows]

    def get_movie_by_id(self, movie_id):
        query = "SELECT id, name, genre, duration, description, created_at FROM movies WHERE id = %s AND is_deleted = FALSE"
        row = self.db_service.fetch_one(query, (movie_id,))
        return Movie(*row) if row else None

    def add_movie(self, name, genre, duration, description):
        query = """
        INSERT INTO movies (name, genre, duration, description, is_deleted, created_at) 
        VALUES (%s, %s, %s, %s, FALSE, NOW())
        """
        params = (name, genre, duration, description)
        self.db_service.execute_query(query, params)

    def update_movie(self, movie_id, name, genre, duration, description):
        query = """
        UPDATE movies SET name = %s, genre = %s, duration = %s, description = %s 
        WHERE id = %s AND is_deleted = FALSE
        """
        params = (name, genre, duration, description, movie_id)
        self.db_service.execute_query(query, params)

    def delete_movie(self, movie_id):
        query = "UPDATE movies SET is_deleted = TRUE WHERE id = %s"
        self.db_service.execute_query(query, (movie_id,))
