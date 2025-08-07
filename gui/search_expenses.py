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