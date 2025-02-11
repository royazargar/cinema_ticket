import tkinter as tk
from tkinter import messagebox
import math

from model.service.db_service import DBService
from view.reservation_view import ReservationView

db_service = DBService()

class TicketBookingView:
    def __init__(self, root, booking_controller, showtime_controller, hall_controller, user_id, showtime_id):
        if not showtime_id:
            messagebox.showerror("خطا", "شناسه سانس معتبر نیست!")
            root.destroy()
            return

        self.root = root
        self.booking_controller = booking_controller
        self.showtime_controller = showtime_controller
        self.hall_controller = hall_controller
        self.db_service = db_service
        self.user_id = user_id
        self.showtime_id = showtime_id
        self.selected_seats = set()

        self.root.title("رزرو بلیت")
        self.root.geometry("1400x1000")

        tk.Label(root, text="رزرو بلیت", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(root, text=f"شناسه نمایش: {self.showtime_id}", font=("Arial", 12)).pack(pady=5)

        hall_info = self.booking_controller.get_hall_info_by_showtime(self.showtime_id)
        if not hall_info:
            messagebox.showerror("خطا", "اطلاعات سالن یافت نشد!")
            self.root.destroy()
            return

        self.hall_id, self.total_seats = hall_info

        self.ticket_price = self.showtime_controller.get_ticket_price(self.showtime_id) or 0

        reserved_seats = self.showtime_controller.get_reserved_seats(self.showtime_id) or []
        self.seat_status = set(map(int, reserved_seats))

        self.create_seat_selection()
        self.create_booking_summary()

    def create_seat_selection(self):
        seat_frame = tk.Frame(self.root)
        seat_frame.pack(pady=10)

        rows = math.ceil(self.total_seats / 10)
        self.seat_buttons = {}

        for i in range(rows):
            for j in range(10):
                seat_num = i * 10 + j + 1
                if seat_num > self.total_seats:
                    break
                state = "disabled" if seat_num in self.seat_status else "normal"
                color = "red" if state == "disabled" else "lightgray"

                btn = tk.Button(seat_frame, text=str(seat_num), width=4, height=2,
                                state=state, bg=color,
                                command=lambda s=seat_num: self.toggle_seat(s) if s not in self.seat_status else None)
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.seat_buttons[seat_num] = btn

    def toggle_seat(self, seat_num):
        if seat_num in self.selected_seats:
            self.selected_seats.remove(seat_num)
            self.seat_buttons[seat_num].config(bg="lightgray")
        else:
            self.selected_seats.add(seat_num)
            self.seat_buttons[seat_num].config(bg="green")

        self.update_price()

    def create_booking_summary(self):
        summary_frame = tk.Frame(self.root)
        summary_frame.pack(pady=10)

        tk.Label(summary_frame, text="تعداد صندلی: ").grid(row=0, column=0)
        self.seats_label = tk.Label(summary_frame, text="0")
        self.seats_label.grid(row=0, column=1)

        tk.Label(summary_frame, text="مبلغ کل: ").grid(row=1, column=0)
        self.price_label = tk.Label(summary_frame, text="0 تومان")
        self.price_label.grid(row=1, column=1)

        tk.Button(summary_frame, text="رزرو بلیت", command=self.book_ticket).grid(row=2, columnspan=2, pady=10)

    def update_price(self):
        total_price = self.ticket_price * len(self.selected_seats)
        formatted_price = f"{total_price:,} تومان"
        self.seats_label.config(text=str(len(self.selected_seats)))
        self.price_label.config(text=formatted_price)

    def book_ticket(self):
        if not self.selected_seats:
            messagebox.showwarning("خطا", "لطفا حداقل یک صندلی انتخاب کنید.")
            return

        success, message = self.booking_controller.book_ticket(
            self.user_id, self.showtime_id, list(self.selected_seats), self.ticket_price
        )

        if success:
            messagebox.showinfo("موفقیت", message)
            self.root.destroy()
            self.open_reservations()
        else:
            messagebox.showerror("خطا", message)

    def open_reservations(self):
        if not self.root or not self.root.winfo_exists():
            print("⚠️ خطا: پنجره اصلی دیگر وجود ندارد!")
        else:
            self.root.withdraw()
        print(f"🔍 مقدار db_service در open_reservations: {self.db_service}")
        reservations_root = tk.Toplevel()
        ReservationView(reservations_root, self.db_service, self.user_id)
        reservations_root.protocol("WM_DELETE_WINDOW", lambda: self.on_close(reservations_root))

    def on_close(self, reservations_root):
        reservations_root.destroy()
        self.root.deiconify()
