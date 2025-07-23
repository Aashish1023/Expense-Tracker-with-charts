import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="your_mysql_user",
    password="your_mysql_password",
    database="expenses_tracker"
)

cursor = conn.cursor()

# Create the expenses table if it doesn't exist
cursor.execute("SELECT id, category, amount, data FROM expenses ORDER BY date DESC")
rows = cursor.fetchall()

#Display the expenses results
print("\n All Expenses: \n")
print("{:<5} {:<15} {:<10} {:<15}".format("ID", "Category", "Amount", "Date"))
print("-" * 50)

for row in rows:
    print("{:<5} {:<15} {:<10} {:<15}".format(row[0], row[1], row[2], row[3]))


#clean up
cursor.close()
conn.close()