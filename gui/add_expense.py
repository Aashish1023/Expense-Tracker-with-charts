def add_expense(amount, category, date, note):
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO expenses (amount, category, date, note) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (amount, category, date, note)) 
    db.commit()
    db.close()