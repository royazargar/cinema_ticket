import bcrypt
from model.service.db_service import DBService
from controller.base_controller import BaseController


class UserController(BaseController):
    def __init__(self, db_service: DBService):
        super().__init__()  # فراخوانی سازنده‌ی کلاس پدر
        self.db_service = db_service

    @BaseController.exception_handler
    def register_user(self, username, password, email, role_id):
        """ ثبت نام کاربر با هش کردن رمز عبور """
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # هش کردن رمز
        query = "INSERT INTO users (username, password, email, role_id) VALUES (%s, %s, %s, %s)"
        params = (username, hashed_password, email, role_id)
        self.db_service.execute_query(query, params)
        return "✅ کاربر با موفقیت ثبت شد."

    @BaseController.exception_handler
    def login_user(self, username, password):
        """ بررسی ورود کاربر با مقایسه رمز عبور هش‌شده """
        query = "SELECT id, username, role_id, password FROM users WHERE username = %s"
        params = (username,)
        user = self.db_service.fetch_one(query, params)

        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            return {"id": user["id"], "username": user["username"], "role_id": user["role_id"]}
        return None

    @BaseController.exception_handler
    def get_user_info(self, user_id):
        """ دریافت اطلاعات کاربر بر اساس شناسه """
        query = "SELECT id, username, email, role_id FROM users WHERE id = %s"
        return self.db_service.fetch_one(query, (user_id,))

    @BaseController.exception_handler
    def update_user_info(self, user_id, username, email):
        """ بروزرسانی اطلاعات کاربر (بدون تغییر رمز) """
        query = "UPDATE users SET username = %s, email = %s WHERE id = %s"
        params = (username, email, user_id)
        success = self.db_service.execute_query(query, params)
        return "✅ اطلاعات کاربر بروزرسانی شد." if success else "❌ خطا در بروزرسانی اطلاعات."

    @BaseController.exception_handler
    def change_password(self, user_id, old_password, new_password):
        """ تغییر رمز عبور کاربر با بررسی رمز قبلی """
        query = "SELECT password FROM users WHERE id = %s"
        user = self.db_service.fetch_one(query, (user_id,))

        if user and bcrypt.checkpw(old_password.encode(), user["password"].encode()):
            new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            update_query = "UPDATE users SET password = %s WHERE id = %s"
            success = self.db_service.execute_query(update_query, (new_hashed_password, user_id))
            return "✅ رمز عبور با موفقیت تغییر کرد." if success else "❌ خطا در تغییر رمز عبور."
        return "❌ رمز عبور فعلی اشتباه است!"

    @BaseController.exception_handler
    def delete_user(self, user_id):
        """ حذف حساب کاربری """
        query = "DELETE FROM users WHERE id = %s"
        success = self.db_service.execute_query(query, (user_id,))
        return "✅ حساب کاربری حذف شد." if success else "❌ خطا در حذف حساب کاربری."
