import tkiner as tk
from tkinter import ttk, messagebox
import mysql.connector

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="expense_tracker"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
        return None


# Fetch expenses from the database
def fetch_filtered_expenses(date_filter=None, category_filter=None):
    conn = create_connection()
    if not conn:
        return[]
    
    cursor = conn.cursor()
    query = "SELECT id, date, category, amount, description FROM expenses WHERE 1=1"
    values = []

    if date_filter:
        query += " AND date = %s"
        values.append(date_filter)
    if category_filter:
        query += " AND category LIKE %s"
        values.append('%' + category_filter + '%')

    cursor, execute(query, tuple(values))
    date = cursor.fetchall()
    cursor.close()
    conn.close()
    return date

# Populate the Treeview with expenses
def populate_table(date):
    tree.delete(*tree.get_children())
    for row in date:
        tree.insert('', 'end', values=row)

#Search button action
def search_expenses():
    date = entry_search_date.get().strip()
    category = entry_category.get().strip()
    data = fetch_filtered_expenses(date, category)
    populate_table(data)