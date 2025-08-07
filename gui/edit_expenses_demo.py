import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Create sample DB and table for demo
def setup_database():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    ''')
    # Sample data
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES ('2025-08-01', 'Food', 20.5, 'Lunch')")
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES ('2025-08-02', 'Travel', 50, 'Bus Ticket')")
    conn.commit()
    conn.close()

# Fetch all expenses
def fetch_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()
    conn.close()
    return data

# Populate the Treeview
def populate_table(data):
    tree.delete(*tree.get_children())
    for row in data:
        tree.insert('', 'end', values=row)

# Update record in DB
def update_record(record_id, new_data):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses
        SET date = ?, category = ?, amount = ?, description = ?
        WHERE id = ?
    """, (new_data['date'], new_data['category'], new_data['amount'], new_data['description'], record_id))
    conn.commit()
    conn.close()

# Open edit popup
def edit_record():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Select a record to edit.")
        return

    record = tree.item(selected[0], 'values')
    record_id = record[0]

    edit_win = tk.Toplevel(window)
    edit_win.title("Edit Record")

    tk.Label(edit_win, text="Date").grid(row=0, column=0)
    entry_date = tk.Entry(edit_win)
    entry_date.insert(0, record[1])
    entry_date.grid(row=0, column=1)

    tk.Label(edit_win, text="Category").grid(row=1, column=0)
    entry_category = tk.Entry(edit_win)
    entry_category.insert(0, record[2])
    entry_category.grid(row=1, column=1)

    tk.Label(edit_win, text="Amount").grid(row=2, column=0)
    entry_amount = tk.Entry(edit_win)
    entry_amount.insert(0, record[3])
    entry_amount.grid(row=2, column=1)

    tk.Label(edit_win, text="Description").grid(row=3, column=0)
    entry_desc = tk.Entry(edit_win)
    entry_desc.insert(0, record[4])
    entry_desc.grid(row=3, column=1)

    def save_changes():
        updated = {
            'date': entry_date.get(),
            'category': entry_category.get(),
            'amount': float(entry_amount.get()),
            'description': entry_desc.get()
        }
        update_record(record_id, updated)
        populate_table(fetch_expenses())
        edit_win.destroy()
        messagebox.showinfo("Success", "Record updated!")

    tk.Button(edit_win, text="Save", command=save_changes, bg='green', fg='white').grid(row=4, columnspan=2, pady=10)

# --- Main Window ---
window = tk.Tk()
window.title("Edit Expense Records")
window.geometry("600x400")

# Table
columns = ("ID", "Date", "Category", "Amount", "Description")
tree = ttk.Treeview(window, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill='both', expand=True)

# Buttons
tk.Button(window, text="Edit Selected", command=edit_record, bg="blue", fg="white").pack(pady=10)

# Initialize and display
setup_database()
populate_table(fetch_expenses())
window.mainloop()
