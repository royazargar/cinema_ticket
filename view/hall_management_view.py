import tkinter as tk
from tkinter import ttk, messagebox
from controller.hall_controller import HallController


class HallManagementView:
    def __init__(self, root, hall_controller: HallController):
        self.root = root
        self.hall_controller = hall_controller
        self.root.title("مدیریت سالن‌ها")
        self.root.geometry("600x600")

        tk.Label(root, text="مدیریت سالن‌ها", font=("Arial", 14, "bold")).pack(pady=10)

        columns = ("id", "name", "seat_count")
        self.hall_tree = ttk.Treeview(root, columns=columns, show="headings", height=8)

        self.hall_tree.heading("id", text="شناسه")
        self.hall_tree.heading("name", text="نام سالن")
        self.hall_tree.heading("seat_count", text="ظرفیت")

        self.hall_tree.column("id", width=50, anchor="center")
        self.hall_tree.column("name", width=150, anchor="center")
        self.hall_tree.column("seat_count", width=100, anchor="center")

        self.hall_tree.pack(pady=10)
        self.hall_tree.bind("<ButtonRelease-1>", self.on_row_selected)
        self.load_halls()

        form_frame = tk.Frame(root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="نام سالن:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(form_frame)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="ظرفیت:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_capacity = tk.Entry(form_frame)
        self.entry_capacity.grid(row=1, column=1, padx=5, pady=5)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="افزودن سالن", command=self.add_hall).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="ویرایش سالن", command=self.update_hall).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="حذف سالن", command=self.delete_hall).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="بازگشت", command=self.close_window).grid(row=0, column=3, padx=5, pady=5)

        self.selected_hall_id = None

    def load_halls(self):
        self.hall_tree.delete(*self.hall_tree.get_children())
        halls = self.hall_controller.get_all_halls()
        for hall in halls:
            self.hall_tree.insert("", "end",
                                  values=(hall['id'], hall['name'], hall['seat_count']))

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_capacity.delete(0, tk.END)
        self.selected_hall_id = None

    def on_row_selected(self, event):
        selected_item = self.hall_tree.selection()
        if not selected_item:
            return

        values = self.hall_tree.item(selected_item, "values")
        self.selected_hall_id = values[0]
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, values[1])

        self.entry_capacity.delete(0, tk.END)
        self.entry_capacity.insert(0, values[2])

    def add_hall(self):
        name = self.entry_name.get()
        capacity = self.entry_capacity.get()

        if not name or not capacity.isdigit():
            messagebox.showerror("خطا", "لطفاً اطلاعات را به درستی وارد کنید.")
            return

        self.hall_controller.add_hall(name, int(capacity))
        messagebox.showinfo("موفقیت", "سالن جدید اضافه شد.")
        self.load_halls()
        self.clear_form()

    def update_hall(self):
        if not self.selected_hall_id:
            messagebox.showwarning("خطا", "ابتدا یک سالن را انتخاب کنید.")
            return

        name = self.entry_name.get()
        capacity = self.entry_capacity.get()

        if not name or not capacity.isdigit():
            messagebox.showerror("خطا", "لطفاً اطلاعات را به درستی وارد کنید.")
            return

        try:
            self.hall_controller.update_hall(int(self.selected_hall_id), name, int(capacity))
            messagebox.showinfo("موفقیت", "سالن بروزرسانی شد.")
            self.load_halls()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("خطا", f"مشکلی پیش آمد: {str(e)}")

    def delete_hall(self):
        if not self.selected_hall_id:
            messagebox.showwarning("خطا", "ابتدا یک سالن را انتخاب کنید.")
            return

        self.hall_controller.delete_hall(int(self.selected_hall_id))
        messagebox.showinfo("موفقیت", "سالن حذف شد.")
        self.load_halls()
        self.clear_form()

    def close_window(self):
        self.root.destroy()
