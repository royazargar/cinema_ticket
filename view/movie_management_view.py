import tkinter as tk
from tkinter import ttk, messagebox
from controller.movie_controller import MovieController


class MovieManagementView:
    def __init__(self, root, movie_controller: MovieController):
        self.root = root
        self.movie_controller = movie_controller
        self.root.title("مدیریت فیلم‌ها")
        self.root.geometry("800x600")

        tk.Label(root, text="مدیریت فیلم‌ها", font=("Arial", 14, "bold")).pack(pady=10)

        columns = ("id", "name", "genre", "duration", "description")
        self.movie_tree = ttk.Treeview(root, columns=columns, show="headings", height=8)

        self.movie_tree.heading("id", text="شناسه")
        self.movie_tree.heading("name", text="نام فیلم")
        self.movie_tree.heading("genre", text="ژانر")
        self.movie_tree.heading("duration", text="مدت زمان")
        self.movie_tree.heading("description", text="توضیحات")

        self.movie_tree.column("id", width=50, anchor="center")
        self.movie_tree.column("name", width=150, anchor="center")
        self.movie_tree.column("genre", width=100, anchor="center")
        self.movie_tree.column("duration", width=100, anchor="center")
        self.movie_tree.column("description", width=250, anchor="center")

        self.movie_tree.pack(pady=10)
        self.movie_tree.bind("<ButtonRelease-1>", self.on_row_selected)
        self.load_movies()

        form_frame = tk.Frame(root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="نام فیلم:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(form_frame)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="ژانر:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_genre = tk.Entry(form_frame)
        self.entry_genre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="مدت زمان (دقیقه):").grid(row=2, column=0, padx=5, pady=5)
        self.entry_duration = tk.Entry(form_frame)
        self.entry_duration.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="توضیحات:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_description = tk.Entry(form_frame)
        self.entry_description.grid(row=3, column=1, padx=5, pady=5)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="افزودن فیلم", command=self.add_movie).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="ویرایش فیلم", command=self.update_movie).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="حذف فیلم", command=self.delete_movie).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="بازگشت", command=self.root.destroy).grid(row=0, column=3, padx=5, pady=5)

        self.selected_movie_id = None

    def load_movies(self):
        self.movie_tree.delete(*self.movie_tree.get_children())
        movies = self.movie_controller.get_all_movies()
        for movie in movies:
            self.movie_tree.insert("", "end", values=(
                movie["id"], movie["name"], movie["genre"], movie["duration"], movie["description"]
            ))

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)
        self.selected_movie_id = None

    def on_row_selected(self, event):
        selected_item = self.movie_tree.selection()
        if not selected_item:
            return

        values = self.movie_tree.item(selected_item, "values")
        self.selected_movie_id = int(values[0])
        print(f"Selected Movie ID: {self.selected_movie_id}")

        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, values[1])

        self.entry_genre.delete(0, tk.END)
        self.entry_genre.insert(0, values[2])

        self.entry_duration.delete(0, tk.END)
        self.entry_duration.insert(0, values[3])

        self.entry_description.delete(0, tk.END)
        self.entry_description.insert(0, values[4])

    def add_movie(self):
        name = self.entry_name.get()
        genre = self.entry_genre.get()
        duration = self.entry_duration.get()
        description = self.entry_description.get()

        if not name or not genre or not duration.isdigit():
            messagebox.showerror("خطا", "لطفاً اطلاعات را به درستی وارد کنید.")
            return

        self.movie_controller.add_movie(name, genre, int(duration), description)
        messagebox.showinfo("موفقیت", "فیلم جدید اضافه شد.")
        self.load_movies()
        self.clear_form()

    def update_movie(self):
        if self.selected_movie_id is None:
            messagebox.showwarning("خطا", "ابتدا یک فیلم را انتخاب کنید.")
            return

        name = self.entry_name.get()
        genre = self.entry_genre.get()
        duration = self.entry_duration.get()
        description = self.entry_description.get()

        if not name or not genre or not duration.isdigit():
            messagebox.showerror("خطا", "لطفاً اطلاعات را به درستی وارد کنید.")
            return

        try:
            self.movie_controller.update_movie(self.selected_movie_id, name, genre, int(duration), description)
            messagebox.showinfo("موفقیت", "فیلم بروزرسانی شد.")
            self.load_movies()
            self.clear_form()
        except Exception as e:
            print(f"Error in update_movie: {e}")
            messagebox.showerror("خطا", f"مشکلی پیش آمد: {str(e)}")

    def delete_movie(self):
        if self.selected_movie_id is None:
            messagebox.showwarning("خطا", "فیلمی را انتخاب کنید.")
            return

        self.movie_controller.delete_movie(self.selected_movie_id)
        messagebox.showinfo("موفقیت", "فیلم حذف شد.")
        self.load_movies()
        self.clear_form()

    def close_window(self):
        self.root.destroy()
