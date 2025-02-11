import tkinter as tk
from tkinter import ttk, messagebox
from controller.reservation_controller import ReservationController
from view.payment_view import PaymentView

class ReservationView:
    def __init__(self, root, db_service, user_id):
        self.root = root
        self.db_service = db_service
        self.user_id = user_id
        self.root.title("رزروهای من")
        self.root.geometry("1400x700")

        self.reservation_controller = ReservationController(self.db_service)

        tk.Label(root, text="رزروهای من", font=("Arial", 14, "bold")).pack(pady=10)

        self.reservation_table = ttk.Treeview(
            root,
            columns=("id", "movie", "showtime", "seats", "price", "status"),
            show="headings"
        )
        self.reservation_table.heading("id", text="شناسه رزرو")
        self.reservation_table.heading("movie", text="فیلم")
        self.reservation_table.heading("showtime", text="سانس")
        self.reservation_table.heading("seats", text="صندلی‌ها")
        self.reservation_table.heading("price", text="مبلغ کل")
        self.reservation_table.heading("status", text="وضعیت پرداخت")
        self.reservation_table.pack(pady=10, fill=tk.BOTH, expand=True)

        self.load_reservations()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.pay_button = tk.Button(btn_frame, text="پرداخت", command=self.open_payment_window)
        self.pay_button.grid(row=0, column=0, padx=5)

        self.cancel_button = tk.Button(btn_frame, text="لغو رزرو", command=self.cancel_reservation)
        self.cancel_button.grid(row=0, column=1, padx=5)

        self.back_button = tk.Button(btn_frame, text="بازگشت", command=self.root.destroy)
        self.back_button.grid(row=0, column=2, padx=5)

    def load_reservations(self):
        reservations = self.reservation_controller.get_user_reservations(self.user_id)
        self.reservation_table.delete(*self.reservation_table.get_children())

        for res in reservations:
            status = "پرداخت شده" if res["payment_status"] == "completed" else "در انتظار پرداخت"
            self.reservation_table.insert("", "end", values=(
                res["id"], res["movie_name"], res["start_time"],
                res["ticket_count"], res["total_price"], status
            ))

    def cancel_reservation(self):
        selected_item = self.reservation_table.selection()
        if not selected_item:
            messagebox.showwarning("خطا", "لطفاً یک رزرو را انتخاب کنید.")
            return

        res_id = self.reservation_table.item(selected_item, "values")[0]
        success, message = self.reservation_controller.delete_reservation(res_id)

        if success:
            messagebox.showinfo("موفقیت", message)
            self.load_reservations()
        else:
            messagebox.showerror("خطا", message)

    def open_payment_window(self):
        selected_item = self.reservation_table.selection()
        if not selected_item:
            messagebox.showwarning("خطا", "لطفاً یک رزرو را انتخاب کنید.")
            return

        res_id, movie_name, showtime, seats, price, status = self.reservation_table.item(selected_item, "values")

        if status == "پرداخت شده":
            messagebox.showinfo("اطلاع", "این رزرو قبلاً پرداخت شده است.")
            return

        payment_window = tk.Toplevel(self.root)
        PaymentView(payment_window, self.db_service, self.user_id, res_id, price, movie_name, self.load_reservations)
