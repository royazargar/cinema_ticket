import bcrypt
from model.repository.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def create_user(self, username, password, email, role_id):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        query = """
        INSERT INTO users (username, password, email, role_id)
        VALUES (%s, %s, %s, %s)
        """
        params = (username, password_hash, email, role_id)
        return self.execute_query(query, params)

    def get_user_by_username(self, username):
        query = """
        SELECT id, username, password, role_id
        FROM users
        WHERE username = %s
        """
        params = (username,)
        return self.fetch_one(query, params)

    def get_user_by_username_and_password(self, username, password):
        user = self.get_user_by_username(username)
        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            return {
                "id": user["id"],
                "username": user["username"],
                "role_id": user["role_id"],
            }
        return None

    def get_user_by_id(self, user_id):
        query = "SELECT id, username, email, role_id FROM users WHERE id = %s"
        params = (user_id,)
        return self.fetch_one(query, params)
