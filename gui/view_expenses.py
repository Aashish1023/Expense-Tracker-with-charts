import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTKAgg
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
        category = row[1]
        amount = row[2]
        category_totals[category] = category_totals.get(category, 0) + amount

    fig, ax = plt.subplots(figsize =(5, 3))
    ax.bar(category_totals.keys(), category_totals.values(), color='skyblue')
    ax.set_tilte('Expenses by Category')
    ax.set_xlabel('Amount')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)


#Display the expenses results
print("\n All Expenses: \n")
print("{:<5} {:<15} {:<10} {:<15}".format("ID", "Category", "Amount", "Date"))
print("-" * 50)

for row in rows:
    print("{:<5} {:<15} {:<10} {:<15}".format(row[0], row[1], row[2], row[3]))


#GUI Setup
window = tk.Tk()
window.title("View Expenses")
window.geometry("700x500")

# Table Setup
columns = ("ID", "Date", "Category", "Amount", "Description")
tree = ttk.Treeview(window, columns=columns, show="headings")
for col in columns:
    tree.headings(col, text=col)
    tree.column(col, width="100")
tree.pack(pady=10, fill='x')

# Fetch and populate data
expense_data = fetcha_expenses()
populate_table(expense_data)
show_chart(expense_data)

window.mainloop()