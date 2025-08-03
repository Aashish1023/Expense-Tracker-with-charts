import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import Label, messagebox
from utils.db_connection import create_connection
# import datetime

def add_expense():
   date = entry_date.get()
   category = entry_category.get()
   amount_str = entry_amount.get()
   description = entry_description.get()
   # category = input("enter expense category(E.g. Food, Transport): ")
   # amount = input("enter expense amount: ")
   # date = input("Enter expense date (YYYY-MM-DD): ")
     
   if not (date and category and amount_str):
      messagebox.showerror("Missing Info", "Please fill in all fields.")
      return
      #  date = datetime.date.today().strftime('%Y-%m-%d')

   try: # Connect to the database
      amount = float(amount_str)
      conn = create_connection()
      if conn is None:
         raise Exception("Failed to connect to the database.")
      cursor = conn.cursor()
      cursor.execute(
         "INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)", 
         (date, category, amount, description)
         )
      
      conn.commit()
      print("Expenses Add successfully!")
      cursor.close()
      conn.close()
      messagebox.showinfo("Success", "Expense added successfully!")
      entry_date.delete(0, tk.END)
      entry_category.delete(0, tk.END)
      entry_amount.delete(0, tk.END)
      entry_description.delete(0, tk.END)
   except Exception as e:
      messagebox.showerror("Error Occured:", str(e))

# GUI Setup
window = tk.Tk()
window.title("Add Expense")
window.geometry("400x300")

tk,Label(window, text="Date (YYYY-MM-DD):").pack()
entry_date = tk.Entry(window)
entry_date.pack()

tk.Label(window, text="Category:").pack()
entry_category = tk.Entry(window)   
entry_category.pack()

tk.Label(window, text="Amount:").pack()
entry_amount = tk.Entry(window)
entry_amount.pack()

tk.Label(window, text="Description:").pack()
entry_description = tk.Entry(window)
entry_description.pack()

tk.Button(window, text="Add Expense", command=add_expense).pack(pady=10)

window.mainloop()
