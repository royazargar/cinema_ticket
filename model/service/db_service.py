import mysql.connector
from mysql.connector import Error

class DBService:
    def __init__(self, host="localhost", user="root", password="root123", database="cinema_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connect()

    def connect(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                if self.connection.is_connected():
                    print("✅ اتصال به دیتابیس برقرار شد")
        except Error as e:
            self.connection = None
            print(f"❌ خطا در اتصال به دیتابیس: {e}")

    def execute_query(self, query, params=None):
        self.connect()
        if self.connection is None:
            print("❌ اتصال به دیتابیس وجود ندارد!")
            return False

        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            print(f"❌ خطا در اجرای کوئری: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def fetch_all(self, query, params=None):
        self.connect()
        if self.connection is None:
            print("❌ اتصال به دیتابیس وجود ندارد!")
            return []

        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            print(f"📝 اجرای کوئری: {query} | پارامترها: {params}")
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            print(f"📌 داده‌های دریافت‌شده: {result}")
            return result
        except Error as e:
            print(f"❌ خطا در دریافت داده‌ها: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def fetch_one(self, query, params=None):
        self.connect()
        if self.connection is None:
            print("❌ اتصال به دیتابیس وجود ندارد!")
            return None

        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except Error as e:
            print(f"❌ خطا در دریافت داده: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 اتصال به دیتابیس بسته شد")
            self.connection = None

    def __del__(self):
        self.close_connection()
