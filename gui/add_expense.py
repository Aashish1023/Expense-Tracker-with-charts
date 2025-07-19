def add_expense():
    category = input("enter expense category(E.g. Food, Transport): ")
    amount = input("enter expense amount: ")
    date = input("Enter expense date (YYYY-MM-DD): ")
     
    if not date:
       date = datetime.date.today().strftime('%Y-%m-%d')

    
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO expenses (amount, category, date, note) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (amount, category, date, note)) 
    db.commit()
    db.close()