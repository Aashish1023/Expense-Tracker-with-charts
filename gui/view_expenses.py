import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.db_connection import create_connection

def fetch_expenses():
    conn = create_connection()
    if not conn:
        return[]

    cursor = conn.cursor()
    cursor.execute("SELECT id, date, category, amount, description FROM expenses")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def populate_table(data):
    tree.delete(*tree.get_children())  # ✅ Clear existing rows
    for row in data:
        tree.insert('', 'end', values=row)  # ✅ Insert new rows

#Search function
def search_expenses():
    data = entry_search_date.get()
    category = entry_search_category.get()

    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if data:
        query += " AND date = %s"
        params.append(data)
    if category:
        query += " AND category LIKE %s"
        params.append('%s' + category + '%s')

    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    populate_table(results)

def delete_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a record to delete.")
        return
    
    record = tree.item(selected_item)["values"]
    record_id = record[0]  # Assuming the first column is the ID

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete record ID {record_id}?")
    if confirm:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = %s", (record_id,))
        conn.commit()
        cursor.close()
        conn.close()

        updated_data = fetch_expenses()
        populate_table(updated_data)

        messagebox.showinfo("Deleted", "Record deleted Successfully!")

#draw bar chart from data
def draw_bar_chart(data):
    category_totals = {}
    for row in data:
        print(row)  # Debug: See the structure
        id, date, category, amount, description = row  # Adjust if needed
        amount = float(amount)  # Convert string amount to number
        category_totals[category] = category_totals.get(category, 0) + amount

    categories = list(category_totals.keys())
    totals = list(category_totals.values())

    fig, ax = plt.subplots(figsize =(5, 3))
    ax.bar(category_totals.keys(), category_totals.values(), color='skyblue')
    ax.set_title('Expenses by Category')
    ax.set_xlabel('Amount')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

# Function to filter expenses based on date and category
def filter_expenses(date_filter=None, category_filter=None):
    conn = create_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    query = "SELECT id, date, category, amount, description FROM expenses WHERE 1=1"
    values = []

    if date_filter:
        query += " AND date = %s"
        values.append(date_filter)
    if category_filter:
        query += " AND category = %s"
        values.append(category_filter)

    cursor.execute(query, tuple(values))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def draw_pie_chart(data):
    category_totals = {}
    for row in data:
        category = row[2]
        amount = float(row[3])
        category_totals[category] = category_totals.get(category, 0) + amount

    labels = list(category_totals.keys())
    sizes = list(category_totals.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.set_title("Expenses by Category")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()



#GUI Setup
window = tk.Tk()
window.title("View Expenses")
window.geometry("700x500")

# Search Bar
search_frame = tk.Frame(window)
search_frame.pack(pady=10)

#date Entry
tk.Label(search_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
enter_search_date = tk.Entry(search_frame)
enter_search_date.grid(row=0, column=1, padx=5)

# Category Entry
tk.Label(search_frame, text="Category").grid(row=0, column=2, padx=5)
enter_search_category = ttk.Combobox(search_frame, values=["Food",  "Travel", "Shopping", "Bills", "Other"])
enter_search_category.grid(row=0, column=3, padx=5)

# Search Button
def on_search():
    date_val = entry_search_date.get().strip()
    category_val = enter_search_category.get().strip()
    filtered_date =filter_expenses(date_val if date_val else None, catgeory_val if category_val else None)
    populated_table(filtered_date)
    draw_bar_chart(filtered_date)

btn_search = tk.Button(search_frame, text="Search", command=on_search, bg="blue", fg="white")
btn_search.grid(row=0, column=4, padx=10)

# Table Setup
columns = ("ID", "Date", "Category", "Amount", "Description")
tree = ttk.Treeview(window, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width="100")
tree.pack(pady=10, fill='x')

# Buttons
btn_delete = tk.Button(window, text="Delete Selected", command=delete_record, bg="red", fg="white")
btn_delete.pack(pady=5)

# Fetch and populate data
expense_data = fetch_expenses()
populate_table(expense_data)
draw_bar_chart(expense_data)

window.mainloop()