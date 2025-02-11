import tkinter as tk
from controller.hall_controller import HallController
from controller.movie_controller import MovieController
from controller.showtime_controller import ShowtimeController
from model.repository.hall_repository import HallRepository
from view.hall_management_view import HallManagementView
from view.movie_management_view import MovieManagementView
from view.showtime_management_view import ShowtimeManagementView


class AdminDashboard:
    def __init__(self, root, db_service):
        self.root = root
        self.db_service = db_service

        self.movie_controller = MovieController(self.db_service)
        self.hall_repository = HallRepository(self.db_service)
        self.showtime_controller = ShowtimeController(self.db_service)
        self.setup_ui()

    def setup_ui(self):
        self.root.title("پنل مدیریت")
        self.root.geometry("400x400")

        tk.Label(self.root, text="مدیریت سینما", font=("Arial", 14, "bold")).pack(pady=10)

        self.hall_button = tk.Button(self.root, text="مدیریت سالن‌ها", command=self.open_hall_management, width=20)
        self.hall_button.pack(pady=5)

        self.movie_button = tk.Button(self.root, text="مدیریت فیلم‌ها", command=self.open_movie_management, width=20)
        self.movie_button.pack(pady=5)

        self.showtime_button = tk.Button(self.root, text="مدیریت سانس‌ها", command=self.open_showtime_management,
                                         width=20)
        self.showtime_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="خروج", command=self.root.quit, width=20)
        self.exit_button.pack(pady=5)

    def open_hall_management(self):
        if hasattr(self, "hall_window") and self.hall_window.winfo_exists():
            self.hall_window.lift()
            return

        self.hall_window = tk.Toplevel(self.root)
        hall_repository = HallRepository(self.db_service)
        hall_controller = HallController(hall_repository)
        HallManagementView(self.hall_window, hall_controller)

    def open_movie_management(self):
        if hasattr(self, "movie_window") and self.movie_window.winfo_exists():
            self.movie_window.lift()
            return

        self.movie_window = tk.Toplevel(self.root)
        movie_controller = MovieController(self.db_service)
        MovieManagementView(self.movie_window, movie_controller)

    def open_showtime_management(self):
        if hasattr(self, "showtime_window") and self.showtime_window.winfo_exists():
            self.showtime_window.lift()
            return

        self.showtime_window = tk.Toplevel(self.root)
        showtime_controller = ShowtimeController(self.db_service)
        movie_controller = MovieController(self.db_service)
        hall_controller = HallController(self.db_service)
        ShowtimeManagementView(self.showtime_window, showtime_controller, movie_controller, hall_controller)
