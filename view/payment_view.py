import tkinter as tk
from tkinter import ttk, messagebox
from controller.payment_controller import PaymentController

class PaymentView:
    def __init__(self, root, db_service, user_id, reservation_id, amount, movie_name, refresh_callback):
        self.root = root
        self.db_service = db_service
        self.user_id = user_id
        self.reservation_id = reservation_id
        self.amount = amount
        self.movie_name = movie_name
        self.refresh_callback = refresh_callback

        self.payment_controller = PaymentController(self.db_service)

        self.root.title("پرداخت بلیت")
        self.root.geometry("400x300")

        tk.Label(root, text="پرداخت بلیت", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(root, text=f"فیلم: {self.movie_name}").pack()
        tk.Label(root, text=f"شماره رزرو: {self.reservation_id}").pack()
        tk.Label(root, text=f"مبلغ: {self.amount} تومان").pack()

        tk.Label(root, text="روش پرداخت:").pack(pady=5)
        self.payment_method = ttk.Combobox(root, values=["پرداخت آنلاین", "فیش بانکی", "کارت به کارت"])
        self.payment_method.pack(pady=5)
        self.payment_method.current(0)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="پرداخت", command=self.process_payment, width=12, bg="green", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="بازگشت", command=self.root.destroy, width=12, bg="red", fg="white").grid(row=0, column=1, padx=5)

    def process_payment(self):
        method = self.payment_method.get()

        success, message = self.payment_controller.process_payment(self.user_id, self.reservation_id)

        if success:
            messagebox.showinfo("موفقیت", f"{message} ✅\nروش پرداخت: {method}")
            self.root.destroy()
            self.refresh_callback()
        else:
            messagebox.showerror("خطا", message)