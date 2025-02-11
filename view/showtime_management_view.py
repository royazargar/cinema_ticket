import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controller.showtime_controller import ShowtimeController
from controller.movie_controller import MovieController
from controller.hall_controller import HallController

class ShowtimeManagementView:
    def __init__(self, root, showtime_controller: ShowtimeController, movie_controller: MovieController, hall_controller: HallController):
        self.root = root
        self.showtime_controller = showtime_controller
        self.movie_controller = movie_controller
        self.hall_controller = hall_controller
        self.root.title("مدیریت سانس‌های نمایش")
        self.root.geometry("900x600")

        tk.Label(root, text="مدیریت سانس‌های نمایش", font=("Arial", 14, "bold")).pack(pady=10)

        columns = ("id", "movie", "hall", "start_date", "end_date", "start_time", "ticket_price")
        self.showtime_tree = ttk.Treeview(root, columns=columns, show="headings", height=8)

        column_names = {
            "id": "شناسه",
            "movie": "فیلم",
            "hall": "سالن",
            "start_date": "تاریخ شروع",
            "end_date": "تاریخ پایان",
            "start_time": "ساعت شروع",
            "ticket_price": "قیمت بلیت"
        }

        for col, name in column_names.items():
            self.showtime_tree.heading(col, text=name)
            self.showtime_tree.column(col, width=120, anchor="center")

        self.showtime_tree.pack(pady=10)
        self.showtime_tree.bind("<ButtonRelease-1>", self.on_row_selected)

        form_frame = tk.Frame(root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="فیلم:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_movie = ttk.Combobox(form_frame, state="readonly")
        self.combo_movie.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="سالن:").grid(row=1, column=0, padx=5, pady=5)
        self.combo_hall = ttk.Combobox(form_frame, state="readonly")
        self.combo_hall.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="تاریخ شروع:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_start_date = DateEntry(form_frame, date_pattern='yyyy-mm-dd')
        self.entry_start_date.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="تاریخ پایان:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_end_date = DateEntry(form_frame, date_pattern='yyyy-mm-dd')
        self.entry_end_date.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="ساعت شروع:").grid(row=4, column=0, padx=5, pady=5)
        self.entry_start_time = tk.Entry(form_frame)
        self.entry_start_time.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="قیمت بلیت:").grid(row=5, column=0, padx=5, pady=5)
        self.entry_ticket_price = tk.Entry(form_frame)
        self.entry_ticket_price.grid(row=5, column=1, padx=5, pady=5)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="افزودن سانس", command=self.add_showtime).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="ویرایش سانس", command=self.update_showtime).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="حذف سانس", command=self.delete_showtime).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="بازگشت", command=self.root.destroy).grid(row=0, column=3, padx=5, pady=5)

        self.selected_showtime_id = None
        self.load_movies()
        self.load_halls()
        self.load_showtimes()

    def load_movies(self):
        movies = self.movie_controller.get_all_movies()
        movie_list = [f"{movie['id']} - {movie['name']}" for movie in movies]
        self.combo_movie["values"] = movie_list

    def load_halls(self):
        halls = self.hall_controller.get_all_halls()
        hall_list = [f"{hall['id']} - {hall['name']}" for hall in halls]
        self.combo_hall["values"] = hall_list

    def load_showtimes(self):
        self.showtime_tree.delete(*self.showtime_tree.get_children())
        showtimes = self.showtime_controller.get_all_showtimes()
        for showtime in showtimes:
            movie_name = self.movie_controller.get_movie_by_id(showtime['movie_id'])['name']
            hall_name = self.hall_controller.get_hall_by_id(showtime['hall_id'])['name']
            self.showtime_tree.insert("", "end", values=(showtime['id'], movie_name, hall_name, showtime['start_date'], showtime['end_date'], showtime['start_time'], showtime['ticket_price']))

    def on_row_selected(self, event):
        selected_item = self.showtime_tree.selection()
        if not selected_item:
            return
        row = self.showtime_tree.item(selected_item)['values']
        self.selected_showtime_id = row[0]
        self.combo_movie.set(row[1])
        self.combo_hall.set(row[2])
        self.entry_start_date.set_date(row[3])
        self.entry_end_date.set_date(row[4])
        self.entry_start_time.delete(0, tk.END)
        self.entry_start_time.insert(0, row[5])
        self.entry_ticket_price.delete(0, tk.END)
        self.entry_ticket_price.insert(0, row[6])

    def clear_form(self):
        self.combo_movie.set("")
        self.combo_hall.set("")
        self.entry_start_date.set_date(date.today())
        self.entry_end_date.set_date(date.today())
        self.entry_start_time.delete(0, tk.END)
        self.entry_ticket_price.delete(0, tk.END)
        self.selected_showtime_id = None

    def add_showtime(self):
        try:
            movie = self.combo_movie.get()
            hall = self.combo_hall.get()
            start_time = self.entry_start_time.get()
            start_date = self.entry_start_date.get()
            end_date = self.entry_end_date.get()
            seat_price = self.entry_ticket_price.get()

            if not movie or not hall or not start_time or not start_date or not end_date or not seat_price:
                messagebox.showerror("خطا", "تمام فیلدها را پر کنید.")
                return

            movie_id = int(movie.split(" - ")[0])
            hall_id = int(hall.split(" - ")[0])

            movie_data = self.movie_controller.get_movie_by_id(movie_id)
            if not movie_data:
                messagebox.showerror("خطا", "فیلم انتخاب‌شده نامعتبر است.")
                return
            movie_duration = movie_data["duration"]

            hall_data = self.hall_controller.get_hall_by_id(hall_id)
            if not hall_data:
                messagebox.showerror("خطا", "سالن انتخاب‌شده نامعتبر است.")
                return
            available_seats = hall_data["seat_count"]

            self.showtime_controller.add_showtime(
                movie_id, hall_id, start_time, start_date, end_date, movie_duration, available_seats, int(seat_price)
            )

            messagebox.showinfo("موفقیت", "سانس جدید اضافه شد.")
            self.load_showtimes()
            self.clear_form()

        except Exception as e:
            messagebox.showerror("خطا", f"مشکلی پیش آمد: {e}")

    def update_showtime(self):
        if not self.selected_showtime_id:
            messagebox.showerror("خطا", "ابتدا یک سانس را انتخاب کنید.")
            return

        movie = self.combo_movie.get()
        hall = self.combo_hall.get()
        start_time = self.entry_start_time.get()
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()
        ticket_price = self.entry_ticket_price.get()

        if not movie or not hall or not start_time or not start_date or not end_date or not ticket_price.isdigit():
            messagebox.showerror("خطا", "تمام فیلدها را به‌درستی پر کنید.")
            return

        movie_id = int(movie.split(" - ")[0])
        hall_id = int(hall.split(" - ")[0])
        self.showtime_controller.update_showtime(self.selected_showtime_id, movie_id, hall_id, start_time, start_date, end_date, int(ticket_price))
        messagebox.showinfo("موفقیت", "سانس بروزرسانی شد.")
        self.load_showtimes()
        self.clear_form()

    def delete_showtime(self):
        if not self.selected_showtime_id:
            messagebox.showerror("خطا", "ابتدا یک سانس را انتخاب کنید.")
            return

        confirm = messagebox.askyesno("حذف سانس", "آیا از حذف این سانس مطمئن هستید؟")
        if confirm:
            self.showtime_controller.delete_showtime(self.selected_showtime_id)
            messagebox.showinfo("موفقیت", "سانس حذف شد.")
            self.load_showtimes()
            self.clear_form()
