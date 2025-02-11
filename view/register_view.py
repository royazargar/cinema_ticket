import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
import re

class RegisterView:
    def __init__(self, parent, user_controller, main_app, login_window):
        self.window = tk.Toplevel(parent)
        self.window.title("ثبت نام")
        self.window.geometry("300x350")
        self.user_controller = user_controller
        self.main_app = main_app
        self.login_window = login_window

        tk.Label(self.window, text="نام کاربری:").pack(pady=5)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack(pady=5)

        tk.Label(self.window, text="رمز عبور:").pack(pady=5)
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack(pady=5)

        tk.Label(self.window, text="ایمیل:").pack(pady=5)
        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack(pady=5)

        tk.Label(self.window, text="نقش:").pack(pady=5)
        self.role_combobox = Combobox(self.window, values=["ادمین", "مشتری"], state="readonly")
        self.role_combobox.pack(pady=5)
        self.role_combobox.current(1)

        self.register_button = tk.Button(self.window, text="ثبت نام", command=self.register)
        self.register_button.pack(pady=10)

        self.back_button = tk.Button(self.window, text="بازگشت", command=self.show_login)
        self.back_button.pack(pady=5)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        email = self.email_entry.get().strip()
        role = self.role_combobox.get().strip()

        if not username or not password or not email or not role:
            messagebox.showerror("خطا", "لطفاً تمام فیلدها را پر کنید.")
            return

        if len(password) < 6:
            messagebox.showerror("خطا", "رمز عبور باید حداقل ۶ کاراکتر باشد.")
            return

        if not self.validate_email(email):
            messagebox.showerror("خطا", "ایمیل وارد شده معتبر نیست.")
            return

        role_id = 1 if role == "ادمین" else 2

        try:
            result = self.user_controller.register_user(username, password, email, role_id)
            messagebox.showinfo("نتیجه", result)
            self.show_login()
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در ثبت‌نام: {e}")

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def show_login(self):
        self.window.destroy()
        self.login_window.deiconify()
