from model.service.db_service import DBService
from controller.base_controller import BaseController

class MovieController(BaseController):
    def __init__(self, db_service: DBService):
        super().__init__()
        self.db_service = db_service

    @BaseController.exception_handler
    def get_all_movies(self):
        query = "SELECT id, name, genre, duration, description FROM movies WHERE is_deleted = FALSE"
        return self.db_service.fetch_all(query)

    @BaseController.exception_handler
    def get_movie_by_id(self, movie_id):
        query = "SELECT id, name, genre, duration FROM movies WHERE id = %s AND is_deleted = FALSE"
        result = self.db_service.fetch_one(query, (movie_id,))
        return result

    @BaseController.exception_handler
    def get_showtimes(self, movie_id):
        query = """
        SELECT id, start_time, start_date, hall_id, available_seats
        FROM showtimes
        WHERE movie_id = %s AND is_deleted = FALSE
        """
        return self.db_service.fetch_all(query, (movie_id,))

    @BaseController.exception_handler
    def get_showtimes_by_movie(self, movie_id):
        if not movie_id:
            print("⚠️ movie_id مقدار نامعتبر است!")
            return []

        print(f"🔍 دریافت سانس‌ها برای فیلم با ID: {movie_id}")
        query = """
        SELECT id, hall_id, start_time, start_date, end_date, available_seats
        FROM showtimes
        WHERE movie_id = %s AND is_deleted = FALSE
        """
        result = self.db_service.fetch_all(query, (movie_id,))
        print(f"🎬 نتیجه کوئری: {result}")
        return result if result else []

    @BaseController.exception_handler
    def get_movie_by_id(self, movie_id):
        query = "SELECT id, name, genre, duration FROM movies WHERE id = %s AND is_deleted = FALSE"
        result = self.db_service.fetch_one(query, (movie_id,))
        return result

    @BaseController.exception_handler
    def add_movie(self, name, genre, duration, description):
        if not all([name, genre, isinstance(duration, int) and duration > 0, description]):
            return "❌ اطلاعات ورودی معتبر نیست."

        query = """
        INSERT INTO movies (name, genre, duration, description, is_deleted, created_at) 
        VALUES (%s, %s, %s, %s, FALSE, NOW())
        """
        params = (name, genre, duration, description)
        self.db_service.execute_query(query, params)
        return "✅ فیلم جدید با موفقیت اضافه شد."

    @BaseController.exception_handler
    def update_movie(self, movie_id, name, genre, duration, description):
        if not all([movie_id, name, genre, isinstance(duration, int) and duration > 0, description]):
            return "❌ اطلاعات ورودی معتبر نیست."

        query = """
        UPDATE movies SET name = %s, genre = %s, duration = %s, description = %s 
        WHERE id = %s AND is_deleted = FALSE
        """
        params = (name, genre, duration, description, movie_id)
        self.db_service.execute_query(query, params)
        return "✅ اطلاعات فیلم با موفقیت بروزرسانی شد."

    @BaseController.exception_handler
    def delete_movie(self, movie_id):
        if not movie_id:
            return "❌ شناسه فیلم معتبر نیست."

        query = "UPDATE movies SET is_deleted = TRUE WHERE id = %s"
        self.db_service.execute_query(query, (movie_id,))
        return "✅ فیلم با موفقیت حذف شد."
