import tkinter as tk
from tkinter import ttk, messagebox
from controller.movie_controller import MovieController
from controller.showtime_controller import ShowtimeController
from controller.ticket_booking_controller import TicketBookingController
from view.ticket_booking_view import TicketBookingView


class MovieSelectionView:
    def __init__(self, root, movie_controller: MovieController, showtime_controller: ShowtimeController,
                 booking_controller: TicketBookingController, hall_controller, user_id):
        self.root = root
        self.movie_controller = movie_controller
        self.showtime_controller = showtime_controller
        self.booking_controller = booking_controller
        self.hall_controller = hall_controller
        self.user_id = user_id
        self.selected_movie_id = None

        self.root.title("انتخاب فیلم")
        self.root.geometry("900x500")

        tk.Label(root, text="انتخاب فیلم و سانس", font=("Arial", 14, "bold")).pack(pady=10)

        self.create_movie_table()
        self.load_movies()

    def create_movie_table(self):
        columns = ("id", "name", "genre", "duration")
        self.movie_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)

        headers = ["شناسه", "نام فیلم", "ژانر", "مدت زمان"]
        for col, header in zip(columns, headers):
            self.movie_tree.heading(col, text=header)
            self.movie_tree.column(col, width=150, anchor="center")

        self.movie_tree.pack(pady=10)

        self.selection_frame = tk.Frame(self.root)
        self.selection_frame.pack(pady=10)

        tk.Label(self.selection_frame, text="سانس‌ها:").grid(row=0, column=0, padx=5)
        self.session_combobox = ttk.Combobox(self.selection_frame, state="readonly")
        self.session_combobox.grid(row=0, column=1, padx=5)

        self.reserve_button = tk.Button(self.selection_frame, text="انتقال به رزرو", command=self.go_to_booking)
        self.reserve_button.grid(row=0, column=2, padx=5)

    def load_movies(self):
        self.movie_tree.delete(*self.movie_tree.get_children())
        movies = self.movie_controller.get_all_movies()

        for movie in movies:
            showtimes = self.showtime_controller.get_showtimes_by_movie(movie['id'])
            if showtimes:
                self.movie_tree.insert("", "end", values=(
                    movie['id'], movie['name'], movie['genre'], movie['duration']
                ))

        self.movie_tree.bind("<ButtonRelease-1>", self.on_movie_select)

    def on_movie_select(self, event):
        selected_item = self.movie_tree.selection()
        if not selected_item:
            return

        self.selected_movie_id = int(self.movie_tree.item(selected_item, "values")[0])
        showtimes = self.showtime_controller.get_showtimes_by_movie(self.selected_movie_id)

        if not showtimes:
            messagebox.showinfo("اطلاع", "سانسی برای این فیلم موجود نیست.")
            return

        self.session_combobox['values'] = [f"{st['start_date']} - {str(st['start_time'])}" for st in showtimes]
        self.session_combobox.set("")

    def go_to_booking(self):
        selected_showtime = self.get_selected_showtime()
        print(f"📌 مقدار selected_showtime: {selected_showtime}")
        if not selected_showtime:
            messagebox.showerror("خطا", "لطفاً یک سانس را انتخاب کنید.")
            return

        showtime_id = selected_showtime.get('id')
        print(f"📌 مقدار showtime_id: {showtime_id}")
        if not showtime_id:
            messagebox.showerror("خطا", "شناسه سانس نامعتبر است.")
            return

        print("✅ حالا باید پنجره‌ی جدید باز بشه!")

        booking_window = tk.Toplevel(self.root)

        print("✅ پنجره‌ی جدید ایجاد شد!")

        try:
            TicketBookingView(booking_window, self.booking_controller, self.showtime_controller, self.hall_controller,
                  self.user_id, showtime_id)

            print("✅ کلاس TicketBookingView ساخته شد!")
        except TypeError as e:
            messagebox.showerror("خطای برنامه", f"خطا در باز کردن صفحه رزرو: {e}")
            print(f"❌ خطا در ایجاد کلاس TicketBookingView: {e}")

    def get_selected_showtime(self):
        selected_index = self.session_combobox.current()

        if selected_index == -1:
            messagebox.showwarning("هشدار", "لطفاً یک سانس را انتخاب کنید.")
            return None

        if not self.selected_movie_id:
            messagebox.showwarning("هشدار", "لطفاً یک فیلم را انتخاب کنید.")
            return None

        showtimes = self.showtime_controller.get_showtimes_by_movie(self.selected_movie_id)

        if selected_index >= len(showtimes):
            messagebox.showerror("خطا", "سانس انتخاب شده معتبر نیست.")
            return None

        return showtimes[selected_index]

    def close_window(self):
        self.root.destroy()
