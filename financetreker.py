import tkinter as tk 
from tkinter import ttk
import json

#Settings
TEXT_STYLE = {"font": ("Arial", 16)}
BUTTON_STYLE = {"font": ("Arial", 12)}

#Root
root = tk.Tk()
root.geometry("900x350")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#Function
def show_page(page):
    page.tkraise()

# StartPage
startpage = tk.Frame(root)
startpage.grid(row=0, column=0, sticky="nsew")

startpage.grid_columnconfigure(0, weight=1)

tk.Label(startpage, text="Финансовый трекер", **TEXT_STYLE).grid(row=0, column=0, pady=20)

tk.Button(startpage, text="Добавить операцию", **BUTTON_STYLE, command=lambda: show_page(add_operation)).grid(row=1, column=0, pady=20)

tk.Button(startpage, text="Просмотреть операции", **BUTTON_STYLE, command=lambda: show_page(show_operation)).grid(row=2, column=0, pady=20)

tk.Button(startpage, text="Аналитика и Статистика", **BUTTON_STYLE, command=lambda: show_page(analytics_statistics)).grid(row=3, column=0, pady=20)

tk.Button(startpage, text="Поиск", **BUTTON_STYLE, command=lambda: show_page(search_operation)).grid(row=4, column=0, pady=20)

# AddOperation
add_operation = tk.Frame(root)
add_operation.grid(row=0, column=0, sticky="nsew")

add_operation.grid_columnconfigure(0, weight=1)

tk.Button(add_operation, text="Назад", **BUTTON_STYLE, command=lambda: show_page(startpage)).grid(row=0, column=0, padx=0, sticky="w")

tk.Label(add_operation, text="Доход/Расход:", **TEXT_STYLE).grid(row=1, column=0, padx=150, sticky="w")
operation = ["Доход", "Расход"]
operation_type = ttk.Combobox(add_operation, values=operation)
operation_type.grid(row=1, column=0, pady=20)

tk.Label(add_operation, text="Сумма:", **TEXT_STYLE).grid(row=2, column=0, padx=150, sticky="w")
amount_entry = tk.Entry(add_operation)
amount_entry.grid(row=2, column=0, padx=150)

tk.Label(add_operation, text="Категория:", **TEXT_STYLE).grid(row=3, column=0, padx=150, sticky="w")
category = ["Еда", "Транспорт", "Развлечения", "Путешествия"]
cat = ttk.Combobox(add_operation, values=category)
cat.grid(row=3, column=0, pady=20)

tk.Label(add_operation, text="Описание:", **TEXT_STYLE).grid(row=4, column=0, padx=150, sticky="w")
description_entry = tk.Entry(add_operation)
description_entry.grid(row=4, column=0, padx=150)

def save_operation():
   data = {"operations": []}
   
   try:
     with open("finance.json", "r", encoding="utf-8") as f:
        data = json.load(f)
   except FileNotFoundError:
      pass
   
   new_operation = {
    "id": len(data["operations"]) + 1,
    "type": operation_type.get(),
    "amount": amount_entry.get(),
    "category": cat.get(),
    "description": description_entry.get()
   }

   data["operations"].append(new_operation)

   with open("finance.json", "w", encoding="utf-8") as f:
      json.dump(data, f, ensure_ascii=False, indent=2)

   show_page(startpage)

tk.Button(add_operation, text="Сохранить", **BUTTON_STYLE, command=save_operation).grid(row=5, column=0, padx=0)

#ShowOperation
show_operation = tk.Frame(root)
show_operation.grid(row=0, column=0, sticky="nsew")

show_operation.grid_columnconfigure(0, weight=1)

tk.Button(show_operation, text="Назад", **BUTTON_STYLE, command=lambda: show_page(startpage)).grid(row=0, column=0, padx=0, sticky="w")

tk.Label(show_operation, text="История Операций", **TEXT_STYLE).grid(row=1, column=0)

try:
   with open("finance.json", "r", encoding="utf-8") as f:
      data = json.load(f)
      all_ops = data.get("operations", [])
except FileNotFoundError:
      all_ops = []

last10 = all_ops[-10:]

for i, op in enumerate(last10, start=2):
   text= f"{op['id']}.{op['type']}.{op['amount']}.{op['category']}.{op['description']}"
   tk.Label(show_operation, text=text).grid(row=i, column=0)

#AnaliticStatisticstk 
analytics_statistics = tk.Frame(root)
analytics_statistics.grid(row=0, column=0, sticky="nsew")
table_frame = tk.Frame(analytics_statistics)
table_frame.grid(row=1, column=0, sticky="nsew", pady=10)

analytics_statistics.grid_columnconfigure(0, weight=1)
analytics_statistics.grid_rowconfigure(1, weight=1)

tk.Button(analytics_statistics, text="Назад", **BUTTON_STYLE, command=lambda: show_page(startpage)).grid(row=0, column=0, padx=0, sticky="w")

tk.Label(analytics_statistics, text="Аналитика и статистика", **TEXT_STYLE).grid(row=0, column=0, pady=10)

scrollbar = tk.Scrollbar(table_frame, orient="vertical")
scrollbar.grid(row=0, column=0, sticky="e")

try:
   with open('finance.json', "r", encoding="utf-8") as f:
      data = json.load(f)
      all_operation = data.get("operations", [])
except FileNotFoundError:
   all_operation = []
    
columns = ["id", "type", "amount", "category", "description"]

tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
tree.grid(row=1, column=0, pady=20, sticky="nsew")
scrollbar.config(command=tree.yview)

tree.heading("id", text="ID")
tree.heading("type", text="Тип")
tree.heading("amount", text="Сумма")
tree.heading("category", text="Категория")
tree.heading("description", text="Описание")

tree.column("id", width=50, anchor="center")
tree.column("type", width=100)
tree.column("amount", width=100)
tree.column("category", width=150)
tree.column("description", width=200)

try:
   with open('finance.json', "r", encoding="utf-8") as f:
      data = json.load(f)
      all_operation = data.get("operations", [])
except FileNotFoundError:
   all_operation = []

for op in all_operation:
   tree.insert("", "end", values = (op.get("id"), op.get("type"), op.get("amount"), op.get("category"), op.get("description")))

total_income = sum(float(op.get("amount", 0)) for op in all_operation if op.get("type") == "Расход")
tk.Label(analytics_statistics, text=f"Всего потрачено: {total_income}", **TEXT_STYLE).grid(row=2, column=0, pady=10)

total_expenditure = sum(float(op.get("amount", 0)) for op in all_operation if op.get("type") == "Доход")
tk.Label(analytics_statistics, text=f"Всего заработано: {total_expenditure}", **TEXT_STYLE).grid(row=3, column=0, pady=10)

#Search
search_operation = tk.Frame(root)
search_operation.grid(row=0, column=0, sticky="nsew")
results_frame = tk.Frame(search_operation)
results_frame.grid(row=5, column=0, pady=10, sticky="nsew")

search_operation.grid_columnconfigure(0, weight=1)

tk.Button(search_operation, text="Назад", **BUTTON_STYLE, command=lambda: show_page(startpage)).grid(row=0, column=0, padx=0, sticky="w")

tk.Label(search_operation, text="Поиск", ** TEXT_STYLE).grid(row=0, column=0, pady=40)

tk.Label(search_operation, text="Введите слово для поиска:", **TEXT_STYLE).grid(row=1, column=0, sticky="w")
word_search = tk.Entry(search_operation)
word_search.grid(row=1, column=0, padx=20)

def search_operations():
   for widget in results_frame.winfo_children():
      widget.destroy()
      
   word = word_search.get().lower()

   try:
      with open('finance.json', "r", encoding="utf-8") as f:
         data = json.load(f)
         operations = data.get("operations", [])
   except FileNotFoundError:
      return
   
   found = False

   for op in operations:
      description = op.get("description", "").lower()
      if word in description:
         text = (
            f"{op.get('id')}."
            f"{op.get('type')} |"
            f"{op.get('amount')} |"
            f"{op.get('category')} |"
            f"{op.get('description')}"
         )

         tk.Label(results_frame, text=text, anchor="w", justify="left").grid(row=5, column=0, pady=10)

         found = True

   if not found:
      tk.Label(results_frame, text="Ничего не найдено", fg="grey").grid(row=5, column=0, pady=10)

word_safe = tk.Button(search_operation, text="Поиск", **BUTTON_STYLE, command=search_operations)
word_safe.grid(row=2, column=0, pady=40)

startpage.tkraise()
root.mainloop()