import tkinter as tk
from tkinter import ttk, messagebox
from controller.reservation_controller import ReservationController


class ViewReservationsView:
    def __init__(self, root, db_service, user_id):
        self.root = root
        self.user_id = user_id
        self.reservation_controller = ReservationController(db_service)

        self.root.title("مشاهده رزروها")
        self.root.geometry("800x500")

        tk.Label(root, text="لیست رزروهای من", font=("Arial", 14, "bold")).pack(pady=10)

        columns = ("id", "movie_name", "datetime", "ticket_count", "status")
        self.reservation_tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

        column_labels = {
            "id": "شناسه",
            "movie_name": "نام فیلم",
            "datetime": "زمان نمایش",
            "ticket_count": "تعداد بلیت",
            "status": "وضعیت"
        }
        column_widths = {"id": 80, "movie_name": 200, "datetime": 150, "ticket_count": 100, "status": 120}

        for col in columns:
            self.reservation_tree.heading(col, text=column_labels[col])
            self.reservation_tree.column(col, width=column_widths[col], anchor="center")

        self.reservation_tree.pack(pady=10)
        self.load_reservations()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="حذف رزرو", command=self.delete_reservation, width=12).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="بازگشت", command=self.close_window, width=12).grid(row=0, column=1, padx=5, pady=5)

    def load_reservations(self):
        self.reservation_tree.delete(*self.reservation_tree.get_children())
        reservations = self.reservation_controller.get_user_reservations(self.user_id)

        for res in reservations:
            self.reservation_tree.insert("", "end", values=(
                res["id"], res["movie_name"], res["datetime"],
                res["ticket_count"], res["status"]
            ))

    def delete_reservation(self):
        selected_item = self.reservation_tree.selection()
        if not selected_item:
            messagebox.showwarning("خطا", "رزروی را انتخاب کنید.")
            return

        reservation_id = int(self.reservation_tree.item(selected_item, "values")[0])
        status = self.reservation_tree.item(selected_item, "values")[4]

        if status.lower() != "pending":
            messagebox.showerror("خطا", "فقط رزروهای در انتظار پرداخت قابل حذف هستند.")
            return

        confirm = messagebox.askyesno("تأیید حذف", "آیا مطمئن هستید که می‌خواهید این رزرو را حذف کنید؟")
        if not confirm:
            return

        success, message = self.reservation_controller.delete_reservation(reservation_id)
        if success:
            messagebox.showinfo("موفقیت", message)
            self.load_reservations()
        else:
            messagebox.showerror("خطا", message)

    def close_window(self):
        self.root.destroy()
