from tkinter import ttk

class PaymentsListView:
    def __init__(self, root, payment_controller, user_id):
        self.root = root
        self.payment_controller = payment_controller
        self.user_id = user_id

        self.root.title("لیست پرداخت‌ها")
        self.root.geometry("600x400")

        self.create_widgets()
        self.load_payments()

    def create_widgets(self):
        columns = ("id", "reservation_id", "amount", "status", "date")

        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("id", text="شناسه پرداخت")
        self.tree.heading("reservation_id", text="شناسه رزرو")
        self.tree.heading("amount", text="مبلغ")
        self.tree.heading("status", text="وضعیت پرداخت")
        self.tree.heading("date", text="تاریخ پرداخت")

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("reservation_id", width=100, anchor="center")
        self.tree.column("amount", width=100, anchor="center")
        self.tree.column("status", width=120, anchor="center")
        self.tree.column("date", width=150, anchor="center")

        self.tree.pack(pady=20, fill="both", expand=True)

    def load_payments(self):
        payments = self.payment_controller.get_user_payments(self.user_id)
        for payment in payments:
            self.tree.insert("", "end", values=(
                payment["id"], payment["reservation_id"],
                payment["amount"], payment["status"], payment["date"]
            ))
