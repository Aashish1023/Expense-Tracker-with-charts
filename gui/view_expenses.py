import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.db_connection import create_connection

def fetcha_expenses():
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
    for row in tree.get_children():
        tree.insert(row)
    for row in data:
        tree.insert("", "end", values=row)

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

#GUI Setup
window = tk.Tk()
window.title("View Expenses")
window.geometry("700x500")

# Table Setup
columns = ("ID", "Date", "Category", "Amount", "Description")
tree = ttk.Treeview(window, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width="100")
tree.pack(pady=10, fill='x')

# Fetch and populate data
expense_data = fetcha_expenses()
populate_table(expense_data)
draw_bar_chart(expense_data)

window.mainloop()