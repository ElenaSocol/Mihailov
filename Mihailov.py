import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x500")
        
        self.expenses = self.load_data()

        # Поля ввода
        frame_input = tk.Frame(root, pady=10)
        frame_input.pack()

        tk.Label(frame_input, text="Сумма:").grid(row=0, column=0)
        self.entry_amount = tk.Entry(frame_input)
        self.entry_amount.grid(row=0, column=1)

        tk.Label(frame_input, text="Категория:").grid(row=0, column=2)
        self.combo_category = ttk.Combobox(frame_input, values=["Еда", "Транспорт", "Развлечения", "Другое"])
        self.combo_category.grid(row=0, column=3)

        tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0)
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.grid(row=1, column=1)

        btn_add = tk.Button(frame_input, text="Добавить расход", command=self.add_expense)
        btn_add.grid(row=1, column=3, sticky="we")

        # Фильтры
        frame_filters = tk.LabelFrame(root, text="Фильтрация и Итоги", padx=10, pady=5)
        frame_filters.pack(fill="x", padx=10)

        tk.Label(frame_filters, text="С:").grid(row=0, column=0)
        self.filter_start = tk.Entry(frame_filters, width=12)
        self.filter_start.grid(row=0, column=1)

        tk.Label(frame_filters, text="По:").grid(row=0, column=2)
        self.filter_end = tk.Entry(frame_filters, width=12)
        self.filter_end.grid(row=0, column=3)

        btn_filter = tk.Button(frame_filters, text="Применить", command=self.update_table)
        btn_filter.grid(row=0, column=4, padx=5)

        self.label_total = tk.Label(frame_filters, text="Итого: 0", font=('Arial', 10, 'bold'))
        self.label_total.grid(row=0, column=5, padx=20)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Дата", "Категория", "Сумма"), show='headings')
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_table()

    def add_expense(self):
        amount = self.entry_amount.get()
        category = self.combo_category.get()
        date_str = self.entry_date.get()

        # Валидация
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность суммы (>0) и даты (ГГГГ-ММ-ДД)")
            return

        if not category:
            messagebox.showwarning("Внимание", "Выберите категорию")
            return

        self.expenses.append({"date": date_str, "category": category, "amount": amount})
        self.save_data()
        self.update_table()
        self.entry_amount.delete(0, tk.END)

    def update_table(self):
        # Очистка
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        total = 0
        start_d = self.filter_start.get()
        end_d = self.filter_end.get()

        for exp in self.expenses:
            # Логика фильтрации по дате
            if start_d and exp['date'] < start_d: continue
            if end_d and exp['date'] > end_d: continue
            
            self.tree.insert("", tk.END, values=(exp['date'], exp['category'], exp['amount']))
            total += exp['amount']
        
        self.label_total.config(text=f"Итого: {total:.2f}")

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False)

    def load_data(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()

    
