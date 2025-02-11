import tkinter as tk
from controller.hall_controller import HallController
from controller.movie_controller import MovieController
from controller.showtime_controller import ShowtimeController
from controller.ticket_booking_controller import TicketBookingController
from controller.payment_list_controller import PaymentListController
from view.movie_selection_view import MovieSelectionView
from view.reservation_view import ReservationView
from view.login_view import LoginView
from view.payment_list_view import PaymentsListView


class CustomerDashboard:
    def __init__(self, root, db_service, user_id):
        self.root = root
        self.db_service = db_service
        self.user_id = user_id
        self.root.title("داشبورد مشتری")
        self.root.geometry("400x300")

        tk.Label(root, text="پنل مشتری", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(root, text="رزرو بلیت", command=self.select_movie, width=20).pack(pady=5)
        tk.Button(root, text="مشاهده رزروها", command=self.view_reservations, width=20).pack(pady=5)
        tk.Button(root, text="مشاهده پرداخت‌ها", command=self.view_payments, width=20).pack(pady=5)
        tk.Button(root, text="خروج", command=self.logout, width=20).pack(pady=5)

    def view_payments(self):
        payments_window = tk.Toplevel(self.root)
        payment_list_controller = PaymentListController(self.db_service)
        PaymentsListView(payments_window, payment_list_controller, self.user_id)

    def select_movie(self):
        movie_window = tk.Toplevel(self.root)
        movie_controller = MovieController(self.db_service)
        showtime_controller = ShowtimeController(self.db_service)
        booking_controller = TicketBookingController(self.db_service)
        hall_controller = HallController(self.db_service)

        MovieSelectionView(movie_window, movie_controller, showtime_controller, booking_controller, hall_controller,
                           self.user_id)

    def view_reservations(self):
        reservation_window = tk.Toplevel(self.root)
        ReservationView(reservation_window, self.db_service, self.user_id)

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        LoginView(root, self.db_service, main_app=None)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    db_service = None
    user_id = 1
    CustomerDashboard(root, db_service, user_id)
    root.mainloop()
