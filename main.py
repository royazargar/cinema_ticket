import sys
import os
from tkinter import messagebox

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from model.service.db_service import DBService
from controller.user_controller import UserController
from view.admin_dashboard import AdminDashboard
from view.customer_dashboard import CustomerDashboard
from view.login_view import LoginView

class MainApp:
    def __init__(self):
        self.db_service = DBService(host="localhost", user="root", password="root123", database="cinema_db")
        self.user_controller = UserController(self.db_service)
        self.root = tk.Tk()
        self.admin_dashboard = None
        self.customer_dashboard = None
        self.show_login()

    def show_login(self):
        self.clear_window()
        LoginView(self.root, self.user_controller, self)

    def show_dashboard(self, user):
        print("User data in show_dashboard:", user)

        if not user or "role_id" not in user:
            messagebox.showerror("خطا", "خطای ورود: اطلاعات کاربر نامعتبر است.")
            self.show_login()
            return

        self.clear_window()

        if user["role_id"] == 1:  # فرض: 1 = ادمین، 2 = مشتری
            self.admin_dashboard = AdminDashboard(self.root, self.db_service)
        else:
            user_id = user["id"]
            print("Opening customer dashboard for user_id:", user_id)
            self.customer_dashboard = CustomerDashboard(self.root, self.db_service, user_id)

    def clear_window(self):
        if self.root is not None and self.root.winfo_exists():
            for widget in self.root.winfo_children():
                widget.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.root.mainloop()
