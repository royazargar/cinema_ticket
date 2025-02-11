import bcrypt

class User:
    def __init__(self, id, username, email, role_id, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.role_id = role_id  # 1 = ادمین، 2 = مشتری
        self.created_at = created_at
        self._password_hash = None

    def set_password(self, password):
        self._password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self._password_hash.encode())

    @property
    def password_hash(self):
        raise AttributeError("🔒 دسترسی مستقیم به `password_hash` مجاز نیست!")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, role_id={self.role_id})>"
