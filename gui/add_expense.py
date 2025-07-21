from utils.db_connection import create_connection
import datetime

def add_expense():
   category = input("enter expense category(E.g. Food, Transport): ")
   amount = input("enter expense amount: ")
   date = input("Enter expense date (YYYY-MM-DD): ")
     
   if not date:
       date = datetime.date.today().strftime('%Y-%m-%d')

   conn = create_connection()
   if conn:
      cursor = conn.cursor()
      try:
         cursor.execute("
                        INSERT INTO expenses (category, amount, date)
                        VAULES (%s, %s, %s),(category, amount, date)")         conn.commit()
         print("Expense added successfully.")
      except Exception as e:
         print(f"An error occurred: {e}")
      finally:
         cursor.close()
         conn.close()
   else:
      print("Failed to connect to the database.")


    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO expenses (amount, category, date, note) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (amount, category, date, note)) 
    db.commit()
    db.close()