import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox
from utils.db_connection import create_connection
import datetime

def add_expense():
   date = entry_date.get()
   category = entry_category.get()
   amount = entry_amount.get()
   description = entry_description.get()
   # category = input("enter expense category(E.g. Food, Transport): ")
   # amount = input("enter expense amount: ")
   # date = input("Enter expense date (YYYY-MM-DD): ")
     
   if not (date and category and amount):
      messagebox.showerror("Missing Info", "Please fill in all fields.")
      return
      #  date = datetime.date.today().strftime('%Y-%m-%d')

try: # Connect to the database
   amount = float(amount)
   conn = create_connection()
   cursor = conn.cursor()
   cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)", (date, category, amount, description))
   
   conn.commit()
   cursor.close()
   conn.close()
   messagebox.showinfo("Success", "Expense added successfully!")
   entry_date.delete(0, tk.END)
   entry_category.delete(0, tk.END)
   entry_amount.delete(0, tk.END)
   entry_description.delete(0, tk.END)
except Exception as e:
   messagebox.showerror("Error", str(e))