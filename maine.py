import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


class PartnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление Партнерами")
        self.root.geometry("1000x700")
        self.root.configure(bg="#FFFFFF")

        self.conn = sqlite3.connect('partners.db')
        self.create_table()
        self.partners = self.load_partners()

        self.create_main_frame()

    def create_table(self):
        """Создание таблицы в базе данных, если она не существует."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS partners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    city TEXT NOT NULL,
                    street TEXT NOT NULL,
                    house TEXT NOT NULL,
                    director TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            ''')

    def load_partners(self):
        """Загрузка данных о партнерах из базы данных."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM partners")
        partners = []
        for row in cursor.fetchall():
            partners.append({
                'id': row[0],
                'name': row[1],
                'type': row[2],
                'rating': row[3],
                'address': {
                    'city': row[4],
                    'street': row[5],
                    'house': row[6]
                },
                'director': row[7],
                'phone': row[8],
                'email': row[9]
            })
        return partners

    def create_main_frame(self):
        """Создание главного окна со списком партнеров."""
        self.main_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.main_frame, text="Список Партнеров", bg="#FFFFFF", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Добавление новых столбцов для отображения полной информации о партнерах
        self.partner_list = ttk.Treeview(self.main_frame, columns=("Name", "Type", "Rating", "City", "Street", "House", "Director", "Phone", "Email"), show="headings")
        self.partner_list.heading("Name", text="Наименование")
        self.partner_list.heading("Type", text="Тип")
        self.partner_list.heading("Rating", text="Рейтинг")
        self.partner_list.heading("City", text="Город")
        self.partner_list.heading("Street", text="Улица")
        self.partner_list.heading("House", text="Дом")
        self.partner_list.heading("Director", text="Директор")
        self.partner_list.heading("Phone", text="Телефон")
        self.partner_list.heading("Email", text="Email")
        self.partner_list.pack(fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self.main_frame, text="Добавить Партнера", command=self.open_add_edit_form, bg="#67BA80")
        self.add_button.pack(pady=10)

        # Изменение цвета кнопки "Удалить Партнера" на серый
        self.delete_button = tk.Button(self.main_frame, text="Удалить Партнера", command=self.delete_partner, bg="gray", fg="white")
        self.delete_button.pack(pady=10)

        self.partner_list.bind("<Double-1>", self.edit_partner)

        self.update_partner_list()

    def delete_partner(self):
        """Удаление выбранного партнера."""
        selected_item = self.partner_list.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите партнера для удаления.")
            return

        partner_name = self.partner_list.item(selected_item[0], 'values')[0]  # Получаем имя выбранного партнера
        confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить партнера '{partner_name}'?")
        if confirm:
            partner_index = self.partner_list.index(selected_item[0])
            partner_id = self.partners[partner_index]['id']

            with self.conn:
                self.conn.execute("DELETE FROM partners WHERE id=?", (partner_id,))

            self.partners = self.load_partners()
            self.update_partner_list()

    def open_add_edit_form(self, partner=None):
        """Открытие формы для добавления или редактирования партнера."""
        self.form_window = tk.Toplevel(self.root)
        self.form_window.title("Добавление/Редактирование Партнера")
        self.form_window.geometry("600x450")
        self.form_window.configure(bg="#F4E8D3")

        self.name_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.rating_var = tk.IntVar()
        self.city_var = tk.StringVar()
        self.street_var = tk.StringVar()
        self.house_var = tk.StringVar()
        self.director_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        if partner:
            self.name_var.set(partner['name'])
            self.type_var.set(partner['type'])
            self.rating_var.set(partner['rating'])
            self.city_var.set(partner['address']['city'])
            self.street_var.set(partner['address']['street'])
            self.house_var.set(partner['address']['house'])
            self.director_var.set(partner['director'])
            self.phone_var.set(partner['phone'][2:]) 
            self.email_var.set(partner['email'])

        tk.Label(self.form_window, text="Наименование").pack()
        tk.Entry(self.form_window, textvariable=self.name_var).pack()

        tk.Label(self.form_window, text="Тип партнера").pack()
        self.type_combobox = ttk.Combobox(self.form_window, textvariable=self.type_var, values=["Тип 1", "Тип 2", "Тип 3"], state="readonly")
        self.type_combobox.pack()

        tk.Label(self.form_window, text="Рейтинг").pack()
        self.rating_entry = tk.Entry(self.form_window, textvariable=self.rating_var)
        self.rating_entry.pack()
        self.rating_entry.bind("<KeyRelease>", self.validate_rating)

        tk.Label(self.form_window, text="Город ").pack()
        tk.Entry(self.form_window, textvariable=self.city_var).pack()

        tk.Label(self.form_window, text="Улица ").pack()
        tk.Entry(self.form_window, textvariable=self.street_var).pack()

        tk.Label(self.form_window, text="Дом ").pack()
        self.house_entry = tk.Entry(self.form_window, textvariable=self.house_var)
        self.house_entry.pack()
        self.house_entry.bind("<KeyRelease>", self.validate_house)

        tk.Label(self.form_window, text="ФИО Директора").pack()
        tk.Entry(self.form_window, textvariable=self.director_var).pack()

        prefix_frame = tk.Frame(self.form_window)
        prefix_frame.pack()
        tk.Label(prefix_frame, text="+7").pack(side=tk.LEFT)
        
        self.phone_entry = tk.Entry(prefix_frame, textvariable=self.phone_var, width=15, validate="key")
        self.phone_entry.pack(side=tk.LEFT)
        self.phone_entry['validatecommand'] = (self.phone_entry.register(self.validate_phone_input), '%P')

        tk.Label(self.form_window, text="Email ").pack()
        tk.Entry(self.form_window, textvariable=self.email_var).pack()

        self.save_button = tk.Button(self.form_window, text="Сохранить", command=self.save_partner, bg="#67BA80")
        self.save_button.pack(pady=10)

        # Кнопка "Назад"
        self.back_button = tk.Button(self.form_window, text="Назад", command=self.form_window.destroy, bg="#FF9999")
        self.back_button.pack(pady=5)

    def validate_phone_input(self, new_value):
        """Валидация ввода номера телефона (максимум 9 цифр)."""
        if len(new_value) > 9:  
            return False
        if new_value.isdigit() or new_value == "":  
            return True
        return False

    def validate_rating(self, event):
        """Валидация рейтинга (0-100)."""
        try:
            value = int(self.rating_var.get())
            if value < 0:
                self.rating_var.set(0)
            elif value > 100:
                self.rating_var.set(100)
        except ValueError:
            self.rating_var.set(0)

    def validate_house(self, event):
        """Валидация номера дома (только положительные цифры)."""
        if not self.house_var.get().isdigit() and self.house_var.get() != "":
            self.house_var.set('')

    def validate_email(self):
        """Валидация email (должен содержать @ и .)."""
        email = self.email_var.get()
        if "@" not in email or "." not in email:
            return False
        return True

    def save_partner(self):
        """Сохранение данных о партнере."""
        name = self.name_var.get()
        partner_type = self.type_var.get()
        rating = self.rating_var.get()
        city = self.city_var.get()
        street = self.street_var.get()
        house = self.house_var.get()
        director = self.director_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()

        if len(name) < 1:
            messagebox.showerror("Ошибка", "Наименование должно содержать минимум 1 символ.")
            return
        if len(city) < 3:
            messagebox.showerror("Ошибка", "Город должен содержать минимум 3 символа.")
            return
        if len(street) < 3:
            messagebox.showerror("Ошибка", "Улица должна содержать минимум 3 символа.")
            return
        if not house.isdigit() or int(house) < 0:
            messagebox.showerror("Ошибка", "Дом должен содержать только положительные цифры.")
            return
        if len(phone) != 9 or not phone.isdigit():  
            messagebox.showerror("Ошибка", "Телефон должен содержать 9 цифр.")
            return
        if not self.validate_email():
            messagebox.showerror("Ошибка", "Email должен содержать @ и точку.")
            return

        new_partner = {
            'name': name,
            'type': partner_type,
            'rating': rating,
            'city': city,
            'street': street,
            'house': house,
            'director': director,
            'phone': f"+7{phone}",  
            'email': email
        }

        with self.conn:
            if hasattr(self, 'current_partner_index'):
                self.conn.execute('''
                    UPDATE partners SET name=?, type=?, rating=?, city=?, street=?, house=?, director=?, phone=?, email=?
                    WHERE id=?
                ''', (name, partner_type, rating, city, street, house, director, new_partner['phone'], email, self.partners[self.current_partner_index]['id']))
            else:
                self.conn.execute('''
                    INSERT INTO partners (name, type, rating, city, street, house, director, phone, email)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, partner_type, rating, city, street, house, director, new_partner['phone'], email))

        self.partners = self.load_partners()
        self.update_partner_list()
        self.form_window.destroy()

    def edit_partner(self, event):
        """Редактирование выбранного партнера."""
        selected_item = self.partner_list.selection()[0]
        partner_data = self.partner_list.item(selected_item, 'values')
        partner_index = self.partner_list.index(selected_item)
        
        partner = self.partners[partner_index] 
        self.current_partner_index = partner_index 
        self.open_add_edit_form(partner) 

    def update_partner_list(self):
        """Обновление списка партнеров в главном окне."""
        for item in self.partner_list.get_children():
            self.partner_list.delete(item)
        for partner in self.partners:
            self.partner_list.insert("", "end", values=(
                partner['name'],
                partner['type'],
                partner['rating'],
                partner['address']['city'],
                partner['address']['street'],
                partner['address']['house'],
                partner['director'],
                partner['phone'],
                partner['email']
            ))

    def on_closing(self):
        """Закрытие приложения и закрытие соединения с базой данных."""
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PartnerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
