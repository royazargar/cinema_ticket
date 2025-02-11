import tkinter as tk
from tkinter import messagebox

class LoginView:
    def __init__(self, root, user_controller, main_app=None):
        self.root = root
        self.root.title("ورود")
        self.root.geometry("300x250")
        self.user_controller = user_controller
        self.main_app = main_app

        tk.Label(root, text="نام کاربری:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="رمز عبور:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(root, text="ورود", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(root, text="ثبت نام", command=self.show_register)
        self.register_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("خطا", "لطفاً نام کاربری و رمز عبور را وارد کنید.")
            return

        user = self.user_controller.login_user(username, password)
        print("User from login_user:", user)

        if user:
            messagebox.showinfo("خوش آمدید", f"{username} عزیز، خوش آمدید!")
            if self.main_app:
                self.main_app.show_dashboard(user)
            else:
                print("⚠️ خطا: main_app مقداردهی نشده است!")
        else:
            messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است.")

    def show_register(self):
        from view.register_view import RegisterView

        self.root.withdraw()
        RegisterView(self.root, self.user_controller, self.main_app, self.root)
